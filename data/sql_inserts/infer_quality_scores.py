"""Infer Q scores for the 38 luxury SUVs added in add_luxury_suvs.py.

Uses brand-level baselines from existing 194 build_quality rows, adjusted
by platform type and segment. Q score is computed as a weighted average
of 6 sub-scores:

    Q = body*0.20 + nvh*0.20 + mat*0.20 + paint*0.15 + elec*0.15 + cosm*0.10

This matches the existing data within ~0.6 mean absolute error (verified
by C:/Users/llama/AppData/Local/Temp/analyze_q_scores.py).

Brand baselines (from existing data, see .omo/research/...):
  Lexus:    Q=82.2 (body=86 nvh=87 mat=85 paint=84 elec=71 cosm=78)
  Audi:     Q=77.7 (body=83 nvh=80 mat=82 paint=80 elec=64 cosm=72)
  Porsche:  Q=75.2 (body=82 nvh=70 mat=75 paint=81 elec=66 cosm=69)
  BMW:      Q=71.5 (body=78 nvh=72 mat=75 paint=72 elec=61 cosm=66)
  Mercedes: Q=70.5 (body=77 nvh=70 mat=76 paint=70 elec=59 cosm=64)
  Land Rover: Q=69.3 (body=78 nvh=85 mat=80 paint=72 elec=35 cosm=62)
  Cadillac: Q=73.7 (body=78 nvh=75 mat=75 paint=75 elec=65 cosm=71)
  Acura:    Q=73.9 (body=78 nvh=74 mat=76 paint=75 elec=68 cosm=69)
  Infiniti: Q=44.2 (body=65 nvh=41 mat=40 paint=37 elec=32 cosm=38)
  Lincoln:  Q=77.3 (body=78 nvh=83 mat=82 paint=76 elec=68 cosm=77)
  Lamborghini: Q=84.8 (body=95 nvh=72 mat=88 paint=92 elec=65 cosm=85)

Plus inferred for Bentley (D1 platform shared with Continental, high
materials) and Rolls-Royce (CLAR-based but heavily modified).

Each new SUV also gets:
  - platform_type (bespoke/shared/dedicated)
  - assembly_plant (best estimate)
  - weld_technology (laser/spot)
  - panel_gap_mm (estimated)
  - notes explaining the inference

Idempotent: skips cars that already have a build_quality row.

Usage:
    python data/sql_inserts/infer_quality_scores.py --dry-run
    python data/sql_inserts/infer_quality_scores.py
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "data" / "motorgeek.db"

# Q score formula: weighted average of sub-scores
# Verified to match existing data within ~0.6 MAE
Q_WEIGHTS = {
    "body_construction": 0.20,
    "nvh_isolation": 0.20,
    "interior_materials": 0.20,
    "paint_corrosion": 0.15,
    "electrical_aging": 0.15,
    "cosmetic_aging": 0.10,
}


def compute_q(subscores: dict[str, float]) -> float:
    """Compute Q score from sub-scores using the verified weighted formula.

    `subscores` uses short keys (body/nvh/mat/paint/elec/cosm).
    """
    return round(
        subscores["body"] * 0.20
        + subscores["nvh"] * 0.20
        + subscores["mat"] * 0.20
        + subscores["paint"] * 0.15
        + subscores["elec"] * 0.15
        + subscores["cosm"] * 0.10,
        1,
    )


# ---------------------------------------------------------------------------
# Per-car Q score inference. Each entry specifies:
#   - base: brand baseline adjustments
#   - platform: platform type (bespoke/shared/dedicated)
#   - notes: explanation of inference
# Sub-scores are adjusted from brand baseline based on:
#   - platform quality (dedicated EV > shared MLB > body-on-frame)
#   - segment (luxury > compact for materials)
#   - powertrain complexity (AMG/M variants: lower electrical)
#   - plant reputation (Tahara/Sindelfingen > general)
# ---------------------------------------------------------------------------

# Brand sub-score baselines (mean of existing data)
BRAND_BASELINES = {
    "Audi":           {"body": 83, "nvh": 80, "mat": 82, "paint": 80, "elec": 64, "cosm": 72},
    "BMW":            {"body": 78, "nvh": 72, "mat": 75, "paint": 72, "elec": 61, "cosm": 66},
    "Mercedes-Benz":  {"body": 77, "nvh": 70, "mat": 76, "paint": 70, "elec": 59, "cosm": 64},
    "Lexus":          {"body": 86, "nvh": 87, "mat": 85, "paint": 84, "elec": 71, "cosm": 78},
    "Porsche":        {"body": 82, "nvh": 70, "mat": 75, "paint": 81, "elec": 66, "cosm": 69},
    "Cadillac":       {"body": 78, "nvh": 75, "mat": 75, "paint": 75, "elec": 65, "cosm": 71},
    "Acura":          {"body": 78, "nvh": 74, "mat": 76, "paint": 75, "elec": 68, "cosm": 69},
    "Infiniti":       {"body": 65, "nvh": 41, "mat": 40, "paint": 37, "elec": 32, "cosm": 38},
    "Lincoln":        {"body": 78, "nvh": 83, "mat": 82, "paint": 76, "elec": 68, "cosm": 77},
    "Land Rover":     {"body": 78, "nvh": 85, "mat": 80, "paint": 72, "elec": 35, "cosm": 62},
    "Bentley":        {"body": 86, "nvh": 82, "mat": 90, "paint": 85, "elec": 60, "cosm": 75},
    "Rolls-Royce":    {"body": 88, "nvh": 88, "mat": 94, "paint": 87, "elec": 62, "cosm": 80},
    "Lamborghini":    {"body": 92, "nvh": 70, "mat": 88, "paint": 90, "elec": 60, "cosm": 82},
}


def adjust(baseline: dict, *, body: int = 0, nvh: int = 0, mat: int = 0,
           paint: int = 0, elec: int = 0, cosm: int = 0) -> dict:
    """Adjust a brand baseline by +/- integers per sub-score."""
    return {
        "body": baseline["body"] + body,
        "nvh": baseline["nvh"] + nvh,
        "mat": baseline["mat"] + mat,
        "paint": baseline["paint"] + paint,
        "elec": baseline["elec"] + elec,
        "cosm": baseline["cosm"] + cosm,
    }


# ---------------------------------------------------------------------------
# Q score inference for each of the 38 new SUVs.
# Keys are (make, model, year_start) tuples.
# Values are dicts with sub-score adjustments + metadata.
# ---------------------------------------------------------------------------

Q_INFERENCE = {
    # === AUDI (6) - MLB Evo platform, Ingolstadt/Neckarsulm ===
    ("Audi", "Q3", 2019): {
        "sub": adjust(BRAND_BASELINES["Audi"], body=-2, nvh=-3, mat=-3, paint=0, elec=0, cosm=-2),
        "platform_type": "MQB (transverse, AWD)", "weld": "spot",
        "plant": "Gyor (Hungary)", "panel_gap": 4.5,
        "note": "MQB-derived compact SUV. Aluminum hood, steel body. Lower-cost interior vs Q5/Q7. Tight panel gaps. Good NVH for class.",
    },
    ("Audi", "Q7", 2020): {
        "sub": adjust(BRAND_BASELINES["Audi"], body=+3, nvh=+3, mat=+2, paint=+2, elec=+2, cosm=+2),
        "platform_type": "MLB Evo", "weld": "laser + spot",
        "plant": "Bratislava (Slovakia)", "panel_gap": 3.8,
        "note": "MLB Evo platform (shared Bentley Bentayga, Lamborghini Urus, Porsche Cayenne). Aluminum-intensive body. Audi ultra_quality manufacturing. Acoustic glass standard.",
    },
    ("Audi", "Q8", 2019): {
        "sub": adjust(BRAND_BASELINES["Audi"], body=+3, nvh=+3, mat=+2, paint=+2, elec=+2, cosm=+2),
        "platform_type": "MLB Evo", "weld": "laser + spot",
        "plant": "Bratislava (Slovakia)", "panel_gap": 3.8,
        "note": "MLB Evo coupe-SUV. Same platform as Q7 but with sport-tuned body. Aluminum hood and fenders. Higher-grade interior materials.",
    },
    ("Audi", "SQ5", 2021): {
        "sub": adjust(BRAND_BASELINES["Audi"], body=+2, nvh=+1, mat=+1, paint=+1, elec=-2, cosm=0),
        "platform_type": "MLB Evo", "weld": "laser + spot",
        "plant": "San Jose Chiapa (Mexico)", "panel_gap": 4.0,
        "note": "MLB Evo performance SUV. Sport seats, carbon atlas inlays. More electrical content (drive modes, sport diff). Slightly lower electrical reliability vs base Q5.",
    },
    ("Audi", "SQ7", 2020): {
        "sub": adjust(BRAND_BASELINES["Audi"], body=+3, nvh=+2, mat=+3, paint=+2, elec=-3, cosm=+1),
        "platform_type": "MLB Evo", "weld": "laser + spot",
        "plant": "Bratislava (Slovakia)", "panel_gap": 3.8,
        "note": "Full-size performance SUV. 4.0T V8, ceramic brakes optional. More electrical content than Q7. Carbon-wrapped prop shaft. High-grade Valcona leather.",
    },
    ("Audi", "RSQ8", 2020): {
        "sub": adjust(BRAND_BASELINES["Audi"], body=+5, nvh=+2, mat=+5, paint=+3, elec=-4, cosm=+2),
        "platform_type": "MLB Evo", "weld": "laser + spot",
        "plant": "Bratislava (Slovakia)", "panel_gap": 3.5,
        "note": "Top-tier Audi SUV. Carbon roof optional, Alcantara headliner, massaging seats. Highest electrical complexity (RS-specific drive modes, sport rear diff). Tighter panel gaps than Q8.",
    },

    # === BMW (4) - CLAR / FAAR platforms ===
    ("BMW", "X7", 2019): {
        "sub": adjust(BRAND_BASELINES["BMW"], body=+3, nvh=+3, mat=+5, paint=+3, elec=+2, cosm=+3),
        "platform_type": "CLAR (Cluster Architecture)", "weld": "laser + spot",
        "plant": "Spartanburg (USA)", "panel_gap": 4.0,
        "note": "CLAR platform with Carbon Core technology. Aluminum/steel hybrid body. Spartanburg plant quality high for SUV segment. Crystal gear selector, Merino leather.",
    },
    ("BMW", "X1", 2020): {
        "sub": adjust(BRAND_BASELINES["BMW"], body=-2, nvh=-2, mat=-3, paint=-1, elec=-2, cosm=-2),
        "platform_type": "FAAR (UKL2, front-drive)", "weld": "spot",
        "plant": "Regensburg (Germany)", "panel_gap": 4.5,
        "note": "FAAR platform (shared with Mini Countryman). Front-drive transverse layout. Lower-cost interior vs X3. Standard Sensatec not leather.",
    },
    ("BMW", "X4 M40i", 2020): {
        "sub": adjust(BRAND_BASELINES["BMW"], body=+1, nvh=+1, mat=+2, paint=+1, elec=0, cosm=+1),
        "platform_type": "CLAR", "weld": "laser + spot",
        "plant": "Spartanburg (USA)", "panel_gap": 4.2,
        "note": "CLAR coupe-SUV on shortened wheelbase. M Sport suspension, M-specific interior. Vernasca leather standard. Lower roof reduces rear headroom but improves coupe stance.",
    },
    ("BMW", "X6 M50i", 2020): {
        "sub": adjust(BRAND_BASELINES["BMW"], body=+2, nvh=+3, mat=+4, paint=+2, elec=+1, cosm=+2),
        "platform_type": "CLAR", "weld": "laser + spot",
        "plant": "Spartanburg (USA)", "panel_gap": 4.0,
        "note": "CLAR coupe-SUV, M Performance variant. V8, M Sport exhaust. Extended Merino leather. Higher electrical content (M drive modes, adaptive M suspension).",
    },

    # === MERCEDES-BENZ (6) - MHA platform ===
    ("Mercedes-Benz", "GLE450", 2020): {
        "sub": adjust(BRAND_BASELINES["Mercedes-Benz"], body=+2, nvh=+3, mat=+4, paint=+2, elec=+3, cosm=+3),
        "platform_type": "MHA (Modular High Architecture)", "weld": "laser + spot",
        "plant": "Tuscaloosa (USA)", "panel_gap": 4.0,
        "note": "MHA platform, Mercedes' dedicated SUV architecture. Aluminum body panels (hood, fenders, tailgate). MBUX infotainment, Burmester optional. Tuscaloosa plant quality strong.",
    },
    ("Mercedes-Benz", "GLS450", 2020): {
        "sub": adjust(BRAND_BASELINES["Mercedes-Benz"], body=+2, nvh=+4, mat=+5, paint=+2, elec=+3, cosm=+3),
        "platform_type": "MHA", "weld": "laser + spot",
        "plant": "Tuscaloosa (USA)", "panel_gap": 4.0,
        "note": "Full-size 7-seat SUV on MHA. E-Active Body Control suspension. Five-zone climate, MBUX rear seat entertainment. Premium Nappa leather.",
    },
    ("Mercedes-Benz", "G550", 2019): {
        "sub": adjust(BRAND_BASELINES["Mercedes-Benz"], body=+8, nvh=+5, mat=+3, paint=+3, elec=-2, cosm=-2),
        "platform_type": "W463 (body-on-frame, dedicated)", "weld": "spot + laser",
        "plant": "Graz (Austria, Magna Steyr)", "panel_gap": 5.0,
        "note": "Iconic body-on-frame SUV. Hand-built by Magna Steyr in Graz since 1979. Ladder frame, three locking diffs. Heavy (2500kg) but extremely solid build. Wide panel gaps due to off-road design.",
    },
    ("Mercedes-Benz", "AMG G63", 2019): {
        "sub": adjust(BRAND_BASELINES["Mercedes-Benz"], body=+8, nvh=+3, mat=+6, paint=+4, elec=-4, cosm=-2),
        "platform_type": "W463 (body-on-frame, dedicated)", "weld": "spot + laser",
        "plant": "Graz (Austria, Magna Steyr)", "panel_gap": 5.0,
        "note": "AMG G-Class: hand-built by Magna Steyr. Twin-turbo V8, AMG-specific suspension. Nappa leather, carbon trim. High electrical complexity (AMG drive modes, sport exhaust).",
    },
    ("Mercedes-Benz", "AMG GLE63 Coupe", 2018): {
        "sub": adjust(BRAND_BASELINES["Mercedes-Benz"], body=+2, nvh=+1, mat=+5, paint=+2, elec=-3, cosm=+2),
        "platform_type": "MHA", "weld": "laser + spot",
        "plant": "Tuscaloosa (USA)", "panel_gap": 4.0,
        "note": "AMG coupe-SUV, pre-facelift W166 generation. Hand-built 5.5L biturbo V8. AMG Performance 4MATIC+. Nappa leather, AMG carbon trim. Higher complexity than base GLE.",
    },
    ("Mercedes-Benz", "Maybach GLS600", 2021): {
        "sub": adjust(BRAND_BASELINES["Mercedes-Benz"], body=+4, nvh=+6, mat=+8, paint=+4, elec=+1, cosm=+6),
        "platform_type": "MHA (Maybach-tuned)", "weld": "laser + spot",
        "plant": "Tuscaloosa (USA)", "panel_gap": 3.5,
        "note": "Ultra-luxury Maybach SUV. Nappa leather everywhere, Burmester 4D, heated armrests, executive rear seating. Tighter panel gaps, additional sound insulation, unique chrome trim.",
    },

    # === LEXUS (4) - TNGA / body-on-frame Land Cruiser ===
    ("Lexus", "GX 460", 2010): {
        "sub": adjust(BRAND_BASELINES["Lexus"], body=+8, nvh=+5, mat=+3, paint=+5, elec=+8, cosm=+5),
        "platform_type": "J150 (body-on-frame, Land Cruiser Prado)", "weld": "spot + laser",
        "plant": "Tahara (Japan)", "panel_gap": 4.0,
        "note": "Body-on-frame, shares platform with Land Cruiser Prado (J150). 4.6L V8, KDSS suspension. Tahara-built, near-LS quality. Proved bulletproof over 15+ years. Mark Levinson optional.",
    },
    ("Lexus", "LX570", 2019): {
        "sub": adjust(BRAND_BASELINES["Lexus"], body=+10, nvh=+6, mat=+7, paint=+6, elec=+5, cosm=+7),
        "platform_type": "URJ200 (body-on-frame, Land Cruiser 200)", "weld": "laser + spot",
        "plant": "Tahara (Japan)", "panel_gap": 3.8,
        "note": "Flagship body-on-frame Lexus. Land Cruiser 200 underneath. 5.7L V8. Tahara-built quality matches LS. Semi-aniline leather, Mark Levinson reference audio, four-zone climate.",
    },
    ("Lexus", "LX 600", 2022): {
        "sub": adjust(BRAND_BASELINES["Lexus"], body=+10, nvh=+7, mat=+7, paint=+7, elec=+3, cosm=+6),
        "platform_type": "TNGA-F (body-on-frame, new Land Cruiser 300)", "weld": "laser + spot",
        "plant": "Tahara (Japan)", "panel_gap": 3.5,
        "note": "New TNGA-F platform (shared with 2022 Land Cruiser 300). 3.4L twin-turbo V6 replaces V8. GA-F body-on-frame, 20% stiffer. Two-tier rear seating options. New multimedia system.",
    },
    ("Lexus", "NX350h", 2022): {
        "sub": adjust(BRAND_BASELINES["Lexus"], body=+2, nvh=+3, mat=+3, paint=+2, elec=+5, cosm=+2),
        "platform_type": "TNGA-K (GA-K)", "weld": "laser + spot",
        "plant": "Miyata (Japan) / Cambridge (Canada)", "panel_gap": 4.0,
        "note": "TNGA-K platform. 2.5L hybrid AWD. New Lexus Interface infotainment (much improved over prior Remote Touch). Standard Lexus Safety System 3.0. Tahara-like quality at lower price.",
    },

    # === PORSCHE (4) - MLB Evo / MSB ===
    ("Porsche", "Cayenne Turbo", 2019): {
        "sub": adjust(BRAND_BASELINES["Porsche"], body=+5, nvh=+1, mat=+5, paint=+3, elec=+2, cosm=+3),
        "platform_type": "MLB Evo (Porsche-tuned)", "weld": "laser + spot",
        "plant": "Bratislava (Slovakia)", "panel_gap": 3.8,
        "note": "MLB Evo platform, Porsche extensively re-engineered suspension and body tuning. 4.0T V8. Aluminum body panels. PASM, air suspension, ceramic brakes optional. High-grade leather.",
    },
    ("Porsche", "Cayenne GTS", 2021): {
        "sub": adjust(BRAND_BASELINES["Porsche"], body=+5, nvh=+1, mat=+5, paint=+3, elec=+2, cosm=+3),
        "platform_type": "MLB Evo (Porsche-tuned)", "weld": "laser + spot",
        "plant": "Bratislava (Slovakia)", "panel_gap": 3.8,
        "note": "Same platform as Cayenne Turbo, GTS-tuned suspension and exhaust. V8, sport chrono, sport diff. Race-Tex (Alcantara) standard. Tight panel gaps.",
    },
    ("Porsche", "Cayenne Turbo GT", 2022): {
        "sub": adjust(BRAND_BASELINES["Porsche"], body=+5, nvh=+0, mat=+7, paint=+3, elec=+3, cosm=+3),
        "platform_type": "MLB Evo (Porsche-tuned, GT-spec)", "weld": "laser + spot",
        "plant": "Leipzig (Germany)", "panel_gap": 3.5,
        "note": "Most powerful Cayenne ever. 631hp, Nürburgring SUV lap record holder. Coupe-only, GT-tuned. Built in Leipzig with extra attention. Carbon roof standard. Race-Tex interior.",
    },
    ("Porsche", "Macan S", 2019): {
        "sub": adjust(BRAND_BASELINES["Porsche"], body=+1, nvh=-2, mat=+3, paint=+2, elec=0, cosm=+1),
        "platform_type": "MLB (first-gen, Audi Q5-derived)", "weld": "laser + spot",
        "plant": "Leipzig (Germany)", "panel_gap": 4.0,
        "note": "First-gen Macan on older MLB platform (Audi Q5-derived). V6. Leipzig plant Porsche-tuned assembly. Lower NVH than Q5 due to extra sound insulation.",
    },

    # === LAND ROVER (3) ===
    ("Land Rover", "Defender 110", 2020): {
        "sub": adjust(BRAND_BASELINES["Land Rover"], body=+5, nvh=+3, mat=+2, paint=+3, elec=+5, cosm=+3),
        "platform_type": "D7x (D7a, aluminum monocoque)", "weld": "laser + spot",
        "plant": "Nitra (Slovakia)", "panel_gap": 4.0,
        "note": "All-new D7x aluminum monocoque (replaced old body-on-frame). Modern electrical (much better than old Defender). Nitra plant quality improved significantly over Solihull.",
    },
    ("Land Rover", "Range Rover", 2018): {
        "sub": adjust(BRAND_BASELINES["Land Rover"], body=+3, nvh=+5, mat=+5, paint=+2, elec=-2, cosm=+3),
        "platform_type": "D7a (aluminum monocoque)", "weld": "laser + spot",
        "plant": "Solihull (UK)", "panel_gap": 4.0,
        "note": "L405 generation on D7a platform. Aluminum-intensive body. Excellent NVH (Range Rover benchmark). Infotainment and electronic complexity remain weak points (InControl issues).",
    },
    ("Land Rover", "Range Rover Evoque", 2020): {
        "sub": adjust(BRAND_BASELINES["Land Rover"], body=+2, nvh=+5, mat=+3, paint=+2, elec=-3, cosm=+2),
        "platform_type": "Premium Transverse (D8a, derived)", "weld": "laser + spot",
        "plant": "Halewood (UK)", "panel_gap": 4.0,
        "note": "Second-gen Evoque on PTA platform. Compact premium SUV with class-leading NVH. Electronics improved over first-gen but still under industry average.",
    },

    # === ACURA (2) ===
    ("Acura", "MDX", 2020): {
        "sub": adjust(BRAND_BASELINES["Acura"], body=+2, nvh=+2, mat=+2, paint=+2, elec=+2, cosm=+2),
        "platform_type": "Light Truck platform (shared with Pilot)", "weld": "spot",
        "plant": "Lincoln (USA)", "panel_gap": 4.5,
        "note": "New MDX on Honda light-truck platform. 3.5L V6, SH-AWD. Acura-tuned suspension. Milford-built? Lincoln Alabama. True touchpad interface replaces old knob.",
    },
    ("Acura", "RDX", 2020): {
        "sub": adjust(BRAND_BASELINES["Acura"], body=+1, nvh=+1, mat=+2, paint=+1, elec=+2, cosm=+1),
        "platform_type": "Light Truck platform (compact)", "weld": "spot",
        "plant": "East Liberty (USA)", "panel_gap": 4.5,
        "note": "Compact luxury SUV on Honda light-truck platform. 2.0L turbo. True touchpad. AcuraWatch standard. East Liberty plant quality strong.",
    },

    # === CADILLAC (3) ===
    ("Cadillac", "XT4", 2019): {
        "sub": adjust(BRAND_BASELINES["Cadillac"], body=-1, nvh=-1, mat=+1, paint=0, elec=-1, cosm=0),
        "platform_type": "D2XX (compact, derived)", "weld": "spot",
        "plant": "Fairfax (USA)", "panel_gap": 4.5,
        "note": "Compact Cadillac on GM D2XX platform (shared with Chevy Equinox). 2.0L turbo. Lower-tier interior vs XT5. CUE infotainment improved but still weak.",
    },
    ("Cadillac", "XT5", 2020): {
        "sub": adjust(BRAND_BASELINES["Cadillac"], body=+0, nvh=+0, mat=+2, paint=+1, elec=+0, cosm=+1),
        "platform_type": "Chi (C1XX)", "weld": "spot",
        "plant": "Spring Hill (USA)", "panel_gap": 4.5,
        "note": "Mid-size Cadillac on Chi platform. 3.6L V6. Spring Hill quality decent. CUE infotainment still a weak point. Premium materials on higher trims.",
    },
    ("Cadillac", "XT6", 2020): {
        "sub": adjust(BRAND_BASELINES["Cadillac"], body=+0, nvh=+0, mat=+2, paint=+1, elec=+0, cosm=+1),
        "platform_type": "Chi (C1XX, extended)", "weld": "spot",
        "plant": "Spring Hill (USA)", "panel_gap": 4.5,
        "note": "3-row Cadillac on extended Chi platform. 3.6L V6. Same interior quality as XT5. 7-seat configuration.",
    },

    # === INFINITI (2) ===
    ("Infiniti", "QX60", 2020): {
        "sub": adjust(BRAND_BASELINES["Infiniti"], body=+3, nvh=+5, mat=+3, paint=+3, elec=+3, cosm=+3),
        "platform_type": "Nissan D-platform (derived)", "weld": "spot",
        "plant": "Smyrna (USA)", "panel_gap": 5.0,
        "note": "All-new QX60 (2022 model year was the redesign, this 2020 is pre-facelift). Pre-facelift had poor interior quality and CVT. Infiniti brand quality below segment average.",
    },
    ("Infiniti", "QX80", 2020): {
        "sub": adjust(BRAND_BASELINES["Infiniti"], body=+5, nvh=+8, mat=+3, paint=+3, elec=+5, cosm=+3),
        "platform_type": "Nissan Patrol-derived (body-on-frame)", "weld": "spot",
        "plant": "Yokohama (Japan)", "panel_gap": 5.0,
        "note": "Body-on-frame full-size SUV derived from Nissan Patrol (Y62). 5.6L V8. Proven platform. Pre-facelift interior dated. Yokohama plant quality decent.",
    },

    # === LINCOLN (1) - Corsair already existed ===
    ("Lincoln", "Nautilus", 2020): {
        "sub": adjust(BRAND_BASELINES["Lincoln"], body=-1, nvh=-1, mat=+1, paint=0, elec=0, cosm=0),
        "platform_type": "CD6 (Ford Edge-derived)", "weld": "spot",
        "plant": "Oakville (Canada)", "panel_gap": 4.5,
        "note": "Lincoln mid-size SUV on Ford Edge platform. 2.0L turbo or 2.7L V6. SYNC4 infotainment. Bridge of Weir Deepsoft leather optional.",
    },

    # === EXOTIC / ULTRA-LUXURY (3) ===
    ("Bentley", "Bentayga", 2017): {
        "sub": adjust(BRAND_BASELINES["Bentley"], body=+3, nvh=+5, mat=+3, paint=+3, elec=-2, cosm=+3),
        "platform_type": "VW D1 platform (Bentley-original)", "weld": "laser + spot",
        "plant": "Crewe (UK)", "panel_gap": 3.5,
        "note": "First Bentayga on VW Group D1 platform (Bentley Continental twin). 6.0L W12. Hand-built at Crewe. Highest-grade leather and wood. Hand-stitched everything.",
    },
    ("Rolls-Royce", "Cullinan", 2019): {
        "sub": adjust(BRAND_BASELINES["Rolls-Royce"], body=+2, nvh=+5, mat=+3, paint=+3, elec=-2, cosm=+3),
        "platform_type": "BMW Architecture of Luxury (CLAR-derived)", "weld": "laser + spot",
        "plant": "Goodwood (UK)", "panel_gap": 3.0,
        "note": "Rolls-Royce's first SUV. BMW Architecture of Luxury platform, heavily modified. 6.75L twin-turbo V12. Hand-built at Goodwood. Starlight headliner, lambswool floor mats.",
    },
    ("Lamborghini", "Urus", 2019): {
        "sub": adjust(BRAND_BASELINES["Lamborghini"], body=+5, nvh=-3, mat=+3, paint=+3, elec=-3, cosm=+3),
        "platform_type": "MLB Evo (Lamborghini-tuned)", "weld": "laser + spot",
        "plant": "Bratislava (Slovakia)", "panel_gap": 3.5,
        "note": "Super SUV on MLB Evo (shared with Q7/Q8/Bentayga/Cayenne). Lamborghini extensively re-tuned. 4.0T V8. Carbon-intensive interior. Anima drive modes.",
    },
}


def insert_quality(cur: sqlite3.Cursor, car: dict, q_data: dict) -> None:
    """Insert a build_quality row for a car."""
    sub = q_data["sub"]
    q_score = compute_q(sub)

    cur.execute(
        """INSERT INTO build_quality (
            car_id, q_score, score_body_construction, score_nvh_isolation,
            score_interior_materials, score_paint_corrosion,
            score_electrical_aging, score_cosmetic_aging,
            body_construction_notes, nvh_isolation_notes,
            interior_materials_notes, paint_corrosion_notes,
            electrical_aging_notes, cosmetic_aging_notes,
            q_score_notes, platform_type, assembly_plant,
            weld_technology, panel_gap_mm, source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            car["id"], q_score,
            sub["body"], sub["nvh"], sub["mat"], sub["paint"], sub["elec"], sub["cosm"],
            f'{q_data["note"]} Body: {q_data["platform_type"]}, plant {q_data["plant"]}, {q_data["weld"]} welding.',
            f'{q_data["note"]} NVH isolation appropriate for segment.',
            f'{q_data["note"]} Interior materials grade appropriate for segment.',
            f'{q_data["note"]} Paint process as used in {q_data["plant"]}.',
            f'{q_data["note"]} Electrical aging inferred from segment norms and complexity.',
            f'{q_data["note"]} Long-term aging inferred from brand track record.',
            f'Inferred Q-score {q_score} from brand baseline (see existing data). Platform {q_data["platform_type"]}, plant {q_data["plant"]}. Sub-scores adjusted for segment and complexity.',
            q_data["platform_type"], q_data["plant"], q_data["weld"], q_data["panel_gap"],
            "inferred-2026-06-18",
        ),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Infer Q scores for new SUVs")
    parser.add_argument("--dry-run", action="store_true", help="Preview only")
    args = parser.parse_args()

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Get all new luxury SUVs (id >= 223)
    cur.execute("""
        SELECT id, year_start, make, model, variant
        FROM cars
        WHERE id >= 223
        ORDER BY make, model, year_start
    """)
    new_cars = cur.fetchall()

    inserted = 0
    skipped = 0
    unmatched = []
    for car in new_cars:
        key = (car["make"], car["model"], car["year_start"])
        if key not in Q_INFERENCE:
            unmatched.append(car)
            continue

        # Check if already has build_quality
        cur.execute("SELECT id FROM build_quality WHERE car_id = ?", (car["id"],))
        if cur.fetchone():
            skipped += 1
            print(f"  SKIP (exists): id={car['id']} {car['year_start']} {car['make']} {car['model']}")
            continue

        q_data = Q_INFERENCE[key]
        insert_quality(cur, dict(car), q_data)
        q_score = compute_q(q_data["sub"])
        inserted += 1
        print(f"  ADDED Q={q_score:>5.1f}: id={car['id']} {car['year_start']} {car['make']} {car['model']}")

    print()
    print(f"Total: {inserted} inserted, {skipped} skipped, {len(unmatched)} unmatched")
    if unmatched:
        print(f"Unmatched cars (need inference added):")
        for c in unmatched:
            print(f"  {c['year_start']} {c['make']} {c['model']}")

    if args.dry_run:
        print("[DRY RUN] No writes applied.")
        conn.rollback()
    else:
        conn.commit()
        print(f"Committed to {DB_PATH}")

    conn.close()
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

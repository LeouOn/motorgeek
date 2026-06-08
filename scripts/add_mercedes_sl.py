#!/usr/bin/env python3
"""Add all Mercedes-Benz SL generations to the MotorGeek database.

Covers the full lineage from the 300 SL Gullwing (W198) to the latest AMG SL 63 (R232):
    135 - W198 300 SL Gullwing   (1954-1957)
    136 - W121 190 SL            (1955-1963)
    137 - W113 280 SL Pagoda     (1967-1971)
    138 - R107 560 SL            (1986-1989)
    139 - R129 500 SL            (1990-1998)
    140 - R129 SL 600            (1993-2001)
    141 - R230 SL55 AMG          (2002-2008)
    142 - R231 SL63 AMG          (2013-2020)
    143 - R232 AMG SL 63         (2022-present)

Usage:
    python scripts/add_mercedes_sl.py
    python scripts/add_mercedes_sl.py --db path/to/motorgeek.db
"""

import argparse
import sqlite3
from pathlib import Path


def get_db_path() -> Path:
    cfg = Path("config.yaml")
    if cfg.exists():
        import yaml
        with open(cfg) as f:
            config = yaml.safe_load(f)
        return Path(config.get("database", {}).get("path", "data/motorgeek.db"))
    return Path("data/motorgeek.db")


def add_sl_cars(cur: sqlite3.Cursor):
    """Insert the 9 SL generations into the cars table."""
    cur.execute("DELETE FROM cars WHERE id BETWEEN 135 AND 143")
    cur.executemany(
        """INSERT INTO cars (
            id, make, model, generation, year_start, year_end, era_tag,
            character, family, variant, body_style, country, production_units,
            description, image_paths, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))""",
        [
            (
                135, "Mercedes-Benz", "300 SL", "W198", 1954, 1957, "classic",
                "hyper", "SL", "Gullwing", "coupe", "Germany", 1400,
                "The car that started it all. Born from a racing program, the 300 SL Gullwing featured Bosch mechanical direct fuel injection — the first production car to use it. Its tubular spaceframe necessitated the iconic top-hinged doors. The 3.0L inline-six produced 215 HP, making it the fastest production car of its era at 147 mph. Only 1,400 Gullwing coupes were built before the roadster took over. A masterpiece of engineering and one of the most beautiful cars ever made.",
                "[]",
            ),
            (
                136, "Mercedes-Benz", "190 SL", "W121", 1955, 1963, "classic",
                "classic", "SL", "190 SL", "roadster", "Germany", 25881,
                "The 'people's SL' — a more affordable companion to the 300 SL. Powered by a 1.9L SOHC inline-four with twin Solex carburetors producing 104 HP. Shared the 300 SL's gorgeous styling but used a simpler unitary body instead of the exotic tubular spaceframe. Drum brakes and a swing-axle rear made it more cruiser than sports car, but its beauty is undeniable. Grace Kelly drove one, which tells you everything about its glamour.",
                "[]",
            ),
            (
                137, "Mercedes-Benz", "280 SL", "W113", 1967, 1971, "classic",
                "classic", "SL", "Pagoda", "roadster", "Germany", 23887,
                "The 'Pagoda' — named for its concave hardtop roof that mimics a Japanese temple. The final and most developed W113 variant with the 2.8L M130 inline-six producing 168 HP. Paul Bracq's design is timeless. Four-wheel disc brakes, Bosch fuel injection, and a fully independent suspension made it surprisingly competent. The defining Mercedes GT roadster: elegant, reliable, and engineered to be driven rather than just admired.",
                "[]",
            ),
            (
                138, "Mercedes-Benz", "560 SL", "R107", 1986, 1989, "80s",
                "classic", "SL", "560 SL", "roadster", "Germany", 49347,
                "The longest-running SL generation (1971-1989) ended with the 560 SL — the most powerful R107 and a US-market exclusive. The 5.5L M117 V8 produced 227 HP through a 4-speed automatic. A luxury cruiser, not a sports car, but that's the point. The R107 defined the 'Miami Vice' era of Mercedes excess. Reliable, comfortable, and a time capsule of 1980s opulence. Values are climbing as 80s nostalgia peaks.",
                "[]",
            ),
            (
                139, "Mercedes-Benz", "500 SL", "R129", 1990, 1998, "90s",
                "luxury", "SL", "500 SL", "roadster", "Germany", 79827,
                "The R129 brought the SL into the modern era with a stunning Bruno Sacco design, a fully automatic soft top, and the magnificent M119 5.0L DOHC 32-valve V8 producing 315 HP. The first SL with a rollover bar that deployed in milliseconds. Princess Diana drove one — which caused a stir since she was technically not supposed to drive a 'foreign' car. Biodegradable wiring harnesses on pre-1996 cars are the main headache, but the M119 engine is bulletproof.",
                "[]",
            ),
            (
                140, "Mercedes-Benz", "SL 600", "R129", 1993, 2001, "90s",
                "luxury", "SL", "SL 600", "roadster", "Germany", 11089,
                "The V12 flagship of the R129 lineup. The M120 6.0L SOHC 48-valve V12 produced 389 HP and 570 Nm of torque — the same engine that Pagani used in the Zonda. The SL 600 was the ultimate expression of Mercedes over-engineering: dual coil packs, dual fuel pumps, 24 spark plugs, and an active hydraulic suspension (ADS). Expensive to maintain but magnificently smooth. The last of the analog V12 super-roadsters.",
                "[]",
            ),
            (
                141, "Mercedes-AMG", "SL55 AMG", "R230", 2002, 2008, "00s",
                "hot", "SL", "SL55 AMG", "roadster", "Germany", None,
                "The SL that redefined what an SL could be. AMG's M113K 5.4L supercharged V8 produced 493 HP and an earth-moving 700 Nm of torque from just 2,750 RPM. The R230 introduced the folding hardtop (Vario Roof) and Active Body Control (ABC) suspension. 0-60 in 4.5 seconds — genuinely supercar-fast in 2002. The SL55 AMG was the car Mercedes built to remind everyone they could still do brutal. ABC suspension and SBC brakes are the known trouble spots.",
                "[]",
            ),
            (
                142, "Mercedes-AMG", "SL63 AMG", "R231", 2013, 2020, "10s",
                "hot", "SL", "SL63 AMG", "roadster", "Germany", None,
                "The R231 was the first all-aluminum SL, shedding significant weight. The facelift SL63 AMG got the M157 5.5L biturbo V8 producing 577 HP and 900 Nm — absurd torque for a roadster. AMG's MCT 7-speed transmission delivered it to the rear wheels. The aluminum body and carbon fiber components made it lighter than the R230 despite being larger. A high-speed GT weapon that can also drop the top on a sunny afternoon.",
                "[]",
            ),
            (
                143, "Mercedes-AMG", "SL 63", "R232", 2022, None, "modern",
                "hot", "SL", "SL 63 4MATIC+", "roadster", "Germany", None,
                "The SL reborn — developed entirely by AMG for the first time. Returns to a soft top (saving 46 lbs vs the folding hardtop) and adds 4MATIC+ all-wheel drive. The M177 4.0L biturbo V8 (hot-vee layout from the AMG GT) produces 577 HP. 0-60 in 3.0 seconds. 2+2 seating returns for the first time since the R129. The R232 is a statement: AMG can build a better SL than Mercedes could. Active rear-axle steering, carbon fiber structure, and a chassis tuned at the Nordschleife.",
                "[]",
            ),
        ],
    )
    print("  Inserted 9 cars (IDs 135-143)")


def add_sl_performance(cur: sqlite3.Cursor):
    """Insert performance data."""
    cur.execute("DELETE FROM performance WHERE car_id BETWEEN 135 AND 143")
    cur.executemany(
        """INSERT INTO performance (
            car_id, source, accel_0_60, accel_0_100, quarter_mile_time,
            quarter_mile_speed, top_speed_mph, power_to_weight, lateral_g
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        [
            # 135 - 300 SL Gullwing
            (135, "manual", 7.5, 9.3, 15.3, 92.0, 147.0, 166.28, None),
            # 136 - 190 SL
            (136, "manual", 13.3, 14.5, None, None, 107.0, 91.23, None),
            # 137 - 280 SL Pagoda
            (137, "manual", 9.0, 10.5, None, None, 124.0, 123.53, None),
            # 138 - 560 SL R107
            (138, "manual", 6.6, 7.5, 14.7, 86.0, 149.0, 135.12, None),
            # 139 - 500 SL R129
            (139, "manual", 6.2, 7.0, 14.6, 97.0, 155.0, 177.97, None),
            # 140 - SL 600 R129
            (140, "manual", 5.8, 6.5, 14.2, 100.0, 155.0, 196.46, None),
            # 141 - SL55 AMG R230
            (141, "manual", 4.5, 5.0, 11.9, 120.0, 155.0, 252.17, 0.91),
            # 142 - SL63 AMG R231
            (142, "manual", 3.5, 4.0, 11.8, 123.0, 155.0, 313.14, 0.95),
            # 143 - AMG SL 63 R232
            (143, "manual", 3.0, 3.4, 11.2, 125.0, 196.0, 295.14, 1.01),
        ],
    )
    print("  Inserted performance: 9 rows")


def add_sl_powertrain(cur: sqlite3.Cursor):
    """Insert powertrain_ice data."""
    cur.execute("DELETE FROM powertrain_ice WHERE car_id BETWEEN 135 AND 143")
    cur.executemany(
        """INSERT INTO powertrain_ice (
            car_id, source, engine_layout, displacement_cc, cylinders, aspiration,
            horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm, redline_rpm,
            compression_ratio, fuel_system, transmission_type, gear_count, drivetrain,
            curb_weight_kg, weight_dist_pct, suspension_fr, brakes_fr,
            drag_coefficient, is_hybrid, cargo_volume_liters
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        [
            # 135 - 300 SL Gullwing
            (135, "manual", "Inline-6", 2996.0, 6, "Naturally aspirated",
             215.0, 5800, 275.0, 4600, None,
             9.5, "Bosch mechanical direct injection", "4-speed manual", 4, "RWD",
             1293.0, "47/53", "Double wishbone", "drum", 0.38, 0, None),
            # 136 - 190 SL
            (136, "manual", "Inline-4", 1897.0, 4, "Naturally aspirated",
             104.0, 5700, 142.0, 3200, None,
             8.8, "Twin Solex 44PHH carburetors", "4-speed manual", 4, "RWD",
             1140.0, "50/50", "Double wishbone", "drum", 0.36, 0, None),
            # 137 - 280 SL Pagoda
            (137, "manual", "Inline-6", 2778.0, 6, "Naturally aspirated",
             168.0, 5750, 240.0, 4500, None,
             9.5, "Bosch mechanical fuel injection", "4-speed manual", 4, "RWD",
             1360.0, "50/50", "Double wishbone", "disc", 0.42, 0, None),
            # 138 - 560 SL R107
            (138, "manual", "V8", 5547.0, 8, "Naturally aspirated",
             227.0, 4750, 378.0, 3250, None,
             9.0, "Bosch KE-Jetronic (CIS-E)", "4-speed automatic", 4, "RWD",
             1680.0, "52/48", "Double wishbone", "disc", None, 0, None),
            # 139 - 500 SL R129
            (139, "manual", "V8", 4973.0, 8, "Naturally aspirated",
             315.0, 5500, 450.0, 4000, 6500,
             10.0, "Bosch KE-Jetronic (CIS-E)", "4-speed automatic", 4, "RWD",
             1770.0, "52/48", "Double wishbone", "vented disc", 0.30, 0, None),
            # 140 - SL 600 R129
            (140, "manual", "V12", 5987.0, 12, "Naturally aspirated",
             389.0, 5200, 570.0, 3800, 6500,
             10.0, "Bosch LH-Jetronic", "4-speed automatic", 4, "RWD",
             1980.0, "53/47", "Double wishbone", "vented disc", 0.30, 0, None),
            # 141 - SL55 AMG R230
            (141, "manual", "V8", 5439.0, 8, "Supercharged (Lysholm screw-type, 11.6 psi)",
             493.0, 6100, 700.0, 2750, None,
             9.0, "EFI", "5-speed automatic (Speedshift)", 5, "RWD",
             1955.0, "53/47", "Double wishbone", "vented disc", 0.29, 0, None),
            # 142 - SL63 AMG R231
            (142, "manual", "V8", 5461.0, 8, "BiTurbo",
             577.0, 5500, 900.0, 2000, None,
             10.0, "Direct injection", "7-speed MCT (AMG Speedshift)", 7, "RWD",
             1845.0, "53/47", "Double wishbone", "carbon ceramic (opt)", 0.29, 0, None),
            # 143 - AMG SL 63 R232
            (143, "manual", "V8", 3982.0, 8, "BiTurbo (hot-vee)",
             577.0, 6000, 800.0, 2500, None,
             8.6, "Direct injection", "9-speed MCT (AMG Speedshift)", 9, "AWD (4MATIC+)",
             1955.0, "55/45", "Double wishbone (multilink)", "carbon ceramic (opt)", 0.31, 0, None),
        ],
    )
    print("  Inserted powertrain_ice: 9 rows")


def add_sl_reliability(cur: sqlite3.Cursor):
    """Insert reliability data."""
    cur.execute("DELETE FROM reliability WHERE car_id BETWEEN 135 AND 143")
    cur.executemany(
        """INSERT INTO reliability (
            car_id, source, reliability_score, common_failures, avg_repair_cost,
            recall_count, part_availability, diy_friendliness, known_issues
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        [
            # 135 - 300 SL Gullwing
            (135, "manual", 72, '{"fuel injection pump": 4, "drum brakes": 2}', 5000.0, 0,
             "Specialist only (MB Classic Center)", "Difficult (specialist required)",
             '{"fuel injection pump": "Bosch mechanical DI pump requires specialist rebuild.", "brakes": "Drum brakes all around — period correct but weak by modern standards."}'),
            # 136 - 190 SL
            (136, "manual", 70, '{"Solex carburetors": 3, "drum brakes": 2}', 3500.0, 0,
             "Good (specialist + aftermarket)", "Moderate (simple mechanicals)",
             '{"carburetors": "Twin Solex 44PHH need periodic rebuild and sync.", "drum brakes": "All drums — adequate for cruising, not for spirited driving."}'),
            # 137 - 280 SL Pagoda
            (137, "manual", 82, '{"fuel injection pump": 3, "swing axle": 2}', 2500.0, 0,
             "Good (specialist network)", "Moderate",
             '{"injection pump": "Bosch mechanical injection pump needs calibration every 30k mi.", "swing axle": "Rear swing axle can cause tuck-under if driven hard."}'),
            # 138 - 560 SL R107
            (138, "manual", 80, '{"timing chain guides": 3, "AC system": 3}', 2000.0, 1,
             "Excellent (MB Classic + aftermarket)", "Good (simple V8)",
             '{"timing chain": "Inspect/replace guides at 100k mi.", "AC": "R12 to R134a conversion needed. Compressor seal leaks common."}'),
            # 139 - 500 SL R129
            (139, "manual", 75, '{"biodegradable wiring harness": 4, "soft top hydraulics": 3}', 3000.0, 2,
             "Good (specialist network)", "Moderate (tight engine bay)",
             '{"wiring harness": "Pre-1996 cars have biodegradable insulation that crumbles. Full harness replacement $2-4K.", "soft top": "Hydraulic cylinder seals leak over time. $800-1500 per cylinder."}'),
            # 140 - SL 600 R129
            (140, "manual", 65, '{"dual coil packs": 4, "ADS suspension": 4, "wiring harness": 4}', 5000.0, 2,
             "Moderate (V12-specific parts scarce)", "Difficult (complex V12, tight access)",
             '{"coil packs": "Two coil packs, ~$600-1200 each. 24 spark plugs to replace.", "ADS": "Active hydraulic suspension — accumulator spheres and valve blocks fail. Very expensive.", "coolant hoses": "13+ engine coolant hoses, many buried deep. Preventative replacement recommended."}'),
            # 141 - SL55 AMG R230
            (141, "manual", 55, '{"ABC suspension": 5, "SBC brakes": 4, "roof hydraulics": 3}', 4500.0, 3,
             "Good (AMG parts available)", "Difficult (complex systems)",
             '{"ABC": "Active Body Control hydraulic suspension is THE known issue. Struts, lines, pump — $5-10K+ when it fails.", "SBC": "Sensotronic Brake Control pump fails and has a 10-year/service life counter. MB extended warranty on this.", "intercooler pump": "Supercharger intercooler coolant pump fails — cheap part, causes heat soak."}'),
            # 142 - SL63 AMG R231
            (142, "manual", 62, '{"turbo wastegate rattle": 3, "ABC suspension": 3, "oil consumption": 2}', 3500.0, 2,
             "Good (AMG network)", "Difficult (biturbo packaging)",
             '{"wastegate": "M157 turbo wastegate rattle under deceleration. AMG extended warranty on turbos.", "ABC": "Same ABC issues as R230 but somewhat improved.", "battery": "Multiple battery drain issues if not driven regularly."}'),
            # 143 - AMG SL 63 R232
            (143, "manual", 70, '{"48V system glitches": 2, "MBUX infotainment": 2, "rear axle steering sensor": 1}', 2000.0, 1,
             "Good (current dealer network)", "Difficult (electronics-heavy)",
             '{"48V": "Early 2022 models had 48V electrical system glitches — resolved via software updates.", "MBUX": "Infotainment system occasional reboots, OTA updates fix most issues.", "warranty": "Most cars still under factory warranty through 2026."}'),
        ],
    )
    print("  Inserted reliability: 9 rows")


def add_sl_cost_to_own(cur: sqlite3.Cursor):
    """Insert cost_to_own data."""
    cur.execute("DELETE FROM cost_to_own WHERE car_id BETWEEN 135 AND 143")
    cur.executemany(
        """INSERT INTO cost_to_own (
            car_id, source, msrp_original, msrp_currency, msrp_inflation_adj,
            fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est,
            insurance_group, depreciation_5yr_pct
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        [
            # 135 - 300 SL Gullwing - MSRP ~$7,500 in 1955
            (135, "manual", 7500.0, "USD", 89000.0, 10.0, 14.0, 3000.0, "classic", -100.0),
            # 136 - 190 SL - MSRP ~$4,000
            (136, "manual", 4000.0, "USD", 46000.0, 14.0, 19.0, 2000.0, "classic", -80.0),
            # 137 - 280 SL Pagoda - MSRP ~$6,900
            (137, "manual", 6900.0, "USD", 58000.0, 14.0, 19.0, 1800.0, "classic", -60.0),
            # 138 - 560 SL R107 - MSRP ~$55,000
            (138, "manual", 55000.0, "USD", 148000.0, 12.0, 16.0, 2000.0, "classic", -50.0),
            # 139 - 500 SL R129 - MSRP ~$85,000
            (139, "manual", 85000.0, "USD", 197000.0, 14.0, 20.0, 2500.0, "17", 75.0),
            # 140 - SL 600 R129 - MSRP ~$120,000
            (140, "manual", 120000.0, "USD", 258000.0, 12.0, 18.0, 4500.0, "19", 80.0),
            # 141 - SL55 AMG R230 - MSRP ~$115,500
            (141, "manual", 115500.0, "USD", 178000.0, 12.0, 23.0, 3500.0, "20", 75.0),
            # 142 - SL63 AMG R231 - MSRP ~$150,000
            (142, "manual", 150000.0, "USD", 195000.0, 14.0, 24.0, 3000.0, "20", 65.0),
            # 143 - AMG SL 63 R232 - MSRP ~$183,000
            (143, "manual", 183000.0, "USD", 188000.0, 14.0, 21.0, 1500.0, "21", 35.0),
        ],
    )
    print("  Inserted cost_to_own: 9 rows")


def add_sl_market_history(cur: sqlite3.Cursor):
    """Insert market_history data."""
    cur.execute("DELETE FROM market_history WHERE car_id BETWEEN 135 AND 143")
    cur.executemany(
        """INSERT INTO market_history (
            car_id, date_recorded, price_low, price_high, volume_sold_est,
            market_trend_indicator, source_site
        ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
        [
            # 300 SL Gullwing — million-dollar classic
            (135, "2026-05-01", 1000000.0, 2500000.0, 8, "rising", "RM Sotheby's"),
            # 190 SL — strong classic market
            (136, "2026-05-01", 100000.0, 350000.0, 12, "rising", "Hagerty"),
            # 280 SL Pagoda — climbing steadily
            (137, "2026-05-01", 80000.0, 200000.0, 15, "rising", "Hagerty"),
            # 560 SL R107 — affordable classic
            (138, "2026-05-01", 10000.0, 75000.0, 20, "rising", "BaT"),
            # 500 SL R129 — still depreciated, beginning to climb
            (139, "2026-05-01", 8000.0, 50000.0, 10, "rising", "BaT"),
            # SL 600 R129 — V12 tax keeps prices down
            (140, "2026-05-01", 5400.0, 80000.0, 5, "rising", "BaT"),
            # SL55 AMG R230 — depreciated hard, starting to climb
            (141, "2026-05-01", 20000.0, 45000.0, 8, "rising", "BaT"),
            # SL63 AMG R231 — still depreciating
            (142, "2026-05-01", 22700.0, 90000.0, 6, "stable", "BaT"),
            # AMG SL 63 R232 — current model
            (143, "2026-05-01", 88000.0, 175000.0, 3, "depreciating", "Autotrader"),
        ],
    )
    print("  Inserted market_history: 9 rows")


def add_sl_dimensions(cur: sqlite3.Cursor):
    """Insert dimensions data."""
    cur.execute("DELETE FROM dimensions WHERE car_id BETWEEN 135 AND 143")
    cur.executemany(
        """INSERT INTO dimensions (
            car_id, length_mm, width_mm, height_mm, wheelbase_mm,
            track_front_mm, track_rear_mm, source
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        [
            # 135 - 300 SL Gullwing
            (135, 4570, 1778, 1302, 2400, 1384, 1435, "manual"),
            # 136 - 190 SL
            (136, 4290, 1740, 1320, 2400, 1430, 1470, "manual"),
            # 137 - 280 SL Pagoda
            (137, 4285, 1760, 1305, 2400, 1485, 1485, "manual"),
            # 138 - 560 SL R107
            (138, 4580, 1790, 1307, 2456, None, None, "manual"),
            # 139 - 500 SL R129
            (139, 4470, 1811, 1300, 2515, None, None, "manual"),
            # 140 - SL 600 R129
            (140, 4470, 1810, 1290, 2520, None, None, "manual"),
            # 141 - SL55 AMG R230
            (141, 4535, 1827, 1295, 2560, None, None, "manual"),
            # 142 - SL63 AMG R231
            (142, 4617, 1877, 1315, 2585, None, None, "manual"),
            # 143 - AMG SL 63 R232
            (143, 4705, 1915, 1353, 2700, None, None, "manual"),
        ],
    )
    print("  Inserted dimensions: 9 rows")


def main():
    parser = argparse.ArgumentParser(description="Add Mercedes SL generations to MotorGeek DB")
    parser.add_argument("--db", type=Path, default=None, help="Path to motorgeek.db")
    args = parser.parse_args()

    db_path = args.db or get_db_path()
    if not db_path.exists():
        print(f"Database not found at {db_path}")
        print("Run 'python seed_data.py' first to create the database.")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    print("Adding Mercedes-Benz SL generations (9 cars)...")

    add_sl_cars(cur)
    add_sl_performance(cur)
    add_sl_powertrain(cur)
    add_sl_reliability(cur)
    add_sl_cost_to_own(cur)
    add_sl_market_history(cur)
    add_sl_dimensions(cur)

    conn.commit()
    conn.close()

    print("\nDone! 9 Mercedes-Benz SL generations added (IDs 135-143).")
    print("Run 'motorgeek serve' and browse your collection.")


if __name__ == "__main__":
    main()

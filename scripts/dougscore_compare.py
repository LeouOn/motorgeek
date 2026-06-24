"""Doug Score comparison: side-by-side our composite vs Doug DeMuro's Dougscore.

Matches the 33 entries in data/dougscore_anchors.json against DB cars by
make/model/year proximity, then emits a comparison table.

Usage:
    python scripts/dougscore_compare.py           # full comparison
    python scripts/dougscore_compare.py --limit 10  # top 10 only
    python scripts/dougscore_compare.py --json    # JSON output
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "motorgeek.db"
DOUGSCORE_PATH = ROOT / "data" / "dougscore_anchors.json"


def load_dougscore() -> list[dict]:
    with open(DOUGSCORE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_db() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def match_cars(dougscore: list[dict], db: sqlite3.Connection) -> list[tuple[dict, sqlite3.Row | None, float]]:
    """Match each Doug Score entry to a DB car.

    Returns list of (ds_entry, db_car_or_None, match_confidence 0-1).
    """
    cur = db.cursor()
    cur.execute("SELECT id, year_start, make, model, body_style FROM cars")
    all_cars = cur.fetchall()

    results = []
    for ds in dougscore:
        ds_make = ds["make"].lower()
        ds_model = ds["model"].lower()
        ds_year = ds["year"]

        candidates = []
        for car in all_cars:
            c_make = car["make"].lower()
            c_model = car["model"].lower()
            c_year = car["year_start"]

            # Make must match
            if ds_make not in c_make and c_make not in ds_make:
                continue

            # Normalize model (strip generation suffixes)
            ds_model_norm = ds_model.split("(")[0].strip()
            c_model_norm = c_model.split("(")[0].strip()

            # Exact model match
            if ds_model_norm == c_model_norm:
                year_diff = abs(c_year - ds_year)
                confidence = max(0.5, 1.0 - year_diff * 0.1)
                candidates.append((car, confidence))
                continue

            # Substring model match (less confident)
            if ds_model_norm in c_model_norm or c_model_norm in ds_model_norm:
                year_diff = abs(c_year - ds_year)
                confidence = max(0.3, 0.7 - year_diff * 0.1)
                candidates.append((car, confidence))

        if candidates:
            candidates.sort(key=lambda x: -x[1])
            best_car, conf = candidates[0]
            results.append((ds, best_car, conf))
        else:
            results.append((ds, None, 0.0))

    return results


def get_composite_breakdown(db: sqlite3.Connection, car_id: int) -> dict | None:
    """Get our composite score breakdown for a car, matching the composite.py
    logic but reading directly from the DB so we don't need to import all the
    heavy modules from the CLI here.
    """
    cur = db.cursor()

    # Quality from build_quality.q_score
    cur.execute("SELECT q_score FROM build_quality WHERE car_id = ?", (car_id,))
    row = cur.fetchone()
    q_score = row["q_score"] if row and row["q_score"] else None

    # Reliability from reliability.reliability_score
    cur.execute("SELECT reliability_score FROM reliability WHERE car_id = ?", (car_id,))
    row = cur.fetchone()
    rel_score = row["reliability_score"] if row and row["reliability_score"] else None

    # ZP from zeperfs_indices
    cur.execute("SELECT zeperfs_index FROM zeperfs_indices WHERE car_id = ?", (car_id,))
    row = cur.fetchone()
    zp = row["zeperfs_index"] if row and row["zeperfs_index"] else None

    # Practicality from cargo + body style -- simplified version
    cur.execute("""
        SELECT pt.cargo_volume_liters, c.body_style,
               d.seat_count, d.cargo_volume_liters_seats_down,
               d.rear_legroom_mm, d.tow_capacity_kg
        FROM cars c
        LEFT JOIN powertrain_ice pt ON pt.car_id = c.id
        LEFT JOIN dimensions d ON d.car_id = c.id
        WHERE c.id = ?
    """, (car_id,))
    row = cur.fetchone()
    if not row:
        return None

    # Simplified practicality: cargo cf -> tier 1-10
    cargo = row["cargo_volume_liters"] or 0
    body_style = (row["body_style"] or "").lower()
    cargo_cf = cargo / 28.32
    if cargo_cf < 3.0: tier = 1
    elif cargo_cf < 6.5: tier = 2
    elif cargo_cf < 11.0: tier = 3
    elif cargo_cf < 16.0: tier = 4
    elif cargo_cf < 24.0: tier = 5
    elif cargo_cf < 34.0: tier = 6
    elif cargo_cf < 48.0: tier = 7
    elif cargo_cf < 64.0: tier = 8
    elif cargo_cf < 72.0: tier = 9
    else: tier = 10

    # Wagon bonus
    if body_style in ("wagon", "estate"):
        tier = min(10, tier + 1)

    # v2 bonuses
    if row["cargo_volume_liters_seats_down"] and row["cargo_volume_liters_seats_down"] > 1500:
        tier = min(10, tier + 0.5)
    if row["seat_count"] and row["seat_count"] >= 7:
        tier = min(10, tier + 0.5)
    if row["rear_legroom_mm"] and row["rear_legroom_mm"] > 950:
        tier = min(10, tier + 0.5)
    if row["tow_capacity_kg"] and row["tow_capacity_kg"] > 2000:
        tier = min(10, tier + 0.5)

    p_score = tier * 10

    # ZP normalization (linear /3)
    zp_norm = (zp / 3.0) if zp else None

    # Composite: 40/30/15/15 with redistribution
    dims = {"Q": q_score, "R": rel_score, "P": p_score, "ZP": zp_norm}
    weights = {"Q": 0.40, "R": 0.30, "P": 0.15, "ZP": 0.15}
    present = {k: v for k, v in dims.items() if v is not None}
    if len(present) < 2:
        return None
    total_weight = sum(weights[k] for k in present)
    composite = sum(dims[k] * weights[k] for k in present) / total_weight

    return {
        "composite": round(composite, 1),
        "Q": round(q_score, 1) if q_score else None,
        "R": round(rel_score, 1) if rel_score else None,
        "P": p_score,
        "ZP": round(zp, 1) if zp else None,
        "ZP_norm": round(zp_norm, 1) if zp_norm else None,
    }


def render_table(matches: list, limit: int | None = None) -> str:
    """Render a rich-style comparison table."""
    lines = []
    lines.append("")
    lines.append("                          Doug Score vs MotorGeek Composite")
    lines.append("=" * 110)
    header = (
        f"{'#':>3} {'Car':<28} {'Doug':>5} {'Weekend':>8} {'Daily':>6} "
        f"{'Our Comp':>9} {'Q':>4} {'R':>4} {'P':>4} {'ZP':>6} {'Match':>6}"
    )
    lines.append(header)
    lines.append("-" * 110)

    for i, (ds, car, conf) in enumerate(matches[:limit] if limit else matches, 1):
        car_label = f"{ds['year']} {ds['make']} {ds['model']}"[:28]
        weekend = ds["weekend_total"]
        daily = ds["daily_total"]
        dougscore = ds["dougscore"]

        if car is None:
            our_comp = "N/A"
            q = r = p = zp = "—"
        else:
            br = get_composite_breakdown(load_db(), car["id"])
            if br is None:
                our_comp = "N/A"
                q = r = p = zp = "—"
            else:
                our_comp = f"{br['composite']:.1f}"
                q = f"{br['Q']:.0f}" if br["Q"] else "—"
                r = f"{br['R']:.0f}" if br["R"] else "—"
                p = f"{br['P']:.0f}" if br["P"] else "—"
                zp = f"{br['ZP']:.0f}" if br["ZP"] else "—"

        match_pct = f"{conf*100:.0f}%" if conf > 0 else "—"
        lines.append(
            f"{i:>3} {car_label:<28} {dougscore:>5} {weekend:>8} {daily:>6} "
            f"{our_comp:>9} {q:>4} {r:>4} {p:>4} {zp:>6} {match_pct:>6}"
        )

    lines.append("-" * 110)
    return "\n".join(lines)


def render_subscore_breakdown(matches: list, limit: int | None = None) -> str:
    """Show Doug Score sub-score breakdown for matched cars."""
    lines = []
    lines.append("")
    lines.append("                          Doug Score Sub-Score Breakdown")
    lines.append("=" * 110)
    header = (
        f"{'#':>3} {'Car':<28} {'Sty':>4} {'Acc':>4} {'Han':>4} {'Fun':>4} {'Coo':>4} "
        f"{'Fea':>4} {'Com':>4} {'Qua':>4} {'Pra':>4} {'Val':>4} {'Tot':>4}"
    )
    lines.append(header)
    lines.append("-" * 110)

    for i, (ds, car, conf) in enumerate(matches[:limit] if limit else matches, 1):
        car_label = f"{ds['year']} {ds['make']} {ds['model']}"[:28]
        lines.append(
            f"{i:>3} {car_label:<28} "
            f"{ds['styling']:>4} {ds['acceleration']:>4} {ds['handling']:>4} "
            f"{ds['fun_factor']:>4} {ds['cool_factor']:>4} "
            f"{ds['features']:>4} {ds['comfort']:>4} {ds['quality']:>4} "
            f"{ds['practicality']:>4} {ds['value']:>4} "
            f"{ds['dougscore']:>4}"
        )

    lines.append("-" * 110)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Doug Score comparison")
    parser.add_argument("--limit", type=int, default=None, help="Limit output rows")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--subscores", action="store_true", help="Show sub-score breakdown")
    parser.add_argument("--min-match", type=float, default=0.0, help="Min match confidence 0-1")
    args = parser.parse_args()

    dougscore = load_dougscore()
    db = load_db()
    matches = match_cars(dougscore, db)

    # Filter by min match
    if args.min_match > 0:
        matches = [m for m in matches if m[2] >= args.min_match]

    if args.json:
        out = []
        for ds, car, conf in matches:
            entry = {
                "dougscore_entry": ds,
                "match_confidence": conf,
                "db_car": None,
            }
            if car is not None:
                br = get_composite_breakdown(db, car["id"])
                entry["db_car"] = {
                    "id": car["id"],
                    "year_start": car["year_start"],
                    "make": car["make"],
                    "model": car["model"],
                    "body_style": car["body_style"],
                    "motorgeek_breakdown": br,
                }
            out.append(entry)
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    # Sort by Doug Score descending
    matches.sort(key=lambda m: -m[0]["dougscore"])

    print(render_table(matches, args.limit))
    if args.subscores:
        print(render_subscore_breakdown(matches, args.limit))

    # Summary stats
    matched_with_data = [m for m in matches if m[1] is not None]
    print(f"\nMatched: {len(matched_with_data)} / {len(dougscore)} Doug Score entries to DB cars")
    unmatched = [m for m in matches if m[1] is None]
    if unmatched:
        print("Unmatched:")
        for ds, _, _ in unmatched:
            print(f"  {ds['year']} {ds['make']} {ds['model']}")


if __name__ == "__main__":
    main()

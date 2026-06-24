"""Compare v2 vs v3 composite scores for the 27 cars that have Dougscore data.

Runs both composite formulas side-by-side and outputs a comparison table
showing how each car's score changes when Dougscore becomes a 20% dimension
(instead of being absent). This is the answer to the user's question:
"what does the weighted numbers reveal?"

Output: a plain-text table sorted by |v3 - v2| descending, so the cars
where the formula change has the biggest impact are at the top.
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from motorgeek.core.calculators.composite import (
    WEIGHTS,
    WEIGHTS_V3,
    compute_composite,
    compute_composite_v3,
)


def main() -> None:
    conn = sqlite3.connect(str(ROOT / "data" / "motorgeek.db"))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Load the 33 Doug Score entries
    import json
    dougscore_path = ROOT / "data" / "dougscore_anchors.json"
    doug_list = json.loads(dougscore_path.read_text(encoding="utf-8"))

    # Match Doug Score entries to DB cars (fuzzy: make + normalized model + year)
    def match_db(ds_entry):
        ds_make = ds_entry["make"].lower()
        ds_model_norm = ds_entry["model"].lower().split("(")[0].strip()
        ds_year = ds_entry["year"]
        cur.execute(
            "SELECT id, year_start, make, model FROM cars WHERE LOWER(make) = ?",
            (ds_make,),
        )
        cands = cur.fetchall()
        scored = []
        for c in cands:
            c_model_norm = c["model"].lower().split("(")[0].strip()
            if c_model_norm == ds_model_norm:
                yr_diff = abs(c["year_start"] - ds_year)
                scored.append((10 - yr_diff, c))
            elif ds_model_norm in c_model_norm or c_model_norm in ds_model_norm:
                yr_diff = abs(c["year_start"] - ds_year)
                scored.append((5 - yr_diff, c))
        if scored:
            scored.sort(key=lambda x: (-x[0], x[1]["id"]))
            return scored[0][1]
        return None

    # For each matched car, compute v2 and v3 composites
    print(f"=== v2 vs v3 composite comparison for {len(doug_list)} Doug Score cars ===\n")
    print(f"v2 weights: Quality={WEIGHTS['quality']:.0%}, Reliability={WEIGHTS['reliability']:.0%}, "
          f"Practicality={WEIGHTS['practicality']:.0%}, Performance={WEIGHTS['performance']:.0%}")
    print(f"v3 weights: Quality={WEIGHTS_V3['quality']:.0%}, Reliability={WEIGHTS_V3['reliability']:.0%}, "
          f"Dougscore={WEIGHTS_V3['dougscore']:.0%}, Practicality={WEIGHTS_V3['practicality']:.0%}, "
          f"Performance={WEIGHTS_V3['performance']:.0%}")
    print()
    header = (
        f"{'#':>3} {'Car':<32} {'v2':>5} {'v3':>5} {'diff':>6} "
        f"{'Q':>4} {'R':>4} {'D':>4} {'P':>4} {'Z':>4} {'year':>4}"
    )
    print(header)
    print("-" * len(header))

    rows = []
    for ds in doug_list:
        car = match_db(ds)
        if car is None:
            continue

        # Fetch Q, R, P, ZP for this car
        cur.execute("SELECT q_score FROM build_quality WHERE car_id = ?", (car["id"],))
        row = cur.fetchone()
        q = row["q_score"] if row and row["q_score"] else None

        cur.execute("SELECT reliability_score FROM reliability WHERE car_id = ?", (car["id"],))
        row = cur.fetchone()
        r = row["reliability_score"] if row and row["reliability_score"] else None

        # Practicality v2 (cargo + body style + v2 bonuses)
        cur.execute("""
            SELECT pt.cargo_volume_liters, c.body_style,
                   d.cargo_volume_liters_seats_down, d.seat_count,
                   d.rear_legroom_mm, d.tow_capacity_kg
            FROM cars c
            LEFT JOIN powertrain_ice pt ON pt.car_id = c.id
            LEFT JOIN dimensions d ON d.car_id = c.id
            WHERE c.id = ?
        """, (car["id"],))
        prow = cur.fetchone()
        cargo = (prow["cargo_volume_liters"] if prow else 0) or 0
        body = ((prow["body_style"] if prow else "") or "").lower()
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
        if body in ("wagon", "estate"):
            tier = min(10, tier + 1)
        if prow and prow["cargo_volume_liters_seats_down"] and prow["cargo_volume_liters_seats_down"] > 1500:
            tier = min(10, tier + 0.5)
        if prow and prow["seat_count"] and prow["seat_count"] >= 7:
            tier = min(10, tier + 0.5)
        if prow and prow["rear_legroom_mm"] and prow["rear_legroom_mm"] > 950:
            tier = min(10, tier + 0.5)
        if prow and prow["tow_capacity_kg"] and prow["tow_capacity_kg"] > 2000:
            tier = min(10, tier + 0.5)
        p = tier * 10

        # ZP
        cur.execute("SELECT zeperfs_index FROM zeperfs_indices WHERE car_id = ?", (car["id"],))
        row = cur.fetchone()
        zp_raw = row["zeperfs_index"] if row and row["zeperfs_index"] else None
        zp_norm = min(100.0, zp_raw / 3.0) if zp_raw else None

        ds_score = ds["dougscore"]

        v2 = compute_composite(q, r, p, zp_norm)
        v3 = compute_composite_v3(q, r, ds_score, p, zp_norm)

        if v2 is None and v3 is None:
            continue

        diff = (v3 - v2) if (v2 is not None and v3 is not None) else None
        rows.append({
            "car": car,
            "year": ds["year"],
            "v2": v2,
            "v3": v3,
            "diff": diff,
            "Q": q or 0, "R": r or 0, "D": ds_score,
            "P": p, "Z": zp_norm or 0,
        })

    # Sort by |diff| descending to show biggest changes first
    rows.sort(key=lambda r: -abs(r["diff"]) if r["diff"] is not None else 0)

    for i, row in enumerate(rows, 1):
        car_label = f"{row['year']} {row['car']['make']} {row['car']['model']}"[:32]
        v2_s = f"{row['v2']:.1f}" if row["v2"] is not None else "N/A"
        v3_s = f"{row['v3']:.1f}" if row["v3"] is not None else "N/A"
        diff_s = f"{row['diff']:+.1f}" if row["diff"] is not None else "N/A"
        # Color hint: positive diff means v3 > v2 (Doug lifted the score)
        sign = "+" if (row["diff"] is not None and row["diff"] > 0) else ("" if row["diff"] is None else "")
        print(f"{i:>3} {car_label:<32} {v2_s:>5} {v3_s:>5} {diff_s:>6} "
              f"{row['Q']:>4.0f} {row['R']:>4.0f} {row['D']:>4} {row['P']:>4.0f} "
              f"{row['Z']:>4.0f} {row['year']:>4}")

    print("-" * len(header))
    matched = len(rows)
    print(f"\nMatched: {matched}/{len(doug_list)} Doug Score entries to DB cars")

    # Summary stats
    v2_vals = [r["v2"] for r in rows if r["v2"] is not None]
    v3_vals = [r["v3"] for r in rows if r["v3"] is not None]
    diffs = [r["diff"] for r in rows if r["diff"] is not None]
    if diffs:
        avg_diff = sum(diffs) / len(diffs)
        print(f"v2 mean: {sum(v2_vals)/len(v2_vals):.1f}")
        print(f"v3 mean: {sum(v3_vals)/len(v3_vals):.1f}")
        print(f"v3-v2 mean: {avg_diff:+.2f} (range {min(diffs):+.1f} to {max(diffs):+.1f})")
        pos = sum(1 for d in diffs if d > 0)
        neg = sum(1 for d in diffs if d < 0)
        zero = sum(1 for d in diffs if d == 0)
        print(f"v3 > v2: {pos} cars, v3 < v2: {neg} cars, v3 = v2: {zero} cars")

    conn.close()


if __name__ == "__main__":
    main()

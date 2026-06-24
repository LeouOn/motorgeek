"""Show top 30 cars in the DB by v3 composite (40Q/20R/20Doug/10P/10Z).

Computes the v3 composite for every car that has a dougscore (115/253).
For cars without dougscore, v3 returns None -- those cars can only be
ranked by v2 (40Q/30R/15P/15Z). We show both views.

Uses the OFFICIAL `compute_practicality_for_car_v2` function from
`motorgeek.core.calculators.practicality` (which applies body-style
fallback when real cargo data is missing, plus the coupe penalty for
2-door cars). This matches the composite calculator's actual scoring.

Output:
  1. v3 top 30 (cars with dougscore -- "the weights we set")
  2. v2 top 30 for context (all 253 cars)
  3. Coverage stats
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
from motorgeek.core.calculators.practicality import compute_practicality_for_car_v2
from motorgeek.core.models import Car, Dimensions, PowertrainEV, PowertrainICE


def _row_to_car(row) -> Car:
    """Convert a SQLite Row into a minimal Car-like object."""
    car = Car()
    car.id = row["id"]
    car.make = row["make"]
    car.model = row["model"]
    car.year_start = row["year_start"]
    car.body_style = row["body_style"]
    car.dougscore = row["dougscore"]
    return car


def _row_to_powertrain_ice(row) -> PowertrainICE | None:
    """Build a PowertrainICE-like object if cargo data exists."""
    if row["cargo_volume_liters"] is None:
        return None
    pt = PowertrainICE()
    pt.cargo_volume_liters = row["cargo_volume_liters"]
    return pt


def _row_to_dimensions(row) -> Dimensions | None:
    """Build a Dimensions-like object if any enrichment field is set."""
    fields = ["cargo_volume_liters_seats_down", "seat_count", "rear_legroom_mm", "tow_capacity_kg"]
    if all(row[f] is None for f in fields):
        return None
    d = Dimensions()
    d.cargo_volume_liters_seats_down = row["cargo_volume_liters_seats_down"]
    d.seat_count = row["seat_count"]
    d.rear_legroom_mm = row["rear_legroom_mm"]
    d.tow_capacity_kg = row["tow_capacity_kg"]
    return d


def main() -> None:
    conn = sqlite3.connect(str(ROOT / "data" / "motorgeek.db"))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Load ALL cars + their practicality-related fields in one query.
    cur.execute("""
        SELECT c.id, c.year_start, c.make, c.model, c.body_style, c.dougscore,
               pt.cargo_volume_liters,
               d.cargo_volume_liters_seats_down, d.seat_count,
               d.rear_legroom_mm, d.tow_capacity_kg
        FROM cars c
        LEFT JOIN powertrain_ice pt ON pt.car_id = c.id
        LEFT JOIN dimensions d ON d.car_id = c.id
    """)
    car_rows = cur.fetchall()

    results = []
    for car_row in car_rows:
        car_id = car_row["id"]

        # Quality
        cur.execute("SELECT q_score FROM build_quality WHERE car_id = ?", (car_id,))
        row = cur.fetchone()
        q = row["q_score"] if row and row["q_score"] else None

        # Reliability
        cur.execute("SELECT reliability_score FROM reliability WHERE car_id = ?", (car_id,))
        row = cur.fetchone()
        r = row["reliability_score"] if row and row["reliability_score"] else None

        # Practicality -- using OFFICIAL formula (body-style fallback + coupe penalty)
        car_obj = _row_to_car(car_row)
        ice_obj = _row_to_powertrain_ice(car_row)
        dim_obj = _row_to_dimensions(car_row)
        p, _bonuses = compute_practicality_for_car_v2(car_obj, ice_obj, None, dim_obj)

        # ZP
        cur.execute("SELECT zeperfs_index FROM zeperfs_indices WHERE car_id = ?", (car_id,))
        row = cur.fetchone()
        zp_raw = row["zeperfs_index"] if row and row["zeperfs_index"] else None
        zp_norm = min(100.0, zp_raw / 3.0) if zp_raw else None

        ds = car_row["dougscore"]

        v2 = compute_composite(q, r, p, zp_norm)
        v3 = compute_composite_v3(q, r, ds, p, zp_norm)

        results.append({
            "id": car_id,
            "year": car_row["year_start"],
            "make": car_row["make"],
            "model": car_row["model"],
            "body": car_row["body_style"] or "",
            "v2": v2,
            "v3": v3,
            "Q": q, "R": r, "D": ds, "P": p, "Z": zp_norm,
        })

    # ===== v3 TOP 30 (cars with dougscore) =====
    v3_cars = [r for r in results if r["v3"] is not None]
    v3_cars.sort(key=lambda r: -r["v3"])

    print("=" * 110)
    print("TOP 30 BY v3 COMPOSITE (40Q / 20R / 20Doug / 10P / 10Z)")
    print(f"  Covers {len(v3_cars)} of {len(car_rows)} cars (those with dougscore)")
    print("=" * 110)
    header = (f"{'#':>3} {'v3':>5} {'Car':<38} {'Q':>5} {'R':>5} {'D':>4} {'P':>5} {'Z':>5} "
              f"{'body':<12}")
    print(header)
    print("-" * 110)
    for i, r in enumerate(v3_cars[:30], 1):
        car_label = f"{r['year']} {r['make']} {r['model']}"[:38]
        q_s = f"{r['Q']:.0f}" if r['Q'] else "--"
        r_s = f"{r['R']:.0f}" if r['R'] else "--"
        d_s = f"{r['D']:.0f}" if r['D'] else "--"
        p_s = f"{r['P']:.0f}" if r['P'] else "--"
        z_s = f"{r['Z']:.0f}" if r['Z'] else "--"
        print(f"{i:>3} {r['v3']:>5.1f} {car_label:<38} {q_s:>5} {r_s:>5} {d_s:>4} {p_s:>5} {z_s:>5} "
              f"{r['body']:<12}")

    # ===== v2 TOP 10 for context (all cars) =====
    v2_cars = [r for r in results if r["v2"] is not None]
    v2_cars.sort(key=lambda r: -r["v2"])

    print()
    print("=" * 110)
    print("TOP 10 BY v2 COMPOSITE (40Q / 30R / 15P / 15Z) -- for context")
    print(f"  Covers {len(v2_cars)} of {len(car_rows)} cars (all with >= 2 dimensions)")
    print("  Cars WITHOUT dougscore can only be ranked here")
    print("=" * 110)
    header2 = (f"{'#':>3} {'v2':>5} {'v3':>5} {'Car':<38} {'Q':>5} {'R':>5} {'D':>4} {'P':>5} {'Z':>5}")
    print(header2)
    print("-" * 110)
    for i, r in enumerate(v2_cars[:10], 1):
        car_label = f"{r['year']} {r['make']} {r['model']}"[:38]
        q_s = f"{r['Q']:.0f}" if r['Q'] else "--"
        r_s = f"{r['R']:.0f}" if r['R'] else "--"
        d_s = f"{r['D']:.0f}" if r['D'] else "--"
        p_s = f"{r['P']:.0f}" if r['P'] else "--"
        z_s = f"{r['Z']:.0f}" if r['Z'] else "--"
        v3_s = f"{r['v3']:.1f}" if r['v3'] else "n/a"
        print(f"{i:>3} {r['v2']:>5.1f} {v3_s:>5} {car_label:<38} {q_s:>5} {r_s:>5} {d_s:>4} {p_s:>5} {z_s:>5}")

    # ===== Coverage stats =====
    print()
    print("=" * 110)
    print("COVERAGE STATS")
    print("=" * 110)
    print(f"Total cars in DB          : {len(car_rows)}")
    print(f"Cars with v3 (dougscore)  : {len(v3_cars)} ({100*len(v3_cars)/len(car_rows):.1f}%)")
    print(f"Cars with v2 only         : {len([r for r in v2_cars if r['v3'] is None])}")
    print(f"Cars with neither         : {len([r for r in results if r['v2'] is None and r['v3'] is None])}")
    print()
    dim_counts = {
        "Q": sum(1 for r in results if r["Q"]),
        "R": sum(1 for r in results if r["R"]),
        "D": sum(1 for r in results if r["D"]),
        "P": sum(1 for r in results if r["P"]),
        "Z": sum(1 for r in results if r["Z"]),
    }
    print(f"Dimension coverage across all {len(car_rows)} cars:")
    for dim, count in dim_counts.items():
        print(f"  {dim}: {count}/{len(car_rows)} ({100*count/len(car_rows):.1f}%)")

    conn.close()


if __name__ == "__main__":
    main()

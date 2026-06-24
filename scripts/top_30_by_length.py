"""Show top 30 cars by v3 composite, filtered to length <= 190 inches.

A "compact" luxury filter -- excludes full-size SUVs and long sedans.
190" threshold is the boundary between mid-size and full-size for
most luxury segments (BMW X5 is 194", Audi Q7 is 199", Lexus LX is
~200", but BMW X3 is 186", Audi Q5 is 184").

Output:
  1. v3 top 30 (cars with dougscore AND length <= 190")
  2. v2 top 10 for context (all length-filtered cars with >= 2 dims)
  3. Filter coverage stats
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from motorgeek.core.calculators.composite import (
    compute_composite,
    compute_composite_v3,
)
from motorgeek.core.calculators.practicality import compute_practicality_for_car_v2
from motorgeek.core.models import Car, Dimensions, PowertrainICE


# Length threshold: 195 inches (~4953 mm). Cars at or below this are
# considered "compact to mid-size+" in the luxury segment. This catches
# compact SUVs (X3, GLC, Macan, Model Y) AND mid-size SUVs (X5, GLE,
# Cayenne) but excludes full-size luxury SUVs (X7, GLS, LX, Q7, Escalade).
LENGTH_MAX_INCHES = 195.0
MM_PER_INCH = 25.4
LENGTH_MAX_MM = LENGTH_MAX_INCHES * MM_PER_INCH  # 4953.0 mm


def _row_to_car(row) -> Car:
    car = Car()
    car.id = row["id"]
    car.make = row["make"]
    car.model = row["model"]
    car.year_start = row["year_start"]
    car.body_style = row["body_style"]
    car.dougscore = row["dougscore"]
    return car


def _row_to_powertrain_ice(row) -> PowertrainICE | None:
    if row["cargo_volume_liters"] is None:
        return None
    pt = PowertrainICE()
    pt.cargo_volume_liters = row["cargo_volume_liters"]
    return pt


def _row_to_dimensions(row) -> Dimensions | None:
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

    # Load all cars + dimensions + powertrain data in one query.
    # LEFT JOIN: include cars even if dimensions missing (length_mm = NULL).
    cur.execute("""
        SELECT c.id, c.year_start, c.make, c.model, c.body_style, c.dougscore,
               pt.cargo_volume_liters,
               d.cargo_volume_liters_seats_down, d.seat_count,
               d.rear_legroom_mm, d.tow_capacity_kg, d.length_mm
        FROM cars c
        LEFT JOIN powertrain_ice pt ON pt.car_id = c.id
        LEFT JOIN dimensions d ON d.car_id = c.id
    """)
    car_rows = cur.fetchall()

    results = []
    for car_row in car_rows:
        car_id = car_row["id"]
        length_mm = car_row["length_mm"]

        # Quality
        cur.execute("SELECT q_score FROM build_quality WHERE car_id = ?", (car_id,))
        row = cur.fetchone()
        q = row["q_score"] if row and row["q_score"] else None

        # Reliability
        cur.execute("SELECT reliability_score FROM reliability WHERE car_id = ?", (car_id,))
        row = cur.fetchone()
        r = row["reliability_score"] if row and row["reliability_score"] else None

        # Practicality (official formula)
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
            "length_mm": length_mm,
        })

    # Filter: length <= 190" (4826 mm) OR length is NULL (include unknown
    # so we don't accidentally drop them silently).
    filtered = [r for r in results if r["length_mm"] is None or r["length_mm"] <= LENGTH_MAX_MM]
    excluded = [r for r in results if r["length_mm"] is not None and r["length_mm"] > LENGTH_MAX_MM]

    # ===== v3 TOP 30 (filtered, with dougscore) =====
    v3_filtered = [r for r in filtered if r["v3"] is not None]
    v3_filtered.sort(key=lambda r: -r["v3"])

    print("=" * 110)
    print(f"TOP 30 BY v3 COMPOSITE (40Q / 20R / 20Doug / 10P / 10Z) -- length <= {LENGTH_MAX_INCHES:.0f}\" ({LENGTH_MAX_MM:.0f} mm)")
    print(f"  Covers {len(v3_filtered)} of {len(results)} total cars (length-filtered, with dougscore)")
    print("=" * 110)
    header = (f"{'#':>3} {'v3':>5} {'Car':<32} {'Q':>4} {'R':>4} {'D':>3} {'P':>4} {'Z':>4} "
              f"{'len(mm)':>8} {'body':<12}")
    print(header)
    print("-" * 110)
    for i, r in enumerate(v3_filtered[:30], 1):
        car_label = f"{r['year']} {r['make']} {r['model']}"[:32]
        q_s = f"{r['Q']:.0f}" if r['Q'] else "--"
        r_s = f"{r['R']:.0f}" if r['R'] else "--"
        d_s = f"{r['D']:.0f}" if r['D'] else "--"
        p_s = f"{r['P']:.0f}" if r['P'] else "--"
        z_s = f"{r['Z']:.0f}" if r['Z'] else "--"
        len_s = f"{r['length_mm']:.0f}" if r['length_mm'] else "--"
        print(f"{i:>3} {r['v3']:>5.1f} {car_label:<32} {q_s:>4} {r_s:>4} {d_s:>3} {p_s:>4} {z_s:>4} "
              f"{len_s:>8} {r['body']:<12}")

    # ===== v2 TOP 10 for context (all length-filtered cars) =====
    v2_filtered = [r for r in filtered if r["v2"] is not None]
    v2_filtered.sort(key=lambda r: -r["v2"])

    print()
    print("=" * 110)
    print(f"TOP 10 BY v2 COMPOSITE (40Q / 30R / 15P / 15Z) -- length <= {LENGTH_MAX_INCHES:.0f}\" -- for context")
    print(f"  Covers {len(v2_filtered)} of {len(results)} total cars (length-filtered, all with >= 2 dims)")
    print("=" * 110)
    header2 = (f"{'#':>3} {'v2':>5} {'v3':>5} {'Car':<32} {'Q':>4} {'R':>4} {'D':>3} {'P':>4} {'Z':>4} {'len(mm)':>8}")
    print(header2)
    print("-" * 110)
    for i, r in enumerate(v2_filtered[:10], 1):
        car_label = f"{r['year']} {r['make']} {r['model']}"[:32]
        q_s = f"{r['Q']:.0f}" if r['Q'] else "--"
        r_s = f"{r['R']:.0f}" if r['R'] else "--"
        d_s = f"{r['D']:.0f}" if r['D'] else "--"
        p_s = f"{r['P']:.0f}" if r['P'] else "--"
        z_s = f"{r['Z']:.0f}" if r['Z'] else "--"
        v3_s = f"{r['v3']:.1f}" if r['v3'] else "n/a"
        len_s = f"{r['length_mm']:.0f}" if r['length_mm'] else "--"
        print(f"{i:>3} {r['v2']:>5.1f} {v3_s:>5} {car_label:<32} {q_s:>4} {r_s:>4} {d_s:>3} {p_s:>4} {z_s:>4} {len_s:>8}")

    # ===== Filter stats =====
    print()
    print("=" * 110)
    print("FILTER STATS")
    print("=" * 110)
    print(f"Length threshold          : {LENGTH_MAX_INCHES:.0f}\" = {LENGTH_MAX_MM:.0f} mm")
    print(f"Total cars in DB          : {len(results)}")
    print(f"Cars with length data     : {len([r for r in results if r['length_mm'] is not None])}")
    print(f"Cars with NULL length     : {len([r for r in results if r['length_mm'] is None])} (included by default)")
    print(f"Cars <= {LENGTH_MAX_INCHES:.0f}\"            : {len(filtered)}")
    print(f"Cars >  {LENGTH_MAX_INCHES:.0f}\" (excluded)  : {len(excluded)}")
    print()
    print(f"v3 rankings:")
    print(f"  All cars with dougscore       : {len([r for r in results if r['v3'] is not None])}")
    print(f"  Length-filtered + dougscore   : {len(v3_filtered)}")
    print()
    print(f"v2 rankings:")
    print(f"  All cars with >= 2 dims       : {len([r for r in results if r['v2'] is not None])}")
    print(f"  Length-filtered + >= 2 dims   : {len(v2_filtered)}")
    print()
    # Show what got excluded (top 10 by length)
    excluded.sort(key=lambda r: -(r["length_mm"] or 0))
    print(f"Top 10 longest cars EXCLUDED from this view:")
    for r in excluded[:10]:
        car_label = f"{r['year']} {r['make']} {r['model']}"[:32]
        v3_s = f"v3={r['v3']:.1f}" if r['v3'] else "v3=n/a"
        len_in = r['length_mm'] / MM_PER_INCH if r['length_mm'] else 0
        print(f"  {car_label:<32} {len_in:>5.1f}\"  ({r['length_mm']:.0f} mm)  {v3_s}")

    conn.close()


if __name__ == "__main__":
    main()

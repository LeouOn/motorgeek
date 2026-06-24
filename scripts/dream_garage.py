"""Build the dream garage -- one car from each role, optimized by v3.

Selects one car per role from the DB and ranks by v3 composite.
"""
import sqlite3
import sys
from pathlib import Path

ROOT = Path('C:/Users/llama/OneDrive/proj/motorgeek')
sys.path.insert(0, str(ROOT))

from motorgeek.core.calculators.composite import compute_composite, compute_composite_v3
from motorgeek.core.calculators.practicality import compute_practicality_for_car_v2
from motorgeek.core.models import Car, Dimensions, PowertrainICE


def main():
    conn = sqlite3.connect(str(ROOT / 'data' / 'motorgeek.db'))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT c.id, c.year_start, c.make, c.model, c.variant, c.body_style, c.dougscore,
               pt.cargo_volume_liters,
               d.cargo_volume_liters_seats_down, d.seat_count,
               d.rear_legroom_mm, d.tow_capacity_kg, d.length_mm,
               b.q_score, r.reliability_score, z.zeperfs_index
        FROM cars c
        LEFT JOIN powertrain_ice pt ON pt.car_id = c.id
        LEFT JOIN dimensions d ON d.car_id = c.id
        LEFT JOIN build_quality b ON b.car_id = c.id
        LEFT JOIN reliability r ON r.car_id = c.id
        LEFT JOIN zeperfs_indices z ON z.car_id = c.id
    """)
    all_rows = cur.fetchall()

    cars = []
    for r in all_rows:
        car = Car()
        car.id = r['id']
        car.year_start = r['year_start']
        car.make = r['make']
        car.model = r['model']
        car.body_style = r['body_style']
        car.dougscore = r['dougscore']
        pt = PowertrainICE()
        pt.cargo_volume_liters = r['cargo_volume_liters']
        dim = Dimensions()
        dim.cargo_volume_liters_seats_down = r['cargo_volume_liters_seats_down']
        dim.seat_count = r['seat_count']
        dim.rear_legroom_mm = r['rear_legroom_mm']
        dim.tow_capacity_kg = r['tow_capacity_kg']
        p, _ = compute_practicality_for_car_v2(car, pt, None, dim)
        zp_norm = min(100.0, r['zeperfs_index'] / 3.0) if r['zeperfs_index'] else None
        v3 = compute_composite_v3(r['q_score'], r['reliability_score'], r['dougscore'], p, zp_norm)
        v2 = compute_composite(r['q_score'], r['reliability_score'], p, zp_norm)
        cars.append({
            'id': r['id'], 'year': r['year_start'], 'make': r['make'],
            'model': r['model'], 'variant': r['variant'] or '',
            'body': r['body_style'],
            'q': r['q_score'], 'r': r['reliability_score'], 'p': p,
            'z_raw': r['zeperfs_index'], 'z': zp_norm,
            'd': r['dougscore'],
            'v3': v3, 'v2': v2,
            'length_mm': r['length_mm'], 'seat_count': r['seat_count'],
        })

    def pick_role(filter_fn, sort_key, n=3):
        candidates = [c for c in cars if filter_fn(c)]
        candidates.sort(key=sort_key)
        return candidates[:n]

    def fmt(v):
        return f"{v:.0f}" if v is not None else "--"

    roles_def = [
        ("Daily driver sedan (efficient, comfortable, reliable)",
         lambda c: c['body'] == 'sedan' and c['d'] is not None and (c['length_mm'] or 9999) < 4900,
         lambda c: -(c['v3'] or 0)),
        ("Sport sedan (ZP >= 130, M/AMG/RS territory)",
         lambda c: c['body'] == 'sedan' and c['d'] is not None and (c['z_raw'] or 0) >= 130,
         lambda c: -(c['v3'] or 0)),
        ("Sports car / coupe (weekend fun)",
         lambda c: c['body'] == 'coupe' and c['d'] is not None,
         lambda c: -(c['v3'] or 0)),
        ("Compact luxury SUV (< 4750mm, city-friendly)",
         lambda c: c['body'] == 'SUV' and c['d'] is not None and (c['length_mm'] or 0) < 4750,
         lambda c: -(c['v3'] or 0)),
        ("Family hauler SUV (3-row, seat_count >= 7)",
         lambda c: c['body'] == 'SUV' and c['d'] is not None and (c['seat_count'] or 0) >= 7,
         lambda c: -(c['v3'] or 0)),
        ("Off-road / adventure (Land Cruiser family, G-Wagon, 4Runner)",
         lambda c: c['d'] is not None and (
             ('Land Cruiser' in (c['model'] or '')) or
             ('GX' in (c['model'] or '') and c['make'] == 'Lexus') or
             ('4Runner' in (c['model'] or '')) or
             ('G550' in (c['model'] or '') or 'G63' in (c['model'] or ''))
         ),
         lambda c: -(c['v3'] or 0)),
        ("Track-day weapon (highest ZP raw)",
         lambda c: c['d'] is not None and c['z_raw'] is not None,
         lambda c: -(c['z_raw'] or 0)),
        ("Flagship luxury sedan (best Q + R)",
         lambda c: c['body'] == 'sedan' and c['d'] is not None,
         lambda c: -((c['q'] or 0) + (c['r'] or 0))),
        ("Doug's favorite (highest single dougscore)",
         lambda c: c['d'] is not None,
         lambda c: -(c['d'] or 0)),
        ("Hidden gem (mainstream cheap-make, high v3)",
         lambda c: c['d'] is not None and c['make'] in ('Mazda', 'Subaru', 'Hyundai', 'Kia', 'Volkswagen', 'Honda'),
         lambda c: -(c['v3'] or 0)),
    ]

    print("=" * 100)
    print("THE DREAM GARAGE -- one car from each role, picked from the DB by v3 composite")
    print("=" * 100)
    print()

    selected = []
    for role_name, filter_fn, sort_key in roles_def:
        top = pick_role(filter_fn, sort_key, n=3)
        if not top:
            print(f"### {role_name}")
            print("   (no cars matched)")
            print()
            continue
        best = top[0]
        selected.append((role_name, best))
        v3_str = f"v3={best['v3']:.1f}" if best['v3'] else f"v2={best['v2']:.1f}"
        d_str = f" D={best['d']}" if best['d'] else " D=--"
        len_str = f"  {best['length_mm']:.0f}mm" if best['length_mm'] else ""
        print(f"### {role_name}")
        print(f"   PICK: {best['year']} {best['make']} {best['model']}")
        if best['variant']:
            print(f"         ({best['variant']})")
        print(f"         {v3_str}{d_str}  Q={fmt(best['q'])} R={fmt(best['r'])} P={fmt(best['p'])} Z={fmt(best['z'])}{len_str}")
        if len(top) > 1:
            for c in top[1:]:
                v3_str2 = f"v3={c['v3']:.1f}" if c['v3'] else f"v2={c['v2']:.1f}"
                d_str2 = f" D={c['d']}" if c['d'] else " D=--"
                len_str2 = f"  {c['length_mm']:.0f}mm" if c['length_mm'] else ""
                print(f"   alt:  {c['year']} {c['make']} {c['model']}  {v3_str2}{d_str2}  Q={fmt(c['q'])} R={fmt(c['r'])} P={fmt(c['p'])}{len_str2}")
        print()

    print("=" * 100)
    print("DREAM GARAGE SUMMARY")
    print("=" * 100)
    makes = {}
    for role_name, car in selected:
        makes[car['make']] = makes.get(car['make'], 0) + 1
    print(f"Brand distribution (10 slots):")
    for make, n in sorted(makes.items(), key=lambda x: -x[1]):
        print(f"  {make:<14} {n} cars")
    bodies = {}
    for role_name, car in selected:
        bodies[car['body']] = bodies.get(car['body'], 0) + 1
    print(f"Body style mix:")
    for body, n in bodies.items():
        print(f"  {body:<14} {n} cars")
    valid_v3 = [c['v3'] for _, c in selected if c['v3']]
    if valid_v3:
        print(f"\nv3 sum: {sum(valid_v3):.1f}  avg: {sum(valid_v3)/len(valid_v3):.1f}")
    short_count = sum(1 for _, c in selected if c['length_mm'] and c['length_mm'] < 4826)
    long_count = sum(1 for _, c in selected if c['length_mm'] and c['length_mm'] >= 4826)
    no_length = sum(1 for _, c in selected if not c['length_mm'])
    print(f"\nLength distribution:")
    print(f"  < 190\" (city-friendly): {short_count} cars")
    print(f"  >= 190\" (needs real garage): {long_count} cars")
    if no_length:
        print(f"  unknown length: {no_length} cars")

    conn.close()


if __name__ == "__main__":
    main()
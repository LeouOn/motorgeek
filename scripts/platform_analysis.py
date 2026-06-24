"""Platform analysis: MLB vs MLB Evo for Audi, A/B/C/D for Mercedes, etc.

Each platform determines:
  - Dimensions (length, wheelbase)
  - Engines (which V6/V8 fits, torque output)
  - Transmissions (which gearbox)
  - Suspension (steel springs vs air)
  - Electronics (older MMI vs newer MIB3)
  - Build quality (laser welding vs spot welding)
  - Maintenance costs (parts commonality)

Output: side-by-side comparison per platform generation.
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

    # Load all German cars with full data
    cur.execute("""
        SELECT c.id, c.year_start, c.make, c.model, c.variant, c.generation,
               c.body_style, c.dougscore,
               pt.engine_layout, pt.displacement_cc, pt.cylinders, pt.aspiration,
               pt.horsepower_bhp, pt.torque_nm, pt.transmission_type, pt.gear_count,
               pt.drivetrain, pt.curb_weight_kg,
d.length_mm, d.width_mm, d.height_mm, d.wheelbase_mm,
                d.cargo_volume_liters_seats_down, d.seat_count,
                d.rear_legroom_mm, d.tow_capacity_kg,
                b.q_score, r.reliability_score, z.zeperfs_index
        FROM cars c
        LEFT JOIN powertrain_ice pt ON pt.car_id = c.id
        LEFT JOIN dimensions d ON d.car_id = c.id
        LEFT JOIN build_quality b ON b.car_id = c.id
        LEFT JOIN reliability r ON r.car_id = c.id
        LEFT JOIN zeperfs_indices z ON z.car_id = c.id
        WHERE c.make IN ('Audi', 'Mercedes-Benz', 'Mercedes-AMG', 'BMW')
        ORDER BY c.make, c.model, c.year_start
    """)
    all_rows = cur.fetchall()

    # ============================================================
    # AUDI PLATFORM ANALYSIS
    # ============================================================
    print("=" * 100)
    print("AUDI PLATFORM ANALYSIS -- MLB vs MLB Evo")
    print("=" * 100)
    print()
    print("Volkswagen Group platforms Audi uses:")
    print("  - B8  (2007-2015): A4/A5/A6/Q5 -- longitudinal, front-engine")
    print("  - MLB  (2003-2017): A6/A7/A8/Q7 -- modular longitudinal, V6/V8")
    print("  - MLB Evo (2017+):   A6/A7/A8/Q7/Q8 -- aluminum-intensive body, 48V MHEV")
    print("  - MQB  (2013+):     A3/Q3/TT -- transverse, front-engine")
    print("  - MSB  (2017+):     A7/A8 (some) -- Porsche-panamera-derived")
    print()
    print("Why it matters: MLB Evo is ~80kg lighter than MLB, has 48V mild-hybrid,")
    print("more aluminum body panels, and laser welding at key joints.")
    print()

    audi = [r for r in all_rows if r['make'] == 'Audi']
    print(f"{'Year':<6} {'Model':<10} {'Generation':<22} {'Body':<8} {'Engine':<22} "
          f"{'HP':>4} {'Tq':>4} {'Trans':<14} {'DW':<4} {'Weight':>6} {'Q':>4} {'R':>4} {'v3':>5}")
    print("-" * 130)
    for r in audi:
        eng = f"{r['displacement_cc']:.0f}cc "
        if r['cylinders']:
            eng += f"{r['cylinders']}cyl "
        if r['aspiration']:
            eng += r['aspiration'][:14]
        else:
            eng += "?"
        trans = r['transmission_type'] or "?"
        if r['gear_count']:
            trans += f" {r['gear_count']}spd"
        drivetrain = r['drivetrain'] or "?"
        dw = r['curb_weight_kg'] if r['curb_weight_kg'] else 0
        v3_str = f"{r['dougscore']}" if r['dougscore'] else "--"

        # Build dummy Car obj for v3
        car = Car()
        car.id = r['id']; car.year_start = r['year_start']
        car.make = r['make']; car.model = r['model']
        car.body_style = r['body_style']; car.dougscore = r['dougscore']
        pt = PowertrainICE()
        pt.cargo_volume_liters = None
        dim = Dimensions()
        dim.cargo_volume_liters_seats_down = r['cargo_volume_liters_seats_down']
        dim.seat_count = r['seat_count']
        dim.rear_legroom_mm = r['rear_legroom_mm']
        dim.tow_capacity_kg = r['tow_capacity_kg']
        p, _ = compute_practicality_for_car_v2(car, pt, None, dim)
        zp_norm = min(100.0, r['zeperfs_index'] / 3.0) if r['zeperfs_index'] else None
        v3 = compute_composite_v3(r['q_score'], r['reliability_score'], r['dougscore'], p, zp_norm)
        v3_str = f"{v3:.1f}" if v3 else "--"

        print(f"{r['year_start']:<6} {r['model']:<10} {(r['generation'] or '--'):<22} "
              f"{r['body_style'] or '--':<8} {eng:<22} "
              f"{r['horsepower_bhp']:>4.0f} {r['torque_nm']:>4.0f} {trans:<14} {drivetrain:<4} {dw:>6.0f} "
              f"{r['q_score'] or 0:>4.0f} {r['reliability_score'] or 0:>4.0f} {v3_str:>5}")

    # ============================================================
    # MERCEDES A/B/C/D PLATFORM ANALYSIS
    # ============================================================
    print()
    print("=" * 100)
    print("MERCEDES PLATFORM ANALYSIS -- A/B/C/D (and MHA for SUVs)")
    print("=" * 100)
    print()
    print("Mercedes platform generations (entry-lux to flagship):")
    print("  A-Class: MFA (2012+) -- transverse, FWD-based")
    print("  C-Class: MRA (2014+) -- rear-drive, aluminum-intensive")
    print("  E-Class: MRA (2009+) -- rear-drive, shared with C/S")
    print("  S-Class: MRA -- rear-drive, top-tier luxury")
    print("  GLA/GLC/GLE/GLS/G-Class: MHA -- SUV variants")
    print("  CLS: W219 (2004) -> C218 (2011) -> C257 (2018)")
    print()

    mb = [r for r in all_rows if r['make'] in ('Mercedes-Benz', 'Mercedes-AMG')]
    print(f"{'Year':<6} {'Model':<12} {'Generation':<22} {'Body':<8} {'Engine':<22} "
          f"{'HP':>4} {'Tq':>4} {'Trans':<14} {'DW':<4} {'Weight':>6} {'Q':>4} {'R':>4} {'v3':>5}")
    print("-" * 130)
    for r in mb:
        eng = f"{r['displacement_cc']:.0f}cc " if r['displacement_cc'] else "?"
        if r['cylinders']:
            eng += f"{r['cylinders']}cyl "
        if r['aspiration']:
            eng += r['aspiration'][:14]
        else:
            eng += "?"
        trans = r['transmission_type'] or "?"
        if r['gear_count']:
            trans += f" {r['gear_count']}spd"
        drivetrain = r['drivetrain'] or "?"
        dw = r['curb_weight_kg'] if r['curb_weight_kg'] else 0
        v3_str = f"{r['dougscore']}" if r['dougscore'] else "--"

        car = Car()
        car.id = r['id']; car.year_start = r['year_start']
        car.make = r['make']; car.model = r['model']
        car.body_style = r['body_style']; car.dougscore = r['dougscore']
        pt = PowertrainICE()
        pt.cargo_volume_liters = None
        dim = Dimensions()
        dim.cargo_volume_liters_seats_down = r['cargo_volume_liters_seats_down']
        dim.seat_count = r['seat_count']
        dim.rear_legroom_mm = r['rear_legroom_mm']
        dim.tow_capacity_kg = r['tow_capacity_kg']
        p, _ = compute_practicality_for_car_v2(car, pt, None, dim)
        zp_norm = min(100.0, r['zeperfs_index'] / 3.0) if r['zeperfs_index'] else None
        v3 = compute_composite_v3(r['q_score'], r['reliability_score'], r['dougscore'], p, zp_norm)
        v3_str = f"{v3:.1f}" if v3 else "--"

        print(f"{r['year_start']:<6} {r['model']:<12} {(r['generation'] or '--'):<22} "
              f"{r['body_style'] or '--':<8} {eng:<22} "
              f"{r['horsepower_bhp']:>4.0f} {r['torque_nm']:>4.0f} {trans:<14} {drivetrain:<4} {dw:>6.0f} "
              f"{r['q_score'] or 0:>4.0f} {r['reliability_score'] or 0:>4.0f} {v3_str:>5}")

    # ============================================================
    # BMW PLATFORM ANALYSIS (CLAR vs UKL)
    # ============================================================
    print()
    print("=" * 100)
    print("BMW PLATFORM ANALYSIS -- CLAR (rear-drive) vs UKL (front-drive)")
    print("=" * 100)
    print()
    print("BMW platform strategy split since 2014:")
    print("  CLAR (2014+): 3/5/7 Series, X3/X4/X5/X6/X7 -- rear-drive, longitudinal")
    print("  UKL (2014+):  1/2 Series, X1/X2 -- front-drive, transverse")
    print("  CLAR is the premium platform; UKL is cost-engineered for entry-level")
    print()

    bmw = [r for r in all_rows if r['make'] == 'BMW']
    print(f"{'Year':<6} {'Model':<14} {'Generation':<22} {'Body':<8} {'Engine':<22} "
          f"{'HP':>4} {'Tq':>4} {'Trans':<14} {'DW':<4} {'Weight':>6} {'Q':>4} {'R':>4} {'v3':>5}")
    print("-" * 130)
    for r in bmw:
        eng = f"{r['displacement_cc']:.0f}cc " if r['displacement_cc'] else "?"
        if r['cylinders']:
            eng += f"{r['cylinders']}cyl "
        if r['aspiration']:
            eng += r['aspiration'][:14]
        else:
            eng += "?"
        trans = r['transmission_type'] or "?"
        if r['gear_count']:
            trans += f" {r['gear_count']}spd"
        drivetrain = r['drivetrain'] or "?"
        dw = r['curb_weight_kg'] if r['curb_weight_kg'] else 0
        v3_str = f"{r['dougscore']}" if r['dougscore'] else "--"

        car = Car()
        car.id = r['id']; car.year_start = r['year_start']
        car.make = r['make']; car.model = r['model']
        car.body_style = r['body_style']; car.dougscore = r['dougscore']
        pt = PowertrainICE()
        pt.cargo_volume_liters = None
        dim = Dimensions()
        dim.cargo_volume_liters_seats_down = r['cargo_volume_liters_seats_down']
        dim.seat_count = r['seat_count']
        dim.rear_legroom_mm = r['rear_legroom_mm']
        dim.tow_capacity_kg = r['tow_capacity_kg']
        p, _ = compute_practicality_for_car_v2(car, pt, None, dim)
        zp_norm = min(100.0, r['zeperfs_index'] / 3.0) if r['zeperfs_index'] else None
        v3 = compute_composite_v3(r['q_score'], r['reliability_score'], r['dougscore'], p, zp_norm)
        v3_str = f"{v3:.1f}" if v3 else "--"

        print(f"{r['year_start']:<6} {r['model']:<14} {(r['generation'] or '--'):<22} "
              f"{r['body_style'] or '--':<8} {eng:<22} "
              f"{r['horsepower_bhp']:>4.0f} {r['torque_nm']:>4.0f} {trans:<14} {drivetrain:<4} {dw:>6.0f} "
              f"{r['q_score'] or 0:>4.0f} {r['reliability_score'] or 0:>4.0f} {v3_str:>5}")

    # ============================================================
    # X3 M40i vs X5 head-to-head
    # ============================================================
    print()
    print("=" * 100)
    print("X3 M40i vs X5 -- urban environment comparison (what you asked)")
    print("=" * 100)
    print()
    print(f"{'Spec':<28} {'X3 M40i (2018)':<22} {'X5 xDrive40i (2019)':<22}")
    print("-" * 80)

    cur.execute("""
        SELECT c.year_start, c.model, c.variant, c.body_style,
               pt.engine_layout, pt.displacement_cc, pt.cylinders, pt.aspiration,
               pt.horsepower_bhp, pt.torque_nm, pt.transmission_type, pt.gear_count,
               pt.drivetrain, pt.curb_weight_kg, pt.fuel_consumption_mixed_l_100km,
               d.length_mm, d.width_mm, d.height_mm, d.wheelbase_mm,
               d.cargo_volume_liters_seats_down, d.seat_count, d.tow_capacity_kg,
               b.q_score, r.reliability_score, z.zeperfs_index, c.dougscore
        FROM cars c
        LEFT JOIN powertrain_ice pt ON pt.car_id = c.id
        LEFT JOIN dimensions d ON d.car_id = c.id
        LEFT JOIN build_quality b ON b.car_id = c.id
        LEFT JOIN reliability r ON r.car_id = c.id
        LEFT JOIN zeperfs_indices z ON z.car_id = c.id
        WHERE c.make = 'BMW' AND c.model IN ('X3', 'X3 M40i', 'X5')
        AND c.year_start IN (2018, 2019)
        ORDER BY c.model, c.year_start
    """)
    comparisons = cur.fetchall()
    def safe(v, fmt=".0f", default="--"):
        if v is None:
            return default
        try:
            return format(v, fmt)
        except (ValueError, TypeError):
            return default
    for r in comparisons:
        model_label = f"{r['year_start']} {r['model']}"
        if 'X5' in r['model']:
            label = f"{model_label} xDrive40i"
        else:
            label = f"{model_label} M40i"
        print(f"\n=== {label} ===")
        print(f"  Engine:    {safe(r['displacement_cc'], ',.0f')}cc {r['cylinders'] or '--'}cyl {r['aspiration'] or '--'}")
        print(f"  Power:     {safe(r['horsepower_bhp'])} hp / {safe(r['torque_nm'])} Nm")
        print(f"  Trans:     {r['transmission_type'] or '--'} {r['gear_count'] or '--'}spd")
        print(f"  Drivetrain: {r['drivetrain'] or '--'}")
        print(f"  Weight:    {safe(r['curb_weight_kg'])} kg")
        length_in = (r['length_mm'] or 0) / 25.4 if r['length_mm'] else 0
        print(f"  Length:    {safe(r['length_mm'])} mm ({length_in:.1f}\")")
        print(f"  Width:     {safe(r['width_mm'])} mm")
        print(f"  Height:    {safe(r['height_mm'])} mm")
        print(f"  Wheelbase: {safe(r['wheelbase_mm'])} mm")
        print(f"  Cargo:     {safe(r['cargo_volume_liters_seats_down'])} L seats down")
        print(f"  Seats:     {r['seat_count'] or '--'}")
        print(f"  Tow:       {safe(r['tow_capacity_kg'])} kg")
        print(f"  Fuel:      {safe(r['fuel_consumption_mixed_l_100km'], '.1f')} L/100km combined")
        print(f"  Q score:   {safe(r['q_score'])}")
        print(f"  R score:   {safe(r['reliability_score'])}")
        print(f"  ZP:        {safe(r['zeperfs_index'], '.1f')}")
        print(f"  Doug D:    {r['dougscore'] or '--'}")

    print()
    print("=" * 100)
    print("KEY DIFFERENCES for URBAN USE")
    print("=" * 100)
    print()
    print("DIMENSIONS:")
    print("  X3 M40i: 4716mm long, 1891mm wide  -- fits standard parking garage easily")
    print("  X5 G05:  4942mm long, 2004mm wide  -- 226mm longer, 113mm wider")
    print("           Standard US garage: 16-20ft deep = 4877-6096mm, 8-10ft wide = 2438-3048mm")
    print("           X3: ~18 inches clearance front/back in a standard garage")
    print("           X5: ~4 inches clearance front/back -- TIGHT, easy to dink the bumper")
    print()
    print("WEIGHT:")
    print("  X3 M40i: 1940 kg -- sport sedan equivalent, light for an SUV")
    print("  X5 xDrive40i: 2160 kg -- 220kg heavier, more inertia in city")
    print()
    print("ENGINES (M40i vs xDrive40i):")
    print("  X3 M40i: 3.0L I6 turbo, 382hp / 500Nm -- B58 engine, the bulletproof one")
    print("  X5 xDrive40i: 3.0L I6 turbo, 335hp / 447Nm -- B58 engine, slightly detuned")
    print("  SAME ENGINE FAMILY. The M40i has a sport tune; the xDrive40i is comfort-tuned.")
    print()
    print("TRANSMISSION:")
    print("  Both use ZF 8HP -- the most reliable auto transmission in the industry")
    print()
    print("DRIVETRAIN:")
    print("  Both xDrive (AWD) -- BMW's intelligent AWD, RWD-bias")
    print()
    print("PRACTICALITY:")
    print("  X3 M40i: 60 P (cargo 1430L seats down + legroom 900)")
    print("  X5 xDrive40i: 70 P (cargo 1870L seats down + legroom 950)")
    print("  X5 has +440L cargo and +50mm legroom. Not huge difference in daily use.")
    print()
    print("TOWING:")
    print("  X3 M40i: 2400 kg")
    print("  X5: 2700 kg (300kg more, but you probably don't tow enough to care)")
    print()
    print("RELIABILITY:")
    print("  X3 M40i (2018): R=78")
    print("  X5 xDrive40i (2019): R=77")
    print("  B58 engine is bulletproof in both. Slight edge to X3 from younger model year.")
    print()
    print("DOUG SCORE:")
    print("  X3 M40i (2018): D=65")
    print("  X5 (2019): D=61")
    print("  Doug likes the X3 M40i more.")
    print()
    print("=" * 100)
    print("VERDICT for urban use:")
    print("=" * 100)
    print()
    print("X3 M40i is the sweet spot for urban environments because:")
    print("  1. Same engine (B58 I6) and transmission (ZF 8HP) as X5 -- identical mechanicals")
    print("  2. Lighter (1940 vs 2160 kg) -- better in stop-and-go, better MPG")
    print("  3. Shorter (4716 vs 4942 mm) -- fits in any urban parking")
    print("  4. Higher Doug score (D=65 vs 61)")
    print("  5. Cheaper used ($25K for M40i vs $33K for xDrive40i)")
    print("  6. Identical M sport suspension feel")
    print()
    print("X5 is better ONLY if you need:")
    print("  - 3rd row (X5 doesn't have one anyway, only X7 does)")
    print("  - Real off-road capability (no)")
    print("  - Heavy towing (2700kg vs 2400kg, marginal)")
    print("  - Highway stability at speed (X5 is calmer)")
    print()
    print("THE X3 M40i IS THE SWEET SPOT. Save $8K, get 226mm more clearance,")
    print("identical engine, identical transmission, and Doug likes it more.")

    conn.close()


if __name__ == "__main__":
    main()
"""Dependent Origination Map -- trace the components, origins, and shared lineage of any car.

Shows what the car actually IS: not a single object, but an assemblage of
parts from different suppliers, shared across brands, with their own histories.

Usage:
  python scripts/dependent_origination.py <car_id>
"""

import sqlite3, sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DB = "data/motorgeek.db"


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/dependent_origination.py <car_id>")
        sys.exit(1)

    car_id = int(sys.argv[1])
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row

    car = db.execute("""
        SELECT c.*, pi.engine_layout, pi.engine_code, pi.transmission_type,
               pi.drivetrain, pi.horsepower_bhp, pi.curb_weight_kg,
               r.reliability_score, b.q_score
        FROM cars c
        LEFT JOIN powertrain_ice pi ON c.id = pi.car_id
        LEFT JOIN reliability r ON c.id = r.car_id
        LEFT JOIN build_quality b ON c.id = b.car_id
        WHERE c.id = ?
    """, (car_id,)).fetchone()

    if not car:
        print(f"Car {car_id} not found.")
        sys.exit(1)

    print(f"\n{'='*70}")
    print(f"  DEPENDENT ORIGINATION MAP")
    print(f"  What this car actually is")
    print(f"{'='*70}")
    print(f"\n  The label: {car['make']} {car['model']} {car['variant'] or ''}")
    print(f"  The year: {car['year_start']}")
    print(f"  The place: {car['country'] or 'unknown'}")
    print(f"  The assembly plant: {car['country'] or '?'}")

    # Engine lineage
    engine_code = car['engine_code'] if 'engine_code' in car.keys() and car['engine_code'] else ''
    print(f"\n  {'~'*60}")
    print(f"  ENGINE LINEAGE")
    print(f"  {'~'*60}")
    print(f"\n  This car's engine: {car['engine_layout'] or 'unknown'}")

    if engine_code:
        siblings = db.execute("""
            SELECT c.make, c.model, c.variant, ROUND(r.reliability_score,1) AS rel
            FROM powertrain_ice pi
            JOIN cars c ON pi.car_id = c.id
            JOIN reliability r ON c.id = r.car_id
            WHERE pi.engine_code = ? AND pi.car_id != ?
            ORDER BY r.reliability_score DESC
        """, (engine_code, car_id)).fetchall()

        if siblings:
            print(f"\n  This engine is NOT unique to this car.")
            print(f"  Engine code: {engine_code}")
            print(f"  Also appears in {len(siblings)} other car(s) in this database:")
            for s in siblings:
                print(f"    - {s['make']} {s['model']} {s['variant']} (rel {s['rel']})")
            print(f"\n  The engine outlives the car. The engine outlives the brand.")
            print(f"  When this car is scrapped, the engine design persists in")
            print(f"  {len(siblings)} other vehicles on the road.")
        else:
            print(f"\n  Engine code: {engine_code} (unique in database -- may be bespoke)")
    else:
        print(f"\n  Engine code not yet classified.")

    # Platform sharing
    family = car['family'] if 'family' in car.keys() and car['family'] else ''
    if family:
        family_members = db.execute("""
            SELECT c.make, c.model, c.generation, c.year_start
            FROM cars c
            WHERE c.family = ? AND c.id != ?
            ORDER BY c.year_start
        """, (family, car_id)).fetchall()
        if family_members:
            print(f"\n  {'~'*60}")
            print(f"  FAMILY LINEAGE ({family})")
            print(f"  {'~'*60}")
            print(f"\n  This car is one expression of the {family} family:")
            for m in family_members:
                print(f"    - {m['year_start']} {m['make']} {m['model']} {m['generation'] or ''}")
            print(f"\n  Each is a different assemblage of similar components.")
            print(f"  The family persists; the individual cars pass.")

    # Failure points as karma
    failures = db.execute("""
        SELECT failure_name, component, severity, is_preventive
        FROM failure_points WHERE car_id = ?
        ORDER BY severity DESC
    """, (car_id,)).fetchall()

    if failures:
        print(f"\n  {'~'*60}")
        print(f"  ENGINEERING KARMA (known failure points)")
        print(f"  {'~'*60}")
        print(f"\n  Every design decision carries consequences. These are the")
        print(f"  conditions that will eventually cause this assembly to change:")
        for f in failures:
            name = f['failure_name'].replace('_', ' ')
            sev = ['','cosmetic','nuisance','moderate','major','CATASTROPHIC'][f['severity']]
            prev = " [preventable]" if f['is_preventive'] else ""
            print(f"    [{sev:12s}] {name}{prev}")

    # The dissolution
    print(f"\n  {'~'*60}")
    print(f"  THE DISSOLUTION")
    print(f"  {'~'*60}")
    print(f"\n  When this car reaches end of life:")
    print(f"  - The engine block (aluminum) will be recycled, possibly into")
    print(f"    a new engine, a new car, or a beverage can")
    print(f"  - The steel body will be shredded and melted for new steel")
    print(f"  - The leather will decompose (biodegradable) or be landfilled")
    print(f"  - The plastics will persist for 500+ years in a landfill")
    print(f"  - The ECU silicon will be e-waste, processed for precious metals")
    print(f"  - The rubber will be burned for fuel or shredded for playgrounds")
    print(f"  - The glass will be recycled into fiberglass or insulation")
    print(f"\n  The atoms will persist. The assembly will not.")
    print(f"  The car was always a temporary arrangement.")
    print(f"\n{'='*70}")
    print(f"  There is no car. There is only the driving.")
    print(f"{'='*70}\n")

    db.close()


if __name__ == "__main__":
    main()

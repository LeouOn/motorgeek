"""Add the Toyota Crown sedan (2023+) to the MotorGeek DB.

The Crown is the spiritual successor to the Avalon — Toyota's flagship sedan.
Three trims:
  - Crown XLE: 2.5L hybrid, 236hp, FWD (efficiency play)
  - Crown Limited: 2.5L hybrid, 236hp, AWD (premium hybrid)
  - Crown Platinum: 2.4L turbo hybrid, 340hp, AWD (the "small car + big engine" car)

The Crown is also a "lifted sedan" — slightly higher ride height than a traditional
sedan (similar to a Subaru Outback) but lower than a crossover.

Idempotent: skips cars that already exist.
"""
import argparse
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "data" / "motorgeek.db"

CARS = [
    # Crown XLE - 2.5L hybrid, FWD, base trim
    {
        "make": "Toyota", "model": "Crown", "year": 2023, "gen": "S220 (1st gen NA)",
        "variant": "XLE 2.5L Hybrid", "body": "sedan", "country": "Japan",
        "family": "Crown", "character": "lifted-sedan-flagship",
        "length": 4980, "width": 1840, "height": 1470, "wheelbase": 2850,
        "cargo_seats_down": None, "seat_count": 5, "rear_legroom": 970, "tow_capacity": None,
        "engine_layout": "front transverse", "displacement_cc": 2487, "cylinders": 4,
        "aspiration": "naturally aspirated + hybrid", "horsepower_bhp": 236, "torque_nm": 240,
        "transmission": "CVT (eCVT)", "gear_count": None, "drivetrain": "FWD",
        "curb_weight_kg": 1740, "fuel_consumption_l_100km": 5.7,
        "dougscore": None,
        "q_score": 84,  # Toyota's flagship, modern interior
        "score_body": 86, "score_nvh": 85, "score_materials": 84,
        "score_paint": 85, "score_electrical": 82, "score_cosmetic": 84,
        "r_score": 88,  # Hybrid system proven, but new platform
        "score_engine": 90, "score_transmission": 90, "score_chassis": 88,
        "score_electronics": 85, "score_ease_repair": 88,
        "platform_type": "TNGA-L (S220)", "weld": "laser + adhesive",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 3.2,
    },
    # Crown Limited - 2.5L hybrid, AWD, premium trim
    {
        "make": "Toyota", "model": "Crown", "year": 2024, "gen": "S220 (1st gen NA)",
        "variant": "Limited 2.5L Hybrid AWD", "body": "sedan", "country": "Japan",
        "family": "Crown", "character": "lifted-sedan-flagship",
        "length": 4980, "width": 1840, "height": 1470, "wheelbase": 2850,
        "cargo_seats_down": None, "seat_count": 5, "rear_legroom": 970, "tow_capacity": None,
        "engine_layout": "front + rear transverse (AWD)", "displacement_cc": 2487, "cylinders": 4,
        "aspiration": "naturally aspirated + hybrid", "horsepower_bhp": 236, "torque_nm": 240,
        "transmission": "CVT (eCVT)", "gear_count": None, "drivetrain": "AWD (e-Four)",
        "curb_weight_kg": 1810, "fuel_consumption_l_100km": 5.9,
        "dougscore": None,
        "q_score": 87,  # Premium trim, leather, etc.
        "score_body": 88, "score_nvh": 88, "score_materials": 88,
        "score_paint": 85, "score_electrical": 82, "score_cosmetic": 86,
        "r_score": 87,  # AWD hybrid - early
        "score_engine": 90, "score_transmission": 90, "score_chassis": 88,
        "score_electronics": 85, "score_ease_repair": 88,
        "platform_type": "TNGA-L (S220)", "weld": "laser + adhesive",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 3.2,
    },
    # Crown Platinum - 2.4L turbo hybrid, 340hp, AWD
    # The "small car + bigger engine" car!
    {
        "make": "Toyota", "model": "Crown", "year": 2025, "gen": "S220 (1st gen NA)",
        "variant": "Platinum 2.4L Turbo Hybrid MAX", "body": "sedan", "country": "Japan",
        "family": "Crown", "character": "lifted-sedan-flagship",
        "length": 4980, "width": 1840, "height": 1470, "wheelbase": 2850,
        "cargo_seats_down": None, "seat_count": 5, "rear_legroom": 970, "tow_capacity": None,
        "engine_layout": "front + rear transverse (AWD)", "displacement_cc": 2393, "cylinders": 4,
        "aspiration": "turbo + hybrid", "horsepower_bhp": 340, "torque_nm": 460,
        "transmission": "6-speed automatic", "gear_count": 6, "drivetrain": "AWD (e-Four)",
        "curb_weight_kg": 1950, "fuel_consumption_l_100km": 6.5,
        "dougscore": None,
        "q_score": 88,  # Top trim, premium everything
        "score_body": 90, "score_nvh": 88, "score_materials": 90,
        "score_paint": 88, "score_electrical": 82, "score_cosmetic": 88,
        "r_score": 86,  # Turbo hybrid, new - early
        "score_engine": 88, "score_transmission": 88, "score_chassis": 88,
        "score_electronics": 85, "score_ease_repair": 85,
        "platform_type": "TNGA-L (S220)", "weld": "laser + adhesive",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 3.0,
    },
]


def main():
    parser = argparse.ArgumentParser(description="Add Toyota Crown sedan")
    parser.add_argument("--dry-run", action="store_true", help="Don't commit changes")
    args = parser.parse_args()

    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    inserted = 0
    skipped = 0
    for car in CARS:
        cur.execute(
            "SELECT id FROM cars WHERE make = ? AND model = ? AND year_start = ?",
            (car["make"], car["model"], car["year"]),
        )
        if cur.fetchone():
            print(f"  SKIP (exists): {car['year']} {car['make']} {car['model']}")
            skipped += 1
            continue

        cur.execute(
            """INSERT INTO cars (make, model, generation, variant, year_start, body_style,
                                  country, character, family, created_at, dougscore)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                car["make"], car["model"], car.get("gen"),
                car.get("variant"), car["year"], car["body"],
                car.get("country"), car.get("character"),
                car.get("family"),
                datetime.now(timezone.utc).isoformat(),
                car.get("dougscore"),
            ),
        )
        car_id = cur.lastrowid

        asp = car.get("aspiration") or ""
        is_hybrid = "hybrid" in asp.lower()
        cur.execute(
            """INSERT INTO powertrain_ice (
                car_id, source, engine_layout, displacement_cc, cylinders, aspiration,
                horsepower_bhp, torque_nm, transmission_type, gear_count, drivetrain,
                curb_weight_kg, fuel_consumption_mixed_l_100km, is_hybrid)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                car_id, "manufacturer-spec-2026-06-20",
                car.get("engine_layout"), car.get("displacement_cc"),
                car.get("cylinders"), car.get("aspiration"),
                car.get("horsepower_bhp"), car.get("torque_nm"),
                car.get("transmission"), car.get("gear_count"),
                car.get("drivetrain"), car.get("curb_weight_kg"),
                car.get("fuel_consumption_l_100km"),
                is_hybrid,
            ),
        )

        cur.execute(
            """INSERT INTO dimensions (
                car_id, length_mm, width_mm, height_mm, wheelbase_mm,
                source, extra, seat_count, cargo_volume_liters_seats_down,
                rear_legroom_mm, tow_capacity_kg)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                car_id, car.get("length"), car.get("width"),
                car.get("height"), car.get("wheelbase"),
                "manufacturer-spec-2026-06-20", "{}",
                car.get("seat_count"), car.get("cargo_seats_down"),
                car.get("rear_legroom"), car.get("tow_capacity"),
            ),
        )

        cur.execute(
            """INSERT INTO build_quality (
                car_id, q_score, score_body_construction, score_nvh_isolation,
                score_interior_materials, score_paint_corrosion,
                score_electrical_aging, score_cosmetic_aging,
                q_score_notes, platform_type, assembly_plant,
                weld_technology, panel_gap_mm, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                car_id, car.get("q_score"),
                car.get("score_body"), car.get("score_nvh"),
                car.get("score_materials"), car.get("score_paint"),
                car.get("score_electrical"), car.get("score_cosmetic"),
                f"Inferred Q-score {car.get('q_score')} from platform type {car.get('platform_type')}, plant {car.get('plant')}, {car.get('weld')} welding.",
                car.get("platform_type"), car.get("plant"),
                car.get("weld"), car.get("panel_gap"),
                "inferred-2026-06-20",
            ),
        )

        cur.execute(
            """INSERT INTO reliability (
                car_id, source, reliability_score,
                score_engine, score_transmission, score_chassis,
                score_electronics, score_ease_of_repair)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                car_id, "inferred-2026-06-20",
                car.get("r_score"),
                car.get("score_engine"), car.get("score_transmission"),
                car.get("score_chassis"), car.get("score_electronics"),
                car.get("score_ease_repair"),
            ),
        )

        inserted += 1
        print(f"  ADDED id={car_id}: {car['year']} {car['make']} {car['model']} {car['variant']}")

    print()
    print(f"Total: {inserted} inserted, {skipped} skipped, {len(CARS)} attempted")

    if args.dry_run:
        print("[DRY RUN] No writes applied.")
        conn.rollback()
    else:
        conn.commit()
        print(f"Committed to {DB_PATH}")

    conn.close()


if __name__ == "__main__":
    sys.exit(main() or 0)

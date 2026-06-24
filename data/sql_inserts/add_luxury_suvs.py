"""Add missing luxury SUVs to the MotorGeek DB.

Inserts ~40 luxury SUVs across all relevant tables:
  - cars (identity)
  - powertrain_ice (engine, weight, transmission)
  - performance (0-60, top speed)
  - dimensions (L/W/H, wheelbase, cargo, tow capacity, seats)
  - reliability (engine/trans/chassis/electronics scores)

After running this script, run:
  python scripts/recompute_zp.py        # auto-generates ZP indices
  python scripts/populate_dougscore.py  # backfills dougscore from anchors

Idempotent: uses INSERT OR IGNORE on (make, model, year_start) to skip
cars that already exist.

Usage:
    python data/sql_inserts/add_luxury_suvs.py --dry-run  # preview
    python data/sql_inserts/add_luxury_suvs.py            # apply
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "data" / "motorgeek.db"

# ---------------------------------------------------------------------------
# Car data: each entry is a dict with all fields needed for ZP, dimensions,
# performance, and reliability. Specs sourced from manufacturer data and
# well-known automotive references (Car and Driver, Edmunds, Wikipedia).
# ---------------------------------------------------------------------------

CARS = [
    # ===== AUDI (6) =====
    {
        "make": "Audi", "model": "Q3", "generation": "F3", "year_start": 2019,
        "era_tag": "10s", "body_style": "SUV", "country": "Germany",
        "character": "compact-luxury-suv", "family": "Q3", "variant": "45 TFSI Quattro",
        "engine_layout": "front transverse", "displacement_cc": 1984, "cylinders": 4,
        "aspiration": "turbo", "horsepower_bhp": 228, "torque_nm": 350,
        "transmission_type": "automatic", "gear_count": 8, "drivetrain": "AWD",
        "curb_weight_kg": 1670, "fuel_consumption_mixed_l_100km": 8.3,
        "accel_0_60": 7.0, "top_speed_mph": 130,
        "length_mm": 4484, "width_mm": 1849, "height_mm": 1616, "wheelbase_mm": 2680,
        "seat_count": 5, "cargo_volume_liters_seats_down": 1525, "tow_capacity_kg": 1800,
        "front_legroom_mm": 1000, "rear_legroom_mm": 920,
        "reliability_score": 72, "score_engine": 78, "score_transmission": 80,
        "score_chassis": 75, "score_electronics": 65, "score_ease_of_repair": 60,
    },
    {
        "make": "Audi", "model": "Q7", "generation": "4M", "year_start": 2020,
        "era_tag": "20s", "body_style": "SUV", "country": "Germany",
        "character": "full-size-luxury-suv", "family": "Q7", "variant": "3.0T Prestige Quattro",
        "engine_layout": "front longitudinal", "displacement_cc": 2995, "cylinders": 6,
        "aspiration": "turbo", "horsepower_bhp": 335, "torque_nm": 443,
        "transmission_type": "automatic", "gear_count": 8, "drivetrain": "AWD",
        "curb_weight_kg": 2299, "fuel_consumption_mixed_l_100km": 11.2,
        "accel_0_60": 5.7, "top_speed_mph": 155,
        "length_mm": 5052, "width_mm": 1968, "height_mm": 1740, "wheelbase_mm": 2994,
        "seat_count": 7, "cargo_volume_liters_seats_down": 2090, "tow_capacity_kg": 3500,
        "front_legroom_mm": 1020, "rear_legroom_mm": 970,
        "reliability_score": 74, "score_engine": 82, "score_transmission": 85,
        "score_chassis": 80, "score_electronics": 65, "score_ease_of_repair": 58,
    },
    {
        "make": "Audi", "model": "Q8", "generation": "4M", "year_start": 2019,
        "era_tag": "20s", "body_style": "SUV", "country": "Germany",
        "character": "coupe-suv", "family": "Q8", "variant": "55 TFSI Quattro",
        "engine_layout": "front longitudinal", "displacement_cc": 2995, "cylinders": 6,
        "aspiration": "turbo", "horsepower_bhp": 335, "torque_nm": 443,
        "transmission_type": "automatic", "gear_count": 8, "drivetrain": "AWD",
        "curb_weight_kg": 2285, "fuel_consumption_mixed_l_100km": 11.0,
        "accel_0_60": 5.6, "top_speed_mph": 155,
        "length_mm": 4986, "width_mm": 1995, "height_mm": 1705, "wheelbase_mm": 2998,
        "seat_count": 5, "cargo_volume_liters_seats_down": 1755, "tow_capacity_kg": 3500,
        "front_legroom_mm": 1020, "rear_legroom_mm": 940,
        "reliability_score": 73, "score_engine": 82, "score_transmission": 85,
        "score_chassis": 80, "score_electronics": 65, "score_ease_of_repair": 58,
    },
    {
        "make": "Audi", "model": "SQ5", "generation": "FY", "year_start": 2021,
        "era_tag": "20s", "body_style": "SUV", "country": "Germany",
        "character": "performance-suv", "family": "SQ5", "variant": "3.0T Quattro",
        "engine_layout": "front longitudinal", "displacement_cc": 2995, "cylinders": 6,
        "aspiration": "turbo", "horsepower_bhp": 349, "torque_nm": 500,
        "transmission_type": "automatic", "gear_count": 8, "drivetrain": "AWD",
        "curb_weight_kg": 2110, "fuel_consumption_mixed_l_100km": 11.5,
        "accel_0_60": 4.7, "top_speed_mph": 155,
        "length_mm": 4680, "width_mm": 1893, "height_mm": 1659, "wheelbase_mm": 2825,
        "seat_count": 5, "cargo_volume_liters_seats_down": 1530, "tow_capacity_kg": 2700,
        "front_legroom_mm": 1010, "rear_legroom_mm": 930,
        "reliability_score": 73, "score_engine": 80, "score_transmission": 84,
        "score_chassis": 82, "score_electronics": 65, "score_ease_of_repair": 58,
    },
    {
        "make": "Audi", "model": "SQ7", "generation": "4M", "year_start": 2020,
        "era_tag": "20s", "body_style": "SUV", "country": "Germany",
        "character": "performance-suv", "family": "SQ7", "variant": "4.0T V8 Quattro",
        "engine_layout": "front longitudinal", "displacement_cc": 3996, "cylinders": 8,
        "aspiration": "turbo", "horsepower_bhp": 500, "torque_nm": 770,
        "transmission_type": "automatic", "gear_count": 8, "drivetrain": "AWD",
        "curb_weight_kg": 2410, "fuel_consumption_mixed_l_100km": 13.0,
        "accel_0_60": 4.3, "top_speed_mph": 155,
        "length_mm": 5069, "width_mm": 1968, "height_mm": 1741, "wheelbase_mm": 2996,
        "seat_count": 7, "cargo_volume_liters_seats_down": 2090, "tow_capacity_kg": 3500,
        "front_legroom_mm": 1020, "rear_legroom_mm": 970,
        "reliability_score": 70, "score_engine": 78, "score_transmission": 84,
        "score_chassis": 82, "score_electronics": 62, "score_ease_of_repair": 55,
    },
    {
        "make": "Audi", "model": "RSQ8", "generation": "4M", "year_start": 2020,
        "era_tag": "20s", "body_style": "SUV", "country": "Germany",
        "character": "performance-suv", "family": "RSQ8", "variant": "4.0T V8 Quattro",
        "engine_layout": "front longitudinal", "displacement_cc": 3996, "cylinders": 8,
        "aspiration": "twin-turbo", "horsepower_bhp": 591, "torque_nm": 800,
        "transmission_type": "automatic", "gear_count": 8, "drivetrain": "AWD",
        "curb_weight_kg": 2440, "fuel_consumption_mixed_l_100km": 13.5,
        "accel_0_60": 3.7, "top_speed_mph": 190,
        "length_mm": 5008, "width_mm": 1995, "height_mm": 1692, "wheelbase_mm": 2998,
        "seat_count": 5, "cargo_volume_liters_seats_down": 1755, "tow_capacity_kg": 3500,
        "front_legroom_mm": 1020, "rear_legroom_mm": 940,
        "reliability_score": 68, "score_engine": 75, "score_transmission": 82,
        "score_chassis": 85, "score_electronics": 60, "score_ease_of_repair": 52,
    },

    # ===== BMW (4) =====
    {
        "make": "BMW", "model": "X7", "generation": "G07", "year_start": 2019,
        "era_tag": "20s", "body_style": "SUV", "country": "Germany",
        "character": "full-size-luxury-suv", "family": "X7", "variant": "xDrive50i",
        "engine_layout": "front longitudinal", "displacement_cc": 4395, "cylinders": 8,
        "aspiration": "turbo", "horsepower_bhp": 456, "torque_nm": 650,
        "transmission_type": "automatic", "gear_count": 8, "drivetrain": "AWD",
        "curb_weight_kg": 2520, "fuel_consumption_mixed_l_100km": 13.5,
        "accel_0_60": 5.2, "top_speed_mph": 155,
        "length_mm": 5151, "width_mm": 2000, "height_mm": 1805, "wheelbase_mm": 3105,
        "seat_count": 7, "cargo_volume_liters_seats_down": 2050, "tow_capacity_kg": 2700,
        "front_legroom_mm": 1030, "rear_legroom_mm": 1000,
        "reliability_score": 71, "score_engine": 80, "score_transmission": 85,
        "score_chassis": 78, "score_electronics": 60, "score_ease_of_repair": 55,
    },
    {
        "make": "BMW", "model": "X1", "generation": "F48", "year_start": 2020,
        "era_tag": "20s", "body_style": "SUV", "country": "Germany",
        "character": "compact-luxury-suv", "family": "X1", "variant": "xDrive28i",
        "engine_layout": "front transverse", "displacement_cc": 1998, "cylinders": 4,
        "aspiration": "turbo", "horsepower_bhp": 228, "torque_nm": 350,
        "transmission_type": "automatic", "gear_count": 8, "drivetrain": "AWD",
        "curb_weight_kg": 1620, "fuel_consumption_mixed_l_100km": 8.0,
        "accel_0_60": 6.3, "top_speed_mph": 130,
        "length_mm": 4447, "width_mm": 1821, "height_mm": 1598, "wheelbase_mm": 2670,
        "seat_count": 5, "cargo_volume_liters_seats_down": 1554, "tow_capacity_kg": 2000,
        "front_legroom_mm": 1010, "rear_legroom_mm": 950,
        "reliability_score": 75, "score_engine": 80, "score_transmission": 82,
        "score_chassis": 76, "score_electronics": 68, "score_ease_of_repair": 65,
    },
    {
        "make": "BMW", "model": "X4 M40i", "generation": "G02", "year_start": 2020,
        "era_tag": "20s", "body_style": "SUV", "country": "Germany",
        "character": "coupe-suv", "family": "X4", "variant": "M40i",
        "engine_layout": "front longitudinal", "displacement_cc": 2998, "cylinders": 6,
        "aspiration": "turbo", "horsepower_bhp": 382, "torque_nm": 500,
        "transmission_type": "automatic", "gear_count": 8, "drivetrain": "AWD",
        "curb_weight_kg": 1940, "fuel_consumption_mixed_l_100km": 10.5,
        "accel_0_60": 4.6, "top_speed_mph": 155,
        "length_mm": 4752, "width_mm": 1918, "height_mm": 1621, "wheelbase_mm": 2864,
        "seat_count": 5, "cargo_volume_liters_seats_down": 1430, "tow_capacity_kg": 2400,
        "front_legroom_mm": 1020, "rear_legroom_mm": 900,
        "reliability_score": 74, "score_engine": 82, "score_transmission": 85,
        "score_chassis": 80, "score_electronics": 65, "score_ease_of_repair": 60,
    },
    {
        "make": "BMW", "model": "X6 M50i", "generation": "G06", "year_start": 2020,
        "era_tag": "20s", "body_style": "SUV", "country": "Germany",
        "character": "coupe-suv", "family": "X6", "variant": "M50i",
        "engine_layout": "front longitudinal", "displacement_cc": 4395, "cylinders": 8,
        "aspiration": "turbo", "horsepower_bhp": 523, "torque_nm": 750,
        "transmission_type": "automatic", "gear_count": 8, "drivetrain": "AWD",
        "curb_weight_kg": 2255, "fuel_consumption_mixed_l_100km": 12.8,
        "accel_0_60": 4.1, "top_speed_mph": 155,
        "length_mm": 4935, "width_mm": 2004, "height_mm": 1696, "wheelbase_mm": 2975,
        "seat_count": 5, "cargo_volume_liters_seats_down": 1525, "tow_capacity_kg": 2700,
        "front_legroom_mm": 1025, "rear_legroom_mm": 920,
        "reliability_score": 71, "score_engine": 80, "score_transmission": 84,
        "score_chassis": 82, "score_electronics": 60, "score_ease_of_repair": 55,
    },

    # ===== MERCEDES-BENZ (6) =====
    {
        "make": "Mercedes-Benz", "model": "GLE450", "generation": "V167", "year_start": 2020,
        "era_tag": "20s", "body_style": "SUV", "country": "Germany",
        "character": "mid-luxury-suv", "family": "GLE", "variant": "4MATIC",
        "engine_layout": "front longitudinal", "displacement_cc": 2999, "cylinders": 6,
        "aspiration": "turbo", "horsepower_bhp": 362, "torque_nm": 500,
        "transmission_type": "automatic", "gear_count": 9, "drivetrain": "AWD",
        "curb_weight_kg": 2245, "fuel_consumption_mixed_l_100km": 10.8,
        "accel_0_60": 5.6, "top_speed_mph": 155,
        "length_mm": 4917, "width_mm": 2005, "height_mm": 1776, "wheelbase_mm": 2995,
        "seat_count": 7, "cargo_volume_liters_seats_down": 2055, "tow_capacity_kg": 3500,
        "front_legroom_mm": 1020, "rear_legroom_mm": 980,
        "reliability_score": 73, "score_engine": 80, "score_transmission": 85,
        "score_chassis": 80, "score_electronics": 60, "score_ease_of_repair": 55,
    },
    {
        "make": "Mercedes-Benz", "model": "GLS450", "generation": "V167", "year_start": 2020,
        "era_tag": "20s", "body_style": "SUV", "country": "Germany",
        "character": "full-size-luxury-suv", "family": "GLS", "variant": "4MATIC",
        "engine_layout": "front longitudinal", "displacement_cc": 2999, "cylinders": 6,
        "aspiration": "turbo", "horsepower_bhp": 362, "torque_nm": 500,
        "transmission_type": "automatic", "gear_count": 9, "drivetrain": "AWD",
        "curb_weight_kg": 2485, "fuel_consumption_mixed_l_100km": 11.2,
        "accel_0_60": 6.2, "top_speed_mph": 155,
        "length_mm": 5194, "width_mm": 2005, "height_mm": 1822, "wheelbase_mm": 3135,
        "seat_count": 7, "cargo_volume_liters_seats_down": 2400, "tow_capacity_kg": 3500,
        "front_legroom_mm": 1030, "rear_legroom_mm": 1010,
        "reliability_score": 73, "score_engine": 80, "score_transmission": 85,
        "score_chassis": 78, "score_electronics": 60, "score_ease_of_repair": 55,
    },
    {
        "make": "Mercedes-Benz", "model": "G550", "generation": "W463", "year_start": 2019,
        "era_tag": "20s", "body_style": "SUV", "country": "Germany",
        "character": "off-road-luxury-suv", "family": "G-Class", "variant": "G550 4MATIC",
        "engine_layout": "front longitudinal", "displacement_cc": 3982, "cylinders": 8,
        "aspiration": "turbo", "horsepower_bhp": 416, "torque_nm": 450,
        "transmission_type": "automatic", "gear_count": 9, "drivetrain": "AWD",
        "curb_weight_kg": 2465, "fuel_consumption_mixed_l_100km": 13.5,
        "accel_0_60": 5.4, "top_speed_mph": 130,
        "length_mm": 4749, "width_mm": 1945, "height_mm": 1968, "wheelbase_mm": 2850,
        "seat_count": 5, "cargo_volume_liters_seats_down": 1650, "tow_capacity_kg": 3500,
        "front_legroom_mm": 990, "rear_legroom_mm": 960,
        "reliability_score": 68, "score_engine": 78, "score_transmission": 82,
        "score_chassis": 80, "score_electronics": 58, "score_ease_of_repair": 50,
    },
    {
        "make": "Mercedes-Benz", "model": "AMG G63", "generation": "W463", "year_start": 2019,
        "era_tag": "20s", "body_style": "SUV", "country": "Germany",
        "character": "performance-off-road-suv", "family": "G-Class", "variant": "G63 AMG",
        "engine_layout": "front longitudinal", "displacement_cc": 3982, "cylinders": 8,
        "aspiration": "twin-turbo", "horsepower_bhp": 577, "torque_nm": 627,
        "transmission_type": "automatic", "gear_count": 9, "drivetrain": "AWD",
        "curb_weight_kg": 2550, "fuel_consumption_mixed_l_100km": 15.0,
        "accel_0_60": 4.4, "top_speed_mph": 149,
        "length_mm": 4749, "width_mm": 1945, "height_mm": 1968, "wheelbase_mm": 2850,
        "seat_count": 5, "cargo_volume_liters_seats_down": 1650, "tow_capacity_kg": 3500,
        "front_legroom_mm": 990, "rear_legroom_mm": 960,
        "reliability_score": 65, "score_engine": 75, "score_transmission": 80,
        "score_chassis": 82, "score_electronics": 55, "score_ease_of_repair": 48,
    },
    {
        "make": "Mercedes-Benz", "model": "AMG GLE63 Coupe", "generation": "C167", "year_start": 2018,
        "era_tag": "10s", "body_style": "SUV", "country": "Germany",
        "character": "performance-coupe-suv", "family": "GLE Coupe", "variant": "GLE63 S AMG",
        "engine_layout": "front longitudinal", "displacement_cc": 5461, "cylinders": 8,
        "aspiration": "twin-turbo", "horsepower_bhp": 577, "torque_nm": 760,
        "transmission_type": "automatic", "gear_count": 9, "drivetrain": "AWD",
        "curb_weight_kg": 2380, "fuel_consumption_mixed_l_100km": 14.0,
        "accel_0_60": 4.1, "top_speed_mph": 155,
        "length_mm": 4922, "width_mm": 2005, "height_mm": 1732, "wheelbase_mm": 2930,
        "seat_count": 5, "cargo_volume_liters_seats_down": 1720, "tow_capacity_kg": 3500,
        "front_legroom_mm": 1020, "rear_legroom_mm": 940,
        "reliability_score": 66, "score_engine": 72, "score_transmission": 80,
        "score_chassis": 82, "score_electronics": 55, "score_ease_of_repair": 48,
    },
    {
        "make": "Mercedes-Benz", "model": "Maybach GLS600", "generation": "V167", "year_start": 2021,
        "era_tag": "20s", "body_style": "SUV", "country": "Germany",
        "character": "ultra-luxury-suv", "family": "GLS", "variant": "Maybach GLS 600 4MATIC",
        "engine_layout": "front longitudinal", "displacement_cc": 3982, "cylinders": 8,
        "aspiration": "turbo", "horsepower_bhp": 550, "torque_nm": 770,
        "transmission_type": "automatic", "gear_count": 9, "drivetrain": "AWD",
        "curb_weight_kg": 2710, "fuel_consumption_mixed_l_100km": 12.8,
        "accel_0_60": 4.8, "top_speed_mph": 155,
        "length_mm": 5205, "width_mm": 2030, "height_mm": 1838, "wheelbase_mm": 3135,
        "seat_count": 4, "cargo_volume_liters_seats_down": 520, "tow_capacity_kg": 2700,
        "front_legroom_mm": 1080, "rear_legroom_mm": 1120,
        "reliability_score": 68, "score_engine": 78, "score_transmission": 84,
        "score_chassis": 75, "score_electronics": 58, "score_ease_of_repair": 45,
    },

    # ===== LEXUS (4) =====
    {
        "make": "Lexus", "model": "GX 460", "generation": "J150", "year_start": 2010,
        "era_tag": "10s", "body_style": "SUV", "country": "Japan",
        "character": "off-road-luxury-suv", "family": "GX", "variant": "Base",
        "engine_layout": "front longitudinal", "displacement_cc": 4608, "cylinders": 8,
        "aspiration": "naturally aspirated", "horsepower_bhp": 301, "torque_nm": 446,
        "transmission_type": "automatic", "gear_count": 6, "drivetrain": "4WD",
        "curb_weight_kg": 2310, "fuel_consumption_mixed_l_100km": 14.0,
        "accel_0_60": 7.4, "top_speed_mph": 110,
        "length_mm": 4840, "width_mm": 1885, "height_mm": 1880, "wheelbase_mm": 2790,
        "seat_count": 7, "cargo_volume_liters_seats_down": 1830, "tow_capacity_kg": 2950,
        "front_legroom_mm": 1050, "rear_legroom_mm": 890,
        "reliability_score": 92, "score_engine": 95, "score_transmission": 92,
        "score_chassis": 90, "score_electronics": 80, "score_ease_of_repair": 82,
    },
    {
        "make": "Lexus", "model": "LX570", "generation": "URJ200", "year_start": 2019,
        "era_tag": "10s", "body_style": "SUV", "country": "Japan",
        "character": "full-size-luxury-suv", "family": "LX", "variant": "Base",
        "engine_layout": "front longitudinal", "displacement_cc": 5663, "cylinders": 8,
        "aspiration": "naturally aspirated", "horsepower_bhp": 383, "torque_nm": 546,
        "transmission_type": "automatic", "gear_count": 8, "drivetrain": "4WD",
        "curb_weight_kg": 2750, "fuel_consumption_mixed_l_100km": 15.5,
        "accel_0_60": 6.7, "top_speed_mph": 137,
        "length_mm": 5070, "width_mm": 1980, "height_mm": 1910, "wheelbase_mm": 2850,
        "seat_count": 8, "cargo_volume_liters_seats_down": 2200, "tow_capacity_kg": 3175,
        "front_legroom_mm": 1050, "rear_legroom_mm": 940,
        "reliability_score": 94, "score_engine": 96, "score_transmission": 94,
        "score_chassis": 92, "score_electronics": 82, "score_ease_of_repair": 85,
    },
    {
        "make": "Lexus", "model": "LX 600", "generation": "V310", "year_start": 2022,
        "era_tag": "20s", "body_style": "SUV", "country": "Japan",
        "character": "full-size-luxury-suv", "family": "LX", "variant": "Ultra Luxury",
        "engine_layout": "front longitudinal", "displacement_cc": 3444, "cylinders": 6,
        "aspiration": "twin-turbo", "horsepower_bhp": 409, "torque_nm": 650,
        "transmission_type": "automatic", "gear_count": 10, "drivetrain": "4WD",
        "curb_weight_kg": 2740, "fuel_consumption_mixed_l_100km": 12.5,
        "accel_0_60": 6.5, "top_speed_mph": 137,
        "length_mm": 5085, "width_mm": 1990, "height_mm": 1885, "wheelbase_mm": 2850,
        "seat_count": 7, "cargo_volume_liters_seats_down": 1900, "tow_capacity_kg": 3628,
        "front_legroom_mm": 1060, "rear_legroom_mm": 970,
        "reliability_score": 92, "score_engine": 95, "score_transmission": 93,
        "score_chassis": 90, "score_electronics": 78, "score_ease_of_repair": 82,
    },
    {
        "make": "Lexus", "model": "NX350h", "generation": "AZ20", "year_start": 2022,
        "era_tag": "20s", "body_style": "SUV", "country": "Japan",
        "character": "compact-luxury-suv", "family": "NX", "variant": "Hybrid AWD",
        "engine_layout": "front transverse", "displacement_cc": 2487, "cylinders": 4,
        "aspiration": "naturally aspirated", "horsepower_bhp": 240, "torque_nm": 240,
        "transmission_type": "automatic", "gear_count": 1, "drivetrain": "AWD",
        "is_hybrid": True,
        "curb_weight_kg": 1880, "fuel_consumption_mixed_l_100km": 6.5,
        "accel_0_60": 6.7, "top_speed_mph": 124,
        "length_mm": 4680, "width_mm": 1865, "height_mm": 1660, "wheelbase_mm": 2690,
        "seat_count": 5, "cargo_volume_liters_seats_down": 1450, "tow_capacity_kg": 1500,
        "front_legroom_mm": 1010, "rear_legroom_mm": 930,
        "reliability_score": 90, "score_engine": 95, "score_transmission": 94,
        "score_chassis": 88, "score_electronics": 82, "score_ease_of_repair": 85,
    },

    # ===== PORSCHE (4) =====
    {
        "make": "Porsche", "model": "Cayenne Turbo", "generation": "9YA", "year_start": 2019,
        "era_tag": "20s", "body_style": "SUV", "country": "Germany",
        "character": "performance-suv", "family": "Cayenne", "variant": "Turbo",
        "engine_layout": "front longitudinal", "displacement_cc": 3996, "cylinders": 8,
        "aspiration": "twin-turbo", "horsepower_bhp": 541, "torque_nm": 770,
        "transmission_type": "automatic", "gear_count": 8, "drivetrain": "AWD",
        "curb_weight_kg": 2255, "fuel_consumption_mixed_l_100km": 12.5,
        "accel_0_60": 3.9, "top_speed_mph": 165,
        "length_mm": 4918, "width_mm": 1983, "height_mm": 1696, "wheelbase_mm": 2895,
        "seat_count": 5, "cargo_volume_liters_seats_down": 1710, "tow_capacity_kg": 3500,
        "front_legroom_mm": 1010, "rear_legroom_mm": 940,
        "reliability_score": 72, "score_engine": 78, "score_transmission": 85,
        "score_chassis": 88, "score_electronics": 65, "score_ease_of_repair": 50,
    },
    {
        "make": "Porsche", "model": "Cayenne GTS", "generation": "9YA", "year_start": 2021,
        "era_tag": "20s", "body_style": "SUV", "country": "Germany",
        "character": "performance-suv", "family": "Cayenne", "variant": "GTS 4.0 V8",
        "engine_layout": "front longitudinal", "displacement_cc": 3996, "cylinders": 8,
        "aspiration": "twin-turbo", "horsepower_bhp": 453, "torque_nm": 660,
        "transmission_type": "automatic", "gear_count": 8, "drivetrain": "AWD",
        "curb_weight_kg": 2220, "fuel_consumption_mixed_l_100km": 12.8,
        "accel_0_60": 4.5, "top_speed_mph": 168,
        "length_mm": 4930, "width_mm": 1983, "height_mm": 1676, "wheelbase_mm": 2895,
        "seat_count": 5, "cargo_volume_liters_seats_down": 1710, "tow_capacity_kg": 3500,
        "front_legroom_mm": 1010, "rear_legroom_mm": 940,
        "reliability_score": 73, "score_engine": 80, "score_transmission": 85,
        "score_chassis": 88, "score_electronics": 65, "score_ease_of_repair": 50,
    },
    {
        "make": "Porsche", "model": "Cayenne Turbo GT", "generation": "9YA", "year_start": 2022,
        "era_tag": "20s", "body_style": "SUV", "country": "Germany",
        "character": "ultra-performance-suv", "family": "Cayenne", "variant": "Turbo GT Coupe",
        "engine_layout": "front longitudinal", "displacement_cc": 3996, "cylinders": 8,
        "aspiration": "twin-turbo", "horsepower_bhp": 631, "torque_nm": 849,
        "transmission_type": "automatic", "gear_count": 8, "drivetrain": "AWD",
        "curb_weight_kg": 2340, "fuel_consumption_mixed_l_100km": 13.0,
        "accel_0_60": 3.1, "top_speed_mph": 187,
        "length_mm": 4932, "width_mm": 1994, "height_mm": 1663, "wheelbase_mm": 2895,
        "seat_count": 4, "cargo_volume_liters_seats_down": 1530, "tow_capacity_kg": 3500,
        "front_legroom_mm": 1010, "rear_legroom_mm": 940,
        "reliability_score": 70, "score_engine": 75, "score_transmission": 84,
        "score_chassis": 90, "score_electronics": 62, "score_ease_of_repair": 48,
    },
    {
        "make": "Porsche", "model": "Macan S", "generation": "95B", "year_start": 2019,
        "era_tag": "10s", "body_style": "SUV", "country": "Germany",
        "character": "performance-compact-suv", "family": "Macan", "variant": "S 3.0 V6",
        "engine_layout": "front longitudinal", "displacement_cc": 2995, "cylinders": 6,
        "aspiration": "turbo", "horsepower_bhp": 345, "torque_nm": 480,
        "transmission_type": "automatic", "gear_count": 7, "drivetrain": "AWD",
        "curb_weight_kg": 1885, "fuel_consumption_mixed_l_100km": 10.5,
        "accel_0_60": 5.1, "top_speed_mph": 158,
        "length_mm": 4696, "width_mm": 1923, "height_mm": 1613, "wheelbase_mm": 2807,
        "seat_count": 5, "cargo_volume_liters_seats_down": 1505, "tow_capacity_kg": 2400,
        "front_legroom_mm": 1000, "rear_legroom_mm": 870,
        "reliability_score": 74, "score_engine": 80, "score_transmission": 84,
        "score_chassis": 90, "score_electronics": 65, "score_ease_of_repair": 55,
    },

    # ===== LAND ROVER (3) =====
    {
        "make": "Land Rover", "model": "Defender 110", "generation": "L663", "year_start": 2020,
        "era_tag": "20s", "body_style": "SUV", "country": "UK",
        "character": "off-road-suv", "family": "Defender", "variant": "P400 X-Dynamic",
        "engine_layout": "front longitudinal", "displacement_cc": 2996, "cylinders": 6,
        "aspiration": "turbo", "horsepower_bhp": 395, "torque_nm": 550,
        "transmission_type": "automatic", "gear_count": 8, "drivetrain": "AWD",
        "curb_weight_kg": 2330, "fuel_consumption_mixed_l_100km": 11.5,
        "accel_0_60": 5.7, "top_speed_mph": 130,
        "length_mm": 5018, "width_mm": 2008, "height_mm": 1969, "wheelbase_mm": 3022,
        "seat_count": 7, "cargo_volume_liters_seats_down": 1820, "tow_capacity_kg": 3500,
        "front_legroom_mm": 1040, "rear_legroom_mm": 960,
        "reliability_score": 60, "score_engine": 70, "score_transmission": 75,
        "score_chassis": 85, "score_electronics": 50, "score_ease_of_repair": 60,
    },
    {
        "make": "Land Rover", "model": "Range Rover", "generation": "L405", "year_start": 2018,
        "era_tag": "10s", "body_style": "SUV", "country": "UK",
        "character": "ultra-luxury-suv", "family": "Range Rover", "variant": "Supercharged V8",
        "engine_layout": "front longitudinal", "displacement_cc": 5000, "cylinders": 8,
        "aspiration": "supercharged", "horsepower_bhp": 518, "torque_nm": 625,
        "transmission_type": "automatic", "gear_count": 8, "drivetrain": "AWD",
        "curb_weight_kg": 2330, "fuel_consumption_mixed_l_100km": 14.0,
        "accel_0_60": 5.1, "top_speed_mph": 155,
        "length_mm": 5000, "width_mm": 1983, "height_mm": 1869, "wheelbase_mm": 2922,
        "seat_count": 5, "cargo_volume_liters_seats_down": 1943, "tow_capacity_kg": 3500,
        "front_legroom_mm": 1030, "rear_legroom_mm": 970,
        "reliability_score": 55, "score_engine": 65, "score_transmission": 72,
        "score_chassis": 80, "score_electronics": 45, "score_ease_of_repair": 48,
    },
    {
        "make": "Land Rover", "model": "Range Rover Evoque", "generation": "L551", "year_start": 2020,
        "era_tag": "20s", "body_style": "SUV", "country": "UK",
        "character": "compact-luxury-suv", "family": "Range Rover Evoque", "variant": "P250 R-Dynamic",
        "engine_layout": "front transverse", "displacement_cc": 1997, "cylinders": 4,
        "aspiration": "turbo", "horsepower_bhp": 246, "torque_nm": 365,
        "transmission_type": "automatic", "gear_count": 9, "drivetrain": "AWD",
        "curb_weight_kg": 1820, "fuel_consumption_mixed_l_100km": 9.0,
        "accel_0_60": 7.0, "top_speed_mph": 142,
        "length_mm": 4371, "width_mm": 1900, "height_mm": 1649, "wheelbase_mm": 2681,
        "seat_count": 5, "cargo_volume_liters_seats_down": 1383, "tow_capacity_kg": 2500,
        "front_legroom_mm": 990, "rear_legroom_mm": 870,
        "reliability_score": 58, "score_engine": 68, "score_transmission": 75,
        "score_chassis": 78, "score_electronics": 50, "score_ease_of_repair": 55,
    },

    # ===== ACURA (2) =====
    {
        "make": "Acura", "model": "MDX", "generation": "YD3", "year_start": 2020,
        "era_tag": "20s", "body_style": "SUV", "country": "Japan",
        "character": "mid-luxury-suv", "family": "MDX", "variant": "SH-AWD Advance",
        "engine_layout": "front transverse", "displacement_cc": 3471, "cylinders": 6,
        "aspiration": "naturally aspirated", "horsepower_bhp": 290, "torque_nm": 362,
        "transmission_type": "automatic", "gear_count": 9, "drivetrain": "AWD",
        "curb_weight_kg": 2010, "fuel_consumption_mixed_l_100km": 11.0,
        "accel_0_60": 6.0, "top_speed_mph": 135,
        "length_mm": 4953, "width_mm": 1960, "height_mm": 1715, "wheelbase_mm": 2819,
        "seat_count": 7, "cargo_volume_liters_seats_down": 1344, "tow_capacity_kg": 2268,
        "front_legroom_mm": 1020, "rear_legroom_mm": 950,
        "reliability_score": 85, "score_engine": 90, "score_transmission": 85,
        "score_chassis": 82, "score_electronics": 72, "score_ease_of_repair": 78,
    },
    {
        "make": "Acura", "model": "RDX", "generation": "TC1", "year_start": 2020,
        "era_tag": "20s", "body_style": "SUV", "country": "Japan",
        "character": "compact-luxury-suv", "family": "RDX", "variant": "SH-AWD A-Spec",
        "engine_layout": "front transverse", "displacement_cc": 1996, "cylinders": 4,
        "aspiration": "turbo", "horsepower_bhp": 272, "torque_nm": 380,
        "transmission_type": "automatic", "gear_count": 10, "drivetrain": "AWD",
        "curb_weight_kg": 1855, "fuel_consumption_mixed_l_100km": 10.5,
        "accel_0_60": 6.4, "top_speed_mph": 130,
        "length_mm": 4752, "width_mm": 1900, "height_mm": 1615, "wheelbase_mm": 2750,
        "seat_count": 5, "cargo_volume_liters_seats_down": 1378, "tow_capacity_kg": 1500,
        "front_legroom_mm": 1020, "rear_legroom_mm": 940,
        "reliability_score": 84, "score_engine": 88, "score_transmission": 82,
        "score_chassis": 80, "score_electronics": 70, "score_ease_of_repair": 78,
    },

    # ===== CADILLAC (3) =====
    {
        "make": "Cadillac", "model": "XT4", "generation": "957", "year_start": 2019,
        "era_tag": "10s", "body_style": "SUV", "country": "USA",
        "character": "compact-luxury-suv", "family": "XT4", "variant": "Premium AWD",
        "engine_layout": "front transverse", "displacement_cc": 1998, "cylinders": 4,
        "aspiration": "turbo", "horsepower_bhp": 237, "torque_nm": 350,
        "transmission_type": "automatic", "gear_count": 9, "drivetrain": "AWD",
        "curb_weight_kg": 1750, "fuel_consumption_mixed_l_100km": 10.0,
        "accel_0_60": 6.6, "top_speed_mph": 130,
        "length_mm": 4599, "width_mm": 1881, "height_mm": 1627, "wheelbase_mm": 2750,
        "seat_count": 5, "cargo_volume_liters_seats_down": 1320, "tow_capacity_kg": 1500,
        "front_legroom_mm": 1010, "rear_legroom_mm": 930,
        "reliability_score": 72, "score_engine": 78, "score_transmission": 80,
        "score_chassis": 75, "score_electronics": 65, "score_ease_of_repair": 70,
    },
    {
        "make": "Cadillac", "model": "XT5", "generation": "540", "year_start": 2020,
        "era_tag": "20s", "body_style": "SUV", "country": "USA",
        "character": "mid-luxury-suv", "family": "XT5", "variant": "Premium Luxury AWD",
        "engine_layout": "front transverse", "displacement_cc": 2990, "cylinders": 6,
        "aspiration": "naturally aspirated", "horsepower_bhp": 310, "torque_nm": 400,
        "transmission_type": "automatic", "gear_count": 8, "drivetrain": "AWD",
        "curb_weight_kg": 1955, "fuel_consumption_mixed_l_100km": 11.5,
        "accel_0_60": 6.6, "top_speed_mph": 130,
        "length_mm": 4815, "width_mm": 1903, "height_mm": 1675, "wheelbase_mm": 2857,
        "seat_count": 5, "cargo_volume_liters_seats_down": 1784, "tow_capacity_kg": 1500,
        "front_legroom_mm": 1020, "rear_legroom_mm": 940,
        "reliability_score": 74, "score_engine": 80, "score_transmission": 82,
        "score_chassis": 78, "score_electronics": 68, "score_ease_of_repair": 72,
    },
    {
        "make": "Cadillac", "model": "XT6", "generation": "580", "year_start": 2020,
        "era_tag": "20s", "body_style": "SUV", "country": "USA",
        "character": "full-size-luxury-suv", "family": "XT6", "variant": "Sport AWD",
        "engine_layout": "front transverse", "displacement_cc": 2990, "cylinders": 6,
        "aspiration": "naturally aspirated", "horsepower_bhp": 310, "torque_nm": 400,
        "transmission_type": "automatic", "gear_count": 9, "drivetrain": "AWD",
        "curb_weight_kg": 2035, "fuel_consumption_mixed_l_100km": 11.8,
        "accel_0_60": 6.6, "top_speed_mph": 130,
        "length_mm": 5050, "width_mm": 1964, "height_mm": 1730, "wheelbase_mm": 2863,
        "seat_count": 7, "cargo_volume_liters_seats_down": 1797, "tow_capacity_kg": 1814,
        "front_legroom_mm": 1020, "rear_legroom_mm": 940,
        "reliability_score": 74, "score_engine": 80, "score_transmission": 82,
        "score_chassis": 78, "score_electronics": 68, "score_ease_of_repair": 72,
    },

    # ===== INFINITI (2) =====
    {
        "make": "Infiniti", "model": "QX60", "generation": "R50", "year_start": 2020,
        "era_tag": "20s", "body_style": "SUV", "country": "Japan",
        "character": "mid-luxury-suv", "family": "QX60", "variant": "AWD Luxe",
        "engine_layout": "front transverse", "displacement_cc": 3498, "cylinders": 6,
        "aspiration": "naturally aspirated", "horsepower_bhp": 295, "torque_nm": 362,
        "transmission_type": "CVT", "gear_count": 1, "drivetrain": "AWD",
        "curb_weight_kg": 2055, "fuel_consumption_mixed_l_100km": 11.5,
        "accel_0_60": 6.7, "top_speed_mph": 130,
        "length_mm": 5088, "width_mm": 1960, "height_mm": 1745, "wheelbase_mm": 2900,
        "seat_count": 7, "cargo_volume_liters_seats_down": 1982, "tow_capacity_kg": 2268,
        "front_legroom_mm": 1010, "rear_legroom_mm": 950,
        "reliability_score": 78, "score_engine": 85, "score_transmission": 78,
        "score_chassis": 75, "score_electronics": 68, "score_ease_of_repair": 78,
    },
    {
        "make": "Infiniti", "model": "QX80", "generation": "Z62", "year_start": 2020,
        "era_tag": "20s", "body_style": "SUV", "country": "Japan",
        "character": "full-size-luxury-suv", "family": "QX80", "variant": "AWD",
        "engine_layout": "front longitudinal", "displacement_cc": 5552, "cylinders": 8,
        "aspiration": "naturally aspirated", "horsepower_bhp": 400, "torque_nm": 560,
        "transmission_type": "automatic", "gear_count": 7, "drivetrain": "AWD",
        "curb_weight_kg": 2640, "fuel_consumption_mixed_l_100km": 15.0,
        "accel_0_60": 5.9, "top_speed_mph": 130,
        "length_mm": 5340, "width_mm": 2030, "height_mm": 1925, "wheelbase_mm": 3075,
        "seat_count": 7, "cargo_volume_liters_seats_down": 2693, "tow_capacity_kg": 3855,
        "front_legroom_mm": 1020, "rear_legroom_mm": 990,
        "reliability_score": 80, "score_engine": 88, "score_transmission": 84,
        "score_chassis": 78, "score_electronics": 70, "score_ease_of_repair": 80,
    },

    # ===== LINCOLN (2) =====
    {
        "make": "Lincoln", "model": "Corsair", "generation": "C810", "year_start": 2020,
        "era_tag": "20s", "body_style": "SUV", "country": "USA",
        "character": "compact-luxury-suv", "family": "Corsair", "variant": "Reserve AWD",
        "engine_layout": "front transverse", "displacement_cc": 2487, "cylinders": 4,
        "aspiration": "turbo", "horsepower_bhp": 280, "torque_nm": 400,
        "transmission_type": "automatic", "gear_count": 8, "drivetrain": "AWD",
        "curb_weight_kg": 1820, "fuel_consumption_mixed_l_100km": 10.5,
        "accel_0_60": 6.4, "top_speed_mph": 130,
        "length_mm": 4587, "width_mm": 1884, "height_mm": 1670, "wheelbase_mm": 2710,
        "seat_count": 5, "cargo_volume_liters_seats_down": 1464, "tow_capacity_kg": 1500,
        "front_legroom_mm": 1020, "rear_legroom_mm": 950,
        "reliability_score": 70, "score_engine": 75, "score_transmission": 78,
        "score_chassis": 72, "score_electronics": 62, "score_ease_of_repair": 70,
    },
    {
        "make": "Lincoln", "model": "Nautilus", "generation": "U720", "year_start": 2020,
        "era_tag": "20s", "body_style": "SUV", "country": "USA",
        "character": "mid-luxury-suv", "family": "Nautilus", "variant": "Reserve AWD",
        "engine_layout": "front transverse", "displacement_cc": 1995, "cylinders": 4,
        "aspiration": "turbo", "horsepower_bhp": 250, "torque_nm": 380,
        "transmission_type": "automatic", "gear_count": 8, "drivetrain": "AWD",
        "curb_weight_kg": 1955, "fuel_consumption_mixed_l_100km": 10.8,
        "accel_0_60": 6.7, "top_speed_mph": 130,
        "length_mm": 4826, "width_mm": 2155, "height_mm": 1689, "wheelbase_mm": 2853,
        "seat_count": 5, "cargo_volume_liters_seats_down": 1030, "tow_capacity_kg": 1500,
        "front_legroom_mm": 1015, "rear_legroom_mm": 930,
        "reliability_score": 68, "score_engine": 72, "score_transmission": 76,
        "score_chassis": 70, "score_electronics": 60, "score_ease_of_repair": 68,
    },

    # ===== EXOTIC / ULTRA-LUXURY (3) =====
    {
        "make": "Bentley", "model": "Bentayga", "generation": "XP12", "year_start": 2017,
        "era_tag": "10s", "body_style": "SUV", "country": "UK",
        "character": "ultra-luxury-suv", "family": "Bentayga", "variant": "W12 First Edition",
        "engine_layout": "front longitudinal", "displacement_cc": 5950, "cylinders": 12,
        "aspiration": "twin-turbo", "horsepower_bhp": 600, "torque_nm": 900,
        "transmission_type": "automatic", "gear_count": 8, "drivetrain": "AWD",
        "curb_weight_kg": 2440, "fuel_consumption_mixed_l_100km": 17.0,
        "accel_0_60": 4.0, "top_speed_mph": 187,
        "length_mm": 5141, "width_mm": 1998, "height_mm": 1742, "wheelbase_mm": 2995,
        "seat_count": 5, "cargo_volume_liters_seats_down": 1774, "tow_capacity_kg": 3500,
        "front_legroom_mm": 1030, "rear_legroom_mm": 960,
        "reliability_score": 62, "score_engine": 70, "score_transmission": 78,
        "score_chassis": 75, "score_electronics": 55, "score_ease_of_repair": 40,
    },
    {
        "make": "Rolls-Royce", "model": "Cullinan", "generation": "RR11", "year_start": 2019,
        "era_tag": "20s", "body_style": "SUV", "country": "UK",
        "character": "ultra-luxury-suv", "family": "Cullinan", "variant": "6.75L V12",
        "engine_layout": "front longitudinal", "displacement_cc": 6748, "cylinders": 12,
        "aspiration": "twin-turbo", "horsepower_bhp": 563, "torque_nm": 850,
        "transmission_type": "automatic", "gear_count": 8, "drivetrain": "AWD",
        "curb_weight_kg": 2660, "fuel_consumption_mixed_l_100km": 17.5,
        "accel_0_60": 4.5, "top_speed_mph": 155,
        "length_mm": 5341, "width_mm": 2000, "height_mm": 1835, "wheelbase_mm": 3295,
        "seat_count": 5, "cargo_volume_liters_seats_down": 560, "tow_capacity_kg": 2700,
        "front_legroom_mm": 1060, "rear_legroom_mm": 1020,
        "reliability_score": 65, "score_engine": 75, "score_transmission": 80,
        "score_chassis": 78, "score_electronics": 58, "score_ease_of_repair": 40,
    },
    {
        "make": "Lamborghini", "model": "Urus", "generation": "XS68", "year_start": 2019,
        "era_tag": "20s", "body_style": "SUV", "country": "Italy",
        "character": "ultra-performance-suv", "family": "Urus", "variant": "4.0T V8",
        "engine_layout": "front longitudinal", "displacement_cc": 3996, "cylinders": 8,
        "aspiration": "twin-turbo", "horsepower_bhp": 641, "torque_nm": 850,
        "transmission_type": "automatic", "gear_count": 8, "drivetrain": "AWD",
        "curb_weight_kg": 2200, "fuel_consumption_mixed_l_100km": 13.0,
        "accel_0_60": 3.2, "top_speed_mph": 190,
        "length_mm": 5112, "width_mm": 2016, "height_mm": 1638, "wheelbase_mm": 3003,
        "seat_count": 5, "cargo_volume_liters_seats_down": 1596, "tow_capacity_kg": 2700,
        "front_legroom_mm": 990, "rear_legroom_mm": 900,
        "reliability_score": 60, "score_engine": 70, "score_transmission": 78,
        "score_chassis": 88, "score_electronics": 55, "score_ease_of_repair": 40,
    },
]


def insert_car(cur: sqlite3.Cursor, car: dict) -> int | None:
    """Insert a car and return its new car_id, or None if already exists."""
    # Check existence first (idempotent)
    cur.execute(
        "SELECT id FROM cars WHERE make = ? AND model = ? AND year_start = ?",
        (car["make"], car["model"], car["year_start"]),
    )
    existing = cur.fetchone()
    if existing:
        return None
    cur.execute(
        """INSERT INTO cars (make, model, generation, year_start, era_tag,
                              body_style, country, character, family, variant,
                              created_at, dougscore)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)""",
        (
            car["make"], car["model"], car["generation"], car["year_start"],
            car.get("era_tag"), car.get("body_style"), car.get("country"),
            car.get("character"), car.get("family"), car.get("variant"),
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    return cur.lastrowid


def insert_powertrain(cur: sqlite3.Cursor, car_id: int, car: dict) -> None:
    """Insert engine/transmission data."""
    cur.execute(
        """INSERT INTO powertrain_ice (
            car_id, source, engine_layout, displacement_cc, cylinders, aspiration,
            horsepower_bhp, torque_nm, transmission_type, gear_count, drivetrain,
            curb_weight_kg, is_hybrid, fuel_consumption_mixed_l_100km, extra)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            car_id, "manufacturer-spec-2026-06-18",
            car.get("engine_layout"), car.get("displacement_cc"), car.get("cylinders"),
            car.get("aspiration"), car.get("horsepower_bhp"), car.get("torque_nm"),
            car.get("transmission_type"), car.get("gear_count"), car.get("drivetrain"),
            car.get("curb_weight_kg"), car.get("is_hybrid", False),
            car.get("fuel_consumption_mixed_l_100km"), "{}",
        ),
    )


def insert_performance(cur: sqlite3.Cursor, car_id: int, car: dict) -> None:
    """Insert 0-60 and top speed."""
    cur.execute(
        """INSERT INTO performance (car_id, source, accel_0_60, top_speed_mph, extra)
           VALUES (?, ?, ?, ?, ?)""",
        (car_id, "manufacturer-spec-2026-06-18", car.get("accel_0_60"),
         car.get("top_speed_mph"), "{}"),
    )


def insert_dimensions(cur: sqlite3.Cursor, car_id: int, car: dict) -> None:
    """Insert dimensions + practicality data."""
    extra = json.dumps({"practicality_enriched": True})
    cur.execute(
        """INSERT INTO dimensions (
            car_id, length_mm, width_mm, height_mm, wheelbase_mm,
            source, extra, seat_count, cargo_volume_liters_seats_down,
            front_legroom_mm, rear_legroom_mm, tow_capacity_kg)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            car_id, car.get("length_mm"), car.get("width_mm"),
            car.get("height_mm"), car.get("wheelbase_mm"),
            "manufacturer-spec-2026-06-18", extra,
            car.get("seat_count"), car.get("cargo_volume_liters_seats_down"),
            car.get("front_legroom_mm"), car.get("rear_legroom_mm"),
            car.get("tow_capacity_kg"),
        ),
    )


def insert_reliability(cur: sqlite3.Cursor, car_id: int, car: dict) -> None:
    """Insert reliability sub-scores."""
    cur.execute(
        """INSERT INTO reliability (
            car_id, source, reliability_score,
            score_engine, score_transmission, score_chassis,
            score_electronics, score_ease_of_repair)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            car_id, "estimated-2026-06-18", car.get("reliability_score"),
            car.get("score_engine"), car.get("score_transmission"),
            car.get("score_chassis"), car.get("score_electronics"),
            car.get("score_ease_of_repair"),
        ),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Add missing luxury SUVs")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no writes")
    args = parser.parse_args()

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    inserted = 0
    skipped = 0
    for car in CARS:
        car_id = insert_car(cur, car)
        if car_id is None:
            print(f"  SKIP (exists): {car['year_start']} {car['make']} {car['model']}")
            skipped += 1
            continue
        insert_powertrain(cur, car_id, car)
        insert_performance(cur, car_id, car)
        insert_dimensions(cur, car_id, car)
        insert_reliability(cur, car_id, car)
        inserted += 1
        print(f"  ADDED id={car_id}: {car['year_start']} {car['make']} {car['model']} ({car['variant']})")

    print()
    print(f"Total: {inserted} inserted, {skipped} skipped, {len(CARS)} attempted")

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

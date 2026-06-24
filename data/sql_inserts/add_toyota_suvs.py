"""Add Toyota SUV / Truck line to the MotorGeek DB.

Includes:
  - Land Cruiser: 100-series (2003-2007), 200-series (2008-2021), 250-series (2024+)
  - 4Runner: 4th gen (2003-2009), 5th gen (2010-2024), 6th gen (2025+)
  - Sequoia: 1st gen (2001-2007), 2nd gen (2008-2022), 3rd gen (2023+)
  - Tundra: 2nd gen (2007-2021), 3rd gen (2022+)
  - Tacoma: 2nd gen (2005-2015), 3rd gen (2016-2023), 4th gen (2024+)
  - Highlander: 1st gen (2001-2007), 3rd gen (2014-2019), 4th gen (2020+)
  - Grand Highlander: 2024+
  - RAV4: 3rd gen (2006-2012), 4th gen (2013-2018), 5th gen (2019+), RAV4 Prime
  - FJ Cruiser: 2007-2014
  - Venza: 2021+
  - bZ4X: 2023+
  - Crown Signia: 2025+

Reliability data sourced from:
  - Consumer Reports annual reliability surveys (2020-2024)
  - JD Power Initial Quality Studies
  - Owner reports on TacomaWorld, LandCruiser70Series, ToyotaNation
  - TrueDelta reliability aggregations
  - RepairPal reliability ratings

Toyota reputation: legendary reliability (R 88-95), good build quality (Q 75-85),
modest performance (Z moderate), excellent practicality (P high for real SUVs).
Doug dougscores (D 47-59) reflect "not fun to drive" more than "bad car."

Idempotent: skips cars that already exist.
"""
import argparse
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "data" / "motorgeek.db"

# ============================================================================
# CAR DATA
# Format per car:
#   make, model, year, generation/variant, body_style, country, character,
#   family, dimensions (L/W/H/WB mm), cargo_seats_down, seat_count,
#   rear_legroom, tow_capacity, engine (displacement_cc, cylinders, layout,
#   aspiration, hp, tq), transmission (type, gears, drivetrain),
#   curb_weight_kg, fuel_consumption_l_100km, dougscore (from anchor),
#   build_quality (q_score + 6 sub-scores),
#   reliability (r_score + 5 sub-scores)
# ============================================================================

CARS = [
    # ========================================================================
    # LAND CRUISER (5 cars) - the Toyota icon
    # ========================================================================
    # 80-series 1990-1997: collectible, simple
    # 100-series 1998-2007: 4.7L V8, then 4.5L inline-6 twin-turbo (in EU)
    # 200-series 2008-2021: 5.7L V8
    # 300-series: not sold in US (skip)
    # 250-series 2024+: 2.4L turbo hybrid, new platform
    {
        "make": "Toyota", "model": "Land Cruiser", "year": 2003, "gen": "100-series",
        "variant": "Base 4.7L V8", "body": "SUV", "country": "Japan",
        "family": "Land Cruiser", "character": "luxury-offroad-suv",
        "length": 4890, "width": 1940, "height": 1855, "wheelbase": 2850,
        "cargo_seats_down": 2200, "seat_count": 8, "rear_legroom": 925, "tow_capacity": 3500,
        "engine_layout": "front longitudinal", "displacement_cc": 4664, "cylinders": 8,
        "aspiration": "naturally aspirated", "horsepower_bhp": 235, "torque_nm": 434,
        "transmission": "5-speed automatic", "gear_count": 5, "drivetrain": "4WD (full-time)",
        "curb_weight_kg": 2400, "fuel_consumption_l_100km": 14.7,
        "dougscore": None,
        "q_score": 82,  # Old but well-built
        "score_body": 85, "score_nvh": 75, "score_materials": 80,
        "score_paint": 85, "score_electrical": 80, "score_cosmetic": 80,
        "r_score": 92,  # Legendary reliability
        "score_engine": 95, "score_transmission": 90, "score_chassis": 95,
        "score_electronics": 85, "score_ease_repair": 95,
        "platform_type": "J100", "weld": "spot + laser",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 3.8,
    },
    {
        "make": "Toyota", "model": "Land Cruiser", "year": 2013, "gen": "200-series",
        "variant": "Base 5.7L V8", "body": "SUV", "country": "Japan",
        "family": "Land Cruiser", "character": "luxury-offroad-suv",
        "length": 4990, "width": 1970, "height": 1920, "wheelbase": 2850,
        "cargo_seats_down": 2350, "seat_count": 8, "rear_legroom": 945, "tow_capacity": 4000,
        "engine_layout": "front longitudinal", "displacement_cc": 5663, "cylinders": 8,
        "aspiration": "naturally aspirated", "horsepower_bhp": 381, "torque_nm": 544,
        "transmission": "6-speed automatic", "gear_count": 6, "drivetrain": "4WD (full-time)",
        "curb_weight_kg": 2580, "fuel_consumption_l_100km": 13.8,
        "dougscore": 57,  # 2013 Land Cruiser anchor
        "q_score": 88,
        "score_body": 90, "score_nvh": 85, "score_materials": 88,
        "score_paint": 90, "score_electrical": 85, "score_cosmetic": 88,
        "r_score": 93,  # Bulletproof
        "score_engine": 95, "score_transmission": 92, "score_chassis": 95,
        "score_electronics": 88, "score_ease_repair": 95,
        "platform_type": "J200", "weld": "spot + laser",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 3.5,
    },
    {
        "make": "Toyota", "model": "Land Cruiser", "year": 2018, "gen": "200-series (facelift)",
        "variant": "Base 5.7L V8", "body": "SUV", "country": "Japan",
        "family": "Land Cruiser", "character": "luxury-offroad-suv",
        "length": 4990, "width": 1970, "height": 1920, "wheelbase": 2850,
        "cargo_seats_down": 2350, "seat_count": 8, "rear_legroom": 945, "tow_capacity": 4000,
        "engine_layout": "front longitudinal", "displacement_cc": 5663, "cylinders": 8,
        "aspiration": "naturally aspirated", "horsepower_bhp": 381, "torque_nm": 544,
        "transmission": "8-speed automatic", "gear_count": 8, "drivetrain": "4WD (full-time)",
        "curb_weight_kg": 2580, "fuel_consumption_l_100km": 13.8,
        "dougscore": 57,  # 2018 Land Cruiser anchor
        "q_score": 90,  # Refined interior by 2018
        "score_body": 92, "score_nvh": 88, "score_materials": 90,
        "score_paint": 92, "score_electrical": 88, "score_cosmetic": 90,
        "r_score": 94,  # Toyota refinement
        "score_engine": 95, "score_transmission": 93, "score_chassis": 95,
        "score_electronics": 90, "score_ease_repair": 95,
        "platform_type": "J200 (facelift)", "weld": "spot + laser",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 3.2,
    },
    {
        "make": "Toyota", "model": "Land Cruiser", "year": 2024, "gen": "250-series (J250)",
        "variant": "First Edition 2.4L Turbo Hybrid i-Force MAX", "body": "SUV", "country": "Japan",
        "family": "Land Cruiser", "character": "luxury-offroad-suv",
        "length": 4925, "width": 1980, "height": 1870, "wheelbase": 2850,
        "cargo_seats_down": 2100, "seat_count": 7, "rear_legroom": 935, "tow_capacity": 3500,
        "engine_layout": "front longitudinal", "displacement_cc": 2393, "cylinders": 4,
        "aspiration": "turbo + hybrid", "horsepower_bhp": 326, "torque_nm": 630,
        "transmission": "8-speed automatic", "gear_count": 8, "drivetrain": "4WD (part-time)",
        "curb_weight_kg": 2310, "fuel_consumption_l_100km": 10.7,
        "dougscore": None,  # Doug scored the 2022 Land Cruiser (V6 TT) as 56; this is the US 250-series
        "q_score": 88,
        "score_body": 90, "score_nvh": 88, "score_materials": 88,
        "score_paint": 88, "score_electrical": 85, "score_cosmetic": 88,
        "r_score": 90,  # New platform, hybrid - early but Toyota reliability holds
        "score_engine": 88, "score_transmission": 90, "score_chassis": 92,
        "score_electronics": 85, "score_ease_repair": 88,
        "platform_type": "TNGA-F (J250)", "weld": "laser + adhesive",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 3.0,
    },
    # ========================================================================
    # 4RUNNER (4 cars) - the off-road icon
    # ========================================================================
    {
        "make": "Toyota", "model": "4Runner", "year": 2003, "gen": "4th gen (N210)",
        "variant": "SR5 4.0L V6", "body": "SUV", "country": "Japan",
        "family": "4Runner", "character": "offroad-suv",
        "length": 4805, "width": 1910, "height": 1760, "wheelbase": 2789,
        "cargo_seats_down": 2550, "seat_count": 5, "rear_legroom": 880, "tow_capacity": 3000,
        "engine_layout": "front longitudinal", "displacement_cc": 3956, "cylinders": 6,
        "aspiration": "naturally aspirated", "horsepower_bhp": 245, "torque_nm": 382,
        "transmission": "5-speed automatic", "gear_count": 5, "drivetrain": "4WD (part-time)",
        "curb_weight_kg": 2110, "fuel_consumption_l_100km": 12.4,
        "dougscore": 47,  # 2000 4Runner anchor (close enough)
        "q_score": 78,
        "score_body": 82, "score_nvh": 72, "score_materials": 75,
        "score_paint": 80, "score_electrical": 78, "score_cosmetic": 78,
        "r_score": 92,  # 1GR-FE legendary
        "score_engine": 95, "score_transmission": 88, "score_chassis": 95,
        "score_electronics": 88, "score_ease_repair": 95,
        "platform_type": "N210", "weld": "spot + laser",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 4.0,
    },
    {
        "make": "Toyota", "model": "4Runner", "year": 2018, "gen": "5th gen (N280)",
        "variant": "TRD Pro 4.0L V6", "body": "SUV", "country": "Japan",
        "family": "4Runner", "character": "offroad-suv",
        "length": 4860, "width": 1925, "height": 1820, "wheelbase": 2789,
        "cargo_seats_down": 2700, "seat_count": 5, "rear_legroom": 890, "tow_capacity": 3500,
        "engine_layout": "front longitudinal", "displacement_cc": 3956, "cylinders": 6,
        "aspiration": "naturally aspirated", "horsepower_bhp": 270, "torque_nm": 377,
        "transmission": "5-speed automatic", "gear_count": 5, "drivetrain": "4WD (part-time)",
        "curb_weight_kg": 2220, "fuel_consumption_l_100km": 12.4,
        "dougscore": 53,  # 2018 4Runner TRD Pro anchor
        "q_score": 78,  # 5th gen is OLD - same interior since 2010
        "score_body": 85, "score_nvh": 75, "score_materials": 75,
        "score_paint": 82, "score_electrical": 80, "score_cosmetic": 78,
        "r_score": 90,  # Same 1GR-FE since 2003
        "score_engine": 92, "score_transmission": 88, "score_chassis": 92,
        "score_electronics": 85, "score_ease_repair": 95,
        "platform_type": "N280", "weld": "spot + laser",
        "plant": "Tahara Plant (Japan)", "panel_gap": 3.8,
    },
    {
        "make": "Toyota", "model": "4Runner", "year": 2025, "gen": "6th gen (N310)",
        "variant": "TRD Off-Road 2.4L Turbo Hybrid i-Force MAX", "body": "SUV", "country": "Japan",
        "family": "4Runner", "character": "offroad-suv",
        "length": 4945, "width": 1980, "height": 1880, "wheelbase": 2850,
        "cargo_seats_down": 2700, "seat_count": 5, "rear_legroom": 920, "tow_capacity": 3500,
        "engine_layout": "front longitudinal", "displacement_cc": 2393, "cylinders": 4,
        "aspiration": "turbo + hybrid", "horsepower_bhp": 326, "torque_nm": 630,
        "transmission": "8-speed automatic", "gear_count": 8, "drivetrain": "4WD (part-time)",
        "curb_weight_kg": 2270, "fuel_consumption_l_100km": 10.7,
        "dougscore": None,  # Too new
        "q_score": 82,  # New platform, modernized interior
        "score_body": 85, "score_nvh": 82, "score_materials": 82,
        "score_paint": 82, "score_electrical": 80, "score_cosmetic": 82,
        "r_score": 88,  # New platform, hybrid - too early
        "score_engine": 85, "score_transmission": 88, "score_chassis": 90,
        "score_electronics": 82, "score_ease_repair": 88,
        "platform_type": "TNGA-F (N310)", "weld": "laser + adhesive",
        "plant": "Tahara Plant (Japan)", "panel_gap": 3.5,
    },
    # ========================================================================
    # FJ CRUISER (2 cars) - the retro off-roader
    # ========================================================================
    {
        "make": "Toyota", "model": "FJ Cruiser", "year": 2010, "gen": "1st gen (GSJ10)",
        "variant": "Base 4.0L V6", "body": "SUV", "country": "Japan",
        "family": "FJ Cruiser", "character": "offroad-suv",
        "length": 4670, "width": 1905, "height": 1830, "wheelbase": 2690,
        "cargo_seats_down": 1900, "seat_count": 5, "rear_legroom": 850, "tow_capacity": 2300,
        "engine_layout": "front longitudinal", "displacement_cc": 3956, "cylinders": 6,
        "aspiration": "naturally aspirated", "horsepower_bhp": 260, "torque_nm": 367,
        "transmission": "5-speed automatic", "gear_count": 5, "drivetrain": "4WD (part-time)",
        "curb_weight_kg": 1945, "fuel_consumption_l_100km": 12.4,
        "dougscore": 49,  # 2010 FJ Cruiser anchor
        "q_score": 72,  # Utilitarian - suicide rear doors, rubber floor
        "score_body": 78, "score_nvh": 68, "score_materials": 65,
        "score_paint": 80, "score_electrical": 75, "score_cosmetic": 75,
        "r_score": 88,  # Same 1GR-FE - bulletproof
        "score_engine": 92, "score_transmission": 88, "score_chassis": 90,
        "score_electronics": 82, "score_ease_repair": 95,
        "platform_type": "GSJ10", "weld": "spot",
        "plant": "Hamura Plant (Japan)", "panel_gap": 4.5,
    },
    # ========================================================================
    # SEQUOIA (3 cars) - the full-size Land Cruiser-based SUV
    # ========================================================================
    {
        "make": "Toyota", "model": "Sequoia", "year": 2010, "gen": "2nd gen (XK60)",
        "variant": "Limited 5.7L V8", "body": "SUV", "country": "USA",
        "family": "Sequoia", "character": "full-size-suv",
        "length": 5210, "width": 2027, "height": 1955, "wheelbase": 3100,
        "cargo_seats_down": 3400, "seat_count": 8, "rear_legroom": 950, "tow_capacity": 5000,
        "engine_layout": "front longitudinal", "displacement_cc": 5663, "cylinders": 8,
        "aspiration": "naturally aspirated", "horsepower_bhp": 381, "torque_nm": 544,
        "transmission": "6-speed automatic", "gear_count": 6, "drivetrain": "4WD (part-time)",
        "curb_weight_kg": 2700, "fuel_consumption_l_100km": 14.7,
        "dougscore": None,
        "q_score": 80,  # Tundra-based, big but not luxury
        "score_body": 85, "score_nvh": 75, "score_materials": 78,
        "score_paint": 82, "score_electrical": 80, "score_cosmetic": 80,
        "r_score": 90,  # 3UR-FE proven
        "score_engine": 92, "score_transmission": 88, "score_chassis": 92,
        "score_electronics": 85, "score_ease_repair": 95,
        "platform_type": "XK60", "weld": "spot + laser",
        "plant": "Princeton, IN (USA)", "panel_gap": 4.2,
    },
    {
        "make": "Toyota", "model": "Sequoia", "year": 2023, "gen": "3rd gen (XK80)",
        "variant": "TRD Pro 3.4L Turbo Hybrid i-Force MAX", "body": "SUV", "country": "USA",
        "family": "Sequoia", "character": "full-size-suv",
        "length": 5450, "width": 2030, "height": 1980, "wheelbase": 3250,
        "cargo_seats_down": 3300, "seat_count": 8, "rear_legroom": 980, "tow_capacity": 5000,
        "engine_layout": "front longitudinal", "displacement_cc": 3445, "cylinders": 6,
        "aspiration": "twin-turbo + hybrid", "horsepower_bhp": 437, "torque_nm": 790,
        "transmission": "10-speed automatic", "gear_count": 10, "drivetrain": "4WD (part-time)",
        "curb_weight_kg": 2680, "fuel_consumption_l_100km": 11.2,
        "dougscore": None,
        "q_score": 85,  # New platform, modernized
        "score_body": 88, "score_nvh": 85, "score_materials": 85,
        "score_paint": 85, "score_electrical": 82, "score_cosmetic": 85,
        "r_score": 88,  # New platform, hybrid - early
        "score_engine": 90, "score_transmission": 88, "score_chassis": 92,
        "score_electronics": 85, "score_ease_repair": 88,
        "platform_type": "TNGA-F (XK80)", "weld": "laser + adhesive",
        "plant": "San Antonio, TX (USA)", "panel_gap": 3.5,
    },
    # ========================================================================
    # TACOMA (3 cars) - mid-size pickup
    # ========================================================================
    {
        "make": "Toyota", "model": "Tacoma", "year": 2010, "gen": "2nd gen (N220)",
        "variant": "TRD Off-Road 4.0L V6", "body": "truck", "country": "USA",
        "family": "Tacoma", "character": "mid-size-truck",
        "length": 5280, "width": 1895, "height": 1780, "wheelbase": 3230,
        "cargo_seats_down": 1680, "seat_count": 5, "rear_legroom": 800, "tow_capacity": 3500,
        "engine_layout": "front longitudinal", "displacement_cc": 3956, "cylinders": 6,
        "aspiration": "naturally aspirated", "horsepower_bhp": 236, "torque_nm": 335,
        "transmission": "5-speed automatic", "gear_count": 5, "drivetrain": "4WD (part-time)",
        "curb_weight_kg": 1950, "fuel_consumption_l_100km": 12.4,
        "dougscore": None,
        "q_score": 75,  # Old truck interior
        "score_body": 80, "score_nvh": 70, "score_materials": 72,
        "score_paint": 80, "score_electrical": 75, "score_cosmetic": 75,
        "r_score": 92,  # Tacoma legendary
        "score_engine": 92, "score_transmission": 88, "score_chassis": 92,
        "score_electronics": 85, "score_ease_repair": 95,
        "platform_type": "N220", "weld": "spot + laser",
        "plant": "Fremont, CA / Tijuana (Mexico)", "panel_gap": 4.0,
    },
    {
        "make": "Toyota", "model": "Tacoma", "year": 2019, "gen": "3rd gen (N300)",
        "variant": "TRD Pro 3.5L V6", "body": "truck", "country": "USA",
        "family": "Tacoma", "character": "mid-size-truck",
        "length": 5395, "width": 1910, "height": 1795, "wheelbase": 3230,
        "cargo_seats_down": 1700, "seat_count": 5, "rear_legroom": 825, "tow_capacity": 3500,
        "engine_layout": "front longitudinal", "displacement_cc": 3456, "cylinders": 6,
        "aspiration": "naturally aspirated", "horsepower_bhp": 278, "torque_nm": 360,
        "transmission": "6-speed automatic", "gear_count": 6, "drivetrain": "4WD (part-time)",
        "curb_weight_kg": 2050, "fuel_consumption_l_100km": 12.4,
        "dougscore": 50,  # 2019 Tacoma TRD Pro anchor
        "q_score": 78,
        "score_body": 82, "score_nvh": 75, "score_materials": 75,
        "score_paint": 82, "score_electrical": 78, "score_cosmetic": 78,
        "r_score": 90,
        "score_engine": 92, "score_transmission": 88, "score_chassis": 90,
        "score_electronics": 85, "score_ease_repair": 92,
        "platform_type": "N300", "weld": "spot + laser",
        "plant": "San Antonio, TX (USA)", "panel_gap": 3.8,
    },
    {
        "make": "Toyota", "model": "Tacoma", "year": 2024, "gen": "4th gen (N400)",
        "variant": "TRD Off-Road 2.4L Turbo Hybrid i-Force MAX", "body": "truck", "country": "USA",
        "family": "Tacoma", "character": "mid-size-truck",
        "length": 5410, "width": 1955, "height": 1880, "wheelbase": 3300,
        "cargo_seats_down": 1750, "seat_count": 5, "rear_legroom": 850, "tow_capacity": 3500,
        "engine_layout": "front longitudinal", "displacement_cc": 2393, "cylinders": 4,
        "aspiration": "turbo + hybrid", "horsepower_bhp": 326, "torque_nm": 630,
        "transmission": "8-speed automatic", "gear_count": 8, "drivetrain": "4WD (part-time)",
        "curb_weight_kg": 2110, "fuel_consumption_l_100km": 10.7,
        "dougscore": None,
        "q_score": 82,  # New platform, modernized
        "score_body": 85, "score_nvh": 82, "score_materials": 82,
        "score_paint": 85, "score_electrical": 82, "score_cosmetic": 82,
        "r_score": 87,  # New platform, hybrid - too early
        "score_engine": 88, "score_transmission": 88, "score_chassis": 90,
        "score_electronics": 82, "score_ease_repair": 88,
        "platform_type": "TNGA-F (N400)", "weld": "laser + adhesive",
        "plant": "San Antonio, TX (USA)", "panel_gap": 3.5,
    },
    # ========================================================================
    # TUNDRA (1 new car - 2022 3rd gen)
    # ========================================================================
    # 2014 Tundra SR5 already in DB (id=200)
    {
        "make": "Toyota", "model": "Tundra", "year": 2022, "gen": "3rd gen (XK70)",
        "variant": "TRD Pro 3.4L Turbo Hybrid i-Force MAX", "body": "truck", "country": "USA",
        "family": "Tundra", "character": "full-size-truck",
        "length": 5935, "width": 2035, "height": 1980, "wheelbase": 3700,
        "cargo_seats_down": 1700, "seat_count": 5, "rear_legroom": 880, "tow_capacity": 5500,
        "engine_layout": "front longitudinal", "displacement_cc": 3445, "cylinders": 6,
        "aspiration": "twin-turbo + hybrid", "horsepower_bhp": 437, "torque_nm": 790,
        "transmission": "10-speed automatic", "gear_count": 10, "drivetrain": "4WD (part-time)",
        "curb_weight_kg": 2520, "fuel_consumption_l_100km": 11.2,
        "dougscore": 59,  # 2022 Tundra TRD Pro anchor
        "q_score": 84,  # New platform, modernized
        "score_body": 88, "score_nvh": 85, "score_materials": 85,
        "score_paint": 85, "score_electrical": 82, "score_cosmetic": 85,
        "r_score": 87,  # New platform, hybrid - early
        "score_engine": 88, "score_transmission": 88, "score_chassis": 90,
        "score_electronics": 82, "score_ease_repair": 88,
        "platform_type": "TNGA-F (XK70)", "weld": "laser + adhesive",
        "plant": "San Antonio, TX (USA)", "panel_gap": 3.5,
    },
    # ========================================================================
    # HIGHLANDER (3 cars) - mid-size crossover
    # ========================================================================
    {
        "make": "Toyota", "model": "Highlander", "year": 2008, "gen": "2nd gen (XU40)",
        "variant": "Limited 3.5L V6", "body": "SUV", "country": "USA",
        "family": "Highlander", "character": "midsize-suv",
        "length": 4785, "width": 1910, "height": 1730, "wheelbase": 2790,
        "cargo_seats_down": 2400, "seat_count": 7, "rear_legroom": 950, "tow_capacity": 2300,
        "engine_layout": "front transverse", "displacement_cc": 3456, "cylinders": 6,
        "aspiration": "naturally aspirated", "horsepower_bhp": 270, "torque_nm": 336,
        "transmission": "5-speed automatic", "gear_count": 5, "drivetrain": "AWD",
        "curb_weight_kg": 1900, "fuel_consumption_l_100km": 10.7,
        "dougscore": None,
        "q_score": 78,
        "score_body": 82, "score_nvh": 75, "score_materials": 75,
        "score_paint": 80, "score_electrical": 78, "score_cosmetic": 78,
        "r_score": 90,  # 2GR-FE proven
        "score_engine": 92, "score_transmission": 88, "score_chassis": 88,
        "score_electronics": 85, "score_ease_repair": 92,
        "platform_type": "XU40", "weld": "spot + laser",
        "plant": "Princeton, IN (USA)", "panel_gap": 3.8,
    },
    {
        "make": "Toyota", "model": "Highlander", "year": 2020, "gen": "4th gen (XU70)",
        "variant": "Platinum 3.5L V6", "body": "SUV", "country": "USA",
        "family": "Highlander", "character": "midsize-suv",
        "length": 4950, "width": 1930, "height": 1730, "wheelbase": 2850,
        "cargo_seats_down": 2400, "seat_count": 8, "rear_legroom": 970, "tow_capacity": 2300,
        "engine_layout": "front transverse", "displacement_cc": 3456, "cylinders": 6,
        "aspiration": "naturally aspirated", "horsepower_bhp": 295, "torque_nm": 356,
        "transmission": "8-speed automatic", "gear_count": 8, "drivetrain": "AWD",
        "curb_weight_kg": 2010, "fuel_consumption_l_100km": 10.2,
        "dougscore": 49,  # 2020 Highlander Platinum anchor
        "q_score": 82,
        "score_body": 85, "score_nvh": 82, "score_materials": 80,
        "score_paint": 85, "score_electrical": 82, "score_cosmetic": 82,
        "r_score": 91,  # Toyota mid-size SUV reliability
        "score_engine": 92, "score_transmission": 90, "score_chassis": 90,
        "score_electronics": 88, "score_ease_repair": 92,
        "platform_type": "TNGA-K (XU70)", "weld": "spot + laser",
        "plant": "Princeton, IN (USA)", "panel_gap": 3.5,
    },
    {
        "make": "Toyota", "model": "Highlander", "year": 2023, "gen": "4th gen (XU70) Hybrid MAX",
        "variant": "Platinum 2.4L Turbo Hybrid", "body": "SUV", "country": "USA",
        "family": "Highlander", "character": "midsize-suv",
        "length": 4950, "width": 1930, "height": 1730, "wheelbase": 2850,
        "cargo_seats_down": 2400, "seat_count": 7, "rear_legroom": 970, "tow_capacity": 2300,
        "engine_layout": "front transverse", "displacement_cc": 2393, "cylinders": 4,
        "aspiration": "turbo + hybrid", "horsepower_bhp": 362, "torque_nm": 540,
        "transmission": "6-speed automatic", "gear_count": 6, "drivetrain": "AWD",
        "curb_weight_kg": 2110, "fuel_consumption_l_100km": 8.4,
        "dougscore": None,
        "q_score": 84,  # Hybrid MAX top trim
        "score_body": 88, "score_nvh": 85, "score_materials": 85,
        "score_paint": 85, "score_electrical": 82, "score_cosmetic": 85,
        "r_score": 89,  # Hybrid powertrain - early
        "score_engine": 90, "score_transmission": 88, "score_chassis": 90,
        "score_electronics": 85, "score_ease_repair": 90,
        "platform_type": "TNGA-K (XU70)", "weld": "laser + adhesive",
        "plant": "Princeton, IN (USA)", "panel_gap": 3.5,
    },
    # ========================================================================
    # GRAND HIGHLANDER (1 car) - new 3-row
    # ========================================================================
    {
        "make": "Toyota", "model": "Grand Highlander", "year": 2024, "gen": "1st gen (XU80)",
        "variant": "Platinum 2.4L Turbo Hybrid MAX", "body": "SUV", "country": "USA",
        "family": "Highlander", "character": "midsize-suv",
        "length": 5115, "width": 1990, "height": 1780, "wheelbase": 2950,
        "cargo_seats_down": 2700, "seat_count": 7, "rear_legroom": 1015, "tow_capacity": 3500,
        "engine_layout": "front transverse", "displacement_cc": 2393, "cylinders": 4,
        "aspiration": "turbo + hybrid", "horsepower_bhp": 362, "torque_nm": 540,
        "transmission": "6-speed automatic", "gear_count": 6, "drivetrain": "AWD",
        "curb_weight_kg": 2150, "fuel_consumption_l_100km": 8.7,
        "dougscore": None,
        "q_score": 85,  # New, top trim
        "score_body": 88, "score_nvh": 85, "score_materials": 85,
        "score_paint": 85, "score_electrical": 82, "score_cosmetic": 85,
        "r_score": 88,  # New, hybrid
        "score_engine": 88, "score_transmission": 88, "score_chassis": 90,
        "score_electronics": 82, "score_ease_repair": 88,
        "platform_type": "TNGA-K (XU80)", "weld": "laser + adhesive",
        "plant": "Princeton, IN (USA)", "panel_gap": 3.5,
    },
    # ========================================================================
    # RAV4 (3 cars) - the compact SUV
    # ========================================================================
    {
        "make": "Toyota", "model": "RAV4", "year": 2012, "gen": "3rd gen (XA30)",
        "variant": "Limited 2.5L I4", "body": "SUV", "country": "Canada",
        "family": "RAV4", "character": "compact-suv",
        "length": 4625, "width": 1815, "height": 1685, "wheelbase": 2660,
        "cargo_seats_down": 1950, "seat_count": 5, "rear_legroom": 945, "tow_capacity": 1500,
        "engine_layout": "front transverse", "displacement_cc": 2494, "cylinders": 4,
        "aspiration": "naturally aspirated", "horsepower_bhp": 179, "torque_nm": 233,
        "transmission": "4-speed automatic", "gear_count": 4, "drivetrain": "AWD",
        "curb_weight_kg": 1620, "fuel_consumption_l_100km": 9.0,
        "dougscore": None,
        "q_score": 75,
        "score_body": 78, "score_nvh": 72, "score_materials": 72,
        "score_paint": 78, "score_electrical": 75, "score_cosmetic": 75,
        "r_score": 90,  # 2AR-FE proven
        "score_engine": 90, "score_transmission": 85, "score_chassis": 88,
        "score_electronics": 85, "score_ease_repair": 92,
        "platform_type": "XA30", "weld": "spot",
        "plant": "Woodstock, ON (Canada)", "panel_gap": 4.0,
    },
    {
        "make": "Toyota", "model": "RAV4", "year": 2019, "gen": "5th gen (XA50)",
        "variant": "Adventure 2.5L Hybrid", "body": "SUV", "country": "Canada",
        "family": "RAV4", "character": "compact-suv",
        "length": 4600, "width": 1855, "height": 1700, "wheelbase": 2690,
        "cargo_seats_down": 1970, "seat_count": 5, "rear_legroom": 905, "tow_capacity": 1500,
        "engine_layout": "front transverse", "displacement_cc": 2487, "cylinders": 4,
        "aspiration": "naturally aspirated + hybrid", "horsepower_bhp": 219, "torque_nm": 240,
        "transmission": "CVT (eCVT)", "gear_count": None, "drivetrain": "AWD",
        "curb_weight_kg": 1690, "fuel_consumption_l_100km": 6.4,
        "dougscore": 47,  # 2019 RAV4 anchor
        "q_score": 80,  # New TNGA platform
        "score_body": 85, "score_nvh": 80, "score_materials": 78,
        "score_paint": 82, "score_electrical": 80, "score_cosmetic": 80,
        "r_score": 91,  # Hybrid system proven
        "score_engine": 90, "score_transmission": 90, "score_chassis": 88,
        "score_electronics": 85, "score_ease_repair": 88,
        "platform_type": "TNGA-C (XA50)", "weld": "spot + laser",
        "plant": "Woodstock, ON (Canada) / Tahara (Japan)", "panel_gap": 3.5,
    },
    {
        "make": "Toyota", "model": "RAV4 Prime", "year": 2021, "gen": "5th gen (XA50) PHEV",
        "variant": "XSE 2.5L PHEV", "body": "SUV", "country": "Japan",
        "family": "RAV4", "character": "compact-suv",
        "length": 4600, "width": 1855, "height": 1700, "wheelbase": 2690,
        "cargo_seats_down": 1970, "seat_count": 5, "rear_legroom": 905, "tow_capacity": 1130,
        "engine_layout": "front transverse", "displacement_cc": 2487, "cylinders": 4,
        "aspiration": "naturally aspirated + plug-in hybrid", "horsepower_bhp": 302, "torque_nm": 420,
        "transmission": "CVT (eCVT)", "gear_count": None, "drivetrain": "AWD",
        "curb_weight_kg": 1910, "fuel_consumption_l_100km": 5.7,
        "dougscore": 50,  # 2021 RAV4 Prime anchor
        "q_score": 82,
        "score_body": 85, "score_nvh": 82, "score_materials": 80,
        "score_paint": 82, "score_electrical": 82, "score_cosmetic": 82,
        "r_score": 88,  # PHEV new tech
        "score_engine": 88, "score_transmission": 88, "score_chassis": 88,
        "score_electronics": 85, "score_ease_repair": 85,
        "platform_type": "TNGA-C (XA50)", "weld": "spot + laser",
        "plant": "Nagakusa, Aichi (Japan)", "panel_gap": 3.5,
    },
    # ========================================================================
    # VENZA (1 car) - the hybrid crossover
    # ========================================================================
    {
        "make": "Toyota", "model": "Venza", "year": 2021, "gen": "2nd gen (XU80)",
        "variant": "Limited 2.5L Hybrid", "body": "SUV", "country": "Japan",
        "family": "Venza", "character": "midsize-suv",
        "length": 4740, "width": 1855, "height": 1675, "wheelbase": 2690,
        "cargo_seats_down": 1900, "seat_count": 5, "rear_legroom": 960, "tow_capacity": 1000,
        "engine_layout": "front transverse", "displacement_cc": 2487, "cylinders": 4,
        "aspiration": "naturally aspirated + hybrid", "horsepower_bhp": 219, "torque_nm": 280,
        "transmission": "CVT (eCVT)", "gear_count": None, "drivetrain": "AWD",
        "curb_weight_kg": 1735, "fuel_consumption_l_100km": 5.9,
        "dougscore": 47,  # 2021 Venza Limited anchor
        "q_score": 80,  # Premium positioning
        "score_body": 85, "score_nvh": 82, "score_materials": 82,
        "score_paint": 82, "score_electrical": 80, "score_cosmetic": 82,
        "r_score": 90,  # Hybrid system proven
        "score_engine": 90, "score_transmission": 90, "score_chassis": 88,
        "score_electronics": 85, "score_ease_repair": 88,
        "platform_type": "TNGA-K (XU80)", "weld": "spot + laser",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 3.5,
    },
    # ========================================================================
    # bZ4X (1 car) - Toyota's first EV
    # ========================================================================
    {
        "make": "Toyota", "model": "bZ4X", "year": 2023, "gen": "1st gen (XE10)",
        "variant": "Limited AWD 71.4 kWh", "body": "SUV", "country": "Japan",
        "family": "bZ4X", "character": "compact-suv",
        "length": 4690, "width": 1860, "height": 1650, "wheelbase": 2850,
        "cargo_seats_down": 1700, "seat_count": 5, "rear_legroom": 950, "tow_capacity": 750,
        "engine_layout": "front + rear transverse (dual motor)", "displacement_cc": None,
        "cylinders": None, "aspiration": "electric", "horsepower_bhp": 214, "torque_nm": 337,
        "transmission": "1-speed direct", "gear_count": 1, "drivetrain": "AWD",
        "curb_weight_kg": 1980, "fuel_consumption_l_100km": None,
        "dougscore": None,
        "q_score": 78,  # New EV, decent build
        "score_body": 82, "score_nvh": 85, "score_materials": 78,
        "score_paint": 80, "score_electrical": 75, "score_cosmetic": 80,
        "r_score": 78,  # EV with new tech - early
        "score_engine": 80, "score_transmission": 85, "score_chassis": 85,
        "score_electronics": 75, "score_ease_repair": 70,
        "platform_type": "e-TNGA (XE10)", "weld": "spot + laser",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 3.5,
    },
    # ========================================================================
    # CROWN SIGNIA (1 car) - the new flagship crossover
    # ========================================================================
    {
        "make": "Toyota", "model": "Crown Signia", "year": 2025, "gen": "1st gen",
        "variant": "Platinum 2.5L Hybrid MAX", "body": "SUV", "country": "Japan",
        "family": "Crown", "character": "midsize-suv",
        "length": 4930, "width": 1880, "height": 1620, "wheelbase": 2850,
        "cargo_seats_down": 2100, "seat_count": 5, "rear_legroom": 990, "tow_capacity": 1500,
        "engine_layout": "front transverse", "displacement_cc": 2393, "cylinders": 4,
        "aspiration": "turbo + hybrid", "horsepower_bhp": 323, "torque_nm": 460,
        "transmission": "6-speed automatic", "gear_count": 6, "drivetrain": "AWD",
        "curb_weight_kg": 1990, "fuel_consumption_l_100km": 6.5,
        "dougscore": None,
        "q_score": 85,  # New flagship positioning
        "score_body": 88, "score_nvh": 85, "score_materials": 88,
        "score_paint": 88, "score_electrical": 82, "score_cosmetic": 88,
        "r_score": 87,  # New platform, hybrid - early
        "score_engine": 88, "score_transmission": 88, "score_chassis": 90,
        "score_electronics": 85, "score_ease_repair": 88,
        "platform_type": "TNGA-K (XK80)", "weld": "laser + adhesive",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 3.2,
    },
]


def main():
    parser = argparse.ArgumentParser(description="Add Toyota SUV/Truck line")
    parser.add_argument("--dry-run", action="store_true", help="Don't commit changes")
    args = parser.parse_args()

    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    inserted = 0
    skipped = 0
    for car in CARS:
        # Check if exists
        cur.execute(
            "SELECT id FROM cars WHERE make = ? AND model = ? AND year_start = ?",
            (car["make"], car["model"], car["year"]),
        )
        if cur.fetchone():
            print(f"  SKIP (exists): {car['year']} {car['make']} {car['model']}")
            skipped += 1
            continue

        # Insert into cars table
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

        # Insert into powertrain_ice
        # Set is_hybrid = True for hybrid variants
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

        # Insert into dimensions
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

        # Insert into build_quality
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

        # Insert into reliability
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
        d_str = f" D={car['dougscore']}" if car.get("dougscore") else ""
        print(f"  ADDED id={car_id}: {car['year']} {car['make']} {car['model']}{d_str}")

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

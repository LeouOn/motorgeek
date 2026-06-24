"""Add missing TNGA cars to the MotorGeek DB.

Adds the most important TNGA-platform Toyotas and Lexuses that are missing
from the DB. Focuses on US-market cars that matter for the rankings.

Categories added:
  - TNGA-C: Corolla, Prius, C-HR, Corolla Cross, GR86
  - TNGA-K: Camry XV80, RAV4 XA60, Crown Crossover
  - TNGA-L: Lexus LS 500 (5th gen), Mirai
  - TNGA-F: Lexus GX 550 (2024+)
  - e-TNGA: Lexus RZ, Toyota bZ3
  - Lexus models: NX 2nd gen, RX 5th gen, TX, LC 500, IS 4th gen, LBX, RC F

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
    # ========================================================================
    # TNGA-C (compact)
    # ========================================================================
    # Toyota Corolla 2020+ (E210) - the world's best-selling car
    {
        "make": "Toyota", "model": "Corolla", "year": 2020, "gen": "E210 (12th gen)",
        "variant": "LE 2.0L I4", "body": "sedan", "country": "USA",
        "family": "Corolla", "character": "compact-sedan",
        "length": 4630, "width": 1780, "height": 1435, "wheelbase": 2700,
        "cargo_seats_down": None, "seat_count": 5, "rear_legroom": 950, "tow_capacity": None,
        "engine_layout": "front transverse", "displacement_cc": 1987, "cylinders": 4,
        "aspiration": "naturally aspirated", "horsepower_bhp": 169, "torque_nm": 205,
        "transmission": "CVT (Direct Shift)", "gear_count": None, "drivetrain": "FWD",
        "curb_weight_kg": 1320, "fuel_consumption_l_100km": 6.7,
        "dougscore": None,
        "q_score": 75,
        "score_body": 78, "score_nvh": 72, "score_materials": 72,
        "score_paint": 78, "score_electrical": 75, "score_cosmetic": 75,
        "r_score": 92,  # Corolla = legend
        "score_engine": 92, "score_transmission": 90, "score_chassis": 88,
        "score_electronics": 85, "score_ease_repair": 92,
        "platform_type": "TNGA-C (E210)", "weld": "spot + laser",
        "plant": "Blue Springs, MS (USA) / Burnaston (UK)", "panel_gap": 3.5,
    },
    # Toyota Corolla Hybrid
    {
        "make": "Toyota", "model": "Corolla Hybrid", "year": 2020, "gen": "E210",
        "variant": "LE Hybrid 1.8L I4", "body": "sedan", "country": "USA",
        "family": "Corolla", "character": "compact-sedan",
        "length": 4630, "width": 1780, "height": 1435, "wheelbase": 2700,
        "cargo_seats_down": None, "seat_count": 5, "rear_legroom": 950, "tow_capacity": None,
        "engine_layout": "front transverse", "displacement_cc": 1798, "cylinders": 4,
        "aspiration": "naturally aspirated + hybrid", "horsepower_bhp": 121, "torque_nm": 142,
        "transmission": "CVT (eCVT)", "gear_count": None, "drivetrain": "FWD",
        "curb_weight_kg": 1380, "fuel_consumption_l_100km": 4.7,
        "dougscore": None,
        "q_score": 76,
        "score_body": 78, "score_nvh": 72, "score_materials": 73,
        "score_paint": 78, "score_electrical": 75, "score_cosmetic": 75,
        "r_score": 92,
        "score_engine": 92, "score_transmission": 90, "score_chassis": 88,
        "score_electronics": 85, "score_ease_repair": 90,
        "platform_type": "TNGA-C (E210)", "weld": "spot + laser",
        "plant": "Blue Springs, MS (USA)", "panel_gap": 3.5,
    },
    # Toyota Prius 5th gen (XW60) 2023+
    {
        "make": "Toyota", "model": "Prius", "year": 2024, "gen": "XW60 (5th gen)",
        "variant": "LE 2.0L Hybrid", "body": "hatchback", "country": "Japan",
        "family": "Prius", "character": "hybrid-hatchback",
        "length": 4599, "width": 1782, "height": 1430, "wheelbase": 2750,
        "cargo_seats_down": None, "seat_count": 5, "rear_legroom": 925, "tow_capacity": None,
        "engine_layout": "front transverse", "displacement_cc": 1987, "cylinders": 4,
        "aspiration": "naturally aspirated + hybrid", "horsepower_bhp": 196, "torque_nm": 188,
        "transmission": "CVT (eCVT)", "gear_count": None, "drivetrain": "FWD",
        "curb_weight_kg": 1370, "fuel_consumption_l_100km": 4.7,
        "dougscore": None,
        "q_score": 80,  # New 5th gen, much improved interior
        "score_body": 82, "score_nvh": 80, "score_materials": 80,
        "score_paint": 82, "score_electrical": 80, "score_cosmetic": 80,
        "r_score": 90,  # Hybrid system proven
        "score_engine": 92, "score_transmission": 90, "score_chassis": 88,
        "score_electronics": 85, "score_ease_repair": 90,
        "platform_type": "TNGA-C (XW60)", "weld": "laser + adhesive",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 3.2,
    },
    # Toyota Prius Prime (PHEV) - 5th gen
    {
        "make": "Toyota", "model": "Prius Prime", "year": 2024, "gen": "XW60 PHEV",
        "variant": "SE 2.0L PHEV", "body": "hatchback", "country": "Japan",
        "family": "Prius", "character": "hybrid-hatchback",
        "length": 4599, "width": 1782, "height": 1430, "wheelbase": 2750,
        "cargo_seats_down": None, "seat_count": 5, "rear_legroom": 925, "tow_capacity": None,
        "engine_layout": "front transverse", "displacement_cc": 1987, "cylinders": 4,
        "aspiration": "naturally aspirated + plug-in hybrid", "horsepower_bhp": 220, "torque_nm": 350,
        "transmission": "CVT (eCVT)", "gear_count": None, "drivetrain": "FWD",
        "curb_weight_kg": 1560, "fuel_consumption_l_100km": 4.4,
        "dougscore": None,
        "q_score": 82,
        "score_body": 84, "score_nvh": 82, "score_materials": 82,
        "score_paint": 82, "score_electrical": 80, "score_cosmetic": 82,
        "r_score": 88,  # PHEV new tech
        "score_engine": 90, "score_transmission": 88, "score_chassis": 88,
        "score_electronics": 85, "score_ease_repair": 88,
        "platform_type": "TNGA-C (XW60)", "weld": "laser + adhesive",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 3.2,
    },
    # Toyota C-HR 2018+ (AX20 2nd gen) - small crossover
    {
        "make": "Toyota", "model": "C-HR", "year": 2023, "gen": "AX20 (2nd gen)",
        "variant": "LE 2.0L I4", "body": "SUV", "country": "Japan",
        "family": "C-HR", "character": "compact-crossover",
        "length": 4385, "width": 1795, "height": 1555, "wheelbase": 2640,
        "cargo_seats_down": None, "seat_count": 5, "rear_legroom": 880, "tow_capacity": None,
        "engine_layout": "front transverse", "displacement_cc": 1987, "cylinders": 4,
        "aspiration": "naturally aspirated", "horsepower_bhp": 144, "torque_nm": 188,
        "transmission": "CVT (Direct Shift)", "gear_count": None, "drivetrain": "FWD",
        "curb_weight_kg": 1420, "fuel_consumption_l_100km": 7.4,
        "dougscore": None,
        "q_score": 76,
        "score_body": 78, "score_nvh": 75, "score_materials": 75,
        "score_paint": 78, "score_electrical": 75, "score_cosmetic": 76,
        "r_score": 90,  # Toyota reliability
        "score_engine": 90, "score_transmission": 88, "score_chassis": 85,
        "score_electronics": 82, "score_ease_repair": 90,
        "platform_type": "TNGA-C (AX20)", "weld": "spot + laser",
        "plant": "Sakarya (Turkey) / Toyota Motor Kyushu (Japan)", "panel_gap": 3.5,
    },
    # Toyota Corolla Cross 2022+
    {
        "make": "Toyota", "model": "Corolla Cross", "year": 2022, "gen": "XG10 (1st gen)",
        "variant": "LE 2.0L I4", "body": "SUV", "country": "Japan",
        "family": "Corolla", "character": "compact-crossover",
        "length": 4460, "width": 1825, "height": 1620, "wheelbase": 2640,
        "cargo_seats_down": None, "seat_count": 5, "rear_legroom": 880, "tow_capacity": 1500,
        "engine_layout": "front transverse", "displacement_cc": 1987, "cylinders": 4,
        "aspiration": "naturally aspirated", "horsepower_bhp": 169, "torque_nm": 205,
        "transmission": "CVT (Direct Shift)", "gear_count": None, "drivetrain": "AWD",
        "curb_weight_kg": 1500, "fuel_consumption_l_100km": 7.4,
        "dougscore": None,
        "q_score": 74,
        "score_body": 76, "score_nvh": 72, "score_materials": 72,
        "score_paint": 76, "score_electrical": 75, "score_cosmetic": 74,
        "r_score": 90,
        "score_engine": 90, "score_transmission": 88, "score_chassis": 85,
        "score_electronics": 82, "score_ease_repair": 90,
        "platform_type": "TNGA-C (XG10)", "weld": "spot + laser",
        "plant": "Sakarya (Turkey) / Toyota Motor Kyushu (Japan)", "panel_gap": 3.5,
    },
    # Toyota GR86 2022+ (ZN8) - sports car (not TNGA, but should be in DB)
    {
        "make": "Toyota", "model": "GR86", "year": 2022, "gen": "ZN8 (2nd gen)",
        "variant": "Base 2.4L Flat-4", "body": "coupe", "country": "Japan",
        "family": "86", "character": "sports-coupe",
        "length": 4265, "width": 1775, "height": 1310, "wheelbase": 2575,
        "cargo_seats_down": None, "seat_count": 4, "rear_legroom": 745, "tow_capacity": None,
        "engine_layout": "front longitudinal", "displacement_cc": 2387, "cylinders": 4,
        "aspiration": "naturally aspirated", "horsepower_bhp": 228, "torque_nm": 250,
        "transmission": "6-speed manual", "gear_count": 6, "drivetrain": "RWD",
        "curb_weight_kg": 1270, "fuel_consumption_l_100km": 8.4,
        "dougscore": None,
        "q_score": 72,
        "score_body": 75, "score_nvh": 68, "score_materials": 70,
        "score_paint": 75, "score_electrical": 75, "score_cosmetic": 72,
        "r_score": 85,  # New engine, no major issues yet
        "score_engine": 85, "score_transmission": 88, "score_chassis": 90,
        "score_electronics": 80, "score_ease_repair": 85,
        "platform_type": "Subaru Global Platform (with Toyota tuning)", "weld": "spot + laser",
        "plant": "Subaru Gunma (Japan)", "panel_gap": 3.5,
    },
    # ========================================================================
    # TNGA-K (mid-size)
    # ========================================================================
    # Toyota Camry XV80 2024+ (9th gen)
    {
        "make": "Toyota", "model": "Camry", "year": 2025, "gen": "XV80 (9th gen)",
        "variant": "XLE 2.5L Hybrid AWD", "body": "sedan", "country": "USA",
        "family": "Camry", "character": "midsize-sedan",
        "length": 4915, "width": 1840, "height": 1450, "wheelbase": 2825,
        "cargo_seats_down": None, "seat_count": 5, "rear_legroom": 970, "tow_capacity": None,
        "engine_layout": "front transverse", "displacement_cc": 2487, "cylinders": 4,
        "aspiration": "naturally aspirated + hybrid", "horsepower_bhp": 232, "torque_nm": 230,
        "transmission": "CVT (eCVT)", "gear_count": None, "drivetrain": "AWD (e-Four)",
        "curb_weight_kg": 1640, "fuel_consumption_l_100km": 5.4,
        "dougscore": None,
        "q_score": 80,  # New XV80, hybrid-only
        "score_body": 82, "score_nvh": 82, "score_materials": 80,
        "score_paint": 82, "score_electrical": 78, "score_cosmetic": 80,
        "r_score": 90,  # Hybrid system proven
        "score_engine": 92, "score_transmission": 90, "score_chassis": 88,
        "score_electronics": 85, "score_ease_repair": 88,
        "platform_type": "TNGA-K (XV80)", "weld": "laser + adhesive",
        "plant": "Georgetown, KY (USA)", "panel_gap": 3.2,
    },
    # Toyota Crown Crossover (S235) - the Crossover variant of the Crown
    {
        "make": "Toyota", "model": "Crown Crossover", "year": 2023, "gen": "S235 (1st gen)",
        "variant": "XLE 2.5L Hybrid", "body": "SUV", "country": "Japan",
        "family": "Crown", "character": "lifted-sedan-flagship",
        "length": 4750, "width": 1835, "height": 1540, "wheelbase": 2770,
        "cargo_seats_down": None, "seat_count": 5, "rear_legroom": 970, "tow_capacity": None,
        "engine_layout": "front + rear transverse (AWD)", "displacement_cc": 2487, "cylinders": 4,
        "aspiration": "naturally aspirated + hybrid", "horsepower_bhp": 236, "torque_nm": 240,
        "transmission": "CVT (eCVT)", "gear_count": None, "drivetrain": "AWD (e-Four)",
        "curb_weight_kg": 1760, "fuel_consumption_l_100km": 6.1,
        "dougscore": None,
        "q_score": 83,
        "score_body": 85, "score_nvh": 85, "score_materials": 85,
        "score_paint": 85, "score_electrical": 80, "score_cosmetic": 84,
        "r_score": 88,
        "score_engine": 90, "score_transmission": 90, "score_chassis": 86,
        "score_electronics": 85, "score_ease_repair": 88,
        "platform_type": "TNGA-K (S235)", "weld": "laser + adhesive",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 3.2,
    },
    # ========================================================================
    # TNGA-L (executive)
    # ========================================================================
    # Lexus LS 500 (5th gen) 2018+
    {
        "make": "Lexus", "model": "LS 500", "year": 2018, "gen": "XF50 (5th gen)",
        "variant": "Base 3.5L V6 Twin-Turbo", "body": "sedan", "country": "Japan",
        "family": "LS", "character": "executive-sedan",
        "length": 5235, "width": 1900, "height": 1460, "wheelbase": 3125,
        "cargo_seats_down": None, "seat_count": 5, "rear_legroom": 950, "tow_capacity": None,
        "engine_layout": "front longitudinal", "displacement_cc": 3444, "cylinders": 6,
        "aspiration": "twin-turbo", "horsepower_bhp": 416, "torque_nm": 600,
        "transmission": "10-speed automatic", "gear_count": 10, "drivetrain": "RWD",
        "curb_weight_kg": 2030, "fuel_consumption_l_100km": 10.4,
        "dougscore": None,
        "q_score": 90,  # Top-of-line Lexus
        "score_body": 92, "score_nvh": 92, "score_materials": 92,
        "score_paint": 92, "score_electrical": 88, "score_cosmetic": 90,
        "r_score": 85,  # New platform, but Toyota reliability holds
        "score_engine": 88, "score_transmission": 88, "score_chassis": 92,
        "score_electronics": 85, "score_ease_repair": 85,
        "platform_type": "TNGA-L (XF50)", "weld": "laser + adhesive",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 2.8,
    },
    # Lexus LS 500h (5th gen hybrid)
    {
        "make": "Lexus", "model": "LS 500h", "year": 2018, "gen": "XF50 (5th gen) hybrid",
        "variant": "Base 3.5L V6 Multi Stage Hybrid", "body": "sedan", "country": "Japan",
        "family": "LS", "character": "executive-sedan",
        "length": 5235, "width": 1900, "height": 1460, "wheelbase": 3125,
        "cargo_seats_down": None, "seat_count": 5, "rear_legroom": 950, "tow_capacity": None,
        "engine_layout": "front longitudinal", "displacement_cc": 3456, "cylinders": 6,
        "aspiration": "naturally aspirated + hybrid", "horsepower_bhp": 354, "torque_nm": 350,
        "transmission": "CVT (eCVT) + 4-speed auto (Multi Stage)", "gear_count": 10, "drivetrain": "RWD",
        "curb_weight_kg": 2120, "fuel_consumption_l_100km": 8.4,
        "dougscore": None,
        "q_score": 92,  # Hybrid is the better LS
        "score_body": 94, "score_nvh": 94, "score_materials": 94,
        "score_paint": 92, "score_electrical": 88, "score_cosmetic": 92,
        "r_score": 87,  # Hybrid system reliable
        "score_engine": 90, "score_transmission": 88, "score_chassis": 92,
        "score_electronics": 88, "score_ease_repair": 85,
        "platform_type": "TNGA-L (XF50)", "weld": "laser + adhesive",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 2.8,
    },
    # Toyota Mirai 2021+ (2nd gen)
    {
        "make": "Toyota", "model": "Mirai", "year": 2021, "gen": "JPD20 (2nd gen)",
        "variant": "XLE Hydrogen FCEV", "body": "sedan", "country": "Japan",
        "family": "Mirai", "character": "hydrogen-sedan",
        "length": 4973, "width": 1880, "height": 1470, "wheelbase": 2920,
        "cargo_seats_down": None, "seat_count": 5, "rear_legroom": 960, "tow_capacity": None,
        "engine_layout": "rear transverse (electric)", "displacement_cc": None,
        "cylinders": None, "aspiration": "hydrogen fuel cell", "horsepower_bhp": 182, "torque_nm": 300,
        "transmission": "1-speed direct", "gear_count": 1, "drivetrain": "RWD",
        "curb_weight_kg": 1900, "fuel_consumption_l_100km": None,
        "dougscore": None,
        "q_score": 85,  # Hydrogen flagship
        "score_body": 88, "score_nvh": 90, "score_materials": 88,
        "score_paint": 88, "score_electrical": 85, "score_cosmetic": 86,
        "r_score": 80,  # FCEV new tech, hydrogen infrastructure limited
        "score_engine": 85, "score_transmission": 88, "score_chassis": 88,
        "score_electronics": 85, "score_ease_repair": 75,
        "platform_type": "TNGA-L (JPD20)", "weld": "laser + adhesive",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 3.0,
    },
    # ========================================================================
    # TNGA-F (body-on-frame)
    # ========================================================================
    # Lexus GX 550 Overtrail (2024+)
    {
        "make": "Lexus", "model": "GX 550", "year": 2024, "gen": "J250 (2nd gen)",
        "variant": "Overtrail 3.4L V6 Twin-Turbo", "body": "SUV", "country": "Japan",
        "family": "GX", "character": "luxury-offroad-suv",
        "length": 4965, "width": 1990, "height": 1935, "wheelbase": 2850,
        "cargo_seats_down": 2200, "seat_count": 7, "rear_legroom": 945, "tow_capacity": 3500,
        "engine_layout": "front longitudinal", "displacement_cc": 3444, "cylinders": 6,
        "aspiration": "twin-turbo", "horsepower_bhp": 349, "torque_nm": 650,
        "transmission": "10-speed automatic", "gear_count": 10, "drivetrain": "4WD (full-time)",
        "curb_weight_kg": 2360, "fuel_consumption_l_100km": 11.7,
        "dougscore": None,
        "q_score": 86,  # New J250 platform, premium trim
        "score_body": 88, "score_nvh": 88, "score_materials": 88,
        "score_paint": 86, "score_electrical": 82, "score_cosmetic": 86,
        "r_score": 87,  # New platform, too early
        "score_engine": 88, "score_transmission": 88, "score_chassis": 92,
        "score_electronics": 85, "score_ease_repair": 88,
        "platform_type": "TNGA-F (J250)", "weld": "laser + adhesive",
        "plant": "Tahara Plant (Japan)", "panel_gap": 3.2,
    },
    # ========================================================================
    # e-TNGA (EVs)
    # ========================================================================
    # Lexus RZ 450e (electric)
    {
        "make": "Lexus", "model": "RZ 450e", "year": 2023, "gen": "EB10 (1st gen)",
        "variant": "Luxury AWD 71.4 kWh", "body": "SUV", "country": "Japan",
        "family": "RZ", "character": "compact-suv",
        "length": 4810, "width": 1895, "height": 1635, "wheelbase": 2850,
        "cargo_seats_down": 1700, "seat_count": 5, "rear_legroom": 950, "tow_capacity": 750,
        "engine_layout": "front + rear transverse (dual motor)", "displacement_cc": None,
        "cylinders": None, "aspiration": "electric", "horsepower_bhp": 308, "torque_nm": 435,
        "transmission": "1-speed direct", "gear_count": 1, "drivetrain": "AWD",
        "curb_weight_kg": 2070, "fuel_consumption_l_100km": None,
        "dougscore": None,
        "q_score": 84,  # Premium EV
        "score_body": 86, "score_nvh": 88, "score_materials": 85,
        "score_paint": 85, "score_electrical": 80, "score_cosmetic": 85,
        "r_score": 80,  # EV with new tech
        "score_engine": 82, "score_transmission": 88, "score_chassis": 88,
        "score_electronics": 80, "score_ease_repair": 75,
        "platform_type": "e-TNGA (EB10)", "weld": "spot + laser",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 3.2,
    },
    # Toyota bZ3 (electric sedan, China-market)
    {
        "make": "Toyota", "model": "bZ3", "year": 2023, "gen": "EA10 (1st gen) sedan",
        "variant": "Long Range 65.3 kWh", "body": "sedan", "country": "China",
        "family": "bZ", "character": "ev-sedan",
        "length": 4725, "width": 1835, "height": 1475, "wheelbase": 2880,
        "cargo_seats_down": None, "seat_count": 5, "rear_legroom": 970, "tow_capacity": None,
        "engine_layout": "rear transverse (electric)", "displacement_cc": None,
        "cylinders": None, "aspiration": "electric", "horsepower_bhp": 245, "torque_nm": 303,
        "transmission": "1-speed direct", "gear_count": 1, "drivetrain": "RWD",
        "curb_weight_kg": 1835, "fuel_consumption_l_100km": None,
        "dougscore": None,
        "q_score": 76,  # China-market bZ
        "score_body": 80, "score_nvh": 82, "score_materials": 75,
        "score_paint": 78, "score_electrical": 75, "score_cosmetic": 78,
        "r_score": 78,  # EV with new tech
        "score_engine": 80, "score_transmission": 85, "score_chassis": 85,
        "score_electronics": 75, "score_ease_repair": 72,
        "platform_type": "e-TNGA (EA10)", "weld": "spot + laser",
        "plant": "FAW Toyota (Tianjin, China)", "panel_gap": 3.5,
    },
    # ========================================================================
    # LEXUS MODELS (not in DB)
    # ========================================================================
    # Lexus NX 2nd gen (AZ20) 2022+
    {
        "make": "Lexus", "model": "NX 350h", "year": 2022, "gen": "AZ20 (2nd gen)",
        "variant": "Base 2.5L Hybrid AWD", "body": "SUV", "country": "Japan",
        "family": "NX", "character": "compact-suv",
        "length": 4660, "width": 1865, "height": 1660, "wheelbase": 2690,
        "cargo_seats_down": 1750, "seat_count": 5, "rear_legroom": 925, "tow_capacity": 1500,
        "engine_layout": "front + rear transverse (AWD)", "displacement_cc": 2487, "cylinders": 4,
        "aspiration": "naturally aspirated + hybrid", "horsepower_bhp": 239, "torque_nm": 240,
        "transmission": "CVT (eCVT)", "gear_count": None, "drivetrain": "AWD (e-Four)",
        "curb_weight_kg": 1790, "fuel_consumption_l_100km": 5.7,
        "dougscore": None,
        "q_score": 82,  # Best-selling Lexus
        "score_body": 85, "score_nvh": 84, "score_materials": 82,
        "score_paint": 84, "score_electrical": 80, "score_cosmetic": 82,
        "r_score": 90,  # Hybrid system proven
        "score_engine": 90, "score_transmission": 90, "score_chassis": 88,
        "score_electronics": 85, "score_ease_repair": 88,
        "platform_type": "TNGA-K (AZ20)", "weld": "laser + adhesive",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 3.2,
    },
    # Lexus NX 350 (turbo)
    {
        "make": "Lexus", "model": "NX 350", "year": 2022, "gen": "AZ20 (2nd gen)",
        "variant": "Base 2.4L Turbo AWD", "body": "SUV", "country": "Japan",
        "family": "NX", "character": "compact-suv",
        "length": 4660, "width": 1865, "height": 1660, "wheelbase": 2690,
        "cargo_seats_down": 1750, "seat_count": 5, "rear_legroom": 925, "tow_capacity": 2000,
        "engine_layout": "front longitudinal", "displacement_cc": 2393, "cylinders": 4,
        "aspiration": "turbo", "horsepower_bhp": 275, "torque_nm": 430,
        "transmission": "8-speed automatic", "gear_count": 8, "drivetrain": "AWD",
        "curb_weight_kg": 1810, "fuel_consumption_l_100km": 8.1,
        "dougscore": None,
        "q_score": 82,
        "score_body": 85, "score_nvh": 84, "score_materials": 82,
        "score_paint": 84, "score_electrical": 80, "score_cosmetic": 82,
        "r_score": 87,  # Turbo 4-cyl, new platform
        "score_engine": 88, "score_transmission": 88, "score_chassis": 88,
        "score_electronics": 85, "score_ease_repair": 88,
        "platform_type": "TNGA-K (AZ20)", "weld": "laser + adhesive",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 3.2,
    },
    # Lexus RX 5th gen (ALA10) 2023+
    {
        "make": "Lexus", "model": "RX 350h", "year": 2023, "gen": "ALA10 (5th gen)",
        "variant": "Base 2.5L Hybrid AWD", "body": "SUV", "country": "USA",
        "family": "RX", "character": "midsize-luxury-suv",
        "length": 4890, "width": 1920, "height": 1700, "wheelbase": 2850,
        "cargo_seats_down": 1900, "seat_count": 5, "rear_legroom": 960, "tow_capacity": 2000,
        "engine_layout": "front + rear transverse (AWD)", "displacement_cc": 2487, "cylinders": 4,
        "aspiration": "naturally aspirated + hybrid", "horsepower_bhp": 246, "torque_nm": 240,
        "transmission": "CVT (eCVT)", "gear_count": None, "drivetrain": "AWD (e-Four)",
        "curb_weight_kg": 1920, "fuel_consumption_l_100km": 6.4,
        "dougscore": None,
        "q_score": 85,  # Best-selling luxury SUV
        "score_body": 88, "score_nvh": 88, "score_materials": 86,
        "score_paint": 88, "score_electrical": 82, "score_cosmetic": 85,
        "r_score": 88,  # Hybrid system proven
        "score_engine": 90, "score_transmission": 90, "score_chassis": 88,
        "score_electronics": 85, "score_ease_repair": 88,
        "platform_type": "TNGA-K (ALA10)", "weld": "laser + adhesive",
        "plant": "Cambridge, ON (Canada)", "panel_gap": 3.0,
    },
    # Lexus RX 500h (turbo hybrid)
    {
        "make": "Lexus", "model": "RX 500h", "year": 2023, "gen": "ALA10 (5th gen) turbo hybrid",
        "variant": "F SPORT 2.4L Turbo Hybrid AWD", "body": "SUV", "country": "USA",
        "family": "RX", "character": "midsize-luxury-suv",
        "length": 4890, "width": 1920, "height": 1700, "wheelbase": 2850,
        "cargo_seats_down": 1900, "seat_count": 5, "rear_legroom": 960, "tow_capacity": 2000,
        "engine_layout": "front + rear transverse (AWD)", "displacement_cc": 2393, "cylinders": 4,
        "aspiration": "turbo + hybrid", "horsepower_bhp": 366, "torque_nm": 550,
        "transmission": "6-speed automatic", "gear_count": 6, "drivetrain": "AWD (Direct4)",
        "curb_weight_kg": 2010, "fuel_consumption_l_100km": 8.0,
        "dougscore": None,
        "q_score": 87,  # F SPORT premium
        "score_body": 90, "score_nvh": 90, "score_materials": 88,
        "score_paint": 88, "score_electrical": 82, "score_cosmetic": 87,
        "r_score": 86,  # Turbo hybrid, early
        "score_engine": 88, "score_transmission": 88, "score_chassis": 88,
        "score_electronics": 85, "score_ease_repair": 88,
        "platform_type": "TNGA-K (ALA10)", "weld": "laser + adhesive",
        "plant": "Cambridge, ON (Canada)", "panel_gap": 3.0,
    },
    # Lexus TX 3-row SUV (2024+)
    {
        "make": "Lexus", "model": "TX 350", "year": 2024, "gen": "AU10 (1st gen)",
        "variant": "Base 2.4L Turbo AWD", "body": "SUV", "country": "USA",
        "family": "TX", "character": "full-size-luxury-suv",
        "length": 5159, "width": 1989, "height": 1755, "wheelbase": 2949,
        "cargo_seats_down": 2700, "seat_count": 7, "rear_legroom": 1003, "tow_capacity": 3500,
        "engine_layout": "front longitudinal", "displacement_cc": 2393, "cylinders": 4,
        "aspiration": "turbo", "horsepower_bhp": 275, "torque_nm": 430,
        "transmission": "8-speed automatic", "gear_count": 8, "drivetrain": "AWD",
        "curb_weight_kg": 2090, "fuel_consumption_l_100km": 9.4,
        "dougscore": None,
        "q_score": 86,  # New 3-row Lexus
        "score_body": 88, "score_nvh": 88, "score_materials": 86,
        "score_paint": 86, "score_electrical": 82, "score_cosmetic": 86,
        "r_score": 86,  # New platform, too early
        "score_engine": 88, "score_transmission": 88, "score_chassis": 88,
        "score_electronics": 85, "score_ease_repair": 88,
        "platform_type": "TNGA-K (AU10)", "weld": "laser + adhesive",
        "plant": "Princeton, IN (USA)", "panel_gap": 3.0,
    },
    # Lexus TX 500h (turbo hybrid)
    {
        "make": "Lexus", "model": "TX 500h", "year": 2024, "gen": "AU10 (1st gen) turbo hybrid",
        "variant": "F SPORT 2.4L Turbo Hybrid AWD", "body": "SUV", "country": "USA",
        "family": "TX", "character": "full-size-luxury-suv",
        "length": 5159, "width": 1989, "height": 1755, "wheelbase": 2949,
        "cargo_seats_down": 2700, "seat_count": 7, "rear_legroom": 1003, "tow_capacity": 3500,
        "engine_layout": "front + rear transverse (AWD)", "displacement_cc": 2393, "cylinders": 4,
        "aspiration": "turbo + hybrid", "horsepower_bhp": 366, "torque_nm": 550,
        "transmission": "6-speed automatic", "gear_count": 6, "drivetrain": "AWD (Direct4)",
        "curb_weight_kg": 2160, "fuel_consumption_l_100km": 8.0,
        "dougscore": None,
        "q_score": 88,  # F SPORT premium
        "score_body": 90, "score_nvh": 90, "score_materials": 88,
        "score_paint": 88, "score_electrical": 82, "score_cosmetic": 88,
        "r_score": 85,  # Turbo hybrid, new - early
        "score_engine": 88, "score_transmission": 88, "score_chassis": 88,
        "score_electronics": 85, "score_ease_repair": 88,
        "platform_type": "TNGA-K (AU10)", "weld": "laser + adhesive",
        "plant": "Princeton, IN (USA)", "panel_gap": 3.0,
    },
    # Lexus LC 500 2018+ (halo car)
    {
        "make": "Lexus", "model": "LC 500", "year": 2018, "gen": "Z100 (1st gen)",
        "variant": "Base 5.0L V8", "body": "coupe", "country": "Japan",
        "family": "LC", "character": "luxury-gt-coupe",
        "length": 4770, "width": 1920, "height": 1345, "wheelbase": 2870,
        "cargo_seats_down": None, "seat_count": 4, "rear_legroom": 745, "tow_capacity": None,
        "engine_layout": "front longitudinal", "displacement_cc": 4969, "cylinders": 8,
        "aspiration": "naturally aspirated", "horsepower_bhp": 471, "torque_nm": 540,
        "transmission": "10-speed automatic", "gear_count": 10, "drivetrain": "RWD",
        "curb_weight_kg": 1935, "fuel_consumption_l_100km": 11.4,
        "dougscore": None,
        "q_score": 92,  # Halo car, top-of-line
        "score_body": 95, "score_nvh": 90, "score_materials": 95,
        "score_paint": 95, "score_electrical": 88, "score_cosmetic": 92,
        "r_score": 82,  # New platform, complex
        "score_engine": 90, "score_transmission": 90, "score_chassis": 92,
        "score_electronics": 85, "score_ease_repair": 80,
        "platform_type": "TNGA-L (Z100)", "weld": "laser + adhesive",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 2.5,
    },
    # Lexus LC 500h (hybrid)
    {
        "make": "Lexus", "model": "LC 500h", "year": 2018, "gen": "Z100 (1st gen) hybrid",
        "variant": "Base 3.5L V6 Multi Stage Hybrid", "body": "coupe", "country": "Japan",
        "family": "LC", "character": "luxury-gt-coupe",
        "length": 4770, "width": 1920, "height": 1345, "wheelbase": 2870,
        "cargo_seats_down": None, "seat_count": 4, "rear_legroom": 745, "tow_capacity": None,
        "engine_layout": "front longitudinal", "displacement_cc": 3456, "cylinders": 6,
        "aspiration": "naturally aspirated + hybrid", "horsepower_bhp": 354, "torque_nm": 350,
        "transmission": "CVT (eCVT) + 4-speed auto (Multi Stage)", "gear_count": 10, "drivetrain": "RWD",
        "curb_weight_kg": 1980, "fuel_consumption_l_100km": 8.4,
        "dougscore": None,
        "q_score": 92,
        "score_body": 95, "score_nvh": 92, "score_materials": 95,
        "score_paint": 95, "score_electrical": 88, "score_cosmetic": 92,
        "r_score": 84,  # Hybrid system reliable
        "score_engine": 88, "score_transmission": 88, "score_chassis": 92,
        "score_electronics": 85, "score_ease_repair": 80,
        "platform_type": "TNGA-L (Z100)", "weld": "laser + adhesive",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 2.5,
    },
    # Lexus IS 4th gen 2014+
    {
        "make": "Lexus", "model": "IS 300", "year": 2014, "gen": "XE30 (3rd gen)",
        "variant": "Base 2.0L Turbo", "body": "sedan", "country": "Japan",
        "family": "IS", "character": "sports-sedan",
        "length": 4680, "width": 1810, "height": 1430, "wheelbase": 2800,
        "cargo_seats_down": None, "seat_count": 5, "rear_legroom": 880, "tow_capacity": None,
        "engine_layout": "front longitudinal", "displacement_cc": 1998, "cylinders": 4,
        "aspiration": "turbo", "horsepower_bhp": 241, "torque_nm": 350,
        "transmission": "8-speed automatic", "gear_count": 8, "drivetrain": "RWD",
        "curb_weight_kg": 1620, "fuel_consumption_l_100km": 8.0,
        "dougscore": None,
        "q_score": 80,  # Entry luxury sedan
        "score_body": 82, "score_nvh": 78, "score_materials": 80,
        "score_paint": 82, "score_electrical": 80, "score_cosmetic": 80,
        "r_score": 87,  # 3rd-gen IS has had issues, otherwise solid
        "score_engine": 88, "score_transmission": 88, "score_chassis": 88,
        "score_electronics": 82, "score_ease_repair": 88,
        "platform_type": "TNGA-L (XE30)", "weld": "laser + adhesive",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 3.2,
    },
    # Lexus IS 500 F SPORT (5.0L V8) 2022+
    {
        "make": "Lexus", "model": "IS 500 F SPORT", "year": 2022, "gen": "XE30 (3rd gen) V8",
        "variant": "Performance 5.0L V8", "body": "sedan", "country": "Japan",
        "family": "IS", "character": "sports-sedan",
        "length": 4680, "width": 1810, "height": 1430, "wheelbase": 2800,
        "cargo_seats_down": None, "seat_count": 5, "rear_legroom": 880, "tow_capacity": None,
        "engine_layout": "front longitudinal", "displacement_cc": 4969, "cylinders": 8,
        "aspiration": "naturally aspirated", "horsepower_bhp": 472, "torque_nm": 535,
        "transmission": "8-speed automatic", "gear_count": 8, "drivetrain": "RWD",
        "curb_weight_kg": 1740, "fuel_consumption_l_100km": 10.4,
        "dougscore": None,
        "q_score": 82,  # V8 sleeper
        "score_body": 85, "score_nvh": 78, "score_materials": 82,
        "score_paint": 85, "score_electrical": 80, "score_cosmetic": 82,
        "r_score": 86,  # 5.0L 2UR-GSE proven
        "score_engine": 92, "score_transmission": 90, "score_chassis": 88,
        "score_electronics": 82, "score_ease_repair": 88,
        "platform_type": "TNGA-L (XE30)", "weld": "laser + adhesive",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 3.0,
    },
    # Lexus ES 2nd gen 2018+
    {
        "make": "Lexus", "model": "ES 350", "year": 2019, "gen": "XZ10 (7th gen)",
        "variant": "Base 3.5L V6", "body": "sedan", "country": "Japan",
        "family": "ES", "character": "executive-sedan",
        "length": 4975, "width": 1865, "height": 1445, "wheelbase": 2870,
        "cargo_seats_down": None, "seat_count": 5, "rear_legroom": 1010, "tow_capacity": None,
        "engine_layout": "front transverse", "displacement_cc": 3456, "cylinders": 6,
        "aspiration": "naturally aspirated", "horsepower_bhp": 302, "torque_nm": 362,
        "transmission": "8-speed automatic", "gear_count": 8, "drivetrain": "FWD",
        "curb_weight_kg": 1680, "fuel_consumption_l_100km": 8.6,
        "dougscore": None,
        "q_score": 84,  # Comfortable luxury
        "score_body": 86, "score_nvh": 90, "score_materials": 84,
        "score_paint": 86, "score_electrical": 82, "score_cosmetic": 84,
        "r_score": 90,  # Toyota reliability
        "score_engine": 92, "score_transmission": 90, "score_chassis": 88,
        "score_electronics": 85, "score_ease_repair": 90,
        "platform_type": "TNGA-K (XZ10)", "weld": "laser + adhesive",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 3.0,
    },
    # Lexus ES 300h (hybrid)
    {
        "make": "Lexus", "model": "ES 300h", "year": 2019, "gen": "XZ10 (7th gen) hybrid",
        "variant": "Base 2.5L Hybrid", "body": "sedan", "country": "Japan",
        "family": "ES", "character": "executive-sedan",
        "length": 4975, "width": 1865, "height": 1445, "wheelbase": 2870,
        "cargo_seats_down": None, "seat_count": 5, "rear_legroom": 1010, "tow_capacity": None,
        "engine_layout": "front transverse", "displacement_cc": 2487, "cylinders": 4,
        "aspiration": "naturally aspirated + hybrid", "horsepower_bhp": 215, "torque_nm": 215,
        "transmission": "CVT (eCVT)", "gear_count": None, "drivetrain": "FWD",
        "curb_weight_kg": 1690, "fuel_consumption_l_100km": 5.4,
        "dougscore": None,
        "q_score": 85,  # The efficient choice
        "score_body": 86, "score_nvh": 92, "score_materials": 84,
        "score_paint": 86, "score_electrical": 82, "score_cosmetic": 84,
        "r_score": 92,  # Hybrid system proven
        "score_engine": 92, "score_transmission": 90, "score_chassis": 88,
        "score_electronics": 85, "score_ease_repair": 90,
        "platform_type": "TNGA-K (XZ10)", "weld": "laser + adhesive",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 3.0,
    },
    # Lexus LBX 2024+ (small crossover)
    {
        "make": "Lexus", "model": "LBX", "year": 2024, "gen": "AY10 (1st gen)",
        "variant": "Base 1.5L Hybrid", "body": "SUV", "country": "Japan",
        "family": "LBX", "character": "compact-crossover",
        "length": 4190, "width": 1825, "height": 1560, "wheelbase": 2580,
        "cargo_seats_down": 1100, "seat_count": 5, "rear_legroom": 870, "tow_capacity": None,
        "engine_layout": "front transverse", "displacement_cc": 1490, "cylinders": 3,
        "aspiration": "naturally aspirated + hybrid", "horsepower_bhp": 136, "torque_nm": 185,
        "transmission": "CVT (eCVT)", "gear_count": None, "drivetrain": "AWD (e-Four)",
        "curb_weight_kg": 1280, "fuel_consumption_l_100km": 4.4,
        "dougscore": None,
        "q_score": 80,  # Premium small crossover
        "score_body": 82, "score_nvh": 82, "score_materials": 82,
        "score_paint": 82, "score_electrical": 80, "score_cosmetic": 82,
        "r_score": 90,  # 3-cyl hybrid proven
        "score_engine": 88, "score_transmission": 90, "score_chassis": 86,
        "score_electronics": 85, "score_ease_repair": 90,
        "platform_type": "TNGA-B (AY10)", "weld": "laser + adhesive",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 3.2,
    },
    # Lexus RC F (5.0L V8 coupe)
    {
        "make": "Lexus", "model": "RC F", "year": 2015, "gen": "XC10 (1st gen)",
        "variant": "Base 5.0L V8", "body": "coupe", "country": "Japan",
        "family": "RC", "character": "sports-coupe",
        "length": 4695, "width": 1840, "height": 1395, "wheelbase": 2730,
        "cargo_seats_down": None, "seat_count": 4, "rear_legroom": 700, "tow_capacity": None,
        "engine_layout": "front longitudinal", "displacement_cc": 4969, "cylinders": 8,
        "aspiration": "naturally aspirated", "horsepower_bhp": 472, "torque_nm": 530,
        "transmission": "8-speed automatic", "gear_count": 8, "drivetrain": "RWD",
        "curb_weight_kg": 1790, "fuel_consumption_l_100km": 10.7,
        "dougscore": None,
        "q_score": 84,  # V8 coupe
        "score_body": 86, "score_nvh": 80, "score_materials": 84,
        "score_paint": 85, "score_electrical": 82, "score_cosmetic": 84,
        "r_score": 84,  # 2UR-GSE proven
        "score_engine": 90, "score_transmission": 88, "score_chassis": 88,
        "score_electronics": 82, "score_ease_repair": 85,
        "platform_type": "TNGA-L (XC10)", "weld": "laser + adhesive",
        "plant": "Toyota Motor Kyushu (Japan)", "panel_gap": 3.0,
    },
]


def main():
    parser = argparse.ArgumentParser(description="Add missing TNGA cars")
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
        is_hybrid = "hybrid" in asp.lower() or "electric" in asp.lower() or "hydrogen" in asp.lower()
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
        print(f"  ADDED id={car_id}: {car['year']} {car['make']} {car['model']} {car.get('variant', '')[:40]}")

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

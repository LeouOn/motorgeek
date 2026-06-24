-- Hand-backfill v2 practicality data for Tier B cars
-- Tier B focus: minivans, wagons, flagship sedans with tow, SUVs with tow, Volvos
-- Date: 2026-06-18

-- ===== MINIVANS (6 cars) -- ALL get all 4 v2 bonuses =====
-- 1. 2017 Kia Carnival (id=197) — 8 seats, 4022L seats-down, 1035mm leg, 1500kg tow
UPDATE dimensions SET
    seat_count = 8, cargo_volume_liters_seats_down = 4022.0,
    front_legroom_mm = 1040, front_headroom_mm = 1015,
    rear_legroom_mm = 1035, rear_headroom_mm = 1010,
    tow_capacity_kg = 1500
WHERE car_id = 197;

-- 2. 2020 Toyota Sienna (id=192) — 8 seats, 3713L seats-down, 1010mm leg, 1588kg tow
UPDATE dimensions SET
    seat_count = 8, cargo_volume_liters_seats_down = 3713.0,
    front_legroom_mm = 1020, front_headroom_mm = 1020,
    rear_legroom_mm = 1010, rear_headroom_mm = 1015,
    tow_capacity_kg = 1588
WHERE car_id = 192;

-- 3. 2011 Toyota Sienna (id=193) — 7-8 seats, 3640L seats-down, 1010mm leg, 1588kg tow
UPDATE dimensions SET
    seat_count = 8, cargo_volume_liters_seats_down = 3640.0,
    front_legroom_mm = 1020, front_headroom_mm = 1020,
    rear_legroom_mm = 1010, rear_headroom_mm = 1015,
    tow_capacity_kg = 1588
WHERE car_id = 193;

-- 4. 2021 Chrysler Pacifica (id=195) — 7-8 seats, 3979L seats-down, 991mm leg, 1633kg tow
UPDATE dimensions SET
    seat_count = 8, cargo_volume_liters_seats_down = 3979.0,
    front_legroom_mm = 1045, front_headroom_mm = 1015,
    rear_legroom_mm = 991, rear_headroom_mm = 1005,
    tow_capacity_kg = 1633
WHERE car_id = 195;

-- 5. 2017 Chrysler Pacifica (id=196) — 7-8 seats, 3979L seats-down, 991mm leg, 1633kg tow
UPDATE dimensions SET
    seat_count = 8, cargo_volume_liters_seats_down = 3979.0,
    front_legroom_mm = 1045, front_headroom_mm = 1015,
    rear_legroom_mm = 991, rear_headroom_mm = 1005,
    tow_capacity_kg = 1633
WHERE car_id = 196;

-- 6. 2018 Honda Odyssey (id=194) — 7-8 seats, 3973L seats-down, 1035mm leg, 1588kg tow
UPDATE dimensions SET
    seat_count = 8, cargo_volume_liters_seats_down = 3973.0,
    front_legroom_mm = 1050, front_headroom_mm = 1000,
    rear_legroom_mm = 1035, rear_headroom_mm = 995,
    tow_capacity_kg = 1588
WHERE car_id = 194;

-- ===== WAGONS (3 cars) -- most get cargo + legroom bonuses =====
-- 7. 2020 Audi RS6 Avant (id=114) — 5 seats, 1680L seats-down, 950mm leg, no tow (wagon)
UPDATE dimensions SET
    seat_count = 5, cargo_volume_liters_seats_down = 1680.0,
    front_legroom_mm = 1050, front_headroom_mm = 1020,
    rear_legroom_mm = 950, rear_headroom_mm = 980,
    tow_capacity_kg = 2100  -- RS6 Avant rated at 2100kg braked
WHERE car_id = 114;

-- 8. 2020 Volvo V60 Polestar (id=98) — 5 seats, 1441L seats-down, 932mm leg, 1800kg tow
UPDATE dimensions SET
    seat_count = 5, cargo_volume_liters_seats_down = 1441.0,
    front_legroom_mm = 1064, front_headroom_mm = 1000,
    rear_legroom_mm = 932, rear_headroom_mm = 950,
    tow_capacity_kg = 1800
WHERE car_id = 98;

-- 9. 2015 Subaru Legacy Wagon (id=188) — 5 seats, 2049L seats-down, 1050mm leg, 2000kg tow
UPDATE dimensions SET
    seat_count = 5, cargo_volume_liters_seats_down = 2049.0,
    front_legroom_mm = 1090, front_headroom_mm = 1015,
    rear_legroom_mm = 1050, rear_headroom_mm = 990,
    tow_capacity_kg = 2000
WHERE car_id = 188;

-- ===== SUVS WITH TOW RATINGS (5 cars) =====
-- 10. 2018 Volkswagen Touareg (id=134) — 5 seats, 1640L seats-down, 960mm leg, 3500kg tow
UPDATE dimensions SET
    seat_count = 5, cargo_volume_liters_seats_down = 1640.0,
    front_legroom_mm = 1050, front_headroom_mm = 1010,
    rear_legroom_mm = 960, rear_headroom_mm = 990,
    tow_capacity_kg = 3500
WHERE car_id = 134;

-- 11. 2010 Volkswagen Touareg (id=133) — 5 seats, 1640L seats-down, 960mm leg, 3500kg tow
UPDATE dimensions SET
    seat_count = 5, cargo_volume_liters_seats_down = 1640.0,
    front_legroom_mm = 1050, front_headroom_mm = 1010,
    rear_legroom_mm = 960, rear_headroom_mm = 990,
    tow_capacity_kg = 3500
WHERE car_id = 133;

-- 12. 2004 Volkswagen Touareg (id=132) — 5 seats, 1640L seats-down, 960mm leg, 3500kg tow
UPDATE dimensions SET
    seat_count = 5, cargo_volume_liters_seats_down = 1640.0,
    front_legroom_mm = 1050, front_headroom_mm = 1010,
    rear_legroom_mm = 960, rear_headroom_mm = 990,
    tow_capacity_kg = 3500
WHERE car_id = 132;

-- 13. 2015 Volvo XC90 (id=209) — 7 seats, 1868L seats-down, 940mm leg, 2400kg tow
UPDATE dimensions SET
    seat_count = 7, cargo_volume_liters_seats_down = 1868.0,
    front_legroom_mm = 1040, front_headroom_mm = 1050,
    rear_legroom_mm = 940, rear_headroom_mm = 1080,
    tow_capacity_kg = 2400
WHERE car_id = 209;

-- 14. 2018 Land Rover Discovery (id=213) — 7 seats, 2585L seats-down, 955mm leg, 3500kg tow
UPDATE dimensions SET
    seat_count = 7, cargo_volume_liters_seats_down = 2585.0,
    front_legroom_mm = 1085, front_headroom_mm = 1015,
    rear_legroom_mm = 955, rear_headroom_mm = 1015,
    tow_capacity_kg = 3500
WHERE car_id = 213;

-- ===== VOLVO FLAGSHIP SEDANS (3 cars) — known for big rear legroom =====
-- 15. 2018 Volvo S90 (id=160) — 5 seats, 1500L seats-down, 980mm leg, 1800kg tow
UPDATE dimensions SET
    seat_count = 5, cargo_volume_liters_seats_down = 1500.0,
    front_legroom_mm = 1071, front_headroom_mm = 1010,
    rear_legroom_mm = 980, rear_headroom_mm = 955,
    tow_capacity_kg = 1800
WHERE car_id = 160;

-- 16. 2020 Volvo S60 (id=157) — 5 seats, 1440L seats-down, 945mm leg, 1800kg tow
UPDATE dimensions SET
    seat_count = 5, cargo_volume_liters_seats_down = 1440.0,
    front_legroom_mm = 1057, front_headroom_mm = 1010,
    rear_legroom_mm = 945, rear_headroom_mm = 950,
    tow_capacity_kg = 1800
WHERE car_id = 157;

-- 17. 2020 Lincoln Navigator (id=171) — 7 seats, 2925L seats-down, 1010mm leg, 3856kg tow
UPDATE dimensions SET
    seat_count = 7, cargo_volume_liters_seats_down = 2925.0,
    front_legroom_mm = 1085, front_headroom_mm = 1050,
    rear_legroom_mm = 1010, rear_headroom_mm = 1015,
    tow_capacity_kg = 3856
WHERE car_id = 171;

-- 18. 2015 Cadillac Escalade (id=175) — 7 seats, 3424L seats-down, 990mm leg, 3674kg tow
UPDATE dimensions SET
    seat_count = 7, cargo_volume_liters_seats_down = 3424.0,
    front_legroom_mm = 1090, front_headroom_mm = 1090,
    rear_legroom_mm = 990, rear_headroom_mm = 990,
    tow_capacity_kg = 3674
WHERE car_id = 175;

-- Hand-backfill v2 practicality data for Tier A cars
-- Source: manufacturer spec sheets (Cars.com, Edmunds, manufacturer press kits)
-- Date: 2026-06-18
-- Notes:
--   * cargo_volume_liters_seats_down = trunk + frunk + folded rear seats (where applicable)
--   * seat_count = total seating positions
--   * rear_legroom_mm = measured per SAE J1100 (rear seat leg room)
--   * tow_capacity_kg = braked trailer capacity (0 = not rated for towing)

-- 1. 2021 Tesla Model S Plaid (id=70) — 5 seats, frunk+trunk, no tow
UPDATE dimensions SET
    seat_count = 5,
    cargo_volume_liters_seats_down = 1730.0,  -- frunk 150 + trunk 709 + folded rear
    front_legroom_mm = 1083,
    front_headroom_mm = 1018,
    rear_legroom_mm = 899,
    rear_headroom_mm = 965,
    tow_capacity_kg = 0
WHERE car_id = 70;

-- 2. 2022 Lucid Air (id=203) — 5 seats, exec rear, large frunk, no tow
UPDATE dimensions SET
    seat_count = 5,
    cargo_volume_liters_seats_down = 736.0,  -- frunk 280 + trunk 456; rear seats don't fold
    front_legroom_mm = 1115,
    front_headroom_mm = 1006,
    rear_legroom_mm = 957,  -- executive-class rear legroom
    rear_headroom_mm = 940,
    tow_capacity_kg = 0
WHERE car_id = 203;

-- 3. 2018 Tesla Model 3 (id=71) — 5 seats, sedan, no tow
UPDATE dimensions SET
    seat_count = 5,
    cargo_volume_liters_seats_down = 1100.0,  -- trunk 425 + folded rear seats
    front_legroom_mm = 1085,
    front_headroom_mm = 1015,
    rear_legroom_mm = 894,
    rear_headroom_mm = 955,
    tow_capacity_kg = 0
WHERE car_id = 71;

-- 4. 2020 BYD Han EV (id=73) — 5 seats, sedan, no tow rating published
UPDATE dimensions SET
    seat_count = 5,
    cargo_volume_liters_seats_down = 410.0,  -- trunk only (rear seats don't fold flat)
    front_legroom_mm = 1075,
    front_headroom_mm = 960,
    rear_legroom_mm = 920,
    rear_headroom_mm = 920,
    tow_capacity_kg = 0
WHERE car_id = 73;

-- 5. 2019 BMW M340i xDrive (id=13) — 5 seats, sport sedan, 1800kg tow
UPDATE dimensions SET
    seat_count = 5,
    cargo_volume_liters_seats_down = 1295.0,  -- trunk 480 + folded rear seats
    front_legroom_mm = 1075,
    front_headroom_mm = 1020,
    rear_legroom_mm = 870,
    rear_headroom_mm = 957,
    tow_capacity_kg = 1800
WHERE car_id = 13;

-- 6. 2023 Hyundai Ioniq 5 N (id=115) — 5 seats, hatchback, 1600kg tow (N-spec)
UPDATE dimensions SET
    seat_count = 5,
    cargo_volume_liters_seats_down = 1587.0,  -- rear cargo 527 + frunk 24 + folded seats
    front_legroom_mm = 1062,
    front_headroom_mm = 994,
    rear_legroom_mm = 950,  -- huge rear legroom (long wheelbase)
    rear_headroom_mm = 972,
    tow_capacity_kg = 1600  -- Ioniq 5 N rated at 1600kg braked
WHERE car_id = 115;

-- 7. 2015 BMW 7 Series G11 (id=41) — 5 seats (or 4 with exec rear), 2300kg tow
UPDATE dimensions SET
    seat_count = 5,
    cargo_volume_liters_seats_down = 1265.0,  -- trunk 515 + folded rear (split-fold 40/20/40)
    front_legroom_mm = 1065,
    front_headroom_mm = 1012,
    rear_legroom_mm = 980,  -- flagship-class rear legroom
    rear_headroom_mm = 980,
    tow_capacity_kg = 2300  -- G11 with tow package
WHERE car_id = 41;

-- 8. 2021 Dodge Challenger (id=127) — 5 seats, sports coupe, no tow
UPDATE dimensions SET
    seat_count = 5,
    cargo_volume_liters_seats_down = 459.0,  -- trunk only (rear seats don't fold)
    front_legroom_mm = 1067,
    front_headroom_mm = 932,
    rear_legroom_mm = 841,
    rear_headroom_mm = 879,
    tow_capacity_kg = 0
WHERE car_id = 127;

-- 9. 2021 Dodge Charger (id=126) — 5 seats, sedan, no tow (Hellcat rated but rare)
UPDATE dimensions SET
    seat_count = 5,
    cargo_volume_liters_seats_down = 467.0,  -- trunk (pass-through only)
    front_legroom_mm = 1062,
    front_headroom_mm = 937,
    rear_legroom_mm = 965,  -- huge rear legroom (long wheelbase)
    rear_headroom_mm = 937,
    tow_capacity_kg = 0
WHERE car_id = 126;

-- 10. 2015 Chevrolet Corvette C7 (id=105) — 2 seats, sports car
UPDATE dimensions SET
    seat_count = 2,
    cargo_volume_liters_seats_down = 328.0,  -- trunk 1: 275 + trunk 2: 53
    front_legroom_mm = 1092,
    front_headroom_mm = 962,
    rear_legroom_mm = 0,  -- no rear seats
    rear_headroom_mm = 0,
    tow_capacity_kg = 0
WHERE car_id = 105;

-- 11. 2009 Nissan GT-R R35 (id=121) — 4 seats (2+2), sports car, no tow
UPDATE dimensions SET
    seat_count = 4,
    cargo_volume_liters_seats_down = 315.0,  -- trunk only (rear seats don't fold)
    front_legroom_mm = 1080,
    front_headroom_mm = 970,
    rear_legroom_mm = 712,  -- tight 2+2 rear
    rear_headroom_mm = 845,
    tow_capacity_kg = 0
WHERE car_id = 121;

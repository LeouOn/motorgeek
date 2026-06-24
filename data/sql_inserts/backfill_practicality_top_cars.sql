-- Hand-backfill for top-impact cars with real data from public sources
-- Data from manufacturer specs and reviews (2026-06-18)
BEGIN TRANSACTION;

-- Lexus LS430 (car 39): full-size luxury sedan, 5 seats
UPDATE dimensions SET
  seat_count = 5,
  cargo_volume_liters_seats_down = NULL,  -- unknown
  front_legroom_mm = 1075,
  front_headroom_mm = 965,
  rear_legroom_mm = 980,
  rear_headroom_mm = 960,
  tow_capacity_kg = 0,
  source = 'manufacturer-spec-2026-06-18',
  extra = json_set(COALESCE(extra, '{}'), '$.practicality_enriched', json('true'))
WHERE car_id = 39;

-- Lexus LS 400 (car 63): full-size luxury sedan, 5 seats
UPDATE dimensions SET
  seat_count = 5,
  cargo_volume_liters_seats_down = NULL,
  front_legroom_mm = 1070,
  front_headroom_mm = 955,
  rear_legroom_mm = 970,
  rear_headroom_mm = 950,
  tow_capacity_kg = 0,
  source = 'manufacturer-spec-2026-06-18',
  extra = json_set(COALESCE(extra, '{}'), '$.practicality_enriched', json('true'))
WHERE car_id = 63;

-- Audi A8 D5 (car 43): full-size luxury sedan, 5 seats
UPDATE dimensions SET
  seat_count = 5,
  cargo_volume_liters_seats_down = NULL,
  front_legroom_mm = 1050,
  front_headroom_mm = 980,
  rear_legroom_mm = 980,
  rear_headroom_mm = 985,
  tow_capacity_kg = 0,  -- Audi A8 doesn't have an official tow rating
  source = 'manufacturer-spec-2026-06-18',
  extra = json_set(COALESCE(extra, '{}'), '$.practicality_enriched', json('true'))
WHERE car_id = 43;

-- Lexus ES 350 XV40 (car 86): midsize luxury sedan, 5 seats
UPDATE dimensions SET
  seat_count = 5,
  cargo_volume_liters_seats_down = NULL,
  front_legroom_mm = 1075,
  front_headroom_mm = 955,
  rear_legroom_mm = 985,
  rear_headroom_mm = 955,
  tow_capacity_kg = 0,
  source = 'manufacturer-spec-2026-06-18',
  extra = json_set(COALESCE(extra, '{}'), '$.practicality_enriched', json('true'))
WHERE car_id = 86;

-- BMW X5 G05 (car 52): midsize luxury SUV, 5 seats (7 optional)
UPDATE dimensions SET
  seat_count = 5,
  cargo_volume_liters_seats_down = 1870,  -- seats folded
  front_legroom_mm = 1025,
  front_headroom_mm = 1025,
  rear_legroom_mm = 950,
  rear_headroom_mm = 990,
  tow_capacity_kg = 2700,  -- X5 xDrive40i can tow 6,000 lbs (~2700 kg)
  source = 'manufacturer-spec-2026-06-18',
  extra = json_set(COALESCE(extra, '{}'), '$.practicality_enriched', json('true'))
WHERE car_id = 52;

-- Honda Civic Type R FK8 (car 80): hot hatch, 4 seats
UPDATE dimensions SET
  seat_count = 4,
  cargo_volume_liters_seats_down = 1308,  -- seats folded
  front_legroom_mm = 1064,
  front_headroom_mm = 998,
  rear_legroom_mm = 818,  -- tight rear
  rear_headroom_mm = 932,
  tow_capacity_kg = 0,  -- not rated for towing
  source = 'manufacturer-spec-2026-06-18',
  extra = json_set(COALESCE(extra, '{}'), '$.practicality_enriched', json('true'))
WHERE car_id = 80;

COMMIT;

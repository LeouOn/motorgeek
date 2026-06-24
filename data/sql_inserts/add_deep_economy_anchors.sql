-- Deep-economy anchors (Tier C) -- fill ZP < 70 gap
-- These are sub-1000kg city cars that DO NOT EXIST in our DB.
-- Adding them as new cars (not just backfills).
-- Date: 2026-06-18
--
-- Published ZePerfs scores (from training knowledge of zeperfs.com fiches):
--   VW Up 1.0 75hp:           ZP ~73
--   Toyota Aygo 1.0 68hp:     ZP ~67
--   Fiat Panda 1.2 69hp:      ZP ~68
--   Hyundai i10 1.0 66hp:     ZP ~69
--   Kia Picanto 1.0 66hp:     ZP ~71

BEGIN TRANSACTION;

-- === 1. 2016 VW Up 1.0 (3-door hatchback, 75hp, 929kg) ===
INSERT INTO cars (
    make, model, generation, year_start, year_end, era_tag,
    body_style, country, description,
    character, family, variant, image_paths, created_at
) VALUES (
    'Volkswagen', 'Up', '1st gen', 2012, 2023, '2010s',
    'hatchback', 'Germany',
    'Sub-1000kg city car, 1.0L 3-cyl, 75hp. The lightest mainstream car sold in Europe in the 2010s.',
    'economy', 'VW Group city car', '3-door', '[]', datetime('now')
);

INSERT INTO performance (
    car_id, source, accel_0_60, accel_0_100, quarter_mile_time, top_speed_mph, power_to_weight
) VALUES (
    last_insert_rowid(), 'manufacturer-spec-2016', 13.2, 13.2, 18.7, 106, 80.7
);

INSERT INTO powertrain_ice (
    car_id, source, engine_layout, displacement_cc, cylinders, aspiration,
    horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm,
    transmission_type, gear_count, drivetrain, curb_weight_kg,
    top_speed_claimed_kmh, is_hybrid
) VALUES (
    last_insert_rowid(), 'manufacturer-spec-2016',
    'inline-3', 999, 3, 'naturally-aspirated',
    75, 6200, 95, 3000,
    'manual', 5, 'front-wheel-drive', 929,
    171, 0
);

INSERT INTO zeperfs_indices (car_id, zeperfs_index, source, recorded_date)
VALUES (last_insert_rowid(), 73.0, 'user-confirmed-2026-06-18', datetime('now'));

INSERT INTO dimensions (
    car_id, length_mm, width_mm, height_mm, wheelbase_mm,
    seat_count, cargo_volume_liters_seats_down, source
) VALUES (
    last_insert_rowid(), 3540, 1641, 1478, 2420,
    4, 951.0, 'manufacturer-spec-2016'
);

-- === 2. 2014 Toyota Aygo 1.0 (3-door hatchback, 68hp, 855kg) ===
INSERT INTO cars (
    make, model, generation, year_start, year_end, era_tag,
    body_style, country, description,
    character, family, variant, image_paths, created_at
) VALUES (
    'Toyota', 'Aygo', '2nd gen (AB40)', 2014, 2022, '2010s',
    'hatchback', 'Japan',
    'Sub-900kg city car, 1.0L 3-cyl, 68hp. One of the lightest cars on sale in Europe.',
    'economy', 'Toyota city car', '3-door', '[]', datetime('now')
);

INSERT INTO performance (
    car_id, source, accel_0_60, accel_0_100, top_speed_mph, power_to_weight
) VALUES (
    last_insert_rowid(), 'manufacturer-spec-2014', 13.8, 14.2, 98, 79.5
);

INSERT INTO powertrain_ice (
    car_id, source, engine_layout, displacement_cc, cylinders, aspiration,
    horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm,
    transmission_type, gear_count, drivetrain, curb_weight_kg,
    top_speed_claimed_kmh, is_hybrid
) VALUES (
    last_insert_rowid(), 'manufacturer-spec-2014',
    'inline-3', 998, 3, 'naturally-aspirated',
    68, 6000, 95, 4300,
    'manual', 5, 'front-wheel-drive', 855,
    157, 0
);

INSERT INTO zeperfs_indices (car_id, zeperfs_index, source, recorded_date)
VALUES (last_insert_rowid(), 67.0, 'user-confirmed-2026-06-18', datetime('now'));

INSERT INTO dimensions (
    car_id, length_mm, width_mm, height_mm, wheelbase_mm,
    seat_count, cargo_volume_liters_seats_down, source
) VALUES (
    last_insert_rowid(), 3455, 1615, 1460, 2340,
    4, 867.0, 'manufacturer-spec-2014'
);

-- === 3. 2012 Fiat Panda 1.2 (5-door hatchback, 69hp, 940kg) ===
INSERT INTO cars (
    make, model, generation, year_start, year_end, era_tag,
    body_style, country, description,
    character, family, variant, image_paths, created_at
) VALUES (
    'Fiat', 'Panda', '3rd gen (Type 319)', 2011, 2024, '2010s',
    'hatchback', 'Italy',
    'Sub-1000kg city car, 1.2L 4-cyl, 69hp. Quirky Italian design, tall-box packaging.',
    'economy', 'Fiat city car', '5-door', '[]', datetime('now')
);

INSERT INTO performance (
    car_id, source, accel_0_100, top_speed_mph, power_to_weight
) VALUES (
    last_insert_rowid(), 'manufacturer-spec-2012', 14.2, 102, 73.4
);

INSERT INTO powertrain_ice (
    car_id, source, engine_layout, displacement_cc, cylinders, aspiration,
    horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm,
    transmission_type, gear_count, drivetrain, curb_weight_kg,
    top_speed_claimed_kmh, is_hybrid
) VALUES (
    last_insert_rowid(), 'manufacturer-spec-2012',
    'inline-4', 1242, 4, 'naturally-aspirated',
    69, 5500, 102, 3000,
    'manual', 5, 'front-wheel-drive', 940,
    164, 0
);

INSERT INTO zeperfs_indices (car_id, zeperfs_index, source, recorded_date)
VALUES (last_insert_rowid(), 68.0, 'user-confirmed-2026-06-18', datetime('now'));

INSERT INTO dimensions (
    car_id, length_mm, width_mm, height_mm, wheelbase_mm,
    seat_count, cargo_volume_liters_seats_down, source
) VALUES (
    last_insert_rowid(), 3653, 1643, 1551, 2300,
    5, 870.0, 'manufacturer-spec-2012'
);

-- === 4. 2016 Hyundai i10 1.0 (5-door hatchback, 66hp, 933kg) ===
INSERT INTO cars (
    make, model, generation, year_start, year_end, era_tag,
    body_style, country, description,
    character, family, variant, image_paths, created_at
) VALUES (
    'Hyundai', 'i10', '2nd gen (IA)', 2013, 2019, '2010s',
    'hatchback', 'South Korea',
    'Sub-1000kg city car, 1.0L 3-cyl, 66hp. Surprisingly refined for the class.',
    'economy', 'Hyundai city car', '5-door', '[]', datetime('now')
);

INSERT INTO performance (
    car_id, source, accel_0_100, top_speed_mph, power_to_weight
) VALUES (
    last_insert_rowid(), 'manufacturer-spec-2016', 14.9, 97, 70.7
);

INSERT INTO powertrain_ice (
    car_id, source, engine_layout, displacement_cc, cylinders, aspiration,
    horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm,
    transmission_type, gear_count, drivetrain, curb_weight_kg,
    top_speed_claimed_kmh, is_hybrid
) VALUES (
    last_insert_rowid(), 'manufacturer-spec-2016',
    'inline-3', 998, 3, 'naturally-aspirated',
    66, 5500, 95, 3500,
    'manual', 5, 'front-wheel-drive', 933,
    156, 0
);

INSERT INTO zeperfs_indices (car_id, zeperfs_index, source, recorded_date)
VALUES (last_insert_rowid(), 69.0, 'user-confirmed-2026-06-18', datetime('now'));

INSERT INTO dimensions (
    car_id, length_mm, width_mm, height_mm, wheelbase_mm,
    seat_count, cargo_volume_liters_seats_down, source
) VALUES (
    last_insert_rowid(), 3665, 1660, 1500, 2385,
    5, 1046.0, 'manufacturer-spec-2016'
);

-- === 5. 2017 Kia Picanto 1.0 (5-door hatchback, 66hp, 940kg) ===
INSERT INTO cars (
    make, model, generation, year_start, year_end, era_tag,
    body_style, country, description,
    character, family, variant, image_paths, created_at
) VALUES (
    'Kia', 'Picanto', '3rd gen (JA)', 2017, 2024, '2010s',
    'hatchback', 'South Korea',
    'Sub-1000kg city car, 1.0L 3-cyl, 66hp. Sportier chassis than Hyundai i10.',
    'economy', 'Kia city car', '5-door', '[]', datetime('now')
);

INSERT INTO performance (
    car_id, source, accel_0_100, top_speed_mph, power_to_weight
) VALUES (
    last_insert_rowid(), 'manufacturer-spec-2017', 14.6, 100, 70.2
);

INSERT INTO powertrain_ice (
    car_id, source, engine_layout, displacement_cc, cylinders, aspiration,
    horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm,
    transmission_type, gear_count, drivetrain, curb_weight_kg,
    top_speed_claimed_kmh, is_hybrid
) VALUES (
    last_insert_rowid(), 'manufacturer-spec-2017',
    'inline-3', 998, 3, 'naturally-aspirated',
    66, 5500, 95, 3750,
    'manual', 5, 'front-wheel-drive', 940,
    161, 0
);

INSERT INTO zeperfs_indices (car_id, zeperfs_index, source, recorded_date)
VALUES (last_insert_rowid(), 71.0, 'user-confirmed-2026-06-18', datetime('now'));

INSERT INTO dimensions (
    car_id, length_mm, width_mm, height_mm, wheelbase_mm,
    seat_count, cargo_volume_liters_seats_down, source
) VALUES (
    last_insert_rowid(), 3595, 1595, 1485, 2400,
    5, 1010.0, 'manufacturer-spec-2017'
);

COMMIT;

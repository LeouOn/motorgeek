-- =====================================================================
-- Add 5 more EV anchors + populate ZP for 2 existing EVs (2026-06-18)
-- Source: user-provided zeperfs.com battle page (image_83ba23.png)
--         match13126-13107-10632-9426-12158-11613.htm (BYD Tang battle)
--
-- Cars added:
--   214. Volvo EX90 Twin Motor Performance AWD 517 PS (2023-2025) ZP=152
--   215. Nio ES8 544 PS (2021-)                          ZP=169
--   216. Nio EL6 Long Range 490 PS (2024-)               ZP=165
--
-- Cars UPDATED (already in DB, just adding ZP):
--   car_id 75  (Hongqi E-HS9):    ZP=152
--   car_id 123 (BMW iX xDrive50): ZP=169
--   car_id 205 (BYD Tang):        already has ZP=153 from prior batch
-- =====================================================================

BEGIN TRANSACTION;

-- ---------------------------------------------------------------------
-- 1. CARS (3 new)
-- ---------------------------------------------------------------------
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, character, family, variant, image_paths, created_at)
VALUES
(214, 'Volvo', 'EX90', 'Twin Motor Performance', 2023, 2025, 'modern', 'suv', 'Sweden', 'ev', 'EX90', 'Twin Motor Performance AWD 517 PS', '[]', datetime('now')),
(215, 'Nio', 'ES8', 'first gen', 2021, NULL, 'modern', 'suv', 'China', 'ev', 'ES8', '544 PS', '[]', datetime('now')),
(216, 'Nio', 'EL6', 'Long Range', 2024, NULL, 'modern', 'suv', 'China', 'ev', 'EL6', 'Long Range 490 PS', '[]', datetime('now'));

-- ---------------------------------------------------------------------
-- 2. POWERTRAIN_ICE (hp/weight placeholder rows for EVs, existing convention)
-- Weights derived from kg/PS in battle page (EU max)
-- ---------------------------------------------------------------------
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, horsepower_rpm, torque_nm, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES
-- Volvo EX90 Perf: 517 PS @ 5500, 910 Nm, 5.6 kg/PS → 2895 kg
(251, 214, 'zeperfs-battle13126-user-2026-06-18', 'dual motor electric', 0.0, 0, 'electric', 510.0, 5500, 910, 'single-speed automatic', 1, 'AWD', 2895.0, 0),
-- Nio ES8: 544 PS @ 5300, 725 Nm, 4.7 kg/PS → 2557 kg
(252, 215, 'zeperfs-battle13126-user-2026-06-18', 'dual motor electric', 0.0, 0, 'electric', 536.0, 5300, 725, 'single-speed automatic', 1, 'AWD', 2557.0, 0),
-- Nio EL6 LR: 490 PS @ 5000, 700 Nm, 5.1 kg/PS → 2499 kg
(253, 216, 'zeperfs-battle13126-user-2026-06-18', 'dual motor electric', 0.0, 0, 'electric', 483.0, 5000, 700, 'single-speed automatic', 1, 'AWD', 2499.0, 0);

-- ---------------------------------------------------------------------
-- 3. POWERTRAIN_EV (rich EV data)
-- ---------------------------------------------------------------------
INSERT INTO powertrain_ev (id, car_id, source, motor_layout, motor_count, horsepower_bhp, torque_nm, extra)
VALUES
(6, 214, 'zeperfs-battle13126-user-2026-06-18', 'dual motor AWD', 2, 510.0, 910.0, '{"powers_rpm": 5500}'),
(7, 215, 'zeperfs-battle13126-user-2026-06-18', 'dual motor AWD', 2, 536.0, 725.0, '{"powers_rpm": 5300}'),
(8, 216, 'zeperfs-battle13126-user-2026-06-18', 'dual motor AWD', 2, 483.0, 700.0, '{"powers_rpm": 5000}');

-- ---------------------------------------------------------------------
-- 4. PERFORMANCE (use measured midpoints from battle page)
-- ---------------------------------------------------------------------
INSERT INTO performance (id, car_id, source, accel_0_60, accel_0_100, top_speed_mph, extra)
VALUES
-- EX90: 0-100 range 4.5-5.9s, midpoint 5.2s
(214, 214, 'zeperfs-battle-midpoint', 5.2, 5.2, 112.0, '{"0_100_range": "4.5-5.9s", "0_50_range": "2.0-2.5s"}'),
-- ES8: 0-100 = 4.7s (single value)
(215, 215, 'zeperfs-battle-midpoint', 4.7, 4.7, 124.0, '{"0_100_range": "4.7-4.7s", "0_160_range": "9.9-9.9s"}'),
-- EL6 LR: 0-100 range 4.1-4.5s, midpoint 4.3s
(216, 216, 'zeperfs-battle-midpoint', 4.3, 4.3, 124.0, '{"0_100_range": "4.1-4.5s", "0_160_range": "10.2-10.6s"}');

-- ---------------------------------------------------------------------
-- 5. ZEPERFS_INDICES — new cars + populate ZP for existing iX and E-HS9
-- ---------------------------------------------------------------------
INSERT INTO zeperfs_indices (id, car_id, zeperfs_index, source, recorded_date)
VALUES
(25, 214, 152.0, 'zeperfs-battle13126-user-2026-06-18', datetime('now')),
(26, 215, 169.0, 'zeperfs-battle13126-user-2026-06-18', datetime('now')),
(27, 216, 165.0, 'zeperfs-battle13126-user-2026-06-18', datetime('now'));

-- Add ZP for existing cars (BMW iX xDrive 50 = id 123, Hongqi E-HS9 = id 75)
-- These didn't have ZP values before
INSERT INTO zeperfs_indices (id, car_id, zeperfs_index, source, recorded_date)
VALUES
(28, 75, 152.0, 'zeperfs-battle13126-user-2026-06-18', datetime('now')),
(29, 123, 169.0, 'zeperfs-battle13126-user-2026-06-18', datetime('now'));

COMMIT;

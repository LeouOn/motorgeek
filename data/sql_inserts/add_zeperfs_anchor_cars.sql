-- =====================================================================
-- Add 6 new ZPerfs anchor cars (2026-06-18)
-- Source: user-provided zeperfs.com fiches (2026-06-18 session)
-- Purpose: extend ZP calibration set from 9 -> 15 anchors
--
-- Cars added:
--   202. McLaren 765LT Coupe 765 PS (2020-2023)        ZP=221  ICE
--   203. Lucid Air Dream Edition 1126 PS (2022-2023)   ZP=217  EV
--   204. Fisker Ocean Extreme 564 PS (2023-2024)       ZP=168  EV
--   205. BYD Tang 517 PS (2024)                        ZP=153  EV
--   206. Alpine A290 GTS 218 PS (2024)                 ZP=126  EV
--   207. Nissan Leaf 109 PS (2010-2017)                ZP=82   EV
--
-- Notes:
--   * DIN curb weight used (matches zeperfs convention)
--   * 0-100 km/h measured (not claimed) values used for accel
--   * Top speeds in km/h converted to mph for top_speed_mph column
--   * EVs get powertrain_ice row (for formula compat) + powertrain_ev row (rich data)
-- =====================================================================

BEGIN TRANSACTION;

-- ---------------------------------------------------------------------
-- 1. CARS table
-- ---------------------------------------------------------------------
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, character, family, variant, image_paths, created_at)
VALUES
(202, 'McLaren', '765LT', 'Coupé', 2020, 2023, 'modern', 'coupe', 'UK', 'hyper', '765LT', '765 PS', '[]', datetime('now')),
(203, 'Lucid', 'Air', 'Dream Edition', 2022, 2023, 'modern', 'sedan', 'USA', 'ev', 'Air', 'Dream Edition 1126 PS', '[]', datetime('now')),
(204, 'Fisker', 'Ocean', 'Extreme', 2023, 2024, 'modern', 'suv', 'USA', 'ev', 'Ocean', 'Extreme 564 PS', '[]', datetime('now')),
(205, 'BYD', 'Tang', 'first gen', 2024, NULL, 'modern', 'suv', 'China', 'ev', 'Tang', '517 PS', '[]', datetime('now')),
(206, 'Alpine', 'A290', 'GTS', 2024, NULL, 'modern', 'hatchback', 'France', 'ev', 'A290', 'GTS 218 PS', '[]', datetime('now')),
(207, 'Nissan', 'Leaf', 'ZE0', 2010, 2017, 'modern', 'hatchback', 'Japan', 'ev', 'Leaf', '109 PS 24 kWh', '[]', datetime('now'));

-- ---------------------------------------------------------------------
-- 2. POWERTRAIN_ICE table (hp+weight for ALL cars including EVs;
--    EVs get displacement_cc=0 placeholder per existing DB convention)
-- ---------------------------------------------------------------------
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm, redline_rpm, compression_ratio, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES
-- 765LT: 4.0L bi-turbo V8, 765 PS / 755 bhp @ 7500, 800 Nm @ 5500
(239, 202, 'zeperfs-fiche8512', '4.0L V8 twin-turbo M840T', 3994.0, 8, 'twin-turbo', 755.0, 7500, 800, 5500, 8200, NULL, 'direct injection', '7-speed automatic DCT', 7, 'RWD', 1339.0, 0),
-- Lucid Air Dream: dual motor EV, 1126 PS / 1111 bhp, 1390 Nm
(240, 203, 'zeperfs-fiche10323', 'dual motor electric', 0.0, 0, 'electric', 1111.0, 14500, 1390, 5700, 14500, NULL, 'n/a (EV)', 'single-speed automatic', 1, 'AWD', 2360.0, 0),
-- Fisker Ocean Extreme: dual motor EV, 564 PS / 556 bhp, 737 Nm
(241, 204, 'zeperfs-fiche11249', 'dual motor electric', 0.0, 0, 'electric', 556.0, 15000, 737, 5000, 15000, NULL, 'n/a (EV)', 'single-speed automatic', 1, 'AWD', 2434.0, 0),
-- BYD Tang: dual motor EV, 517 PS / 510 bhp, 680 Nm
(242, 205, 'zeperfs-fiche13126', 'dual motor electric', 0.0, 0, 'electric', 510.0, 5500, 680, 5300, NULL, NULL, 'n/a (EV)', 'single-speed automatic', 1, 'AWD', 2555.0, 0),
-- Alpine A290 GTS: single motor FWD EV, 218 PS / 215 bhp, 300 Nm
(243, 206, 'zeperfs-fiche12898', 'single motor electric', 0.0, 0, 'electric', 215.0, 12500, 300, 5100, 12500, NULL, 'n/a (EV)', 'single-speed automatic', 1, 'FWD', 1479.0, 0),
-- Nissan Leaf ZE0: single motor FWD EV, 109 PS / 108 bhp, 280 Nm
(244, 207, 'zeperfs-fiche6938', 'single motor electric', 0.0, 0, 'electric', 108.0, 9800, 280, 2730, 10390, NULL, 'n/a (EV)', 'single-speed automatic', 1, 'FWD', 1525.0, 0);

-- ---------------------------------------------------------------------
-- 3. POWERTRAIN_EV table (rich EV-specific data)
--    NOTE: powertrain_ev table was previously empty; this is the first
--    proper population. Existing EVs (cars 10, 70-73, 115, 124, 125)
--    should be backfilled in a separate migration.
-- ---------------------------------------------------------------------
INSERT INTO powertrain_ev (id, car_id, source, battery_capacity_kwh, chemistry_type, charge_arch_volts, motor_layout, motor_count, horsepower_bhp, torque_nm, range_mi_epa, charge_rate_peak_kw, ground_clearance_mm, cargo_volume_liters, extra)
VALUES
(1, 203, 'zeperfs-fiche10323', 112.0, 'Li-ion NMC', 900.0, 'dual motor AWD', 2, 1111.0, 1390.0, NULL, 300.0, NULL, NULL, '{"motor_max_rpm": 14500, "powers_rpm_range": "5750-14500", "torque_rpm_range": "1-5700"}'),
(2, 204, 'zeperfs-fiche11249', 107.0, 'Li-ion', NULL, 'dual motor AWD', 2, 556.0, 737.0, NULL, 150.0, NULL, NULL, '{"motor_max_rpm": 15000, "powers_rpm_range": "5500-15000", "torque_rpm_range": "1-5000"}'),
(3, 205, 'zeperfs-fiche13126', 109.0, 'Li-ion LFP', NULL, 'dual motor AWD', 2, 510.0, 680.0, NULL, 110.0, NULL, NULL, '{"powers_rpm": 5500, "torque_rpm_range": "1-5300"}'),
(4, 206, 'zeperfs-fiche12898', 49.0, 'Li-ion NMC', 400.0, 'single motor FWD', 1, 215.0, 300.0, NULL, 100.0, NULL, NULL, '{"motor_max_rpm": 12500, "powers_rpm_range": "5250-12500", "torque_rpm_range": "1-5100"}'),
(5, 207, 'zeperfs-fiche6938', 24.0, 'Li-ion LMO', 360.0, 'single motor FWD', 1, 108.0, 280.0, 73.0, 50.0, NULL, NULL, '{"motor_max_rpm": 10390, "powers_rpm_range": "2730-9800", "torque_rpm_range": "1-2730"}');

-- ---------------------------------------------------------------------
-- 4. PERFORMANCE table (0-60 mph, top speed mph)
--    Using MEASURED 0-100 km/h, not claimed.
--    Converted: 0-100 km/h ≈ 0-60 mph (close enough for our purposes)
-- ---------------------------------------------------------------------
INSERT INTO performance (id, car_id, source, accel_0_60, accel_0_100, top_speed_mph, extra)
VALUES
-- 765LT: 0-100 = 3.0s measured (2.8 claimed), top 330 km/h = 205 mph
(202, 202, 'zeperfs-fiche8512-edmunds+topgear', 3.0, 3.0, 205.0, '{"0_200_kph_s": 6.6, "quarter_mile_s": 10.2, "quarter_mile_trap_kph": 233, "100_0_braking_m": 33.0, "lap_hockenheim_gp": "1:46.20", "lap_vir_grand_west_4.1mi": "2:38.40"}'),
-- Lucid Air Dream: 0-100 = 3.0s measured (2.5 claimed), top 280 km/h governed = 174 mph
(203, 203, 'zeperfs-fiche10323-caranddriver+hagerty', 3.0, 3.0, 174.0, '{"0_200_kph_s_measured": "n/a", "0_240_kph_s": 11.8, "quarter_mile_s": 10.1, "quarter_mile_trap_kph": 229, "120_0_braking_m": 56.4, "160_0_braking_m": 98.2}'),
-- Fisker Ocean Extreme: 0-100 = 4.4s measured (3.9 claimed), top 205 km/h governed = 127 mph
(204, 204, 'zeperfs-fiche11249-ams+teknikens', 4.4, 4.4, 127.0, '{"0_200_kph_s": 19.3, "quarter_mile_s": 12.9, "quarter_mile_trap_kph": 174, "100_0_braking_m": 36.7}'),
-- BYD Tang: 0-100 = 4.7s measured (4.9 claimed), top 190 km/h governed = 118 mph
(205, 205, 'zeperfs-fiche13126-autozeitung', 4.7, 4.7, 118.0, '{"0_50_kph_s": 2.1, "0_60_kph_s": 2.6, "0_160_kph_s": 11.6, "100_0_braking_m": 35.3, "lap_autozeitung": "1:47.10"}'),
-- Alpine A290 GTS: 0-100 = 6.4s, top 170 km/h governed = 106 mph
(206, 206, 'zeperfs-fiche12898-10sources', 6.4, 6.4, 106.0, '{"0_50_kph_s": 3.0, "0_60_kph_s": 3.3, "0_160_kph_s": 16.5, "quarter_mile_s": 14.6, "100_0_braking_m": 33.9, "lap_hockenheim_gp": "2:13.30", "lap_sachsenring": "1:44.67"}'),
-- Nissan Leaf ZE0: 0-100 = 11.1s measured (11.9 claimed), top 145 km/h = 90 mph
(207, 207, 'zeperfs-fiche6938-12sources', 11.1, 11.1, 90.0, '{"0_50_kph_s": 3.6, "0_60_kph_s": 4.8, "0_120_kph_s": 16.5, "quarter_mile_s": 17.8, "100_0_braking_m": 39.1, "lap_autozeitung": "1:55.80"}');

-- ---------------------------------------------------------------------
-- 5. ZEPERFS_INDICES table (the actual ZP/sportivity/perfs_prix)
--    These are USER-CONFIRMED values from zeperfs.com fiches.
--    Source tag distinguishes from LLM agentic-ingest guesses.
-- ---------------------------------------------------------------------
INSERT INTO zeperfs_indices (id, car_id, zeperfs_index, sportivity_index, perfs_prix_ratio, source, recorded_date)
VALUES
(13, 202, 221.0, 201.0, 71.0, 'zeperfs-fiche8512-user-2026-06-18', datetime('now')),
(14, 203, 217.0, 141.0, 91.0, 'zeperfs-fiche10323-user-2026-06-18', datetime('now')),
(15, 204, 168.0, 107.0, 123.0, 'zeperfs-fiche11249-user-2026-06-18', datetime('now')),
(16, 205, 153.0, 92.0, 112.0, 'zeperfs-fiche13126-user-2026-06-18', datetime('now')),
(17, 206, 126.0, 116.0, 117.0, 'zeperfs-fiche12898-user-2026-06-18', datetime('now')),
(18, 207, 82.0, 74.0, 75.0, 'zeperfs-fiche6938-user-2026-06-18', datetime('now'));

COMMIT;

-- =====================================================================
-- Verification queries (run after to confirm)
-- =====================================================================
-- SELECT c.id, c.year_start, c.make, c.model, c.generation,
--        pw.horsepower_bhp, pw.curb_weight_kg, p.accel_0_60,
--        z.zeperfs_index, z.sportivity_index, z.perfs_prix_ratio
-- FROM cars c
-- JOIN powertrain_ice pw ON pw.car_id=c.id
-- JOIN performance p ON p.car_id=c.id
-- JOIN zeperfs_indices z ON z.car_id=c.id
-- WHERE c.id BETWEEN 202 AND 207
-- ORDER BY z.zeperfs_index DESC;

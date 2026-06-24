-- =====================================================================
-- Add Skoda Citigo (deep-economy anchor for ZP < 80 gap)
-- Source: user-provided fiche8854 (2026-06-18, hit page limit)
-- =====================================================================
BEGIN TRANSACTION;

INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, character, family, variant, image_paths, created_at)
VALUES
(217, 'Skoda', 'Citigo', 'first gen', 2012, 2019, 'modern', 'hatchback', 'Czech Republic', 'eco', 'Citigo', '1.0 75 PS', '[]', datetime('now'));

INSERT INTO powertrain_ice (id, car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm, redline_rpm, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES
(254, 217, 'zeperfs-fiche8854-user-2026-06-18', '1.0L I3 NA transverse', 999.0, 3, 'naturally aspirated', 74.0, 6200, 95, 3600, 6400, 'multi-point injection', '5-speed manual', 5, 'FWD', 854.0, 0);

INSERT INTO performance (id, car_id, source, accel_0_60, accel_0_100, top_speed_mph, extra)
VALUES
-- 0-100 measured 14.2s, claimed 13.6s; top 171 km/h = 106 mph
(217, 217, 'zeperfs-fiche8854-5sources', 14.2, 14.2, 106.0, '{"0_100_claimed": 13.6, "0_100_measured_avg": 14.2, "quarter_mile_s": 19.2, "quarter_mile_trap_kph": 117, "100_0_braking_m": 38.1, "lap_autozeitung": "1:59.60"}');

INSERT INTO zeperfs_indices (id, car_id, zeperfs_index, sportivity_index, perfs_prix_ratio, source, recorded_date)
VALUES
(30, 217, 71.0, 85.0, 116.0, 'zeperfs-fiche8854-user-2026-06-18', datetime('now'));

COMMIT;

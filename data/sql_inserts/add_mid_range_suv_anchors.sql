-- =====================================================================
-- Add 6 mid-range diesel SUV anchors (2026-06-18, second batch)
-- Source: user-provided zeperfs.com battle page
--         https://zeperfs.com/en/match6676-5883-7625-5554-9673-11245.htm
-- Purpose: fill the ZP 80-110 anchor gap (was 0 anchors; now 6)
--
-- Cars added:
--   208. VW Touareg II V6 TDi 204 PS (2010-2014)         ZP=99
--   209. Volvo XC90 II D5 225 PS (2015-2016)             ZP=102
--   210. BMW X5 III (F15) 25d sDrive 218 PS (2013-2015)  ZP=103
--   211. BMW X5 III (F15) 25d xDrive 218 PS (2013-2015)  ZP=104
--   212. Mitsubishi Pajero 3.2 Di-D 200 PS (2007-2011)   ZP=84
--   213. Land Rover Discovery IV 3.0 TDV6 211 PS (2010-2016) ZP=88
-- =====================================================================

BEGIN TRANSACTION;

-- ---------------------------------------------------------------------
-- 1. CARS table
-- ---------------------------------------------------------------------
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, character, family, variant, image_paths, created_at)
VALUES
(208, 'Volkswagen', 'Touareg', 'Touareg 2 (7P)', 2010, 2014, 'modern', 'suv', 'Germany', 'eco', 'Touareg', '3.0 V6 TDI 204 PS', '[]', datetime('now')),
(209, 'Volvo', 'XC90', 'II', 2015, 2016, 'modern', 'suv', 'Sweden', 'eco', 'XC90', 'D5 225 PS', '[]', datetime('now')),
(210, 'BMW', 'X5', 'F15 (III)', 2013, 2015, 'modern', 'suv', 'Germany', 'eco', 'X5', '25d sDrive 218 PS', '[]', datetime('now')),
(211, 'BMW', 'X5', 'F15 (III)', 2013, 2015, 'modern', 'suv', 'Germany', 'eco', 'X5', '25d xDrive 218 PS', '[]', datetime('now')),
(212, 'Mitsubishi', 'Pajero', 'IV', 2007, 2011, 'modern', 'suv', 'Japan', 'eco', 'Pajero', '3.2 Di-D 200 PS Auto 5p', '[]', datetime('now')),
(213, 'Land Rover', 'Discovery', 'IV', 2010, 2016, 'modern', 'suv', 'UK', 'eco', 'Discovery', '3.0 TDV6 211 PS', '[]', datetime('now'));

-- ---------------------------------------------------------------------
-- 2. POWERTRAIN_ICE table
-- Weight computed from kg/PS ratio in battle page (EU max weight)
-- 0-100 measured range midpoints used for accel_0_60
-- Displacements: V6 TDi = 2967cc, D5 = 2400cc, 25d = 1995cc (B47),
--                3.2 Di-D = 3200cc, 3.0 TDV6 = 2993cc
-- ---------------------------------------------------------------------
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES
-- Touareg 204 PS @ 3200, 450 Nm @ 1250, 11.7 kg/PS → 2387 kg
(245, 208, 'zeperfs-battle6676-5883-7625-5554-9673-11245', '3.0L V6 TDi turbo diesel', 2967.0, 6, 'turbocharged-diesel', 201.0, 3200, 450, 1250, 'direct injection diesel', '8-speed automatic', 8, 'AWD', 2387.0, 0),
-- XC90 D5 225 PS @ 4250, 470 Nm @ 1750, 9.7 kg/PS → 2182 kg (D5 = Volvo D5 2.4L I5 diesel)
(246, 209, 'zeperfs-battle6676-5883-7625-5554-9673-11245', '2.4L I5 D5 turbo diesel', 2400.0, 5, 'turbocharged-diesel', 222.0, 4250, 470, 1750, 'direct injection diesel', '8-speed automatic', 8, 'AWD', 2182.0, 0),
-- X5 25d sDrive 218 PS @ 4400, 450 Nm @ 1500, 9.9 kg/PS → 2158 kg (B47 2.0L I4 diesel)
(247, 210, 'zeperfs-battle6676-5883-7625-5554-9673-11245', '2.0L I4 B47d diesel', 1995.0, 4, 'turbocharged-diesel', 215.0, 4400, 450, 1500, 'direct injection diesel', '8-speed automatic', 8, 'RWD', 2158.0, 0),
-- X5 25d xDrive 218 PS, 10.2 kg/PS → 2224 kg
(248, 211, 'zeperfs-battle6676-5883-7625-5554-9673-11245', '2.0L I4 B47d diesel', 1995.0, 4, 'turbocharged-diesel', 215.0, 4400, 450, 1500, 'direct injection diesel', '8-speed automatic', 8, 'AWD', 2224.0, 0),
-- Pajero 3.2 Di-D 200 PS @ 3800, 441 Nm @ 2000, 12.1 kg/PS → 2420 kg
(249, 212, 'zeperfs-battle6676-5883-7625-5554-9673-11245', '3.2L I4 Di-D diesel', 3200.0, 4, 'turbocharged-diesel', 197.0, 3800, 441, 2000, 'direct injection diesel', '5-speed automatic', 5, 'AWD', 2420.0, 0),
-- Discovery 3.0 TDV6 211 PS @ 4000, 520 Nm @ 1500, 12.8 kg/PS → 2701 kg
(250, 213, 'zeperfs-battle6676-5883-7625-5554-9673-11245', '3.0L V6 TDV6 diesel', 2993.0, 6, 'turbocharged-diesel', 208.0, 4000, 520, 1500, 'direct injection diesel', '8-speed automatic', 8, 'AWD', 2701.0, 0);

-- ---------------------------------------------------------------------
-- 3. PERFORMANCE table — use MEASURED midpoints from battle page
-- ---------------------------------------------------------------------
INSERT INTO performance (id, car_id, source, accel_0_60, accel_0_100, top_speed_mph, extra)
VALUES
-- Touareg: 0-100 range 8.2-9.8, midpoint 9.0; top 203-206 kph = 127 mph
(208, 208, 'zeperfs-battle-midpoint', 9.0, 9.0, 127.0, '{"0_100_range": "8.2-9.8s", "top_kph_range": "203-206", "quarter_mile_range": "16.2-17s", "80_120_min_s": 5.8, "80_180_min_s": 32.6}'),
-- XC90: 0-100 range 8.2-9.4, midpoint 8.8; top 212-215 kph = 133 mph
(209, 209, 'zeperfs-battle-midpoint', 8.8, 8.8, 133.0, '{"0_100_range": "8.2-9.4s", "top_kph_range": "212-215", "quarter_mile_range": "15.2-16.9s", "80_120_min_s": 5.9, "80_180_min_s": 25.1}'),
-- X5 sDrive: 0-100 range 8.0-9.1, midpoint 8.55; top 219-220 kph = 137 mph
(210, 210, 'zeperfs-battle-midpoint', 8.55, 8.55, 137.0, '{"0_100_range": "8.0-9.1s", "top_kph_range": "219-220", "quarter_mile_range": "15.8-16.6s", "80_120_min_s": 6.4, "80_180_min_s": 26.4}'),
-- X5 xDrive: 0-100 range 6.3-9.4 (wide variance), midpoint 7.85; top 210-215 kph = 132 mph
(211, 211, 'zeperfs-battle-midpoint', 7.85, 7.85, 132.0, '{"0_100_range": "6.3-9.4s", "top_kph_range": "210-215", "quarter_mile_range": "16.2-16.6s", "80_120_min_s": 6.0, "80_180_min_s": 28.3}'),
-- Pajero: 0-100 range 11.1-11.4, midpoint 11.25; top 179-189 kph = 114 mph
(212, 212, 'zeperfs-battle-midpoint', 11.25, 11.25, 114.0, '{"0_100_range": "11.1-11.4s", "top_kph_range": "179-189", "quarter_mile_range": "17.6-18.1s", "80_120_min_s": 8.9, "80_180_min_s": 58.3}'),
-- Discovery: 0-100 range 10.3-10.8, midpoint 10.55; top 180-191 kph = 118 mph
(213, 213, 'zeperfs-battle-midpoint', 10.55, 10.55, 118.0, '{"0_100_range": "10.3-10.8s", "top_kph_range": "180-191", "quarter_mile_range": "17.2-17.4s", "80_120_min_s": 8.2, "80_180_min_s": 52.1}');

-- ---------------------------------------------------------------------
-- 4. ZEPERFS_INDICES table
-- ---------------------------------------------------------------------
INSERT INTO zeperfs_indices (id, car_id, zeperfs_index, perfs_prix_ratio, source, recorded_date)
VALUES
(19, 208, 99.0, 73.0, 'zeperfs-battle6676-5883-user-2026-06-18', datetime('now')),
(20, 209, 102.0, 79.0, 'zeperfs-battle6676-5883-user-2026-06-18', datetime('now')),
(21, 210, 103.0, 79.0, 'zeperfs-battle6676-5883-user-2026-06-18', datetime('now')),
(22, 211, 104.0, 78.0, 'zeperfs-battle6676-5883-user-2026-06-18', datetime('now')),
(23, 212, 84.0, 65.0, 'zeperfs-battle6676-5883-user-2026-06-18', datetime('now')),
(24, 213, 88.0, 71.0, 'zeperfs-battle6676-5883-user-2026-06-18', datetime('now'));

COMMIT;

-- =====================================================================
-- Verification
-- =====================================================================
-- SELECT c.id, c.make, c.model, c.variant, pw.horsepower_bhp, pw.curb_weight_kg,
--        pw.displacement_cc, p.accel_0_60, z.zeperfs_index, z.perfs_prix_ratio
-- FROM cars c
-- JOIN powertrain_ice pw ON pw.car_id=c.id
-- JOIN performance p ON p.car_id=c.id
-- JOIN zeperfs_indices z ON z.car_id=c.id
-- WHERE c.id BETWEEN 208 AND 213
-- ORDER BY z.zeperfs_index DESC;

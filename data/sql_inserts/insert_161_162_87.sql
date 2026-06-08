-- ============================================================
-- Clean insert: W212 post-facelift (161), K5 GT (162), Camry V6 (87 backfill)
-- ============================================================

-- W212 post-facelift
INSERT INTO cars (id, make, model, generation, year_start, year_end, body_style, country, created_at)
VALUES (161, 'Mercedes-Benz', 'E-Class', 'W212 (post-facelift)', 2014, 2016, 'sedan', 'Germany', datetime('now'));

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm, fuel_system, transmission_type, gear_count, drivetrain, drag_coefficient, is_hybrid)
VALUES (161, 'sample', 'V6', 3498, 6, 'Naturally aspirated', 302, 6500, 370, 3500, 'Direct injection (DI)', '7G-Tronic (722.9)', 7, 'RWD/AWD', 0.25, 0);

INSERT INTO performance (car_id, source, accel_0_60, top_speed_mph, unlimited_top_speed_mph)
VALUES (161, 'sample', 6.0, 155.0, 149.0);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est, depreciation_5yr_pct)
VALUES (161, 'sample', 52500.0, 'USD', 21.0, 30.0, 1100.0, 55.0);

INSERT INTO dimensions (car_id, length_mm, width_mm, height_mm, wheelbase_mm, source)
VALUES (161, 4868, 1854, 1470, 2874, 'wikipedia');

INSERT INTO reliability (car_id, reliability_score, source, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, common_failures, known_issues, avg_repair_cost, recall_count, part_availability, diy_friendliness, score_notes)
VALUES (161, 71.9, 'sample', 78, 70, 74, 72, 65,
    '["Engine mount failure (60-100K)","722.9 conductor plate (80-130K, less frequent than pre-FL)","ESL steering lock failure","Blower motor failure","AIRMATIC air springs (if equipped)","Valve cover gasket leaks","Cam sensor oil leak (early 2014)"]',
    '["M276 60-degree V6 NO balance shaft","Shares architecture with Pentastar","DI carbon buildup potential","722.9 3rd-gen conductor plate improved","2015-2016 are sweet spot"]',
    1100, 5, 'Good', 'Moderate',
    'The return to form W212. M276 eliminates balance shaft. 4-chain timing. Updated 722.9. Post-FL COMAND improved. Owner consensus: bulletproof for maintained examples.');

-- K5 GT
INSERT INTO cars (id, make, model, generation, year_start, year_end, body_style, country, created_at)
VALUES (162, 'Kia', 'K5 GT', '1st gen', 2021, 2024, 'sedan', 'South Korea', datetime('now'));

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm, fuel_system, transmission_type, gear_count, drivetrain, is_hybrid)
VALUES (162, 'sample', 'I4', 2497, 4, 'Turbocharged', 290, 5800, 311, 1700, 'GDI + MPi dual injection', '8-speed wet DCT', 8, 'FWD', 0);

INSERT INTO performance (car_id, source, accel_0_60, top_speed_mph)
VALUES (162, 'sample', 5.7, 155.0);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est, depreciation_5yr_pct)
VALUES (162, 'sample', 31090.0, 'USD', 23.0, 32.0, 450.0, 50.0);

INSERT INTO dimensions (car_id, length_mm, width_mm, height_mm, wheelbase_mm, source)
VALUES (162, 4905, 1860, 1445, 2845, 'sample');

INSERT INTO reliability (car_id, reliability_score, source, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, common_failures, known_issues, avg_repair_cost, recall_count, part_availability, diy_friendliness, score_notes)
VALUES (162, 73.9, 'sample', 75, 68, 80, 78, 72,
    '["DCT oil pump solder joint (2021-early 2022 recall)","DCT software harsh shifts (TSB SA502/SA526)","Fuel injector failures (2021-22 batch)","Carbon buildup (DI 80K+)","Engine loudness (characteristic)","Turbo wastegate rattle potential"]',
    '["Smartstream Theta III clean-sheet, NOT patched Theta II","Dual injection mitigates carbon buildup","Only 5 years of data - too new for definitive judgment","DCT solder joint recall on early cars, post-Aug 2022 fixed","NA version has piston slap concerns, turbo better","FWD no LSD = torque steer at 290hp","10yr/100K warranty new, 5yr/60K used"]',
    450, 6, 'Good', 'Moderate',
    'Fun but unproven. Smartstream 2.5T improves on Theta II. Dual injection helps. DCT is weak link with early production issues. 2023+ sorted. Scores below Stinger 3.3T (80) mainly on less proven engine and DCT risk.');

-- Camry XV70 V6 backfill
UPDATE cars SET generation = 'XV70 (V6)', year_start = 2018, year_end = 2024, body_style = 'sedan', country = 'Japan' WHERE id = 87;

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm, fuel_system, transmission_type, gear_count, drivetrain, is_hybrid)
VALUES (87, 'sample', 'V6', 3456, 6, 'Naturally aspirated', 301, 6500, 267, 4700, 'D-4S dual injection (GDI + PFI)', 'AA81E 8-speed auto', 8, 'FWD', 0);

INSERT INTO performance (car_id, source, accel_0_60, top_speed_mph)
VALUES (87, 'sample', 5.8, 135.0);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est, depreciation_5yr_pct)
VALUES (87, 'sample', 34400.0, 'USD', 22.0, 32.0, 400.0, 50.0);

INSERT INTO dimensions (car_id, length_mm, width_mm, height_mm, wheelbase_mm, source)
VALUES (87, 4885, 1840, 1455, 2825, 'sample');

INSERT INTO reliability (car_id, reliability_score, source, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, common_failures, known_issues, avg_repair_cost, recall_count, part_availability, diy_friendliness, score_notes)
VALUES (87, 83.9, 'sample', 88, 68, 92, 90, 88,
    '["UA80/AA81E 8-speed harsh shifting (class action)","Timing cover oil leak (80-150K)","Coolant bypass pipe leak (60-120K)","Water pump failure (60-100K)","Ignition coil failure (30-50K GR pattern)","Carbon buildup intake valves (80K+)","Valve cover gasket leak (100K+)"]',
    '["2GR-FKS NOT refreshed FE - different heads block manifolds cams","D-4S dual injection: more power but more complexity","VVT-iW enables Atkinson cycle for economy","Integrated exhaust manifolds cast into heads","UA80 class action lawsuits harsh shifting and failure","2018-2020 worst for trans; 2021+ improved","Engine life 220-240K+ with maintenance","14 NHTSA recalls gen-wide (1 V6-specific: brake booster)"]',
    500, 14, 'Excellent', 'High',
    'The transmission lets down a bulletproof powertrain. 2GR-FKS with D-4S is more powerful but slightly less bulletproof than 2GR-FE. Engine 88 would be 90+ with port injection only. AA81E 8-speed is the genuine problem: class action lawsuits, $7K replacements. Chassis and electronics Toyota-perfect at 92/90. The smart play: 2021+ with improved trans calibration and 40K fluid changes.');

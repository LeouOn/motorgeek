-- ============================================================
-- MotorGeek DB: Fix ID collisions for child tables
-- Cars 151-155 already inserted. Now fix powertrain, cost, market, reliability
-- ============================================================

-- POWERTRAIN (max was 184, start at 185)
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm, compression_ratio, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (185, 151, 'sample', 'V6', 3342.0, 6, 'Twin-turbo', 365.0, 6000, 510.0, 4500, 10.0, 'GDI (direct injection only)', '8-speed automatic (Aisin)', 8, 'RWD / AWD optional', 2070.0, 0);

INSERT INTO powertrain_ice (id, car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm, compression_ratio, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (186, 152, 'sample', 'Inline-4', 2497.0, 4, 'Single turbo', 300.0, 5800, 422.0, 4000, 10.5, 'Dual injection (GDi + MPi)', '8-speed automatic', 8, 'RWD / AWD optional', 1673.0, 0);

INSERT INTO powertrain_ice (id, car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm, compression_ratio, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (187, 153, 'sample', 'Inline-4', 2497.0, 4, 'Single turbo', 300.0, 5800, 422.0, 4000, 10.5, 'Dual injection (GDi + MPi)', '8-speed automatic', 8, 'AWD (HTRAC)', 1890.0, 0);

INSERT INTO powertrain_ice (id, car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm, compression_ratio, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (188, 154, 'sample', 'V6', 3470.0, 6, 'Twin-turbo', 375.0, 5800, 530.0, 1300, 11.0, 'Dual injection (GDi + MPi + center)', '8-speed automatic', 8, 'AWD (HTRAC)', 2226.0, 0);

INSERT INTO powertrain_ice (id, car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm, compression_ratio, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, drag_coefficient, is_hybrid)
VALUES (189, 155, 'sample', 'V6', 2995.0, 6, 'Supercharged (Eaton TVS)', 333.0, 6500, 441.0, 4500, 10.8, 'FSI direct injection + MPI (facelift)', '8-speed Tiptronic (ZF 8HP)', 8, 'quattro AWD', 1835.0, 0.26, 0);

-- RELIABILITY (max was 167, start at 168)
-- New cars
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (168, 151, 'sample', 80.0,
  '{"Carbon buildup (GDI only)": 3, "Turbo oil line leaks": 2, "Coolant leaks (60-80k)": 2, "Adaptive suspension strut actuators": 2}',
  750.0, 1, 'Good (Genesis dealer + Hyundai parts shared)', 'Moderate',
  '{"Lambda II 3.3T": "Proven V6 architecture, twin turbo added. GDI-only = carbon buildup at 40-60k, walnut blasting recommended. 3yr/36k complimentary maintenance.", "Aisin 8-speed": "Generally reliable. Harsh 2-3 shift when cold. Fluid change at 60k.", "10yr/100k powertrain warranty": "Major reliability differentiator vs German competitors."}');

INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (169, 152, 'sample', 78.0,
  '{"ITM (thermal management module)": 2, "Fuel injector sensitivity": 2, "PCV system (turbo blow-by)": 2}',
  600.0, 0, 'Good (Hyundai/Genesis shared parts)', 'Moderate',
  '{"Smartstream G2.5T (G4KR)": "Dual injection (GDi + MPi) significantly reduces carbon buildup vs GDI-only. MPi handles low/mid loads, GDi handles high loads. Expected 200k+ miles.", "ITM module": "Early 2020-2022 Smartstream had some ITM issues. Complex electronic thermostat."}');

INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (170, 153, 'sample', 76.0,
  '{"Rear differential whine": 3, "ITM module": 2, "Rim clear coat peeling": 1, "Seat heater failure": 1}',
  650.0, 1, 'Good (Hyundai/Genesis shared parts)', 'Moderate',
  '{"GV70 platform": "KBB 4.3/5 owner reliability. Rear diff whine at 3.8-6k miles is known TSB issue.", "Dual injection": "Same G4KR engine as G70 2.5T — dual injection prevents most carbon buildup."}');

INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (171, 154, 'sample', 75.0,
  '{"Rear differential pinion nut (TSB)": 3, "Instrument panel software (recall)": 2, "Audio amplifier failure": 1, "ITM cooling module": 2}',
  700.0, 2, 'Good (Genesis dealer network)', 'Low',
  '{"Smartstream G3.5T (G6DS)": "Dual injection (GDi + MPi + center) prevents carbon buildup. 11.0:1 CR. Towing 6000 lbs. Consumer Reports above average.", "GV80 issues": "TSB for rear diff pinion nut (pre-2024). Display recall 2023-2024. KBB 4/5.", "Weight": "4907 lbs = more tire/brake/suspension wear."}');

INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (172, 155, 'sample', 75.0,
  '{"PCV valve failure (under supercharger)": 3, "Water pump/thermostat housing": 3, "Timing chain tensioner (5-10%)": 3, "Supercharger wear": 2, "Carbon buildup (intake valves)": 2}',
  1100.0, 2, 'Good (Audi specialist + aftermarket)', 'Low',
  '{"EA837 (CAJA/CREC)": "One of Audis most reliable modern engines. Risk score 4.0/10 per Autoscore. Facelift 2015+ improved with dual injection + decoupling clutch.", "Timing chain": "At BACK of engine = engine removal for service. Startup rattle >3 seconds warrants inspection. Many 200k+ without chain service.", "ZF 8HP": "One of the best automatics. No mechatronic issues unlike DL382. Fluid change at 40-60k."}');

-- Backfill existing Genesis/Audi/Kia
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (173, 29, 'sample', 85.0,
  '{"Minor electrical gremlins": 1, "Suspension bushings (high mileage)": 2}',
  500.0, 0, 'Good (Hyundai/Genesis shared)', 'High',
  '{"Lambda 3.8 MPI": "Port-injected NA V6 = NO carbon buildup. Dead simple, dead reliable. The unexciting but bulletproof choice. 10yr/100k warranty.", "Aisin 8-speed": "Proven unit. No known issues."}');

INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (174, 38, 'sample', 80.0,
  '{"Carbon buildup (GDI only)": 3, "Turbo oil line leaks": 2, "Differential whine": 2}',
  700.0, 1, 'Good (Hyundai/Genesis shared)', 'Moderate',
  '{"Lambda II 3.3T": "Same G6DP as G80 3.3T Sport. GDI-only = carbon buildup risk. Proven V6.", "G70 platform": "Shared with Kia Stinger GT = larger aftermarket. 10yr/100k warranty."}');

INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (175, 54, 'sample', 76.0,
  '{"Rear differential whine": 3, "ITM thermal management": 2, "Audio amplifier": 1}',
  650.0, 1, 'Good (Hyundai/Genesis shared)', 'Moderate',
  '{"Smartstream G3.5T (G6DS)": "Same as GV80 3.5T. Dual injection. C/D 40k test: no major issues. 20 mpg avg.", "GV70": "KBB 4.3/5 owner reliability."}');

INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (176, 32, 'sample', 75.0,
  '{"Oil consumption": 3, "DL382+ mechatronic (S-tronic)": 3, "Water pump/thermostat": 2, "Timing chain tensioner wear": 2, "Early rocker arm (2018-early 2019)": 2}',
  1200.0, 1, 'Good (Audi specialist + aftermarket)', 'Low',
  '{"EA839 (DLZA)": "Shared with Porsche Macan S, VW Touareg. Generally reliable but oil consumption most reported. NA spec deletes port injector = carbon buildup risk.", "DL382+ S-tronic": "Mechatronic is weak point. Harsh low-speed shifts. P0718, P179F codes. $2-3K mechatronic.", "Cd 0.23": "Best drag coefficient of any combustion Audi."}');

INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (177, 33, 'sample', 80.0,
  '{"Carbon buildup (GDI only)": 3, "Turbo oil line leaks": 2, "Brake rotor warpage": 2}',
  700.0, 0, 'Good (Hyundai/Kia shared parts)', 'Moderate',
  '{"Lambda II 3.3T": "Same as G70 3.3T. GDI-only = carbon buildup at 40-60k. Proven V6.", "Stinger GT": "Brembo brakes standard. Larger aftermarket than G70. 10yr/100k warranty.", "Discontinued 2024": "Values may hold as only Kia liftback GT."}');

INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (178, 8, 'sample', 72.0,
  '{"V8 fuel consumption": 3, "Air suspension (if equipped)": 3, "Electrical gremlins": 2}',
  900.0, 0, 'Limited (Genesis dealer only)', 'Low',
  '{"Tau 5.0 V8": "NA port-injected = no carbon buildup. Simple and proven. 16/24 mpg is thirsty. Rare engine.", "G90 1st gen": "Originally Hyundai Equus. Massive depreciation = great used luxury value."}');

INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (179, 44, 'sample', 80.0,
  '{"Carbon buildup (GDI only)": 3, "Air suspension (if equipped)": 3, "Turbo oil line leaks": 2}',
  800.0, 0, 'Good (Genesis dealer + Hyundai parts)', 'Low',
  '{"Lambda II 3.3T": "Same as G80 3.3T. GDI-only = walnut blasting at 60k.", "G90 flagship": "Massive depreciation from $68K+ MSRP. Used $15-25K gets full-size luxury with 10yr/100k warranty. Best used luxury value per dollar."}');

INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (180, 45, 'sample', 78.0,
  '{"ITM thermal management": 2, "Air suspension complexity": 3, "Rear diff (GV80-shared)": 2}',
  800.0, 1, 'Good (Genesis dealer)', 'Low',
  '{"Smartstream G3.5T": "Same as GV80 3.5T. Dual injection. 409 hp is highest Genesis output.", "G90 2nd gen": "Newer platform, less long-term data. Air suspension adds complexity. 10yr/100k warranty."}');

-- COST TO OWN (max was 188, start at 189)
INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est, depreciation_5yr_pct)
VALUES (189, 151, 'sample', 55250.0, 'USD', 17.0, 25.0, 700.0, 55.0);

INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est, depreciation_5yr_pct)
VALUES (190, 152, 'sample', 39000.0, 'USD', 21.0, 29.0, 550.0, 50.0);

INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est, depreciation_5yr_pct)
VALUES (191, 153, 'sample', 41000.0, 'USD', 22.0, 28.0, 600.0, 52.0);

INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est, depreciation_5yr_pct)
VALUES (192, 154, 'sample', 57295.0, 'USD', 18.0, 23.0, 700.0, 55.0);

INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est, depreciation_5yr_pct)
VALUES (193, 155, 'sample', 56000.0, 'USD', 20.0, 29.0, 1100.0, 60.0);

-- Backfill maintenance for existing entries
UPDATE cost_to_own SET annual_maintenance_est = 550.0 WHERE car_id = 29 AND (annual_maintenance_est IS NULL OR annual_maintenance_est = 0);
UPDATE cost_to_own SET annual_maintenance_est = 700.0 WHERE car_id = 38 AND (annual_maintenance_est IS NULL OR annual_maintenance_est = 0);
UPDATE cost_to_own SET annual_maintenance_est = 650.0, fuel_econ_city_mpg = COALESCE(fuel_econ_city_mpg, 19.0), fuel_econ_hwy_mpg = COALESCE(fuel_econ_hwy_mpg, 25.0) WHERE car_id = 54 AND (annual_maintenance_est IS NULL OR fuel_econ_city_mpg IS NULL OR fuel_econ_city_mpg = 0);
UPDATE cost_to_own SET annual_maintenance_est = 700.0 WHERE car_id = 33 AND (annual_maintenance_est IS NULL OR annual_maintenance_est = 0);

-- MARKET HISTORY (max was 155, start at 156)
INSERT INTO market_history (id, car_id, date_recorded, price_low, price_high, volume_sold_est, market_trend_indicator, source_site, currency)
VALUES (156, 151, '2025-01-01', 15000.0, 25000.0, 8000, 'depreciating', 'sample', 'USD');

INSERT INTO market_history (id, car_id, date_recorded, price_low, price_high, volume_sold_est, market_trend_indicator, source_site, currency)
VALUES (157, 152, '2025-01-01', 25000.0, 35000.0, 5000, 'stable', 'sample', 'USD');

INSERT INTO market_history (id, car_id, date_recorded, price_low, price_high, volume_sold_est, market_trend_indicator, source_site, currency)
VALUES (158, 153, '2025-01-01', 28000.0, 40000.0, 12000, 'stable', 'sample', 'USD');

INSERT INTO market_history (id, car_id, date_recorded, price_low, price_high, volume_sold_est, market_trend_indicator, source_site, currency)
VALUES (159, 154, '2025-01-01', 30000.0, 45000.0, 10000, 'depreciating', 'sample', 'USD');

INSERT INTO market_history (id, car_id, date_recorded, price_low, price_high, volume_sold_est, market_trend_indicator, source_site, currency)
VALUES (160, 155, '2025-01-01', 10000.0, 20000.0, 15000, 'depreciating', 'sample', 'USD');

-- POWERTRAIN BACKFILLS for existing entries
UPDATE powertrain_ice SET displacement_cc = 3342.0, cylinders = 6, aspiration = 'Twin-turbo', transmission_type = '8-speed automatic', gear_count = 8 WHERE car_id = 33 AND (displacement_cc IS NULL OR displacement_cc = 0);
UPDATE powertrain_ice SET cylinders = 6, aspiration = 'Single twin-scroll turbo (hot-vee)', transmission_type = '7-speed S tronic (DL382+)', gear_count = 7, drivetrain = 'quattro AWD', compression_ratio = 11.2, fuel_system = 'FSI direct injection', drag_coefficient = 0.23 WHERE car_id = 32;

-- ============================================================
-- DONE
-- ============================================================

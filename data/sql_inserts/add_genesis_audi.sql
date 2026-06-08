-- ============================================================
-- MotorGeek DB: Add Genesis + Audi cars + backfill existing
-- Date: 2026-06-08
-- Cars added: ids 151-155 (new), backfill ids 8,29,32,33,38,44,45,54
-- ============================================================

-- ============================================================
-- PART 1: NEW CARS (ids 151-155)
-- ============================================================

-- 151: Genesis G80 3.3T Sport (1st gen DH, 2017-2020)
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, character, family, variant, created_at)
VALUES (151, 'Genesis', 'G80', '1st gen (DH)', 2017, 2020, '2017-2020', 'sedan', 'South Korea', 'sleeper', 'Lambda II', 'G80 3.3T Sport', datetime('now'));

-- 152: Genesis G70 2.5T (1st gen facelift, 2022+)
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, character, family, variant, created_at)
VALUES (152, 'Genesis', 'G70', '1st gen (facelift)', 2022, NULL, '2022+', 'sedan', 'South Korea', 'sharp', 'Smartstream/Theta III', 'G70 2.5T', datetime('now'));

-- 153: Genesis GV70 2.5T (1st gen, 2022+)
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, character, family, variant, created_at)
VALUES (153, 'Genesis', 'GV70', '1st gen', 2022, NULL, '2022+', 'SUV', 'South Korea', 'versatile', 'Smartstream/Theta III', 'GV70 2.5T', datetime('now'));

-- 154: Genesis GV80 3.5T (1st gen, 2020+)
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, character, family, variant, created_at)
VALUES (154, 'Genesis', 'GV80', '1st gen', 2020, NULL, '2020+', 'SUV', 'South Korea', 'premium', 'Smartstream/Lambda III', 'GV80 3.5T', datetime('now'));

-- 155: Audi A6 3.0T (C7, 2012-2018)
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, character, family, variant, created_at)
VALUES (155, 'Audi', 'A6', 'C7', 2012, 2018, '2012-2018', 'sedan', 'Germany', 'refined', 'EA837', '3.0T quattro', datetime('now'));

-- ============================================================
-- PART 2: POWERTRAIN FOR NEW CARS
-- ============================================================

-- 151: G80 3.3T Sport — Lambda II 3.3T G6DP twin-turbo V6
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm, compression_ratio, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (151, 151, 'sample', 'V6', 3342.0, 6, 'Twin-turbo', 365.0, 6000, 510.0, 4500, 10.0, 'GDI (direct injection only)', '8-speed automatic (Aisin)', 8, 'RWD / AWD optional', 2070.0, 0);

-- 152: G70 2.5T — Smartstream G4KR turbo I4, dual injection
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm, compression_ratio, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (152, 152, 'sample', 'Inline-4', 2497.0, 4, 'Single turbo', 300.0, 5800, 422.0, 4000, 10.5, 'Dual injection (GDi + MPi)', '8-speed automatic', 8, 'RWD / AWD optional', 1673.0, 0);

-- 153: GV70 2.5T — Smartstream G4KR turbo I4, dual injection
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm, compression_ratio, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (153, 153, 'sample', 'Inline-4', 2497.0, 4, 'Single turbo', 300.0, 5800, 422.0, 4000, 10.5, 'Dual injection (GDi + MPi)', '8-speed automatic', 8, 'AWD (HTRAC)', 1890.0, 0);

-- 154: GV80 3.5T — Smartstream G6DS twin-turbo V6, dual injection
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm, compression_ratio, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (154, 154, 'sample', 'V6', 3470.0, 6, 'Twin-turbo', 375.0, 5800, 530.0, 1300, 11.0, 'Dual injection (GDi + MPi + center)', '8-speed automatic', 8, 'AWD (HTRAC)', 2226.0, 0);

-- 155: Audi A6 3.0T C7 — EA837 supercharged V6
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm, compression_ratio, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, drag_coefficient, is_hybrid)
VALUES (155, 155, 'sample', 'V6', 2995.0, 6, 'Supercharged (Eaton TVS)', 333.0, 6500, 441.0, 4500, 10.8, 'FSI direct injection + MPI (facelift)', '8-speed Tiptronic (ZF 8HP)', 8, 'quattro AWD', 1835.0, 0.26, 0);

-- ============================================================
-- PART 3: RELIABILITY FOR NEW CARS
-- ============================================================

-- 151: G80 3.3T — Lambda II T-GDi, GDI-only, carbon buildup risk, otherwise solid
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (151, 151, 'sample', 80.0,
  '{"Carbon buildup (GDI only)": 3, "Turbo oil line leaks": 2, "Coolant leaks (60-80k)": 2, "Adaptive suspension strut actuators": 2}',
  750.0, 1, 'Good (Genesis dealer + Hyundai parts shared)', 'Moderate',
  '{"Lambda II 3.3T": "Proven V6 architecture, twin turbo added. GDI-only = carbon buildup at 40-60k, walnut blasting recommended. 3yr/36k complimentary maintenance included.", "Aisin 8-speed": "Generally reliable. Harsh 2-3 shift when cold. Fluid change at 60k recommended.", "10yr/100k powertrain warranty": "Major reliability differentiator vs German competitors. Warranty transferable to second owner."}');

-- 152: G70 2.5T — Smartstream dual-injection, newer but promising
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (152, 152, 'sample', 78.0,
  '{"ITM (thermal management module)": 2, "Fuel injector sensitivity": 2, "PCV system (turbo blow-by)": 2}',
  600.0, 0, 'Good (Hyundai/Genesis shared parts)', 'Moderate',
  '{"Smartstream G2.5T (G4KR)": "Dual injection (GDi + MPi) significantly reduces carbon buildup vs GDI-only engines. MPis handles low/mid loads, GDi handles high loads. Expected 200k+ miles with proper maintenance.", "ITM module": "Early 2020-2022 Smartstream engines had some ITM reliability issues. Complex electronic thermostat unit."}');

-- 153: GV70 2.5T — same engine as G70 2.5T, SUV weight penalty
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (153, 153, 'sample', 76.0,
  '{"Rear differential whine": 3, "ITM module": 2, "Rim clear coat peeling": 1, "Seat heater failure": 1}',
  650.0, 1, 'Good (Hyundai/Genesis shared parts)', 'Moderate',
  '{"GV70 platform": "KBB 4.3/5 owner reliability. Rear differential whine at 3.8-6k miles is a known TSB issue. C/D 40k long-term test (3.5T) had no major issues.", "Dual injection benefit": "Same G4KR engine as G70 2.5T — dual injection prevents most carbon buildup."}');

-- 154: GV80 3.5T — Smartstream Lambda III twin-turbo, dual injection
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (154, 154, 'sample', 75.0,
  '{"Rear differential pinion nut (TSB)": 3, "Instrument panel software (recall)": 2, "Audio amplifier failure": 1, "ITM cooling module": 2}',
  700.0, 2, 'Good (Genesis dealer network)', 'Low',
  '{"Smartstream G3.5T (G6DS)": "Dual injection (GDi + MPi + center) is the gold standard for preventing carbon buildup. 11.0:1 CR is aggressive. Towing capacity 6000 lbs. Consumer Reports above average.", "GV80-specific": "TSB for rear diff pinion nut torque (pre-2024). Display software recall for 2023-2024. KBB 4/5 owner rating.", "Weight penalty": "4907 lbs curb weight = more tire/brake/suspension wear than G80 sedan."}');

-- 155: Audi A6 3.0T C7 — EA837 supercharged, proven track record
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (155, 155, 'sample', 75.0,
  '{"PCV valve failure (under supercharger)": 3, "Water pump/thermostat housing": 3, "Timing chain tensioner (5-10%)": 3, "Supercharger wear": 2, "Carbon buildup (intake valves)": 2}',
  1100.0, 2, 'Good (Audi specialist + aftermarket)', 'Low',
  '{"EA837 (CAJA/CREC)": "Considered one of Audis most reliable modern engines. Risk score 4.0/10 per Autoscore (lower=better). Facelift (2015+) improved with dual injection + decoupling clutch.", "Timing chain": "At BACK of engine = engine removal for service. Startup rattle >3 seconds warrants inspection. Many owners report 200k+ without chain service.", "ZF 8HP": "One of the best automatics. No mechatronic issues unlike DL382 S-tronic. Fluid change at 40-60k recommended.", "Supercharger": "Eaton TVS is robust. Oil change often neglected. PCV replacement requires supercharger R&R ($400-800)."}');

-- ============================================================
-- PART 4: COST TO OWN FOR NEW CARS
-- ============================================================

-- 151: G80 3.3T Sport — RWD figures
INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est, depreciation_5yr_pct)
VALUES (151, 151, 'sample', 55250.0, 'USD', 17.0, 25.0, 700.0, 55.0);

-- 152: G70 2.5T — RWD figures
INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est, depreciation_5yr_pct)
VALUES (152, 152, 'sample', 39000.0, 'USD', 21.0, 29.0, 550.0, 50.0);

-- 153: GV70 2.5T — AWD figures (19" wheels)
INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est, depreciation_5yr_pct)
VALUES (153, 153, 'sample', 41000.0, 'USD', 22.0, 28.0, 600.0, 52.0);

-- 154: GV80 3.5T — AWD figures
INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est, depreciation_5yr_pct)
VALUES (154, 154, 'sample', 57295.0, 'USD', 18.0, 23.0, 700.0, 55.0);

-- 155: Audi A6 3.0T C7 — facelift figures (20/29)
INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est, depreciation_5yr_pct)
VALUES (155, 155, 'sample', 56000.0, 'USD', 20.0, 29.0, 1100.0, 60.0);

-- ============================================================
-- PART 5: MARKET HISTORY FOR NEW CARS
-- ============================================================

INSERT INTO market_history (id, car_id, date_recorded, price_low, price_high, volume_sold_est, market_trend_indicator, source_site, currency)
VALUES (151, 151, '2025-01-01', 15000.0, 25000.0, 8000, 'depreciating', 'sample', 'USD');

INSERT INTO market_history (id, car_id, date_recorded, price_low, price_high, volume_sold_est, market_trend_indicator, source_site, currency)
VALUES (152, 152, '2025-01-01', 25000.0, 35000.0, 5000, 'stable', 'sample', 'USD');

INSERT INTO market_history (id, car_id, date_recorded, price_low, price_high, volume_sold_est, market_trend_indicator, source_site, currency)
VALUES (153, 153, '2025-01-01', 28000.0, 40000.0, 12000, 'stable', 'sample', 'USD');

INSERT INTO market_history (id, car_id, date_recorded, price_low, price_high, volume_sold_est, market_trend_indicator, source_site, currency)
VALUES (154, 154, '2025-01-01', 30000.0, 45000.0, 10000, 'depreciating', 'sample', 'USD');

INSERT INTO market_history (id, car_id, date_recorded, price_low, price_high, volume_sold_est, market_trend_indicator, source_site, currency)
VALUES (155, 155, '2025-01-01', 10000.0, 20000.0, 15000, 'depreciating', 'sample', 'USD');

-- ============================================================
-- PART 6: BACKFILL EXISTING GENESIS/AUDI/KIA RELIABILITY
-- ============================================================

-- id 29: G80 3.8L (1st gen DH) — NA port-injected, unexciting but dead reliable
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (160, 29, 'sample', 85.0,
  '{"Minor electrical gremlins": 1, "Suspension bushings (high mileage)": 2}',
  500.0, 0, 'Good (Hyundai/Genesis shared)', 'High',
  '{"Lambda 3.8 MPI": "Port-injected NA V6 = NO carbon buildup issues. Dead simple, dead reliable. This is the unexciting but bulletproof choice. 10yr/100k warranty.", "Aisin 8-speed": "Proven unit, shared with many vehicles. No known issues."}');

-- id 38: G70 3.3T (1st gen) — Lambda II twin-turbo V6
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (161, 38, 'sample', 80.0,
  '{"Carbon buildup (GDI only)": 3, "Turbo oil line leaks": 2, "Differential whine": 2}',
  700.0, 1, 'Good (Hyundai/Genesis shared)', 'Moderate',
  '{"Lambda II 3.3T": "Same G6DP engine as G80 3.3T Sport. GDI-only = carbon buildup risk. Proven V6 architecture.", "G70 platform": "Sharing with Kia Stinger GT = larger aftermarket. 10yr/100k warranty."}');

-- id 54: GV70 3.5T — Smartstream Lambda III twin-turbo
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (162, 54, 'sample', 76.0,
  '{"Rear differential whine": 3, "ITM thermal management": 2, "Audio amplifier": 1}',
  650.0, 1, 'Good (Hyundai/Genesis shared)', 'Moderate',
  '{"Smartstream G3.5T (G6DS)": "Same engine as GV80 3.5T. Dual injection (GDi + MPi + center). C/D 40k long-term test: no major mechanical issues. Averaged 20 mpg.", "GV70 platform": "KBB 4.3/5 owner reliability."}');

-- id 32: Audi A6 C8 55 TFSI — EA839 turbo V6
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (163, 32, 'sample', 75.0,
  '{"Oil consumption": 3, "DL382+ mechatronic (S-tronic)": 3, "Water pump/thermostat": 2, "Timing chain tensioner wear": 2, "Early rocker arm issue (2018-early 2019)": 2}',
  1200.0, 1, 'Good (Audi specialist + aftermarket)', 'Low',
  '{"EA839 (DLZA)": "Shared with Porsche Macan S, VW Touareg, Lamborghini Urus (tuned). Generally reliable but oil consumption most reported issue. NA spec deletes port fuel injector = carbon buildup risk remains.", "DL382+ S-tronic": "Mechatronic unit is the weak point. Harsh low-speed shifts inherent. Fault codes P0718, P179F common. $2-3K mechatronic replacement.", "Cd 0.23": "Best drag coefficient of any combustion Audi."}');

-- id 33: Kia Stinger 3.3T — Lambda II twin-turbo V6 (same as G70 3.3T)
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (164, 33, 'sample', 80.0,
  '{"Carbon buildup (GDI only)": 3, "Turbo oil line leaks": 2, "Brake rotor warpage": 2}',
  700.0, 0, 'Good (Hyundai/Kia shared parts)', 'Moderate',
  '{"Lambda II 3.3T (G6DP)": "Same engine as Genesis G70 3.3T and G80 3.3T Sport. GDI-only = carbon buildup at 40-60k. Twin-turbo V6 proven across multiple Hyundai/Genesis/Kia applications.", "Stinger GT": "Brembo brakes standard. Larger aftermarket than G70 due to longer production run and broader appeal. 10yr/100k powertrain warranty.", "Discontinued 2024": "Kia ended Stinger production. Values may hold or appreciate as the only Kia liftback GT."}');

-- id 8: Genesis G90 5.0 V8 — Tau V8, old-school luxury
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (165, 8, 'sample', 72.0,
  '{"V8 fuel consumption": 3, "Air suspension (if equipped)": 3, "Electrical gremlins": 2}',
  900.0, 0, 'Limited (Genesis dealer only)', 'Low',
  '{"Tau 5.0 V8": "NA port-injected V8 = no carbon buildup. Simple and proven. But 16/24 mpg is thirsty. Rare engine, parts availability more limited than Lambda V6s.", "G90 1st gen (pre-2017)": "Originally Hyundai Equus. Massive depreciation = great used luxury value if you can stomach fuel costs."}');

-- id 44: Genesis G90 1st gen (3.3T) — Lambda II twin-turbo
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (166, 44, 'sample', 80.0,
  '{"Carbon buildup (GDI only)": 3, "Air suspension (if equipped)": 3, "Turbo oil line leaks": 2}',
  800.0, 0, 'Good (Genesis dealer + Hyundai parts)', 'Low',
  '{"Lambda II 3.3T (G6DP)": "Same proven twin-turbo V6 as G80 3.3T and G70 3.3T. GDI-only = walnut blasting at 60k.", "G90 flagship": "Massive depreciation from $68K+ MSRP. Used $15-25K gets you a full-size luxury sedan with 10yr/100k warranty. Best used luxury value per dollar."}');

-- id 45: Genesis G90 2nd gen (3.5T) — Smartstream Lambda III
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (167, 45, 'sample', 78.0,
  '{"ITM thermal management": 2, "Air suspension complexity": 3, "Rear diff (GV80-shared issue)": 2}',
  800.0, 1, 'Good (Genesis dealer)', 'Low',
  '{"Smartstream G3.5T (G6DS)": "Same engine as GV80/GV70 3.5T. Dual injection. 409 hp is the highest Genesis output.", "G90 2nd gen": "Newer platform, less long-term data. Air suspension adds complexity. 10yr/100k warranty still applies."}');

-- ============================================================
-- PART 7: BACKFILL MISSING COST_TO_OWNS
-- ============================================================

-- id 29: G80 3.8L — already has cost_to_own, update fuel econ and maintenance
UPDATE cost_to_own SET annual_maintenance_est = 550.0 WHERE car_id = 29 AND annual_maintenance_est IS NULL;

-- id 38: G70 3.3T — fill missing maintenance
UPDATE cost_to_own SET annual_maintenance_est = 700.0 WHERE car_id = 38 AND annual_maintenance_est IS NULL;

-- id 54: GV70 3.5T — fill missing maintenance
UPDATE cost_to_own SET annual_maintenance_est = 650.0, fuel_econ_city_mpg = 19.0, fuel_econ_hwy_mpg = 25.0 WHERE car_id = 54 AND (annual_maintenance_est IS NULL OR fuel_econ_city_mpg IS NULL);

-- id 33: Kia Stinger — fill missing powertrain + cost data
-- Powertrain backfill
UPDATE powertrain_ice SET displacement_cc = 3342.0, cylinders = 6, aspiration = 'Twin-turbo', transmission_type = '8-speed automatic', gear_count = 8 WHERE car_id = 33 AND displacement_cc IS NULL;

-- Cost backfill for Stinger
UPDATE cost_to_own SET annual_maintenance_est = 700.0 WHERE car_id = 33 AND annual_maintenance_est IS NULL;

-- ============================================================
-- PART 8: FILL AUDI A6 C8 (id 32) MISSING POWERTRAIN FIELDS
-- ============================================================

UPDATE powertrain_ice SET cylinders = 6, aspiration = 'Single twin-scroll turbo (hot-vee)', transmission_type = '7-speed S tronic (DL382+)', gear_count = 7, drivetrain = 'quattro AWD', compression_ratio = 11.2, fuel_system = 'FSI direct injection', drag_coefficient = 0.23 WHERE car_id = 32;

-- ============================================================
-- DONE
-- ============================================================

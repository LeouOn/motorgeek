-- ============================================================
-- MotorGeek DB: Genesis + Audi child table inserts + backfill
-- Date: 2026-06-08
-- Cars: 151-155 (already in cars table) + backfill ids 8,29,32,33,38,44,45,54
-- IDs start above existing maxes: powertrain 185+, cost 189+, market 156+, reliability 168+
-- ============================================================

-- ============================================================
-- PART 1: POWERTRAIN (start id 185)
-- ============================================================

INSERT INTO powertrain_ice (id, car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm, compression_ratio, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES
(185, 151, 'sample', 'V6 (60-degree)', 3342.0, 6, 'Twin-turbocharged', 365.0, 6000, 510.0, 1300, 10.0, 'GDI (200 bar, direct injection only)', '8-speed automatic (Aisin)', 8, 'RWD standard / HTRAC AWD optional', 2070.0, 0),
(186, 152, 'sample', 'Inline-4 (longitudinal)', 2497.0, 4, 'Single turbo (BorgWarner)', 300.0, 5800, 422.0, 1650, 10.5, 'Dual injection (GDi + MPi)', '8-speed automatic', 8, 'RWD standard / AWD optional', 1673.0, 0),
(187, 153, 'sample', 'Inline-4 (longitudinal)', 2497.0, 4, 'Single turbo (BorgWarner)', 300.0, 5800, 422.0, 1650, 10.5, 'Dual injection (GDi + MPi)', '8-speed automatic (shift-by-wire)', 8, 'AWD only (HTRAC)', 1890.0, 0),
(188, 154, 'sample', 'V6 (90-degree)', 3470.0, 6, 'Twin-turbocharged', 375.0, 5800, 530.0, 1300, 11.0, 'Triple injection (GDi + MPi + center)', '8-speed automatic (shift-by-wire)', 8, 'AWD standard (HTRAC)', 2226.0, 0),
(189, 155, 'sample', 'V6 (90-degree)', 2995.0, 6, 'Supercharged (Eaton TVS Roots)', 333.0, 5500, 441.0, 2900, 10.8, 'FSI direct injection + MPI (facelift EVO)', '8-speed Tiptronic (ZF 8HP)', 8, 'quattro AWD (permanent)', 1835.0, 0);

-- ============================================================
-- PART 2: RELIABILITY (start id 168)
-- ============================================================

INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES
-- 151: G80 3.3T Sport - 78
(168, 151, 'sample', 78.0, '{"Turbo oil line leaks (TSB 2018-2019)": 3, "Carbon buildup intake valves (GDI)": 3, "Coolant leaks 60-80k": 2, "Adaptive suspension actuators 80k+": 2}',
 650.0, 1, 'Good (Genesis dealer + aftermarket)', 'Moderate',
 '{"Lambda II 3.3T": "Proven twin-turbo V6. GDI-only = carbon buildup at 60k+, walnut blasting recommended. 10yr/100K powertrain warranty."}'),

-- 152: G70 2.5T - 80
(169, 152, 'sample', 80.0, '{"ITM thermal module (early 2022)": 2, "Fuel injector sensitivity": 1, "PCV system blow-by": 1}',
 550.0, 0, 'Good (Genesis + Hyundai parts bin)', 'Moderate',
 '{"Smartstream G2.5T (G4KR)": "Dual injection (GDi + MPi) eliminates carbon buildup risk. Expected 200k+ miles."}'),

-- 153: GV70 2.5T - 80
(170, 153, 'sample', 80.0, '{"Rear differential whine (TSB)": 3, "ITM thermal module": 2, "Seat heater failure": 1}',
 550.0, 0, 'Good (Genesis + Hyundai parts)', 'Low (SUV, AWD)',
 '{"Smartstream G2.5T (G4KR)": "Same dual-injection engine as G70 2.5T. KBB 4.3/5 owner reliability."}'),

-- 154: GV80 3.5T - 78
(171, 154, 'sample', 78.0, '{"Rear differential pinion nut (TSB)": 3, "IP display software (recall)": 2, "Audio amplifier failure": 2}',
 650.0, 1, 'Good (Genesis dealer)', 'Low (large SUV)',
 '{"Smartstream G3.5T (G6DS)": "Triple injection V6. Consumer Reports above average. Towing 6000 lbs."}'),

-- 155: A6 3.0T C7 - 78
(172, 155, 'sample', 78.0, '{"PCV valve under supercharger (~62k)": 3, "Water pump/thermostat housing": 3, "Timing chain tensioner (high mi)": 2, "Supercharger wear": 2, "Carbon buildup (walnut blast 80-100k)": 2}',
 900.0, 2, 'Good (Audi specialist + VW Group)', 'Moderate',
 '{"EA837 3.0T": "One of Audi most reliable modern engines. ZF 8HP bulletproof. Timing chain at back of engine."}'),

-- 29: G80 3.8L - 82 (the unexciting but solid pick)
(173, 29, 'sample', 82.0, '{"Minor electrical gremlins": 1, "Aisin 8-speed normal wear": 1}',
 500.0, 0, 'Excellent (Hyundai parts bin)', 'High',
 '{"Lambda MPI 3.8L V6": "Port-injected, NA. No turbo, no GDI, no carbon buildup. Dead reliable since Hyundai Genesis era. This is the smart boring choice."}'),

-- 38: G70 3.3T - 78
(174, 38, 'sample', 78.0, '{"Carbon buildup (GDI)": 3, "Turbo oil line (early units)": 2, "Brembo brake pad wear": 2}',
 700.0, 0, 'Good (Genesis + Hyundai parts)', 'Moderate',
 '{"Lambda II 3.3T": "Same G6DP as G80 3.3T. GDI-only = carbon buildup at 60k+."}'),

-- 54: GV70 3.5T - 78
(175, 54, 'sample', 78.0, '{"Rear differential whine (TSB)": 3, "ITM thermal module": 2, "Audio issues": 1}',
 600.0, 0, 'Good (Genesis dealer)', 'Low (SUV, AWD)',
 '{"Smartstream G3.5T (G6DS)": "Triple injection. C/D 40k long-term test: no major issues."}'),

-- 8: G90 5.0 V8 - 72
(176, 8, 'sample', 72.0, '{"Tau V8 oil consumption": 2, "Air suspension issues": 3, "Electrical gremlins": 2}',
 900.0, 1, 'Moderate (V8 parts less common)', 'Low (flagship)',
 '{"Tau 5.0L V8": "Older design, more complex than Lambda V6s. Air suspension adds cost."}'),

-- 44: G90 1st gen 3.3T - 76
(177, 44, 'sample', 76.0, '{"Carbon buildup (GDI)": 3, "Air suspension": 3, "Electrical features": 2}',
 850.0, 0, 'Moderate (Genesis dealer)', 'Low (flagship)',
 '{"Lambda II 3.3T in G90": "Proven engine but heavier car. More luxury = more to break."}'),

-- 45: G90 2nd gen 3.5T - 77
(178, 45, 'sample', 77.0, '{"Too new for pattern failures": 1, "Air suspension": 2}',
 800.0, 0, 'Moderate (Genesis dealer)', 'Low (flagship)',
 '{"Smartstream G3.5T (G6DS)": "Dual/triple injection. Too new for long-term pattern data."}'),

-- 32: A6 C8 55 TFSI - 76
(179, 32, 'sample', 76.0, '{"DL382+ mechatronic failure": 3, "EA839 oil consumption": 2, "Water pump/thermostat": 2, "Timing chain tensioner": 2}',
 1100.0, 1, 'Good (Audi specialist + VW Group)', 'Low',
 '{"EA839 (DLZA)": "Good engine but NA spec GDI-only. DL382+ mechatronic is THE weak point vs C7 ZF 8HP."}'),

-- 33: Kia Stinger 3.3T - 78
(180, 33, 'sample', 78.0, '{"Carbon buildup (GDI)": 3, "Brembo brake wear": 2, "Rear diff whine": 2}',
 700.0, 0, 'Good (Kia + Hyundai parts bin)', 'Moderate',
 '{"Lambda II 3.3T": "Same G6DP as Genesis 3.3T variants. Discontinued 2024 — may hold value."}');

-- ============================================================
-- PART 3: COST_TO_OWN (start id 189)
-- ============================================================

INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est, depreciation_5yr_pct)
VALUES
(189, 151, 'sample', 55250.0, 'USD', 17.0, 25.0, 766.0, 55.0),
(190, 152, 'sample', 39000.0, 'USD', 21.0, 29.0, 550.0, 50.0),
(191, 153, 'sample', 41000.0, 'USD', 22.0, 28.0, 550.0, 50.0),
(192, 154, 'sample', 57295.0, 'USD', 18.0, 23.0, 650.0, 55.0),
(193, 155, 'sample', 57000.0, 'USD', 20.0, 29.0, 1000.0, 60.0);

-- ============================================================
-- PART 4: MARKET_HISTORY (start id 156)
-- ============================================================

INSERT INTO market_history (id, car_id, date_recorded, price_low, price_high, volume_sold_est, market_trend_indicator, source_site, currency)
VALUES
(156, 151, '2024-01-01', 18000.0, 32000.0, 12000, 'stable', 'sample', 'USD'),
(157, 152, '2024-01-01', 25000.0, 38000.0, 8000, 'appreciating', 'sample', 'USD'),
(158, 153, '2024-01-01', 28000.0, 42000.0, 15000, 'appreciating', 'sample', 'USD'),
(159, 154, '2024-01-01', 30000.0, 55000.0, 10000, 'stable', 'sample', 'USD'),
(160, 155, '2024-01-01', 12000.0, 25000.0, 20000, 'depreciating', 'sample', 'USD');

-- ============================================================
-- PART 5: BACKFILL EXISTING POWERTRAIN GAPS
-- ============================================================

-- A6 C8 (id 32): fill missing powertrain details
UPDATE powertrain_ice SET
  cylinders = 6,
  aspiration = 'Single twin-scroll turbo (hot-vee)',
  transmission_type = '7-speed S tronic (DL382+)',
  gear_count = 7,
  drivetrain = 'quattro AWD (permanent)',
  curb_weight_kg = 1935.0,
  compression_ratio = 11.2,
  fuel_system = 'FSI direct injection'
WHERE car_id = 32;

-- Kia Stinger (id 33): fill missing powertrain details
UPDATE powertrain_ice SET
  displacement_cc = 3342.0,
  cylinders = 6,
  aspiration = 'Twin-turbocharged',
  transmission_type = '8-speed automatic (in-house)',
  gear_count = 8,
  drivetrain = 'RWD standard / AWD optional'
WHERE car_id = 33;

-- ============================================================
-- PART 6: BACKFILL EXISTING COST GAPS
-- ============================================================

-- G80 3.8L (id 29): add maintenance
UPDATE cost_to_own SET annual_maintenance_est = 500.0 WHERE car_id = 29 AND annual_maintenance_est IS NULL;

-- A6 C8 (id 32): fill missing cost data
UPDATE cost_to_own SET fuel_econ_city_mpg = 22.0, fuel_econ_hwy_mpg = 29.0, annual_maintenance_est = 1100.0, msrp_original = 58900.0 WHERE car_id = 32;

-- Kia Stinger (id 33): fill missing cost data
UPDATE cost_to_own SET fuel_econ_city_mpg = 17.0, fuel_econ_hwy_mpg = 25.0, annual_maintenance_est = 700.0 WHERE car_id = 33;

-- ============================================================
-- DONE
-- ============================================================

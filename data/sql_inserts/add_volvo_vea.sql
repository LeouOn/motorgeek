-- ============================================================
-- MotorGeek DB: Add Geely-era Volvo VEA/Drive-E vehicles
-- Date: 2026-06-08
-- 5 new cars (ids 156-160): S60 T5, S60 T6, XC60 T5, XC60 T6, S90 T6
-- NOTE: No NA 2.0L exists in VEA family. Tiers are T5 (turbo), T6 (turbo+SC)
-- ============================================================

-- ============================================================
-- PART 1: CARS (start id 156)
-- ============================================================

INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, description, created_at, character, family, variant)
VALUES (156, 'Volvo', 'S60', '3rd gen (SPA)', 2019, NULL, '2019+', 'sedan', 'Sweden',
  'The SPA-platform S60 T5 is the base-tier Geely-era Volvo sedan. Powered by the VEA B4204T26 2.0L turbo I4 producing 250 hp, mated to the Aisin TG-81SC 8-speed automatic. FWD standard, EPA 23/34 mpg. This is the "smart" Volvo — all the safety and Scandinavian design without the supercharger complexity. The T5 is the reliability sweet spot of the VEA family: simpler, fewer failure modes, nearly as fast as the T6 in daily driving. 2019+ SPA models are generally sorted after early VEA oil consumption issues were resolved.',
  datetime('now'), 'understated', 'VEA/Drive-E', 'S60 T5');

INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, description, created_at, character, family, variant)
VALUES (157, 'Volvo', 'S60', '3rd gen (SPA)', 2019, 2021, '2019-2021', 'sedan', 'Sweden',
  'The S60 T6 adds an Eaton Roots-type supercharger to the VEA 2.0L turbo I4, producing 316 hp and 295 lb-ft. The supercharger operates via electromagnetic clutch from idle to ~3,500 rpm, then hands off to the BorgWarner turbo. AWD standard. EPA 21/32 mpg. The T6 is the "enthusiast" Volvo — instant low-end torque from the supercharger, linear power delivery, genuinely quick. But the supercharger clutch is a known failure point ($2-3.5K), and oil consumption issues are more common on T6s. 2019+ models are improved over early 2015-2016 VEA engines.',
  datetime('now'), 'sleeper', 'VEA/Drive-E', 'S60 T6 AWD');

INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, description, created_at, character, family, variant)
VALUES (158, 'Volvo', 'XC60', '2nd gen (SPA)', 2018, NULL, '2018+', 'SUV', 'Sweden',
  'The SPA-platform XC60 T5 is the volume-seller Volvo SUV. Same VEA B4204T23 2.0L turbo I4 (250 hp) as the S60 T5, but in a compact luxury SUV. FWD standard, AWD optional. EPA 22/29 mpg (FWD). The XC60 is consistently one of the highest-rated luxury compact SUVs — Scandinavian design, class-leading safety, and the T5 is the reliability pick over the T6. Curb weight ~3,950 lbs. The 2018+ SPA platform is well-sorted.',
  datetime('now'), 'practical', 'VEA/Drive-E', 'XC60 T5');

INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, description, created_at, character, family, variant)
VALUES (159, 'Volvo', 'XC60', '2nd gen (SPA)', 2018, 2020, '2018-2020', 'SUV', 'Sweden',
  'The XC60 T6 pairs the VEA turbo+supercharged B4204T27 (316 hp) with AWD. Same twincharged architecture as the S60 T6, but in a heavier SUV package (~4,045 lbs). EPA 20/27 mpg. The T6 is the "fast" XC60 — genuinely quick for a compact SUV, with instant supercharger response. Same trade-off: more power, more complexity, supercharger clutch risk. Discontinued after 2020 when Volvo shifted to B6 mild-hybrid variants.',
  datetime('now'), 'performance-suv', 'VEA/Drive-E', 'XC60 T6 AWD');

INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, description, created_at, character, family, variant)
VALUES (160, 'Volvo', 'S90', '1st gen (SPA)', 2017, 2021, '2017-2021', 'sedan', 'Sweden',
  'The S90 T6 is Volvos flagship sedan. Same B4204T27 turbo+supercharged 2.0L (316 hp) as the S60/XC60 T6, but in a larger, heavier package (4,819 lbs). AWD standard, EPA 21/31 mpg. The S90 is the "executive" Volvo — gorgeous Scandinavian interior, Pilot Assist semi-autonomous driving, and genuinely premium feel. The 2017-2019 models had more early VEA issues; 2020+ is the sweet spot. MSRP started at $50,550 but massive depreciation means used examples are $20-35K.',
  datetime('now'), 'executive', 'VEA/Drive-E', 'S90 T6 AWD');

-- ============================================================
-- PART 2: POWERTRAIN (start id 190)
-- ============================================================

INSERT INTO powertrain_ice (id, car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm, compression_ratio, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES
(190, 156, 'sample', 'Inline-4', 1969.0, 4, 'Single turbo (BorgWarner)', 250.0, 5500, 350.0, 4500, 10.8, 'Direct injection', 'Aisin TG-81SC 8-speed (Geartronic)', 8, 'FWD', 1659.0, 0),
(191, 157, 'sample', 'Inline-4', 1969.0, 4, 'Turbo + Eaton Roots supercharger', 316.0, 5700, 400.0, 5400, 10.3, 'Direct injection', 'Aisin TG-81SC 8-speed (Geartronic)', 8, 'AWD', 1772.0, 0),
(192, 158, 'sample', 'Inline-4', 1969.0, 4, 'Single turbo (BorgWarner)', 250.0, 5500, 350.0, 4800, 10.3, 'Direct injection', 'Aisin TG-81SC 8-speed (Geartronic)', 8, 'FWD / AWD optional', 1790.0, 0),
(193, 159, 'sample', 'Inline-4', 1969.0, 4, 'Turbo + Eaton Roots supercharger', 316.0, 5700, 400.0, 5400, 10.3, 'Direct injection', 'Aisin TG-81SC 8-speed (Geartronic)', 8, 'AWD', 1835.0, 0),
(194, 160, 'sample', 'Inline-4', 1969.0, 4, 'Turbo + Eaton Roots supercharger', 316.0, 5700, 400.0, 5400, 10.3, 'Direct injection', 'Aisin TG-81SC 8-speed (Geartronic)', 8, 'AWD', 2186.0, 0);

-- ============================================================
-- PART 3: RELIABILITY (start id 181)
-- ============================================================

INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES
-- S60 T5: 78 — simpler T5, SPA 2019+ sorted, no SC complexity
(181, 156, 'sample', 78.0,
  '{"Oil consumption (monitor)": 2, "Sensus infotainment glitches": 2, "Premature front brake wear": 1}',
  650.0, 1, 'Good (Volvo dealer + aftermarket)', 'Moderate',
  '{"VEA T5 B4204T26": "Turbo-only = simpler than T6. No supercharger clutch issues. 2019+ SPA engines resolved early piston ring and oil consumption problems. T5 is the reliability sweet spot per Reddit/SwedeSpeed consensus.", "Aisin TG-81SC": "Reliable 8-speed. Aisin also supplies Toyota. Volvo says sealed for life; Aisin recommends fluid change at 40-50k."}'),

-- S60 T6: 72 — SC clutch risk, oil consumption, more complex
(182, 157, 'sample', 72.0,
  '{"Supercharger electromagnetic clutch failure": 3, "Oil consumption (piston rings)": 3, "Turbo failure (if oil starved)": 2, "Sensus glitches": 2}',
  850.0, 2, 'Good (Volvo dealer)', 'Low (SC complexity)',
  '{"VEA T6 B4204T27": "Twincharged = more failure points. SC electromagnetic clutch is the #1 issue: severe hesitation from stop, often no CEL. $2-3.5K repair. Oil consumption worse than T5, can starve turbo if unmonitored.", "Avoid 2015-2016": "Early VEA had piston ring defect, balancer shaft issues, timing chain tensioner problems. 2019+ SPA models improved but SC clutch remains a risk on all T6 years."}'),

-- XC60 T5: 78 — same T5 engine, SUV weight penalty
(183, 158, 'sample', 78.0,
  '{"Oil consumption (monitor)": 2, "Sensus infotainment glitches": 2, "Body seal leakage": 1, "AC compressor issues": 1}',
  700.0, 1, 'Good (Volvo dealer + aftermarket)', 'Moderate',
  '{"VEA T5 B4204T23": "Same reliable turbo-only engine as S60 T5. XC60 is one of the highest-rated luxury compact SUVs. T5 is the smart pick over T6."}'),

-- XC60 T6: 72 — same T6 issues in heavier SUV
(184, 159, 'sample', 72.0,
  '{"Supercharger electromagnetic clutch failure": 3, "Oil consumption": 3, "Turbo failure (if oil starved)": 2, "Premature brake wear": 2}',
  850.0, 1, 'Good (Volvo dealer)', 'Low (SUV + SC complexity)',
  '{"VEA T6 in XC60": "Same B4204T27 as S60 T6 but heavier vehicle. More stress on drivetrain. SC clutch is the headline issue. T6 discontinued after 2020 (replaced by B6 mild hybrid)."}'),

-- S90 T6: 70 — flagship weight, earlier SPA years, SC complexity
(185, 160, 'sample', 70.0,
  '{"Supercharger clutch failure": 3, "Oil consumption": 3, "Sensus infotainment": 2, "Air suspension (if equipped)": 3}',
  950.0, 2, 'Good (Volvo dealer)', 'Low (flagship complexity)',
  '{"VEA T6 in S90": "Same engine as XC60/S60 T6 but in 4,819 lb flagship. More stress. 2017-2019 models had more early VEA issues. 2020+ is the sweet spot if buying used.", "S90 depreciation": "Massive depreciation from $50K+ MSRP. Used 2018-2020 examples $20-35K = genuinely premium sedan for mainstream money. The SC risk is the trade-off."}');

-- ============================================================
-- PART 4: COST_TO_OWN (start id 194)
-- ============================================================

INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est, depreciation_5yr_pct)
VALUES
(194, 156, 'sample', 36050.0, 'USD', 23.0, 34.0, 650.0, 55.0),
(195, 157, 'sample', 40550.0, 'USD', 21.0, 32.0, 800.0, 55.0),
(196, 158, 'sample', 40150.0, 'USD', 22.0, 29.0, 700.0, 52.0),
(197, 159, 'sample', 45950.0, 'USD', 20.0, 27.0, 850.0, 55.0),
(198, 160, 'sample', 50550.0, 'USD', 21.0, 31.0, 900.0, 58.0);

-- ============================================================
-- PART 5: MARKET_HISTORY (start id 161)
-- ============================================================

INSERT INTO market_history (id, car_id, date_recorded, price_low, price_high, volume_sold_est, market_trend_indicator, source_site, currency)
VALUES
(161, 156, '2024-01-01', 20000.0, 35000.0, 10000, 'depreciating', 'sample', 'USD'),
(162, 157, '2024-01-01', 18000.0, 32000.0, 5000, 'depreciating', 'sample', 'USD'),
(163, 158, '2024-01-01', 22000.0, 38000.0, 25000, 'stable', 'sample', 'USD'),
(164, 159, '2024-01-01', 20000.0, 35000.0, 8000, 'depreciating', 'sample', 'USD'),
(165, 160, '2024-01-01', 15000.0, 35000.0, 6000, 'depreciating', 'sample', 'USD');

-- ============================================================
-- DONE
-- ============================================================

-- ============================================================
-- K5 GT (new car id 162) + Camry XV70 V6 (backfill id 87)
-- ============================================================

-- ============================================================
-- PART 1: Kia K5 GT (2021+, 2.5T, 290hp, 8-speed wet DCT)
-- ============================================================

INSERT INTO cars (id, make, model, generation, year_start, year_end, body_style, country, created_at) VALUES (
    162, 'Kia', 'K5 GT', '1st gen', 2021, 2024, 'sedan', 'South Korea', datetime('now')
);

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm, fuel_system, transmission_type, gear_count, drivetrain, is_hybrid) VALUES (
    162, 'sample',
    'I4', 2497, 4, 'Turbocharged',
    290, 5800, 311, 1700,
    'GDI + MPi dual injection',
    '8-speed wet DCT', 8, 'FWD',
    0
);

INSERT INTO performance (car_id, source, accel_0_60, top_speed_mph) VALUES (
    162, 'sample', 5.7, 155.0
);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est, depreciation_5yr_pct) VALUES (
    162, 'sample', 31090.0, 'USD', 23.0, 32.0, 450.0, 50.0
);

INSERT INTO dimensions (car_id, length_mm, width_mm, height_mm, wheelbase_mm, source) VALUES (
    162, 4905, 1860, 1445, 2845, 'sample'
);

-- Dimensional reliability for K5 GT:
-- Engine 75: Smartstream Theta III 2.5T - significant improvement over Theta II, dual injection,
--   no major failures yet, but only 5 years of data, turbo adds risk
-- Transmission 68: 8-speed wet DCT - early solder joint recall, software gremlins,
--   inherent DCT traffic limitations. 2023+ improved
-- Chassis 80: Modern platform, well-built, but FWD-only with no LSD = torque steer at 290hp
-- Electronics 78: Modern tech, some TSBs (CarPlay, multi-function camera)
-- Ease of repair 72: 10yr/100k warranty helps, but turbo+DCT = expensive OOW,
--   independent shops less familiar with Smartstream
-- Aggregate: 75*0.25 + 68*0.25 + 80*0.15 + 78*0.15 + 72*0.20 = 18.75 + 17.0 + 12.0 + 11.7 + 14.4 = 73.85
INSERT INTO reliability (car_id, reliability_score, source, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, common_failures, known_issues, avg_repair_cost, recall_count, part_availability, diy_friendliness, score_notes) VALUES (
    162, 73.9, 'sample',
    75, 68, 80, 78, 72,
    '["DCT oil pump solder joint failure (2021-early 2022, recall)","DCT software logic - harsh shifts, clunky (TSB SA502/SA526)","Fuel injector failures (2021-2022 batch)","Carbon buildup on intake valves (DI component, 80K+)","Engine characteristically loud (not a failure)","Turbo wastegate rattle (potential, 60K+)"]',
    '["Smartstream G2.5T (G4KP) is Theta III - clean-sheet redesign, NOT patched Theta II","Dual injection (GDi + MPi) mitigates carbon buildup like Toyota D-4S","Too new for definitive high-mileage data - oldest cars only 60K miles","Early 2021 DCT had solder joint failure on electric oil pump circuit board - NHTSA recall, post-Aug 2022 builds fixed","NA version of same engine family has piston slap/oil blowby concerns - turbo version appears better-sorted","DCT replacement cost ~$20K if out of warranty - essentially full unit swap","10yr/100K powertrain warranty (new), 5yr/60K used transfer","FWD-only with no LSD - torque steer under hard acceleration at 290hp"]',
    450, 6,
    'Good (Hyundai/Kia dealer network)',
    'Moderate (good warranty coverage, but turbo+DCT complexity)',
    'Too new for definitive judgment but early signs are positive. Smartstream 2.5T is a genuine improvement over the Theta II - dual injection, no major failures reported yet. The DCT is the weak link: early production solder joint recall, software quirks, and inherent DCT limitations in traffic. 2023+ models significantly improved. Engine is characteristically loud per owner reports. K5 GT is to the Stinger what a sport sedan is to a sports sedan - FWD vs RWD-biased AWD, DCT vs torque converter, 290hp vs 368hp. Scores lower than Stinger 3.3T (80) by ~6 points, mainly due to less proven engine and DCT risk.'
);

-- ============================================================
-- PART 2: Camry XV70 V6 backfill (id 87) — 2GR-FKS, AA81E 8-speed
-- ============================================================

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm, fuel_system, transmission_type, gear_count, drivetrain, is_hybrid) VALUES (
    87, 'sample',
    'V6', 3456, 6, 'Naturally aspirated',
    301, 6500, 267, 4700,
    'D-4S dual injection (GDI + PFI)',
    'AA81E 8-speed auto', 8, 'FWD',
    0
);

INSERT INTO performance (car_id, source, accel_0_60, top_speed_mph) VALUES (
    87, 'sample', 5.8, 135.0
);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est, depreciation_5yr_pct) VALUES (
    87, 'sample', 34400.0, 'USD', 22.0, 32.0, 400.0, 50.0
);

INSERT INTO dimensions (car_id, length_mm, width_mm, height_mm, wheelbase_mm, source) VALUES (
    87, 4885, 1840, 1455, 2825, 'sample'
);

-- Dimensional reliability for Camry XV70 V6:
-- Engine 88: 2GR-FKS proven architecture, D-4S adds mild risk vs 2GR-FE, 220K+ life expectancy,
--   no catastrophic failures. -12 for carbon buildup, water pump, ignition coil patterns
-- Transmission 68: UA80/AA81E class action lawsuits, $7K failures at 60K, harsh shifting TSBs.
--   The Camry V6 weakest link. 2021+ improved
-- Chassis 92: TNGA-K platform excellent, no structural issues
-- Electronics 90: Toyota Safety Sense standard, reliable infotainment, minimal gremlins
-- Ease of repair 88: Parts everywhere, cheap, simple engine bay. D-4S adds some diagnostic complexity
-- Aggregate: 88*0.25 + 68*0.25 + 92*0.15 + 90*0.15 + 88*0.20 = 22.0 + 17.0 + 13.8 + 13.5 + 17.6 = 83.9
INSERT INTO reliability (car_id, reliability_score, source, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, common_failures, known_issues, avg_repair_cost, recall_count, part_availability, diy_friendliness, score_notes) VALUES (
    87, 83.9, 'sample',
    88, 68, 92, 90, 88,
    '["UA80/AA81E 8-speed harsh shifting and hesitation (class action lawsuit)","Timing cover oil leak (80-150K, $800-1500)","Coolant bypass pipe leak (plastic, 60-120K, $300-600)","Water pump failure (60-100K, $400-700)","Ignition coil failure (30-50K, known GR family issue)","Carbon buildup on intake valves (D-4S, 80K+, $200-400 walnut blast)","Valve cover gasket leak (100K+)"]',
    '["2GR-FKS is NOT just a refreshed 2GR-FE - different heads, block, manifolds, cams, cycle","D-4S dual injection adds GDI + PFI: more power (301 vs 268hp) but more complexity","VVT-iW enables simulated Atkinson cycle for fuel economy","Integrated exhaust manifolds cast into heads - makes header swaps impossible","UA80 transmission has multiple class action lawsuits for harsh shifting and premature failure","2018-2020 models worst for transmission issues; 2021+ improved somewhat","Engine life expectancy 220-240K+ miles with maintenance","14 NHTSA recalls across 2018-2024 Camry (V6-specific: brake booster vacuum pump)","Same block as ES 350 2GR-FE but everything else is different"]',
    500, 14,
    'Excellent (Toyota dealer + aftermarket everywhere)',
    'High (simple engine bay, parts cheap, huge DIY community)',
    'The transmission lets down an otherwise bulletproof powertrain. 2GR-FKS is the 2GR-FE with dual injection, Atkinson cycle, and integrated manifolds - more powerful and efficient but slightly less bulletproof than the FE. Engine itself is an 88 - would be 90+ with port injection only. But the AA81E 8-speed is a genuine problem: class action lawsuits, $7K replacements at 60K, harsh shifting TSBs. Chassis and electronics are Toyota-perfect at 92/90. Ease of repair is excellent everywhere except D-4S diagnostics. The smart play: buy a 2021+ with the improved transmission calibration and do fluid changes every 40K.'
);

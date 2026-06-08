-- ============================================================
-- W212 E-Class SPLIT: pre-facelift (2010-2013) vs post-facelift (2014-2016)
-- ============================================================

-- PART 1: UPDATE existing W212 (id 47) → 2010-2013 pre-facelift M272 era

UPDATE cars SET
    year_end = 2013,
    generation = 'W212 (pre-facelift)'
WHERE id = 47;

UPDATE reliability SET
    reliability_score = 67.2,
    score_engine = 70,
    score_transmission = 65,
    score_chassis = 72,
    score_electronics = 68,
    score_ease_of_repair = 62,
    common_failures = '["Engine mount failure (60-100K, $300-600)","722.9 conductor plate/mechatronic sleeve (80-130K, $2-3K)","Electronic steering lock (ESL) failure - car won''t start","Blower motor squeak/failure ($400-800)","Valve cover and oil pan gasket leaks (70K+)","COMAND controller knob delamination","Battery drain from SAM module","AIRMATIC air springs (if equipped, $1.5-2K/corner at 100K+)"]',
    known_issues = '["M272 90-degree V6 still has balance shaft - W212 units are post-2008 revision so catastrophic gear failure resolved, but not eliminated","722.9 7G-Tronic conductor plate - 3 versions exist, NOT interchangeable. Harsh 1-2 shift is early warning","ESL (electronic steering lock) is W212-specific - when it fails car won''t start. $500-1200 repair","Takata airbag recall - CRITICAL to verify completion via VIN check","Rear subframe rust in salt-belt states - NHTSA complaint item","Pre-facelift COMAND firmware glitchy - 2010-2011 units more prone","Fuel tank lid cracking (TSB)"]',
    avg_repair_cost = 1200,
    recall_count = 8,
    part_availability = 'Good (Mercedes specialist network)',
    diy_friendliness = 'Moderate (wide engine bay, but electronics complex)',
    source = 'sample',
    score_notes = 'Pre-facelift W212 (2010-2013) with M272 port-injection V6. Late-revision M272 - balance shaft gear revised after 2008, catastrophic failure largely resolved. But still 90-degree V6 with balance shaft. 722.9 conductor plate is big drivetrain concern at 80-130K. ESL steering lock is annoying W212-specific failure. Doug DeMuro low ranking is aesthetic, not reliability-based.'
WHERE car_id = 47;

-- PART 2: INSERT new post-facelift W212 (id 161) → 2014-2016 M276 DI

INSERT INTO cars (id, make, model, generation, year_start, year_end, body_style, country, created_at) VALUES (
    161, 'Mercedes-Benz', 'E-Class', 'W212 (post-facelift)', 2014, 2016, 'sedan', 'Germany', datetime('now')
);

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, horsepower_rpm, torque_nm, torque_rpm, fuel_system, transmission_type, gear_count, drivetrain, drag_coefficient, is_hybrid) VALUES (
    161, 'sample',
    'V6', 3498, 6, 'Naturally aspirated',
    302, 6500, 370, 3500,
    'Direct injection (DI)',
    '7G-Tronic (722.9)', 7, 'RWD/AWD',
    0.25, 0
);

INSERT INTO performance (car_id, source, accel_0_60, top_speed_mph, unlimited_top_speed_mph) VALUES (
    161, 'sample', 6.0, 155.0, 149.0
);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est, depreciation_5yr_pct) VALUES (
    161, 'sample', 52500.0, 'USD', 21.0, 30.0, 1100.0, 55.0
);

INSERT INTO dimensions (car_id, length_mm, width_mm, height_mm, wheelbase_mm, source) VALUES (
    161, 4868, 1854, 1470, 2874, 'wikipedia'
);

INSERT INTO reliability (car_id, reliability_score, source, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, common_failures, known_issues, avg_repair_cost, recall_count, part_availability, diy_friendliness, score_notes) VALUES (
    161, 71.9, 'sample',
    78, 70, 74, 72, 65,
    '["Engine mount failure (60-100K, $300-600)","722.9 conductor plate (80-130K, $2-3K, less frequent than pre-facelift)","Electronic steering lock (ESL) failure","Blower motor squeak/failure ($400-800)","AIRMATIC air springs (if equipped, Arnott aftermarket lifetime warranty)","Valve cover gasket leaks (80K+)","Camshaft position sensor oil leak into harness (early 2014 units, fixed by 2016)"]',
    '["M276 60-degree V6 - NO balance shaft. Fundamentally better architecture than M272","M276 shares basic architecture with Chrysler Pentastar V6 (DaimlerChrysler era)","DI carbon buildup on intake valves - potential long-term issue, not yet widespread","722.9 3rd-generation conductor plate in post-facelift - improved but still a known wear item","ESL (electronic steering lock) remains W212-specific Achilles heel","Post-facelift COMAND significantly improved over 2010-2013 units","Takata airbag recall still applies - verify via VIN","2015-2016 models are the sweet spot - fully refined M276, updated transmission, best electronics"]',
    1100, 5,
    'Good (Mercedes specialist network + better aftermarket documentation)',
    'Moderate (improved documentation, still Mercedes parts pricing)',
    'The return to form W212. M276 60-degree V6 eliminates balance shaft entirely. 4-chain timing vs M272 single chain. Updated 722.9 calibration with improved conductor plate. Post-facelift COMAND significantly improved. Owner consensus overwhelmingly positive - bulletproof for well-maintained examples. 2015-2016 are best years. Doug DeMuro ranked it poorly for looks, not reliability.'
);

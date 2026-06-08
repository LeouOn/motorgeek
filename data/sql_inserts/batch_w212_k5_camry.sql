-- ============================================================
-- W212 E-Class SPLIT + K5 GT + Camry V6 backfill
-- All in one clean file, idempotent
-- ============================================================

-- ============================================================
-- PART 1: W212 PRE-FACELIFT (update existing id=47)
-- ============================================================
UPDATE cars SET
    generation = 'W212 (pre-facelift)',
    year_start = 2010,
    year_end = 2013
WHERE id = 47;

UPDATE powertrain_ice SET
    horsepower_bhp = 268,
    torque_nm = 350,
    fuel_system = 'MPI (port injection)'
WHERE car_id = 47;

UPDATE reliability SET
    reliability_score = 67.2,
    score_engine = 70,
    score_transmission = 65,
    score_chassis = 72,
    score_electronics = 68,
    score_ease_of_repair = 62,
    common_failures = '["Engine mount failure (60-100K, $300-600)","722.9 conductor plate (80-130K, $2-3K)","Electronic steering lock (ESL) failure","Blower motor squeak/failure ($400-800)","Valve cover and oil pan gasket leaks (70K+)","COMAND controller knob delamination","Battery drain from SAM module","AIRMATIC air springs (if equipped, $1.5-2K/corner at 100K+)"]',
    known_issues = '["M272 90° V6 still has balance shaft — W212 units are post-2008 revision so catastrophic gear failure resolved","722.9 conductor plate — 3 versions, NOT interchangeable. Harsh 1-2 shift is early warning","ESL steering lock is W212-specific — car won''t start when it fails","Takata airbag recall — verify via VIN","Rear subframe rust in salt-belt states","Pre-facelift COMAND firmware more glitchy"]',
    avg_repair_cost = 1200,
    recall_count = 8,
    part_availability = 'Good (Mercedes specialist network)',
    diy_friendliness = 'Moderate (wide engine bay, complex electronics)',
    source = 'sample',
    score_notes = 'Pre-facelift W212 with late-rev M272 port-injection V6. Balance shaft gear revised after 2008 — catastrophic failure resolved but shaft still present. 722.9 conductor plate is the big drivetrain concern. ESL steering lock is an annoying W212-specific failure. Doug DeMuro''s low ranking is aesthetic not reliability-based.'
WHERE car_id = 47;

-- ============================================================
-- PART 2: W212 POST-FACELIFT (new id=161)
-- ============================================================
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
    '["Engine mount failure (60-100K, $300-600)","722.9 conductor plate (80-130K, less frequent than pre-FL)","Electronic steering lock (ESL) failure","Blower motor squeak/failure ($400-800)","AIRMATIC air springs (if equipped, Arnott lifetime warranty)","Valve cover gasket leaks (80K+)","Cam sensor oil leak into harness (2014 early, fixed 2016)"]',
    '["M276 60° V6 — NO balance shaft. Fundamentally better than M272","M276 shares architecture with Chrysler Pentastar (DaimlerChrysler era)","DI carbon buildup on intake valves — potential long-term concern","722.9 3rd-gen conductor plate — improved but still a wear item","ESL remains W212-specific Achilles heel","Post-facelift COMAND significantly improved","2015-2016 are the sweet spot — fully refined"]',
    1100, 5,
    'Good (Mercedes specialist network)',
    'Moderate (improved documentation, still Mercedes parts pricing)',
    'The "return to form" W212. M276 eliminates balance shaft entirely. 4-chain timing vs M272 single chain. Updated 722.9 calibration. Post-facelift COMAND much improved. Owner consensus overwhelmingly positive — "bulletproof" for well-maintained examples. 2015-2016 are best years. SBC eliminated, AIRMATIC optional, better rust protection than W211.'
);

-- ============================================================
-- PART 3: KIA K5 GT (new id=162)
-- ============================================================
INSERT INTO cars (id, make, model, generation, year_start, year_end, body_style, country, created_at)
VALUES (162, 'Kia', 'K5 GT', '1st gen', 2021, 2024, 'sedan', 'South Korea', datetime('now'));

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, torque_nm, fuel_system, transmission_type, gear_count, drivetrain, is_hybrid)
VALUES (162, 'sample', 'I4', 2497, 4, 'Turbocharged', 290, 422, 'GDI + MPi (dual injection)', '8-speed wet DCT', 8, 'FWD', 0);

INSERT INTO performance (car_id, source, accel_0_60, top_speed_mph)
VALUES (162, 'sample', 5.7, 155.0);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est, depreciation_5yr_pct)
VALUES (162, 'sample', 31090.0, 'USD', 23.0, 32.0, 460.0, 50.0);

INSERT INTO dimensions (car_id, length_mm, width_mm, height_mm, wheelbase_mm, source)
VALUES (162, 4905, 1860, 1445, 2845, 'wikipedia');

INSERT INTO reliability (car_id, reliability_score, source, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, common_failures, known_issues, avg_repair_cost, recall_count, part_availability, diy_friendliness, score_notes)
VALUES (162, 74.3, 'sample', 75, 68, 80, 78, 72,
    '["DCT oil pump solder joint (2021-early 2022, recall)","DCT software logic — harsh shifts (TSB SA502/SA526)","Fuel injector failures (2021-22 batch)","Carbon buildup (GDI component, 80K+)","Turbo wastegate rattle (potential, 60K+)","Engine loudness (characteristic, not failure)"]',
    '["Smartstream G2.5T (Theta III) — significant improvement over Theta II, no major failures yet","BUT: only 5 years of data, too new for definitive 100K+ assessment","DCT wet clutch is durable but early production had solder joint recall — get 2023+","No LSD on GT — 290hp through FWD = torque steer under hard acceleration","NA version of same engine has piston slap concerns, turbo version appears better","10yr/100K powertrain warranty helps new buyers, 5yr/60K used"]',
    450, 6,
    'Good (Hyundai/Kia network)',
    'Moderate (turbo + DCT complexity, warranty helps)',
    'The fun but unproven option. Smartstream 2.5T is a clean-sheet design that improves massively on the oil-burning Theta II. Dual injection mitigates carbon buildup. But at only 5 years old, long-term durability is unknown. DCT had early production issues (solder joint recall, software TSBs) — 2023+ builds are sorted. Compared to our Stinger 3.3T (scored 80): less power, FWD only, less proven, but cheaper and better fuel economy. The K5 GT trades Stinger''s proven Lambda II and proper RWD architecture for a lower price and newer tech.'
);

-- ============================================================
-- PART 4: CAMRY XV70 V6 backfill (existing id=87)
-- ============================================================
UPDATE cars SET
    generation = 'XV70 (V6)',
    year_start = 2018,
    year_end = 2024,
    body_style = 'sedan',
    country = 'Japan'
WHERE id = 87;

INSERT OR IGNORE INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, torque_nm, fuel_system, transmission_type, gear_count, drivetrain, is_hybrid)
VALUES (87, 'sample', 'V6', 3498, 6, 'Naturally aspirated', 301, 362, 'D-4S (dual injection: GDI + PFI)', 'AA81E 8-speed auto', 8, 'FWD', 0);

INSERT OR IGNORE INTO performance (car_id, source, accel_0_60, top_speed_mph)
VALUES (87, 'sample', 5.8, 135.0);

INSERT OR IGNORE INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est, depreciation_5yr_pct)
VALUES (87, 'sample', 34400.0, 'USD', 22.0, 32.0, 400.0, 48.0);

INSERT OR IGNORE INTO reliability (car_id, reliability_score, source, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, common_failures, known_issues, avg_repair_cost, recall_count, part_availability, diy_friendliness, score_notes)
VALUES (87, 80.4, 'sample', 88, 68, 92, 90, 88,
    '["UA80/AA81E 8-speed harsh shifting — class action lawsuits","Timing cover oil leak (80-150K, $800-1500)","Coolant bypass pipe leak (plastic, 60-120K)","Water pump failure (60-100K)","Ignition coil failure (30-50K, GR family pattern)","Carbon buildup intake valves (D-4S, 80K+, walnut blast)"]',
    '["2GR-FKS: D-4S dual injection adds complexity vs 2GR-FE. More power (301hp) but slightly less reliable per multiple sources","UA80 transmission: THE big liability. Harsh shifts, gear hunting, hesitation. 2018-2020 worst, 2021+ improved. $7K replacement at ~60K if fluid not maintained","VVT-iW Atkinson cycle adds another failure mode vs standard VVT-i","Integrated exhaust manifolds = no header swaps","14 NHTSA recalls across XV70 generation (1 V6-specific: brake booster vacuum pump)","D-4S helps mitigate carbon buildup vs pure GDI but doesn''t eliminate it"]',
    500, 14,
    'Excellent (Toyota network + every auto parts store)',
    'High (simple engine bay, parts everywhere, D-4S adds slight complexity)',
    'The benchmark V6 sedan — 80% of the Lexus ES experience for 60% of the price. Same 2GR family as ES 350 but with D-4S dual injection and the problematic AA81E 8-speed. The 2GR-FKS is slightly less bulletproof than the 2GR-FE in the ES — more power, more complexity. The transmission is the real concern: multiple class action lawsuits for harsh shifting and premature failure. 2021+ models improved. TNGA platform is excellent. Interior is a step below ES but very good for $34K. The smart buy if you want V6 Toyota reliability but don''t need Lexus luxury.'
);

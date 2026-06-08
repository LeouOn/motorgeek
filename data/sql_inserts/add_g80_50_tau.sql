-- G80 5.0 Tau V8 entry (id 163)
-- Same Tau 5.0 as G90 but in lighter G80 body (2017-2020 DH generation)

-- Car entry
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, production_units, description, image_paths, created_at, character, family, variant)
VALUES (163, 'Genesis', 'G80', '1st gen (DH)', 2017, 2020, '2017-2020', 'sedan', 'South Korea', NULL, 'G80 with Hyundai Tau 5.0 V8 — port-injected NA V8, Wards 10 Best engine. Same engine as G90 5.0 in lighter body. Rare: most G80s sold with 3.8L V6 or 3.3T V6.', '[]', datetime('now'), 'luxury', 'Tau', 'G80 5.0 V8');

-- Powertrain (Tau 5.0 V8)
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, torque_nm, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (201, 163, 'wikipedia', '5.0L V8', 5038.0, 8, 'Naturally aspirated', 420.0, 540.0, 'MPI (port injection)', '8-speed automatic', 8, 'RWD standard / AWD optional', 2050.0, 0);

-- Cost to own
INSERT INTO cost_to_own (id, car_id, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est, insurance_group, source)
VALUES (201, 163, 16.0, 24.0, 900.0, 'luxury', 'sample');

-- Performance indices (placeholder until ZePerfs data)
INSERT INTO performance (id, car_id, source, extra)
VALUES (201, 163, 'sample', '{}');

-- Reliability with dimensional scores
-- Same Tau 5.0 as G90 (id 8) — slightly better ease_of_repair because G80 is lighter/more common
-- Engine 80: Same Tau 5.0 — port injection, roller followers, hydraulic lifters, Wards winner
-- Trans 82: Same ZF/Hyundai 8-speed
-- Chassis 80: Same DH platform
-- Electronics 72: Same as G90
-- Ease 62: Slightly better than G90 (62 vs 60) — G80 more common = slightly better parts network
-- Aggregate: 80*0.25 + 82*0.25 + 80*0.15 + 72*0.15 + 62*0.20 = 20.0 + 20.5 + 12.0 + 10.8 + 12.4 = 75.7
INSERT INTO reliability (id, car_id, reliability_score, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, common_failures, known_issues, avg_repair_cost, recall_count, part_availability, diy_friendliness, source, score_notes)
VALUES (
    201, 163, 75.7, 80, 82, 80, 72, 62,
    '["Parts availability backorders (5.0-specific parts)","Oil pump access requires subframe + both oil pans","Cracked lower timing cover (rare, 90K+)","Air suspension maintenance (if equipped, $1-2K/corner)"]',
    '["Same Tau 5.0 V8 as G90 — port injection, roller cam followers, hydraulic lash adjusters","2012 early PVD ring issue was supplier defect, fixed by late 2012","Forum teardowns show excellent internal condition at 90K with maintenance","Lighter body (2050 vs 2150 kg) = slightly less stress on drivetrain","G80 5.0 is rarer than 3.8L/3.3T variants — most were sold with V6","CRITICAL weakness: same parts availability issues as G90 5.0","Pre-2012: ZF 6-speed. 2012+: Hyundai A8TR1 (adequate for 398lb-ft)"]',
    800, 2,
    'Poor (5.0-specific parts frequently back-ordered, same as G90)',
    'Difficult (rare engine, mechanics unfamiliar, parts scarce)',
    'sample',
    'G80 5.0 Tau shares every strength and weakness of G90 5.0 Tau. Same port-injected NA V8, same Wards-winning architecture. Slightly better ease (62 vs 60) because G80 is the more common body = marginally better parts pipeline. Aggregate 75.7 vs G90 75.3. The gap to LS430 (88.5) is real: Lexus has proven 300K+ longevity, 10x production volume, and dealer-everywhere parts. But 75.7 is honest for what the Tau is — Hyundai best engine in their best sedan body.'
);

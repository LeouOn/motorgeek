-- Update existing W222 (car_id=42) to be specifically pre-facelift M278 S550
UPDATE cars SET
  year_start = 2014,
  year_end = 2017,
  variant = 'S550 M278 pre-facelift',
  description = 'W222 S-Class pre-facelift (2014-2017) with M278 4.7L twin-turbo V8 (449hp/516lb-ft). 7G-Tronic transmission. NTG5 COMAND. AIRMATIC standard, Magic Body Control optional. Known issues: cam sensor oil wicking to ECU (#1 killer,  pigtail fix prevents + ECU death), oil cooler leaks, direct injection carbon buildup (walnut blast ~60K mi), Airmatic struts at 80K+. Aluminum hybrid body requires certified collision repair (~10 shops in USA).'
WHERE id = 42;

-- Recalibrate pre-facelift reliability (M278 cam sensor ECU risk lowers engine score)
UPDATE reliability SET
  score_engine = 66.0,
  score_transmission = 72.0,
  score_chassis = 66.0,
  score_electronics = 62.0,
  score_ease_of_repair = 55.0,
  reliability_score = 66.0*0.25 + 72.0*0.25 + 66.0*0.15 + 62.0*0.15 + 55.0*0.20,
  common_failures = '["cam_sensor_oil_wicking_ECU","oil_cooler_leaks","airmatic_struts","timing_chain_tensioner","carbon_buildup","7g_conductor_plate"]',
  known_issues = '["cam_sensor_ecu: Oil wicks from cam sensors through wiring harness into ECU. #1 S550 killer.  pigtail fix prevents + ECU death. Check all 4 connectors at PPI","oil_cooler: Oil filter housing/oil cooler leaks cause oil+coolant mix. -3000 indie. Common at 80K+","airmatic: CDC struts crack at 80K. Arnott rebuilt  each, dealer  each. Compressor burns out from overwork. -2500 per corner","timing_chain: Pre-Feb 2013 engines need check valves. 2014+ should be OK. Cold-start rattle = tensioner issue","carbon_buildup: Direct injection carbon on intake valves. Walnut blast every 60K mi, -1200","7g_conductor: 7G-Tronic conductor plate failure, rough shifting. -1500","body_repair: Aluminum hybrid bodyshell requires Mercedes Elite Certified Collision Center. Only ~10 in USA"]'
WHERE car_id = 42;

-- Keep pre-facelift build quality scores as-is (78.3 is fair — materials are excellent)

-- Insert facelift W222 S560 as new entry (car_id=181)
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, description, image_paths, created_at, character, family, variant)
VALUES (181, 'Mercedes-Benz', 'S-Class', 'W222', 2018, 2020, 'modern', 'sedan', 'Germany',
'W222 S-Class facelift (2018-2020) S560 with M176 4.0L twin-turbo V8 (463hp/516lb-ft). Hot-V turbo layout. 9G-Tronic transmission. NTG6 COMAND with CarPlay/Android Auto. AIRMATIC standard, improved Magic Body Control optional. 6000+ components redesigned in facelift. Known issues: P06DA00 oil pump solenoid (.5-9.5K on 4MATIC, engine+trans removal), cylinder deactivation lifter failures, hot-V turbo oil seal degradation, valve cover gasket requires front-end removal.',
'[]', datetime('now'), 'luxury', 'S-Class', 'S560 M176 facelift');

-- Powertrain for facelift S560
INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, torque_nm, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (181, 'librarian+analysis', '4.0L twin-turbo V8 M176 (Hot-V)', 3982.0, 8, 'twin-turbo', 463.0, 700.0, 'direct injection', '9-speed automatic', 9, 'RWD/4MATIC', 1995.0, 0);

-- Reliability for facelift S560
INSERT INTO reliability (car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (181, 'librarian+analysis', 68.4,
'["P06DA00_oil_pump_solenoid","cylinder_deactivation_lifters","hot_v_turbo_seals","valve_cover_gasket","airmatic_struts","9g_shift_quality"]',
'["P06DA00: Oil pump solenoid inside oil pan. On 4MATIC the oil pan is bolted to bell housing requiring engine+trans removal. -9500. The M176 defining failure","cylinder_deactivation: Lifters for deactivated cylinders (2,3,5,8) can fail causing rough idle and ticking. Up to ","hot_v_turbo: Twin turbos inside V = heat degradation of oil seals. -5500 per turbo. Cylinder deactivation adds stress","valve_cover: Front end of car must be removed for valve cover gasket service. -3000","airmatic: Same AIRMATIC family as pre-facelift but improved. Struts still wear at 80-100K","9g_tronic: Materially smoother than 7G in town. Conductor plate less problematic"]',
'["engine: M176 is NOT clearly more reliable than M278. Trades cam sensor ECU risk for oil pump solenoid risk. Hot-V layout = more turbo heat stress. Cylinder deactivation adds lifter complexity","transmission: 9G-Tronic is materially better than 7G. Smoother, fewer conductor plate issues","chassis: AIRMATIC improved but same fundamental wear pattern. MBC improved over pre-facelift","electronics: NTG6 COMAND with CarPlay is a real improvement over NTG5. Better driver assists. But still ~100 ECUs","ease_of_repair: Same aluminum body issue. M176 valve cover requires front-end removal. Oil pump solenoid on 4MATIC is engine+trans removal"]');

-- Build quality for facelift S560
INSERT INTO build_quality (car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
  body_construction_notes, nvh_isolation_notes, interior_materials_notes, paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes, q_score_notes,
  leather_grade, paint_stages)
VALUES (181, 81.1, 84.0, 85.0, 90.0, 84.0, 68.0, 72.0,
'W222 facelift aluminum hybrid bodyshell. Same 50% aluminum construction as pre-facelift. Improved panel fit from facelift production updates.',
'Better NVH than pre-facelift. Additional sound deadening in facelift. Improved AIRMATIC calibration. Near-silent cabin.',
'Facelift interior upgrades: three-spoke Nappa leather wheel, new seat controls, Energizing Comfort Control, upgraded trim options. Best S-Class interior until W223.',
'Mercedes paint quality excellent. Same multi-stage process. Aluminum panels resist corrosion.',
'NTG6 COMAND with CarPlay/Android Auto is a genuine usability improvement that extends functional life. But still ~100 ECUs. Driver assistance modules age.',
'Interior materials hold up well. New wheel design more durable. Steering wheel wear at 100K+ common.',
'W222 facelift Q-score 81.1. Improved over pre-facelift (78.3) due to better interior, better COMAND, better NVH calibration. The facelift was 6000+ components — the improvements are real, not cosmetic.',
'Nappa leather', 7);

-- Cost to own for facelift S560
INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (181, 'librarian+analysis', 104000.0, 'USD', 16.0, 24.0, 1600.0);

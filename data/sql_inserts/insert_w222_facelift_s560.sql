INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, description, image_paths, created_at, character, family, variant)
VALUES (182, 'Mercedes-Benz', 'S-Class', 'W222', 2018, 2020, 'modern', 'sedan', 'Germany',
'W222 S-Class facelift S560 with M176 4.0L twin-turbo V8 Hot-V (463hp/516lb-ft). 9G-Tronic. NTG6 COMAND with CarPlay/Android Auto. 6000+ components redesigned. AIRMATIC standard, improved Magic Body Control optional. Cylinder deactivation. Known issues: P06DA00 oil pump solenoid (5.5-9.5K on 4MATIC), cylinder deactivation lifter failures, hot-V turbo oil seal degradation.',
'[]', datetime('now'), 'luxury', 'S-Class', 'S560 M176 facelift');

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, torque_nm, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (182, 'librarian+analysis', '4.0L twin-turbo V8 M176 Hot-V', 3982.0, 8, 'twin-turbo', 463.0, 700.0, 'direct injection', '9G-Tronic 9-speed auto', 9, 'RWD/4MATIC', 1995.0, 0);

INSERT INTO reliability (car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (182, 'librarian+analysis', 68.4,
'["P06DA00_oil_pump_solenoid","cylinder_deactivation_lifters","hot_v_turbo_seals","valve_cover_gasket_front_end_removal","airmatic_struts","9g_conductor_plate"]',
'["P06DA00: Oil pump solenoid inside oil pan. On 4MATIC the oil pan is bolted to bell housing requiring engine+trans removal. -9500. The M176 defining failure","cylinder_deactivation: Lifters for deactivated cylinders (2,3,5,8) can fail causing rough idle and ticking. Up to ","hot_v_turbo: Twin turbos inside V = heat degradation of oil seals. -5500 per turbo","valve_cover: Front end of car must be removed for valve cover gasket service. -3000","airmatic: Same AIRMATIC family as pre-facelift. Struts wear at 80-100K. Arnott rebuilt /corner","9g_tronic: Materially smoother than 7G in town. Conductor plate less problematic"]',
'["engine: M176 is NOT clearly more reliable than M278. Trades cam sensor ECU risk for oil pump solenoid risk. Hot-V layout adds turbo heat stress. Cylinder deactivation adds lifter complexity. But newer design overall","transmission: 9G-Tronic materially better than 7G. Smoother shifting, fewer conductor plate issues","chassis: AIRMATIC improved but same fundamental wear pattern. MBC improved over pre-facelift","electronics: NTG6 COMAND with CarPlay is genuine usability improvement. Better driver assists. Still ~100 ECUs","ease_of_repair: Same aluminum body issue. M176 valve cover requires front-end removal. Oil pump solenoid on 4MATIC is engine+trans removal"]');

INSERT INTO build_quality (car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
  body_construction_notes, nvh_isolation_notes, interior_materials_notes, paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes, q_score_notes,
  leather_grade, paint_stages)
VALUES (182, 81.1, 84.0, 85.0, 90.0, 84.0, 68.0, 72.0,
'W222 facelift aluminum hybrid bodyshell. Same 50% aluminum construction. Improved panel fit from facelift production updates.',
'Better NVH than pre-facelift. Additional sound deadening. Improved AIRMATIC calibration. Near-silent cabin.',
'Facelift interior upgrades: three-spoke Nappa leather wheel, new seat controls, Energizing Comfort, upgraded trim. Best S-Class interior until W223.',
'Mercedes paint quality excellent. Multi-stage process. Aluminum panels resist corrosion.',
'NTG6 COMAND with CarPlay/Android Auto is genuine usability improvement extending functional life. But still ~100 ECUs. Driver assistance modules age.',
'Interior materials hold up well. New wheel design more durable. Steering wheel wear at 100K+.',
'W222 facelift Q-score 81.1. Improved over pre-facelift (78.3) due to better interior, better COMAND, better NVH. The facelift was 6000+ components redesigned.',
'Nappa leather', 7);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (182, 'librarian+analysis', 104000.0, 'USD', 16.0, 24.0, 1600.0);

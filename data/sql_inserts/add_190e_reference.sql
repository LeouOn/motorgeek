-- 190E 2.3 W201 - proper reference car record
DELETE FROM driving_engagement WHERE car_id = 999;
DELETE FROM cost_to_own WHERE car_id = 999;
DELETE FROM build_quality WHERE car_id = 999;
DELETE FROM reliability WHERE car_id = 999;
DELETE FROM powertrain_ice WHERE car_id = 999;
DELETE FROM cars WHERE id = 999;

INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, description, image_paths, created_at, character, family, variant)
VALUES (999, 'Mercedes-Benz', '190E', 'W201', 1984, 1993, 'classic', 'sedan', 'Germany',
'Character reference. 190E 2.3 8V NA - the Mercedes that taught a generation of enthusiasts that you do not need horsepower to have character. Compact RWD, 0-60 in 10.2s, limited-slip diff on sport models. The DNA that runs in every 3-Series today. 190E 2.3-16V had the Cosworth head and was the real one. W201 is the genesis of the 3-Series platform.',
'[]', datetime('now'), 'warm', '190E', '2.3L 8V');

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, torque_nm, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid, engine_code)
VALUES (999, 'manual+analysis', '2.3L I4 M102', 2299, 4, 'naturally aspirated', 127, 190, 'CFI', '4-speed automatic', 4, 'RWD', 1280, 0, 'M102');

INSERT INTO reliability (car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (999, 'manual+analysis', 85.0, '["wiring_harness_age","window_regulator","sunroof_rails"]', '["M102 2.3L is extremely reliable - 300K+ mi examples exist","4-speed auto is slow but reliable","Build quality is excellent - overengineered like all W201s","Rust is the main concern - check arches and jack points"]', 90.0, 85.0, 80.0, 60.0, 75.0, 'M102 2.3L 8V: 85-90 reliability. The old Mercedes reliability is real.');

INSERT INTO build_quality (car_id, source, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging)
VALUES (999, 'manual+analysis', 72.0, 80.0, 65.0, 60.0, 40.0, 30.0, 45.0);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (999, 'manual+analysis', 32000.0, 'USD', 18.0, 24.0, 600.0);

INSERT INTO driving_engagement (car_id, steering_feel, chassis_balance, transmission_engagement, powertrain_character, lightness_agility, limit_accessibility, des_score, des_notes, source)
VALUES (999, 7.0, 6.0, 5.0, 6.0, 8.0, 8.0, 6.3, 'Character reference. 190E 2.3 8V RWD NA. Recirculating-ball steering with actual feel. Compact RWD. Modest power but excellent chassis. The DNA that runs in every 3-Series today.', 'manual+analysis');

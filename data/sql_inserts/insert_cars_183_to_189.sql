PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

-- ============================================================
-- Car 183: Toyota Camry XV50 V6 (2012-2017) XSE V6 2GR-FE
-- ============================================================
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (183, 'Toyota', 'Camry', 'XV50', 2012, 2017, 'modern', 'sedan', 'Japan', '[]', datetime('now'), 'family', 'Camry', 'XSE V6 2GR-FE');

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, torque_nm, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (183, 'librarian+analysis', '3.5L V6 2GR-FE', 3456, 6, 'naturally aspirated', 268, 332, 'port injection', '6-speed automatic', 6, 'FWD', 1490, 0);

INSERT INTO reliability (car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (183, 'librarian+analysis', 87.6,
  '["vvti_gear_rattle","water_pump_weep","oil_cooler_pipe_leak","torque_converter_shudder"]',
  '["vvti_rattle: Cold start rattle from VVT-i gear assembly","u660e_tc: Torque converter shudder under light throttle"]',
  93, 87, 86, 84, 88,
  '["engine: 2GR-FE proven, watch VVT-i gear","transmission: U660E solid but TC shudder common","electronics: Standard Toyota reliable","ease_of_repair: Familiar platform, good parts availability"]');

INSERT INTO build_quality (car_id, source, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging)
VALUES (183, 'librarian+analysis', 70.0, 72, 68, 66, 66, 80, 68);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (183, 'librarian+analysis', 31000, 'USD', 20, 29, 450);

-- ============================================================
-- Car 184: Toyota Camry XV50 Hybrid (2012-2017) Hybrid XLE HSD
-- ============================================================
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (184, 'Toyota', 'Camry', 'XV50', 2012, 2017, 'modern', 'sedan', 'Japan', '[]', datetime('now'), 'family', 'Camry', 'Hybrid XLE HSD');

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, torque_nm, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (184, 'librarian+analysis', '2.5L I4 2AR-FXE Atkinson hybrid', 2494, 4, 'naturally aspirated', 200, 199, 'port injection', 'e-CVT (planetary)', 0, 'FWD', 1560, 1);

INSERT INTO reliability (car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (184, 'librarian+analysis', 85.2,
  '["inverter_converter_recall","brake_booster_leak","hybrid_battery_degradation","egr_cooler_clog"]',
  '["inverter_recall: OEM recall for inverter/converter, free fix","brake_booster: Nitrogen leak causes hard pedal"]',
  90, 92, 86, 80, 78,
  '["engine: 2AR-FXE Atkinson cycle proven","transmission: e-CVT planetary bulletproof","electronics: Hybrid controls reliable after recalls","ease_of_repair: Hybrid systems need specialist tools"]');

INSERT INTO build_quality (car_id, source, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging)
VALUES (184, 'librarian+analysis', 70.5, 73, 68, 70, 66, 78, 68);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (184, 'librarian+analysis', 29000, 'USD', 43, 39, 450);

-- ============================================================
-- Car 185: Honda Accord 10th gen 2.0T (2018-2022) Sport K20C4 6MT
-- ============================================================
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (185, 'Honda', 'Accord', '10th gen', 2018, 2022, 'modern', 'sedan', 'Japan', '[]', datetime('now'), 'sport', 'Accord', '2.0T Sport K20C4 6MT');

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, torque_nm, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (185, 'librarian+analysis', '2.0L turbo I4 K20C4', 1996, 4, 'turbo', 252, 370, 'direct injection', '6-speed manual', 6, 'FWD', 1530, 0);

INSERT INTO reliability (car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (185, 'librarian+analysis', 84.4,
  '["oil_dilution_mild","intake_valve_carbon","ac_compressor_failure","infotainment_freezes"]',
  '["oil_dilution: Direct injection, less severe than 1.5T","infotainment: 2018 head unit laggy and glitchy"]',
  86, 84, 86, 82, 84,
  '["engine: K20C4 derived from Type R, robust","transmission: 6MT simple and durable","electronics: Infotainment glitches common","ease_of_repair: Modern but accessible"]');

INSERT INTO build_quality (car_id, source, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging)
VALUES (185, 'librarian+analysis', 71.0, 75, 65, 70, 68, 72, 70);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (185, 'librarian+analysis', 31000, 'USD', 22, 32, 550);

-- ============================================================
-- Car 186: Honda Accord 9th gen I4 (2013-2017) Sport K24W3 6MT
-- ============================================================
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (186, 'Honda', 'Accord', '9th gen', 2013, 2017, 'modern', 'sedan', 'Japan', '[]', datetime('now'), 'family', 'Accord', 'Sport K24W3 6MT');

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, torque_nm, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (186, 'librarian+analysis', '2.4L I4 K24W3 Earth Dreams', 2356, 4, 'naturally aspirated', 189, 245, 'direct injection', '6-speed manual', 6, 'FWD', 1470, 0);

INSERT INTO reliability (car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (186, 'librarian+analysis', 84.4,
  '["vtc_actuator_rattle","oil_consumption","direct_injector_seals","display_audio_glitches"]',
  '["vtc_actuator: Cold start rattle, TSB/recall available","oil_consumption: Some K24W3 consume oil, monitor level"]',
  87, 80, 85, 82, 88,
  '["engine: K24W3 solid, VTC actuator is known issue","transmission: 6MT simple","electronics: Display Audio head unit laggy","ease_of_repair: Excellent parts availability and docs"]');

INSERT INTO build_quality (car_id, source, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging)
VALUES (186, 'librarian+analysis', 70.0, 72, 65, 68, 68, 80, 68);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (186, 'librarian+analysis', 24500, 'USD', 24, 34, 450);

-- ============================================================
-- Car 187: Mazda 3 Skyactiv 2.5 (2014-2018) BM hatch 6MT
-- ============================================================
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (187, 'Mazda', 'Mazda3', 'BM', 2014, 2018, 'modern', 'hatchback', 'Japan', '[]', datetime('now'), 'commuter', 'Mazda3', '2.5L Skyactiv-G 6MT');

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, torque_nm, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (187, 'librarian+analysis', '2.5L I4 Skyactiv-G', 2488, 4, 'naturally aspirated', 184, 251, 'direct injection', '6-speed manual', 6, 'FWD', 1320, 0);

INSERT INTO reliability (car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (187, 'librarian+analysis', 82.0,
  '["cylinder_head_crack_early","thermostat_housing","motor_mount_wear","infotainment_reboots"]',
  '["cylinder_head: 2014-2015 only, revised casting after","motor_mount: Passenger side mount fails early"]',
  84, 84, 82, 76, 84,
  '["engine: Skyactiv reliable after head revision","transmission: 6MT smooth, DMF clutch wear","electronics: Infotainment reboots occasional","ease_of_repair: Compact packaging adds time"]');

INSERT INTO build_quality (car_id, source, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging)
VALUES (187, 'librarian+analysis', 69.0, 72, 64, 68, 72, 70, 68);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (187, 'librarian+analysis', 24500, 'USD', 27, 37, 450);

-- ============================================================
-- Car 188: Subaru Legacy 4th gen GT (2005-2009) BL/BP wagon EJ255 turbo
-- ============================================================
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (188, 'Subaru', 'Legacy', 'BL/BP', 2005, 2009, 'modern', 'wagon', 'Japan', '[]', datetime('now'), 'sport', 'Legacy', 'GT wagon EJ255 turbo');

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, torque_nm, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (188, 'librarian+analysis', '2.5L turbo H4 EJ255', 2457, 4, 'turbo', 250, 339, 'port injection', '5-speed manual', 5, 'AWD', 1490, 0);

INSERT INTO reliability (car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (188, 'librarian+analysis', 77.4,
  '["ringland_failure","head_gasket","turbo_oil_coking","banjo_bolt_starvation"]',
  '["ringland: #4 cylinder piston ringland cracks under boost","banjo_bolt: Oil feed filter clogs, many remove"]',
  77, 80, 76, 72, 82,
  '["engine: EJ255 turbo has ringland and head gasket risks","transmission: 5MT robust, clutch upgrades common","chassis: AWD system reliable","ease_of_repair: Boxer access tight, head gasket expensive"]');

INSERT INTO build_quality (car_id, source, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging)
VALUES (188, 'librarian+analysis', 68.3, 70, 68, 68, 70, 68, 66);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (188, 'librarian+analysis', 28000, 'USD', 17, 23, 700);

-- ============================================================
-- Car 189: Subaru Legacy 2nd gen (1993-1998) BD/BG wagon EJ22
-- ============================================================
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (189, 'Subaru', 'Legacy', 'BD/BG', 1993, 1998, 'classic', 'wagon', 'Japan', '[]', datetime('now'), 'utility', 'Legacy', 'L wagon EJ22');

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, torque_nm, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (189, 'librarian+analysis', '2.2L H4 EJ22', 2212, 4, 'naturally aspirated', 137, 196, 'port injection', '5-speed manual', 5, 'AWD', 1340, 0);

INSERT INTO reliability (car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (189, 'librarian+analysis', 80.6,
  '["head_gasket","timing_belt_service","rust_rockers","valve_cover_gasket"]',
  '["timing_belt: Interference engine, 105K interval","rust: Rocker panels and rear quarters"]',
  85, 80, 74, 78, 86,
  '["engine: EJ22 exceptionally durable for Subaru","transmission: 5MT durable","chassis: Rust is the real killer","ease_of_repair: Simple and well-documented"]');

INSERT INTO build_quality (car_id, source, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging)
VALUES (189, 'librarian+analysis', 62.2, 66, 62, 62, 55, 70, 58);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (189, 'librarian+analysis', 19000, 'USD', 19, 26, 500);

COMMIT;
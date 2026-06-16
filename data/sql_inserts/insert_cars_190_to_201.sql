PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

-- ============================================================
-- Car 190: Toyota Avalon V6 (2013-2018) XLE V6 2GR-FE
-- ============================================================
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (190, 'Toyota', 'Avalon', '3rd gen', 2013, 2018, 'modern', 'sedan', 'Japan', '[]', datetime('now'), 'luxury', 'Avalon', 'XLE V6 2GR-FE');

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, torque_nm, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (190, 'librarian+analysis', '3.5L V6 2GR-FE', 3456, 6, 'naturally aspirated', 268, 332, 'port injection', '6-speed automatic', 6, 'FWD', 1570, 0);

INSERT INTO reliability (car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (190, 'librarian+analysis', 86.8,
  '["water_pump","vvt_oil_line"]',
  '["2GR-FE: Same engine as Camry V6 and Lexus ES350. 300k+ miles common. Rubber VVT oil line recalled. Minor water pump seep at 80-110K."]',
  93, 88, 82, 80, 86,
  '["2GR-FE benchmark reliability", "6-speed proven", "Same parts as Camry V6"]');

INSERT INTO build_quality (car_id, source, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging)
VALUES (190, 'librarian+analysis', 76.1, 76, 80, 76, 72, 78, 76);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (190, 'librarian+analysis', 33000, 'USD', 19, 28, 450);

-- ============================================================
-- Car 191: Toyota Avalon Hybrid (2013-2018) Hybrid XLE HSD
-- ============================================================
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (191, 'Toyota', 'Avalon', '3rd gen', 2013, 2018, 'modern', 'sedan', 'Japan', '[]', datetime('now'), 'luxury', 'Avalon', 'Hybrid XLE HSD');

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, torque_nm, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (191, 'librarian+analysis', '2.5L I4 HSD hybrid', 2494, 4, 'naturally aspirated', 200, 199, 'port injection', 'e-CVT planetary', 0, 'FWD', 1620, 1);

INSERT INTO reliability (car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (191, 'librarian+analysis', 85.7,
  '["rear_brake_caliper","hybrid_battery_fan"]',
  '["2.5L HSD proven across Prius and Camry Hybrid", "Rear brake caliper freeze at 40K ($700)", "Hybrid battery fan filter needs cleaning"]',
  88, 92, 82, 80, 82,
  '["HSD bulletproof", "eCVT planetary indestructible", "40 mpg sleeper"]');

INSERT INTO build_quality (car_id, source, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging)
VALUES (191, 'librarian+analysis', 76.2, 76, 81, 76, 72, 78, 76);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (191, 'librarian+analysis', 35000, 'USD', 39, 40, 450);

-- ============================================================
-- Car 192: Toyota Sienna V6 (2011-2020) XLE V6 2GR-FE AWD
-- ============================================================
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (192, 'Toyota', 'Sienna', '3rd gen', 2011, 2020, 'modern', 'minivan', 'Japan', '[]', datetime('now'), 'family', 'Sienna', 'XLE V6 2GR-FE AWD');

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, torque_nm, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (192, 'librarian+analysis', '3.5L V6 2GR-FE/FKS', 3456, 6, 'naturally aspirated', 296, 353, 'port injection', '6-speed automatic', 6, 'AWD', 1960, 0);

INSERT INTO reliability (car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (192, 'librarian+analysis', 83.4,
  '["vvt_oil_line","sliding_door_latch","rear_tire_wear"]',
  '["2GR-FE same as Camry/Lexus. Rubber VVT line recalled. 8-speed (2017+) jerky at low speed. Sliding door latch recall 2011-2016. AWD rear tire wear."] ',
  89, 83, 80, 76, 85,
  '["2GR-FE parts everywhere", "6-speed better than 8-speed", "AWD available"]');

INSERT INTO build_quality (car_id, source, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging)
VALUES (192, 'librarian+analysis', 74.6, 76, 78, 74, 72, 74, 74);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (192, 'librarian+analysis', 37000, 'USD', 16, 22, 500);

-- ============================================================
-- Car 193: Toyota Sienna Hybrid (2021+) XLE Hybrid AWD
-- ============================================================
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (193, 'Toyota', 'Sienna', '4th gen', 2021, NULL, 'modern', 'minivan', 'Japan', '[]', datetime('now'), 'family', 'Sienna', 'XLE Hybrid AWD');

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, torque_nm, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (193, 'librarian+analysis', '2.5L I4 A25A-FXS hybrid', 2487, 4, 'naturally aspirated', 245, 176, 'port injection', 'e-CVT planetary', 0, 'AWD', 2010, 1);

INSERT INTO reliability (car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (193, 'librarian+analysis', 84.6,
  '["sliding_door_sensor","3rd_row_bolt_recall"]',
  '["HSD proven track record. Hybrid system is last thing to worry about per owners. 3rd-row seatback bolt recall. Sliding door sensor issues."] ',
  88, 92, 80, 80, 78,
  '["Best hybrid minivan", "eCVT bulletproof", "HSD 150k+ mi battery life"]');

INSERT INTO build_quality (car_id, source, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging)
VALUES (193, 'librarian+analysis', 75.3, 76, 78, 76, 72, 75, 75);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (193, 'librarian+analysis', 41000, 'USD', 36, 36, 500);

-- ============================================================
-- Car 194: Honda Odyssey (2018-2024) EX-L J35Y6 VCM
-- ============================================================
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (194, 'Honda', 'Odyssey', '5th gen', 2018, 2024, 'modern', 'minivan', 'Japan/USA', '[]', datetime('now'), 'family', 'Odyssey', 'EX-L J35Y6 VCM');

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, torque_nm, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (194, 'librarian+analysis', '3.5L V6 J35Y6 VCM', 3471, 6, 'naturally aspirated', 280, 355, 'direct injection', '10-speed automatic', 10, 'FWD', 1950, 0);

INSERT INTO reliability (car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (194, 'librarian+analysis', 76.2,
  '["vcm_oil_consumption","vcm_mount_failure","sliding_door_actuator","infotainment_freeze"]',
  '["VCM causes oil consumption and mount failure. VCMuzzler II $130 prevents. 9-speed (2018-19) problematic. 10-speed (2020+) much better. Sliding door actuators $300-600."] ',
  79, 73, 78, 70, 80,
  '["VCM is the Achilles heel", "10-speed much better than 9-speed", "VCMuzzler mandatory"]');

INSERT INTO build_quality (car_id, source, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging)
VALUES (194, 'librarian+analysis', 71.3, 74, 76, 70, 70, 68, 70);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (194, 'librarian+analysis', 38000, 'USD', 19, 28, 550);

-- ============================================================
-- Car 195: Chrysler Pacifica (2017-2023) Touring L Pentastar V6
-- ============================================================
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (195, 'Chrysler', 'Pacifica', '1st gen', 2017, 2023, 'modern', 'minivan', 'USA/Canada', '[]', datetime('now'), 'family', 'Pacifica', 'Touring L Pentastar V6');

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, torque_nm, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (195, 'librarian+analysis', '3.6L V6 Pentastar Gen3', 3604, 6, 'naturally aspirated', 287, 352, 'port injection', '9-speed automatic ZF 948TE', 9, 'FWD', 1930, 0);

INSERT INTO reliability (car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (195, 'librarian+analysis', 70.3,
  '["plastic_oil_cooler","zf_9speed_valve_body","rocker_arm_failure","head_gasket"]',
  '["Plastic oil cooler cracks at 60-100K ($1000-1500, aluminum aftermarket $300). ZF 9-speed rough shifts valve body. Rocker arm failures. Head gasket rear head."] ',
  72, 65, 72, 68, 75,
  '["ZF 9-speed is the problem", "Plastic oil cooler must be replaced", "Pentastar itself decent if maintained"]');

INSERT INTO build_quality (car_id, source, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging)
VALUES (195, 'librarian+analysis', 69.5, 70, 74, 72, 68, 65, 68);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (195, 'librarian+analysis', 35000, 'USD', 17, 25, 650);

-- ============================================================
-- Car 196: Chrysler Pacifica Hybrid PHEV (2017-2023) PHEV Hybrid
-- ============================================================
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (196, 'Chrysler', 'Pacifica', '1st gen', 2017, 2023, 'modern', 'minivan', 'USA/Canada', '[]', datetime('now'), 'family', 'Pacifica', 'PHEV Hybrid');

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, torque_nm, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (196, 'librarian+analysis', '3.6L V6 Pentastar + dual electric motors', 3604, 6, 'naturally aspirated', 260, 304, 'port injection', 'eFlite hybrid single-clutch', 0, 'FWD', 2120, 1);

INSERT INTO reliability (car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (196, 'librarian+analysis', 66.8,
  '["phev_battery_failure","eflite_transmission","charging_system","plastic_oil_cooler"]',
  '["PHEV battery replacement $7000-17000. 8yr/100k warranty only. eFlite transmission more failure-prone than Toyota eCVT. HV battery bricked failures at under 9K miles. Gas Pacifica is smarter buy."] ',
  74, 62, 72, 60, 65,
  '["PHEV battery cost is existential risk", "eFlite not Toyota eCVT", "Avoid unless under warranty"]');

INSERT INTO build_quality (car_id, source, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging)
VALUES (196, 'librarian+analysis', 68.7, 70, 74, 72, 68, 60, 68);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (196, 'librarian+analysis', 43000, 'USD', 30, 31, 800);

-- ============================================================
-- Car 197: Kia Carnival (2022+) EX 3.5L V6
-- ============================================================
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (197, 'Kia', 'Carnival', '1st gen', 2022, NULL, 'modern', 'minivan', 'South Korea', '[]', datetime('now'), 'family', 'Carnival', 'EX 3.5L V6');

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, torque_nm, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (197, 'librarian+analysis', '3.5L V6 Smartstream G6DC', 3497, 6, 'naturally aspirated', 290, 355, 'dual MPi+GDi', '8-speed automatic', 8, 'FWD', 1920, 0);

INSERT INTO reliability (car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (197, 'librarian+analysis', 76.6,
  '["coolant_loss","infotainment_clip","5_recalls_2022"]',
  '["Lambda II 3.5L Smartstream generally good. Coolant loss emerging pattern. 5 NHTSA recalls on 2022. Too new for 200K+ data. Not the problematic 3.3L Lambda II under investigation."] ',
  80, 78, 74, 72, 76,
  '["Too new for definitive judgment", "Lambda II 3.5L cleaner than 3.3L", "Kia 10yr/100k powertrain warranty"]');

INSERT INTO build_quality (car_id, source, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging)
VALUES (197, 'librarian+analysis', 73.4, 74, 76, 76, 72, 70, 72);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (197, 'librarian+analysis', 34000, 'USD', 18, 26, 550);

-- ============================================================
-- Car 198: Toyota 4Runner (2010-2024) SR5 4WD 1GR-FE
-- ============================================================
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (198, 'Toyota', '4Runner', '5th gen', 2010, 2024, 'modern', 'SUV', 'Japan', '[]', datetime('now'), 'adventure', '4Runner', 'SR5 4WD 1GR-FE');

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, torque_nm, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (198, 'librarian+analysis', '4.0L V6 1GR-FE', 3956, 6, 'naturally aspirated', 270, 377, 'port injection', '5-speed automatic', 5, '4WD', 2100, 0);

INSERT INTO reliability (car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (198, 'librarian+analysis', 85.8,
  '["rear_axle_seal","lower_ball_joints","frame_rust"]',
  '["1GR-FE 4.0L is bulletproof. 300K+ miles routine. Rear axle seal leaks contaminate brakes. Lower ball joints catastrophic if fail - replace at 100K. Frame rust on salt belt cars."] ',
  90, 88, 80, 82, 85,
  '["1GR-FE truck legend", "5-speed simple and strong", "Body-on-frame durability", "300K+ miles proven"]');

INSERT INTO build_quality (car_id, source, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging)
VALUES (198, 'librarian+analysis', 74.5, 78, 70, 72, 70, 82, 72);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (198, 'librarian+analysis', 39000, 'USD', 16, 19, 550);

-- ============================================================
-- Car 199: Lexus RX350 (2010-2015) RX350 2GR-FE
-- ============================================================
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (199, 'Lexus', 'RX350', '3rd gen', 2010, 2015, 'modern', 'SUV', 'Japan/Canada', '[]', datetime('now'), 'luxury', 'RX', 'RX350 2GR-FE');

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, torque_nm, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (199, 'librarian+analysis', '3.5L V6 2GR-FE', 3456, 6, 'naturally aspirated', 270, 336, 'port injection', '6-speed automatic', 6, 'FWD/AWD', 1955, 0);

INSERT INTO reliability (car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (199, 'librarian+analysis', 85.2,
  '["melting_dashboard","vvt_oil_control_valve","oil_leaks","nav_bluetooth_glitches"]',
  '["2GR-FE same as Camry V6/Avalon. Sticky/melting dashboard 2010-2015 infamous. VVT oil control valve P0014/P0012. Navigation/radio/BT aging. Best-selling luxury SUV = massive parts availability."] ',
  92, 86, 82, 76, 85,
  '["2GR-FE benchmark", "Melting dash is cosmetic but expensive ($1500-2500)", "Best-selling luxury SUV parts availability"]');

INSERT INTO build_quality (car_id, source, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging)
VALUES (199, 'librarian+analysis', 78.1, 80, 84, 82, 76, 74, 72);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (199, 'librarian+analysis', 42000, 'USD', 18, 24, 550);

-- ============================================================
-- Car 200: Toyota Tundra (2014-2021) SR5 5.7L V8 4x4
-- ============================================================
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (200, 'Toyota', 'Tundra', '2nd gen', 2014, 2021, 'modern', 'truck', 'USA', '[]', datetime('now'), 'utility', 'Tundra', 'SR5 5.7L V8 4x4');

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, torque_nm, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (200, 'librarian+analysis', '5.7L V8 3UR-FE', 5663, 8, 'naturally aspirated', 381, 544, 'port injection', '6-speed automatic', 6, '4WD', 2270, 0);

INSERT INTO reliability (car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (200, 'librarian+analysis', 85.5,
  '["air_injection_pump","water_pump","lower_ball_joints"]',
  '["3UR-FE 5.7L V8 is legendary. 400K+ miles documented. AIR pump P0410 at 60-100K ($2500 dealer, $200 bypass kit). Water pump 60-100K ($400-800). Lower ball joints."] ',
  91, 88, 80, 78, 85,
  '["3UR-FE truck legend", "400K+ miles proven", "AIR pump bypass recommended", "5.7L V8 last of the NA truck engines"]');

INSERT INTO build_quality (car_id, source, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging)
VALUES (200, 'librarian+analysis', 75.1, 78, 72, 74, 72, 78, 74);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (200, 'librarian+analysis', 36000, 'USD', 13, 17, 550);

-- ============================================================
-- Car 201: Honda Fit (2015-2020) Sport L15B1
-- ============================================================
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (201, 'Honda', 'Fit', 'GK 3rd gen', 2015, 2020, 'modern', 'hatchback', 'Japan/Mexico', '[]', datetime('now'), 'commuter', 'Fit', 'Sport L15B1');

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, torque_nm, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid)
VALUES (201, 'librarian+analysis', '1.5L I4 L15B1 Earth Dreams', 1496, 4, 'naturally aspirated', 130, 155, 'direct injection', 'CVT', 0, 'FWD', 1140, 0);

INSERT INTO reliability (car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (201, 'librarian+analysis', 77.4,
  '["carbon_buildup","fuel_injector_failure","vtc_actuator_rattle","cvt_whine_2015"]',
  '["Direct injection carbon buildup on intake valves (walnut blast $400-800). Fuel injector failures. VTC actuator rattle at startup. 2015 CVT whining failures. Head replacement at 38K documented."] ',
  78, 75, 76, 78, 80,
  '["DI carbon is the main issue", "2015 CVT avoid", "2017+ improved", "Discontinued US 2020"]');

INSERT INTO build_quality (car_id, source, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging)
VALUES (201, 'librarian+analysis', 69.9, 72, 68, 68, 66, 76, 68);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (201, 'librarian+analysis', 17000, 'USD', 29, 36, 400);

COMMIT;

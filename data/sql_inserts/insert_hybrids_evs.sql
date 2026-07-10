-- Insert 20 hybrid/EV/PHEV entries
-- Car IDs: 374-393 (MAX(id) was 373)
-- powertrain_ice ids: 411-430, reliability ids: 506-525,
-- build_quality ids: 363-382, cost_to_own ids: 267-286

PRAGMA foreign_keys = OFF;
BEGIN TRANSACTION;

-- ============ 1. Toyota Prius Gen 2 (2004-2009) ============
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (374, 'Toyota', 'Prius', 'Gen 2 (XW20)', 2004, 2009, 'modern', 'hatchback', 'Japan', '[]', datetime('now'), 'eco', 'Prius', '1.5L HSD NiMH');
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, horsepower_bhp, transmission_type, drivetrain, curb_weight_kg, is_hybrid)
VALUES (411, 374, 'librarian+analysis', '1.5L I4 1NZ-FXE Atkinson HSD', 110, 'e-CVT planetary', 'FWD', 1295, 1);
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (506, 374, 'librarian+analysis', 80.5, '["HV battery fan clogging","inverter coolant pump failure","brake actuator accumulator leak"]', '["NiMH battery gradual capacity loss","multifunction display fade"]', 80, 90, 80, 80, 70, 'null');
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging, source)
VALUES (363, 374, 61.7, 70, 60, 60, 50, 80, 50, 'librarian+analysis');
INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (267, 374, 'librarian+analysis', 22000, 'USD', 48, 45, 400);

-- ============ 2. Toyota Prius Gen 3 (2010-2015) ============
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (375, 'Toyota', 'Prius', 'Gen 3 (XW30)', 2010, 2015, 'modern', 'hatchback', 'Japan', '[]', datetime('now'), 'eco', 'Prius', '1.8L HSD NiMH');
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, horsepower_bhp, transmission_type, drivetrain, curb_weight_kg, is_hybrid)
VALUES (412, 375, 'librarian+analysis', '1.8L I4 2ZR-FXE Atkinson HSD', 134, 'e-CVT planetary', 'FWD', 1380, 1);
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (507, 375, 'librarian+analysis', 72.0, '["EGR cooler clogging","head gasket failure","inverter coolant pump failure"]', '["Oil consumption at 100-200k mi","intake manifold carbon buildup"]', 60, 90, 80, 80, 60, '{"engine":"EGR/head gasket issue at 100-200K mi"}');
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging, source)
VALUES (364, 375, 63.3, 70, 70, 70, 50, 70, 50, 'librarian+analysis');
INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (268, 375, 'librarian+analysis', 24000, 'USD', 51, 48, 450);

-- ============ 3. Toyota Prius Gen 4 (2016-2022) ============
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (376, 'Toyota', 'Prius', 'Gen 4 (XW50)', 2016, 2022, 'modern', 'hatchback', 'Japan', '[]', datetime('now'), 'eco', 'Prius', '1.8L HSD Li-ion');
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, horsepower_bhp, transmission_type, drivetrain, curb_weight_kg, is_hybrid)
VALUES (413, 376, 'librarian+analysis', '1.8L I4 2ZR-FXE Atkinson HSD', 121, 'e-CVT planetary', 'FWD', 1420, 1);
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (508, 376, 'librarian+analysis', 82.5, '["brake actuator noise","rear brake caliper seizure"]', '["Li-ion battery mild degradation"]', 90, 90, 80, 80, 70, 'null');
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging, source)
VALUES (365, 376, 71.7, 70, 80, 70, 60, 80, 60, 'librarian+analysis');
INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (269, 376, 'librarian+analysis', 25000, 'USD', 54, 50, 400);

-- ============ 4. Honda Insight Gen 2 (2010-2014) ============
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (377, 'Honda', 'Insight', 'Gen 2', 2010, 2014, 'modern', 'hatchback', 'Japan', '[]', datetime('now'), 'eco', 'Insight', '1.3L IMA NiMH');
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, horsepower_bhp, transmission_type, drivetrain, curb_weight_kg, is_hybrid)
VALUES (414, 377, 'librarian+analysis', '1.3L I4 LDA2 i-VTEC IMA', 98, 'CVT', 'FWD', 1220, 1);
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (509, 377, 'librarian+analysis', 59.5, '["IMA battery degradation","CVT shudder","LDA bearing failure"]', '["Battery replacement cost","low power"]', 70, 50, 70, 60, 60, 'null');
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging, source)
VALUES (366, 377, 52.0, 60, 60, 50, 50, 60, 40, 'librarian+analysis');
INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (270, 377, 'librarian+analysis', 20000, 'USD', 41, 44, 500);

-- ============ 5. Honda Civic Hybrid (2003-2011) ============
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (378, 'Honda', 'Civic Hybrid', '', 2003, 2011, 'modern', 'sedan', 'Japan', '[]', datetime('now'), 'eco', 'Civic', '1.3L IMA NiMH CVT');
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, horsepower_bhp, transmission_type, drivetrain, curb_weight_kg, is_hybrid)
VALUES (415, 378, 'librarian+analysis', '1.3L I4 LDA2 i-VTEC IMA', 110, 'CVT', 'FWD', 1250, 1);
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (510, 378, 'librarian+analysis', 50.0, '["IMA battery failure","CVT judder","LDA engine stator burn"]', '["Class action IMA battery","premature battery failure"]', 70, 30, 70, 50, 50, 'null');
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging, source)
VALUES (367, 378, 51.7, 60, 60, 50, 50, 50, 40, 'librarian+analysis');
INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (271, 378, 'librarian+analysis', 20000, 'USD', 44, 45, 600);

-- ============ 6. Ford Fusion Hybrid (2010-2012) ============
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (379, 'Ford', 'Fusion Hybrid', '', 2010, 2012, 'modern', 'sedan', 'USA', '[]', datetime('now'), 'eco', 'Fusion', '2.5L eCVT licensed');
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, horsepower_bhp, transmission_type, drivetrain, curb_weight_kg, is_hybrid)
VALUES (416, 379, 'librarian+analysis', '2.5L I4 Atkinson HSD (Toyota-licensed eCVT)', 191, 'e-CVT planetary (Toyota-licensed)', 'FWD', 1610, 1);
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (511, 379, 'librarian+analysis', 74.5, '["coolant pump failure","evaporative canister","steering rack"]', '["eCVT licensed from Toyota - reliable"]', 80, 90, 70, 60, 60, 'null');
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging, source)
VALUES (368, 379, 56.7, 60, 60, 60, 50, 60, 50, 'librarian+analysis');
INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (272, 379, 'librarian+analysis', 28000, 'USD', 41, 36, 500);

-- ============ 7. Chevy Volt Gen 1 (2011-2015) ============
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (380, 'Chevrolet', 'Volt', 'Gen 1', 2011, 2015, 'modern', 'hatchback', 'USA', '[]', datetime('now'), 'eco', 'Volt', '1.4L Voltec PHEV');
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, horsepower_bhp, transmission_type, drivetrain, curb_weight_kg, is_hybrid)
VALUES (417, 380, 'librarian+analysis', '1.4L I4 + dual electric motors Voltec', 149, 'Voltec planetary (no traditional transmission)', 'FWD', 1615, 1);
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (512, 380, 'librarian+analysis', 73.5, '["battery cell balancing","BECM software issues","charge port"]', '["Voltec drivetrain complexity"]', 80, 90, 70, 70, 50, 'null');
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging, source)
VALUES (369, 380, 66.7, 70, 70, 70, 60, 70, 60, 'librarian+analysis');
INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (273, 380, 'librarian+analysis', 40000, 'USD', 42, 42, 500);

-- ============ 8. Nissan Leaf Gen 1 (2011-2017) ============
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (381, 'Nissan', 'Leaf', 'Gen 1 (ZE0)', 2011, 2017, 'modern', 'hatchback', 'Japan', '[]', datetime('now'), 'eco', 'Leaf', '24-30 kWh air-cooled BEV');
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, horsepower_bhp, transmission_type, drivetrain, curb_weight_kg, is_hybrid)
VALUES (418, 381, 'librarian+analysis', '80-110 kW electric motor (air-cooled battery)', 107, 'single-speed reduction gear', 'FWD', 1520, 1);
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (513, 381, 'librarian+analysis', 71.0, '["battery capacity loss in hot climates","PDM converter failure","3G telematics obsolete"]', '["No thermal management","rapid degradation in heat","no active battery cooling"]', 90, 90, 70, 60, 40, '{"electronics":"battery degradation risk"}');
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging, source)
VALUES (370, 381, 51.7, 60, 50, 60, 50, 40, 50, 'librarian+analysis');
INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (274, 381, 'librarian+analysis', 33000, 'USD', 0, 0, 400);

-- ============ 9. Chevy Volt Gen 2 (2016-2019) ============
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (382, 'Chevrolet', 'Volt', 'Gen 2', 2016, 2019, 'modern', 'hatchback', 'USA', '[]', datetime('now'), 'eco', 'Volt', '1.5L Voltec II PHEV');
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, horsepower_bhp, transmission_type, drivetrain, curb_weight_kg, is_hybrid)
VALUES (419, 382, 'librarian+analysis', '1.5L I4 + dual motors Voltec II', 149, 'Voltec II planetary', 'FWD', 1607, 1);
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (514, 382, 'librarian+analysis', 70.0, '["BECM recall","charge port","high voltage cable"]', '["Voltec II complexity"]', 90, 90, 80, 50, 40, 'null');
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging, source)
VALUES (371, 382, 68.3, 70, 70, 70, 70, 70, 60, 'librarian+analysis');
INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (275, 382, 'librarian+analysis', 34000, 'USD', 42, 42, 500);

-- ============ 10. Honda Accord Hybrid (2018+) ============
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (383, 'Honda', 'Accord Hybrid', '10th gen+', 2018, NULL, 'modern', 'sedan', 'Japan', '[]', datetime('now'), 'eco', 'Accord', '2.0L i-MMD Hybrid');
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, horsepower_bhp, transmission_type, drivetrain, curb_weight_kg, is_hybrid)
VALUES (420, 383, 'librarian+analysis', '2.0L I4 Atkinson i-MMD two-motor', 212, 'e-CVT (no transmission, direct drive)', 'FWD', 1560, 1);
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (515, 383, 'librarian+analysis', 78.5, '["AC compressor","12V battery"]', '["i-MMD reliable"]', 90, 90, 80, 70, 60, 'null');
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging, source)
VALUES (372, 383, 76.7, 80, 80, 80, 70, 70, 70, 'librarian+analysis');
INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (276, 383, 'librarian+analysis', 30000, 'USD', 48, 47, 500);

-- ============ 11. Chevy Bolt (2017-2023) ============
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (384, 'Chevrolet', 'Bolt', '', 2017, 2023, 'modern', 'hatchback', 'USA', '[]', datetime('now'), 'eco', 'Bolt', '60-65 kWh BEV (LG cells)');
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, horsepower_bhp, transmission_type, drivetrain, curb_weight_kg, is_hybrid)
VALUES (421, 384, 'librarian+analysis', '150 kW electric motor (liquid-cooled LG battery)', 200, 'single-speed reduction gear', 'FWD', 1625, 1);
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (516, 384, 'librarian+analysis', 73.0, '["LG cell fire recall","battery replacement","HV cable"]', '["Cell defect recall 2020-22"]', 90, 90, 70, 60, 40, 'null');
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging, source)
VALUES (373, 384, 60.0, 70, 60, 60, 60, 50, 60, 'librarian+analysis');
INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (277, 384, 'librarian+analysis', 30000, 'USD', 0, 0, 500);

-- ============ 12. BMW i3 (2014-2021) ============
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (385, 'BMW', 'i3', '', 2014, 2021, 'modern', 'hatchback', 'Germany', '[]', datetime('now'), 'eco', 'i3', '22-42 kWh BEV/REx CFRP');
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, horsepower_bhp, transmission_type, drivetrain, curb_weight_kg, is_hybrid)
VALUES (422, 385, 'librarian+analysis', '125 kW rear motor (CFRP body, liquid-cooled battery)', 168, 'single-speed reduction gear', 'RWD', 1345, 1);
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (517, 385, 'librarian+analysis', 70.0, '["small battery capacity","CFRP repair cost","REx maintenance"]', '["Expensive body repair","software bugs"]', 90, 90, 80, 60, 30, 'null');
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging, source)
VALUES (374, 385, 66.7, 90, 70, 60, 50, 60, 40, 'librarian+analysis');
INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (278, 385, 'librarian+analysis', 45000, 'USD', 0, 0, 800);

-- ============ 13. Hyundai Ioniq (2017-2021) ============
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (386, 'Hyundai', 'Ioniq', '', 2017, 2021, 'modern', 'hatchback', 'South Korea', '[]', datetime('now'), 'eco', 'Ioniq', '1.6L Hybrid 6DCT');
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, horsepower_bhp, transmission_type, drivetrain, curb_weight_kg, is_hybrid)
VALUES (423, 386, 'librarian+analysis', '1.6L I4 Atkinson + 32kW motor + 6-speed DCT', 139, '6-speed DCT', 'FWD', 1380, 1);
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (518, 386, 'librarian+analysis', 68.5, '["6DCT clutch","12V battery"]', '["DCT jerky at low speed"]', 80, 70, 70, 60, 60, 'null');
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging, source)
VALUES (375, 386, 64.0, 70, 70, 60, 60, 60, 60, 'librarian+analysis');
INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (279, 386, 'librarian+analysis', 23000, 'USD', 57, 59, 500);

-- ============ 14. Kia Niro HEV (2017-2022) ============
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (387, 'Kia', 'Niro', 'Gen 1', 2017, 2022, 'modern', 'SUV', 'South Korea', '[]', datetime('now'), 'eco', 'Niro', '1.6L Hybrid 6DCT');
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, horsepower_bhp, transmission_type, drivetrain, curb_weight_kg, is_hybrid)
VALUES (424, 387, 'librarian+analysis', '1.6L I4 Atkinson + 32kW motor + 6-speed DCT', 139, '6-speed DCT', 'FWD', 1430, 1);
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (519, 387, 'librarian+analysis', 73.5, '["6DCT clutch","hybrid clutch"]', '["DCT low speed hesitation"]', 80, 70, 80, 70, 70, 'null');
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging, source)
VALUES (376, 387, 67.0, 80, 70, 70, 60, 60, 60, 'librarian+analysis');
INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (280, 387, 'librarian+analysis', 24000, 'USD', 50, 49, 500);

-- ============ 15. Ford Mustang Mach-E (2021+) ============
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (388, 'Ford', 'Mustang Mach-E', '', 2021, NULL, 'modern', 'SUV', 'USA', '[]', datetime('now'), 'ev', 'Mustang Mach-E', '68-88 kWh AWD');
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, horsepower_bhp, transmission_type, drivetrain, curb_weight_kg, is_hybrid)
VALUES (425, 388, 'librarian+analysis', 'dual motor AWD (liquid-cooled NCM battery)', 346, 'single-speed reduction gear', 'AWD', 2100, 1);
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (520, 388, 'librarian+analysis', 70.0, '["HV junction box","contactors","software OTA issues"]', '["Software quality","Mustang name controversy"]', 90, 90, 70, 50, 40, 'null');
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging, source)
VALUES (377, 388, 66.7, 70, 70, 80, 60, 60, 60, 'librarian+analysis');
INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (281, 388, 'librarian+analysis', 43000, 'USD', 0, 0, 700);

-- ============ 16. Hyundai Ioniq 5 (2022+) ============
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (389, 'Hyundai', 'Ioniq 5', '', 2022, NULL, 'modern', 'SUV', 'South Korea', '[]', datetime('now'), 'ev', 'Ioniq 5', '77.4 kWh AWD 800V');
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, horsepower_bhp, transmission_type, drivetrain, curb_weight_kg, is_hybrid)
VALUES (426, 389, 'librarian+analysis', 'dual motor AWD 800V (liquid-cooled battery)', 320, 'single-speed reduction gear', 'AWD', 2050, 1);
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (521, 389, 'librarian+analysis', 70.0, '["ICCU failure","charge port"]', '["ICCU recall","software bugs"]', 90, 90, 80, 50, 40, 'null');
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging, source)
VALUES (378, 389, 68.3, 80, 60, 80, 70, 50, 60, 'librarian+analysis');
INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (282, 389, 'librarian+analysis', 45000, 'USD', 0, 0, 600);

-- ============ 17. Kia EV6 (2022+) ============
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (390, 'Kia', 'EV6', '', 2022, NULL, 'modern', 'SUV', 'South Korea', '[]', datetime('now'), 'ev', 'EV6', '77.4 kWh AWD 800V');
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, horsepower_bhp, transmission_type, drivetrain, curb_weight_kg, is_hybrid)
VALUES (427, 390, 'librarian+analysis', 'dual motor AWD 800V (liquid-cooled battery)', 320, 'single-speed reduction gear', 'AWD', 2020, 1);
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (522, 390, 'librarian+analysis', 70.0, '["ICCU failure","charge port"]', '["ICCU recall","software bugs"]', 90, 90, 80, 50, 40, 'null');
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging, source)
VALUES (379, 390, 68.3, 80, 60, 80, 70, 50, 60, 'librarian+analysis');
INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (283, 390, 'librarian+analysis', 42000, 'USD', 0, 0, 600);

-- ============ 18. Rivian R1T (2022+) ============
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (391, 'Rivian', 'R1T', 'Gen 1', 2022, NULL, 'modern', 'truck', 'USA', '[]', datetime('now'), 'ev', 'R1T', 'Quad-motor 128 kWh');
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, horsepower_bhp, transmission_type, drivetrain, curb_weight_kg, is_hybrid)
VALUES (428, 391, 'librarian+analysis', 'quad motor AWD (liquid-cooled 2170 cells)', 835, 'single-speed per motor', 'AWD', 2630, 1);
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (523, 391, 'librarian+analysis', 60.0, '["front motor bearings","12V battery","software OTA issues"]', '["Early build quality issues","teething problems"]', 90, 90, 70, 40, 30, 'null');
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging, source)
VALUES (380, 391, 51.7, 50, 60, 60, 50, 50, 40, 'librarian+analysis');
INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (284, 391, 'librarian+analysis', 73000, 'USD', 0, 0, 800);

-- ============ 19. Volvo XC90 T8 (2016+) ============
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (392, 'Volvo', 'XC90', 'T8 PHEV', 2016, NULL, 'modern', 'SUV', 'Sweden', '[]', datetime('now'), 'luxury', 'XC90', '2.0T + electric T8 AWD');
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, horsepower_bhp, transmission_type, drivetrain, curb_weight_kg, is_hybrid)
VALUES (429, 392, 'librarian+analysis', '2.0L turbo + supercharger I4 + electric (ERAD rear)', 400, '8-speed automatic', 'AWD', 2180, 1);
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (524, 392, 'librarian+analysis', 65.0, '["ERAD rear motor","software issues","air suspension"]', '["Complex PHEV system"]', 70, 70, 70, 60, 50, 'null');
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging, source)
VALUES (381, 392, 77.5, 80, 80, 85, 75, 65, 70, 'librarian+analysis');
INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (285, 392, 'librarian+analysis', 68000, 'USD', 55, 58, 900);

-- ============ 20. Porsche Cayenne E-Hybrid (2019+) ============
INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, image_paths, created_at, character, family, variant)
VALUES (393, 'Porsche', 'Cayenne', 'E-Hybrid', 2019, NULL, 'modern', 'SUV', 'Germany', '[]', datetime('now'), 'luxury', 'Cayenne', '3.0T V6 PHEV');
INSERT INTO powertrain_ice (id, car_id, source, engine_layout, horsepower_bhp, transmission_type, drivetrain, curb_weight_kg, is_hybrid)
VALUES (430, 393, 'librarian+analysis', '3.0L turbo V6 + electric motor PHEV', 455, '8-speed automatic', 'AWD', 2310, 1);
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (525, 393, 'librarian+analysis', 71.5, '["PDK valve body","charge port","coolant leak"]', '["PHEV complexity","expensive repairs"]', 75, 80, 80, 65, 55, 'null');
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging, source)
VALUES (382, 393, 80.8, 85, 85, 88, 82, 68, 75, 'librarian+analysis');
INSERT INTO cost_to_own (id, car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (286, 393, 'librarian+analysis', 81000, 'USD', 46, 47, 1200);

COMMIT;

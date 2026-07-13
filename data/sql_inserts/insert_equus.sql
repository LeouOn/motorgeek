-- Hyundai Equus 5.0 V8 (2012-2016) — the Korean LS430

INSERT INTO cars (id, make, model, generation, year_start, year_end, era_tag, body_style, country, description, image_paths, created_at, character, family, variant)
VALUES (394, 'Hyundai', 'Equus', 'DH', 2011, 2016, 'modern', 'sedan', 'South Korea',
'Hyundai flagship luxury sedan. predecessor to Genesis G90. Same Tau 5.0L V8 (Wards 10 Best). Port injection (no carbon buildup). Hydraulic lash adjusters (maintenance-free). Pre-2012: ZF 6-speed (excellent). 2012+: Hyundai 8-speed. RWD. Air suspension optional. Extremely deep depreciation — $60K+ new to $8-15K used. Interior quality genuinely premium. Parts availability is the existential risk.',
'[]', datetime('now'), 'luxury', 'Equus', '5.0 V8 Ultimate');

INSERT INTO powertrain_ice (car_id, source, engine_layout, displacement_cc, cylinders, aspiration, horsepower_bhp, torque_nm, fuel_system, transmission_type, gear_count, drivetrain, curb_weight_kg, is_hybrid, engine_code)
VALUES (394, 'librarian+analysis', '5.0L V8 Tau G8BA', 5038.0, 8, 'naturally aspirated', 429.0, 510.0, 'port injection', '8-speed automatic', 8, 'RWD', 2060.0, 0, 'Tau 5.0');

INSERT INTO reliability (car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (394, 'librarian+analysis', 73.0,
'["pvd_piston_rings_oil_consumption_pre2012","parts_backorder_tau_specific","air_suspension_optional","electronics_aging"]',
'["tau_5.0: Same engine as Genesis G90. Wards 10 Best. Port injection = no carbon buildup. Hydraulic lash adjusters = maintenance-free. Roller cam followers superior to tappet-style. Pre-2012 PVD ring oil consumption was supplier defect, fixed late 2012. Forum teardowns pristine at 90K.","zf_6speed: Pre-2012 Equus got ZF 6-speed — excellent, shared with BMW/Audi. 2012+ got Hyundai A8TR1 8-speed — adequate, not as smooth.","parts_availability: CRITICAL. Equus was discontinued. Hyundai sold under 3K/year at peak US volume. 5.0-specific parts frequently backordered. Almost no aftermarket. This is the existential risk — not the engine failing, but not being able to get parts when something peripheral breaks.","air_suspension: Optional. Same family as Genesis/Lexus air systems. Struts $800-1500/corner if available."] ',
80.0, 75.0, 75.0, 68.0, 58.0,
'["engine: Tau 5.0 is objectively Hyundais best engine. Port injected, hydraulic lash, Wards winner. Same as G90. Score matches G90 at 80","transmission: Pre-2012 ZF 6-speed scores higher (~82). 2012+ Hyundai 8-speed adequate but not ZF-tier. Blended score 75","chassis: BH platform is competent. Air suspension optional — if equipped, adds risk. Base coil suspension is simpler and more durable","electronics: Aging 2011-era Hyundai infotainment and modules. Not as bad as German rivals but not Toyota-tier either","ease_of_repair: Parts availability is the killer. Same issue as G90. Low volume + discontinued nameplate = thin supply chain. Independent shops can work on the engine but cant get parts quickly"]');

INSERT INTO build_quality (car_id, source, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging)
VALUES (394, 'librarian+analysis', 73.0, 74.0, 82.0, 84.0, 70.0, 52.0, 58.0);

INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES (394, 'librarian+analysis', 58000.0, 'USD', 15.0, 23.0, 900.0);

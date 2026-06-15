-- Clean up failed partial inserts
DELETE FROM cars WHERE id = 182;
DELETE FROM build_quality WHERE car_id = 182;
DELETE FROM powertrain_ice WHERE car_id = 182;
DELETE FROM cost_to_own WHERE car_id = 182;

-- Add reliability for car_id=181 (W222 facelift S560)
INSERT INTO reliability (car_id, source, reliability_score, common_failures, known_issues, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, score_notes)
VALUES (181, 'librarian+analysis', 68.4,
'["P06DA00_oil_pump_solenoid","cylinder_deactivation_lifters","hot_v_turbo_seals","valve_cover_gasket","airmatic_struts"]',
'["P06DA00: Oil pump solenoid in oil pan. On 4MATIC requires engine+trans removal. 5500-9500. The M176 defining failure","cylinder_deactivation: Lifters for cylinders 2,3,5,8 can fail causing rough idle. Up to 7500","hot_v_turbo: Turbos inside V means heat degradation of oil seals. 3500-5500 per turbo","valve_cover: Front end removal required for gasket service. 1500-3000","airmatic: Same family as pre-facelift but improved. Struts wear at 80-100K"]',
70.0, 78.0, 68.0, 68.0, 55.0,
'["engine: M176 trades M278 cam sensor ECU risk for oil pump solenoid risk. Hot-V adds turbo heat stress. Cylinder deactivation adds lifter complexity","transmission: 9G-Tronic materially better than 7G. Smoother. Fewer conductor plate issues","chassis: AIRMATIC improved but same fundamental wear pattern. MBC improved over pre-facelift","electronics: NTG6 COMAND with CarPlay is genuine usability improvement. Better driver assists. Still 100 ECUs","ease_of_repair: Same aluminum body issue. Oil pump solenoid on 4MATIC is engine+trans removal"]');

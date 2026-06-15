-- Step 1: Update existing W222 (car_id=42) to be explicitly pre-facelift M278 S550
UPDATE cars SET
  year_start = 2014,
  year_end = 2017,
  variant = 'S550 M278 pre-facelift'
WHERE id = 42;

UPDATE powertrain_ice SET
  engine_layout = '4.7L twin-turbo V8 M278',
  displacement_cc = 4663.0,
  cylinders = 8,
  aspiration = 'twin-turbo',
  horsepower_bhp = 449.0,
  torque_nm = 700.0,
  fuel_system = 'direct injection',
  transmission_type = '7G-Tronic 7-speed auto',
  gear_count = 7,
  drivetrain = 'RWD/4MATIC',
  is_hybrid = 0
WHERE car_id = 42;

-- Recalibrate pre-facelift reliability (M278 cam sensor ECU risk, AIRMATIC wear, 100 ECUs)
UPDATE reliability SET
  score_engine = 68.0,
  score_transmission = 72.0,
  score_chassis = 64.0,
  score_electronics = 60.0,
  score_ease_of_repair = 55.0,
  reliability_score = 68.0*0.25 + 72.0*0.25 + 64.0*0.15 + 60.0*0.15 + 55.0*0.20,
  known_issues = '["cam_sensor_oil_wicking: The #1 S550 killer. Oil travels up cam sensor wire harness into ECU causing random misfires and transmission issues.  pigtail fix prevents + ECU death. CHECK FIRST on any used M278","cylinder_scoring: Pre-2015 Silitec liners prone to scoring. NanoSlide coating introduced ~2015. Check compression on cylinders 5/6","timing_chain_tensioner: Pre-Feb 2013 engines lack check valves. 2016 should be past cutoff but verify by engine serial","oil_cooler_leaks: Oil filter housing leaks at 80K+. Oil+coolant mix. -3000. Part of PPI","carbon_buildup: Direct injection carbon on intake valves. Walnut blast at 60K intervals. -1200","airmatic_struts: Air bags crack at 80K+. Arnott rebuilt /corner, dealer . Compressor fails from overwork","magic_body_control: If equipped, hydraulic ABC system. Pump failure -5K. Cannot coil-convert MBC cars"]',
  common_failures = '["cam_sensor_oil_wicking","airmatic_struts","oil_cooler_leaks","7g_conductor_plate","comand_screen_aging","turbo_coolant_lines"]',
  score_notes = '["engine: M278 shares block with M273 but different failure modes. Cam sensor oil wicking is existential risk. Pre-2015 cylinder scoring. Direct injection carbon. Engine score dropped from 72 to 68 for these documented issues","transmission: 7G-Tronic conductor plate failures at 80K+. Rough shifting. 9G in facelift is better","chassis: AIRMATIC struts at 80K+ are a -5K wear item. MBC if equipped is worse. Score dropped from 66 to 64","electronics: ~100 ECUs. COMAND NTG5 ages poorly. No CarPlay on early models. Score dropped from 62 to 60","ease_of_repair: Aluminum hybrid bodyshell requires Mercedes Elite Certified Collision Center (only ~10 in USA). M278 is complex. Already at 55"]'
WHERE car_id = 42;

-- Build quality stays at 78.3 (materials are genuinely excellent, that's not the problem)
-- Q-score unchanged

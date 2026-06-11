-- ============================================================
-- Reliability + Build Quality scores: 14 exotic/EV/misc cars
-- Cars: Alpine A110, Jaguar XJ X351, Range Rover Sport, Peugeot 406 Coupe,
--       Tesla Model 3/S/Y, BYD Han, Hongqi E-HS9, Hyundai Ioniq 5 N,
--       Lamborghini Huracan, Lucid Air, VinFast VF8, Xiaomi SU7 Max
-- Calibration: LS430 Rel=88.5 Q=92.3 (best). Infiniti Q50 Rel=39.6 Q=39.6 (worst).
-- Reliability: 5 dims w/ catastrophe penalty if any < 50
-- Build Quality: 6 dims, weighted, no penalty
-- ============================================================


-- ============================================================
-- 1. RELIABILITY INSERTS (ids 288-301, car_id order)
-- ============================================================

-- Alpine A110 (car_id=15, id=288) — Rel=67.2
-- Mid-engine, 1.8T Nissan MR18DDT (shared with Megane RS). Low-volume, niche.
-- Fuel pump failures, timing chain wear, oil consumption, parts scarcity.
INSERT INTO reliability (id, car_id, source, reliability_score, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (288, 15, 'sample', 67.2, 72, 78, 80, 65, 45,
  '{"Fuel pump sudden failure": 3, "Excessive oil consumption": 2, "Premature timing chain wear": 2, "Brake disc corrosion (standing)": 2, "Sporadic warning lights": 2}',
  850.0, 2,
  'Fair (Renault/Nissan shared engine, but Alpine-specific body parts scarce)',
  'Low',
  '{"MR18DDT 1.8T": "Nissan-sourced turbo four. Same as Megane RS 280/300. Generally reliable if serviced regularly. Oil consumption and timing chain wear are known issues from neglect.", "Getrag 7DCT300": "Dual-clutch, mostly reliable. Some shift hesitation reported.", "Aluminum chassis": "Bonded and riveted aluminum. Lightweight but rear wheel arch corrosion is a known weak spot.", "Fuel pump": "Sudden failure without warning. Root cause unclear (control module overheating suspected). Third-party cooling kit available.", "Niche brand": "Low volume (~20K global). Alpine dealer network thin outside Europe. Parts wait times can be long."}');

-- Jaguar XJ X351 (car_id=46, id=289) — Rel=59.2
-- All-aluminum body, gorgeous car. 5.0L SC V8. Jaguar electronics = caution.
INSERT INTO reliability (id, car_id, source, reliability_score, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (289, 46, 'sample', 59.2, 70, 72, 75, 42, 40,
  '{"5.0L SC timing chain tensioner": 3, "Water pump failure": 2, "Infotainment/can bus failures": 3, "Coolant loss (heater core)": 2, "Air suspension (if equipped)": 3}',
  1400.0, 4,
  'Poor (Jaguar specialist required, many parts dealer-only)',
  'Low',
  '{"5.0L AJ-V8 SC": "Supercharged V8. Timing chain tensioner and water pump are known failure points. Coolant loss from heater core O-rings common.", "ZF 6HP28": "Proven unit but Jaguar-specific tuning. Generally OK at moderate mileage.", "Aluminum body": "Riv-bonded aluminum monocoque. No rust issues. Excellent chassis rigidity.", "Jaguar electronics": "THE weakness. CAN bus gremlins, infotainment crashes, module failures. Ages poorly. Many owners report constant warning lights.", "Air suspension": "Optional but when it fails, expensive. Compressor and air bags at 80-120K miles."}');

-- Range Rover Sport 2nd gen HSE (car_id=55, id=290) — Rel=51.0
-- Legendary electrical issues. Air suspension fails. Supercharged V6 coolant problems.
INSERT INTO reliability (id, car_id, source, reliability_score, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (290, 55, 'sample', 51.0, 62, 68, 55, 38, 35,
  '{"3.0L SC timing chain stretch": 3, "Coolant loss/leak": 3, "Air suspension failure": 3, "Electrical module failures": 3, "Infotainment black screen": 3}',
  1800.0, 6,
  'Poor (expensive parts, dealer specialist required)',
  'Low',
  '{"3.0L SC V6": "Timing chain stretch at 60-100K. Coolant loss from multiple potential sources. Supercharger nose cone bearing whine.", "ZF 8HP": "Proven transmission but stressed in 2.3-ton SUV. Fluid changes critical.", "Air suspension": "The Achilles heel. Compressor fails, air bags leak. $3-5K per corner. Many owners convert to coils.", "Electronics": "Legendary for all the wrong reasons. Screen goes blank, modules fail, warning lights cascade. Terrain Response system adds complexity.", "Cost to own": "Among the most expensive SUVs to maintain. $2-3K/year typical after warranty."}');

-- Peugeot 406 Coupe (car_id=68, id=291) — Rel=71.0
-- Pininfarina design, PSA underpinnings. ES9 V6 or 2.0T. Simple by modern standards.
INSERT INTO reliability (id, car_id, source, reliability_score, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (291, 68, 'sample', 71.0, 78, 72, 75, 68, 60,
  '{"ES9 V6 coil pack failure": 2, "Suspension bush wear": 2, "Climate control servo failure": 1, "Power window regulators": 1, "Age-related trim degradation": 1}',
  500.0, 1,
  'Fair (PSA shared parts, but coupe-specific panels scarce)',
  'Moderate',
  '{"ES9 V6": "3.0L NA V6 (also used in Renault Laguna, Citroen C5). Proven unit. Coil packs are the main failure item.", "4-speed auto / 5-speed manual": "Both proven. Auto is old-school hydraulic, unbreakable but slow. Manual is excellent.", "Pininfarina body": "Built at Pininfarina Italy, not PSA main plant. Higher build quality than standard 406.", "Electronics": "Simple era (late 90s/early 2000s). Few electronic failure points. Analog gauges.", "Aging": "20+ years old now. Rubber components, suspension bushes, trim pieces aging. Parts getting scarce outside Europe."}');

-- Tesla Model 3 Performance (car_id=71, id=292) — Rel=79.9
-- Proven electric drivetrain. Software bugs, panel gaps, but motor/gear are reliable.
INSERT INTO reliability (id, car_id, source, reliability_score, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (292, 71, 'sample', 79.9, 88, 90, 78, 62, 72,
  '{"12V battery replacement (3-4 yr)": 1, "MCU/eMMC wear (pre-2018)": 2, "Phantom braking (Autopilot)": 2, "Suspension control arm (high mileage)": 2, "HV battery connector recall": 2}',
  450.0, 10,
  'Good (Tesla mobile service, OTA updates, growing parts network)',
  'Moderate',
  '{"Electric motor": "Permanent magnet reluctance motor. Very few reported failures. No oil changes, no spark plugs, no timing belt. Revolution counts as reliability.", "Reduction gear": "Single-speed. No gears to shift, no clutches to wear. Essentially a differential. Virtually zero failures reported.", "Software": "Tesla''s strength and weakness. OTA updates fix bugs but also introduce new ones. Phantom braking, Autopilot glitches, MCU reboots.", "Build quality": "Not a reliability issue per se, but panel gaps and paint quality are inconsistent. Improving over model years.", "HV battery": "Degradation is gradual and predictable. 70-80% capacity at 150K+ miles typical. Battery connector recall on early units."}');

-- Tesla Model S Plaid (car_id=70, id=293) — Rel=76.2
-- Tri-motor 1020hp. Drivetrain solid, but software complexity higher than M3.
INSERT INTO reliability (id, car_id, source, reliability_score, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (293, 70, 'sample', 76.2, 85, 88, 75, 58, 65,
  '{"Tri-motor inverter firmware updates": 2, "HV battery heat management (track)": 2, "MCU/infotainment resets": 3, "Air suspension (if equipped)": 2, "Complex electronics diagnostics": 2}',
  700.0, 12,
  'Fair (Tesla service centers, but Plaid-specific parts limited)',
  'Low',
  '{"Tri-motor drivetrain": "Three motors = more complexity but individually proven. Rear motors are the same PM reluctance units as M3. Inverter firmware updates are common.", "Reduction gears": "Three separate gearsets. Proven design, no mechanical failures reported.", "Software complexity": "More systems than M3: active damping, rear steering, Track Mode. More code = more bugs. MCU reboots while driving reported.", "Platform age": "Model S platform dates to 2012. Plaid is heavily updated but some legacy architecture remains.", "Repair costs": "Out-of-warranty Tesla repairs are expensive. Battery replacement $12-20K. Motor replacement $5-10K."}');

-- Tesla Model Y Range (car_id=72, id=294) — Rel=80.5
-- Best-selling EV globally. Proven drivetrain, growing parts ecosystem.
INSERT INTO reliability (id, car_id, source, reliability_score, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (294, 72, 'sample', 80.5, 88, 90, 76, 65, 74,
  '{"12V battery (3-4 yr)": 1, "Suspension clunk (early builds)": 2, "Steering rack vibration": 1, "HV battery connector recall": 2, "Heat pump failure (cold climates)": 2}',
  400.0, 11,
  'Good (most DIY-friendly Tesla, abundant parts)',
  'High',
  '{"Electric motor": "Same proven PM reluctance motor as M3. Highest production volume of any EV drivetrain.", "Reduction gear": "Single-speed, proven. Zero mechanical failures at scale.", "Suspension": "Early 2020-2022 builds had suspension clunk issues. Mostly resolved in later builds.", "Heat pump": "Standard on MY. Some failures in very cold climates. $1K repair.", "DIY": "Most DIY-friendly Tesla. Abundant parts, extensive community knowledge, Munro teardowns available."}');

-- BYD Han EV (car_id=73, id=295) — Rel=72.5
-- Blade Battery LFP (very safe, 2000+ cycles). Large-scale production, limited non-China data.
INSERT INTO reliability (id, car_id, source, reliability_score, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (295, 73, 'sample', 72.5, 80, 82, 75, 65, 55,
  '{"Software updates (over-the-air)": 1, "Charging speed inconsistency": 2, "Infotainment quirks": 1, "Single-phase AC charging limitation": 2, "Suspension calibration (early units)": 1}',
  350.0, 1,
  'Fair in China; Poor outside Asia (limited dealer network)',
  'Low',
  '{"Blade Battery LFP": "BYD''s crown jewel. LFP chemistry = no thermal runaway risk. 2000+ charge cycles claimed, 5000 advertised. 8-year/160K km warranty.", "Electric motor": "BYD manufactures own motors. Proven across millions of vehicles (buses, taxis, passenger cars). 93% of BYDs still within spec at 100K km.", "Reduction gear": "Single-speed, standard EV design. No reported issues.", "Infotainment": "Feels underdeveloped per reviews. Menu navigation inconsistent. Charging performance below claimed 120kW DC.", "Parts/Service": "Excellent in China and expanding markets. Limited or non-existent in most Western markets."}');

-- Hongqi E-HS9 (car_id=75, id=296) — Rel=56.8
-- China-only luxury EV. Unproven long-term. Thin panels, infotainment problems.
INSERT INTO reliability (id, car_id, source, reliability_score, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (296, 75, 'sample', 56.8, 68, 70, 65, 55, 35,
  '{"Infotainment crashes/glitches": 3, "Air suspension issues": 2, "Electronic module failures": 2, "Strange cabin noises": 2, "Unproven long-term durability": 3}',
  600.0, 0,
  'Poor (limited dealer network, mainly Middle East and China)',
  'Low',
  '{"Electric motor": "Dual-motor setup. Limited long-term data. No catastrophic failure reports yet but very small sample size.", "Air suspension": "Standard equipment. Smooth ride but repair costs unknown at high mileage.", "Electronics": "Infotainment system widely criticized as buggy and unfinished. Multiple owner reports of system crashes.", "Build quality": "Thin metal panels (hood flexes with finger push). Interior materials look premium but feel synthetic.", "Service": "Almost no service network outside China and Middle East. Parts availability essentially zero in Western markets."}');

-- Hyundai Ioniq 5 N (car_id=115, id=297) — Rel=75.8
-- E-GMP platform. Performance-tuned. ICCU failures on base cars, N-specific brake recall.
INSERT INTO reliability (id, car_id, source, reliability_score, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (297, 115, 'sample', 75.8, 82, 84, 78, 60, 68,
  '{"ICCU charging failure (shared E-GMP issue)": 3, "12V battery drain": 2, "N-specific brake software recall": 3, "Software/driver-assist glitches": 1, "Tire wear (performance rubber)": 1}',
  500.0, 3,
  'Good (Hyundai dealer network, 10-year powertrain warranty)',
  'Moderate',
  '{"E-GMP motor": "Proven platform shared with EV6, Ioniq 5, Genesis GV60. Motor failures are rare.", "Reduction gear": "Standard E-GMP unit. N-tuned for faster response but mechanically proven.", "ICCU": "The known E-GMP issue. Integrated Charging Control Unit can fail, disabling DC/AC charging. Mostly pre-2023 cars. Fixed in later production.", "N brake software": "Performance models had a recall for left-foot braking logic that could reduce stopping effectiveness. Software fix.", "Warranty": "Hyundai 10-year/100K powertrain + 8-year EV component warranty. Strong safety net."}');

-- Lamborghini Huracan LP 580-2 (car_id=116, id=298) — Rel=62.5
-- NA V10 (Audi R8 shared). Hand-built excellence but astronomical maintenance costs.
INSERT INTO reliability (id, car_id, source, reliability_score, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (298, 116, 'sample', 62.5, 80, 82, 85, 62, 25,
  '{"Front lift system failure": 2, "MagneRide damper failure (high mileage)": 2, "Battery drain (low use)": 1, "Carbon ceramic brake replacement cost": 3, "E-gear actuator (high mileage)": 2}',
  3500.0, 1,
  'Poor (Lamborghini dealer only, parts expensive and sometimes backordered)',
  'None',
  '{"5.2L NA V10": "Hand-assembled at Sant''Agata. Shared architecture with Audi R8. Naturally aspirated = no turbos to fail. Proven robust at high mileage.", "LDF 7-speed DCT": "Audi-derived dual-clutch. Excellent reliability. E-gear actuator can need service at high mileage.", "Carbon-aluminum hybrid chassis": "Incredibly rigid. No structural issues reported. aerospace-grade construction.", "Electronics": "Complex when they fail: MagneRide sensors, front lift system, ECU. Expensive diagnostics. Lamborghini-specific tools required.", "Cost of ownership": "Oil change $800+. Brake job $5-10K (carbon ceramics). Annual service $3-5K. Front lift system $4K+. This is the real reliability penalty."}');

-- Lucid Air Touring (car_id=124, id=299) — Rel=64.0
-- Brilliant hardware, software startup problems. Multiple recalls on harness/routing.
INSERT INTO reliability (id, car_id, source, reliability_score, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (299, 124, 'sample', 64.0, 78, 80, 75, 48, 40,
  '{"Infotainment/screen freezes and reboots": 3, "Rear subframe wiring harness (recall)": 3, "Rear camera display failure (recall)": 2, "Half-shaft bolts (recall)": 3, "Driver-assist faults (adaptive cruise)": 2}',
  900.0, 5,
  'Poor (limited service network, startup growing pains)',
  'Low',
  '{"Motor/drivetrain": "Lucid miniaturized in-house motor design. Very efficient. Catastrophic motor failures are rare.", "Reduction gear": "Proven, no issues reported.", "Wiring harness recall": "2024-2025 Pure RWD models. Harness too short, strains connection, causes power loss. Recall fix is replacement.", "Software": "The Achilles heel. Screen freezes, driver-assist dropouts, CarPlay glitches, lost settings. Multiple OTA updates but still buggy.", "Service network": "Small and variable. Mobile service available in some areas. Some owners report long waits and repeat visits."}');

-- VinFast VF8 (car_id=76, id=300) — Rel=41.9
-- Worst production EV tested. Software disaster, hardware QC failures, unresponsive service.
INSERT INTO reliability (id, car_id, source, reliability_score, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (300, 76, 'sample', 41.9, 55, 58, 50, 30, 25,
  '{"Vehicle unresponsive (stranded)": 3, "Software crashes (infotainment, gear selector)": 3, "Lane assist malfunction (pulls wrong direction)": 3, "Rolling backward on incline": 3, "Climate control malfunction (cold air when off)": 2}',
  700.0, 2,
  'Very Poor (tiny dealer network, parts unavailable, slow service)',
  'None',
  '{"Motor": "Basic EV motor. Functions but throttle response has >1 second delay — dangerous in emergency situations.", "Reduction gear": "Functional but unremarkable.", "Software": "Worst in any production vehicle tested. Menus crash, gear selector intermittent, backup camera 240p quality, settings don''t persist between drives. Core vehicle systems dependent on unfinished software.", "Build quality": "Body squeaks and rattles. Paint color uneven. Broken parts found on delivery. Feels like a prototype rushed to market.", "Safety": "ESC and hydraulic brake assist error messages within first week. Vehicle unresponsive incidents reported. Car rolled while parked in gear."}');

-- Xiaomi SU7 Max (car_id=74, id=301) — Rel=67.2
-- State-of-art factory, premium materials, but dead last in 2025 Q1 quality ranking.
INSERT INTO reliability (id, car_id, source, reliability_score, score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (301, 74, 'sample', 67.2, 75, 78, 78, 62, 45,
  '{"High complaint-to-sales ratio (239 penalty points Q1 2025)": 3, "Interior edge wear (light colors)": 1, "Energy efficiency below Tesla": 1, "Low chassis (battery damage risk)": 1, "Unusual accident rate (driver-related)": 1}',
  400.0, 0,
  'Good in China; Non-existent outside China',
  'Low',
  '{"Motor": "Dual-motor setup, 673hp. No reported motor failures. Autobild durability test showed excellent results.", "Reduction gear": "Standard dual-motor reduction gear setup. No reported issues.", "Quality ranking": "Dead last in 2025 Q1 China Automobile Quality Network ranking for large BEV sedans. 239 penalty points, 56 above segment average. High complaint-to-sales ratio.", "Build quality": "Robotic factory, AI quality control, tight panel gaps. Physical build quality is genuinely impressive.", "Service": "5-year overall warranty, 8-year battery/motor warranty in China. Zero service infrastructure outside China. Xiaomi won''t export before 2027."}');


-- ============================================================
-- 2. BUILD QUALITY INSERTS (ids 145-158, car_id order)
-- ============================================================

-- Alpine A110 (car_id=15, id=145) — Q=69.3
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
  body_construction_notes, nvh_isolation_notes, interior_materials_notes, paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes, q_score_notes,
  platform_type, assembly_plant, weld_technology, panel_gap_mm, engine_mount_type, glass_type, leather_grade, wood_type, paint_stages, sound_deadening_rating, source)
VALUES (145, 15, 69.2, 82, 68, 62, 72, 60, 65,
  'Bonded and riveted aluminum chassis. Mid-engine layout. Lightweight at 1,100kg. Body panels aluminum. Rear wheel arch area prone to corrosion where bumper attaches.',
  'Lightweight sports car compromises. No acoustic glass. Engine noise is intentional (sport exhaust). Road noise above average at highway speed. Acceptable for purpose-built sports car.',
  'Sabelt carbon-back seats (optional) or standard sport seats. Basic infotainment (pre-Carplay units poor). Renault-sourced switchgear. Cost-conscious but purposeful. Hard plastic on lower panels.',
  'Aluminum body panels resist corrosion well overall. Known weak spot: rear wheel arches and bumper attachment point. Clear coat holds up in moderate climates. Brake discs corrode quickly when standing.',
  'Sporadic electrical issues reported: warning lights without cause, power windows require engine running, battery drain when standing. Fuel pump electronics suspected root cause of sudden failures.',
  'Materials are basic but durable. Sport seats hold up well. Exterior trim and panel alignment generally good for low-volume production. Paint bubbling at rear arches is the main cosmetic concern over time.',
  'Alpine A110 Q-score 69.2. Purpose-built lightweight sports car with aluminum chassis. Build quality is competent for low-volume but not luxury-tier. Interior is the weakest dimension — cost-conscious with basic materials. Rear arch corrosion is the known cosmetic Achilles heel.',
  'bespoke', 'Dieppe (Alpine, France)', 'bonded_aluminum', 4.5,
  'solid', 'standard', 'sport_fabric', 'none', 4, 'minimal', 'sample');

-- Jaguar XJ X351 (car_id=46, id=146) — Q=75.6
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
  body_construction_notes, nvh_isolation_notes, interior_materials_notes, paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes, q_score_notes,
  platform_type, assembly_plant, weld_technology, panel_gap_mm, engine_mount_type, glass_type, leather_grade, wood_type, paint_stages, sound_deadening_rating, source)
VALUES (146, 46, 75.6, 90, 85, 82, 78, 40, 70,
  'All-aluminum riv-bonded monocoque. Lightweight and rigid. Jaguars most advanced body construction at the time. No corrosion issues with aluminum structure.',
  'Excellent luxury sedan isolation. Hydraulic engine mounts. Acoustic laminated windshield. Active noise cancellation. Whisper-quiet at cruise. Jaguar suspension tuning absorbs road imperfections beautifully.',
  'Premium leather throughout. Real wood veneers (multiple options). Jaguar rotary gear selector. Analog instruments on early models, virtual on later. Soft-touch surfaces everywhere. Bowers and Wilkins audio option excellent.',
  'Good paint quality from Castle Bromwich plant. Self-healing clear coat on premium colors. No major paint epidemics. Aluminum body means no rust-through concerns.',
  'THE weakness of the X351. CAN bus architecture ages poorly. Infotainment system crash-prone and slow. Touchscreen response degrades. Module communication failures cascade. Electrical gremlins are the #1 owner complaint.',
  'Premium materials age well physically. Leather develops patina rather than cracking. Wood veneers hold up. But electronic failures undermine the ownership experience — a beautiful cabin with a dead screen feels broken.',
  'Jaguar XJ X351 Q-score 75.6. Physically the best-built Jaguar. Aluminum body is gorgeous and corrosion-proof. Interior materials are genuinely premium. But Jaguar electronics drag the entire score down — the car that looks like a $100K car until the screen goes blank.',
  'bespoke', 'Castle Bromwich (Birmingham, UK)', 'rivet_bonded_aluminum', 3.8,
  'hydraulic', 'acoustic_laminated', 'premium', 'real_wood', 5, 'extensive', 'sample');

-- Range Rover Sport 2nd gen HSE (car_id=55, id=147) — Q=69.4
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
  body_construction_notes, nvh_isolation_notes, interior_materials_notes, paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes, q_score_notes,
  platform_type, assembly_plant, weld_technology, panel_gap_mm, engine_mount_type, glass_type, leather_grade, wood_type, paint_stages, sound_deadening_rating, source)
VALUES (147, 55, 69.3, 78, 85, 80, 72, 35, 62,
  'Aluminum-intensive body on modified T5 platform. Good rigidity for SUV. Panel gaps inconsistent on early builds. Air suspension excellent for ride but adds complexity.',
  'Excellent luxury SUV isolation. Active noise cancellation. Acoustic glass. Whisper-quiet cabin. One of the quietest SUVs at cruise.',
  'Premium Oxford leather. Real wood trim options. Windsor leather on upper trims. Land Rover traditional rotary gear selector. Good soft-touch surfaces.',
  'Decent paint quality but some clear coat issues reported on dark colors. Aluminum body prevents rust-through but paint adhesion can be inconsistent.',
  'Legendary for all the wrong reasons. Screen goes blank. Modules fail and cascade warnings. Terrain Response system adds failure points. Electrical issues are THE defining characteristic of Range Rover ownership.',
  'Physical materials are premium and hold up. Leather ages well. But the constant electronic failures erode confidence and the ownership experience. A luxury SUV with a blank infotainment screen doesn''t feel luxurious.',
  'Range Rover Sport Q-score 69.3. When the electronics work, it''s a beautiful luxury SUV. Excellent NVH, premium interior materials, aluminum body. But the electronic aging score (35) is among the worst in the database and drags everything down.',
  'shared', 'Solihull (UK)', 'mixed_aluminum_steel', 4.2,
  'hydraulic', 'acoustic_laminated', 'premium', 'real_wood', 5, 'extensive', 'sample');

-- Peugeot 406 Coupe (car_id=68, id=148) — Q=74.3
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
  body_construction_notes, nvh_isolation_notes, interior_materials_notes, paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes, q_score_notes,
  platform_type, assembly_plant, weld_technology, panel_gap_mm, engine_mount_type, glass_type, leather_grade, wood_type, paint_stages, sound_deadening_rating, source)
VALUES (148, 68, 74.2, 82, 72, 70, 75, 72, 70,
  'Pininfarina-designed and assembled in Italy (not standard PSA plant). Steel monocoque. Higher build quality than standard 406 sedan. Good rigidity for era.',
  'Adequate for era. Not luxury-tier isolation but well-insulated for a late-90s coupe. Engine refinement from ES9 V6 helps. Road noise moderate at highway speed.',
  'Momo leather seats (optional). Alcantara headliner option. French design flair. Real aluminum trim (not plastic). Simple, elegant instrumentation. Feels more special than PSA parts bin would suggest.',
  'Good European paint standards for era. Galvanized steel body. No major rust epidemics reported. Paint holds up well 20+ years on well-maintained examples.',
  'Simple late-90s electronics are an advantage. Analog gauges, basic ECU, no touchscreen. Very few electronic failure points. What electronics exist are durable.',
  'Materials age gracefully. Momo leather develops character. Aluminum trim doesn''t peel. Simple interior design means fewer things to break. 20+ year old examples can still look sharp.',
  'Peugeot 406 Coupe Q-score 74.2. Pininfarina build quality elevates it above standard PSA products. Simple electronics are a feature, not a bug — they age better than complex modern systems. A 20+ year old example that''s been cared for can still look and feel special.',
  'shared', 'Pininfarina (Turin, Italy)', 'spot_weld', 4.5,
  'solid_rubber', 'standard', 'standard', 'real_wood', 4, 'moderate', 'sample');

-- Tesla Model 3 Performance (car_id=71, id=149) — Q=64.1
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
  body_construction_notes, nvh_isolation_notes, interior_materials_notes, paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes, q_score_notes,
  platform_type, assembly_plant, weld_technology, panel_gap_mm, engine_mount_type, glass_type, leather_grade, wood_type, paint_stages, sound_deadening_rating, source)
VALUES (149, 71, 64.0, 65, 72, 62, 60, 68, 60,
  'Steel/aluminum mixed construction. Panel gaps are Tesla''s well-documented weakness — inconsistent across vehicles and even within the same car. Structural rigidity is good. Gigapress rear improves later builds.',
  'Improved over model years but still behind luxury competition. Glass roof adds NVH. Road noise at highway speeds above average. No engine noise to mask it (it''s an EV). Highland refresh improved significantly.',
  'Minimalist interior. Performance gets sport seats (good). Mostly hard surfaces. Wood/decorative trim is thin. The everything-on-a-screen approach means no physical buttons. Materials feel below price point.',
  'Tesla paint is thin. Orange peel texture common. Paint chips easily from road debris. Multi-coat colors (red, blue) slightly better. Clear coat holds up acceptably but not exceptional.',
  'MCU1 aging on early cars (eMMC wear). MCU2/AMD-based better. Software updates extend useful life but can also introduce new bugs. Over-the-air is both strength and risk.',
  'Interior shows wear at moderate mileage. Alcantara on Performance seats holds up. Piano black trim scratches easily. Paint chips from road debris are the main cosmetic aging issue.',
  'Tesla Model 3 Performance Q-score 64.0. The drivetrain is revolutionary but the build quality tells a different story. Panel gaps, thin paint, minimalist-cheap interior materials. Performance seats are good. Highland refresh improves many of these issues.',
  'bespoke', 'Fremont / Shanghai Gigafactory', 'gigapress_adhesive', 5.5,
  'solid_rubber', 'laminated_glass_roof', 'sport_leather', 'none', 3, 'moderate', 'sample');

-- Tesla Model S Plaid (car_id=70, id=150) — Q=63.3
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
  body_construction_notes, nvh_isolation_notes, interior_materials_notes, paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes, q_score_notes,
  platform_type, assembly_plant, weld_technology, panel_gap_mm, engine_mount_type, glass_type, leather_grade, wood_type, paint_stages, sound_deadening_rating, source)
VALUES (150, 70, 63.3, 62, 78, 65, 58, 62, 60,
  'Older platform (2012 architecture heavily updated). Panel gaps still inconsistent for a $100K+ car. Structural rigidity adequate but not class-leading. Update refreshed front/rear but core architecture dates back.',
  'Better than M3 due to larger cabin and more insulation. Acoustic glass on newer builds. Luxury-tier effort at isolation. Wind noise from frameless doors can be an issue.',
  'Updated interior with yoke steering (polarizing). Materials improved over pre-refresh but still below S-Class/EQS. Open-pore wood decor is nice. Screen-driven everything. Rear screen is a nice touch.',
  'Same Tesla paint issues as M3 but more noticeable at this price point. Thin paint, orange peel, easy chipping. Unacceptable at $130K+ MSRP.',
  'Complex electronics with tri-motor, rear steering, active damping. More failure points. MCU resets while driving reported. Software bugs on Plaid-specific features. Good OTA update cadence but bugs persist.',
  'Similar to M3 — materials show wear at moderate mileage. Yoke steering material can peel. Paint chips from road debris. Interior aging below Mercedes/BMW at same price point.',
  'Tesla Model S Plaid Q-score 63.3. For a $130K+ car, build quality should be much better. Panel gaps, thin paint, interior materials below German luxury standard. The technology and performance are incredible, but the physical build doesn''t match the price.',
  'bespoke', 'Fremont Gigafactory', 'mixed', 5.0,
  'solid_rubber', 'laminated_glass_roof', 'premium', 'none', 3, 'above_average', 'sample');

-- Tesla Model Y Range (car_id=72, id=151) — Q=61.6
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
  body_construction_notes, nvh_isolation_notes, interior_materials_notes, paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes, q_score_notes,
  platform_type, assembly_plant, weld_technology, panel_gap_mm, engine_mount_type, glass_type, leather_grade, wood_type, paint_stages, sound_deadening_rating, source)
VALUES (151, 72, 61.6, 62, 68, 60, 58, 66, 58,
  'Same platform as M3 in SUV form. Panel gaps slightly worse than M3 (hatchback adds variability). Structural rigidity good. Gigapress rear casting on later builds improves consistency.',
  'More road noise than M3 due to hatchback design and larger cargo area. Wind noise from roofline. Adequate for price point but not luxury. Juniper refresh should improve.',
  'Same minimalist approach as M3. Even fewer physical buttons. Base materials feel cheaper than Performance trim. Adequate for $45K crossover but not premium.',
  'Same thin Tesla paint. Chips easily. Orange peel common. White seats stain. Multi-coat colors slightly more durable.',
  'Similar to M3. MCU aging on early units. Software updates help but bugs remain. Heat pump adds complexity versus M3 in cold climates.',
  'Interior shows wear faster than M3 (family car usage). White upholstery stains. Cargo area trim scratches. Paint chips on front fascia from highway driving.',
  'Tesla Model Y Q-score 61.6. Best-selling EV globally but build quality is the weakest of the three Teslas. Hatchback design adds panel gap challenges. Same thin paint and basic interior as M3 but in a more expensive form factor.',
  'shared', 'Fremont / Shanghai / Berlin / Austin Gigafactory', 'gigapress_adhesive', 5.8,
  'solid_rubber', 'laminated_glass_roof', 'standard', 'none', 3, 'moderate', 'sample');

-- BYD Han EV (car_id=73, id=152) — Q=74.1
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
  body_construction_notes, nvh_isolation_notes, interior_materials_notes, paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes, q_score_notes,
  platform_type, assembly_plant, weld_technology, panel_gap_mm, engine_mount_type, glass_type, leather_grade, wood_type, paint_stages, sound_deadening_rating, source)
VALUES (152, 73, 74.0, 78, 82, 78, 75, 60, 70,
  'BYD e-platform. 5-meter sedan with solid construction. Immaculate panel fit reported by reviewers. Galvanized steel body. Good rigidity.',
  'Impressive NVH for the price point. Whisper-quiet cabin. Extensive sound deadening. "Rattling, shuddering, grinding or wind noise? Not in this rolling fortress" — review quote.',
  'Premium materials throughout. Quilted leather seats. Real wood trim. Head-up display. Spacious cabin. Feels above price point. Some infotainment menu logic is unintuitive.',
  'Good paint quality. Multi-coat process. No reported epidemics. Consistent across BYD Changsha production.',
  'Infotainment feels unfinished in certain aspects. Navigation commands don''t work on HUD. Menu navigation inconsistent. Software updates improving but charging logic still has quirks (70-80kW average vs 120kW claimed).',
  'Materials hold up well in ownership reports. Leather durable. Wood trim resists fading. Interior aging appears graceful at 3-4 year mark. Limited data beyond that.',
  'BYD Han EV Q-score 74.0. Impressive craftsmanship that punches above its price. NVH isolation is excellent. Interior materials feel premium. Main deductions for unfinished-feeling infotainment and limited long-term aging data outside China.',
  'bespoke', 'BYD Changsha (Hunan, China)', 'robotic_weld', 3.8,
  'solid_rubber', 'acoustic_laminated', 'premium', 'real_wood', 5, 'above_average', 'sample');

-- Hongqi E-HS9 (car_id=75, id=153) — Q=61.7
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
  body_construction_notes, nvh_isolation_notes, interior_materials_notes, paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes, q_score_notes,
  platform_type, assembly_plant, weld_technology, panel_gap_mm, engine_mount_type, glass_type, leather_grade, wood_type, paint_stages, sound_deadening_rating, source)
VALUES (153, 75, 61.6, 65, 78, 62, 65, 48, 55,
  'Steel body. Thin metal panels — hood visibly flexes with light finger pressure. Looks imposing but substance is lacking. Air suspension provides smooth ride.',
  'Quiet cabin aided by air suspension and large cabin volume. Road and wind noise well-suppressed. Commendable for the class.',
  'Looks premium at first glance but closer inspection reveals synthetic-feeling materials. Quilted seats have synthetic portions. Center console padding thin. Dashboard dominated by screens. "Feels like plastic more than leather" — owner review.',
  'Paint inconsistencies reported between body panels (top vs bottom of door). Quality varies between units. Acceptable but not premium.',
  'Infotainment system widely criticized as "a disaster." Sound quality poor. Menu navigation difficult. Blinker sound and pace irregular. Strange cabin noises reported. Electronics feel first-generation.',
  'Materials that look premium initially may not age as gracefully. Synthetic leather surfaces, thin padding, and electronic gremlins suggest faster cosmetic aging than true luxury competitors.',
  'Hongqi E-HS9 Q-score 61.6. 80% of a Rolls-Royce experience from 50 feet away. Up close: thin metal panels, synthetic-feeling materials, disastrous infotainment. Air suspension provides excellent ride quality. First-gen Chinese luxury — impressive ambition, execution needs work.',
  'shared', 'FAW (Changchun, China)', 'robotic_weld', 4.5,
  'solid_rubber', 'laminated', 'synthetic_premium', 'real_wood', 4, 'above_average', 'sample');

-- Hyundai Ioniq 5 N (car_id=115, id=154) — Q=72.0
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
  body_construction_notes, nvh_isolation_notes, interior_materials_notes, paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes, q_score_notes,
  platform_type, assembly_plant, weld_technology, panel_gap_mm, engine_mount_type, glass_type, leather_grade, wood_type, paint_stages, sound_deadening_rating, source)
VALUES (154, 115, 72.0, 78, 72, 72, 76, 62, 68,
  'E-GMP platform with N-specific structural reinforcements. Good rigidity. VGIS (Virtual Gear Shift) adds drivetrain mounting complexity. Solid body construction typical of Hyundai/Kia.',
  'Performance-tuned so NVH is intentionally compromised. Tire roar from performance rubber. Simulated engine sounds in N mode. Adequate daily comfort in Normal mode but not luxury-quiet.',
  'N-specific sport bucket seats (excellent). Alcantara and leather combination. Physical buttons for key functions (praised). N-specific steering wheel with drive mode buttons. Good materials for the price.',
  'Hyundai paint quality is solid. No reported paint issues specific to Ioniq 5. Good clear coat durability. Consistent quality from Ulsan production.',
  'ICCU failures on standard Ioniq 5 are the concern. N models share the E-GMP electrical architecture. Software-dependent systems. N-specific brake software recall shows growing pains. OTA updates help.',
  'N sport seats hold up well. Alcantara is durable. Performance tires wear faster. Interior plastics can scratch. Good but not exceptional cosmetic aging expected.',
  'Hyundai Ioniq 5 N Q-score 72.0. Solid E-GMP platform construction with N-specific reinforcements. Sport seats and physical buttons are highlights. NVH intentionally compromised for performance character. ICCU electrical architecture is the long-term concern.',
  'shared', 'Ulsan (South Korea)', 'robotic_weld', 4.0,
  'solid_rubber', 'acoustic_laminated', 'sport_leather_alcantara', 'none', 4, 'above_average', 'sample');

-- Lamborghini Huracan LP 580-2 (car_id=116, id=155) — Q=84.9
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
  body_construction_notes, nvh_isolation_notes, interior_materials_notes, paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes, q_score_notes,
  platform_type, assembly_plant, weld_technology, panel_gap_mm, engine_mount_type, glass_type, leather_grade, wood_type, paint_stages, sound_deadening_rating, source)
VALUES (155, 116, 84.8, 95, 72, 88, 92, 65, 85,
  'Carbon fiber and aluminum hybrid chassis. Aerospace-grade construction. Incredibly rigid. Hand-finished body panels. Panel gaps tight and consistent for hand-built car. The gold standard of supercar body construction.',
  'Not applicable to judge as luxury NVH — this is a mid-engine supercar. Intake noise is a feature. Engine behind your head. Road noise present but character-appropriate. Cabin is well-isolated from wind noise.',
  'Hand-stitched Alcantara and leather throughout. Carbon fiber trim. Audi-sourced switchgear (elevated quality). Fully digital cockpit. Every surface premium. The interior justifies the price.',
  'Multi-stage hand-applied paint process. Any color available. Deep, lustrous finish. Clear coat excellent. Paint quality among the best in automotive production.',
  'Complex electronics: MagneRide dampers, front lift system, E-gear transmission, multi-mode drive select. All work well when new but expensive when they fail. Front lift system is the most common electronic complaint.',
  'Premium materials age beautifully. Alcantara develops character. Leather patina is prized. Carbon fiber doesn''t degrade. Hand-built quality means things stay tight. The car will look better in 10 years than most cars do new.',
  'Lamborghini Huracan Q-score 84.8. The highest build quality score in this batch. Hand-assembled at Sant''Agata with aerospace-grade materials. Body, paint, and interior are world-class. Deductions for electronic complexity (MagneRide, lift system) and NVH (supercar, not luxury car).',
  'bespoke', 'Sant''Agata Bolognese (Italy)', 'carbon_aluminum_hybrid', 3.0,
  'solid_rubber', 'laminated', 'semi_aniline', 'carbon_fiber', 7, 'performance_tuned', 'sample');

-- Lucid Air Touring (car_id=124, id=156) — Q=72.7
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
  body_construction_notes, nvh_isolation_notes, interior_materials_notes, paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes, q_score_notes,
  platform_type, assembly_plant, weld_technology, panel_gap_mm, engine_mount_type, glass_type, leather_grade, wood_type, paint_stages, sound_deadening_rating, source)
VALUES (156, 124, 72.7, 80, 85, 82, 72, 45, 68,
  'Clean-sheet EV platform. Aero-optimized body. Panel gaps inconsistent for a $80K+ car — some arrive nearly perfect, others need service visits for wind noise and trim alignment.',
  'World-class NVH isolation. One of the quietest cars at any price. Extensive aero work reduces wind noise. Cabin feels insulated from the world. Strongest build quality dimension.',
  'Beautiful materials. Glass Cockpit (34" curved display) is stunning. Nappa leather. Real wood and metal trim options. Spacious cabin (largest frunk of any EV). Materials genuinely premium.',
  'Adequate paint quality. Some quality control misses at delivery — panel gaps, wind noise from doors, trim misalignment. Not terrible but below expectations for the segment.',
  'Software is the weak link. Screen freezes, driver-assist dropouts, CarPlay glitches. Multiple recalls for wiring harness, rear camera, coolant heater. Hardware is brilliant; software feels beta.',
  'Physical materials hold up well. Leather, wood, metal trim age gracefully. But electronic issues (screen reboots, warning chimes) make the car FEEL less premium than it is. Confidence erodes with each glitch.',
  'Lucid Air Q-score 72.7. Brilliant hardware let down by software. NVH isolation and interior materials are world-class. But panel gap inconsistencies and persistent software bugs prevent a higher score. The car that could be a 90 if the software worked.',
  'bespoke', 'Casa Grande (Arizona, USA)', 'mixed', 4.5,
  'solid_rubber', 'acoustic_laminated', 'nappa', 'real_wood', 5, 'extensive', 'sample');

-- VinFast VF8 (car_id=76, id=157) — Q=41.9
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
  body_construction_notes, nvh_isolation_notes, interior_materials_notes, paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes, q_score_notes,
  platform_type, assembly_plant, weld_technology, panel_gap_mm, engine_mount_type, glass_type, leather_grade, wood_type, paint_stages, sound_deadening_rating, source)
VALUES (157, 76, 41.9, 45, 50, 48, 42, 25, 40,
  'Body squeaks and rattles reported by multiple owners. "Like it is going to fall apart" — owner review. Thin panels. Overall structural feel below segment standard.',
  'Poor NVH. Road and wind noise above average. Steering vibrations at normal speeds. Throttle response has >1 second delay. Feels unfinished.',
  'Cheap materials. Back seat lever found broken in door pocket on delivery. Speakers unresponsive then blast noise. Hard plastics throughout. Below even budget EV standards.',
  'Paint color uneven between panels (driver side top vs bottom visibly different). Frunk battery cover broken on delivery. Clear coat quality below average.',
  'Worst production EV software tested. Menus crash, gear selector intermittent, backup camera 240p quality. Settings don''t persist between drives. ESC and brake assist failure messages within first week.',
  'Poor. Materials that start cheap don''t age well. Paint chips. Interior scratches. Speaker failures. Trim pieces break. Everything about this car suggests rapid deterioration.',
  'VinFast VF8 Q-score 41.9. The worst build quality score in this batch and one of the lowest in the database. "The worst production electric vehicle I''ve ever tested" — EVTV review. Rushed to market with prototype-quality hardware and software.',
  'shared', 'Hai Phong (Vietnam)', 'robotic_weld', 6.0,
  'solid_rubber', 'standard', 'synthetic', 'none', 3, 'minimal', 'sample');

-- Xiaomi SU7 Max (car_id=74, id=158) — Q=76.5
INSERT INTO build_quality (id, car_id, q_score, score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
  body_construction_notes, nvh_isolation_notes, interior_materials_notes, paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes, q_score_notes,
  platform_type, assembly_plant, weld_technology, panel_gap_mm, engine_mount_type, glass_type, leather_grade, wood_type, paint_stages, sound_deadening_rating, source)
VALUES (158, 74, 76.5, 82, 82, 85, 78, 55, 72,
  'State-of-art robotic factory with AI quality control. Tight, consistent panel gaps. Air suspension standard. 5m long, 2m wide. Construction quality impresses Motor Trend and other reviewers.',
  'Extensive NVH work. Road and wind noise kept impressively low. Conversations between front and rear passengers comfortable at highway speed. Air suspension isolates cabin well.',
  'Premium perforated leather. Bolstered sport seats. Physical buttons for key controls (praised by reviewers). Large high-quality center display with slim bezels. Airplane-style HVAC buttons. Feels premium.',
  'Good paint quality consistent with robotic factory. No reported paint epidemics. Michelin Pilot Sport EV tires standard on 20" rims.',
  'Too new for long-term data. 2025 Q1 China quality ranking: dead last in large BEV sedan segment (239 penalty points). High complaint-to-sales ratio. Autobild durability testing showed excellent results. Contradictory signals — jury is out.',
  'Minor edge wear reported on light-colored interiors after 1 year. Later production batches reportedly improved. Good materials suggest graceful aging but only 1-2 years of data.',
  'Xiaomi SU7 Max Q-score 76.5. Best build quality score among Chinese EVs in this batch. State-of-art factory produces genuinely premium results. Interior materials and NVH isolation impress. Main risk: electrical aging — dead last in Q1 2025 quality ranking contradicts the premium physical build.',
  'bespoke', 'Xiaomi EV Factory (Beijing, China)', 'robotic_weld_adhesive', 3.5,
  'solid_rubber', 'acoustic_laminated', 'premium_perforated', 'none', 5, 'extensive', 'sample');

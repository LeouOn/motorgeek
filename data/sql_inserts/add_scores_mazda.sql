-- ============================================================
-- Mazda Reliability + Build Quality Inserts (6 cars)
-- CX-5 KF 2.5T (92), MX-5 ND2 (14), Mazda6 GJ (91),
-- RX-7 FD3S (89), RX-7 Spirit R (109), RX-8 R3 (90)
-- Scores based on librarian + web research: forums, TSB, NHTSA aggregation
-- Catastrophe penalty applies to RX-7 FD, Spirit R, and RX-8 (engine < 50)
-- ============================================================


-- ============================================================
-- PART 1: RELIABILITY (IDs 282-287)
-- ============================================================

-- -----------------------------------------------------------
-- 282: CX-5 KF 2.5T AWD (car_id 92) — Reliability 80.5
-- Engine 78: Skyactiv-G 2.5T proven but cylinder head cracks (class action 2019-2020),
--   carbon buildup (DI), valve seal oil consumption pre-2021. Head redesigned 2021+.
--   Dual injection helps. Generally reliable turbo.
-- Transmission 82: 6-speed Aisin torque converter auto, proven. Some ATF contamination
--   from single lockup clutch (cyl deactivation models). Minor 3-4 chirp TSB.
-- Chassis 85: KF well-built, bushing wear at 100K+, no structural issues, good rust resistance.
-- Electronics 78: Infotainment updates, MAF contamination at 60K, no epidemics but not Toyota-tier.
-- Ease of repair 80: Decent dealer network, parts available, DI needs walnut blast,
--   turbo replacement tight (subframe work). Moderate DIY.
-- Aggregate: 78*0.25 + 82*0.25 + 85*0.15 + 78*0.15 + 80*0.20 = 19.5+20.5+12.75+11.7+16.0 = 80.45 -> 80.5
-- No dimension < 50, no catastrophe penalty.
-- -----------------------------------------------------------
INSERT INTO reliability (
    id, car_id, reliability_score, source,
    score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair,
    common_failures, known_issues, avg_repair_cost, recall_count,
    part_availability, diy_friendliness, score_notes
) VALUES (
    282, 92, 80.5, 'sample',
    78, 82, 85, 78, 80,
    '["Skyactiv-G 2.5T cylinder head cracking (class action, 2019-2020, redesigned 2021+)","Carbon buildup on intake valves (direct injection, 60K+ miles)","Valve stem seal oil consumption (pre-2021 2.5T, TSB issued)","MAF sensor contamination triggering fault codes (60K miles)","Cylinder deactivation ATF contamination from lockup clutch wear","Infotainment system freezes requiring reboot"]',
    '["Skyactiv-G 2.5T is generally reliable — not a Theta II situation","Class action lawsuit alleges cylinder head structural weakness causing coolant leaks and stalling","Covers 2019-2020 CX-5, 2016-2020 CX-9, 2018-2020 Mazda6","Mazda redesigned cylinder head and exhaust manifold gasket for 2021+ — appears to fix issue","Pre-2021 cars should be checked for coolant loss","Carbon buildup is a DI issue, not Mazda-specific — walnut blast every 60-80K","6-speed Aisin auto is proven with no systemic failures","Cylinder deactivation adds complexity and some ATF contamination risk","Engine bay is tight — turbo replacement requires subframe drop"]',
    550.0, 3,
    'Good (Mazda dealer network + aftermarket)',
    'Moderate (DI maintenance, tight turbo access)',
    'CX-5 2.5T reliability 80.5. The Skyactiv-G 2.5T is a generally reliable turbo engine after 2021 revisions. Pre-2021 cars carry cylinder head crack risk (class action) — buy 2021+ if possible. Transmission is a proven Aisin 6-speed with no systemic issues. Chassis and electronics are above average for mass-market CUV. Carbon buildup and MAF sensor are routine DI maintenance items. Deductions mainly for cylinder head risk and Mazda-tier (not Toyota-tier) electrical aging.'
);

-- -----------------------------------------------------------
-- 283: MX-5 Miata ND2 Soft Top (car_id 14) — Reliability 83.2
-- Engine 85: Skyactiv-G 2.0 NA with forged internals (ND2-specific). Excellent reliability.
--   Carbon buildup (DI) is the only real issue. Very few engine complaints.
-- Transmission 72: Manual has known issues — 5 revisions since V1. Synchro problems
--   on 2022-2023. Case flex, bearing quality questioned. ND2 2019-2021 better than early/late.
-- Chassis 88: Excellent handling. Some reports of chassis not as robust as NC ("gram strategy").
--   No structural failures. Rust resistance good.
-- Electronics 82: Simple electronics. Battery drain parasitic loss reported. Soft top leaks
--   can cause electrical damage. Otherwise minimal.
-- Ease of repair 92: Huge Miata community. Parts everywhere. Simple engine bay.
--   Every mechanic knows Miatas. The quintessential DIY sports car.
-- Aggregate: 85*0.25 + 72*0.25 + 88*0.15 + 82*0.15 + 92*0.20 = 21.25+18.0+13.2+12.3+18.4 = 83.15 -> 83.2
-- No dimension < 50, no catastrophe penalty.
-- -----------------------------------------------------------
INSERT INTO reliability (
    id, car_id, reliability_score, source,
    score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair,
    common_failures, known_issues, avg_repair_cost, recall_count,
    part_availability, diy_friendliness, score_notes
) VALUES (
    283, 14, 83.2, 'sample',
    85, 72, 88, 82, 92,
    '["Manual transmission synchro issues (especially 2nd/3rd gear, 5 revisions since launch)","Carbon buildup on intake valves (direct injection, 60K+ miles)","Soft top water leaks causing interior and electrical damage","Battery parasitic drain (some ND2 units)","Clutch slave cylinder failure (hydraulic leak)"]',
    '["ND2 Skyactiv-G 2.0 has forged connecting rods — stronger than ND1 cast rods","Engine is virtually bulletproof in stock form — no engine failure reports on stock power","Transmission is the ND weak link: lightweight design (38-40kg) means material compromises","2019-2021 ND2 transmissions are the safest years; 2022-2023 have more synchro complaints","5 manual transmission revisions — V1 (2016-2017) worst, V5 (2020+) improved","Carbon buildup is a DI issue mitigated by regular highway driving","Soft top leaks are well-documented — check drain tubes, replace weatherstripping","Huge aftermarket support — every part is available from multiple vendors","Miata.net and Reddit r/Miata are unmatched DIY resources"]',
    400.0, 1,
    'Excellent (massive Miata aftermarket + Mazda dealers)',
    'High (simple engine bay, huge community, every mechanic knows Miatas)',
    'MX-5 ND2 reliability 83.2. The engine (85) is excellent — forged internals, no stock failures reported. Transmission (72) is the weak link with known synchro issues across 5 revisions; buy 2019-2021 for best odds. Chassis (88) is well-engineered with no structural concerns. Electronics (82) are simple — the biggest electrical risk is soft top leaks, not component failure. Ease of repair (92) is among the highest in the database — the Miata community is the gold standard for DIY support. The transmission knocks 11 points off what would otherwise be a 90+ car.'
);

-- -----------------------------------------------------------
-- 284: Mazda6 GJ 2.5L Skyactiv-G Touring (car_id 91) — Reliability 81.5
-- Engine 80: Skyactiv-G 2.5 NA proven workhorse. Early 2014 had cylinder head issues.
--   Carbon buildup (DI). Thermostat failures. MAF sensor contamination.
--   Generally excellent at 200K+ miles. No class action (unlike 2.5T).
-- Transmission 82: Same proven 6-speed Aisin auto as CX-5. Manual option also reliable.
--   No major transmission issues documented.
-- Chassis 82: GJ platform solid. Rust improved over previous gen.
--   Standard midsize sedan construction. No structural issues.
-- Electronics 78: Infotainment updates, MAF sensor, no major gremlins.
--   Simpler than luxury brands. Typical Mazda electronics — adequate.
-- Ease of repair 85: Shared platform with CX-5 and Mazda3. Parts everywhere.
--   Simple transverse 4-cyl engine bay. Every mechanic can work on it.
-- Aggregate: 80*0.25 + 82*0.25 + 82*0.15 + 78*0.15 + 85*0.20 = 20.0+20.5+12.3+11.7+17.0 = 81.5
-- No dimension < 50, no catastrophe penalty.
-- -----------------------------------------------------------
INSERT INTO reliability (
    id, car_id, reliability_score, source,
    score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair,
    common_failures, known_issues, avg_repair_cost, recall_count,
    part_availability, diy_friendliness, score_notes
) VALUES (
    284, 91, 81.5, 'sample',
    80, 82, 82, 78, 85,
    '["Cylinder head cracking (early 2014 models, TSB issued)","Carbon buildup on intake valves (direct injection, 60K+)","Thermostat housing failure (plastic, 60-120K)","MAF sensor contamination triggering fault codes","PCV valve clogging contributing to carbon buildup","Intake camshaft wear increasing engine noise (high mileage)"]',
    '["Skyactiv-G 2.5 NA is one of Mazda''s best engines — over a decade in production with minimal issues","Early 2014 models had cylinder head problems — 2015+ significantly improved","No class action lawsuit for the 2.5 NA (unlike the 2.5T)","Direct injection carbon buildup is the main recurring maintenance item","Engine life expectancy 200K+ miles with regular maintenance","6-speed Aisin auto is the same proven unit used across Mazda lineup","Shared platform with CX-5 and Mazda3 means parts are everywhere","Transverse 4-cylinder engine bay is simple and accessible","European owners report excellent long-term reliability for Skyactiv-G engines"]',
    450.0, 2,
    'Excellent (Mazda shared platform, parts everywhere)',
    'High (simple engine bay, every mechanic can work on it)',
    'Mazda6 GJ reliability 81.5. The Skyactiv-G 2.5 NA is a proven workhorse with no class actions and 200K+ mile life expectancy. Engine (80) loses points for early 2014 cylinder head issues and DI carbon buildup, but 2015+ cars are excellent. Transmission (82) is the same bulletproof Aisin 6-speed across Mazda''s lineup. Chassis (82) is solid with no structural concerns. Electronics (78) are typical Mazda — not Toyota-tier but no epidemics. Ease of repair (85) benefits from shared platform and transverse simplicity. A reliable midsize sedan that just works.'
);

-- -----------------------------------------------------------
-- 285: RX-7 FD3S Twin Turbo (car_id 89) — Reliability 60.5
-- Engine 42: THE defining rotary problem. Apex seals fail from oil starvation, pre-ignition,
--   overheating, carbon deposits. Rebuilds at 40-80K miles typical ($5K-10K).
--   Sequential twin turbos fail from heat/oil. Cooling system issues.
--   Catalytic converter failure cascades. Oil consumption by design.
-- Transmission 80: 5-speed manual robust when not abused. 4-speed auto weaker.
--   Clutch at 60-80K. Differential holds up well.
-- Chassis 88: Legendary double-wishbone all corners. Incredible handling.
--   Rust in wheel arches, sills, behind taillights (JDM import issue).
-- Electronics 62: 1990s electronics — mostly simple but aging.
--   Pop-up headlight switches fail. Vacuum hose failures affect sequential turbo.
--   ECU capacitor leakage.
-- Ease of repair 45: Rotary specialists only. Parts increasingly scarce (JDM).
--   No mainstream mechanic will touch it. Complex sequential turbo system.
--   Engine rebuilds expensive and frequent.
-- Raw: 42*0.25 + 80*0.25 + 88*0.15 + 62*0.15 + 45*0.20 = 10.5+20.0+13.2+9.3+9.0 = 62.0
-- MIN DIM = 42 < 50 -> CATASTROPHE PENALTY:
--   penalty = 0.85 + (42/50)*0.15 = 0.85 + 0.126 = 0.976
--   aggregate = 62.0 * 0.976 = 60.512 -> 60.5
-- -----------------------------------------------------------
INSERT INTO reliability (
    id, car_id, reliability_score, source,
    score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair,
    common_failures, known_issues, avg_repair_cost, recall_count,
    part_availability, diy_friendliness, score_notes
) VALUES (
    285, 89, 60.5, 'sample',
    42, 80, 88, 62, 45,
    '["Apex seal failure — THE defining rotary weakness, requires full engine rebuild ($5K-10K)","Sequential twin turbo failure from heat cycling and oil contamination ($3K-5K rebuild)","Cooling system overheating — AST cap failure, coolant pipe leaks, cracked radiator","Excessive oil consumption (1 quart per 2500 miles normal, more indicates seal failure)","Catalytic converter clogging from carbon deposits cascades into engine damage","Vacuum hose degradation causing sequential turbo system malfunction","Turbo manifold cracking from extreme heat"]',
    '["13B-REW apex seals are the engine killer — oil starvation and pre-ignition from carbon are primary causes","Well-maintained stock engines CAN exceed 150K miles but this is exceptional, not typical","Rebuild at 40-80K miles is the expected norm, not a failure of maintenance","Sequential twin turbo system is complex and failure-prone — many owners convert to single turbo","Cooling system overhaul is essential preventative maintenance","Rotary engines burn oil by design (oil metering pump) — must check oil every fill-up","Compression test is CRITICAL when buying: 100psi spec, below 85psi = rebuild needed","Must use non-synthetic oil and consider premix for seal lubrication","Engine must be warmed up before shutdown to prevent flooding and carbon buildup","Parts increasingly scarce — FD was never sold in large volumes outside Japan","Rotary specialists are few and far between — most mechanics will not touch it"]',
    2500.0, 0,
    'Poor (rotary specialists only, JDM import parts scarce)',
    'Low (rotary expertise required, complex sequential turbo, frequent rebuilds)',
    'RX-7 FD reliability 60.5 (catastrophe penalty applied: engine 42 < 50). The 13B-REW twin-turbo rotary defines "unreliable by design" — apex seals fail at 40-80K miles requiring $5K-10K rebuilds. The sequential turbo system, cooling system, and catalytic converter all compound the engine''s inherent weaknesses. Transmission (80) and chassis (88) are excellent — the FD drives like a dream WHEN the engine runs. Electronics (62) are simple but aging vacuum hoses create turbo system gremlins. Ease of repair (45) reflects rotary specialist scarcity and JDM parts unavailability. The raw score of 62.0 drops to 60.5 with the catastrophe penalty (min dim=42, penalty=0.976). This car earns its reputation: legendary chassis, unreliable engine.'
);

-- -----------------------------------------------------------
-- 286: RX-7 FD3S Spirit R Type RS (car_id 109) — Reliability 65.7
-- Engine 48: Same 13B-REW as standard FD but Spirit R is the final Series 8 (2002).
--   Reinforced apex seals, better cooling channels, improved turbos.
--   Slightly better reliability than earlier FDs but fundamentally same engine.
--   Rebuild interval 60-100K with meticulous care. Still a rotary — apex seals
--   remain the defining weakness. Better than standard FD but still LOW.
-- Transmission 85: Spirit R came only with 5-speed manual. Upgraded clutch.
--   Higher-spec drivetrain components. No auto option. Same robust gearbox.
-- Chassis 90: Same legendary FD chassis + Spirit R Bilstein shocks,
--   cross-drilled rotors, Recaro seats. Best-of-breed FD. Final production quality.
-- Electronics 65: 2002 most mature FD electronics. Revised ECU. Better reliability
--   than 1993-1995 units. Still 1990s-era with aging wiring and vacuum hoses.
-- Ease of repair 48: Same as FD — rotary specialists only. Spirit R parts EXTREMELY rare
--   (1,500 made). Recaro seats, BBS wheels unobtainium. Standard 13B-REW engine
--   parts shared with other FDs. Same fundamental DIY difficulty.
-- Raw: 48*0.25 + 85*0.25 + 90*0.15 + 65*0.15 + 48*0.20 = 12.0+21.25+13.5+9.75+9.6 = 66.1
-- MIN DIM = 48 < 50 -> CATASTROPHE PENALTY:
--   penalty = 0.85 + (48/50)*0.15 = 0.85 + 0.144 = 0.994
--   aggregate = 66.1 * 0.994 = 65.7034 -> 65.7
-- -----------------------------------------------------------
INSERT INTO reliability (
    id, car_id, reliability_score, source,
    score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair,
    common_failures, known_issues, avg_repair_cost, recall_count,
    part_availability, diy_friendliness, score_notes
) VALUES (
    286, 109, 65.7, 'sample',
    48, 85, 90, 65, 48,
    '["Apex seal failure — same 13B-REW fundamental weakness (improved but not eliminated)","Sequential twin turbo aging — 20+ year old turbos, many already rebuilt or replaced","Cooling system aging — radiator, AST cap, coolant pipes all 20+ years old","Vacuum hose degradation (rubber 20+ years old) affecting turbo operation","Oil consumption inherent to rotary design","Spirit R-specific parts unobtainium — Recaro seats, BBS wheels, unique trim"]',
    '["Spirit R is the FINAL FD — Series 8 with all refinements Mazda learned over 10 years of production","Reinforced apex seals and better cooling channels than earlier Series 6/7","Engine is marginally more reliable than 1993 FD but fundamentally the same 13B-REW","Must meet 2002 build quality — these are the best-sorted FDs from the factory","Only 1,500 Spirit Rs produced — Spirit R-specific parts are essentially unobtainable","Standard 13B-REW engine parts shared across all FDs — engine parts not the scarcity issue","Most Spirit Rs are collector-owned and maintained to a higher standard than average FDs","Manual transmission only — no auto weakness","Same rotary maintenance demands: premix, frequent oil changes, warm-up before shutdown","Compression test still critical — 100psi spec, below 85psi = rebuild needed"]',
    2500.0, 0,
    'Poor (rotary specialists only, Spirit R trim parts unobtainium)',
    'Low (rotary expertise required, Spirit R-specific parts rare)',
    'RX-7 Spirit R reliability 65.7 (catastrophe penalty applied: engine 48 < 50). The best FD Mazda ever built — Series 8 refinements improve reliability over earlier cars but the fundamental 13B-REW apex seal weakness remains. Engine (48) is 6 points higher than standard FD (42) thanks to reinforced seals and better cooling, but still below the catastrophe threshold. Transmission (85) benefits from manual-only specification. Chassis (90) is the highest in this Mazda batch — Bilstein, cross-drilled brakes, final production quality. Electronics (65) are the most mature FD electronics. Ease of repair (48) is same as FD minus Spirit R-specific parts scarcity. The raw score of 66.1 drops minimally to 65.7 (penalty=0.994, engine is close to 50).'
);

-- -----------------------------------------------------------
-- 287: RX-8 SE3P R3 high-power (car_id 90) — Reliability 54.7
-- Engine 35: Renesis 13B-MSP is WORSE than 13B-REW. Apex seals, flooding, low compression
--   at 80-100K, catalytic converter clogging kills engines, coil pack failures,
--   hot-start problems, excessive oil consumption. "Not Suggested" rating.
--   Extended warranties issued. Many engines fail before 100K.
-- Transmission 78: 6-speed manual decent. Some synchro issues. Not the weak point.
--   Clutch hydraulic cylinder failures. Better than the engine.
-- Chassis 82: Excellent handling — front-midship, 50/50 weight distribution.
--   Suspension well-designed. Some wear at 100K+. Let down by the engine.
-- Electronics 58: More complex than RX-7. Renesis ECU, coil pack failures chronic,
--   engine harness wear, door lock failures, waterlogged headlights,
--   starter motor failures from chronic cranking (flooding).
-- Ease of repair 40: Rotary specialists needed. More RX-8s made than FD so parts slightly
--   more available. Renesis-specific parts still scarce. Rebuild $4K-8K.
--   Compression test requires rotary-specific equipment.
-- Raw: 35*0.25 + 78*0.25 + 82*0.15 + 58*0.15 + 40*0.20 = 8.75+19.5+12.3+8.7+8.0 = 57.25
-- MIN DIM = 35 < 50 -> CATASTROPHE PENALTY:
--   penalty = 0.85 + (35/50)*0.15 = 0.85 + 0.105 = 0.955
--   aggregate = 57.25 * 0.955 = 54.67375 -> 54.7
-- -----------------------------------------------------------
INSERT INTO reliability (
    id, car_id, reliability_score, source,
    score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair,
    common_failures, known_issues, avg_repair_cost, recall_count,
    part_availability, diy_friendliness, score_notes
) VALUES (
    287, 90, 54.7, 'sample',
    35, 78, 82, 58, 40,
    '["Apex seal failure and compression loss — most problematic rotary Mazda ever made","Engine flooding from short trips and cold shutdowns — excess fuel soaks spark plugs","Low compression causing hot-start failure (cannot restart within 3-5 min of shutdown)","Catalytic converter clogging — unburned fuel melts cat, creates backpressure, kills engine","Ignition coil pack failure — chronic, causes misfires, rough idle, power loss","Starter motor failure from chronic cranking during flood-clearing procedures","Engine harness wear from component interference","Door lock actuator failure","Waterlogged headlights"]',
    '["Renesis 13B-MSP is rated ''Not Suggested'' by multiple reliability sources","Mazda issued extended warranties for early RX-8 engines due to widespread compression loss","Many engines fail before 80-100K miles — even well-maintained examples struggle to 125K","The Renesis is WORSE than the 13B-REW in the RX-7 — NA but more failure modes","Flooding is a design flaw: engine must be fully warmed before shutdown, no short trips","Hot-start failure (low compression when warm) is the telltale sign of engine death","Catalytic converter failure cascades: bad coils/plugs -> rich mixture -> cat melts -> backpressure -> apex seal death","Oil must be checked every fill-up — rotary burns oil by design","Compression test is essential when buying: below 85psi means rebuild needed ($4K-8K)","Must use mineral oil (NOT synthetic) to prevent carbon residue","More RX-8s produced than FD RX-7s so parts slightly more available","R3 (2009-2011) is the best year — improved engine, better cooling, revised ECU","Still fundamentally unreliable — buy one with a fresh rebuild or budget for one"]',
    3000.0, 2,
    'Poor (rotary specialists only, Renesis-specific parts scarce)',
    'Low (rotary expertise required, frequent engine attention needed)',
    'RX-8 R3 reliability 54.7 (catastrophe penalty applied: engine 35 < 50). The Renesis 13B-MSP is the most problematic rotary Mazda ever made — rated "Not Suggested" by reliability sources. Engine (35) scores lowest in this entire Mazda batch: apex seals, flooding, low compression, catalytic converter cascading failure, chronic coil pack issues. Most engines need rebuild by 80-100K miles. Transmission (78) is decent — not the problem. Chassis (82) is excellent with brilliant handling, completely let down by the engine. Electronics (58) suffer from coil pack failures, starter motor death from chronic cranking, and harness wear. Ease of repair (40) is the lowest — while parts are slightly more available than FD, the Renesis-specific failure modes make it arguably worse to own. The raw score of 57.25 drops to 54.7 with the catastrophe penalty (min dim=35, penalty=0.955). If you want the RX-8 experience, buy one that already has a fresh engine rebuild.'
);


-- ============================================================
-- PART 2: BUILD QUALITY Q-FACTOR (IDs 139-144)
-- ============================================================

-- -----------------------------------------------------------
-- 139: CX-5 KF 2.5T AWD (car_id 92) — Q-score 68.7
-- Body 70: Shared Skyactiv-Vehicle architecture. Not bespoke. High-strength steel.
--   MacPherson strut. Good for CUV class but not premium-tier.
-- NVH 65: Decent for CUV. Not luxury-quiet. Road noise. Standard glass.
--   Mazda improved NVH in KF gen but below premium brands.
-- Interior 62: Good for price. Leather on upper trims. Soft-touch upper, hard lower.
--   Real stitching. Piano black. Above mass-market average.
-- Paint 75: Good Mazda paint. No epidemics. Electrostatic primer. Galvanized steel.
-- Electrical 72: Modern Mazda electronics. Infotainment glitches. 6-speed proven.
--   Cylinder deactivation adds complexity.
-- Cosmetic 68: Mazda interiors age reasonably. Leather holds up. Piano black scratches.
--   Dashboard plastics resist UV. Average for mass-market CUV.
-- Aggregate: 70*0.25 + 65*0.10 + 62*0.20 + 75*0.15 + 72*0.15 + 68*0.15
--   = 17.5+6.5+12.4+11.25+10.8+10.2 = 68.65 -> 68.7
-- -----------------------------------------------------------
INSERT INTO build_quality (
    id, car_id, q_score,
    score_body_construction, score_nvh_isolation, score_interior_materials,
    score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
    body_construction_notes, nvh_isolation_notes, interior_materials_notes,
    paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes,
    q_score_notes,
    platform_type, assembly_plant, weld_technology, panel_gap_mm,
    engine_mount_type, glass_type, leather_grade, wood_type,
    paint_stages, sound_deadening_rating, source
) VALUES (
    139, 92, 68.7,
    70, 65, 62,
    75, 72, 68,
    'Shared Mazda Skyactiv-Vehicle architecture (not bespoke). High-strength steel increased significantly over previous generation. MacPherson strut front, multi-link rear. Spot welding throughout with structural adhesive in key areas. Panel gaps ~4.5mm — improved over KE generation but not luxury-tight. Good rigid construction for the CUV class.',
    'Decent NVH for a mass-market CUV but not luxury-quiet. Standard rubber engine mounts (some liquid-filled on upper trims). Some acoustic treatment in firewall and floor pan. Laminated front windshield on Signature trim. Road noise noticeable at highway speeds from 19-inch wheels on Turbo trim. The Skyactiv-G 2.5T is characteristically loud under boost — direct injection tick at idle. Better than previous generation CX-5 but below Lexus NX or Audi Q5.',
    'Good materials for the price point — above average for mainstream CUV. Available Caturra Brown Nappa leather on Signature trim (standard leather on lower trims). Real contrast stitching on dash and door panels. Santos rosewood trim on Signature (genuine wood). Aluminum-look trim on lower trims. Soft-touch upper dash and door panels, hard plastics on lower panels and console. Mazda Connect infotainment functional but aging. Above Camry RAV4 tier, below Lexus.',
    'Good Mazda paint quality with no known epidemics. Electrostatic primer application. Galvanized steel panels throughout. Self-healing clear coat on darker colors. Paint chipping on front bumper from road debris reported. Holds up well at 5-10 years with no premature clear coat failure. Standard mass-market paint quality — better than Korean competitors, not quite Japanese premium.',
    'Modern Mazda electronics are generally reliable. Infotainment system can require reboots. Cylinder deactivation adds electronic complexity. MAF sensor contamination at 60K is more of a maintenance item than a design flaw. No systemic electrical gremlins like German competitors. Good electrical track record at 5-10 years of data. Simpler than luxury-brand electronics.',
    'Mazda interiors age reasonably well. Nappa leather on Signature trim holds up at 100K+ miles. Standard leather shows minor bolster wear at 80K+. Piano black trim scratches easily and shows dust. Dashboard plastics resist UV cracking. Steering wheel shows wear at 100K+. Center console armrest material thins. Better than average for mass-market CUV aging.',
    'CX-5 KF Q-score 68.7. Honest mass-market CUV build quality — Mazda punches above its price class. Body construction (70) is solid for shared platform. NVH (65) is adequate but below premium competitors — the 2.5T DI tick and road noise are noticeable. Interior materials (62) on Signature trim approach entry-luxury with Nappa leather and genuine wood. Paint (75) is good quality with no issues. Electrical aging (72) is above average. Cosmetic aging (68) is average for the class. The CX-5 is the best-driving CUV in its class and the build quality reflects a driver-focused, not luxury-focused, philosophy.',
    'shared', 'Hofu Plant (Yamaguchi, Japan) / Ujina Plant (Hiroshima, Japan)', 'spot', 4.5,
    'liquid', 'laminated', 'nappa', 'real_wood',
    4, 'above_average', 'expert_analysis'
);

-- -----------------------------------------------------------
-- 140: MX-5 Miata ND2 Soft Top (car_id 14) — Q-score 60.3
-- Body 75: Purpose-built ND platform. Not shared with Mazda3. Excellent roadster rigidity.
--   Aluminum hood, trunk lid, front fenders. Double-wishbone front, multi-link rear.
--   Well-engineered lightweight platform.
-- NVH 30: Soft-top roadster with minimal NVH. Road noise, wind noise above 50mph.
--   No acoustic glass. Minimal sound deadening. The loudness is by design.
-- Interior 45: Minimalist sports car. Basic materials. Some hard plastics.
--   Small cabin. Functional not luxurious. Updated for ND2 but still modest.
-- Paint 72: Good Mazda paint. No epidemics. Some clear coat at 10+ years.
--   Soft top means exposed panels. Front bumper chips from low nose.
-- Electrical 75: Simple electronics — Miata advantage. Basic infotainment.
--   No complex ADAS in ND2. Battery drain issues. Otherwise simple and durable.
-- Cosmetic 50: Roadster life is hard. Soft top replacement at 8-12 years ($1-2K).
--   Seat bolster wear. Steering wheel leather wears. Interior plastics scratch.
--   Dashboard UV damage if not garaged.
-- Aggregate: 75*0.25 + 30*0.10 + 45*0.20 + 72*0.15 + 75*0.15 + 50*0.15
--   = 18.75+3.0+9.0+10.8+11.25+7.5 = 60.3
-- -----------------------------------------------------------
INSERT INTO build_quality (
    id, car_id, q_score,
    score_body_construction, score_nvh_isolation, score_interior_materials,
    score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
    body_construction_notes, nvh_isolation_notes, interior_materials_notes,
    paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes,
    q_score_notes,
    platform_type, assembly_plant, weld_technology, panel_gap_mm,
    engine_mount_type, glass_type, leather_grade, wood_type,
    paint_stages, sound_deadening_rating, source
) VALUES (
    140, 14, 60.3,
    75, 30, 45,
    72, 75, 50,
    'Purpose-built ND platform — not shared with Mazda3 or CX-5. Exceptional rigidity for a roadster — hood strut brace, undercarriage bracing, reinforced A-pillars. Aluminum hood, trunk lid, and front fenders for weight reduction. Double-wishbone front, multi-link rear. One of the best-handling cars at any price. Well-engineered lightweight structure.',
    'Soft-top roadster with functionally minimal NVH isolation — by design. Wind noise significant above 50mph with top up. No acoustic glass anywhere. Minimal sound deadening — Mazda saved every gram. The Skyactiv-G at 7500rpm and exhaust note are the intended audio experience. With top down, NVH is moot — you bought a roadster. Better than S2000 for isolation but not by much.',
    'Minimalist sports car interior prioritizing weight savings over comfort. Cloth seats standard (leather optional on Grand Touring). Soft-touch surfaces limited to upper dash and door tops — hard plastics dominate lower panels. No wood anywhere — aluminum-look or piano black trim. Small steering wheel. Functional gauges. Mazda Connect infotainment on small screen. Updated for ND2 with slightly better materials than ND1. The driving position is perfect; the materials are not the point.',
    'Good Mazda paint quality. No epidemic issues. Some clear coat thinning on Soul Red Crystal and Machine Gray at 10+ years — these metallic colors are more susceptible. Front bumper paint chips from low nose stance. Soft top frame exposed to elements. Better paint aging than NA/NB Miata generations.',
    'Simple electronics — the Miata advantage. No complex ADAS in ND2 (2019-2024). Basic Mazda Connect infotainment. No touchscreen while driving (rotary knob only). Minimal sensors. Battery parasitic drain reported on some units. No air suspension, no motorized everything. Nearly 1990s simplicity in a modern package. Good electrical aging expected.',
    'Roadster life accelerates cosmetic aging. Soft top requires replacement at 8-12 years ($1-2K aftermarket). Seat bolsters wear quickly from low ingress/egress. Steering wheel leather wears at crown. Interior plastics scratch and scuff easily. Dashboard can crack in hot climates (Arizona, Texas) if not garaged. Paint rock chips from low nose. Hard to keep pristine — most ND2s show their mileage. Better than S2000 aging due to Mazda paint quality.',
    'MX-5 ND2 Q-score 60.3. The lowest build quality score among the non-rotary Mazdas — appropriately so for a purpose-built roadster. Body construction (75) is excellent for a roadster. NVH (30) is among the lowest in the database — a soft-top roadster is not built for silence. Interior materials (45) are functional, not luxurious. Electrical aging (75) scores well due to Miata simplicity. Cosmetic aging (50) reflects the harsh reality of roadster life — everything ages faster when exposed to the elements. The ND2 is evaluated as a sports car on luxury build quality metrics — the low scores reflect design purpose, not quality deficiency.',
    'bespoke', 'Ujina Plant (Hiroshima, Japan)', 'spot', 5.0,
    'rubber', 'standard', 'none', 'none',
    4, 'minimal', 'expert_analysis'
);

-- -----------------------------------------------------------
-- 141: Mazda6 GJ 2.5L Skyactiv-G Touring (car_id 91) — Q-score 66.6
-- Body 68: Shared Mazda6/GJ platform. Not bespoke. High-strength steel.
--   MacPherson strut front, multi-link rear. Good for midsize sedan.
--   Panel gaps decent but not luxury-tight.
-- NVH 62: Decent for midsize sedan. Not as quiet as Camry or Accord.
--   Road noise at highway speed. Skyactiv engine characteristically loud (DI tick).
-- Interior 60: Good for segment. Leather available. Soft-touch upper, hard lower.
--   Real stitching. Aluminum-look trim. Above base Camry but not luxury.
-- Paint 72: Good Mazda paint. No epidemics. Galvanized steel. Standard quality.
-- Electrical 72: Typical Mazda electronics. Infotainment glitches. No major epidemics.
-- Cosmetic 65: Mazda interiors age acceptably. Leather wears at bolster.
--   Steering wheel shows age. Dashboard resists UV. Piano black scratches.
-- Aggregate: 68*0.25 + 62*0.10 + 60*0.20 + 72*0.15 + 72*0.15 + 65*0.15
--   = 17.0+6.2+12.0+10.8+10.8+9.75 = 66.55 -> 66.5 (round)
-- -----------------------------------------------------------
INSERT INTO build_quality (
    id, car_id, q_score,
    score_body_construction, score_nvh_isolation, score_interior_materials,
    score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
    body_construction_notes, nvh_isolation_notes, interior_materials_notes,
    paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes,
    q_score_notes,
    platform_type, assembly_plant, weld_technology, panel_gap_mm,
    engine_mount_type, glass_type, leather_grade, wood_type,
    paint_stages, sound_deadening_rating, source
) VALUES (
    141, 91, 66.5,
    68, 62, 60,
    72, 72, 65,
    'Shared Mazda6 GJ platform (related to CX-5 architecture). Not bespoke. High-strength steel in key structural areas. MacPherson strut front, multi-link rear. Spot welding throughout. Panel gaps ~4.5mm — decent for midsize sedan but not luxury-tight. Standard mass-market Japanese sedan construction.',
    'Decent NVH for midsize sedan but a known weakness vs competitors. Not as quiet as Camry or Accord at cruise. The Skyactiv-G 2.5 is characteristically loud — direct injection ticking at idle and under load. Standard rubber engine mounts. Some acoustic treatment in firewall. Laminated front windshield. Road noise present at highway speed. Mazda prioritized driving dynamics over isolation.',
    'Good materials for the midsize segment. Available leather on Touring and Grand Touring trims. Soft-touch upper dash and door panels. Hard plastics on lower panels and console. Real contrast stitching. Aluminum-look trim — not real metal. Piano black on center stack. No real wood anywhere. Above base Camry and Accord for material quality but below luxury. The Touring trim adds enough to feel premium without being premium.',
    'Good Mazda paint quality with no known epidemics. Electrostatic primer. Galvanized steel panels. Some clear coat thinning on Machine Gray and Soul Red at 10+ years in sunbelt states. Paint holds up well overall. Front bumper paint chips from road debris. Standard mass-market paint — better than domestic, on par with Japanese competitors.',
    'Typical Mazda electronics — functional but not bulletproof. Infotainment system can freeze requiring reboot. MAF sensor contamination is more maintenance than design flaw. No complex ADAS until later model years. Simpler electronics than German competitors in this class. Good electrical aging for 2012-2021 vintage. No systemic electrical gremlins reported.',
    'Mazda interiors age acceptably for mass market. Leather on Touring trim shows bolster wear at 80K+ miles. Steering wheel leather wears at crown. Dashboard plastics resist UV cracking. Piano black trim scratches and shows fingerprints. Center console armrest material thins. Door panel scuffs at entry points. Better than average for Japanese midsize sedan aging.',
    'Mazda6 GJ Q-score 66.5. Honest midsize sedan build quality — Mazda prioritizes driving dynamics over isolation. Body construction (68) is standard shared-platform. NVH (62) is the weakness — the Skyactiv DI tick and road noise keep it below Camry/Acord quietness. Interior materials (60) are above average for the class with leather and real stitching on Touring. Paint (72) is good quality. Electrical aging (72) is above average — simple electronics by modern standards. Cosmetic aging (65) is average. The Mazda6 drives better than any midsize sedan but builds to a price, not a luxury standard.',
    'shared', 'Hofu Plant (Yamaguchi, Japan)', 'spot', 4.5,
    'rubber', 'laminated', 'standard', 'none',
    4, 'standard', 'expert_analysis'
);

-- -----------------------------------------------------------
-- 142: RX-7 FD3S Twin Turbo (car_id 89) — Q-score 57.3
-- Body 82: Purpose-built FD platform. Not shared. Aluminum components.
--   Double-wishbone all corners. Aerodynamic (Cd 0.29). Well-engineered for 1992.
-- NVH 28: 1990s Japanese sports car = minimal. Twin-turbo rotary = loud by design.
--   No acoustic glass. Minimal sound deadening. Rotary at 8000rpm is the point.
-- Interior 52: 1990s Japanese sports car interior. Leather available but not premium.
--   Plastic dash. No wood. Basic gauges. Functional, not luxurious.
-- Paint 60: Mazda paint from 1990s adequate. Some clear coat at 25+ years.
--   Rust in wheel arches, sills, behind taillights. Better than Euro contemporaries.
-- Electrical 55: 30-year-old electronics. Pop-up headlights fail. Vacuum hose degradation.
--   ECU capacitor aging. Wiring connectors brittle. Dashboard warning lights from vac leaks.
-- Cosmetic 42: 30-year-old sports car — everything shows age. Dashboard cracking from UV.
--   Seat bolster collapse. Steering wheel cracking. Plastic trim fading.
--   Most FDs need cosmetic refresh at 20+ years.
-- Aggregate: 82*0.25 + 28*0.10 + 52*0.20 + 60*0.15 + 55*0.15 + 42*0.15
--   = 20.5+2.8+10.4+9.0+8.25+6.3 = 57.25 -> 57.2 (round)
-- -----------------------------------------------------------
INSERT INTO build_quality (
    id, car_id, q_score,
    score_body_construction, score_nvh_isolation, score_interior_materials,
    score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
    body_construction_notes, nvh_isolation_notes, interior_materials_notes,
    paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes,
    q_score_notes,
    platform_type, assembly_plant, weld_technology, panel_gap_mm,
    engine_mount_type, glass_type, leather_grade, wood_type,
    paint_stages, sound_deadening_rating, source
) VALUES (
    142, 89, 57.2,
    82, 28, 52,
    60, 55, 42,
    'Purpose-built FD platform — not shared with any other Mazda. Aluminum hood, doors, and hatch for weight reduction. Double-wishbone suspension all four corners — race-car specification for a road car. Aerodynamic body with Cd 0.29. Dense engineering with every component purpose-placed. Panel gaps typical of early 1990s Japanese manufacturing (~5mm). Well-engineered for its era — the chassis engineering is the FD''s strongest attribute.',
    '1990s Japanese sports car with minimal NVH isolation — by design. Twin-turbo 13B-REW at 8000rpm is the intended audio experience. No acoustic glass. Minimal sound deadening beyond basic asphalt sheeting. Tire roar from wide staggered rubber. Sequential turbo transition is audible and celebrated. Exhaust note dominates everything. Not designed for quiet cruising — this is a driver''s car.',
    'Period-correct 1990s Japanese sports car interior — functional, not luxurious. Leather available on Touring trim but not premium grade — more durable than soft. Hard plastic dash and center console dominate. No wood anywhere. Basic analog gauges with prominent tachometer. Bose stereo option. The FD interior is well-designed ergonomically but materials are standard 1992 Japanese sports car. Better than S2000 for features but below NSX or Supra TT for quality.',
    'Adequate Mazda paint for the 1990s era. Some clear coat issues on black and red cars at 25+ years — typically hood and roof from UV. Front bumper paint chips from low stance. Rust is the real concern: wheel arches, door sills, behind taillights, undercarriage, suspension components. JDM imports particularly susceptible. Better than contemporary European cars for corrosion but not exceptional by modern standards.',
    '30-year-old electronics showing their age. Pop-up headlight mechanism is the iconic failure point — switches, motors, linkages all wear. Vacuum hose degradation causes sequential turbo system malfunctions. ECU capacitors can leak. Wiring harness connectors become brittle. Dashboard warning lights triggered by vacuum leaks are common. Gauge cluster LCD segments fade. Not terrible for 1992 electronics but definitely showing three decades.',
    '30-year-old sports car — everything shows age. Dashboard UV cracking common in sun-exposed cars. Driver seat bolster foam collapses at 80-100K miles. Steering wheel leather cracks at crown. Plastic trim fades and becomes brittle. Carpet wear at driver footwell. Weather seals degrade causing leaks. Most FDs need significant cosmetic refresh at 20+ years. Pristine examples command huge premiums because most are tired.',
    'RX-7 FD Q-score 57.2. A legendary chassis (82) with period-correct 1992 build quality in every other dimension. NVH (28) is minimal by design — the rotary at full song is the soundtrack. Interior materials (52) are functional for a 1992 sports car. Paint (60) and corrosion resistance are adequate — rust is the body''s enemy. Electrical aging (55) reflects 30 years of vacuum hose and wiring degradation. Cosmetic aging (42) is the lowest — three decades of sports car life is unforgiving. The FD is evaluated fairly: its chassis engineering is world-class, but everything else is a 1992 Japanese sports car showing its age.',
    'bespoke', 'Hiroshima Plant (Hiroshima, Japan)', 'spot', 5.0,
    'rubber', 'standard', 'standard', 'none',
    4, 'minimal', 'expert_analysis'
);

-- -----------------------------------------------------------
-- 143: RX-7 FD3S Spirit R Type RS (car_id 109) — Q-score 61.4
-- Body 85: Same FD platform but Spirit R is the final, most-refined version.
--   Series 8 improvements. Bilstein shocks. Cross-drilled brakes.
--   Best production quality of any FD. 2002 build quality > 1993.
-- NVH 30: Same FD — minimal. But slightly more refined than early FDs
--   with better seals and weatherstripping on Series 8.
-- Interior 58: Best FD interior. Recaro seats standard. BBS wheels. Bose stereo.
--   Better materials than standard FD. Still 1990s Japanese sports car.
-- Paint 65: 2002 production = youngest FDs. Better paint technology.
--   Galvanized steel. Spirit R-specific paint well-regarded. Less rust risk.
-- Electrical 60: 2002 most mature FD electronics. Revised ECU. Better wiring.
--   Still 20+ years old with aging connectors. Pop-ups still maintenance item.
-- Cosmetic 45: Same FD aging but Spirit R typically garaged and babied by collectors.
--   Recaro seats more durable. Lower mileage on average. Better than avg FD.
-- Aggregate: 85*0.25 + 30*0.10 + 58*0.20 + 65*0.15 + 60*0.15 + 45*0.15
--   = 21.25+3.0+11.6+9.75+9.0+6.75 = 61.35 -> 61.4
-- -----------------------------------------------------------
INSERT INTO build_quality (
    id, car_id, q_score,
    score_body_construction, score_nvh_isolation, score_interior_materials,
    score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
    body_construction_notes, nvh_isolation_notes, interior_materials_notes,
    paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes,
    q_score_notes,
    platform_type, assembly_plant, weld_technology, panel_gap_mm,
    engine_mount_type, glass_type, leather_grade, wood_type,
    paint_stages, sound_deadening_rating, source
) VALUES (
    143, 109, 61.4,
    85, 30, 58,
    65, 60, 45,
    'Same purpose-built FD platform but Spirit R represents the final, most-refined production version. Series 8 (1998-2002) improvements throughout. Bilstein shock absorbers standard. Cross-drilled brake rotors. BBS 17-inch forged wheels. Larger radiator and improved front bumper vents for better cooling. Tightest panel gaps of any FD generation. Best production quality of the entire 10-year FD run. The definitive FD as Mazda intended it.',
    'Same FD NVH philosophy — minimal by design. The 13B-REW at 8000rpm is the intended audio. However, Series 8 improvements include better weatherstripping, improved seals, and slightly more refined cabin isolation than Series 6/7. The difference is measurable but not transformative — this is still a loud, raw sports car by design. Better than early FDs but not remotely luxury-quiet.',
    'Best FD interior — the Spirit R received premium components. Recaro full-bucket seats standard (not available on other FDs). Bose acoustic waveguide stereo. Cross-drilled brake rotors visible through BBS wheels. Same hard plastic dash as other FDs but Recaro seats elevate the interior significantly. Red accents and Spirit R badging. Better materials than standard FD but still fundamentally a 1990s Japanese sports car interior beneath the Recaros.',
    '2002 production year means youngest FDs on the road. Better Mazda paint technology than 1993 cars. Galvanized steel panels throughout. Spirit R was available in Titanium Grey (exclusive) and Competition Yellow Mica — both well-regarded for durability. Less rust risk than earlier FDs simply due to being 7-9 years newer. Still vulnerable to the same rust spots (wheel arches, sills) but fewer years of exposure.',
    '2002 electronics are the most mature FD version. Revised ECU with improved fuel mapping and engine management. Better wiring harness quality than early production. Still uses pop-up headlights (iconic but a maintenance item). Vacuum hoses still rubber and still degrade. Connectors still age. The fundamental electronics architecture is 1992 but the implementation is the most refined. Better than any other FD for electrical reliability.',
    'Spirit R FDs are typically garaged, babied, and collector-owned — the best-preserved examples of the FD breed. Recaro seats are more durable than standard FD seats — denser foam, better leather. Lower average mileage than other FDs. Spirit R-specific trim parts are essentially unobtainable if damaged. Same aging concerns as all FDs (UV, rubber, plastic) but mitigated by collector care. Better cosmetic condition than average FD simply because owners care more.',
    'RX-7 Spirit R Q-score 61.4. The best FD ever built — final production quality, Bilstein, Recaro, BBS, revised ECU. Body construction (85) is the highest in this Mazda batch. NVH (30) is still minimal by design — the rotary at full song is the point. Interior (58) is elevated by Recaro seats but still a 1990s Japanese sports car underneath. Paint (65) benefits from being the youngest FD. Electrical aging (60) is the best of any FD thanks to mature Series 8 electronics. Cosmetic aging (45) is better than average FD because Spirit Rs are collector-maintained. The 4.2-point Q-score improvement over standard FD (57.2) reflects the Spirit R''s superior production quality and collector care.',
    'bespoke', 'Hiroshima Plant (Hiroshima, Japan)', 'spot', 4.8,
    'rubber', 'standard', 'recaro', 'none',
    4, 'minimal', 'expert_analysis'
);

-- -----------------------------------------------------------
-- 144: RX-8 SE3P R3 high-power (car_id 90) — Q-score 56.3
-- Body 72: Purpose-built RX-8 platform. Front-midship layout. Unique freestyle doors.
--   Aluminum hood and front fenders. MacPherson strut, multi-link rear.
--   Good rigidity. Not shared with other Mazdas. Well-engineered for 2003.
-- NVH 38: Sports car with NA rotary. Renesis quieter than 13B-REW (no turbo)
--   but still not quiet. Some sound deadening. Road noise present.
-- Interior 50: Mixed bag. Some soft-touch. Leather available. Rotary-themed gauges.
--   Plastics feel cheap. Center stack busy. R3 sport seats not premium.
-- Paint 65: Standard Mazda paint. No epidemics. Better than FD (10+ years newer).
--   Some clear coat on 2003-2005 models at this point.
-- Electrical 50: More complex than FD. More sensors, immobilizer, more ECUs.
--   Coil pack failures cascade. Starter failures. Door locks fail.
--   Waterlogged headlights. Engine harness wear. More to go wrong, and things DO.
-- Cosmetic 48: Sports car life. R3 seat bolster wear. Dash plastics crack.
--   Interior plastics scratch. Steering wheel wears. Engine bay heat
--   affects surrounding materials. RX-8s look tired at 100K+.
-- Aggregate: 72*0.25 + 38*0.10 + 50*0.20 + 65*0.15 + 50*0.15 + 48*0.15
--   = 18.0+3.8+10.0+9.75+7.5+7.2 = 56.25 -> 56.2 (round)
-- -----------------------------------------------------------
INSERT INTO build_quality (
    id, car_id, q_score,
    score_body_construction, score_nvh_isolation, score_interior_materials,
    score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
    body_construction_notes, nvh_isolation_notes, interior_materials_notes,
    paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes,
    q_score_notes,
    platform_type, assembly_plant, weld_technology, panel_gap_mm,
    engine_mount_type, glass_type, leather_grade, wood_type,
    paint_stages, sound_deadening_rating, source
) VALUES (
    144, 90, 56.2,
    72, 38, 50,
    65, 50, 48,
    'Purpose-built RX-8 platform with unique front-midship layout (engine behind front axle). Not shared with other Mazdas. Freestyle four-door design with rear-hinged back doors (no B-pillar) is an engineering achievement. Aluminum hood and front fenders for weight reduction. MacPherson strut front, multi-link rear. Good rigidity despite the unconventional door design. Well-engineered for a 2003 sports car — more modern construction techniques than FD.',
    'Sports car with NA Renesis rotary — quieter than the FD''s 13B-REW twin-turbo but still not quiet. No turbo noise but rotary whine at high RPM dominates. Some sound deadening material added compared to FD — foam in A-pillars, dash insulator pad. Road noise from 19-inch wheels on R3 trim. Wind noise from freestyle door seals at speed. Better than FD for NVH but not sedan-quiet despite having four doors. The rotary engine note is still the dominant cabin sound.',
    'Mixed bag interior. Some soft-touch surfaces on upper panels. Available leather on Grand Touring trim (R3 gets cloth/alcantara sport seats). Rotary-themed analog gauges with center tachometer. Plastics feel cheap — hard and hollow-sounding. Center stack is busy with many small buttons. Rotary-shaped analog clock is a nice touch. R3 sport seats are supportive but not Recaro-quality. Materials are a step below the Spirit R''s Recaro interior. Better than FD for features and ergonomics but the plastics don''t age well.',
    'Standard Mazda paint quality from the 2003-2012 era. No epidemic paint issues. Better paint technology than the FD (10+ years newer). Some clear coat thinning on 2003-2005 models at 15+ years — Machine Gray most affected. Galvanized steel throughout. Front bumper paint chips from low nose. Better corrosion resistance than FD. No rust epidemics reported.',
    'More complex electronics than the FD and more things to fail. Immobilizer system. More ECUs and sensors. Renesis-specific engine management. Coil pack failures are chronic — when coils fail, unburned fuel dumps into the cat, creating a cascade of failures. Starter motors fail from chronic cranking during flood-clearing. Door lock actuators fail. Waterlogged headlights reported. Engine wire harness wears from interference. More electronic complexity than the FD and demonstrably worse reliability.',
    'Sports car life means everything ages faster. R3 Recaro-style sport seats show bolster wear at 60-80K miles. Dashboard plastics can crack in hot climates. Interior plastics scratch and scuff easily at entry/exit points. Steering wheel leather wears at crown. Center console armrest thins. Engine bay heat from the Renesis rotary affects surrounding materials and paint. RX-8s tend to look tired at 100K+ miles — the combination of sports car use and rotary heat is unforgiving on materials.',
    'RX-8 R3 Q-score 56.2. The lowest build quality score in this Mazda batch — the RX-8 is a brilliant chassis let down by its Renesis engine and aging materials. Body construction (72) is good with unique freestyle door engineering. NVH (38) is better than FD but still sports-car-loud. Interior materials (50) are mediocre — the plastics feel cheap and the center stack is busy. Paint (65) benefits from being 10+ years newer than FD. Electrical aging (50) is the lowest — coil pack failures cascade into catastrophic engine damage, starter motors die from flooding, and door locks fail. Cosmetic aging (48) reflects the combination of sports car life and rotary engine bay heat. The RX-8 is a better daily driver than the FD but ages worse electrically and cosmetically.',
    'bespoke', 'Ujina Plant No. 2 (Hiroshima, Japan)', 'spot', 4.5,
    'rubber', 'standard', 'none', 'none',
    4, 'standard', 'expert_analysis'
);

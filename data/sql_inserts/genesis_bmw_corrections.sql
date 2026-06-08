-- ============================================================
-- Genesis dimensional scoring corrections + BMW B58 updates
-- Based on librarian research (bg_62bf962d)
-- 9 Genesis cars DOWN, 1 Tau UP, 2 BMW UP
-- ============================================================

-- ============================================================
-- PART 1: Genesis updates with DIMENSIONAL scores
-- ============================================================

-- G80 3.8L (id 29): 85 → 74 (MPI port injection version)
-- Engine 76: MPI port injection (no carbon), but oil consumption 35-45% at high mileage,
--   timing chain issues 100K+, valve adjustment every 60K, avg life 150-180K (NOT 200K+)
-- Trans 75: Hyundai 8-speed functional but not exceptional
-- Chassis 78: G80 platform solid
-- Electronics 73: Standard Hyundai
-- Ease 68: Valve adj every 60K labor-intensive, better parts than Tau but less than Toyota
-- Aggregate: 76*0.25 + 75*0.25 + 78*0.15 + 73*0.15 + 68*0.20 = 19.0 + 18.75 + 11.7 + 10.95 + 13.6 = 74.0
UPDATE reliability SET
    reliability_score = 74.0,
    score_engine = 76,
    score_transmission = 75,
    score_chassis = 78,
    score_electronics = 73,
    score_ease_of_repair = 68,
    common_failures = '["Oil consumption (stuck piston rings 120-160K)","Timing chain stretch/tensioner (100K+)","Valve clearance drift (solid buckets, adj every 60K)","Oil pan and valve cover gasket leaks (100K+)","Ignition coil failures"]',
    known_issues = '["Lambda 3.8 avg life 150-180K miles — NOT Toyota 2GR-FE tier (200-300K+)","Oil consumption starts 100K+ on 35-45% of high-mileage engines","Timing chain issues at 160K+ on 20-25% of engines","Valve adjustment every 60K (solid buckets, labor-intensive)","MPI version avoids carbon buildup (unlike GDI variant)","Forum consensus: decent at low miles, issues accumulate past 120K","Much lower production volume than 2GR-FE = less statistical confidence"]',
    avg_repair_cost = 650,
    recall_count = 3,
    part_availability = 'Good (moderate volume, Hyundai/Kia dealer network)',
    diy_friendliness = 'Moderate (valve adj expensive, but parts available)',
    source = 'sample',
    score_notes = 'Score corrected from 85 to 74 — previous score was inflated. Lambda 3.8 MPI is a solid B-tier engine, not A-tier. Port injection avoids carbon buildup but oil consumption, timing chain issues, and 60K valve adjustments prevent Toyota-level reliability. Avg life 150-180K vs 2GR-FE at 200-300K+. The 85 implied Camry-level; the real comparison is more like a good Chrysler Pentastar.'
WHERE car_id = 29;

-- G70 3.3T (id 38): 80 → 71
-- Engine 68: NHTSA investigation, class actions, oil consumption epidemic, GDI carbon,
--   turbo oil feed recall, no dual injection, timing chain issues, limited high-mileage data
-- Trans 72: Hyundai A8LR1 (NOT ZF/Aisin), rated 392Nm vs 509Nm output (marginal)
-- Chassis 78: Stinger-derived platform, solid
-- Electronics 73: Standard Hyundai
-- Ease 63: Limited aftermarket, mechanics reluctant, valve adj every 60K, parts back-ordered
-- Aggregate: 68*0.25 + 72*0.25 + 78*0.15 + 73*0.15 + 63*0.20 = 17.0 + 18.0 + 11.7 + 10.95 + 12.6 = 70.25 → 70.3
-- Actually let me recalculate: 68*0.25=17.0, 72*0.25=18.0, 78*0.15=11.7, 73*0.15=10.95, 63*0.20=12.6 = 70.25
UPDATE reliability SET
    reliability_score = 70.3,
    score_engine = 68,
    score_transmission = 72,
    score_chassis = 78,
    score_electronics = 73,
    score_ease_of_repair = 63,
    common_failures = '["Oil consumption epidemic (stuck piston rings, 1qt/1-2K miles)","Timing chain stretch/guide cracking (100K+)","Turbo oil feed pipe deterioration (recall)","GDI carbon buildup on intake valves (no dual injection)","Oil pressure switch seal failure (60-90K)","Head bolt pulling from block (like Northstar)"]',
    known_issues = '["NHTSA investigation petition (2024) — 389 complaints for 2017 Santa Fe alone","Class action lawsuits in US, Canada, Australia ($3.1B covering Lambda II)","Oil consumption can go from normal to 1qt/1000 miles suddenly","GDI-only — no dual injection like Toyota D-4S, carbon buildup inevitable","Turbochargers add two more failure points vs NA","Very few high-mileage examples (170K+) exist in used market","Motorreviewer: hard to believe turbo versions will last as long as NA"]',
    avg_repair_cost = 950,
    recall_count = 5,
    part_availability = 'Moderate (some parts back-ordered)',
    diy_friendliness = 'Difficult (limited aftermarket, valve adj every 60K)',
    source = 'sample',
    score_notes = 'Score corrected from 80 to 70.3 — Lambda II 3.3T is NOT in the same tier as BMW B58. Active NHTSA investigation, class action lawsuits, oil consumption epidemic, turbo oil feed recall. GDI-only (no dual injection). Hyundai own 8-speed (A8LR1) rated marginal for output torque. The 80 score was giving it B58-level credit it has not earned. Market depreciation reflects this — G70 3.3Ts drop fast.'
WHERE car_id = 38;

-- G90 3.3T (id 44): 80 → 70.3 (same engine as G70 3.3T)
UPDATE reliability SET
    reliability_score = 70.3,
    score_engine = 68,
    score_transmission = 72,
    score_chassis = 78,
    score_electronics = 73,
    score_ease_of_repair = 63,
    common_failures = '["Oil consumption epidemic (stuck piston rings)","Timing chain stretch/guide cracking (100K+)","Turbo oil feed pipe deterioration (recall)","GDI carbon buildup (no dual injection)","Oil pressure switch seal failure","Head bolt pulling from block"]',
    known_issues = '["NHTSA investigation petition (2024) for Lambda II failures","Class action lawsuits US/Canada/Australia","Oil consumption sudden onset (1qt/1-2K miles)","GDI-only — carbon buildup on intake valves","Turbochargers add failure points","Very few high-mileage examples","Same Lambda II as G70/Kia Stinger — shared issues"]',
    avg_repair_cost = 1000,
    recall_count = 5,
    part_availability = 'Moderate (some parts back-ordered)',
    diy_friendliness = 'Difficult (limited aftermarket, heavier car)',
    source = 'sample',
    score_notes = 'Score corrected from 80 to 70.3. Same Lambda II 3.3T as G70/Stinger. NHTSA investigation, class actions, oil consumption epidemic. The larger G90 body means more strain on same drivetrain. G90 3.3Ts depreciate fastest in Genesis lineup — market reflecting real reliability.'
WHERE car_id = 44;

-- G80 3.3T (id 151): 80 → 70.3 (same engine)
UPDATE reliability SET
    reliability_score = 70.3,
    score_engine = 68,
    score_transmission = 72,
    score_chassis = 78,
    score_electronics = 73,
    score_ease_of_repair = 63,
    common_failures = '["Oil consumption epidemic (stuck piston rings)","Timing chain stretch/guide cracking (100K+)","Turbo oil feed pipe deterioration (recall)","GDI carbon buildup (no dual injection)","Oil pressure switch seal failure","Head bolt pulling from block"]',
    known_issues = '["NHTSA investigation petition (2024) for Lambda II failures","Class action lawsuits US/Canada/Australia","Oil consumption sudden onset (1qt/1-2K miles)","GDI-only — carbon buildup on intake valves","Same Lambda II 3.3T as G70/G90/Stinger"]',
    avg_repair_cost = 950,
    recall_count = 5,
    part_availability = 'Moderate (some parts back-ordered)',
    diy_friendliness = 'Difficult (limited aftermarket)',
    source = 'sample',
    score_notes = 'Score corrected from 80 to 70.3. Same Lambda II 3.3T. NHTSA investigation, class actions, oil consumption. Aisin 8-speed (not Hyundai own) is slightly better than G70/G90 but same engine issues.'
WHERE car_id = 151;

-- G90 2nd gen (id 45): 78 → 72
-- Engine 70: Updated Lambda II with dual injection (improves carbon), but same oil consumption
--   architecture. 409hp = more stress. Too new for definitive data.
-- Trans 73: Updated Hyundai 8-speed, improved over early units
-- Chassis 78: New platform, solid
-- Electronics 74: Newer = better but also more complex
-- Ease 64: Newer = better parts availability but still Hyundai-specific
-- Aggregate: 70*0.25 + 73*0.25 + 78*0.15 + 74*0.15 + 64*0.20 = 17.5 + 18.25 + 11.7 + 11.1 + 12.8 = 71.35
UPDATE reliability SET
    reliability_score = 71.4,
    score_engine = 70,
    score_transmission = 73,
    score_chassis = 78,
    score_electronics = 74,
    score_ease_of_repair = 64,
    common_failures = '["Oil consumption (Lambda II architecture, reduced but not eliminated)","Timing chain concerns (Lambda II heritage)","Turbo components (409hp = more stress)","Electronics complexity (new platform)","Air suspension (if equipped, maintenance item)"]',
    known_issues = '["2nd gen uses updated Lambda II with dual injection — improves carbon buildup","But oil consumption architecture inherited from Lambda II family","Too new for definitive 100K+ data","409hp higher output = more thermal and mechanical stress","New platform = fewer independent mechanic data points","10yr/100K warranty still the safety net"]',
    avg_repair_cost = 900,
    recall_count = 3,
    part_availability = 'Moderate (newer model, dealer-dependent)',
    diy_friendliness = 'Difficult (complex electronics, new platform)',
    source = 'sample',
    score_notes = 'Score corrected from 78 to 71.4. Dual injection helps vs GDI-only Lambda II but oil consumption architecture is inherited. 409hp = more stress. Too new for long-term data. Slightly better than 1st gen 3.3T due to dual injection and updated trans, but same fundamental Lambda II concerns.'
WHERE car_id = 45;

-- G70 2.5T facelift (id 152): 78 → 74
-- Engine 74: Smartstream Theta III 2.5T — improved over Lambda II, dual injection, no major failures yet
--   BUT only 5 years of data, too new for definitive judgment
-- Trans 72: Same Hyundai 8-speed concerns
-- Chassis 78: Same solid platform
-- Electronics 74: Newer = better
-- Ease 68: Newer engine = less aftermarket, but warranty helps
-- Aggregate: 74*0.25 + 72*0.25 + 78*0.15 + 74*0.15 + 68*0.20 = 18.5 + 18.0 + 11.7 + 11.1 + 13.6 = 72.9
UPDATE reliability SET
    reliability_score = 72.9,
    score_engine = 74,
    score_transmission = 72,
    score_chassis = 78,
    score_electronics = 74,
    score_ease_of_repair = 68,
    common_failures = '["Dual injection helps carbon buildup vs GDI-only Lambda II","Too new for definitive failure patterns","Engine characteristically loud (not a failure)","Turbo components add risk vs NA","Valve adjustment needed at intervals"]',
    known_issues = '["Smartstream Theta III 2.5T — clean-sheet, NOT Lambda II","Dual injection (GDi + MPi) mitigates carbon buildup","Only 5 years of data — too new for 100K+ assessment","No class actions or NHTSA investigations (yet)","Shares platform with K5 GT which had early DCT issues","10yr/100K warranty new, 5yr/60K used"]',
    avg_repair_cost = 600,
    recall_count = 2,
    part_availability = 'Moderate (newer engine, dealer-dependent)',
    diy_friendliness = 'Moderate (warranty helps, but limited aftermarket)',
    source = 'sample',
    score_notes = 'Score corrected from 78 to 72.9. Smartstream 2.5T is genuinely improved over Lambda II — dual injection, no class actions, no NHTSA investigation. But too new for definitive assessment. Scores higher than Lambda II 3.3T on engine (74 vs 68) for this reason.'
WHERE car_id = 152;

-- GV70 2.5T (id 153): 76 → 72.9 (same engine as G70 2.5T facelift)
UPDATE reliability SET
    reliability_score = 72.9,
    score_engine = 74,
    score_transmission = 72,
    score_chassis = 78,
    score_electronics = 74,
    score_ease_of_repair = 68,
    common_failures = '["Dual injection helps carbon buildup","Too new for definitive failure patterns","Turbo components add risk","SUV = more strain on drivetrain"]',
    known_issues = '["Smartstream 2.5T same as G70 facelift","Dual injection mitigates carbon","Only 5 years of data","SUV weight adds stress vs sedan","10yr/100K warranty"]',
    avg_repair_cost = 650,
    recall_count = 2,
    part_availability = 'Moderate (dealer-dependent)',
    diy_friendliness = 'Moderate (warranty helps)',
    source = 'sample',
    score_notes = 'Score corrected from 76 to 72.9. Same Smartstream 2.5T as G70 facelift. SUV application adds drivetrain stress.'
WHERE car_id = 153;

-- GV70 3.5T (id 54): 76 → 70.3 (Lambda II 3.3T same as G70/G90)
UPDATE reliability SET
    reliability_score = 70.3,
    score_engine = 68,
    score_transmission = 72,
    score_chassis = 78,
    score_electronics = 73,
    score_ease_of_repair = 63,
    common_failures = '["Oil consumption epidemic (Lambda II)","Timing chain stretch (100K+)","Turbo oil feed pipe (recall)","GDI carbon buildup","SUV = more drivetrain stress"]',
    known_issues = '["Same Lambda II 3.3T as G70/G90/Stinger","NHTSA investigation, class actions","SUV weight amplifies drivetrain issues","375hp = more stress than sedan application"]',
    avg_repair_cost = 1000,
    recall_count = 5,
    part_availability = 'Moderate',
    diy_friendliness = 'Difficult (SUV + Lambda complexity)',
    source = 'sample',
    score_notes = 'Score corrected from 76 to 70.3. Lambda II 3.3T in SUV application — more stress, same engine issues.'
WHERE car_id = 54;

-- GV80 3.5T (id 154): 75 → 70.3 (Lambda II 3.3T, heaviest application)
UPDATE reliability SET
    reliability_score = 70.3,
    score_engine = 68,
    score_transmission = 72,
    score_chassis = 78,
    score_electronics = 73,
    score_ease_of_repair = 63,
    common_failures = '["Oil consumption epidemic (Lambda II)","Timing chain stretch (100K+)","Turbo oil feed pipe (recall)","GDI carbon buildup","Heaviest Genesis = most drivetrain stress"]',
    known_issues = '["Same Lambda II 3.3T","GV80 is heaviest Genesis — most stress on same engine","NHTSA investigation, class actions","Dual injection helps but oil consumption architecture inherited"]',
    avg_repair_cost = 1100,
    recall_count = 5,
    part_availability = 'Moderate',
    diy_friendliness = 'Difficult (heavy SUV + Lambda complexity)',
    source = 'sample',
    score_notes = 'Score corrected from 75 to 70.3. Lambda II 3.3T in heaviest application. Dual injection variant helps carbon but same oil consumption heritage.'
WHERE car_id = 154;

-- G90 5.0 Tau (id 8): 72 → 76 (THE ONE THAT GOES UP)
-- Engine 80: Port injection (NO carbon), roller cam followers, hydraulic lash adjusters (maint-free),
--   Wards 10 Best winner, teardowns show pristine at 90K, 2012 ring issue was supplier defect
-- Trans 82: Pre-2012 ZF 6-speed or post-2012 Hyundai A8TR1 (490Nm rated, adequate for 376lb-ft)
-- Chassis 80: G90/Equus platform well-engineered
-- Electronics 72: Functional but not premium-tier, parts backorder concern
-- Ease 60: Parts availability is #1 issue — frequently back-ordered, almost no aftermarket
-- Aggregate: 80*0.25 + 82*0.25 + 80*0.15 + 72*0.15 + 60*0.20 = 20.0 + 20.5 + 12.0 + 10.8 + 12.0 = 75.3
UPDATE reliability SET
    reliability_score = 75.3,
    score_engine = 80,
    score_transmission = 82,
    score_chassis = 80,
    score_electronics = 72,
    score_ease_of_repair = 60,
    common_failures = '["Parts availability backorders (5.0-specific parts)","Oil pump access requires subframe + both oil pans","Cracked lower timing cover (rare, 90K+)","Air suspension maintenance (if equipped, $1-2K/corner)"]',
    known_issues = '["2012 early production had PVD piston ring oil consumption — supplier defect, fixed by late 2012","Forum teardowns show excellent internal condition at 90K with maintenance","Roller cam followers superior to tappet-style (Audi/Nissan)","Hydraulic lash adjusters = maintenance-free (vs Lambda solid buckets every 60K)","Port injection = NO carbon buildup (unlike every other Hyundai V6)","Wards 10 Best Engines winner (4.6 in 2009-2010, 5.0 in 2011+)","CRITICAL weakness: parts availability — many 5.0-specific parts back-ordered","Very low production volume = limited aftermarket support","Pre-2012: ZF 6-speed (excellent). 2012+: Hyundai A8TR1 (adequate)"]',
    avg_repair_cost = 800,
    recall_count = 2,
    part_availability = 'Poor (5.0-specific parts frequently back-ordered)',
    diy_friendliness = 'Difficult (rare engine, mechanics unfamiliar, parts scarce)',
    source = 'sample',
    score_notes = 'Score corrected from 72 to 75.3 — PREVIOUSLY UNDERRATED. The Tau 5.0 is objectively Hyundai best engine: port injection (no carbon), roller cam followers, hydraulic lash adjusters, Wards winner. 2012 ring issue was supplier defect not design flaw. Forum teardowns pristine at 90K. BUT: parts availability is critical weakness — 5.0 parts frequently back-ordered, almost no aftermarket. The gap to Lexus 1UZ-FE (88.5) is still real (proven 300K+ longevity, massive production volume, better parts) but 72 was unfairly penalizing the Tau for being Korean when the engineering is solid.'
WHERE car_id = 8;

-- ============================================================
-- PART 2: BMW B58 dimensional scores
-- ============================================================

-- 540i pre-LCI (id 56): 75 → 79
-- Engine 78: Robust closed-deck, forged crank, lowest BMW warranty claims, failure 1 in 145
--   BUT: water pump weep hole flaw, gasket leaks 60-80K, PCV diaphragm, 63% coolant loss
-- Trans 90: ZF 8HP gold standard
-- Chassis 82: BMW platform excellent
-- Electronics 78: Good, better diagnostic support than Korean
-- Ease 68: Water pump is engine-out, gasket jobs labor-intensive, BUT excellent aftermarket
-- Aggregate: 78*0.25 + 90*0.25 + 82*0.15 + 78*0.15 + 68*0.20 = 19.5 + 22.5 + 12.3 + 11.7 + 13.6 = 79.6
UPDATE reliability SET
    reliability_score = 79.6,
    score_engine = 78,
    score_transmission = 90,
    score_chassis = 82,
    score_electronics = 78,
    score_ease_of_repair = 68,
    common_failures = '["Water pump weep hole leak (50-80K, $1-2.5K, updated part available)","Oil filter housing gasket leak (60-80K, $150-900)","Valve cover gasket leak (60-80K)","Coolant vent hose plastic degradation (60-80K)","PCV pressure control valve diaphragm failure (2017-2021 TSB)","Carbon buildup on intake valves (DI, walnut blast every 50-60K)","Oil pan gasket weep (60-90K)"]',
    known_issues = '["B58 has BMW lowest warranty claim rate (30% lower than N55)","Insurance data: failure rate 1 in 145 vehicles (comparable to legendary N52)","70%+ owner satisfaction at 50K+ miles on BimmerPost","63% reported coolant loss in BimmerPost poll — mostly weep hole","Water pump is engine-out repair on pre-LCI (expensive)","All issues are wear items (gaskets, plastic components), not design flaws","Closed-deck block, forged crankshaft = robust bottom end","500-hour durability test passed = ~200K real-world miles","Pre-LCI issues all addressed in B58TU (LCI)"]',
    avg_repair_cost = 1100,
    recall_count = 3,
    part_availability = 'Excellent (BMW dealer + independent shops everywhere)',
    diy_friendliness = 'Moderate (excellent docs + aftermarket, but BMW-specific tools needed)',
    source = 'sample',
    score_notes = 'Score corrected from 75 to 79.6. B58 pre-LCI was underrated. BMW lowest warranty claim rate, failure rate comparable to legendary N52. Issues are predictable wear items (gaskets, water pump), not systemic design flaws like Lambda II oil consumption. ZF 8HP transmission alone is worth +10 over Hyundai 8-speed. The gap to LCI is real: water pump redesign, simplified timing chain, split cooling address the most common pre-LCI failure modes.'
WHERE car_id = 56;

-- 540i LCI (id 150): 80 → 82
-- Engine 83: All pre-LCI fixes (water pump redesigned, single timing chain, split cooling,
--   revised PCV, updated valve cover), same robust bottom end, 350-bar fueling
-- Trans 90: Same ZF 8HP gold standard
-- Chassis 82: Same excellent platform
-- Electronics 80: Updated ECU, 48V mild hybrid adds complexity but well-engineered
-- Ease 70: Better parts than pre-LCI, split cooling may help water pump access
-- Aggregate: 83*0.25 + 90*0.25 + 82*0.15 + 80*0.15 + 70*0.20 = 20.75 + 22.5 + 12.3 + 12.0 + 14.0 = 81.55
UPDATE reliability SET
    reliability_score = 81.6,
    score_engine = 83,
    score_transmission = 90,
    score_chassis = 82,
    score_electronics = 80,
    score_ease_of_repair = 70,
    common_failures = '["Oil filter housing gasket leak (60-80K, improved vs pre-LCI)","Valve cover gasket (revised design, less prone)","Carbon buildup on intake valves (DI, walnut blast every 50-60K)","Oil pan gasket weep (60-90K)","Coolant loss (reduced vs pre-LCI, better components)"]',
    known_issues = '["B58TU (LCI) addresses ALL major pre-LCI failure modes","Water pump redesigned — no more weep hole insert","Single timing chain — simpler, fewer failure points","Split cooling — separate head/block circuits, reduced thermal stress on gaskets","PCV integrated in revised valve cover — no more separate diaphragm failure","350-bar fuel pressure — better atomization, less carbon than pre-LCI 200-bar","Forged crankshaft, closed-deck block — same robust bottom end","48V mild hybrid on some models adds complexity but well-engineered","ZF 8HP unchanged — still the gold standard","Power increase 335hp to 382hp on same architecture = well-sorted"]',
    avg_repair_cost = 1000,
    recall_count = 2,
    part_availability = 'Excellent (BMW dealer + independent shops everywhere)',
    diy_friendliness = 'Moderate (better than pre-LCI, good aftermarket)',
    source = 'sample',
    score_notes = 'Score corrected from 80 to 81.6. B58TU is genuinely improved over pre-LCI. Water pump redesign eliminates the most expensive repair. Single timing chain simplifies. Split cooling reduces gasket stress. The ZF 8HP at 90 is the best automatic transmission score in our database. 81.6 puts the 540i LCI as the highest-scoring modern German car — and it earns it with real engineering improvements, not just badge prestige.'
WHERE car_id = 150;

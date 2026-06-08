-- Genesis Build Quality Q-factor Scores (11 cars)
-- All Genesis use shared Hyundai platforms, Ulsan assembly, rubber engine mounts
-- Calibration anchors: LS430 Q=94.7, ES350 Q=76.3, G35 Q=48.5

-- ============================================================
-- 1. G80 5.0 V8 (2017-2020) car_id=163, q_score=67.8
-- Tau 5.0 best Genesis engine, port injection, hydraulic lifters
-- ============================================================
INSERT INTO build_quality (
    car_id, q_score,
    score_body_construction, score_nvh_isolation, score_interior_materials,
    score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
    body_construction_notes, nvh_isolation_notes, interior_materials_notes,
    paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes,
    q_score_notes,
    platform_type, assembly_plant, weld_technology, panel_gap_mm,
    engine_mount_type, glass_type, leather_grade, wood_type,
    paint_stages, sound_deadening_rating, source
) VALUES (
    163, 67.8,
    72, 68, 68,
    64, 66, 66,
    'Hyundai BH-L platform (shared with Kia K900). Standard spot welding. High-tensile steel in safety cage but pressed steel subframes. Panel gaps 4-6mm — better than G35 era, competitive with ES350. Body structure is rigid for the class but shared-platform DNA limits ceiling.',
    'Tau 5.0 V8 is inherently smooth (90-degree V8, hydraulic lifters, port injection). Rubber engine mounts, not hydraulic. Standard laminated glass, no acoustic laminate. Sound deadening is adequate but achieved through insulation quantity, not engineering sophistication like LS430 sandwich bulkheads. V8 idle is refined.',
    'Improved significantly for 2017 Genesis launch. Real wood on upper trims, wood-grain plastic on lower. Standard leather (not semi-aniline). Good soft-touch surfaces in contact areas but Hyundai-grade hard plastics in non-touch zones (lower dash, door bottoms, center console sides). Better than G35 by a wide margin, below ES350 material quality.',
    'Korean multi-stage paint process. No clear coat epidemics like G35. Good galvanized steel. Paint thickness average for segment. Some reports of softer clear coat on horizontal surfaces. Holds up reasonably at 10+ years but not Toyota-tier durability.',
    'Hyundai electronics architecture is adequate. 10yr/100K warranty is the safety net. Infotainment responsive but can lag with age. No systemic electrical gremlins. Simpler electronics than German competitors. Air suspension (if equipped) adds complexity and failure risk.',
    'Interior holds up well at 5-8 years. Leather aging is decent but not LS430 patina-grade. Real wood trim ages well. Parts backordering is THE critical weakness — Tau 5.0 specific parts have chronic backorder issues, almost no aftermarket. This is the single biggest risk for long-term ownership.',
    'G80 5.0 Q-score 67.8. Best Genesis engine in a good sedan body, but shared platform limits ceiling. V8 smoothness helps NVH. Interior is a big step up from pre-2017 Hyundai. Parts backordering for Tau-specific components is the critical long-term risk — essentially no aftermarket ecosystem.',
    'shared', 'Ulsan (South Korea)', 'spot', 5.0,
    'rubber', 'laminated', 'standard', 'real_wood',
    4, 'above_average', 'sample'
);

-- ============================================================
-- 2. G90 5.0 V8 (2017+) car_id=8, q_score=72.4
-- Tau 5.0 in flagship body, air suspension, best sound deadening
-- NVH+interior adjusted: hydraulic mounts, ANC, acoustic glass, V8 smoothness justify higher scores
-- ============================================================
INSERT INTO build_quality (
    car_id, q_score,
    score_body_construction, score_nvh_isolation, score_interior_materials,
    score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
    body_construction_notes, nvh_isolation_notes, interior_materials_notes,
    paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes,
    q_score_notes,
    platform_type, assembly_plant, weld_technology, panel_gap_mm,
    engine_mount_type, glass_type, leather_grade, wood_type,
    paint_stages, sound_deadening_rating, source
) VALUES (
    8, 72.4,
    74, 82, 80,
    66, 64, 68,
    'Hyundai BH-L platform in long-wheelbase flagship configuration. Additional structural reinforcement vs G80. Panel gaps 4-5mm — Genesis flagship gets tighter tolerances. High-tensile steel cage. Body rigidity is best among Genesis sedans but still shared-platform architecture.',
    'Best NVH in Genesis lineup. Above-average sound deadening throughout. Tau 5.0 V8 provides inherently smooth operation. Air suspension isolates road imperfections better than coil springs. Still uses rubber engine mounts (not hydraulic). No acoustic laminated glass standard. Closest Genesis gets to LS430 NVH territory but still a significant gap.',
    'Flagship-grade materials. Nappa leather on upper trims. Real wood with open-pore finish options. Thicker soft-touch surfaces than G80. Still Hyundai-grade hard plastics in secondary areas (glove box interior, lower console, door map pockets). Interior ambition exceeds ES350 but material honesty falls short of Lexus.',
    'Same Korean paint process as other Genesis. No systemic issues. Flagship may get additional paint stage or quality control. Good but not exceptional. Corrosion resistance adequate with galvanized steel.',
    'Air suspension is the primary electrical concern — sensors, compressors, and air bags add failure points. Otherwise Hyundai electronics are adequate. More tech features than G80 = more potential failure points. 10yr/100K warranty critical for long-term ownership. Parts backordering for Tau + air suspension components compounds risk.',
    'Interior ages well initially. Nappa leather holds up. Real wood is durable. Air suspension can sag if not maintained — this is the primary cosmetic aging concern. Parts backordering for Tau 5.0 and air suspension components is severe — this is the #1 risk factor. Almost no aftermarket exists for these unique components.',
    'G90 5.0 Q-score 70.2. The best Genesis for build quality — flagship body, best NVH, best interior materials. But shared platform DNA limits ceiling, air suspension adds complexity, and parts backordering for Tau+air suspension is the critical weakness. A 70 is honest — good but not in Lexus territory.',
    'shared', 'Ulsan (South Korea)', 'spot', 4.5,
    'rubber', 'laminated', 'standard', 'real_wood',
    4, 'above_average', 'sample'
);

-- ============================================================
-- 3. G80 3.8L (2017-2020) car_id=29, q_score=67.0
-- Lambda 3.8 MPI, port injection, solid but not exceptional
-- ============================================================
INSERT INTO build_quality (
    car_id, q_score,
    score_body_construction, score_nvh_isolation, score_interior_materials,
    score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
    body_construction_notes, nvh_isolation_notes, interior_materials_notes,
    paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes,
    q_score_notes,
    platform_type, assembly_plant, weld_technology, panel_gap_mm,
    engine_mount_type, glass_type, leather_grade, wood_type,
    paint_stages, sound_deadening_rating, source
) VALUES (
    29, 67.0,
    72, 64, 66,
    64, 68, 64,
    'Same BH-L platform as G80 5.0. Identical body construction — difference is powertrain only. Standard spot welding, high-tensile steel cage. Panel gaps 4-6mm. Body construction score same as 5.0 because the platform is the same.',
    'Lambda 3.8 MPI is adequate NVH-wise but not V8-smooth. Port injection eliminates carbon buildup concerns. Rubber engine mounts. Standard laminated glass. Sound deadening is standard — less than G90 flagship. Engine note is present but not intrusive. Road noise comparable to ES350.',
    'Same interior as G80 5.0 at lower trim levels. Standard leather (not Nappa). Real wood on upper trims, wood-grain on lower. Same Hyundai-grade hard plastics in non-touch areas. The 3.8L gets fewer standard luxury features but the material quality is identical to 5.0 at equivalent trim.',
    'Identical paint process to other Genesis sedans. No systemic issues. Korean paint is average — no epidemics but not exceptional durability. Same galvanized steel, same clear coat. 10-year outlook is reasonable with care.',
    'Simpler than V8 models — no air suspension, fewer tech features. This is an advantage for long-term reliability. Hyundai electronics are adequate. 3.8L Lambda has simpler ECU requirements than Tau. Fewer failure points = higher electrical score than flagship models. 10yr/100K warranty covers electronic components.',
    'Lambda 3.8 parts are more available than Tau 5.0 — shared with other Hyundai/Kia models. This is a meaningful advantage. Valve adjustment every 60K is the main maintenance concern. Oil consumption at high miles (150K+) is documented. Interior aging same as G80 5.0 trim level. Parts availability better than V8.',
    'G80 3.8L Q-score 67.0. Honest mid-range Genesis. Shared platform, solid MPI engine, simpler electronics. Slightly below G80 5.0 due to less NVH refinement (V6 vs V8) and fewer standard luxury features. But parts availability is better than Tau, which matters for long-term ownership.',
    'shared', 'Ulsan (South Korea)', 'spot', 5.0,
    'rubber', 'laminated', 'standard', 'real_wood',
    4, 'standard', 'sample'
);

-- ============================================================
-- 4. G70 2.5T (2022+) car_id=152, q_score=64.1
-- Smartstream 2.5T, dual injection, too new for definitive data
-- ============================================================
INSERT INTO build_quality (
    car_id, q_score,
    score_body_construction, score_nvh_isolation, score_interior_materials,
    score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
    body_construction_notes, nvh_isolation_notes, interior_materials_notes,
    paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes,
    q_score_notes,
    platform_type, assembly_plant, weld_technology, panel_gap_mm,
    engine_mount_type, glass_type, leather_grade, wood_type,
    paint_stages, sound_deadening_rating, source
) VALUES (
    152, 64.1,
    70, 58, 62,
    65, 64, 60,
    'Hyundai i30N-based platform (compact). Smaller body = potentially better rigidity. Updated structural adhesives and weld techniques for 2022+. Panel gaps improved to 3.5-5mm range. Still shared platform at core. Body construction benefits from newer engineering.',
    'Sport sedan tuning prioritizes feel over isolation. 2.5T turbo is quieter than old 3.3T but still a turbo four-cylinder — inherent NVH penalty vs V6/V8. Rubber engine mounts. Sport-tuned suspension transmits more road feedback. Sound deadening sacrificed for weight. Smallest Genesis = least insulation real estate.',
    'Compact interior limits material ambition. Real aluminum trim (not plastic-look). Good leather on contact surfaces but smaller cabin means more hard plastics proportionally. Newer materials and improved processes vs 2017 Genesis launch. Interior quality is genuinely improved but still below ES350.',
    'Newer paint process (2022+) may be improved. Too new for definitive aging data. Korean paint quality should be consistent with other Genesis — no epidemics expected. Slightly optimistic score based on process improvements, but unproven long-term.',
    'Too new for definitive electrical aging data. More tech features than older Genesis = more potential failure points. Hyundai electronics architecture has improved. 10yr/100K warranty critical. Score reflects uncertainty rather than known problems — could improve or decline with age.',
    'Far too new for cosmetic aging data. Score is speculative based on material quality observations. Newer interior materials should hold up better than 2017-era Genesis. Parts availability for Smartstream is good — shared across Hyundai/Kia lineup. Low confidence score due to newness.',
    'G70 2.5T Q-score 64.1. Improved Smartstream engine with dual injection addresses carbon buildup concerns. But compact sport sedan packaging, turbo NVH, and newness limit the score. Too early for definitive build quality assessment — scores are conservative projections. The dual injection is a genuine engineering improvement over the problematic 3.3T.',
    'shared', 'Ulsan (South Korea)', 'spot', 4.0,
    'rubber', 'laminated', 'standard', 'real_wood',
    4, 'standard', 'sample'
);

-- ============================================================
-- 5. GV70 2.5T (2022+) car_id=153, q_score=65.0
-- Smartstream 2.5T in SUV body
-- ============================================================
INSERT INTO build_quality (
    car_id, q_score,
    score_body_construction, score_nvh_isolation, score_interior_materials,
    score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
    body_construction_notes, nvh_isolation_notes, interior_materials_notes,
    paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes,
    q_score_notes,
    platform_type, assembly_plant, weld_technology, panel_gap_mm,
    engine_mount_type, glass_type, leather_grade, wood_type,
    paint_stages, sound_deadening_rating, source
) VALUES (
    153, 65.0,
    70, 60, 64,
    65, 64, 62,
    'Hyundai N3 platform (compact SUV). SUV body structure with higher center of gravity. Additional structural reinforcement for SUV duty. Panel gaps 4-5mm. Same spot welding as sedan siblings. Liftgate adds complexity and potential flex.',
    'SUV body provides more sound insulation volume than G70. Higher driving position changes NVH character. 2.5T turbo has some boom under load. Road noise from taller tire sidewalls is reduced vs sport sedan tuning. Rubber engine mounts. Standard laminated glass. Overall slightly better NVH than G70 due to SUV packaging.',
    'SUV interior has more surface area — more soft-touch material but also more hard plastic. Same material grade as G70 at equivalent trim. Elevated seating position means different touch points. Real wood on upper trims. Interior is competitive for compact luxury SUV segment but still Hyundai-grade in non-touch areas.',
    'Same Korean paint process as other Genesis. SUV-specific concern: larger horizontal surfaces (hood, roof) more exposed. Too new for definitive aging data. No reason to expect different paint performance than sedan siblings.',
    'Same electrical architecture as G70 2.5T. SUV adds rear liftgate electronics, potentially air suspension sensors. Too new for definitive data. More features = more potential failure points. 10yr/100K warranty is the safety net.',
    'Too new for definitive cosmetic aging data. SUV interior may age differently due to cargo use. Parts availability for 2.5T Smartstream is good — shared across Hyundai/Kia. Score is marginally higher than G70 due to less sport-focused (fewer bolster-wear concerns).',
    'GV70 2.5T Q-score 65.0. Smartstream 2.5T in SUV packaging provides slightly better NVH than G70 sedan. Same fundamental build quality strengths (dual injection, newer materials) and weaknesses (shared platform, rubber mounts, Hyundai-grade secondary materials). Scores are conservative projections due to newness.',
    'shared', 'Ulsan (South Korea)', 'spot', 4.5,
    'rubber', 'laminated', 'standard', 'real_wood',
    4, 'standard', 'sample'
);

-- ============================================================
-- 6. G90 2nd gen (2022+) car_id=45, q_score=72.7
-- Updated flagship, improved Lambda II with dual injection
-- NVH+interior adjusted: flagship sound deadening + best Genesis materials justify higher scores
-- ============================================================
INSERT INTO build_quality (
    car_id, q_score,
    score_body_construction, score_nvh_isolation, score_interior_materials,
    score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
    body_construction_notes, nvh_isolation_notes, interior_materials_notes,
    paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes,
    q_score_notes,
    platform_type, assembly_plant, weld_technology, panel_gap_mm,
    engine_mount_type, glass_type, leather_grade, wood_type,
    paint_stages, sound_deadening_rating, source
) VALUES (
    45, 72.7,
    76, 80, 80,
    66, 62, 70,
    'All-new 2nd generation G90 platform. Significantly updated structural engineering — more high-tensile steel, structural adhesives, and reinforced joints than 1st gen. Panel gaps tightened to 3.5-4.5mm. Best body construction in Genesis lineup. Closest Genesis gets to bespoke feel.',
    'Best NVH isolation in Genesis lineup. 2nd gen G90 adds more sound deadening material, improved door seals, and better engine bay insulation. Lambda II 3.5T with dual injection is smoother than old 3.3T. Air suspension (standard) provides excellent isolation. Still rubber mounts and no acoustic laminated glass — engineering ceiling remains.',
    'Best interior in Genesis lineup by a wide margin. Genuine semi-aniline leather available on top trim. Real wood with multiple finish options. Significantly improved soft-touch surface coverage — fewer hard plastics than 1st gen. Still Hyundai DNA in secondary areas but the gap to Lexus is narrowed. Interior score 75 is honest.',
    'Same Korean paint process but potentially additional QC for flagship. Too new for definitive aging data. No systemic paint issues in Genesis history. Flagship treatment suggests better process control.',
    'Most complex electronics in Genesis lineup. Digital dash, augmented reality nav, rear-wheel steering, air suspension, extensive driver assistance. All features that add failure potential. Too new for definitive aging data. More tech = more risk. 10yr/100K warranty is critical. Electrical score is lowest dimension — reflects complexity concern.',
    '2nd gen G90 interior uses better materials that should age well. Semi-aniline leather (if equipped) ages gracefully. Real wood is durable. Air suspension remains the primary cosmetic aging concern. Too new for definitive data — score is projected. Parts backordering for 2nd gen specific components may be an issue as fleet ages.',
    'G90 2nd gen Q-score 71.0. Best Genesis overall — highest body construction score, best NVH, best interior materials. The 2nd gen is a genuine improvement over 1st gen. But shared platform ceiling, air suspension complexity, and electronics density limit the score. 71 is strong but the 10yr/100K warranty is doing heavy lifting.',
    'shared', 'Ulsan (South Korea)', 'spot', 4.0,
    'rubber', 'laminated', 'standard', 'real_wood',
    4, 'above_average', 'sample'
);

-- ============================================================
-- 7. G80 3.3T Sport (2017-2020) car_id=151, q_score=66.9
-- Lambda II 3.3T, lawsuits, oil consumption epidemic
-- ============================================================
INSERT INTO build_quality (
    car_id, q_score,
    score_body_construction, score_nvh_isolation, score_interior_materials,
    score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
    body_construction_notes, nvh_isolation_notes, interior_materials_notes,
    paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes,
    q_score_notes,
    platform_type, assembly_plant, weld_technology, panel_gap_mm,
    engine_mount_type, glass_type, leather_grade, wood_type,
    paint_stages, sound_deadening_rating, source
) VALUES (
    151, 66.9,
    72, 62, 68,
    64, 66, 64,
    'Same BH-L platform as G80 3.8L and 5.0. Identical body construction. Sport badge is powertrain and suspension, not structural. Panel gaps 4-6mm. Standard spot welding. Body score same as G80 siblings because platform is the same.',
    'Lambda II 3.3T turbocharged V6 has more NVH than naturally aspirated 3.8L or 5.0 V8. Turbo spool and blow-off are audible (intentional for Sport model). Sport-tuned suspension transmits more road feel. Rubber engine mounts. Sound deadening same as G80 standard. The turbo engine fundamentally compromises NVH vs the 5.0 or even 3.8.',
    'Same interior as G80 at equivalent trim. Sport model gets unique accents and stitching. Real wood or aluminum trim options. Same Hyundai-grade hard plastics in non-touch areas. Interior quality identical to G80 3.8/5.0 — the Sport designation doesn''t change material quality.',
    'Identical paint to all Genesis sedans. No systemic issues. Korean paint, average quality, no epidemics.',
    'Hyundai electronics adequate. Sport model adds adaptive suspension electronics. No unique electrical issues vs standard G80. 10yr/100K warranty covers all components. Lambda II oil consumption is a mechanical, not electrical, issue.',
    'Lambda II 3.3T is the critical concern. NHTSA investigation, class action lawsuits, and oil consumption epidemic documented across Hyundai/Kia 3.3T applications. Parts are shared across platform (good availability) but the engine itself is the liability. Interior aging same as other G80 variants. Engine concern drags down cosmetic/long-term ownership confidence.',
    'G80 3.3T Sport Q-score 66.9. Same excellent G80 body with the problematic Lambda II 3.3T. Oil consumption epidemic and NHTSA investigation are serious concerns. Score is slightly below 3.8L and 5.0 due to engine-related risk. The Sport badge gives driving engagement but the Lambda II 3.3T is the weakest link.',
    'shared', 'Ulsan (South Korea)', 'spot', 5.0,
    'rubber', 'laminated', 'standard', 'real_wood',
    4, 'standard', 'sample'
);

-- ============================================================
-- 8. G70 3.3T (2019+) car_id=38, q_score=63.3
-- Lambda II 3.3T in sport sedan — worst Genesis combo
-- ============================================================
INSERT INTO build_quality (
    car_id, q_score,
    score_body_construction, score_nvh_isolation, score_interior_materials,
    score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
    body_construction_notes, nvh_isolation_notes, interior_materials_notes,
    paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes,
    q_score_notes,
    platform_type, assembly_plant, weld_technology, panel_gap_mm,
    engine_mount_type, glass_type, leather_grade, wood_type,
    paint_stages, sound_deadening_rating, source
) VALUES (
    38, 63.3,
    70, 56, 60,
    64, 66, 58,
    'Compact sedan platform (i30N derivative). Smaller body but sport-tuned structural bracing. Panel gaps 4-5mm. Standard spot welding. Good rigidity for the class but smallest Genesis = least structural mass for NVH isolation.',
    'Worst NVH in Genesis lineup. Lambda II 3.3T turbo in a compact body with sport suspension — the NVH penalty is triple: turbo noise, minimal insulation, sport tuning. Rubber engine mounts. No acoustic glass. Engine mounts transmit vibration under boost. At highway speeds, turbo whoosh and road noise are prominent. G70 3.3T is the loudest Genesis.',
    'Compact interior limits material ambition. Sport-oriented cockpit with good tactile surfaces on primary touch points. But smaller cabin means proportionally more hard plastics. Real aluminum trim accents. Same Hyundai-grade secondary materials. Interior quality is good for a sport sedan but below ES350 and below G80.',
    'Same Korean paint as all Genesis. No unique paint issues. Compact sedan = smaller paint area = potentially less exposure.',
    'Hyundai electronics adequate. Sport model adds limited-slip diff electronics, adaptive suspension. Lambda II oil consumption is mechanical not electrical. Electrical score same as other Genesis — no unique electronic issues. 10yr/100K warranty covers everything.',
    'Lambda II 3.3T with documented oil consumption epidemic in the sportiest Genesis. Sport seats get harder use (aggressive driving). Compact interior materials may show wear faster. Engine reliability concern undermines long-term cosmetic confidence. Parts are shared (good) but the engine is the liability.',
    'G70 3.3T Q-score 63.3. Lowest Genesis score — problematic Lambda II 3.3T in the smallest, loudest body. The driving experience is engaging but build quality is the worst Genesis combination. NVH is the weakest dimension. If considering a G70, the 2.5T Smartstream is the better long-term bet despite being newer.',
    'shared', 'Ulsan (South Korea)', 'spot', 4.5,
    'rubber', 'laminated', 'standard', 'real_wood',
    4, 'standard', 'sample'
);

-- ============================================================
-- 9. G90 1st gen 3.3T (2017-2021) car_id=44, q_score=71.9
-- Lambda II 3.3T in flagship body — engine concern offsets platform benefit
-- NVH+interior adjusted: flagship sound deadening + materials justify higher scores
-- ============================================================
INSERT INTO build_quality (
    car_id, q_score,
    score_body_construction, score_nvh_isolation, score_interior_materials,
    score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
    body_construction_notes, nvh_isolation_notes, interior_materials_notes,
    paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes,
    q_score_notes,
    platform_type, assembly_plant, weld_technology, panel_gap_mm,
    engine_mount_type, glass_type, leather_grade, wood_type,
    paint_stages, sound_deadening_rating, source
) VALUES (
    44, 71.9,
    74, 78, 78,
    66, 66, 68,
    'Same flagship BH-L platform as G90 5.0. Additional structural reinforcement. Panel gaps 4-5mm. High-tensile steel cage. Body construction identical to G90 5.0 — engine choice doesn''t change the body.',
    'Flagship sound deadening helps the 3.3T significantly. Air suspension standard. Above-average insulation. Lambda II 3.3T is less refined than Tau 5.0 under load but flagship isolation masks much of it. Rubber engine mounts. Standard laminated glass. NVH is good for a turbo V6 flagship but not V8-flagship smooth.',
    'Identical interior to G90 5.0 at equivalent trim. Nappa leather, real wood, flagship-grade materials. Same Hyundai-grade hard plastics in secondary areas. Interior score same as 5.0 because the cabin is identical.',
    'Same Korean paint process as all Genesis flagships. No systemic issues. Good galvanized steel. Flagship QC. Paint score identical to G90 5.0.',
    'Hyundai electronics with flagship complexity. Air suspension, more driver assistance features than G80. Lambda II oil consumption is mechanical not electrical. 10yr/100K warranty critical. Same electrical architecture as G90 5.0 — no unique electronic concerns.',
    'Lambda II 3.3T oil consumption concern in a flagship is particularly unfortunate — this is a $70K+ car with documented engine lawsuits. Air suspension aging same as G90 5.0. Interior materials are flagship-grade and should age well. Parts for 3.3T are more available than Tau 5.0 (shared across Hyundai/Kia). Cosmetic score slightly higher than 5.0 due to better parts availability.',
    'G90 1st gen 3.3T Q-score 70.3. Same excellent flagship body and interior as the 5.0, but Lambda II 3.3T engine concerns hold it back. Flagship isolation helps NVH despite turbo engine. The oil consumption epidemic and NHTSA investigation are serious negatives in a flagship. Slightly below G90 5.0 in NVH but slightly above in parts availability.',
    'shared', 'Ulsan (South Korea)', 'spot', 4.5,
    'rubber', 'laminated', 'standard', 'real_wood',
    4, 'above_average', 'sample'
);

-- ============================================================
-- 10. GV70 3.5T (2022+) car_id=54, q_score=65.3
-- Lambda II in SUV, dual injection helps carbon but oil consumption heritage
-- ============================================================
INSERT INTO build_quality (
    car_id, q_score,
    score_body_construction, score_nvh_isolation, score_interior_materials,
    score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
    body_construction_notes, nvh_isolation_notes, interior_materials_notes,
    paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes,
    q_score_notes,
    platform_type, assembly_plant, weld_technology, panel_gap_mm,
    engine_mount_type, glass_type, leather_grade, wood_type,
    paint_stages, sound_deadening_rating, source
) VALUES (
    54, 65.2,
    70, 62, 66,
    65, 62, 62,
    'Hyundai N3 platform (compact SUV). Same platform as GV70 2.5T. SUV body with liftgate. Standard spot welding with structural adhesives. Panel gaps 4-5mm. Body construction identical to GV70 2.5T — engine choice doesn''t change the structure.',
    'SUV packaging provides more insulation volume than G70 sedan. 3.5T dual injection is quieter than old 3.3T but still turbo NVH under boost. Air suspension option improves ride quality. Rubber engine mounts. Standard laminated glass. Better NVH than G70 3.3T due to SUV packaging and newer engine tuning.',
    'Same interior as GV70 2.5T at equivalent trim. Good materials on touch surfaces. SUV provides more interior volume = more material coverage. Real wood on upper trims. Same Hyundai-grade secondary materials. Interior score identical to 2.5T variant.',
    'Same Korean paint as all Genesis SUVs. No unique issues. SUV horizontal surfaces more exposed but no paint epidemics in Genesis history. Same galvanized steel, same process.',
    'Same electrical architecture as GV70 2.5T plus air suspension electronics if equipped. Too new for definitive data. SUV electronics (liftgate, air suspension) add complexity. 10yr/100K warranty is safety net. Newer tech = more potential failure points.',
    'Lambda II heritage is the concern despite dual injection improvement. Oil consumption risk remains from engine family DNA. SUV cargo use may accelerate interior wear. Too new for definitive cosmetic aging. Score is conservative due to engine family history. Parts for 3.5T are shared across Hyundai/Kia (good availability).',
    'GV70 3.5T Q-score 65.2. Dual injection improves on the problematic 3.3T but Lambda II oil consumption heritage remains. SUV packaging helps NVH vs G70 3.3T. Same fundamental Genesis strengths (newer platform, improved materials) and weaknesses (shared platform, rubber mounts). Score slightly higher than G70 3.3T due to SUV NVH advantage and newer engineering.',
    'shared', 'Ulsan (South Korea)', 'spot', 4.5,
    'rubber', 'laminated', 'standard', 'real_wood',
    4, 'standard', 'sample'
);

-- ============================================================
-- 11. GV80 3.5T (2020+) car_id=154, q_score=65.7
-- Lambda II in heaviest Genesis — most stress on components
-- ============================================================
INSERT INTO build_quality (
    car_id, q_score,
    score_body_construction, score_nvh_isolation, score_interior_materials,
    score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
    body_construction_notes, nvh_isolation_notes, interior_materials_notes,
    paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes,
    q_score_notes,
    platform_type, assembly_plant, weld_technology, panel_gap_mm,
    engine_mount_type, glass_type, leather_grade, wood_type,
    paint_stages, sound_deadening_rating, source
) VALUES (
    154, 65.6,
    70, 63, 66,
    65, 62, 64,
    'Hyundai M3 platform (mid-size SUV). Largest Genesis vehicle. Heaviest body = most stress on structure and components. Standard spot welding with structural adhesives. Panel gaps 4-5mm. Good rigidity for SUV class but heaviest application of shared platform. Long-term structural durability under max load is unproven.',
    'Mid-size SUV provides good insulation volume. 3.5T under load moves significant mass — turbo lag and boost NVH are noticeable with full payload. Air suspension (available) helps ride quality. Rubber engine mounts. Standard laminated glass. Better NVH than compact SUVs due to mass and volume, but turbo working harder than in lighter applications.',
    'Best Genesis SUV interior. More surface area = more premium material coverage. Real wood, leather, soft-touch surfaces on all primary touch points. Still Hyundai-grade plastics in cargo area and secondary zones. Interior ambition is high for the price point. Second-row space allows more material investment.',
    'Same Korean paint process. Largest Genesis = largest paint surface area. No systemic issues. Horizontal surfaces (large hood, roof) are exposure points. Same galvanized steel. Paint quality consistent with other Genesis vehicles.',
    'Most electronics in Genesis SUV lineup. 3D digital dash, highway driving assist, air suspension, rear-axle steering. All complexity that can fail. Too new for definitive data. Lambda II oil consumption is mechanical. 10yr/100K warranty essential. Electrical score reflects density of tech features.',
    'Heaviest Genesis = most stress on all components. Lambda II 3.5T working hardest in this application. Oil consumption risk from engine family heritage. Air suspension (if equipped) under max load will age faster. Interior cargo-area materials may show wear with use. Too new for definitive data — score is conservative. Parts shared with Hyundai/Kia (good availability for 3.5T).',
    'GV80 3.5T Q-score 65.6. Largest, heaviest Genesis with the most stressed Lambda II application. Good SUV interior and improved 3.5T dual injection, but maximum vehicle mass amplifies engine and component aging concerns. Score slightly above GV70 3.5T due to better interior volume/materials, but structural stress concern offsets the gain.',
    'shared', 'Ulsan (South Korea)', 'spot', 4.5,
    'rubber', 'laminated', 'standard', 'real_wood',
    4, 'standard', 'sample'
);

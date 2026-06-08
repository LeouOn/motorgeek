-- Volvo S60 T5 (2019-?) Build Quality Q-factor (car_id=156)
-- SPA platform (shared with XC60/S90). Simple turbo, clean Swedish design.

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
    156, 74.6,
    76, 78, 74,
    75, 72, 73,
    'SPA platform shared with XC60/S90. Extensive use of hot-formed boron steel (40% of body). Good crash structure. MacPherson strut front, multi-link rear. Spot welding primary with structural adhesive bonding. Panel gaps 4-5mm, consistent.',
    'SPA platform engineered for low NVH from the ground up. Hydraulic engine mounts standard. Acoustic laminated windshield. Additional sound deadening in floor pan and firewall. Engine cover insulated. T5 single-turbo is inherently smoother than T6 twin-charge. Road noise well suppressed but not LS-tier.',
    'Minimalist Scandinavian interior. Good soft-touch surfaces on touch points. Leatherette standard on base, genuine leather on higher trims. Driftwood inlay is real wood on Inscription. Sensus portrait tablet dominates dash — clean but polarizing. Fit and finish above average, materials a step below German luxury.',
    'Volvo multi-stage paint process. Good galvanized steel. Some reports of thin paint on horizontal surfaces (hood, roof) chipping easily. Not a clear coat epidemic but more chips than expected at highway mileage. Corrosion resistance good underneath.',
    'Sensus infotainment is the weak point. Laggy, crash-prone on early 2019 models. OTA updates improved it but never great. Otherwise electrical systems are solid. No systemic gremlins beyond infotainment. Sensor reliability good.',
    'Interior holds up well. Leather/leatherette ages gracefully. Real wood trim doesn''t delaminate. Piano black trim scratches easily. Steering wheel wears at 80K+. Door panels stay tight. Good long-term cosmetic durability for the segment.',
    'S60 T5 Q-score 74.6. Honest SPA platform execution with single-turbo simplicity. Strong body structure, good NVH engineering, clean interior. Not luxury-grade materials (semi-aniline, Optitron) but above-average for the $40K segment. Sensus infotainment is the main electrical liability.',
    'shared', 'Torslanda (Gothenburg, Sweden)', 'mixed', 4.5,
    'hydraulic', 'acoustic_laminated', 'standard', 'real_wood',
    4, 'above_average', 'sample'
);

-- Volvo S60 T6 AWD (2019-2021) Build Quality Q-factor (car_id=157)
-- Same SPA platform but supercharged+ turbo. More complexity.

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
    157, 72.0,
    76, 74, 74,
    75, 68, 72,
    'Identical SPA body structure to T5. Same hot-formed boron steel cage, same panel gaps, same welding. AWD adds Haldex fifth-generation coupling at rear axle — well-integrated, doesn''t compromise body. No body construction difference vs T5.',
    'T6 supercharger+ turbo adds mechanical complexity and slight NVH penalty. Supercharger whine audible under hard acceleration. Hydraulic mounts same as T5. AWD system adds minor drivetrain noise. Acoustic laminated windshield same. Marginally louder than T5 at idle and cruise.',
    'Identical interior to T5 same trim level. Same materials, same fit. No interior difference between T5 and T6 of same trim. Inscription gets real wood, leather. Momentum gets leatherette, aluminum trim.',
    'Identical paint to T5. Same Volvo paint process, same thin-on-hood issue, same good underneath corrosion resistance.',
    'T6 engine is the electrical/complexity penalty. Supercharger + turbo + AWD = more sensors, more vacuum lines, more potential failure points. Supercharger bearings known to fail at 80-100K. Oil consumption higher than T5. Sensus infotraction same weakness. Polestar-optimized ECU tunes can stress components.',
    'Same cosmetic aging as T5. Interior materials identical. Engine bay runs hotter (supercharger + turbo) — rubber hoses and plastic engine covers degrade faster. Cosmetic under-hood aging faster.',
    'S60 T6 Q-score 72.0. Same excellent SPA body as T5 but twin-charge engine adds complexity without adding build quality. Supercharger is a known wear item. Scores lower than T5 on NVH (supercharger whine), electrical (more sensors/failures), and cosmetic (hotter engine bay).',
    'shared', 'Torslanda (Gothenburg, Sweden)', 'mixed', 4.5,
    'hydraulic', 'acoustic_laminated', 'standard', 'real_wood',
    4, 'above_average', 'sample'
);

-- Volvo S90 T6 AWD (2017-2021) Build Quality Q-factor (car_id=160)
-- SPA platform flagship sedan. Good materials, minimalist Scandinavian design.

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
    160, 73.5,
    76, 80, 77,
    75, 68, 73,
    'SPA platform stretched for S90 flagship. Same boron steel cage architecture as S60/XC60 but longer wheelbase adds torsional rigidity challenge. Air suspension available on Inscription. Panel gaps 4-5mm. Good structure but not bespoke — shared with 60-series.',
    'Best NVH in the SPA family. Longer wheelbase = more isolation. Additional sound deadening vs S60. Air suspension (optional) improves ride quality significantly. Acoustic laminated windshield standard. Side windows acoustic laminated on Inscription. Engine noise better isolated in longer engine bay. T6 supercharger still audible under load.',
    'Flagship-level materials. Nappa leather on Inscription (upgrade from S60 standard leather). Real wood options: flame birch, linear walnut. Orrefors crystal gear selector. Broader, richer interior than S60. Fit and finish very good. Sensus portrait tablet still dominates. Not German-luxury tier but the best Volvo can do.',
    'Same Volvo paint process as S60/XC60. Same thin paint on horizontal surfaces. Same good galvanized steel underneath. Flagship gets no paint upgrade over 60-series — shared platform limitation.',
    'T6 twin-charge same complexity as S60 T6. Supercharger bearing failures, oil consumption. Sensus infotainment same weakness — actually worse on early 2017-2018 S90 (first SPA model year). Air suspension (if equipped) adds pneumatic sensor and compressor failure risk. More electrical complexity than S60.',
    'Interior materials age well. Nappa leather superior to standard. Real wood ages gracefully. Crystal gear selector durable. Longer cabin means more interior panels — slightly more rattle potential. Air suspension can sag. Overall good cosmetic longevity.',
    'S90 T6 Q-score 73.5. Best SPA interior materials and NVH but T6 engine complexity and Sensus infotainment limit the score. Flagship positioning but shared platform means no bespoke body engineering upgrade. The car Volvo wants to sell you, not the car they engineered from scratch.',
    'shared', 'Daqing (China) / Torslanda (Sweden)', 'mixed', 4.5,
    'hydraulic', 'acoustic_laminated', 'semi_aniline', 'real_wood',
    4, 'extensive', 'sample'
);

-- Volvo V60 Polestar (2014-2018) Build Quality Q-factor (car_id=98)
-- Old P3 platform (not SPA). Twin-charged. Enthusiast car but aging platform.

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
    98, 58.0,
    65, 50, 60,
    55, 52, 55,
    'P3 platform predates SPA. Conventional steel body, less boron steel. MacPherson front, multi-link rear. Standard spot welding. Panel gaps 5-7mm. Stiffer Polestar suspension (Ohlins dampers, stiffer springs, strut brace) improves structural feel but doesn''t change body construction. Aging architecture vs SPA.',
    'Polestar tuning prioritizes handling over comfort. Stiff suspension transmits road noise directly. Ohlins monotube dampers are firm. Engine mounts stiffer than standard. T6 twin-charge engine is mechanically noisy under boost. Some sound deadening removed for weight. Acoustic windshield not standard. The enthusiast trade-off: it handles but it''s not quiet.',
    'Polestar-specific sport seats by Polestar/Sparco (later Polestar-branded). Good bolsters, durable fabric/leather combination. Piano black trim, blue contrast stitching. Materials are adequate but not luxury — this is an enthusiast special, not a luxury car. Real aluminum trim on Polestar models. Interior simpler than SPA Volvos.',
    'P3-era Volvo paint is average. Some reports of clear coat issues on dark colors at 8-10 years. Not epidemic like Infiniti G35 but not as good as SPA-era paint. Nordic climate cars (many Polestars are Swedish-market) often have underbody corrosion from road salt.',
    'T6 twin-charged engine is the liability. Supercharger + turbo on a 2.0L 4-cylinder running high boost. Known for oil consumption, supercharger bearing failure, PCV issues. Polestar ECU tune increases stress. Ohlins dampers need rebuild at 50-70K. Sensus infotainment of this era (pre-SPA) is worse than later versions. More electrical gremlins than SPA cars.',
    'Sport seats hold up well. Leather/fabric combination is durable. Piano black shows scratches and fingerprints. Exterior Polestar-specific body kit (front splitter, rear diffuser, spoiler) is unpainted plastic — scuffs easily. Ohlins dampers can weep fluid at 60K+. Paint on wheels chips from stiff suspension. Ages like a sports car, not a luxury car.',
    'V60 Polestar Q-score 58.0. Enthusiast car on aging P3 platform. The driving experience is the point (350hp, AWD, Ohlins, manual available in some markets), but build quality is mid-tier. Twin-charge engine complexity, stiff NVH, aging electrics. Buy it for the drive, not the quality.',
    'shared', 'Torslanda (Gothenburg, Sweden)', 'spot', 5.5,
    'rubber', 'standard', 'standard', 'none',
    4, 'standard', 'sample'
);

-- Volvo XC60 T5 (2018-?) Build Quality Q-factor (car_id=158)
-- SPA platform SUV. Very popular, good build quality.

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
    158, 74.0,
    76, 77, 74,
    74, 72, 72,
    'SPA platform SUV. Same boron steel cage as S60/S90. SUV body has higher center of gravity but good structural rigidity for the class. Hot-formed steel in B-pillars, roof rails, door reinforcements. Panel gaps 4-5mm, consistent with SPA sedan siblings. Well-engineered safety cage.',
    'SUV form factor inherently noisier than sedan — more tire roar from larger contact patch, more wind noise from taller profile. Volvo compensates with extensive sound deadening in floor, firewall, doors. Hydraulic engine mounts standard. Acoustic laminated windshield. T5 single-turbo is smooth. Not sedan-quiet but very good for SUV.',
    'Same interior architecture as S60. Same materials at same trim levels. Inscription gets Nappa leather and real wood. Momentum gets leatherette. Portrait Sensus tablet identical. Good materials for the class, not luxury-tier. XC60 benefits from higher price point — more Inscription trims sold, so average interior quality higher.',
    'Same Volvo paint process. SUV adds more chip risk — higher ride height means more stone exposure from other vehicles. Front bumper and hood take more hits. Lower body cladding helps protect doors. Good underneath, same thin-on-hood issue.',
    'SPA electrical architecture. Sensus infotraction same weakness — laggy, occasionally crashes. T5 engine is electrically simple (single turbo, fewer sensors than T6). No systemic electrical issues beyond infotainment. Sensor reliability good.',
    'Interior ages well on Inscription trim. Nappa leather durable. Real wood ages gracefully. Piano black trim scratches (XC60 has more of it than S60). Door panels stay tight. Cargo area materials are utilitarian — scratch-prone. Steering wheel wears at 80K+. Good overall.',
    'XC60 T5 Q-score 74.0. SPA platform SUV done right. Same body engineering strengths as S60 with SUV trade-offs (more tire noise, more chip risk). T5 simplicity is an advantage. Sensus infotainment is the universal Volvo weakness. Best-selling Volvo for good reason — honest quality.',
    'shared', 'Torslanda (Gothenburg, Sweden) / Luqiao (China)', 'mixed', 4.5,
    'hydraulic', 'acoustic_laminated', 'standard', 'real_wood',
    4, 'above_average', 'sample'
);

-- Volvo XC60 T6 AWD (2018-2020) Build Quality Q-factor (car_id=159)
-- Same SUV, more complex engine.

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
    159, 71.5,
    76, 73, 74,
    74, 66, 71,
    'Identical SPA body structure to XC60 T5. Same boron steel, same panel gaps, same safety cage. AWD adds Haldex coupling. Air suspension optional. No body construction difference vs T5.',
    'T6 supercharger whine plus SUV tire roar = louder than T5. Supercharger adds high-frequency mechanical noise under acceleration. Hydraulic mounts same. Sound deadening same. Net result: more noise sources than T5. AWD system adds minor drivetrain whine at highway speed.',
    'Identical interior to XC60 T5 at same trim level. No difference in materials, fit, or finish between T5 and T6.',
    'Identical paint to XC60 T5. Same process, same chip vulnerability, same good corrosion resistance.',
    'T6 twin-charge same issues as S60 T6 and S90 T6. Supercharger bearing failures at 80-100K. Higher oil consumption. More sensors, more vacuum lines. AWD Haldex coupling needs fluid changes or seizes. Air suspension (if equipped) adds compressor and air bladder failure risk. More electrical failure modes than T5.',
    'Same interior aging as T5. Engine bay runs hotter — under-hood rubber and plastic components degrade faster. Same exterior cosmetic aging. Same chip risk.',
    'XC60 T6 Q-score 71.5. Same excellent SPA body as T5 but T6 complexity penalties across NVH, electrical, and cosmetic dimensions. The supercharger adds power (316 vs 250 hp) but subtracts reliability and refinement. AWD is nice in snow but Haldex is a wear item.',
    'shared', 'Torslanda (Gothenburg, Sweden) / Luqiao (China)', 'mixed', 4.5,
    'hydraulic', 'acoustic_laminated', 'standard', 'real_wood',
    4, 'above_average', 'sample'
);

-- Kia K5 GT (2021-2024) Build Quality Q-factor (car_id=162)
-- Hyundai shared platform. Smartstream 2.5T. Value-oriented, good but not luxury.

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
    162, 55.0,
    62, 52, 55,
    52, 55, 50,
    'Hyundai-Kia N3 platform (shared with Sonata, Santa Fe). Unibody steel construction. Hot-stamped steel in A/B pillars and roof rails for safety. MacPherson strut front, multi-link rear. Standard spot welding. Panel gaps 5-7mm, acceptable but not tight. Good crash test ratings (IIHS Top Safety Pick). Economy-car architecture competent but not overbuilt.',
    'Economy-car NVH strategy: insulation quantity over sophistication. Rubber engine mounts. No acoustic laminated glass. Sound deadening in floor and firewall but basic materials. 2.5T engine is smooth at idle but boomy under boost. Exhaust is tuned for sport (loud). Tire roar with 19-inch wheels on GT. Wind noise at 75+ mph. Adequate for the price, not competitive with luxury.',
    'GT trim gets synthetic leather (not real) with suede inserts. Heavily textured plastic trim. Piano black center console (fingerprint magnet, scratches easily). Fake aluminum trim. The panoramic curved display (dual screens under one glass) looks modern but the surrounding materials are hard plastic. Good design, mediocre materials. Above average for Kia, below luxury.',
    'Kia/Hyundai paint of this era is thin. Multiple owner reports of easy chipping on hood and front bumper. Some early reports of clear coat hazing on dark colors. Not a known epidemic yet (too new) but history suggests average-to-below. Good galvanization underneath. 10-year corrosion warranty suggests confidence.',
    'Too new for definitive aging data. Early signs: UVO/Connect infotainment is responsive but Korean-market software with US localization quirks. Digital key system works but fiddly. 2.5T engine has some early turbo wastegate rattle reports (carryover from Sonata N-Line). No systemic electrical issues yet but Hyundai-Kia electrical history is mixed.',
    'Too new for long-term data. Predictions based on Kia materials: synthetic leather will crack at 60-80K miles. Piano black trim will be scratched within 20K. Suede inserts wear fast on bolsters. Steering wheel leather thin. Interior will look good for 5 years, tired at 10. Economy-grade materials throughout.',
    'K5 GT Q-score 55.0. Honest economy-sport sedan with great design and good value. Not built like a luxury car because it isn''t one. N3 platform is competent, 2.5T is powerful, but materials are economy-grade, NVH is basic, and long-term aging will be average at best. The $32K MSRP is reflected in every dimension.',
    'shared', 'West Point (Georgia, USA)', 'spot', 5.5,
    'rubber', 'standard', 'synthetic', 'none',
    3, 'standard', 'sample'
);

-- Infiniti Q50 1st gen (2014-2024) Build Quality Q-factor (car_id=34)
-- Nissan D-platform. Direct adaptive steering. Poor interior materials. Infiniti''s worst era.

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
    34, 38.5,
    58, 40, 32,
    35, 28, 35,
    'Nissan D-platform (Front-Mid, shared with 370Z successor, never fully updated). FM layout is theoretically good for weight distribution but execution is dated. Standard spot welding, pressed steel throughout, no structural adhesives. Panel gaps 5-7mm, inconsistent. No advanced high-strength steel usage worth noting. Underneath, it''s a 2008 platform with a 2014 body. Worse than G35 FM platform in terms of advancement.',
    'Poor. Direct Adaptive Steering (DAS) on equipped models creates a disconnected steering feel that also transmits weird feedback. No acoustic glass. Rubber engine mounts. Minimal sound deadening — Infiniti prioritized the "sporty" exhaust note. V6 VR30DDTT (twin-turbo) is mechanically noisy. Road noise with sport tires is high. Wind noise at highway speed above average. The 2014 Q50 was criticized by every reviewer for NVH regression vs the G37 it replaced.',
    'The weakest dimension. Interior materials are a known disgrace for the brand. Hard plastics everywhere. "Leather" is thinly coated synthetic that peels at 40-50K miles. "Kacchu" aluminum trim is textured plastic. Wood trim is glossy wood-grain vinyl. The dual-screen infotraction (upper + lower) was dated at launch in 2014 and never updated meaningfully through 2024. Panel fit inside is loose. Every surface feels cheaper than a Maxima. Infiniti''s cost-cutting is palpable.',
    'Nissan paint of this era is poor. Multiple owner reports of clear coat failure on hood, roof, trunk at 5-7 years. White and black especially vulnerable. The Q50 paint is thin and soft — chips easily, scratches in car washes. No evidence of improved paint process over G35 era. Corrosion resistance below average — some early rust on rear quarter panels at 80K+.',
    'DAS (Direct Adaptive Steering) is the Q50''s signature failure. Steer-by-wire with a mechanical backup clutch that engages when the electronic system fails (which it does). Three generations of DAS, all problematic. Intouch dual-screen infotainment is universally criticized — laggy, crashes, requires reboots. The 2014-2017 models are especially bad. Climate control integration means when the screen dies, you lose AC control. Electrical architecture is a mess. VR30DDTT turbo engines have sensor reliability issues.',
    'Interior materials degrade rapidly. Synthetic leather cracks and peels at 40-50K miles (documented extensively on forums). Steering wheel wrap wears through at 50-60K. Piano black trim scratched within months. Headliner sags near sunroof at 80K+. Exterior clear coat fails at 5-7 years. The Q50 ages worse than the G35 it replaced — cheaper materials, more electronics, same poor paint. A 10-year-old Q50 looks like a 15-year-old car.',
    'Q50 Q-score 38.5. Infiniti''s worst era in one car. D-platform FM architecture never properly updated. DAS steer-by-wire is a liability. Interior materials are disgraceful for a $40-50K car. Dual-screen infotainment was bad at launch and aged terribly. Paint quality poor. The VR30DDTT engine is powerful but surrounded by cheap. G35 was a driver''s car with bad materials; Q50 is a bad car with bad materials.',
    'shared', 'Tochigi (Japan)', 'spot', 6.5,
    'rubber', 'standard', 'synthetic', 'plastic',
    3, 'minimal', 'sample'
);

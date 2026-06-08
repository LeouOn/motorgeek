-- Build Quality Q-factor scores for Lexus, Toyota, Honda, Kia batch
-- Calibrated against LS430 (94.7), ES350 (76.3), G35 (48.5) anchors

-- Lexus LS 400 (1989-1994) — id=63, reliability=92.0
-- FIRST LS. Clean-sheet F1 platform, world-first laser welding, same philosophy as LS430 but simpler era
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
    63, 87.8,
    94, 89, 87,
    84, 90, 83,
    'Clean-sheet F1 platform designed to beat Mercedes S-Class. World-first laser welding on body seams (patented Toyota process). 0.005mm body panel tolerance (20x tighter than contemporaries). High-tensile steel door beams. Double-wishbone suspension all four corners. Aerodynamic flat underbody panel.',
    'Hydraulic fluid-filled engine mounts. 2-ton sand-filled frame rails for vibration damping during development. Extensive asphalt sheet deadening in floor pan and doors. Pre-acoustic glass era but thick laminated windshield. Famous coin-balancing idle test from development — 1UZ-FE smooth enough to balance a coin at idle.',
    'Semi-aniline leather standard — same grade that would carry through to LS430. Real California walnut trim (genuine, not veneer). Electroluminescent gauges (predecessor to Optitron). Interior panel tolerance 5mm. First car with in-dash CD player. Climate control with plasmacluster ion purifier.',
    'Tahara multi-coat paint process with electrostatic primer. Galvanized steel body panels. Excellent corrosion resistance for era — no rust epidemics after 30+ years. Some clear coat thinning on horizontal surfaces at 25+ years but better than any German or American contemporary.',
    'Remarkably simple electronics for a flagship — this is the LS400''s secret weapon. Analog gauges, basic ECU, no touchscreen. Very few electronic failure points. A/C system reliable. Power seats and windows durable. Nearly bulletproof at 30+ years and 300K+ miles.',
    'Premium materials age exceptionally well. Semi-aniline leather develops patina rather than cracking at 200K+. Real walnut resists delamination. Tight 4mm panel gaps prevent squeaks and rattles. Dashboard resists UV cracking better than Nissan or BMW of era. Some steering wheel wear at 200K+.',
    'LS400 Q-score 87.8. The car that invented Japanese luxury build quality. First LS set every benchmark that LS430 later perfected. Deductions from LS430 for older NVH technology (no acoustic glass, no sandwich steel), wider panel gaps (4.0 vs 3.5mm), and simpler paint process. Electronics score (90) highest in database due to 1989 simplicity.',
    'bespoke', 'Tahara Plant (Aichi, Japan)', 'laser', 4.0,
    'hydraulic', 'laminated', 'semi_aniline', 'real_wood',
    5, 'extensive', 'expert_analysis'
);

-- Lexus GS 4th gen (2013-2020) — id=35, reliability=85.0
-- Shared Toyota N platform (NOT bespoke like LS). Double wishbone front. Good materials but not LS-tier.
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
    35, 76.3,
    70, 78, 74,
    80, 80, 76,
    'Shared Toyota N platform (same as Crown and Mark X, NOT bespoke LS). Double wishbone front suspension is unusual for a shared platform and adds credibility. Multi-link rear. High-strength steel in key structural areas. Good rigidity but lacks the bespoke engineering investment of an LS.',
    'Lexus-grade NVH tuning applied to shared platform. Hydraulic engine mounts standard — unusual at this price point. Acoustic laminated front windshield. Active Noise Control available on F Sport models. Sound-deadening glass on upper trims. Notably quieter than German competitors (5 Series, E-Class) at cruise.',
    'Quality Lexus materials but not LS-tier. Standard leather (not semi-aniline). Real aluminum trim and genuine wood options. Analog clock on dash. Good soft-touch surfaces on upper panels. Lexus Enform infotainment dated but functional. S2000-style driver-focused cockpit. Better materials than ES350.',
    'Standard Toyota/Lexus paint process. Good quality with no known epidemics. Self-healing clear coat on darker colors. Corrosion-resistant galvanized steel throughout. Holds up well at 10+ years. Paint quality consistent across Motomachi production.',
    'Generally reliable Lexus electronics. Some reports of navigation screen delamination at 8+ years. Adaptive variable suspension sensors can fail. Mark Levinson amp holds up well. No systemic electrical gremlins. Significantly better electrical track record than LS460 despite sharing some components.',
    'Lexus interior quality means graceful aging. Leather holds up at 100K+ miles. Real wood trim doesn''t fade. Some center console armrest wear at high mileage. F Sport seats show minor bolster wear. Steering wheel holds up. Overall better aging than any German competitor in this class.',
    'GS 4th gen Q-score 76.3. The best non-LS Lexus for build quality — double wishbone front suspension adds engineering credibility. Shared platform prevents bespoke-level scores but Lexus-level NVH tuning and material selection elevate it above ES350. Discounted for not being bespoke and slightly below LS-tier interior materials.',
    'shared', 'Motomachi Plant (Aichi, Japan)', 'mixed', 4.5,
    'hydraulic', 'acoustic_laminated', 'standard', 'real_wood',
    4, 'above_average', 'expert_analysis'
);

-- Lexus LS 4th gen LS460 (2007-2017) — id=40, reliability=69.7
-- Bespoke platform, great build quality but complex (8-speed auto, air suspension, motorized everything)
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
    40, 82.7,
    94, 92, 90,
    90, 55, 75,
    'Bespoke LS platform with laser welding carried forward from LS430. Multi-link front and rear with standard air suspension. 0.002mm body panel tolerance (improved from LS400''s 0.005mm). Aluminum hood, doors, and fenders for weight reduction. First LS with LED headlights. Same Tahara Takumi craftsmanship.',
    'Exceptional NVH isolation matching LS430 benchmark. Hydraulic engine mounts. Acoustic laminated glass all around including rear quarter windows. Active Noise Control. Sound-insulating resin injected into body pillars. Helmholtz resonators in wheel wells. 56dB at 100km/h cruising — whisper-quiet.',
    'Semi-aniline leather available. Shimamoku wood option is hand-sanded through a 67-day, 38-step process — the most expensive wood trim in automotive production. Optitron gauges. Mark Levinson Reference audio. Executive-class rear seat with ottoman option. Interior tolerance maintained at 1mm like LS430.',
    'Tahara multi-coat process identical to LS430. Robot-applied electrostatic primer. Self-healing clear coat on darker colors. Excellent long-term corrosion resistance with galvanized steel throughout. No clear coat epidemics documented. Paint quality fully matches LS430 after 15+ years of data.',
    '8-speed AA80E automatic valve body failures are common — harsh 2-3 and 5-6 shifts at 60-100K miles. Air suspension compressor and air bags fail at 80-120K ($3-5K repair). Brake actuator/accumulator failures documented across forums. Motorized tilt-telescope column can stick. Mark Levinson amp can fail from cold solder joints. The most complex LS before 600h.',
    'Premium physical materials age well — semi-aniline leather patinas nicely, Shimamoku wood is durable. Air suspension sag if not maintained affects vehicle stance. Motorized features can stick or fail. Better than any German competitor for cosmetic aging but below LS430 and LS400 due to complexity-induced neglect.',
    'LS460 Q-score 82.7. Incredible physical build quality matching LS430 in every dimension except electrical aging. The 8-speed auto, air suspension, and motorized feature complexity result in a -37 point electrical deduction versus LS430 (82). Body, NVH, and materials are all 90+ — it is built as well as any car. Complexity is the enemy, not construction quality.',
    'bespoke', 'Tahara Plant (Aichi, Japan)', 'laser', 3.5,
    'hydraulic', 'acoustic_laminated', 'semi_aniline', 'real_wood',
    5, 'extensive', 'expert_analysis'
);

-- Lexus LS 600h (2007-2018) — id=24, reliability=56.3
-- Same LS460 platform + hybrid complexity. Heaviest LS. Battery + CVT + air suspension = lots to go wrong.
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
    24, 78.0,
    94, 94, 92,
    90, 30, 68,
    'Same bespoke LS460 platform with additional structural reinforcement for 150kg+ hybrid battery pack. Laser welding throughout. Same 0.002mm panel tolerance. Heaviest LS ever at 2,410kg. AWD system adds front differential and driveshaft. Battery mounted behind rear seat for weight distribution.',
    'Best NVH isolation of any LS ever made. Hybrid system eliminates engine vibration at low speed entirely — EV-only mode up to 40mph is tomb-silent. Active engine mounts supplement hydraulic mounts. Acoustic laminated glass all around including rear quarter. At idle it is the quietest production car tested by Car and Driver in 2008.',
    'Top-shelf everything exceeding LS460. Semi-aniline leather standard. Shimamoku wood (67-day process) standard on Executive class. Alcantara headliner. Rear executive seats with massage and ottoman. Rear climate control with separate zones. Premium material selection exceeds every non-L sedan.',
    'Same Tahara multi-coat process as LS460. Excellent quality with no known paint issues. Self-healing clear coat. Corrosion-resistant galvanized steel. Identical paint aging characteristics to LS460.',
    'Catastrophic electrical complexity. Hybrid battery degradation at 10-15 years ($6-10K replacement). Inverter/converter failures documented across owner forums — some TSBs issued. CVT uses two-motor planetary gearset, not serviceable if internal failure occurs. Air suspension failures inherited from LS460. Brake booster/actuator failures. Parking assist camera module failures. Motorized everything means everything can break. Reliability score of 56.3 is the lowest of any LS.',
    'Same premium physical materials as LS460 but 2,410kg curb weight stresses components more. Air suspension more heavily loaded — failures affect ride height visibly. Heavier doors stress hinges over time. Battery heat can affect trunk area materials. Otherwise same excellent Lexus cosmetic material quality.',
    'LS600h Q-score 78.0. The best NVH (94) and materials (92) of any LS, but catastrophic electrical aging (30) — the lowest electrical score of any Lexus ever made. Hybrid battery, inverter, CVT, air suspension, and motorized features create a $15K+ deferred maintenance time bomb. Physical build quality is LS-tier but electronics drag the overall score down 16.7 points from LS430.',
    'bespoke', 'Tahara Plant (Aichi, Japan)', 'laser', 3.5,
    'active', 'acoustic_laminated', 'semi_aniline', 'real_wood',
    5, 'extensive', 'expert_analysis'
);

-- Toyota Camry XV70 V6 (2018-2024) — id=87, reliability=83.9
-- Standard Camry. Good but shared platform, rubber everything, standard materials.
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
    87, 69.2,
    64, 65, 52,
    78, 88, 68,
    'Toyota TNGA-K platform shared with ES350, Avalon, Highlander, Sienna. MacPherson strut front (not double wishbone). Multi-link rear. High-strength steel increased significantly over previous generation. Spot welding throughout with laser screw welding on select joints. Panel gaps improved to ~4.8mm — better than XV50 but not Lexus-grade.',
    'Significant NVH improvement over previous Camry generations thanks to TNGA. Foam-injected A-pillars and B-pillars. Dash insulator pad. Standard rubber engine mounts (not hydraulic — cost saving). No acoustic laminated glass on any trim. 2GR-FKS V6 is inherently smooth. Quiet for a family sedan but not Lexus-quiet.',
    'SofTex synthetic leather on XSE and XLE trims — convincing but not real. Soft-touch upper dash and door panels. Hard plastics on lower panels and console. No real wood anywhere — piano black or textured aluminum-look trim. Standard gauges with small TFT screen. Entune 3.0 infotainment functional but dated. Acceptable for segment, not luxury.',
    'Standard Toyota paint process. Good quality with no known epidemics. Electrostatic primer application. Galvanized steel panels. Some paint chipping on front bumper from low front overhang. Holds up well at 5+ years with no premature clear coat failure. Expected to age similar to typical Toyota — good but not exceptional.',
    'Extremely reliable Toyota electronics — the Camry''s greatest strength. Simple infotainment by modern standards. No air suspension. No complex motorized features beyond basic power seats. 2GR-FKS V6 is a proven powertrain with no systemic issues. Everything expected to work at 200K+ miles. The electrical reliability champion of this entire batch.',
    'Adequate aging for mass market. SofTex synthetic leather more durable than real leather — resists cracking. Piano black trim scratches easily and shows dust. Cloth seats (base SE) age better than SofTex. Dashboard plastics resist UV cracking. Toyota switchgear proven durable over decades. Better than average for the segment.',
    'Camry XV70 Q-score 69.2. Honest mass-market build quality — the TNGA platform is a genuine improvement over previous Camry generations. Electrical aging (88) is best-in-class and the highest in this entire batch. Held back by shared platform construction, standard (non-hydraulic) mounts, synthetic materials, and no luxury engineering investment. Scores appropriately below ES350 (76.3) — it is an ES350 minus the Lexus premium.',
    'shared', 'Georgetown, Kentucky / Tsutsumi, Japan', 'spot', 4.8,
    'rubber', 'laminated', 'synthetic', 'none',
    3, 'standard', 'expert_analysis'
);

-- Toyota Supra A80 RZ (1993-1998) — id=4, reliability=88.0
-- Legendary 2JZ. Sports car with decent build quality for the era. Not luxury but well-engineered.
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
    4, 60.8,
    78, 32, 48,
    70, 85, 52,
    'Purpose-built A80 platform — not shared with any Celica or Soarer. Steel unibody with bolt-on front and rear subframes. Double-wishbone front, multi-link rear. 30% stiffer than A70 predecessor. Spot welding throughout with structural adhesive in key areas. Floorpan heavily reinforced for 2JZ-GTE torque. Targa top option reduces structural rigidity by ~15%.',
    'Sports car with minimal NVH isolation — by design. No hydraulic mounts — standard rubber. No acoustic glass. No sound deadening beyond minimum asphalt sheeting. Sequential twin-turbo spool and 2JZ exhaust note are the intended audio. Tire roar significant at speed with wide staggered rubber. Not designed for quiet cruising — at 80mph you hear 80mph.',
    'Functional sports car interior, not luxury. Standard leather on RZ trim but not premium grade — more durable than soft. Plastic trim dominates dash and center console. No wood anywhere. Basic analog gauges with prominent tachometer and turbo boost gauge. Recaro-style seats supportive but not plush. Premium for 1993 Toyota sports car but a step below luxury.',
    'Good Toyota paint quality for era. Some clear coat issues on black and white cars at 20+ years — typically hood and roof. Front bumper paint chips from low stance and air dam. Rear hatch area can develop rust if weather seals fail. No epidemic rust issues like G35. Better than average for 1990s Japanese sports car.',
    'Simple 1990s electronics — the 2JZ reliability halo extends here. ECU is virtually indestructible. Analog gauges with minimal electronics. No touchscreen, no navigation (JDM only). VVTi solenoid on 1997+ models occasionally fails. Traction control basic and reliable. Window regulators can fail. Overall excellent electrical aging for a 30-year-old car.',
    'Sports car life means everything shows wear faster. Driver seat bolster foam collapses at 80-100K miles. Steering wheel leather wears at crown. Dashboard UV damage if not garaged. Plastic trim fades and becomes brittle. Targa top weather seals degrade and leak. Many examples modified or tracked which accelerates wear.',
    'Supra A80 Q-score 60.8. Legendary engineering — purpose-built platform, 2JZ-GTE, double-wishbone all corners — but not a luxury car and scores reflect that. Body construction (78) is impressive for a 1993 sports car. NVH (32) is minimal by design — driver connection is the point. Interior (48) is functional. Electrical aging (85) is excellent due to 1990s simplicity. Sports car tax on NVH and cosmetic scores keeps overall Q below luxury sedans.',
    'bespoke', 'Motomachi Plant (Aichi, Japan)', 'spot', 5.0,
    'rubber', 'standard', 'standard', 'none',
    4, 'minimal', 'expert_analysis'
);

-- Honda S2000 AP1 (2000-2009) — id=6, reliability=78.0
-- Purpose-built sports car. High-revving engine, simple interior, good build quality for a roadster.
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
    6, 55.3,
    72, 25, 38,
    70, 82, 45,
    'Purpose-built S2000 platform — not shared with any Civic or Integra. Honda X-bone frame design provides exceptional rigidity for an open-top roadster — one of the stiffest convertibles of its era. High-strength steel central tunnel and side sills. Double-wishbone suspension all four corners. Spot welding with structural adhesive. Engine bay tower brace standard.',
    'Convertible roadster with functionally zero NVH isolation — the metric barely applies. Soft top provides minimal sound insulation versus hardtop. No acoustic treatments, no sound deadening material — Honda saved every gram. F20C at 9000rpm is the audio experience. Wind noise significant above 60mph with top up. With top down, NVH is moot. Engine vibration felt through chassis — intentional for driver connection.',
    'Minimalist sports car interior prioritizing weight savings over comfort. Standard cloth seats (leather optional in some markets). Hard plastic dash and door panels everywhere. Metal-look trim surrounds — not real metal. No wood, no luxury materials. Digital instrument cluster (novel for era). Small steering wheel. Honda AP1 interior philosophy: driving first, comfort distant second.',
    'Good Honda paint quality. No epidemic paint issues. Some clear coat thinning on Berlina Black and New Imola Orange at 15+ years — these colors are more susceptible. Front bumper paint chips from low nose. Rear fender arches can bubble if driven in winter salt. Better paint aging than Mazda MX-5 contemporaries.',
    'Simple Honda electronics — nearly no failure points. No touchscreen. Basic manual HVAC controls. Digital dash cluster is reliable. AP1 does not even have stability control until 2006. VTEC solenoid is bulletproof. No parasitic drain issues. Window regulators the only common electrical failure. Overall very good electrical aging.',
    'Roadster life means everything ages faster. Soft top requires replacement at 8-12 years ($1-2K in aftermarket). Seat foam collapses at 60-80K. Plastic trim fades and cracks in sun exposure. Dashboard can crack in hot climates (Arizona, Texas). Steering wheel leather wears. Convertible weather seals degrade and leak. Hard to keep pristine — most S2000s show their mileage.',
    'S2000 Q-score 55.3. Lowest in this batch but appropriately so — it is a purpose-built roadster evaluated on luxury build quality metrics. Body construction (72) is excellent for a roadster thanks to the X-bone frame. NVH (25) is the lowest score in the entire database — a convertible at 9000rpm is not built for silence. Interior materials (38) are minimal by design. Electrical aging (82) scores well due to Honda simplicity. The score reflects engineering purpose, not quality deficiency.',
    'bespoke', 'Suzuka Plant (Mie, Japan)', 'spot', 5.5,
    'rubber', 'standard', 'none', 'none',
    3, 'minimal', 'expert_analysis'
);

-- Kia Stinger 1st gen (2018-2023) — id=33, reliability=80.0
-- Hyundai shared platform. Good for the price but not luxury-tier. DCT issues.
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
    33, 60.8,
    65, 62, 55,
    65, 60, 58,
    'Hyundai-Kia shared rear-drive platform (shared with Genesis G70 and Hyundai Genesis Coupe predecessor). MacPherson strut front, multi-link rear. High-strength steel in B-pillars and roof rails. Spot welding throughout. Panel gaps inconsistent across production units — some tight, some 5mm+ on the same car. Korean build quality improving rapidly but not yet consistent.',
    'Above-average effort for Kia — clear intent to compete with German sport sedans. Some acoustic treatments in firewall and floor pan. Laminated front glass on GT2 trim. Sound deadening material in door panels. 3.3L twin-turbo Lambda II is refined when cruising but announces itself under boost. Road noise from 19-inch staggered wheels. Better than any previous Korean car.',
    'Good materials for the price point — punches above its class. Nappa leather available on GT2 trim (standard leather on lower trims). Real contrast stitching on dash surface. Aluminum-look trim — not real metal, deceives from photos. Plastic door pull surrounds feel cheap. Harman/Kardon audio. D-shaped steering wheel with paddle shifters. Competitive with BMW 330i interior at 70% of the price.',
    'Kia paint quality has improved dramatically over previous generations. Good clear coat depth. No known epidemics yet — car is relatively new at 5-7 years. Some reports of paint chipping on front bumper from road debris. Long-term corrosion resistance unknown but no early warning signs. Korean steel quality has closed gap with Japanese.',
    '8-speed DCT has documented issues — shudder at low speed, hesitation on takeoff, rough 1-2 shift. Some reports of infotainment system freezes requiring hard reset. Blind spot monitor sensor failures noted on forums. Rearview camera can fail. Not terrible but measurably below Toyota/Honda electrical reliability standards. Long-term aging data still accumulating at 5-7 years.',
    'Good initial quality but long-term data limited to ~7 years maximum. Nappa leather appears to hold up well. Piano black trim scratches easily and shows every fingerprint. Steering wheel wear visible at 60K+ miles. Interior plastics show scuffing at entry points. Center console armrest material thins. Better than early Korean cars but not yet Japanese-tier aging.',
    'Stinger Q-score 60.8. The best Korean attempt at a sports sedan — Albert Biermann (ex-BMW M division) oversaw chassis development and it shows. Body construction (65) is solid for shared platform. NVH effort (62) exceeds expectations for Kia. Interior materials (55) punch above price point. Electrical aging (60) held back by DCT issues. Long-term cosmetic aging uncertain — only 5-7 years of data. Scores appropriately alongside Supra A80 as purpose-engineered but non-luxury.',
    'shared', 'Sohari Plant (Gwangmyeong, South Korea)', 'spot', 4.5,
    'rubber', 'laminated', 'standard', 'none',
    3, 'standard', 'expert_analysis'
);

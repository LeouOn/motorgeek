-- Mercedes-Benz / AMG Reliability + Build Quality Score Inserts
-- 7 cars: CLS 550 C218, E500 W211, E55 AMG W210, EQS V297, GLC 43 X253, S-Class W222, C63 S W206
-- Scoring verified against calibration: W213 E-Class Rel=78 Q=75.5, C300 W205 Rel=82 Q=72,
--   SL 63 R232 Rel=70 Q=77, 500E W124 Rel=78 Q=83.5
-- Reliability weights: engine=0.25, transmission=0.25, chassis=0.15, electronics=0.15, ease_of_repair=0.20
-- Q-factor weights: body=0.25, nvh=0.10, interior=0.20, paint=0.15, elec_aging=0.15, cosmetic_aging=0.15
-- Catastrophe penalty (reliability only): if ANY dim < 50, penalty = 0.85 + (min/50)*0.15

-- ============================================================
-- RELIABILITY INSERTS (IDs 241-247)
-- ============================================================

-- 1. CLS 550 C218 (car_id=82) Rel=68.9 | NO catastrophe
-- dims: engine=72, transmission=70, chassis=72, electronics=68, ease_of_repair=62
-- raw = 72*0.25 + 70*0.25 + 72*0.15 + 68*0.15 + 62*0.20 = 18.0+17.5+10.8+10.2+12.4 = 68.9
-- M278 4.6L twin-turbo V8 on W212-derived platform. Balance shaft and valve stem seal concerns.
-- 7G-Tronic 722.9 mechatronic sleeve at 80-120K. AIRMATIC on some. Aging COMAND electronics.
INSERT INTO reliability (
    id, car_id, source, reliability_score,
    score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair,
    common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues
) VALUES (
    241, 82, 'sample', 68.9,
    72, 70, 72, 68, 62,
    '["M278 balance shaft gear wear (80-120K, engine-out job)","7G-Tronic 722.9 mechatronic sleeve (80-130K)","AIRMATIC air springs (if equipped, $1.5-2K/corner)","DI carbon buildup on intake valves (walnut blast 80-100K)","COMAND infotainment glitches (aging firmware)","Valve cover gasket leaks"]',
    1400, 4, 'Good (Mercedes specialist network)', 'Moderate (tight V8 bay, AIRMATIC complexity)',
    '{"M278": "Same balance shaft family as M272/M276; 80-120K onset. Engine-out on V8 = $5-7K.", "722.9": "3rd-gen conductor plate improved over early versions but still a wear item. Harsh 1-2 shift is early warning.", "AIRMATIC": "Common on CLS; $1.5-2K per corner at 100K+. Coil conversion bypasses this.", "carbon_buildup": "Direct injection legacy — walnut blasting every 80-100K ($800-1200)."}'
);

-- 2. E500 W211 (car_id=79) Rel=70.7 | CATASTROPHE: electronics=48
-- dims: engine=85, transmission=78, chassis=68, electronics=48, ease_of_repair=65
-- raw = 85*0.25 + 78*0.25 + 68*0.15 + 48*0.15 + 65*0.20 = 21.25+19.5+10.2+7.2+13.0 = 71.15
-- penalty = 0.85 + (48/50)*0.15 = 0.994 | 71.15*0.994 = 70.7231 -> 70.7
-- M113 5.0L V8 is bulletproof. But SBC brakes are THE nightmare — service life counter, $2-3K.
-- AIRMATIC, SAM module battery drain, biodegradable wiring harness (pre-2004 cars).
INSERT INTO reliability (
    id, car_id, source, reliability_score,
    score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair,
    common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues
) VALUES (
    242, 79, 'sample', 70.7,
    85, 78, 68, 48, 65,
    '["SBC brake pump failure (service life counter, $2-3K)","AIRMATIC air springs ($1.5-2K/corner at 80K+)","SAM module battery drain","Biodegradable wiring harness (pre-2004 models)","Fuel pump failure","COMAND display pixel fade","Catalytic converter aging"]',
    1600, 6, 'Good (Mercedes specialist network, parts plentiful)', 'Moderate (M113 very accessible, but SBC limits DIY)',
    '{"M113_V8": "3-valve, non-DI,SOHC design — simple and robust. One of Mercedes'' best V8s. No balance shaft issues.", "722.6_transmission": "5-speed automatic is one of Mercedes'' best. Extremely reliable, few known failure modes.", "SBC_nightmare": "Sensotronic Brake Control has a hard service life counter. When it triggers, brakes fail-safe to hydraulic-only. Mercedes extended warranty on this. Many owners do SBC delete (software + conventional brakes).", "AIRMATIC": "Standard W211 issue — $1.5-2K per corner. Coil spring conversion is popular bypass.", "wiring": "Pre-2004 cars have biodegradable insulation that crumbles. Full harness replacement $2-4K."}'
);

-- 3. E55 AMG W210 (car_id=67) Rel=71.8 | CATASTROPHE: chassis=45
-- dims: engine=88, transmission=80, chassis=45, electronics=70, ease_of_repair=68
-- raw = 88*0.25 + 80*0.25 + 45*0.15 + 70*0.15 + 68*0.20 = 22.0+20.0+6.75+10.5+13.6 = 72.85
-- penalty = 0.85 + (45/50)*0.15 = 0.985 | 72.85*0.985 = 71.75725 -> 71.8
-- AMG hand-built M113 5.4L V8 is legendary reliable. 722.6 5-speed is excellent.
-- But W210 RUST is catastrophic — structural rust on subframes, floors, spring perches, fenders.
INSERT INTO reliability (
    id, car_id, source, reliability_score,
    score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair,
    common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues
) VALUES (
    243, 67, 'sample', 71.8,
    88, 80, 45, 70, 68,
    '["Structural rust — rear subframes, floor pans, spring perches, jack points","Fender lip and wheel arch rust","ASR traction control module failure","Radiator leaking (plastic end tanks)","Window regulator failure","Catalytic converter aging","Headlamp wiring degradation"]',
    1100, 3, 'Good (Mercedes specialist network)', 'Good (simple engine bay, M113 very accessible)',
    '{"M113_AMG": "Hand-finished by AMG — one of the most reliable V8s Mercedes ever built. Non-DI, 3-valve, SOHC. No balance shaft issues. 300K+ mile examples exist.", "722.6": "5-speed automatic — proven and robust. AMG-fortified torque converter. Rarely fails below 200K.", "W210_rust": "Mercedes'' worst rust era. Inadequate galvanization, water traps in sill cavities. Rear subframe rust is structural and dangerous. Spring perch rust can cause suspension collapse. Pre-2003 cars are worst affected.", "electronics": "Simple by modern standards — limited ECUs, no SBC, no complex infotainment. ASR module the main electronic failure point."}'
);

-- 4. EQS V297 (car_id=122) Rel=72.7 | NO catastrophe (min=50 exactly)
-- Engine -> motor/drivetrain, Transmission -> reduction gear
-- dims: engine(motor)=86, transmission(reduction gear)=88, chassis=72, electronics=56, ease_of_repair=50
-- raw = 86*0.25 + 88*0.25 + 72*0.15 + 56*0.15 + 50*0.20 = 21.5+22.0+10.8+8.4+10.0 = 72.7
-- Electric drivetrain is inherently simpler and more reliable. Reduction gear is near-bulletproof.
-- But MBUX Hyperscreen software bugs are well-documented. EV = dealer-only for most repairs.
INSERT INTO reliability (
    id, car_id, source, reliability_score,
    score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair,
    common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues
) VALUES (
    244, 122, 'sample', 72.7,
    86, 88, 72, 56, 50,
    '["MBUX Hyperscreen software glitches (freezes, reboots)","12V auxiliary battery drain","AIRMATIC air springs (if equipped)","OTA update failures requiring dealer visit","HV battery preconditioning software bugs","Door handle extension mechanism","Rear axle steering calibration (early units)"]',
    800, 2, 'Limited (dealer-only for EV drivetrain)', 'Difficult (EV systems, dealer tools required)',
    '{"electric_drivetrain": "Permanent magnet synchronous motor with single-speed reduction gear — fewer than 20 moving parts vs 2000+ in ICE. Inherent reliability advantage. Battery warranty 10yr/155K mi.", "reduction_gear": "Single-speed planetary gear set — extremely simple. No clutch packs, no torque converter, no shift logic. Near-zero failure mode.", "MBUX": "Hyperscreen triple-screen system is complex — software bugs, occasional black screens, phantom reboots. Most fixed via OTA but some require dealer visit.", "12V_battery": "EQS uses 12V auxiliary battery for electronics — can drain if car sits unused. Not the traction battery.", "repairability": "EV-specific tools and safety certification required. Independent shops largely locked out. Dealer service is primary path."}'
);

-- 5. GLC 43 X253 (car_id=53) Rel=73.4 | NO catastrophe
-- dims: engine=76, transmission=78, chassis=72, electronics=70, ease_of_repair=68
-- raw = 76*0.25 + 78*0.25 + 72*0.15 + 70*0.15 + 68*0.20 = 19.0+19.5+10.8+10.5+13.6 = 73.4
-- M276 3.0L twin-turbo V6 (AMG-modified). 9G-Tronic AMG Speedshift.
-- Generally reliable platform. SUV engine bay more accessible than sedan counterparts.
INSERT INTO reliability (
    id, car_id, source, reliability_score,
    score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair,
    common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues
) VALUES (
    245, 53, 'sample', 73.4,
    76, 78, 72, 70, 68,
    '["M276 balance shaft wear (80-120K, less severe than M272)","9G-Tronic conductor plate ($600 part, 80-120K)","Air suspension (AIRMATIC, if equipped)","Water pump failure","PCV system breather","Brake pad/rotor wear (AMG sport brakes)"]',
    1000, 2, 'Good (Mercedes dealer + specialist network)', 'Moderate (SUV bay accessible, but AMG parts premium)',
    '{"M276_AMG": "AMG-modified M276 λ 3.0L biturbo V6. Improved over M272 — 60-degree architecture, no catastrophic balance shaft gear. AMG-specific tuning but same block family.", "9G-Tronic_725.0": "Far more reliable than 722.9 it replaced. Conductor plate the main wear item (~$600). AMG Speedshift has faster shifts but same internal architecture.", "SUV_advantage": "SUV engine bay is more accessible than C-Class sedan counterpart — easier to access turbos, manifold, and accessories.", "chassis": "X253 GLC platform is well-proven. Air suspension is the main chassis expense at $1.5-2K/corner."}'
);

-- 6. S-Class W222 (car_id=42) Rel=66.7 | NO catastrophe
-- dims: engine=72, transmission=74, chassis=66, electronics=62, ease_of_repair=55
-- raw = 72*0.25 + 74*0.25 + 66*0.15 + 62*0.15 + 55*0.20 = 18.0+18.5+9.9+9.3+11.0 = 66.7
-- M278 4.6L twin-turbo V8. Flagship complexity: dual 12.3" screens, COMAND, numerous ECUs.
-- AIRMATIC standard, ABC optional. 7G-Tronic (early) or 9G-Tronic (post-2017).
-- Low ease_of_repair reflects flagship cost — expensive parts, limited DIY.
INSERT INTO reliability (
    id, car_id, source, reliability_score,
    score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair,
    common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues
) VALUES (
    246, 42, 'sample', 66.7,
    72, 74, 66, 62, 55,
    '["M278 balance shaft gear wear (80-120K, engine-out, $5-7K)","M278 valve stem seals (oil consumption TSB)","DI carbon buildup (walnut blast 80-100K)","AIRMATIC air springs ($1.5-2K/corner at 100K+)","7G-Tronic mechatronic sleeve (early cars, 80-130K)","COMAND screen delamination/blanking","SAM module electrical gremlins","Engine mount failure (60-100K)","Coolant leak from thermostat housing"]',
    1800, 5, 'Good (Mercedes dealer + specialist network)', 'Difficult (flagship complexity, expensive parts)',
    '{"M278_V8": "Same balance shaft family issue. 80-120K onset. Engine-out on V8 = $5-7K. Valve stem seals revised 2016+. Carbon buildup from DI requires walnut blasting.", "transmission": "Early W222 used 7G-Tronic 722.9 (same mechatronic issues). Post-2017 facelift switched to 9G-Tronic 725.0 (much improved). 2017+ cars are the sweet spot.", "AIRMATIC_S-Class": "Standard on W222 — not optional. Every S-Class will need air spring replacement. $1.5-2K per corner, heavier car = faster wear.", "electronics_complexity": "W222 was Mercedes'' most complex car at launch. Dual 12.3 screens, COMAND Online, night vision option, 360 camera, massage seats, fragrance system, magic body control. More potential failure points than any non-Maybach Mercedes.", "flagship_tax": "Parts and labor carry the S-Class premium. Independent specialists charge 20-40% more than E-Class for same jobs due to complexity."}'
);

-- 7. C63 S W206 (car_id=117) Rel=60.9 | CATASTROPHE: ease_of_repair=48
-- The controversial P4HEV: M139l 2.0L turbo 4-cyl + electric motor replacing the beloved V8.
-- dims: engine=68, transmission=65, chassis=67, electronics=56, ease_of_repair=48
-- raw = 68*0.25 + 65*0.25 + 67*0.15 + 56*0.15 + 48*0.20 = 17.0+16.25+10.05+8.4+9.6 = 61.3
-- penalty = 0.85 + (48/50)*0.15 = 0.994 | 61.3*0.994 = 60.9322 -> 60.9
INSERT INTO reliability (
    id, car_id, source, reliability_score,
    score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair,
    common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues
) VALUES (
    247, 117, 'sample', 60.9,
    68, 65, 67, 56, 48,
    '["PHEV battery management system glitches","Rear differential failures (early production)","MBUX software bugs (freezes, black screens)","400V electrical system warning lights (false positives)","AMG Ride Control+ damper failures","Rear axle steering sensor faults","E-motor inverter thermal management (track use)","Brake-by-wire calibration issues"]',
    2200, 3, 'Limited (AMG dealer primary, PHEV specialist rare)', 'Difficult (PHEV system, dealer tools, 400V safety)',
    '{"M139l": "AMG hand-built 2.0L turbo based on proven M139 from A45 S. Making 476hp from 2.0L is extreme specific output — long-term durability at high stress unknown. Electric spool turbocharger is new technology with limited track record.", "PHEV_system": "400V lithium-ion battery + 204hp e-motor integrated into 9G-Tronic. Complex thermal management, BMS, and inverter. Battery warranty 10yr/62K mi but replacement cost is $15-20K+", "controversy": "Replaced the beloved W205 C63''s 4.0L twin-turbo V8 with a 4-cylinder hybrid. Enthusiast backlash was immense. Power output is higher (671hp combined) but character is fundamentally different.", "repairability": "PHEV system requires HV-certified technicians. Independent shops mostly locked out. 400V safety protocols limit DIY to non-hybrid components only.", "platform": "W206 is new platform with some early teething issues. Rear differential and rear axle steering had early production failures. Most resolved by 2024."}'
);


-- ============================================================
-- BUILD QUALITY Q-FACTOR INSERTS (IDs 98-104)
-- ============================================================

-- 1. CLS 550 C218 (car_id=82) Q=73.0
-- dims: body=77, nvh=75, interior=76, paint=75, elec_aging=64, cosmetic_aging=68
-- Q = 77*0.25 + 75*0.10 + 76*0.20 + 75*0.15 + 64*0.15 + 68*0.15
--   = 19.25 + 7.5 + 15.2 + 11.25 + 9.6 + 10.2 = 73.0
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
    98, 82, 73.0,
    77, 75, 76,
    75, 64, 68,
    'W212-derived platform with CLS-specific body — sleeker roofline, frameless doors, wider rear haunches. Steel and aluminum hybrid construction with laser-brazed roof joint. Good structural rigidity despite pillarless coupe profile. Panel fit above average for the era.',
    'Mercedes coupe standards apply — acoustic laminated front glass, double door seals, asphalt-lined floor pans, hydraulic engine mounts. The twin-turbo V8 is intrinsically smooth. Wind noise well-suppressed despite frameless doors. Road noise the weakest link on rough surfaces.',
    'CLS-specific interior with flowing dashboard design, dual-zone trim, and ambient lighting (post-facelift). Leather quality is genuine Mercedes premium — not Designo-level but above E-Class sedan. Real wood or carbon fiber trim. Sport seats with good bolstering. Materials feel cohesive.',
    'Multi-stage paint process on galvanized steel. CLS-specific panels painted to high Mercedes standards. Good corrosion resistance — the C218 generation benefitted from improved galvanizing over earlier W219 CLS. Minor clear coat thinning on horizontal surfaces at 10+ years.',
    'COMAND Online system ages — slow response, outdated graphics, occasional reboots. Harmon/Kardon Logic 7 amp can develop channel dropout. Instrument cluster pixel fade on early units. Not catastrophic but noticeably dated compared to newer MBUX systems.',
    'Interior holds up well — leather develops patina rather than cracking. Dashboard materials remain tight. Soft-touch rubberized coatings on center console and door pulls begin to peel at 8-10 years. Chrome trim retains finish. Wood trim does not delaminate.',
    'CLS 550 C218 Q-score 73.0. W212-based coupe with premium CLS-specific interior. Build quality above W212 sedan but below S-Class flagship. Body construction and interior materials are highlights. Aging COMAND electronics (-11) and soft-touch surface peeling (-7 cosmetic) are the deductions.',
    'W212 (coupe variant)', 'Sindelfingen (Germany)', 'laser_brazed', 4.0,
    'hydraulic', 'acoustic_laminated', 'premium', 'real_wood',
    5, 'above_average', 'sample'
);

-- 2. E500 W211 (car_id=79) Q=65.6
-- dims: body=72, nvh=70, interior=65, paint=70, elec_aging=52, cosmetic_aging=62
-- Q = 72*0.25 + 70*0.10 + 65*0.20 + 70*0.15 + 52*0.15 + 62*0.15
--   = 18.0 + 7.0 + 13.0 + 10.5 + 7.8 + 9.3 = 65.6
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
    99, 79, 65.6,
    72, 70, 65,
    70, 52, 62,
    'W211 body represents the era when Mercedes began cost-cutting from W210 peak but before W212 recovery. Steel unibody with partial galvanization — better than W210 rust issues but not up to W212 standards. Panel fit is acceptable. Structural rigidity is good — Mercedes still over-engineered crash structure.',
    'Good NVH isolation for the era — hydraulic engine mounts, double door seals, asphalt-lined floor pans. The M113 V8 is intrinsically smooth. Acoustic damping on firewall. Wind noise acceptable at autobahn speeds. Not W222-quiet but solid for mid-2000s.',
    'Interior quality dip compared to W210 — harder plastics on lower dash and door panels, cheaper-feeling switchgear on climate controls. Upper dash and seats still use quality leather and real wood veneer. Fit and finish is precise but materials selection is the letdown. The premium-ness gap vs BMW E60 of the same era is noticeable.',
    'Multi-stage paint on galvanized steel. Significant improvement over W210 rust issues. Pre-2004 cars less thoroughly galvanized than post-facelift. Clear coat holds up well. Rust rare unless accident-repaired. Minor paint chipping on leading edges after 15+ years.',
    'SBC (Sensotronic Brake Control) is the defining electrical aging issue — electromechanical brake system with service life counter that eventually requires pump replacement ($2-3K). COMAND navigation display pixel fade. SAM module under rear seat can develop corrosion. Pre-2004 biodegradable wiring insulation crumbles. These are real and expensive aging issues.',
    'Dashboard upper surface holds up. Seat leather is durable Mercedes quality — develops patina rather than cracking. Real wood trim does not delaminate. Lower plastics scratch easily. Soft-touch coatings on center console peel. Door panel vinyl can pucker at seams. Rubber door seals compress and leak wind noise at 15+ years.',
    'E500 W211 Q-score 65.6. The M113 V8-powered luxury sedan from Mercedes'' cost-cutting era. Body and paint improved over W210, but interior materials dipped significantly. SBC brakes are the defining electrical aging issue (-13). Interior materials (-10 from W213) and cosmetic aging reflect 20-year-old materials technology.',
    'W211 (E-Class)', 'Sindelfingen (Germany)', 'spot', 4.5,
    'hydraulic', 'laminated', 'standard', 'real_wood',
    5, 'good', 'sample'
);

-- 3. E55 AMG W210 (car_id=67) Q=63.3
-- dims: body=58, nvh=68, interior=78, paint=48, elec_aging=65, cosmetic_aging=63
-- Q = 58*0.25 + 68*0.10 + 78*0.20 + 48*0.15 + 65*0.15 + 63*0.15
--   = 14.5 + 6.8 + 15.6 + 7.2 + 9.75 + 9.45 = 63.3
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
    100, 67, 63.3,
    58, 68, 78,
    48, 65, 63,
    'W210 body is Mercedes'' rust nadir — inadequate galvanization, water traps in sill cavities and rear subframes. Spot-welded steel unibody with insufficient seam sealing. E55 AMG adds AMG-specific front/reward bumper covers and side skirts but shares the same rust-prone body. Structural rust on rear subframes and spring perches is well-documented and dangerous.',
    'Bank-vault feel from Mercedes NVH engineering. Hydraulic engine mounts isolate the AMG V8 well. Double door seals, asphalt-lined floor pans, acoustic-damped firewall. Wind noise well-controlled. The M113 AMG V8 is smooth at idle and cruise — NVH was a Mercedes strength even during the rust era.',
    'Peak Mercedes interior — this is the era when MB still used premium materials. Real burled walnut or carbon fiber trim, thick leather on seats and door panels, soft-touch surfaces everywhere, precision switchgear with satisfying detents. AMG-specific sport seats with two-tone leather. The interior is where the W210 still feels expensive.',
    'Catastrophic — W210 rust is Mercedes'' worst paint/corrosion chapter. Inadequate galvanization combined with water traps in body cavities. Fender lips, wheel arches, door bottoms, rear subframes, floor pans, spring perches, jack points — all rust zones. Mercedes eventually issued TSBs and extended corrosion warranties. Pre-2001 cars are worst affected.',
    'Simple electronics by modern standards — fewer ECUs, no complex infotainment, no SBC. ASR traction control module is the main failure point. Instrument cluster pixel fade on early VDO units. Wiring harness insulation degradation on pre-2000 cars (biodegradable insulation). Overall, the simplicity is an advantage — fewer things to fail.',
    'Interior materials are excellent and age beautifully — leather develops rich patina, wood retains luster, dashboard does not crack. But exterior rubber components (seals, trim, window sweeps) degrade from 20+ years of exposure. Chrome trim pits in harsh climates. The disconnect: gorgeous interior, rotting exterior.',
    'E55 AMG W210 Q-score 63.3. The tale of two cars: AMG hand-built M113 V8 with premium interior materials (78) versus Mercedes'' worst body rust era (58 body, 48 paint). Interior is peak Mercedes quality that modern cars struggle to match. But structural rust is an existential threat. The AMG engine elevates the experience; the W210 body undermines it.',
    'W210 (E-Class)', 'Sindelfingen (Germany)', 'spot', 5.0,
    'hydraulic', 'laminated', 'premium', 'real_wood',
    4, 'good', 'sample'
);

-- 4. EQS V297 (car_id=122) Q=79.9
-- dims: body=88, nvh=85, interior=85, paint=82, elec_aging=66, cosmetic_aging=68
-- Q = 88*0.25 + 85*0.10 + 85*0.20 + 82*0.15 + 66*0.15 + 68*0.15
--   = 22.0 + 8.5 + 17.0 + 12.3 + 9.9 + 10.2 = 79.9
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
    101, 122, 79.9,
    88, 85, 85,
    82, 66, 68,
    'Aluminum-intensive body with carbon fiber roof panel and steel reinforcements in crash structure. Purpose-built EV architecture (EVA2 platform) with no ICE packaging compromises — optimal weight distribution, low center of gravity from floor-mounted battery. Laser-brazed joints, structural adhesives, and extensive use of cast aluminum nodes. Panel gaps consistently under 4mm.',
    'Best-in-class NVH for a production car at launch — 0.20 Cd drag coefficient means virtually zero wind noise. Acoustic laminated glass all around, twin-door seals, and no engine noise means total silence at speed. Road noise is the only remaining sound source, well-damped by low-profile tires and acoustic wheel liners. The gold standard for EV quietness.',
    'Premium throughout — MBUX Hyperscreen spans full dashboard width. Open-pore woods, real metal trim, Nappa leather standard. Vegan leather option (artico/man-made). Dashboard wrapped in stitched leather. Optional rear executive seats with massage. Materials selection rivals Bentley Flying Spur. The interior is the EQS''s strongest statement.',
    'Multi-stage paint process (up to 7 layers including primer, base, metallic, clear) on aluminum and steel. Electro-dip galvanization on steel components. Excellent corrosion resistance — EV architecture eliminates many traditional corrosion points (no exhaust, no fuel lines under body). Paint quality is Mercedes flagship standard.',
    'Too new for definitive aging assessment, but risks are clear: MBUX Hyperscreen relies on ongoing software support — when Mercedes stops updating it, functionality will degrade. 12V auxiliary system drains if car sits. HV battery capacity will degrade over time. OTA update dependency means the car needs network connectivity to stay current.',
    'High-quality materials should age well — Nappa leather is durable, open-pore wood does not delaminate, metal trim does not corrode. But the Hyperscreen is a large glass surface vulnerable to cracking and delamination over decades. Seat comfort foam may compress. EV-specific: battery thermal management adds structural complexity to floor assembly.',
    'EQS V297 Q-score 79.9. Purpose-built EV flagship with best-in-class body construction and NVH isolation. Aluminum-intensive EVA2 platform with laser welding and structural adhesives. Interior materials rival ultra-luxury brands. Deductions for long-term electrical aging uncertainty (software-dependent MBUX, -14) and cosmetic aging unknowns (-12). Second only to the 500E W124 among Mercedes in this database.',
    'EVA2 (purpose-built EV)', 'Sindelfingen (Germany)', 'laser_brazed', 3.5,
    'solid_rubber', 'acoustic_laminated', 'nappa', 'real_wood_open_pore',
    7, 'outstanding', 'sample'
);

-- 5. GLC 43 X253 (car_id=53) Q=70.6
-- dims: body=74, nvh=68, interior=72, paint=74, elec_aging=65, cosmetic_aging=67
-- Q = 74*0.25 + 68*0.10 + 72*0.20 + 74*0.15 + 65*0.15 + 67*0.15
--   = 18.5 + 6.8 + 14.4 + 11.1 + 9.75 + 10.05 = 70.6
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
    102, 53, 70.6,
    74, 68, 72,
    74, 65, 67,
    'C-Class-based SUV platform (X253) with reinforced structure for SUV duty. Steel unibody with partial aluminum panels (hood, tailgate). Good crash structure and panel fit. Spot-welded and laser-brazed joints. Solid for the segment but not flagship-level — shared platform with C-Class means structural compromises vs purpose-built.',
    'SUV NVH is class-competitive but not S-Class level. Engine bay insulation is adequate. Acoustic laminated front glass on premium packages. Wind noise increases at SUV aerodynamics. The M276 biturbo V6 is smooth but not whisper-quiet under acceleration. Road noise from wider AMG tires is noticeable on coarse surfaces.',
    'AMG-specific interior trim — sport seats with two-tone leather, DINAMICA suede inserts, carbon fiber or brushed aluminum trim. Above average for the segment but clearly shared C-Class architecture — same HVAC controls, same steering wheel base, same switchgear. Leather quality is good but not Nappa-grade standard. AMG branding throughout adds perceived quality.',
    'Modern Mercedes multi-stage paint process on galvanized steel. Good corrosion resistance — the X253 generation benefitted from improved galvanizing. AMG-specific paint options (designo colors) available at premium. Paint thickness consistent. Clear coat holds up well at 5-8 years.',
    'MBNT infotainment (COMAND-based) ages — slow response on older firmware, map updates expensive. Instrument cluster is traditional analog + small screen (pre-facelift). AMG-specific electronics (performance display, drive mode selector) are reliable. Harman/Kardon surround sound amp can develop channel dropout at 5+ years.',
    'Interior holds up well for daily-driven SUV — DINAMICA suede is more durable than leather on seat bolsters. Carbon fiber trim does not fade. Cup holder coatings wear. Steering wheel leather can show wear at 60K+ miles. SUV duty means more cargo area scuffing. Overall above average for the class.',
    'GLC 43 X253 Q-score 70.6. AMG-enhanced C-Class SUV platform with good but not exceptional build quality. Interior materials benefit from AMG-specific trim but shared architecture with C-Class is evident. Solid paint and body construction. Electronics aging is the main concern (-5 from modern MBNT). A well-built SUV but not in the same league as S-Class or EQS.',
    'C-Class (X253 SUV)', 'Bremen (Germany)', 'spot', 4.2,
    'hydraulic', 'laminated', 'premium', 'carbon_fiber',
    5, 'above_average', 'sample'
);

-- 6. S-Class W222 (car_id=42) Q=77.2
-- dims: body=82, nvh=82, interior=85, paint=80, elec_aging=62, cosmetic_aging=68
-- Q = 82*0.25 + 82*0.10 + 85*0.20 + 80*0.15 + 62*0.15 + 68*0.15
--   = 20.5 + 8.2 + 17.0 + 12.0 + 9.3 + 10.2 = 77.2
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
    103, 42, 77.2,
    82, 82, 85,
    80, 62, 68,
    'Flagship Mercedes body engineering — aluminum/steel hybrid with aluminum hood, front fenders, trunk lid, and doors. Laser-brazed roof joint, structural adhesives throughout, double-skinned panels in crash zones. Extensive use of hot-stamped boron steel in A/B-pillars and rockers. Panel gaps consistently under 4mm. The W222 set the benchmark for body quality in its class.',
    'Best-in-class NVH at launch — acoustic laminated glass front and rear, double-door seals, hydraulic engine mounts, extensive asphalt and foam sound deadening. Magic Body Control (optional) uses stereo camera to read road surface. The M278 twin-turbo V8 is barely perceptible at idle. Wind noise virtually absent at autobahn speeds. The gold standard for luxury sedan quietness.',
    'The interior that defined luxury for a generation — flowing dashboard design, dual 12.3 screens (post-facelift), ambient lighting with 64 colors. Designo Nappa leather, open-pore woods (eucalyptus, walnut, ash), real aluminum trim. Seat comfort unmatched — hot stone massage, energizing comfort control. Rear-seat executive package available. Only the Maybach S-Class surpasses it.',
    'Mercedes flagship paint process — multi-stage with up to 7 layers including cathodic dip primer, base coat, metallic/candy layers, and clear coat. Electro-dip galvanization on all steel components. Ceramic Pro factory option available. Paint quality is the best Mercedes produces — consistent thickness, deep gloss, excellent long-term durability.',
    'Complex electronics will define the W222''s aging — dual 12.3 screens will eventually have pixel/brightness issues, COMAND Online depends on cellular connectivity that Mercedes will eventually discontinue, and the car has over 100 ECUs. Magic Body Control air suspension struts are $3-5K per corner. Night vision and 360 camera systems add failure points.',
    'Premium materials age well — Nappa leather develops patina rather than cracking. Real wood does not delaminate. Metal trim retains finish. But soft-touch rubberized coatings on center console and lower trim begin to deteriorate at 8-10 years. The dual-screen setup will look dated as newer designs adopt larger integrated displays. Dashboard leather stitching holds up well.',
    'S-Class W222 Q-score 77.2. Mercedes'' flagship from 2014-2020 — the benchmark for luxury sedan build quality in its era. Aluminum/steel body with laser welding. Interior materials are second only to Maybach among production cars. Deductions for electronics aging complexity (-13: 100+ ECUs, screen dependency) and soft-touch surface deterioration (-7 cosmetic). Only 1.3 points below the SL 63 R232 despite being a much higher-volume car.',
    'W222 (S-Class)', 'Sindelfingen (Germany)', 'laser_brazed', 3.8,
    'hydraulic', 'acoustic_laminated', 'designo_nappa', 'real_wood_open_pore',
    7, 'outstanding', 'sample'
);

-- 7. C63 S W206 (car_id=117) Q=72.7
-- dims: body=78, nvh=76, interior=78, paint=76, elec_aging=56, cosmetic_aging=68
-- Q = 78*0.25 + 76*0.10 + 78*0.20 + 76*0.15 + 56*0.15 + 68*0.15
--   = 19.5 + 7.6 + 15.6 + 11.4 + 8.4 + 10.2 = 72.7
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
    104, 117, 72.7,
    78, 76, 78,
    76, 56, 68,
    'W206 C-Class platform — all-new for 2022 with significantly improved body rigidity over W205. Steel unibody with aluminum hood and front fenders. Laser-brazed roof joint. Improved spot weld density and structural adhesives over previous generation. Panel gaps tight and consistent. AMG-specific front/rear bumper covers and wider fender flares integrated cleanly.',
    'PHEV advantage — the C63 S can operate in pure EV mode making it eerily quiet at low speeds. Acoustic laminated glass, improved door sealing, and AMG-specific exhaust tuning. The 4-cylinder turbo is less sonically satisfying than the previous V8 but cabin isolation is objectively better. Wind noise well-suppressed for a compact sedan. Road noise from wider AMG rubber is the primary sound source.',
    'W206 interior is a genuine step up from W205 — vertical MBUX infotainment screen inspired by S-Class, turbine-look air vents, ambient lighting with multiple zones. AMG-specific sport seats with DINAMICA suede and Nappa leather. Real metal trim (not plastic chrome). Digital-first cockpit feels modern and premium. The interior is the C63 S''s strongest quality statement.',
    'Modern Mercedes multi-stage paint on galvanized steel — good quality and consistent application. AMG-specific colors (obsidian black metallic, spectral blue) are deep and lustrous. Corrosion resistance is modern Mercedes standard — well-galvanized with electro-dip process. Limited long-term data (car is 2022+) but paint quality matches Mercedes contemporary standards.',
    'PHEV complexity is the defining aging risk — 400V battery management system, e-motor inverter, and integrated thermal management add significant electronic complexity beyond a conventional ICE car. MBUX system depends on OTA updates and cellular connectivity. When Mercedes stops supporting this generation, functionality will degrade. The P4HEV system is unproven beyond 5 years.',
    'Materials are high quality and should age well in theory — DINAMICA suede is durable, Nappa leather is premium, metal trim retains finish. But the car is too new (2022+) for meaningful long-term cosmetic aging data. Screen-heavy interior may look dated as display technology evolves. Limited historical precedent for 400V PHEV aging.',
    'C63 S W206 Q-score 72.7. Well-built modern AMG with excellent interior materials and PHEV-quiet NVH. W206 platform is a genuine quality improvement over W205. But the 400V PHEV system adds unproven electronic complexity (-14 elec aging) and limited long-term cosmetic data (-7). The controversial 4-cylinder replacement for the V8 doesn''t affect build quality but colors perception of the entire car.',
    'W206 (C-Class AMG)', 'Bremen (Germany)', 'laser_brazed', 3.9,
    'hydraulic', 'acoustic_laminated', 'nappa', 'carbon_fiber',
    6, 'very_good', 'sample'
);

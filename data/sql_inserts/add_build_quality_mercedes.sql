-- Mercedes-Benz Build Quality Q-factor Inserts
-- Era calibration: W124=peak, W210=decline, W212=mixed, W213/W205=modern recovery
-- Q = body*0.25 + nvh*0.10 + interior*0.20 + paint*0.15 + elec*0.15 + cosmetic*0.15

-- ============================================================
-- CLASSIC MERCEDES (1950s-1970s)
-- ============================================================

-- 300 SL Gullwing W198 (1954-1957) car_id=135 reliability=72
-- Museum piece. Hand-built race car for the road. 70+ years of materials aging.
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
    135, 55.5,
    85, 42, 60,
    45, 35, 40,
    'Tubular space frame with hand-formed aluminum body panels (hood, doors, trunk lid). Extraordinary engineering for 1954 — direct descendant of W194 race car. Hand-fitted panels by Mercedes Sindelfingen craftsmen, but 1950s precision is not modern laser-welding.',
    'Zero NVH engineering by modern standards. Race-bred chassis transmits every surface imperfection. No sound deadening material. Gearbox whine, engine roar, and wind noise define the driving experience. 1950s isolation technology.',
    'Spartan 1950s racing cockpit with functional gauges and minimal luxury. Beautiful to look at but not a luxury interior by any era standard. Leather and Bakelite were period-appropriate quality materials.',
    '70+ years means virtually every surviving Gullwing has been repainted at least once. Original nitrocellulose lacquer was period-correct but thin. Galvanizing did not exist — bare aluminum panels resist corrosion but steel subframe does not.',
    'Minimal 1950s electrical system: few circuits, simple wiring. Bosch mechanical components survive but wiring insulation becomes brittle and cracks at 50+ years. Capacitor and coil failures are routine.',
    'Dashboard leather shrinks and cracks. Steering wheel Bakelite chips. Rubber seals harden and leak. Seat leather splits at stress points. Most surviving examples are restored, making original-condition assessment difficult.',
    '300 SL Gullwing Q-score 55.5. Extraordinary hand-built engineering for 1954 but scored as a car, not a collectible. Body construction is the highlight — tubular space frame and aluminum panels were race-bred. Every other dimension suffers from 70 years of materials aging.',
    'bespoke', 'Sindelfingen (Germany)', 'spot', 6.0,
    'rubber', 'laminated', 'standard', 'none',
    3, 'minimal', 'sample'
);

-- 190 SL W121 (1955-1963) car_id=136 reliability=70
-- Entry-level SL, monocoque construction, not race-bred like 300 SL.
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
    136, 51.5,
    72, 48, 55,
    42, 38, 38,
    'Monocoque steel construction, heavier and less sophisticated than the 300 SL space frame. Standard Mercedes production of the 1950s — competent but not race-derived. Spot-welded steel panels with no galvanizing.',
    'Soft-top roadster with minimal insulation. Ponton-derived chassis transmits road noise directly. Canvas top provides negligible sound barrier. Engine noise prominent at all speeds.',
    'Entry-level positioning shows — simpler materials than 300 SL. Standard vinyl and cloth trim common; leather optional. Dashboard layout functional but not luxurious. Period-correct but not Mercedes-best.',
    '60+ years of aging on non-galvanized steel. Rust is the primary threat to survival — sills, floor pans, and wheel arches are vulnerability zones. Original paint was thin nitrocellulose.',
    'Simple 1950s electrical systems with few components. Wiring harness deterioration after 50+ years is nearly universal. Generator (not alternator) and mechanical regulator add reliability but primitive by modern standards.',
    'Canvas tops rot at 15-20 years. Seat foam disintegrates. Dashboard vinyl cracks. Chrome pitting on all exterior brightwork. Rubber weather seals harden and fail. Most survivors have been restored.',
    '190 SL Q-score 51.5. The 300 SL''s lesser sibling — competent 1950s roadster but never possessed the race-bred engineering of the Gullwing. Monocoque steel body and entry-level materials mean it scores lower across every dimension. Rust is the existential threat.',
    'bespoke', 'Sindelfingen (Germany)', 'spot', 6.5,
    'rubber', 'standard', 'standard', 'none',
    3, 'minimal', 'sample'
);

-- 280 SL Pagoda W113 (1967-1971) car_id=137 reliability=82
-- Legendary W113. Hand-built, meticulous engineering. But 1960s materials and 55+ years of aging.
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
    137, 64.9,
    88, 60, 72,
    55, 45, 50,
    'W113 unibody was meticulously engineered with the iconic pagoda-shaped hardtop providing exceptional rigidity. Hand-built at Sindelfingen with careful panel fit. Dual-circuit braking, crumple zones, and the concave hardtop were engineering firsts. Excellent for the 1960s.',
    'Roadster with detachable hardtop — inherently compromised NVH. Soft top versions transmit significant wind noise. Inline-6 is mechanically smooth but road and tire noise dominate. Some sound deadening in floor and firewall, better than British roadsters of the era.',
    'Genuine MB-Tex and optional leather held to Mercedes standards. Real wood or leather-wrapped steering wheel. Becker radio was premium for the era. Chrome fixtures and toggle switches had a quality feel. But 1960s dashboard plastics become brittle with age.',
    '55+ years means most Pagodas have been repainted. Original paint was high-quality for the era but pre-galvanization — rust on sills, floors, and wheel arches is common in unrestored cars. Pagoda Owners International reports rust as the #1 concern.',
    'Bosch electrical components generally durable. Points and condenser ignition requires regular maintenance. Wiring harness insulation becomes brittle at 40+ years. Fuel gauge senders fail. Simple system means fewer failure modes but no modern reliability.',
    'Dashboard padding cracks and shrinks in UV. Leather seats develop patina (acceptable) but foam collapses. Rubber seals throughout harden and leak. Chrome exterior trim pits. Pagoda hardtop seals shrink causing water ingress. MB-Tex outperforms leather for longevity.',
    '280 SL Pagoda Q-score 64.9. Meticulously hand-built 1960s Mercedes with engineering decades ahead of contemporaries. Body construction scores well (88) — the W113 unibory was exceptional for its era. Every other dimension suffers from 55+ years of materials aging. Better than a TR6, not as good as a W124.',
    'bespoke', 'Sindelfingen (Germany)', 'spot', 5.0,
    'rubber', 'laminated', 'standard', 'real_wood',
    3, 'standard', 'sample'
);

-- 560 SL R107 (1986-1989) car_id=138 reliability=80
-- R107, robust but not W124-tier. Standard Mercedes of the era.
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
    138, 66.6,
    82, 58, 68,
    65, 55, 58,
    'R107 chassis was overbuilt for a roadster — the platform survived essentially unchanged from 1971 to 1989. Heavy gauge steel throughout, robust subframes, and the removable hardtop added structural rigidity. Not W124-tier refinement but solid Mercedes construction.',
    'Roadster NVH compromises inherent — removable hardtop improves things significantly. V8 engine is smooth but transmits vibration through rubber mounts. Soft top allows wind noise at speed. Some sound deadening material in doors and floor but not sedan-level.',
    'Genuine leather and MB-Tex upholstery options. Real wood veneer on console and dash. Mercedes switchgear of the 1980s was satisfying and durable. But design was dated even when new — the R107 interior was essentially 1971 vintage updated with minor changes through 1989.',
    'Mercedes galvanized bodies starting mid-1980s — late R107 models benefit. Paint quality is good for the era. Soft top cars suffer from moisture exposure. Hardtop seals degrade causing water ingress. Some clear coat fading on horizontal surfaces at 35+ years.',
    'Bosch CIS fuel injection is robust. Climate control system (automatic) is the weak point — servo motors and vacuum actuators fail. Power windows and locks generally reliable. Becker radio holds up. Instrument cluster capacitors can leak.',
    'Leather seats wear at bolsters after 100K miles. Dashboard padding shrinks and cracks in sun-exposed cars. Wood veneer can delaminate at edges. Chrome exterior trim pits with age. Rubber body mounts and suspension bushings harden, causing harsh ride.',
    '560 SL Q-score 66.6. The R107 was solid 1980s Mercedes construction but not the legendary overengineering of the W124 sedan. Roadster packaging limits NVH and interior scores. The 18-year production run meant the design aged in place while competitors advanced.',
    'bespoke', 'Sindelfingen (Germany)', 'spot', 5.0,
    'rubber', 'laminated', 'standard', 'real_wood',
    4, 'standard', 'sample'
);

-- ============================================================
-- W124 ERA — PEAK MERCEDES (1990s)
-- ============================================================

-- 500E W124 (1990-1995) car_id=7 reliability=75
-- Porsche-assembled W124. Peak Mercedes overengineering. Hand-fitted by Porsche at Zuffenhausen.
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
    7, 83.5,
    95, 88, 88,
    85, 65, 72,
    'W124 body engineered to survive 30+ years — double-skinned panels, extensive galvanization, seam-sealed cavities, wax injection. 500E specifically hand-assembled by Porsche at Zuffenhausen: widened fenders, reinforced subframes, additional structural bracing. The gold standard of Mercedes body engineering.',
    'Bank-vault isolation is real — W124 development targeted 30-year durability. Hydraulic engine mounts, double-door seals, asphalt-lined floor pans, acoustic-damped dash panel. The 5.0L V8 is intrinsically smooth. Road noise almost nonexistent. Wind noise absent at autobahn speeds.',
    'Peak Mercedes interior: real wood veneer (burled walnut or zebrano), thick leather (optional), soft-touch surfaces everywhere, precision German switchgear with satisfying detents. Tolerances measured in tenths of millimeters. The 500E added sport Recaro seats and specific trim. Nothing rattles at 30 years.',
    'W124-era Mercedes paint on galvanized steel resists corrosion for decades. Multi-stage paint process with clear coat. 500E-specific panels were painted to Porsche standards. Rust rare unless accident-repaired. Some minor clear coat thinning on horizontal surfaces at 30+ years.',
    'Generally excellent but the M119 V8 adds complexity — wiring harness insulation degradation (biodegradable wiring insulation per Mercedes environmental mandate of the early 1990s) is a known issue. ASR traction control modules can fail. LH-SFI injection system is reliable.',
    'Interior holds up remarkably — leather develops patina rather than cracking. Real wood does not delaminate. Dashboard does not crack. Door panels stay tight. Rubber components (seals, bushings) are the primary aging items — softer compounds for NVH degrade at 20-25 years.',
    '500E W124 Q-score 83.5. The pinnacle of Mercedes-Benz build quality, elevated further by Porsche hand-assembly at Zuffenhausen. W124 platform was engineered for 30-year durability and delivers. Only deductions: biodegradable wiring insulation (-8 electrical), 30-year rubber aging (-5 cosmetic), M119 complexity.',
    'bespoke', 'Porsche Zuffenhausen (Germany)', 'spot', 3.5,
    'hydraulic', 'laminated', 'standard', 'real_wood',
    5, 'extensive', 'sample'
);

-- 500 SL R129 (1990-1998) car_id=139 reliability=75
-- R129 roadster. Good build, some typical roadster NVH compromises.
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
    139, 73.5,
    85, 62, 78,
    78, 60, 65,
    'R129 shares the W124-era overengineering philosophy — robust chassis, galvanized steel, extensive corrosion protection. Automatic roll bar and reinforced A-pillars for safety. But roadster structure can''t match sedan rigidity — cowl shake present with top down on uneven surfaces.',
    'Roadster NVH is inherently compromised — soft top allows wind noise even when raised. With hardtop fitted, isolation approaches W124 levels. V8 engine is smooth. Hydraulic engine mounts help. Some cowl resonance at certain speeds. Better than any contemporary roadster.',
    'W124-era Mercedes interior quality: real wood, thick leather, quality switchgear. Sport seats with multiple adjustments. Automatic wind deflector was innovative. But roadster packaging limits interior storage and some surfaces use harder materials than the sedan.',
    'Galvanized body with Mercedes multi-stage paint process. Hardtop cars age better than soft-top. Soft top mechanisms require maintenance to prevent water ingress. Some rust at jack points and behind wheel arches if drains clog. Generally good for 30+ years.',
    'Soft top mechanism adds significant electrical complexity — hydraulic pump, sensors, limit switches. Roll bar deployment system. Early models had wiring harness degradation (same biodegradable insulation as W124). Climate control servo failures. Bose speaker foam disintegration.',
    'Convertible-specific aging: soft top canvas deteriorates at 10-15 years, rear window clouds. Hydraulic top cylinders leak at 15-20 years. Seat leather wears faster due to UV exposure. Dashboard padding can shrink in sun-belt cars. Roll bar covers crack.',
    '500 SL R129 Q-score 73.5. W124-era Mercedes engineering applied to a roadster — solid but compromised by convertible architecture. Body and paint scores reflect the overengineering, NVH deduction for roadster nature. Electrical and cosmetic deductions for top mechanism complexity and UV exposure.',
    'bespoke', 'Sindelfingen (Germany)', 'spot', 4.5,
    'hydraulic', 'laminated', 'standard', 'real_wood',
    5, 'above_average', 'sample'
);

-- SL 600 R129 (1993-2001) car_id=140 reliability=65
-- V12 R129. Complex but still W129 platform.
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
    140, 69.5,
    83, 68, 75,
    72, 48, 60,
    'Same R129 platform as 500 SL with additional V12-specific reinforcements. The M120 V12 required modified subframes and engine mounts. Body construction is W124-era quality — galvanized, wax-injected, overbuilt. But the V12 adds heat stress to engine bay components.',
    'V12 is inherently smoother than V8 — the M120 is one of the silkiest engines ever made. NVH with hardtop is excellent, approaching W124 sedan levels. Soft top still allows wind noise. Hydraulic mounts standard. The SL 600 was the luxury-oriented SL, tuned for refinement over sport.',
    'Nappa leather standard on SL 600, a step above 500 SL trim. Real wood veneer, specific V12 badging. Exclusive interior color combinations. Mercedes switchgear of the era at its best. But same roadster packaging limitations as the 500 SL.',
    'Same galvanized body and paint process as 500 SL. V12 heat can accelerate paint degradation on hood over long periods. Soft top canvas and seals same as other R129 models. Hardtop cars age better.',
    'The M120 V12 doubles the complexity — two ignition coils, two distributors (early), 24 valves, two catalytic converters. Wiring harness degradation more critical with more circuits. Electronic throttle (ETA) failures. Soft top hydraulics. Climate control. The combination is significantly more failure-prone than V8 models.',
    'Same roadster aging as 500 SL plus V12 heat effects: under-hood rubber hoses and wiring age faster. Engine bay heat accelerates plastic component embrittlement. Same soft top and hydraulic cylinder issues. Nappa leather is softer but may not wear as well as standard leather.',
    'SL 600 R129 Q-score 69.5. The M120 V12 is magnificent but doubles the complexity penalty — electrical score drops to 48. Body and interior quality remain W124-era Mercedes excellence. The V12 heat soak accelerates cosmetic aging underhood. The smoothest R129 but the most expensive to maintain.',
    'bespoke', 'Sindelfingen (Germany)', 'spot', 4.5,
    'hydraulic', 'laminated', 'standard', 'real_wood',
    5, 'above_average', 'sample'
);

-- ============================================================
-- W212 E-CLASS ERA — MIXED QUALITY (2010s)
-- ============================================================

-- E-Class W212 pre-facelift (2010-2013) car_id=47 reliability=67.2
-- Early W212, some cost-cutting remnants from DaimlerChrysler era.
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
    47, 65.2,
    70, 68, 65,
    68, 58, 60,
    'W212 improved over W211 with high-strength steel and aluminum hood/fenders. But pre-facelift interiors revealed DaimlerChrysler-era cost-cutting — cheaper plastics, less consistent panel gaps. Body structure is safe and rigid but the "bank vault" feel of the W124 was gone.',
    'E-Class isolation remains a Mercedes strength — laminated glass, hydraulic engine mounts, sound-deadened firewall. At highway speed it is quiet. But road noise from run-flat tire options intrudes. Not W124 vault-like but competitive for the era.',
    'Pre-facelift W212 interior was widely criticized — hard plastics on center console and lower dash, three different grain patterns that didn''t match, an angular design language that felt cold. Real wood was available but the overall execution lacked the warmth of competitors.',
    'Mercedes paint quality recovered from the W210 rust epidemic. Multi-stage process with clear coat. Some early-build W212 examples had orange peel texture. Galvanized steel throughout. No systemic rust issues reported.',
    'Pre-facelift electronics had teething issues — COMAND system freezes, Bluetooth connectivity problems, parking sensor malfunctions. SBC brake system (early models) was a known failure point. AIRMATIC suspension on V6 models can leak. Not terrible but not Mercedes-best.',
    'Hard plastics scratch easily and show wear at contact points. Leather (where equipped) holds up adequately. Dashboard materials can develop a sheen at contact areas. Center console trim peels on early production. Post-2014 facelift materials are significantly better.',
    'E-Class W212 pre-facelift Q-score 65.2. A decent modern Mercedes but the pre-facelift interior is a visible reminder of DaimlerChrysler cost-cutting. Body structure is safe and the car is quiet, but the materials gap vs Audi A6 and BMW 5-Series of the same era was notable.',
    'shared', 'Sindelfingen (Germany)', 'spot', 4.5,
    'hydraulic', 'laminated', 'standard', 'real_wood',
    4, 'above_average', 'sample'
);

-- E-Class W212 post-facelift (2014-2016) car_id=161 reliability=71.9
-- Improved over pre-facelift with better materials and revised electronics.
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
    161, 70.1,
    74, 72, 72,
    72, 62, 66,
    'Facelift addressed many pre-facelift complaints — tighter panel gaps, improved body rigidity, revised front and rear structures. Aluminum hood and fenders retained. The 2014 refresh was more than cosmetic; structural improvements were made to crash performance.',
    'Improved NVH over pre-facelift with additional sound deadening material, better door seals, and revised engine mounts. laminated glass standard. Highway cruising is very quiet. Some 4-cylinder diesel models transmit more vibration through the drivetrain.',
    'Major interior refresh replaced the angular, cheap-feeling pre-facelift design. Softer materials on touch surfaces, better grain matching, improved switchgear feel. Real wood trim options expanded. Still not W124-tier warmth but a significant step up. The analog clock was a nice touch.',
    'Same paint process as pre-facelift with minor improvements. Mercedes paint of this era is generally good. No systemic rust issues. Some early facelift cars had paint adhesion issues on plastic bumper covers — minor but noticeable.',
    'COMAND system improved with more stable software. SBC brake system replaced with conventional brakes (major reliability improvement). AIRMATIC still present on some models but updated. Bluetooth and connectivity more reliable. Overall electrical improvement over pre-facelift.',
    'Better materials age better than pre-facelift — the softer touch surfaces resist scratching more effectively. Leather options improved. Dashboard materials don''t develop the glossy sheen as quickly. Center console trim more durable. A genuine improvement over 2010-2013 cars.',
    'E-Class W212 post-facelift Q-score 70.1. The 2014 facelift was a meaningful quality recovery — better materials, improved electronics, and tighter assembly. Still not peak Mercedes but a clear step up from the pre-facelift. The gap to Audi A6 narrowed significantly.',
    'shared', 'Sindelfingen (Germany)', 'mixed', 4.0,
    'hydraulic', 'laminated', 'standard', 'real_wood',
    4, 'above_average', 'sample'
);

-- E550 W212 facelift (2014-2016) car_id=83 reliability=55
-- Biturbo V8 adds stress and complexity to W212 platform.
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
    83, 65.7,
    72, 70, 70,
    68, 52, 58,
    'Same W212 facelift body structure but the M278 biturbo V8 adds heat stress to engine bay components and front subframe. AIRMATIC suspension standard — air springs add failure points. Body is well-built but the powertrain complexity taxes the platform.',
    'Biturbo V8 provides effortless thrust but deeper exhaust note permeates cabin at throttle application. Hydraulic engine mounts contain vibration. AIRMATIC provides excellent ride isolation when functioning. Laminated glass standard. Highway cruising refined when air suspension holds.',
    'Same improved facelift interior as other W212 models — AMG-line option adds sport seats and trim. Real wood, decent leather, improved soft-touch materials. But the E550 was positioned below AMG, so some AMG-specific interior upgrades are absent.',
    'Same Mercedes paint process as W212 facelift — good quality, no systemic issues. Twin turbo heat can cause slightly faster paint aging on hood surface over very long term. Not a practical concern in normal ownership periods.',
    'The M278 biturbo V8 is the liability — turbo wastegate rattles, timing chain guide wear, coolant pipe leaks. AIRMATIC air springs fail at 80-100K miles. COMAND system updates. The combination of V8 complexity and air suspension makes electrical/aging the weakest dimension.',
    'AIRMATIC failures leave the car undriveable — not just cosmetic. Engine bay heat accelerates rubber and plastic aging underhood. Interior materials same as facelift W212 (adequate). V8 heat soak can affect under-hood cosmetic components over time.',
    'E550 W212 Q-score 65.7. The biturbo V8 transforms the driving experience but adds significant complexity and failure risk. AIRMATIC suspension and turbo-related issues drag the electrical score to 52. Body and interior quality match the W212 facelift but the powertrain tax is real.',
    'shared', 'Sindelfingen (Germany)', 'mixed', 4.0,
    'hydraulic', 'laminated', 'standard', 'real_wood',
    4, 'above_average', 'sample'
);

-- E-Class W213 (2016-2023) car_id=31 reliability=78
-- Modern E-Class, significant quality improvement. W213 interior was widely praised.
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
    31, 75.5,
    78, 78, 80,
    75, 68, 72,
    'W213 uses aluminum-intensive body construction with laser-welded joints. Significant weight reduction despite increased dimensions. Dual-phase and ultra-high-strength steel in safety structure. Tight panel gaps. A genuine return to form for Mercedes body engineering.',
    'Acoustic laminated glass standard — a meaningful NVH upgrade over W212. Hydraulic engine mounts, extensive sound deadening in firewall and floor. Aerodynamically optimized for wind noise. The W213 is notably quieter than the W212 at highway speed.',
    'W213 interior was named one of the best in any production car — flowing dashboard design, ambient lighting with 64 colors, widescreen cockpit display, open-pore wood options, and leather-wrapped surfaces on every touch point. A leap forward from W212. Real design leadership.',
    'Modern Mercedes multi-stage paint process with ceramic clear coat option. Excellent corrosion protection. No reported systemic paint issues. Paint depth and consistency visibly better than W212. Some early-production color matching issues on bumper covers reported.',
    'MBUX infotainment system generally stable after early software updates. Electronic architecture is complex but well-integrated. Some 48V mild-hybrid system issues on early EQ Boost models. Driver assistance sensors can require recalibration. Not bad for the complexity level.',
    'Interior materials are holding up well in early long-term assessments. Ambient lighting strips durable. Leather options improved over W212. Piano black trim shows fingerprints and micro-scratches. Too new for definitive 10+ year aging data but early signs are positive.',
    'E-Class W213 Q-score 75.5. A genuine return to form for Mercedes-Benz — the W213 interior was class-leading at launch and the body engineering is modern and precise. Acoustic glass and extensive sound deadening deliver excellent NVH. Complexity keeps electrical below 70 but this is the best E-Class since W124.',
    'shared', 'Sindelfingen (Germany)', 'laser', 3.5,
    'hydraulic', 'acoustic_laminated', 'standard', 'real_wood',
    5, 'extensive', 'sample'
);

-- E 450 4MATIC W213 (2020-2023) car_id=149 reliability=72
-- Same W213 platform, more complexity from AWD and turbo inline-6.
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
    149, 73.9,
    77, 76, 80,
    75, 62, 70,
    'Same W213 aluminum-intensive body with 4MATIC hardware packaged into the front subframe — minor additional stress points. AWD system adds weight but no structural compromise. Laser-welded body same as RWD W213.',
    'Same acoustic laminated glass and extensive sound deadening as RWD W213. Inline-6 turbo is smooth but slightly more mechanically audible than V6 at cold start. AWD drivetrain adds minor gear whine. Still very quiet at highway speed.',
    'Identical W213 interior — one of the best in any production car. Same flowing dashboard, ambient lighting, widescreen displays, and premium materials. The E 450 badge doesn''t change the interior execution. Leather and wood options identical.',
    'Same modern Mercedes paint process — excellent quality with no systemic issues. Same corrosion protection and clear coat quality as standard W213. AWD hardware underneath is well-protected from corrosion.',
    'EQ Boost 48V mild-hybrid system adds complexity — integrated starter-generator (ISG) can fail, 48V battery degradation, additional control modules. 4MATIC transfer case and front differential add maintenance items. More potential failure modes than RWD version.',
    'Same W213 interior materials that are aging well. Additional under-hood heat from turbo inline-6 and 48V system may accelerate rubber hose aging slightly. AWD adds no interior cosmetic impact. Piano black trim still shows fingerprints.',
    'E 450 4MATIC Q-score 73.9. Same excellent W213 platform with added 4MATIC and 48V hybrid complexity — electrical score drops to 62. Interior and body quality unchanged from the standard W213 (which is a compliment). The inline-6 is smooth but the added systems create more failure potential.',
    'shared', 'Sindelfingen (Germany)', 'laser', 3.5,
    'hydraulic', 'acoustic_laminated', 'standard', 'real_wood',
    5, 'extensive', 'sample'
);

-- ============================================================
-- C-CLASS — W204 AND W205
-- ============================================================

-- C300 W204 (2007-2014) car_id=144 reliability=62
-- Cost-cut era Mercedes. W204 had quality issues.
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
    144, 58.5,
    65, 62, 55,
    60, 52, 55,
    'W204 was the DaimlerChrysler-era C-Class — competent safety structure but noticeably cheaper than W203 predecessor in material feel. High-strength steel in key areas but standard spot welding throughout. Panel gaps inconsistent at 5-7mm. The "Mercedes quality" reputation took a hit.',
    'Adequate noise isolation but not E-Class level. Standard rubber engine mounts, no acoustic glass on base models. Some road noise intrusion on rough surfaces. The M272 V6 (early) or M274 turbo-4 (late) transmit different NVH signatures. Competitive with BMW 3-Series but not class-leading.',
    'The W204 interior is where cost-cutting was most visible — hard plastics on center console and lower surfaces, a slab-like dashboard design, and switchgear that felt one tier below the E-Class. Real wood was optional; wood-grain plastic was standard. Leather optional; MB-Tex standard.',
    'Mercedes paint quality on the W204 is average — some owners report clear coat issues on horizontal surfaces at 8-12 years. Not the rust epidemic of the W210, but not W124-quality either. Some paint chipping on leading edges reported.',
    'COMAND system is the primary electrical concern — navigation screen delamination, Bluetooth module failures, frozen displays. Harmon/Kardon speaker surrounds deteriorate. Window regulator failures common. Sunroof mechanism issues. Early balance shaft gear failures on M272 V6 (engine serial below 2729..30 088914).',
    'Hard plastics scratch and show wear quickly at contact points. Leather (where equipped) wears at bolsters. MB-Tex is more durable but looks plastic. Dashboard sheen develops at driver touch points. Interior trim pieces can rattle loose at 80K+ miles.',
    'C300 W204 Q-score 58.5. The DaimlerChrysler cost-cutting era C-Class — functional but the cheapest-feeling Mercedes of the modern era. Interior materials are the weakest dimension. Body is safe but lacks the solidity of W212. Electrical gremlins are common. A car you tolerate, not admire.',
    'shared', 'Bremen (Germany)', 'spot', 6.0,
    'rubber', 'standard', 'standard', 'wood_grain',
    3, 'standard', 'sample'
);

-- C300 W205 (2014-2021) car_id=145 reliability=82
-- Significant improvement over W204. Modern Mercedes quality recovery.
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
    145, 71.8,
    75, 72, 72,
    72, 68, 70,
    'W205 is aluminum-intensive with mixed laser and spot welding — a dramatic improvement over W204. Tighter panel gaps, lighter weight, more rigid structure. The C-Class finally felt like a proper Mercedes again. Some early-production models had interior rattles that were addressed in later builds.',
    'Laminated glass on higher trims, improved door seals, hydraulic engine mounts available. The W205 is noticeably quieter than W204 at speed. Some tire noise from run-flat options. The M274 turbo-4 is refined but transmits more vibration at idle than the old V6.',
    'Massive improvement over W204 — flowing dashboard design previewed the W213 E-Class interior (before the E-Class got it). Real wood trim standard on upper trims. Leather options improved. Soft-touch surfaces everywhere. Not quite E-Class level but the gap narrowed dramatically.',
    'Modern Mercedes paint quality — multi-stage process with good clear coat depth. No systemic rust issues. Paint adhesion improved over W204. Some metallic colors show more orange peel than others. Overall competitive with Audi A4.',
    'COMAND system more stable than W204 generation. Driver assistance systems added complexity but generally functional. Some early-model teething issues with Bluetooth and smartphone integration resolved via updates. Sunroof mechanism more reliable than W204. Above average for the era.',
    'Interior materials holding up better than W204 in early long-term reports. Leather options age well. Soft-touch surfaces resist scratching better. Ambient lighting strips durable. Piano black center console shows micro-scratches. A genuine improvement over the W204 at every touch point.',
    'C300 W205 Q-score 71.8. A dramatic quality recovery from the W204 — the W205 C-Class finally feels like a proper Mercedes. The interior is the highlight, previewing the W213 E-Class design language. Not E-Class tier in body engineering but competitive with the BMW 3-Series and Audi A4.',
    'shared', 'Bremen (Germany)', 'mixed', 4.5,
    'rubber', 'laminated', 'standard', 'real_wood',
    4, 'above_average', 'sample'
);

-- C 400 W205 (2015-2018) car_id=147 reliability=73
-- Same platform as C300 but more complex drivetrain.
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
    147, 70.2,
    74, 70, 72,
    72, 62, 68,
    'Same W205 aluminum-intensive body structure as C300 with minor reinforcement for the more powerful drivetrain. 4MATIC hardware adds front differential and transfer case but no structural compromise. Panel gaps and body quality identical to C300.',
    'Same laminated glass and improved seals as C300. Turbo V6 produces more exhaust note that permeates cabin under throttle. 4MATIC adds minor drivetrain whine. Slightly less isolated than C300 due to sportier character but still quiet at cruise.',
    'Identical W205 interior to C300 — same flowing dashboard, same material quality, same trim options. The C 400 badge doesn''t add unique interior elements beyond AMG-line package availability. Same real wood and leather options.',
    'Same modern Mercedes paint process as C300 — good quality, no systemic issues. Same corrosion protection. Twin-scroll turbo heat underhood is well-managed with shielding. No paint-specific concerns.',
    'Turbo V6 adds complexity over turbo-4 — more sensors, more actuators, intercooler plumbing. 4MATIC transfer case and front differential add maintenance items. 7G-Tronic transmission generally reliable but more stressed. Overall more failure points than C300.',
    'Same W205 interior materials as C300 — aging characteristics identical. Under-hood turbo V6 heat may slightly accelerate rubber component aging. No interior cosmetic difference from C300 ownership.',
    'C 400 W205 Q-score 70.2. Same excellent W205 platform as C300 with turbo V6 and 4MATIC complexity — electrical score drops to 62. Interior and body quality unchanged. The additional power is nice but the complexity tax is reflected in the reliability and electrical scores.',
    'shared', 'Bremen (Germany)', 'mixed', 4.5,
    'rubber', 'laminated', 'standard', 'real_wood',
    4, 'above_average', 'sample'
);

-- C 450 AMG W205 (2016-2018) car_id=148 reliability=78
-- AMG Sport line, better components and AMG-enhanced assembly.
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
    148, 72.2,
    76, 68, 75,
    74, 65, 70,
    'W205 body with AMG-specific front subframe and suspension components. AMG Sport line received additional bracing and different suspension tuning. Slightly tighter assembly attention at Bremen for AMG-badged models. Same aluminum-intensive body structure.',
    'Sportier tuning means more exhaust note by design — AMG Sport exhaust is audible under throttle. Hydraulic engine mounts standard. Same laminated glass. Sport suspension transmits more road detail. Some tire roar from wider staggered fitment. A sporting compromise by intent.',
    'AMG Sport interior upgrades: sport seats with enhanced bolsters, AMG-specific steering wheel with flat bottom, DINAMICA suede inserts, aluminum shift paddles, AMG-specific gauges. Real carbon fiber or aluminum trim options. A noticeable step up from C 400 interior.',
    'Same Mercedes paint process with AMG-specific color options. Designo paint options available with enhanced depth. No quality-specific differences from standard W205 paint — good quality throughout.',
    'AMG-tuned M276 turbo V6 with 4MATIC — more robust than C 400 powertrain but still complex. AMG SpeedShift transmission has more aggressive shift programming. Sport differential adds a maintenance item. Driver mode electronics add complexity but AMG-tested reliability.',
    'AMG Sport seats hold up well — DINAMICA inserts resist wear better than leather alone. Flat-bottom steering wheel leather wears at 9-and-3. Same W205 dashboard materials. AMG-specific trim (carbon fiber, aluminum) more durable than wood-grain plastic. Better overall than C 400.',
    'C 450 AMG Q-score 72.2. AMG Sport enhancements elevate the W205 C-Class — better seats, better trim, AMG-tuned powertrain. The sportier character sacrifices some NVH for driving engagement. Electrical score slightly better than C 400 due to AMG-tested components. The sweet spot in the W205 C-Class lineup.',
    'shared', 'Bremen (Germany)', 'mixed', 4.0,
    'hydraulic', 'laminated', 'standard', 'real_wood',
    4, 'above_average', 'sample'
);

-- ============================================================
-- SUV / CROSSOVER
-- ============================================================

-- GLK350 X204 (2008-2015) car_id=146 reliability=65
-- Truck-ish Mercedes, adequate but not sedan-tier build quality.
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
    146, 59.2,
    65, 58, 58,
    60, 55, 55,
    'W204 C-Class platform adapted for SUV duty — boxed sections for rigidity but the engineering budget went to the C-Class sedan first. High ride height and boxy shape create aerodynamic noise. Panel gaps at 5-6mm — W204-era quality, which is to say adequate.',
    'SUV form factor works against NVH — boxy shape creates wind noise at A-pillars and mirrors. No acoustic glass. Engine bay isolation below sedan standards. Tire noise from larger SUV rubber. The M272/M274 engines are smooth but the packaging lets noise in.',
    'Direct carryover from W204 C-Class interior — same hard plastics, same angular dashboard design, same cost-cutting DaimlerChrysler era materials. SUV-specific: higher seating position and different center console but same mediocre material quality. Wood-grain plastic trim standard.',
    'Same W204-era Mercedes paint — adequate with some clear coat aging on horizontal surfaces. SUV exposure to more stone chips and road debris. Rear hatch paint more prone to chipping. Not terrible but not memorable.',
    'Same W204-era electrical concerns — COMAND system issues, Bluetooth module failures. Add SUV-specific: 4MATIC transfer case, power liftgate mechanism (failure-prone), panoramic sunroof mechanism. More things to break than the C-Class sedan.',
    'Same W204-era interior materials that age poorly — hard plastics scratch, MB-Tex holds up, leather (if equipped) wears at bolsters. SUV use patterns are harder on interiors — cargo area scratches, rear seat abuse. Power liftgate struts fail at 8-10 years.',
    'GLK350 Q-score 59.2. A W204 C-Class in SUV clothing — all the DaimlerChrysler-era cost-cutting with added SUV complexity. The boxy design is distinctive but aerodynamically noisy. Interior quality is the weak point. Reliable enough mechanically but feels cheaper than a Mercedes should.',
    'shared', 'Bremen (Germany)', 'spot', 5.5,
    'rubber', 'standard', 'standard', 'wood_grain',
    3, 'standard', 'sample'
);

-- ============================================================
-- SL ROADSTERS — MODERN ERA
-- ============================================================

-- SL55 AMG R230 (2002-2008) car_id=141 reliability=55
-- Kompressor V8, complex, ABC suspension issues. The problem child of SLs.
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
    141, 54.9,
    68, 60, 58,
    55, 35, 45,
    'R230 SL platform with AMG-enhanced structure — front subframe reinforcement for the M113K kompressor V8. Aluminum body panels over steel passenger cell. Not the R129''s overbuilt feel. Some early R230 cars had quality issues from the DaimlerChrysler efficiency programs.',
    'ABC (Active Body Control) hydraulic suspension provides remarkable flat cornering but the pump and accumulators create a constant low-frequency hydraulic hum. Kompressor V8 supercharger whine is audible. Vario roof (folding hardtop) seals degrade and whistle. Better with roof closed.',
    'Early 2000s Mercedes interior — adequate materials but some cost-cutting visible in switchgear feel and plastic quality. AMG-specific: sport seats, AMG steering wheel, carbon fiber or wood trim options. Real design was angular and blocky. Not as premium as the price suggested.',
    'Mercedes paint quality of this era is average — some clear coat issues reported, particularly on horizontal surfaces and the folding roof panels. Vario roof mechanical attachment points can chip. Not W124-tier paint.',
    'ABC suspension is the Achilles heel — hydraulic accumulators fail ($$$), ABC pump leaks, ABC lines corrode. SBC electronic braking system (2003-2006) is a known failure risk requiring pump replacement. Kompressor bearings wear. Vario roof hydraulic cylinders leak. Active Body Control is Active Bank Account Cleaner.',
    'ABC fluid leaks stain and damage underbody components. Vario roof mechanism aging — hydraulic cylinders leak, seals harden, alignment drifts. Dashboard materials of this era can develop sticky residue in hot climates. AMG seat bolsters wear. Folding roof panel gaps increase over time.',
    'SL55 AMG R230 Q-score 54.9. The car that defined the "expensive to maintain AMG" stereotype. The M113K kompressor V8 is bombproof but everything around it is fragile — ABC suspension, SBC brakes, Vario roof hydraulics. Body and interior are merely adequate for the era. Buy one for the engine, budget for the rest.',
    'bespoke', 'Sindelfingen (Germany)', 'spot', 5.0,
    'hydraulic', 'laminated', 'standard', 'real_wood',
    4, 'above_average', 'sample'
);

-- SL63 AMG R231 (2013-2020) car_id=142 reliability=62
-- Biturbo V8, good modern AMG build. Much improved over R230.
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
    142, 69.2,
    78, 72, 72,
    70, 55, 62,
    'R231 is all-aluminum body shell — a significant improvement over R230. Lighter, stiffer, better-balanced. AMG-specific front subframe for M157 biturbo V8. Mixed laser and spot welding. Panel gaps improved to 4-5mm. The R231 feels like a proper modern Mercedes.',
    'Vario roof (folding hardtop) is better sealed than R230. Laminated glass when roof is up. Hydraulic engine mounts. The M157 biturbo V8 has deeper exhaust note but more refined than kompressor whine. Some roadster cowl shake on rough surfaces. Much improved over R230.',
    'Modern Mercedes interior with AMG-specific upgrades — sport seats, AMG steering wheel, carbon fiber or piano black trim. Materials improved over R230 with softer surfaces and better switchgear. But the interior design is functional rather than stunning — the W213 E-Class interior it shares architecture with is more impressive.',
    'Modern Mercedes multi-stage paint process. Good clear coat depth. No systemic rust issues (aluminum body helps). Vario roof panels paint-matched and generally holding up well. Some stone chip vulnerability on front fascia typical of low-slung roadsters.',
    'ABC suspension eliminated on most R231 models (replaced with conventional steel springs or AIRMATIC). That removes the biggest R230 failure mode. But: M157 biturbo wastegate rattles, intercooler pump failures, COMAND system updates needed. Vario roof hydraulic cylinders still leak at 8-10 years. Better than R230 but still complex.',
    'Vario roof aging is the primary cosmetic concern — hydraulic cylinders leak, seals harden, alignment drifts causing wind noise. Interior materials age reasonably well — AMG seats durable, carbon fiber trim doesn''t delaminate. Paint on folding roof panels shows wear at hinge points over time.',
    'SL63 AMG R231 Q-score 69.2. A massive improvement over the R230 — aluminum body eliminates rust, ABC suspension gone from most models, modern AMG build quality. The M157 is powerful but wastegate rattles are known. Vario roof hydraulics remain the long-term maintenance item. Best modern SL before the R232.',
    'bespoke', 'Bremen (Germany)', 'mixed', 4.5,
    'hydraulic', 'laminated', 'standard', 'real_wood',
    4, 'above_average', 'sample'
);

-- SL 63 R232 (2022+) car_id=143 reliability=70
-- Newest AMG SL platform. Best AMG build quality. AMG-specific architecture.
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
    143, 77.0,
    82, 78, 80,
    78, 68, 72,
    'R232 is the first SL developed entirely by AMG — not a shared platform adapted by AMG. Active aerodynamics with retractable rear spoiler integrated into the trunk lid. Aluminum-intensive body with carbon fiber structural elements. Laser-welded primary joints. Panel gaps at 3-4mm.',
    'Acoustic laminated glass standard. Active engine mounts that adjust damping based on drive mode. Extensive sound deadening in bulkhead and floor. Fabric soft top (not folding hardtop) saves weight and improves packaging. Very quiet with top up for a roadster.',
    'Hyper-analog dashboard with standalone instrument cluster gauges — a deliberate return to classic design language. Nappa leather standard, semi-aniline available. AMG Performance seats with heating/ventilation/massage. Real aluminum and carbon fiber trim. The best SL interior in decades.',
    'Modern AMG paint processes with MANUFAKTUR exclusive paint options. Multi-stage with ceramic clear coat. Aluminum body eliminates rust concern. Fabric top doesn''t have paint-match issues of folding hardtops. Paint quality is at Mercedes-AMG highest standards.',
    'M177 hand-built AMG engine — one man, one engine philosophy. MBUX infotainment is modern but complex. Active aerodynamics actuators are a new failure mode. Fabric top mechanism simpler than Vario roof. Too new for definitive long-term data but the architecture is cleaner than R231.',
    'Too new for meaningful long-term aging data — extrapolating from material quality and modern AMG standards. Semi-aniline leather will patina but not crack. Fabric top should be more durable than folding hardtop seals. Active aerodynamics components are unproven long-term. Materials quality suggests good aging.',
    'SL 63 R232 Q-score 77.0. The first AMG-developed SL from the ground up — and it shows. Body construction, NVH, and interior materials are all at or near the top of the Mercedes-AMG range. Deductions for new-platform uncertainty (electrical 68, cosmetic 72). The fabric soft top is a regression some will welcome and others won''t.',
    'bespoke', 'Bremen AMG (Germany)', 'laser', 3.5,
    'active', 'acoustic_laminated', 'semi_aniline', 'real_wood',
    5, 'extensive', 'sample'
);

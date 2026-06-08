-- BMW 540i pre-LCI G30 Build Quality Q-factor (car_id=56)
-- CLAR shared platform, B58 engine, ZF 8HP50. Good German build quality but BMW plastic cooling and electrical aging.

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
    56, 74.15,
    80, 78, 78,
    75, 62, 68,
    'CLAR (Cluster Architecture) shared platform across G30 5 Series, G01 X3, G11 7 Series. Mixed high-strength steel and aluminum construction — aluminum hood, front fenders, doors. Multi-link front and rear suspension. Good crash structure. Panel gaps 4-5mm (competitive for class but not LS-grade). BMW''s modular approach means shared weld standards across CLAR vehicles. B-pillar and roof rail use hot-stamped ultra-high-strength steel. Body rigidity good but not bespoke-level — shared platforms always trade some stiffness for commonality.',
    'Good NVH for the segment. Hydraulic engine mounts standard on 540i (not on 520i/530i). Acoustic laminated windshield standard, acoustic side glass available on higher trims. Firewall insulation above average. B58 inherently smooth inline-6. ZF 8HP50 well-isolated. Underbody aero panels reduce wind noise. However: run-flat tires transmit road harshness noticeably (common complaint on Bimmerpost). At 80mph more refined than G35 but not LS430-quiet. Road noise on coarse surfaces above average for class.',
    'Dakota leather standard (BMW mid-grade, below Nappa). Sensatec (synthetic) on base models. Optional Nappa leather on M Sport. Real aluminum trim standard; optional wood trim is genuine open-pore oak or fineline ridge. iDrive 6.0 system (pre-LCI rotary controller) — functional but dated compared to LCI. Soft-touch surfaces on doors and dash. Stitching quality good. Fit and finish above average but not at Audi C8 level. Piano black trim scratches easily. Cup holder materials feel thin.',
    'BMW paint quality is generally good. Multi-stage cathodic dip primer, base coat, clear coat process. Panel gaps consistent. No known epidemic clear coat failures on G30. However: some owners report orange peel on horizontal surfaces (hood, roof). Aluminum panels don''t rust, but steel structural components can if paint compromised. Stone chips on front end expose aluminum which doesn''t rust but can corrode cosmetically. Paint softness is average — not Honda-soft but not ceramic-hard.',
    'BMW electrical aging is the weak point. iDrive CCC/CIC/NBT units can develop screen delamination (purple/white spots). Battery registration required — wrong battery coding causes electrical gremlins. Plastic cooling system components (expansion tank, thermostat housing, radiator end tanks) become brittle at 80-100K miles — not technically electrical but electronic thermostat failures trigger limp mode. Water pump (electric, not mechanical) fails without warning. Door lock actuators fail. K-CAN bus issues cause intermittent warning lights. B58 is better than N-series engines but plastic still plastic.',
    'Dakota leather wears reasonably — develops patina at 80-100K miles rather than cracking. Steering wheel leather can get shiny/glossy at 60K+. Dashboard material holds up well (no G35-style cracking). Piano black center console scratches from keys, rings, seatbelt buckles — looks tired at 5 years. Door armrest leather creases. Optional wood trim ages better than aluminum (which can pit). Overall: ages like a well-maintained German car — functional but showing at 10 years.',
    'BMW 540i G30 pre-LCI Q-score 74.15. CLAR shared platform with good construction but BMW-typical aging: plastic cooling components, electrical quirks, and cosmetic wear on trim pieces. The B58 is a significant improvement over N-series engines. Strong body rigidity and good NVH for class, but not bespoke luxury-level in any dimension. Scores above ES350 on body construction (aluminum panels, CLAR engineering) but below on electrical reliability and cosmetic aging.',
    'shared', 'Dingolfing (Germany)', 'mixed', 4.5,
    'hydraulic', 'acoustic_laminated', 'standard', 'real_wood',
    4, 'above_average', 'sample'
);

-- BMW 540i LCI G30 Build Quality Q-factor (car_id=150)
-- B58TU engine improvements, iDrive 7, facelift refinement. Better sorted than pre-LCI.

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
    150, 77.2,
    82, 80, 80,
    78, 68, 72,
    'Same CLAR platform as pre-LCI but production maturity improvements. 2021+ models benefit from 4 years of production refinements — panel fit tighter, weld consistency improved. Mixed high-strength steel and aluminum unchanged. B58TU (technical update) engine has improved crankshaft, forged connecting rods (some sources), and better oil pump. Body construction identical architecture but better executed. Panel gaps 4-4.5mm on later builds (measured improvements on Bimmerpost owner surveys). G80 M3/M4 share this platform — performance validation at higher loads.',
    'Improvements over pre-LCI: revised acoustic glass standard on more trims. Improved door seal design reduces wind noise at highway speeds. B58TU smoother idle and better NVH calibration from factory. M Sport suspension option has adaptive dampers with better isolation in Comfort mode. Same hydraulic engine mounts (confirmed standard across all 540i LCI). Run-flat tire harshness still present but BMW updated tire specs to softer compounds. Cabin quietness at 80mph improved approximately 1-2dB per owner comparisons.',
    'Vernasca leather replaces Dakota on LCI — noticeably softer, better grain, closer to Nappa quality. Sensatec remains base option. iDrive 7.0 with larger curved display (on iDrive 8 cars), or updated 10.25-inch screen. Improved trim materials: less piano black, more brushed metal and open-pore wood options. Optional Bowers and Wilkins audio (excellent). Cognac Vernasca leather particularly well-regarded. Stitching patterns more elaborate on M Sport. Overall interior step up from pre-LCI.',
    'Same BMW paint process as pre-LCI. Minor improvements in clear coat formulation reportedly. No systemic paint issues reported on LCI cars (too new for long-term data but early signs positive). Individual and BMW Exclusive paint options have more clear coat depth. Standard colors are consistent. Same aluminum panel considerations — no rust but cosmetic corrosion risk on chips.',
    'B58TU addresses many B58 issues: improved water pump design, better thermostat reliability, updated PCV valve (less prone to failure). iDrive 7 more stable than iDrive 6 (fewer crashes, faster response). However: complex mild-hybrid 48V system introduced on some 2022+ models adds failure points. Digital Key and OTA updates add software complexity. G20 B48 owners report similar electrical improvements — BMW learning from N-series era. Still too early for definitive long-term data but trajectory positive.',
    'Vernasca leather should age better than Dakota — initial reports positive at 30-50K miles. Interior materials generally higher quality than pre-LCI. Less piano black means fewer visible scratches. Updated door card materials more durable. Still has the BMW steering wheel wear pattern (glossy at 60K+). Dashboard materials unchanged — should hold up. Overall LCI cosmetic trajectory is improved. Too new for 10-year data but 3-year lease returns look much better than pre-LCI equivalents.',
    'BMW 540i LCI G30 Q-score 77.2. The LCI fixes many pre-LCI issues: better leather (Vernasca), improved B58TU reliability, tighter panel gaps, better NVH calibration. Scores higher across every dimension. The sweet spot G30 — early models had B58 growing pains, LCI has them sorted. Still a shared platform with BMW-typical plastic aging, but significantly better executed.',
    'shared', 'Dingolfing (Germany)', 'mixed', 4.0,
    'hydraulic', 'acoustic_laminated', 'standard', 'real_wood',
    4, 'above_average', 'sample'
);

-- BMW M3 E46 Build Quality Q-factor (car_id=3)
-- Legendary driver's car, 20+ years old now. Subframe cracking, VANOS issues, era-appropriate quality.

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
    3, 53.25,
    70, 45, 55,
    48, 45, 42,
    'E46 platform — genuinely good chassis engineering for era. 50:50 weight distribution. MacPherson strut front, multi-link rear. High-quality steel for period. BUT: rear subframe mounting points crack on coupe and convertible (TSB SI B31 01 03, well-documented on M3Forum). Subframe reinforcement plates are the standard fix ($2000-4000). Rear differential mount bolts shear. Front strut tower mounts fatigue. Now 20+ years old — even well-maintained examples show fatigue. Rust on rear quarter panels, jack points, and underbody common in northern cars. Panel gaps 5-6mm (good for 2000s, not great now).',
    'Era-appropriate NVH — acceptable in 2000, notable by modern standards. No acoustic glass. Solid rubber engine mounts (M3 specific, stiffer than 330i). No hydraulic suspension options. S54 engine is mechanically noisy (valvetrain, injectors) — charming but not refined. Road noise significant with OEM 18/19-inch staggered setup. Exhaust present in cabin at all speeds (intentional M-car character). No active noise cancellation. Minimal sound deadening in pursuit of weight savings. Wind noise around mirrors and A-pillar at speed. At 80mph you hear everything.',
    'Good for year but poor by modern standards. Sport seats well-bolstered but leather quality is mid-grade (not Nappa). Leatherette on non-CSL base models. SMG cars have leather-wrapped shift knob that wears. Door panels use a mix of soft-touch and hard plastic — hard plastic scratches, soft-touch degrades sticky. Carbon fiber trim (real on some models) holds up; aluminum trim scratches. Orange peel texture on some interior plastics. Headliner sag at 15+ years common. Center console armrest vinyl cracks. Steering wheel leather thin — shiny at 50K.',
    'BMW paint quality in 2000-2006 was average. Clear coat failure on horizontal surfaces common at 15+ years — hood, roof, trunk lid. Carbon black and jet black particularly susceptible. Alpine White holds up better. Stone chips on front end expose steel which rusts quickly. Rear quarter panel rust near wheel arch is nearly universal on northern cars. Underbody surface rust common even on southern cars. Paint correction community has documented E46 paint extensively — clear coat is thin (~100 microns vs modern 120-140).',
    'E46 M3 electrical is era-appropriate but aging poorly now. S54 VANOS solenoids fail ($1500-2500 per hub, two hubs). VANOS hub bolts back out and drop into timing chain — catastrophic if not caught. CPS (camshaft position sensors) fail regularly. SMG pump relay fails (strands you in neutral). SMG actuator seals leak. Window regulators fail (cable mechanism design flaw — replaced under warranty, aftermarket fixes exist). Instrument cluster pixels fail on temperature display (common E46 issue). HK audio amplifier fails. Battery discharge from parasitic draw common.',
    'E46 M3 at 20+ years shows its age cosmetically regardless of maintenance. Leather cracks on bolsters at 60-80K miles. Steering wheel glossy at 50K. Dashboard doesn''t crack (better than G35 era Nissan) but fades. Door panel armrest leather wears through. Headliner sags. Exterior trim fades — kidney grilles, window trim, bumper trim all go chalky. Weatherstripping shrinks and cracks causing wind noise and water leaks. Rubber suspension bushings degrade causing clunking. Subframe bushings crack. Every rubber component is 20+ years old. Well-maintained examples can look good but require constant attention.',
    'E46 M3 Q-score 53.25. A legendary driving machine with genuine chassis engineering quality, but 20+ years of aging is unforgiving. Subframe cracking is the structural Achilles heel. S54 VANOS and SMG are the mechanical weak points. Interior and paint are era-appropriate but poor by current standards. Scores above G35 on body construction (better engineering intent) but below on electrical aging (more complex systems aging poorly). The E46 M3 rewards investment but never stops needing it.',
    'derived', 'Regensburg (Germany)', 'spot', 5.5,
    'rubber', 'standard', 'standard', 'carbon_fiber',
    4, 'standard', 'sample'
);

-- Audi A6 C7 3.0T Build Quality Q-factor (car_id=155)
-- MLB platform, supercharged 3.0T V6. Audi interior quality benchmark for era.

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
    155, 72.75,
    78, 76, 82,
    72, 58, 65,
    'MLB (Modularer Längsbaukasten) shared platform — longitudinal engine layout shared with A4 B8, Q5, Q7. Aluminum-intensive body: aluminum hood, fenders, doors, trunk, and structural components. Steel-aluminum hybrid construction with Audi Space Frame (ASF) technology partial application. Multi-link front and rear suspension (5-link front, trapezoidal-link rear). Panel gaps 4-5mm (Audi benchmark for class). Hot-stamped steel in B-pillars and roof rails. Aluminum bolted to steel at junction points — potential galvanic corrosion risk in salty climates if seams compromised. Good torsional rigidity for class.',
    'Audi NVH is a strength of the brand. Hydraulic engine mounts on 3.0T (not on 2.0T base). Acoustic laminated windshield standard, acoustic side glass on Prestige trim. Excellent firewall insulation. Supercharged 3.0T inherently smooth and quiet. 8-speed ZF torque converter well-isolated. MMI system doesn''t add mechanical noise. Underbody panels for aero and sound. However: some supercharger whine reported on early EA837 engines (considered charming by some, annoying by others). Tire noise with 19/20-inch wheels can be intrusive. Road noise on coarse surfaces moderate.',
    'Audi interiors are the class benchmark for this era. Valcona leather standard on 3.0T Premium Plus (genuine, above BMW Dakota grade). Milano leather on Prestige. Real aluminum trim inlays (brushed, not plastic). Optional wood trims are genuine. Soft-touch surfaces everywhere — doors, dash, console. MMI controls feel substantial. Gauge cluster (Virtual Cockpit on 2016+ facelift) high quality. Stitching precise. Fit and finish above BMW F10/G30 of same vintage. Center console layout clean. Only weakness: piano black trim around shifter scratches easily.',
    'Audi paint quality is solid. Multi-stage process with cathodic e-coating. Clear coat holds up well — no epidemic failures reported on C7. Aluminum body panels don''t rust. Steel substructure can rust if paint compromised but galvanizing is thorough. Some reports of clear coat micro-blistering on dark colors (Phantom Black, Moonlight Blue) at 8-10 years. Paint thickness above average (~130 microns). Stone chips on aluminum front end don''t rust but show. Overall: Audi paint quality is top-tier for mainstream luxury.',
    'Audi electrical aging is the weak point. MMI system failures are common — screen goes blank, control module fails ($1500-3000). MMI joystick/touchpad delaminates. Oil level sensor failures trigger false warnings. 3.0T has PCV valve failures (causes rough idle, check engine). Thermostat housing leaks (plastic, cracks at 70-90K). Water pump/thermostat assembly fails. Transmission mechatronic unit can fail (ZF 8HP related). Parking sensors fail individually. LED headlights (2014+ facelift) can develop moisture. Complex electrical systems = more failure points.',
    'Audi interiors age well cosmetically — the brand strength. Valcona leather wears gracefully, developing patina rather than cracking at 100K+. Steering wheel leather shows wear at 80K+. Dashboard materials hold up without cracking or fading. Soft-touch door materials can become slightly tacky at 10+ years in hot climates. Piano black trim scratches (consistent complaint). Aluminum trim holds up well. Headliner generally stays in place. Overall: best-in-class cosmetic aging among German luxury cars of this era.',
    'Audi A6 C7 3.0T Q-score 72.75. MLB shared platform with aluminum-intensive body construction. Interior quality is the standout — Audi benchmark for the era. Good NVH, solid paint. Weak points: MMI failures, plastic cooling components, oil consumption on early 3.0T engines (EA837). Scores between ES350 and G30 on build quality. The interior materials score (82) exceeds BMW G30 because Audi used better leather grades and more soft-touch surfaces.',
    'shared', 'Neckarsulm (Germany)', 'mixed', 4.5,
    'hydraulic', 'acoustic_laminated', 'semi_aniline', 'real_wood',
    4, 'above_average', 'sample'
);

-- Audi A6 C8 Build Quality Q-factor (car_id=32)
-- MLB Evo platform, modern dual-screen interior. Next-gen Audi quality.

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
    32, 77.0,
    82, 80, 85,
    78, 62, 70,
    'MLB Evo (evolved MLB) — significant weight reduction (~100kg vs C7) through increased aluminum content and hot-formed steel optimization. Aluminum exterior panels (hood, fenders, doors, trunk, roof on some configs). Multi-material body with structural adhesives supplementing rivets and bolts at aluminum-steel junctions. 5-link front and rear suspension (more aluminum content than C7). Panel gaps 3.5-4mm (class-leading, matching or beating BMW G30 LCI). Rear-wheel steering available (all-wheel steering). Better torsional rigidity than C7. Good crash structure.',
    'Significant NVH improvement over C7. Hydraulic engine mounts on all 6-cylinder models. Acoustic laminated glass standard on all windows (not just windshield) on Prestige. Improved door seal design with double-lip weatherstripping. Active noise cancellation on some engine configs. 3.0T EA839 smoother than EA837 supercharger. Underbody aero panels more extensive. Cabin is whisper-quiet at 80mph — competitive with E-Class W213. Road noise well-managed even with 20-inch wheels. Wind noise around mirrors reduced from C7.',
    'Best-in-class interior for production year. Dual-screen MMI touch (upper infotainment, lower climate/control). Valcona leather standard, Milano on Prestige, Valcona/Atlas on options. Open-pore wood trims (genuine oak, walnut). Aluminum and carbon fiber options. Soft-touch surfaces everywhere including lower door panels and console sides. Stitching patterns more elaborate. MMI touch response is haptic — satisfying click feedback. Material quality above BMW G30 and Mercedes E-Class W213. Night orange ambient lighting signature. Only weakness: screen-heavy design means fingerprints and glare.',
    'Same Audi paint quality standards as C7 — excellent. Cathodic e-coating, multi-stage process. Clear coat depth good (~130-140 microns). Aluminum panels don''t rust. Galvanized steel substructure. No reported paint epidemics (too new for 10-year data but 5-year results positive). Optional Audi Exclusive paints have additional clear coat. Paint correction community reports C8 paint is marginally harder than C7 (easier to polish without burning through). Overall: continuation of Audi paint excellence.',
    'Complex electrical systems are the risk. Dual-screen MMI has more failure modes than C7 single screen. Both screens can develop dead pixels or touch responsiveness issues. OTA updates sometimes brick MMI requiring dealer visit. 48V mild hybrid system on 3.0T adds complexity (belt starter generator, additional battery). Air suspension (optional) adds sensor and compressor failure points. Matrix LED headlights complex and expensive to replace. Digital gauge cluster is reliable so far but long-term unknown. More sensors = more diagnostic complexity. EA839 engine: too new for definitive long-term reliability data but early signs better than EA837.',
    'Interior materials are higher quality than C7, should age better. Valcona leather grade holds up well (proven from C7 experience). Screens add a new aging concern — fingerprints, micro-scratches, and eventual backlight degradation. Open-pore wood trim ages well (sealed properly). Soft-touch materials slightly improved formulation over C7. Piano black still present but less surface area. Steering wheel leather will show wear at 80K+ (consistent with all Audi). Overall: best-in-class cosmetic aging trajectory, but screen-dependent interior means any electronic failure is also a cosmetic failure.',
    'Audi A6 C8 Q-score 77.0. MLB Evo with significant improvements over C7: better NVH, tighter panel gaps, lighter weight, improved materials. Interior quality is class-leading (85). Risk factors: complex dual-screen MMI, 48V mild hybrid, air suspension. EA839 engine early signs positive. Scores between BMW 540i LCI and ES350 overall. Best interior materials in this comparison set but electrical complexity drags score down.',
    'shared', 'Neckarsulm (Germany)', 'mixed', 4.0,
    'hydraulic', 'acoustic_laminated', 'semi_aniline', 'real_wood',
    4, 'above_average', 'sample'
);

-- Porsche 911 Turbo 996 Build Quality Q-factor (car_id=2)
-- First water-cooled 911 Turbo. Mezger engine (race-derived). Porsche build quality with IMS-era concerns.

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
    2, 69.9,
    85, 62, 72,
    72, 55, 60,
    '996 Turbo body construction is genuinely impressive for era. Steel monocoque with aluminum doors, hood, and front fenders. Turbo-specific wider body (60mm vs Carrera). Fixed front splitter and adjustable rear wing with structural integration. X50 Power Package adds larger intercoolers (structural implications). Mezger engine block (derived from GT1 race car) — different from standard 996 M96 engine, no IMS bearing issue. Weld quality high — Porsche Zuffenhausen production standards. Panel gaps 4-5mm (good for 1998-2005). Some reports of moisture in headlight housings (DRL/turn signal unit delaminates). Underbody cladding comprehensive.',
    '911 Turbo NVH is a mixed bag. Porsche designed it as a daily-driveable supercar but priorities are performance. Solid rubber engine mounts (not hydraulic) for drivetrain rigidity. No acoustic glass. Twin K24 turbochargers muffled by intercoolers but turbo whoosh audible. Air-cooled heritage means less sound deadening than comparable Audi. Suspension is stiffer than standard 996. Pirelli P Zero Rosso or Michelin Pilot Sport tires (18-inch) transmit road texture. Wind noise at speed from wide-body aerodynamics. However: more refined than GT3 or GT2 of same era. Cabin quiet enough for phone calls at 70mph.',
    'Porsche interior quality of this era is above average but not exceptional. Standard partial leather (seating surfaces only) — full leather was a $3000+ option. Leather grade is standard (not semi-aniline). Optional carbon fiber, aluminum, or wood trim (genuine materials). Bose audio option. fit and finish is precise German quality. However: base models had significant shared components with Boxster (cost-cutting complaint among purists). The "fried egg" headlights and shared interior with 986 Boxster were controversial. Climate control buttons feel tactile and precise. Overall: premium but not bespoke luxury.',
    'Porsche paint quality is above average. Multi-stage process at Zuffenhausen. Clear coat holds up reasonably well — no epidemic failures on 996 Turbo. Guards Red and Speed Yellow hold color well. Black and Midnight Blue can show swirl marks more readily. Stone chips on front bumper and hood (daily-driveable supercar = highway miles = chips). Aluminum panels don''t rust. Steel chassis galvanized. Some reports of clear coat micro-checking on 25-year-old examples but not universal. Front bumper cover paint is thinner and chips faster. Paint correction community considers 996 paint average hardness — workable.',
    '996 Turbo avoids the IMS bearing issue (Mezger engine uses different design — integrated ball bearing, not the problematic sealed bearing of M96). However: secondary air injection ports clog (carbon buildup, causes CEL). DME relay failure (strands car — $20 part, catastrophic failure mode). Coolant tank cracks (plastic, fails at 60-80K). Ignition switch failure (common 996 issue — causes electrical gremlins). Window regulators fail. Climate control final stage resistor fails (blower motor issues). Radiator fans fail (biological debris accumulation). Not as electrically fragile as F355 but more complex than Japanese cars of era.',
    '996 Turbo cosmetic aging is moderate. Leather seats wear well with maintenance — bolsters show at 80-100K miles. Dashboard doesn''t crack (better than G35 era). Steering wheel leather thins at 60K+. Door panel leather holds up. Carpet mats wear at driver heel (replaceable). Exterior: rubber seals shrink and harden at 20 years (door, window, trunk seals). Rear wing mechanism can develop play. Headlight lenses yellow slightly (polishable). Wheels: Turbo Twist design collects brake dust in crevices. Overall: a well-maintained 996 Turbo looks good at 20 years but requires active maintenance. Not as resilient as LS430 but better than F355.',
    'Porsche 911 Turbo 996 Q-score 69.9. The Mezger engine saves it from M96 reliability nightmares. Body construction is genuinely good (85) — Porsche engineering and Zuffenhausen assembly standards. Interior materials are premium but not bespoke (72). NVH is adequate but performance-prioritized (62). Electrical aging has known issues (DME relay, SAI ports, coolant tank) but manageable. Paint holds up. Scores above G35 across all dimensions, above E46 M3 on body construction but below on interior (E46 M3 carbon fiber trim). The 996 Turbo is the smart money in air-cooled-adjacent Porsches.',
    'bespoke', 'Zuffenhausen (Stuttgart, Germany)', 'mixed', 4.5,
    'rubber', 'standard', 'standard', 'carbon_fiber',
    4, 'standard', 'sample'
);

-- Ferrari F355 Build Quality Q-factor (car_id=5)
-- Hand-built Ferrari. Exotic materials, incredible engine, but valve guides, capillary leaks, tubular headers.

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
    5, 57.5,
    88, 35, 70,
    55, 30, 35,
    'F355 body construction is hand-built Ferrari quality — impressive and flawed simultaneously. Steel tub with aluminum body panels (hood, trunk, some fender sections). Tubular steel subframes front and rear. Panel gaps vary significantly (6-9mm) due to hand assembly — no two F355s are identical. Weld quality on visible seams is good; hidden structural welds are functional but not over-engineered. Composite bumper covers. The mid-engine layout allows short overhangs but the steel tub adds weight. Pininfarina design is aerodynamically sophisticated (active underbody, downforce-generating rear diffuser). However: the body structure was designed for beauty first, manufacturing consistency second.',
    'F355 NVH is essentially non-existent as a design priority — this is a race car for the road. Solid engine mounts bolt the F129B V8 directly to the chassis. No acoustic glass. No sound deadening material. No hydraulic suspension. The 3.5L V8 at 8500rpm is the NVH — it screams through Tubi Style headers. Interior resonance at cruise is significant. Tire noise with 18-inch wheels on 1995+ models is intrusive. Wind noise from targa (GTS) or spider top is notable. The F355 does not isolate you from the driving experience — it amplifies it. This is by design but objectively scores low on NVH isolation.',
    'Interior materials are exotic-grade but inconsistent. Connolly leather (English hide, among the finest available) on seating surfaces — gorgeous when new. Leather-wrapped dash and door panels. Real aluminum Ferrari gated shifter (iconic). Carbon fiber trim (optional, real). However: plastics used for switchgear are Fiat-sourced and feel cheap (turn signal stalks, HVAC controls, window switches shared with Fiat Coupe). Carpet quality is adequate but not exceptional. Fit and finish varies car-to-car (hand-built). The dichotomy is stark: Connolly leather next to Fiat switchgear.',
    'Ferrari paint quality of this era is mixed. Hand-sprayed at Maranello. Multiple clear coats for depth. Color vibrancy is exceptional (Rosso Corsa, Giallo Modena). However: paint thickness varies due to hand application (80-160 microns on same car). Clear coat micro-checking on 25+ year old cars, especially on horizontal surfaces. Stone chips on aluminum front end — no rust but chips are visible on the Ferrari red. Some owners report clear coat delamination on rear quarters. Paint quality is a strength when new but doesn''t age as well as German or Japanese multi-stage factory processes.',
    'F355 electrical is the single worst aspect of ownership. Valve guides fail on pre-1997 cars (Ferrari TSB, requires engine-out service — $10-15K). Tubular steel headers crack (OEM are known failure point, aftermarket headers solve it — $5-8K). Capillary coolant leak into engine bay (design flaw, seeps from thermostat housing). Motronic 2.7 ECU (pre-1996) can develop cold solder joints. Window regulators fail (Fiat-sourced). Alternator failure common. Warning lights are a permanent feature of F355 ownership — most are false positives but you can never ignore them. Every electrical component is harder to access because mid-engine.',
    'F355 cosmetic aging is harsh. Connolly leather cracks if not conditioned religiously (monthly). Dashboard leather shrinks and pulls at edges. Steering wheel leather deteriorates from hand oils. Carpet thins. Rubber seals harden and shrink (door, window, targa). Headlights yellow (polycarbonate oxidation). Clear coat ages as described above. Tubular header cracks discolor surrounding components. Engine-out service required for belt changes (every 3-5 years, $5-8K) — during which cosmetic issues are addressed but at significant cost. A 25-year-old F355 either looks like a $150K concourse car or a $30K project — no middle ground.',
    'Ferrari F355 Q-score 57.5. The most polarizing car in this set. Body construction (88) reflects genuine hand-built craftsmanship with exotic materials. Interior materials (70) combine Connolly leather with Fiat switchgear. But NVH (35), electrical (30), and cosmetic aging (35) are catastrophically low — the F355 demands constant, expensive attention. Valve guides and headers are $15-20K in known issues alone. Scores above G35 on body construction and interior materials (exotic vs mass-market) but below on electrical and cosmetic aging. The F355 is a masterpiece that costs masterwork money to maintain.',
    'bespoke', 'Maranello (Italy)', 'mixed', 7.5,
    'rubber', 'standard', 'full_aniline', 'carbon_fiber',
    5, 'minimal', 'sample'
);

-- Infiniti Q50 1st gen Build Quality Q-factor (car_id=34)
-- Nissan D-platform, VR30DDTT twin-turbo. Poor interior materials, DAS controversy, infotainment issues.

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
    34, 47.4,
    62, 55, 42,
    45, 35, 40,
    'Nissan D-platform (Front-Mid, shared with 370Z, late G37). FM platform architecture is decent for a sport sedan but Q50 execution is cost-cut. Steel body construction throughout — no aluminum panels on standard models. MacPherson strut front (regression from G37 double wishbone — cost cut). Multi-link rear carried over. Panel gaps 5-7mm (wider than German competitors). Standard Nissan spot welding. Front strut tower braces on Red Sport 400 only. Body rigidity adequate but not impressive — Q50 doesn''t feel as solid as BMW G30 or Audi A6. Rear subframe is same FM platform piece dating to 2003 V35 Skyline — old architecture.',
    'NVH is average-to-below for the luxury segment. VR30DDTT twin-turbo V6 is smooth at idle but turbo whoosh audible under load. Rubber engine mounts (not hydraulic) — vibration transmitted at cold start. No acoustic glass on base models — available on Premium trims. Sound deadening is adequate but not generous — road noise on 19-inch run-flat tires is noticeable. Wind noise around mirrors at 75+ mph. Bose ANC (active noise cancellation) on some trims helps but can''t overcome physical insulation deficit. At 80mph the Q50 lets you know you''re in a Nissan-derived platform. Better than G35 (progress) but well behind ES350 or German luxury.',
    'The Q50 interior is the weakest aspect and a significant regression from G37/G35 interior quality (itself not great). Hard plastics everywhere — center console, lower dash, door panels below beltline. "Leather" on base models is synthetic (Infiniti doesn''t call it leatherette — it''s "leather-appointed seating surfaces"). Real leather only on Premium/Sport trims — and it''s standard grade, not semi-aniline. Kacchu aluminum trim is real but scratches easily. Wood trim is wood-grain plastic on most trims. Dual-screen infotainment (upper 8-inch, lower 7-inch) is dated and laggy. The 2016+ single-screen update is better but still behind competitors. Fit and finish gaps visible — panel alignment issues on early models. Infiniti forums (Q50.org) are full of interior complaints.',
    'Nissan/Infiniti paint quality continues to be below average. Thin clear coat (~100 microns) on most colors. Stone chips penetrate to primer quickly on hood and front bumper. Black Obsidian and Graphite Shadow show defects readily. Some 2014-2016 cars have clear coat peeling on horizontal surfaces at 7-8 years (better than G35 epidemic but still worse than German/Japanese luxury competitors). White paint holds up best. Rear quarter rust is less common than G35 era (improved galvanizing) but still present on northern cars at 100K+. Paint softness means it marks easily in car washes.',
    'Q50 electrical issues are extensive and well-documented. Direct Adaptive Steering (DAS) is the headline failure — steer-by-wire system that disconnects at random, requires dealer software reset (NTB15-041). DAS backup clutch packs wear causing steering vibration. InTouch infotainment system is notoriously slow, freezes, reboots while driving. 2014-2015 models had incompatible Android OS that couldn''t run modern apps — Infiniti eventually abandoned updates. Rearview camera display delays 3-5 seconds (safety issue). Bluetooth connectivity drops. DCT automatic (not available — Q50 uses 7AT from Mercedes, sourced from A-class). Window regulators fail (carried over from G37 design). Climate control servo motors tick. Pre-collision warning false alarms.',
    'Q50 cosmetic aging is poor. Synthetic leather on base models cracks and peels at 60-80K miles (not patina — actual delamination). Real leather on higher trims is better but still standard grade — wears at bolsters. Steering wheel leather thins quickly. Hard plastics scratch from normal use (seatbelt buckle, rings, keys). Center console armrest vinyl peels. Headliner can sag at 8+ years. Dual-screen surround trim fades. Exterior: paint aging as noted. Window trim oxidizes. Q50 at 8-10 years looks its age — cheaper than a maintained BMW or Audi of same vintage. The Q50 Red Sport 400 is mechanically interesting but cosmetically disposable.',
    'Infiniti Q50 1st gen Q-score 47.4. The lowest score in this set (below G35 Coupe). FM platform is old architecture with cost-cut execution. Interior materials (42) are the weakest point — hard plastics, synthetic leather, wood-grain plastic. Electrical (35) dragged down by DAS failures and InTouch infotainment disaster. Paint quality continues Nissan tradition of below-average clear coat. VR30DDTT engine is genuinely good but surrounded by poor execution. The Q50 is a case study in how not to build a luxury sedan — the platform and engine deserved better materials and electronics.',
    'shared', 'Tochigi (Japan)', 'spot', 6.0,
    'rubber', 'standard', 'synthetic', 'plastic',
    3, 'standard', 'sample'
);

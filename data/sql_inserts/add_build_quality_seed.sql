-- LS430 Build Quality Q-factor (car_id=39)
-- Based on extensive librarian research

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
    39, 94.7,
    97, 95, 94,
    93, 82, 90,
    'LS430 bespoke F1 platform. World-first laser welding on LS400 (carried forward). Welds 1.5x stronger than industry standard. Body digitization 0.001mm (10x industry). High-tensile steel cabin cage. Double-wishbone suspension all corners. Sandwich steel bulkheads with sound-insulating resin cores.',
    'Hydraulic fluid-filled engine mounts (mini suspension for engine). Sandwich steel bulkheads. Acoustic laminated glass front+rear standard. Hollow-spoke wheels for road noise. Helmholtz resonators in door cavities. Aerodynamic underbody with flat engine cover. 58dB at 100km/h (LS400 benchmark).',
    'Semi-aniline leather (highest automotive grade). Real California walnut, antique walnut, bird''s eye maple. Optitron electroluminescent gauges. Interior tolerance 1mm. 24 woods and multiple leathers evaluated for 2 years during development.',
    'LS400/430 paint holds 20+ years. Multi-stage Toyota paint process. Corrosion-resistant galvanized steel. Wax and hemming sealers. No known clear coat epidemics. Owners report factory-fresh appearance at 15+ years.',
    'Generally excellent electrical reliability. Air suspension sensors can fail (40% of UL owners). Motorized features add complexity. No systemic electrical gremlins. Mark Levinson audio holds up well.',
    'Interior holds up remarkably at 20+ years. Semi-aniline leather ages gracefully (patina vs cracking). Real wood doesn''t delaminate. Tighter panel gaps prevent squeaks/rattles. Air suspension can sag if not maintained. Rubber components softer for NVH = degrade faster than ES.',
    'LS430 Q-score 94.7. The benchmark car for build quality. Bespoke platform, world-first engineering, highest material grades, Tahara Takumi assembly. Deductions: air suspension aging (-3 electrical), softer rubber aging (-5 cosmetic), motorized features add failure points.',
    'bespoke', 'Tahara (Aichi, Japan)', 'laser', 3.5,
    'hydraulic', 'acoustic_laminated', 'semi_aniline', 'real_wood',
    5, 'extensive', 'sample'
);

-- ES 350 Build Quality Q-factor (car_id=86)
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
    86, 76.3,
    72, 80, 76,
    78, 85, 82,
    'Camry K-platform derivative. MacPherson strut front (not double wishbone). Pressed steel subframes (not aluminum). Standard Toyota spot welding. Panel gaps 5-7mm (good but not LS-grade 3-4mm). Shared platform = shared tooling.',
    'Enhanced over Camry: additional sound deadening in floor pan, firewall, doors. 2GR-FE inherently smooth. Standard rubber engine mounts (not hydraulic). No acoustic laminated glass on base models. No sandwich steel bulkheads. Whisper-quiet but through insulation quantity, not engineering sophistication.',
    'Standard leather (not semi-aniline). Real wood on some trims, wood-grain plastic on lower trims. Standard backlit gauges (not Optitron). Good soft-touch surfaces. Panel fit tighter than G35 but not LS-level. Interior tolerance standard 3-5mm.',
    'Toyota paint of this era is average-to-good. No clear coat epidemics. Rust uncommon unless accident-damaged. Good galvanized steel. Some minor clear coat aging on horizontal surfaces at 15+ years but gradual.',
    'Stone-cold reliable electrically. Everything works at 150K+ miles. Mark Levinson optional system holds up. No systemic gremlins. 2007-2008 had floor mat recall. GPS dated but functional.',
    'Ages gracefully like a well-maintained Camry. 2007-2008 dash melting was addressed by Lexus warranty program ZLD (free replacement). 2010+ models avoided it. Leather holds up at 100K+. Softer plastics scratch more than LS. Faux wood can fade.',
    'ES 350 Q-score 76.3. Honest Camry-based luxury: mechanically bulletproof, cosmetically good but shared-platform DNA shows. 80-90% of LS NVH at 70% of the materials cost.',
    'shared', 'Multiple (Kyushu, Tsutsumi)', 'spot', 5.5,
    'rubber', 'laminated', 'standard', 'real_wood',
    4, 'above_average', 'sample'
);

-- G35 Coupe Build Quality Q-factor (car_id=64)
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
    64, 48.5,
    72, 42, 48,
    38, 35, 40,
    'FM platform (350Z-based) — genuinely good sports car architecture. 52:48 weight distribution. Double wishbone front. But: pressed steel everywhere, standard Nissan spot welding, no structural innovations. Body construction is the one bright spot.',
    'Minimal by design. No hydraulic mounts. No acoustic glass. No sound deadening beyond minimum. Exhaust note prominent (intentional). Tire roar significant with wider tires. Coupe body creates resonance. At 80mph it feels like 80mph.',
    'The single most criticized aspect of long-term ownership. Endemic dashboard cracking (soft sticky mess in warm climates, Infiniti never recalled). Seat bolster foam collapses at 40-60K miles (TSB ITB07-006). Aluminum-look trim peels at 4-6K miles. Rosewood trim is wood-grain overlay on plastic. Leather is mediocre.',
    'Clear coat failure is epidemic. Facebook group Infiniti Paint Problems has ~1000 members. Hood, roof, trunk blister and flake. Rear quarter rust on wheel arches almost universal at 100K+. Paint thin and soft. Some 2003-2005 batches had defective clear coat per body shop reports.',
    'Bose head unit failure is nearly universal on 2003-2006. Internal amp circuit board cold solder joints = no sound. When radio dies, AC controls can stop working (integrated). Parasitic battery drain from faulty circuit. Window motor failures common.',
    'Dashboard cracks at 8-12 years. Seat bolster tears at 40-60K. Clear coat peels at 7-10 years. Interior trim detaches at 5-8 years. Steering wheel wear at 60-80K. Headliner pulls near sunroof. The G35 ages like an athlete — stays capable but everything shows.',
    'G35 Coupe Q-score 48.5. The driving experience is genuinely good (FM platform, VQ35DE, RWD, manual) but the construction quality is objectively poor. Nissan spent money on chassis engineering and cut corners on everything else. At $5K used it is what it is.',
    'shared', 'Multiple (Japan)', 'spot', 6.0,
    'rubber', 'standard', 'standard', 'plastic',
    3, 'minimal', 'sample'
);

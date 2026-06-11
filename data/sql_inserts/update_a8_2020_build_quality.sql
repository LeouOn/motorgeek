UPDATE build_quality SET
  q_score = 86.8,
  score_body_construction = 92.0,
  score_nvh_isolation = 91.0,
  score_interior_materials = 91.0,
  score_paint_corrosion = 88.0,
  score_electrical_aging = 73.0,
  score_cosmetic_aging = 82.0,
  body_construction_notes = 'Same ASF aluminum space frame as pre-facelift D5. +18mm length (5190mm), improved Cd 0.26 from 0.27. Self-piercing rivet + structural adhesive + laser weld construction unchanged',
  nvh_isolation_notes = 'Improved MHEV coasting refinement and better aero contribute to marginally lower NVH. Same excellent acoustic laminated glass all-around. Sound deadening rated excellent',
  interior_materials_notes = 'Same Valcona leather, real wood/aluminum trim. New Matrix LED reading lights in rear. S line exterior package now available. Minor trim updates only - materials quality identical to pre-facelift',
  paint_corrosion_notes = 'Same 7-stage Audi paint process. 5 new matte paint options added (Daytona gray, florette silver, district green, glacier white). Proven corrosion resistance unchanged',
  electrical_aging_notes = 'MIB3 (Qualcomm) replaces MIB2 (Nvidia) - faster, more stable platform. Digital Matrix LED headlights with 1.3M micromirrors are new tech with limited long-term aging data. Digital OLED rear lights standard - unproven beyond 5 years. 48V MHEV system unchanged from 2018',
  cosmetic_aging_notes = 'Same premium materials throughout. New wheel designs 18-21 inch. Same proven interior aging characteristics as pre-facelift',
  q_score_notes = 'Marginal improvement over 2018 (86.7 vs 86.8). NVH slightly better from MHEV refinement. Core build quality identical - facelift is cosmetic/infotainment refresh, not structural change. +40kg from larger fuel tank and new tech hardware'
WHERE car_id = 43;

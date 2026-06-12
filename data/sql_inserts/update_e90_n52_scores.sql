UPDATE reliability SET
  reliability_score = 78.0,
  score_engine = 78.0,
  score_transmission = 85.0,
  score_chassis = 80.0,
  score_electronics = 68.0,
  score_ease_of_repair = 75.0,
  common_failures = json('[{"valve_cover_gasket":"moderate","water_pump":"moderate","oil_filter_housing":"moderate","disa_valve":"low","window_regulators":"moderate","vanos_solenoid":"low"}]'),
  known_issues = json('[{"n52_valve_cover":"Oil weep from valve cover gasket at 60-120K miles. Early magnesium covers (pre-2007) more durable; post-2007 plastic covers crack. -600 shop, ~ DIY","electric_water_pump":"Fails WITHOUT WARNING at 60-100K miles. No serpentine belt drive, so no gradual leak. Sudden overheating triggers limp mode. Replace preventively at 80-100K with thermostat (labor overlaps). -800 total","oil_filter_housing_gasket":"OFHG leak at 60-120K. Rubber hardens and shrinks. CRITICAL: leaking oil on serpentine belt can cause belt to slip off and get sucked into crank seal, destroying engine. Do not ignore. -700 shop, ~ DIY","disa_valve":"Intake manifold flap actuator failure at 80-120K. Rough idle, CEL, loss of low-end torque. -400 per valve. N52B30U1 (detuned 328i) had single-stage or no DISA","hydraulic_lifter_tick":"Pre-November 2008 N52 engines prone to cold-start ticking due to early cylinder head lubrication design. Post-Nov 2008 engines resolved with improved lifters and roller drag levers","window_regulators":"E90 chassis-wide issue, not N52-specific. Cable mechanism fails, window slides down into door. Rear windows more common. -400 per window","vanos_solenoid":"Dirty oil clogs solenoid screens. Less common on N52 than M54. Clean oil changes prevent this. Cleaning often resolves, replacement -600","timing_chain":"Uses chain not belt. Generally robust unlike N20. Guide rails can break at 120K+ miles. Preventive replacement around 150K miles. -3000 if needed","subframe_cracking":"E46 had this issue. E90 chassis largely resolved it. No significant subframe cracking on E90 328i","oil_consumption":"Up to 1qt per 1000-1500 miles is within BMW normal spec (absurd but true). Well-maintained N52s typically 0.5-1qt per 3000-5000 miles"]'),
  score_notes = json('[{"engine":"N52 is one of BMW most reliable engines. Wards 10 Best 2006-2007. Magnesium/aluminum composite block was groundbreaking. Known issues (VCG, EWP, OFHG) are predictable, well-documented, and manageable. M54 predecessor is simpler but N52 is more refined. The failure modes help the appreciation thesis: less and less of them available","transmission":"ZF 6-speed manual is excellent. One of the best manual transmissions BMW ever made. GM 6-speed auto (2007-2008) is also reliable","chassis":"E90 chassis is well-engineered. RWD, near 50/50 weight distribution. Subframe issue from E46 largely resolved. M Sport suspension adds 15mm lower stance","electronics":"iDrive CCC system ages poorly. Window regulators fail across the E90 range. Generally less reliable than Japanese competitors but manageable. CCC to CIC retrofit possible","ease_of_repair":"N52 is one of the easier BMW engines to work on. Large DIY community. Most major services (VCG, OFHG, water pump) are weekend jobs. BMW-specific tools needed for some procedures. Parts more expensive than Toyota but widely available"}]')
WHERE car_id = 37;

UPDATE build_quality SET
  q_score = 67.0,
  score_body_construction = 72.0,
  score_nvh_isolation = 70.0,
  score_interior_materials = 64.0,
  score_paint_corrosion = 65.0,
  score_electrical_aging = 60.0,
  score_cosmetic_aging = 62.0,
  body_construction_notes = 'E90 chassis is well-engineered with good rigidity. Mixed materials: steel body with aluminum hood. RWD architecture. No subframe cracking issues like E46. M Sport package adds aerodynamic body kit with larger intakes and rear diffuser.',
  nvh_isolation_notes = 'Reasonable for a sport sedan. More road feel than luxury sedans. Tire noise present on run-flat tires (early E90). Sport suspension transmits more road texture. Not Lexus-quiet by design.',
  interior_materials_notes = 'Below Japanese competitors. Hard plastics in lower areas. Leather quality decent but not exceptional. M Sport seats have better bolsters. iDrive knob and screen era. Some cost-cutting vs E46 apparent.',
  paint_corrosion_notes = 'Average BMW paint. Early E90 had some paint quality issues. Galvanized body resists corrosion. No widespread rust issues reported.',
  electrical_aging_notes = 'iDrive CCC system (2005-2008) ages poorly. Screen delamination reported. CIC system (2009-2013) better. Window regulators fail across the E90 range. Electrical gremlins in higher-mileage examples.',
  cosmetic_aging_notes = 'Interior materials show age sooner than Japanese competitors. Hard plastics scratch easily. Leather wears well with care. Exterior trim holds up. M Sport aerodynamic pieces durable.',
  q_score_notes = 'E90 Q-score 67.0. Below Japanese luxury competitors (LS430 92.3) but appropriate for the segment. Sport sedan design means comfort features are less prioritized. Build quality is good for a BMW but the interior is notably downmarket from Lexus/Acura of the era. Electrical aging is the weak point.',
  platform_type = 'BMW E90',
  assembly_plant = 'Munich (Germany) / Leipzig (Germany) / Oxford (UK)',
  panel_gap_mm = 3.8,
  leather_grade = 'Dakota leather',
  paint_stages = 5
WHERE car_id = 37;

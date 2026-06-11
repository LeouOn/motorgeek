-- Fix 750i reliability recalibration
UPDATE reliability SET
  score_electronics = 65.0,
  score_ease_of_repair = 46.0,
  reliability_score = 62.0*0.25 + 88.0*0.25 + 85.0*0.15 + 65.0*0.15 + 46.0*0.20
WHERE car_id = 41;

-- Fix 750i build quality recalibration
UPDATE build_quality SET
  score_body_construction = 88.0,
  score_interior_materials = 87.0,
  score_paint_corrosion = 83.0,
  score_electrical_aging = 64.0,
  score_cosmetic_aging = 77.0,
  q_score = 88.0*0.25 + 88.0*0.10 + 87.0*0.20 + 83.0*0.15 + 64.0*0.15 + 77.0*0.15
WHERE car_id = 41;

-- Fix 750i engine_layout field
UPDATE powertrain_ice SET
  engine_layout = '4.4L twin-turbo V8 N63TU2 (750i)'
WHERE car_id = 41;

-- Fix 750i variant in cars table
UPDATE cars SET variant = '750i N63TU2' WHERE id = 41;

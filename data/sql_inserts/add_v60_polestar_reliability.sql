-- MotorGeek: Add V60 Polestar (id 98) reliability row
-- Pre-SPA VEA twincharged 2.0L, Polestar tune, 367 hp

INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (186, 98, 'sample', 68.0,
  '{"Supercharger clutch failure": 3, "Oil consumption (piston rings)": 3, "Turbo failure (if oil starved)": 2, "Polestar-specific suspension bushings": 2, "Electrical gremlins (CEM)": 1}',
  1100.0, 1, 'Limited (Polestar-specific parts)', 'Low',
  '{"VEA B4204T35 Polestar tune": "Same twincharged architecture as T6 but with aggressive Polestar tune pushing 367 hp. Same SC clutch failure risk as T6, but higher boost = more stress. Oil consumption worse than standard T6.", "Pre-Geely build quality": "2014-2018 Polestar models were built during Volvos transition period. Electronics (CEM module) can be finicky. Ohlins dampers are serviceable but expensive to replace.", "Why 68 not 72": "Same engine family as SPA T6 but -4 for: higher boost stress, Polestar-specific parts harder to source, Ohlins suspension rebuild costs, earlier VEA generation with more oil consumption issues. The SPA T6 at 72 runs less boost on a refined engine."}');

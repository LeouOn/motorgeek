-- Lexus dimensional reliability backfill
-- Based on librarian research: TSB/NHTSA/forum aggregation
-- Dimensions: engine, transmission, chassis, electronics, ease_of_repair

-- LS 400 (id 63) — overall 92
-- Engine 95: 1UZ-FE, overbuilt NA V8, port-injected, non-interference, no known systemic failures
-- Trans 93: A341E 4-speed hydraulic, indestructible
-- Chassis 88: Simple coils, proven platform, age-related bushing wear only
-- Electronics 85: Minimal electronics, OBD1/OBD2, no complex modules
-- Ease 95: Parts everywhere (shared with SC400/Supra), every shop knows it
UPDATE reliability SET
  score_engine = 95, score_transmission = 93, score_chassis = 88,
  score_electronics = 85, score_ease_of_repair = 95,
  score_notes = '{"engine": "1UZ-FE, overbuilt NA V8, port-injected, non-interference, forged crank", "transmission": "A341E 4-speed hydraulic, indestructible, zero failure patterns", "chassis": "Simple coils, age-related bushing wear only, no rust issues on JDM", "electronics": "Minimal electronics, OBD1 (pre-93)/OBD2, no complex modules", "ease_of_repair": "Parts everywhere (SC400/Supra/Celsior), every shop knows it, cheap maintenance"}'
WHERE car_id = 63;

-- LS 430 (id 39) — overall 90
-- Engine 92: 3UZ-FE, same 1UZ architecture, port-injected, timing belt
-- Trans 90: A650E 5-speed, proven, smooth
-- Chassis 85: Standard coils (UL has air), well-sorted
-- Electronics 82: More modules than LS400 but still simple era
-- Ease 90: Toyota/Lexus shared, good parts network
UPDATE reliability SET
  score_engine = 92, score_transmission = 90, score_chassis = 85,
  score_electronics = 82, score_ease_of_repair = 90,
  score_notes = '{"engine": "3UZ-FE, same 1UZ architecture bored to 4.3L, port-injected, timing belt", "transmission": "A650E 5-speed, proven unit, zero failure patterns", "chassis": "Standard coils (UL has air ride), well-sorted, no rust issues", "electronics": "More modules than LS400 but still pre-CAN complexity era", "ease_of_repair": "Toyota/Lexus shared parts, good dealer + indie support"}'
WHERE car_id = 39;

-- LS 460 (id 40) — overall 75
-- Engine 88: 1UR-FSE D-4S, sound design, no carbon buildup
-- Trans 45: AA80E 8-speed, valve body failures, FIRST production 8-speed, $2-4K fix
-- Chassis 78: Air suspension widely available, 10+ year air bag leaks
-- Electronics 72: More sensors, modules, CAN bus complexity
-- Ease 75: Lexus dealer + specialist, air suspension parts expensive
UPDATE reliability SET
  score_engine = 88, score_transmission = 45, score_chassis = 78,
  score_electronics = 72, score_ease_of_repair = 75,
  score_notes = '{"engine": "1UR-FSE D-4S, dual injection = no carbon buildup, sound design but more complex than 3UZ", "transmission": "AA80E 8-speed, FIRST production 8-speed auto, valve body failures (grind/hesitation), pre-2012 most affected, $2-4K fix", "chassis": "Air suspension on multiple trims (not just UL), air bags leak at 10+ years, $2-3K/corner", "electronics": "Significantly more sensors/modules than LS430, CAN bus era, more failure points", "ease_of_repair": "Lexus dealer + specialist needed, air suspension parts expensive, D-4S tools required"}'
WHERE car_id = 40;

-- LS 600h (id 24) — overall 68
-- Engine 82: 2UR-FSE D-4S, sound but hybrid adds stress
-- Trans 40: Unique eCVT hybrid transaxle, no aftermarket, $8K+ if it fails
-- Chassis 70: Air suspension STANDARD (all corners), AWD complexity
-- Electronics 60: Hybrid inverter, battery management, regen braking, most complex
-- Ease 40: Low-volume, Lexus hybrid specialist only, very expensive
UPDATE reliability SET
  score_engine = 82, score_transmission = 40, score_chassis = 70,
  score_electronics = 60, score_ease_of_repair = 40,
  score_notes = '{"engine": "2UR-FSE D-4S, sound V8 but hybrid adds thermal/electrical stress on engine", "transmission": "Unique eCVT planetary gear hybrid transaxle, no aftermarket, very few shops, $8K+ replacement", "chassis": "Air suspension STANDARD on all LS600h, permanent AWD adds wear items, heavy vehicle", "electronics": "Hybrid inverter, battery management, regen braking, most complex electronics of any LS", "ease_of_repair": "Low-volume Lexus hybrid specialist only, parts scarce, very expensive repairs"}'
WHERE car_id = 24;

-- ES 350 XV40 (id 86) — overall 89
-- Engine 90: 2GR-FE, port-injected NA V6, millions produced, bulletproof
-- Trans 88: U660E 6-speed Aisin, proven, no failure patterns
-- Chassis 82: Camry platform coils, simple, proven
-- Electronics 80: Standard era electronics, no major issues
-- Ease 95: Camry platform, every shop knows it, cheapest luxury car to maintain
UPDATE reliability SET
  score_engine = 90, score_transmission = 88, score_chassis = 82,
  score_electronics = 80, score_ease_of_repair = 95,
  score_notes = '{"engine": "2GR-FE port-injected NA V6, millions produced, shared with Camry/RX350/Avalon/Sienna/Highlander, bulletproof NA design", "transmission": "U660E 6-speed Aisin, proven unit, no known failure patterns", "chassis": "XXV40 Camry platform, simple coil springs, proven suspension, no air ride", "electronics": "Standard era electronics, throttle body P0505 on some years, no major module failures", "ease_of_repair": "Camry platform = every wear part is a Toyota part, every shop knows this car, cheapest luxury car to maintain"}'
WHERE car_id = 86;

-- GS 350 4th gen (id 35) — overall 88
-- Engine 92: 2GR-FSE/FKS D-4S, NO carbon buildup, proven longitudinal
-- Trans 85: AA81E 8-speed RWD well-sorted / 6-speed AWD bulletproof
-- Chassis 82: Double wishbone + multi-link, no air ride, well-engineered
-- Electronics 80: More complex than ES but Lexus-quality
-- Ease 82: Shared with IS350/RX350, longitudinal access easier
UPDATE reliability SET
  score_engine = 92, score_transmission = 85, score_chassis = 82,
  score_electronics = 80, score_ease_of_repair = 82,
  score_notes = '{"engine": "2GR-FSE/FKS D-4S dual injection = NO carbon buildup, port injection cleans valves, longitudinal mount, one of best V6s ever made", "transmission": "AA81E 8-speed RWD well-sorted, AWD gets bulletproof 6-speed, some shift complaints on 2016+ RWD but not reliability", "chassis": "Double wishbone front + multi-link rear, no air ride option, well-engineered platform", "electronics": "More complex than ES (AVS dampers, more sensors) but Lexus-quality, fuel pump recall (free fix)", "ease_of_repair": "Shared with IS350/RX350 Toyota/Lexus, longitudinal mount = easier timing cover access than transverse ES"}'
WHERE car_id = 35;

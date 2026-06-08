-- ============================================================
-- Lexus Reliability Inserts (6 cars)
-- LS 400 (63), LS 430 (39), LS 460 (40), LS 600h (24), GS 350 (35), ES 350 (86)
-- Scores based on librarian research: TSB/NHTSA/forum aggregation
-- Current methodology: single imputed score (vibes-based, dimensional rework pending)
-- ============================================================

-- ============================================================
-- 1. RELIABILITY ROWS (starting at id 187)
-- ============================================================

-- LS 400 (id 63) — Score: 92
-- The 1UZ-FE 4.0L V8 launched the Lexus legend.
-- Port-injected, NA, non-interference, timing belt. 4-speed A341E unbreakable.
-- Only penalty: age (1989-1994), trim/body parts scarce.
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (
  187, 63, 'sample', 92.0,
  '{"Power steering pump whine": 1, "A/C compressor clutch (age)": 1, "Door lock actuators": 1, "Dash stitching separation (cosmetic)": 1}',
  400.0, 0,
  'Fair (engine/powertrain excellent; trim/body scarce)',
  'High',
  '{"1UZ-FE V8": "The legend. Port-injected, NA, non-interference. Timing belt every 90K. Bulletproof bottom end. No carbon buildup possible.", "A341E 4-speed": "Indestructible. Hydraulic, not electronic. Will outlast the car.", "Age factor": "1989-1994. Engine parts everywhere (shared with Supra/SC400). Body/trim/interior parts getting scarce.", "No OBD2": "1991 and earlier = OBD1. 1993-1994 have OBD2."}'
);

-- LS 430 (id 39) — Score: 90
-- The perfected LS. 3UZ-FE is 1UZ architecture bored to 4.3L.
-- Port-injected NA V8. 5-speed A650E proven. "King of Reliability."
-- Dashboard cracking is cosmetic, not mechanical.
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (
  188, 39, 'sample', 90.0,
  '{"Dashboard cracking (UV)": 1, "Door lock actuators": 1, "Air suspension (UL package only)": 2, "VVT-i oil line (early years)": 1}',
  450.0, 1,
  'Good (Toyota/Lexus shared)',
  'High',
  '{"3UZ-FE V8": "Evolution of the 1UZ. Port-injected NA V8. Timing belt. No carbon buildup possible. Same bulletproof architecture as LS400.", "A650E 5-speed": "Proven hydraulic unit. Smooth and reliable. Not as efficient as newer boxes but unbreakable.", "Dashboard": "UV cracking common in sunbelt states. Cosmetic only. Many replaced under TSB.", "Air suspension": "ONLY on Ultra Luxury package. Standard cars have coil springs. Air bags leak at 15+ years, $2K+ per corner."}'
);

-- LS 460 (id 40) — Score: 75
-- 1UR-FSE 4.6L with D-4S. More complex than LS430.
-- 8-speed AA80E had valve body issues (first production 8-speed).
-- Optional air suspension is the Achilles heel.
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (
  189, 40, 'sample', 75.0,
  '{"8-speed valve body (grind/hesitation)": 3, "Air suspension (if equipped)": 3, "Timing cover oil seep": 2, "Intake manifold runner control": 2, "EVAP canister": 1}',
  800.0, 3,
  'Good (Toyota/Lexus specialist)',
  'Moderate',
  '{"1UR-FSE V8": "D-4S dual injection = no carbon buildup. But more complex than 3UZ. Timing chain (not belt). Timing cover leak possible.", "AA80E 8-speed": "FIRST production 8-speed automatic. Valve body issues: grinding between gears, hesitation on downshift. TSB issued. $2-4K fix. Pre-2012 most affected.", "Air suspension": "Optional on all LS460s. Air bags leak at 10+ years. Compressor fails. $2-3K per corner. Most owners convert to coil springs.", "Complexity jump": "Significantly more electronics than LS430. More sensors, modules, failure points."}'
);

-- LS 600h (id 24) — Score: 68
-- Most complex LS ever: V8 + hybrid + AWD.
-- Hybrid battery aging ($3-5K). Unique CVT. Very low production.
-- $126K MSRP = luxury-tier repair bills forever.
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (
  190, 24, 'sample', 68.0,
  '{"Hybrid battery degradation (10+ yr)": 3, "Inverter/converter failure": 3, "CVT unique to this model": 3, "Air suspension": 3, "Brake booster (regen hybrid)": 2}',
  1200.0, 2,
  'Poor (low-volume Lexus specialist only)',
  'Low',
  '{"Hybrid system": "V8 + electric + AWD = most complex LS drivetrain ever. Battery at 10-15 years = $3-5K replacement. Inverter failures documented.", "CVT hybrid trans": "Planetary gear hybrid transmission unique to LS600h. Very few shops can service. Parts scarce.", "AWD system": "Permanent AWD adds complexity. Not the same as LS460 RWD.", "Value proposition": "$126K MSRP new. Depreciated hard. Repair bills dont depreciate."}'
);

-- GS 350 4th gen (id 35) — Score: 88
-- 2GR-FSE/FKS with D-4S = NO carbon buildup. Major advantage.
-- Longitudinal mount = easier timing cover access than transverse ES.
-- 2013 has first-year issues; 2014+ are excellent.
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (
  191, 35, 'sample', 88.0,
  '{"Fuel pump recall (Denso impeller)": 2, "Timing cover seep (longitudinal, less severe)": 2, "2013 first-year issues": 2, "Serpentine belt tensioner (high mileage)": 1}',
  590.0, 3,
  'Good (Toyota/Lexus shared)',
  'Moderate',
  '{"2GR-FSE/FKS V6": "D-4S dual injection = NO carbon buildup. Port injection cleans valves continuously. One of the best V6s ever made.", "AA81E 8-speed": "Well-sorted. Some shift logic complaints on RWD 2016+ but not reliability. AWD keeps 6-speed = bulletproof.", "Longitudinal advantage": "Timing cover leak much easier to fix on RWD longitudinal than transverse ES. Lower repair cost.", "2013 vs 2014+": "2013 has most complaints (battery, sunroof, wheel bolts). 2014+ excellent. Score reflects whole generation."}'
);

-- ES 350 XV40 (id 86) — Score: 89
-- 2GR-FE 3.5L V6. The Camry engine in a tuxedo.
-- Port-injected, NA. One of the most produced engines ever.
-- Timing cover leak is the big issue ($4.5-8K on transverse).
-- Fundamentally a fancy Camry. That IS the point.
INSERT INTO reliability (id, car_id, source, reliability_score, common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (
  192, 86, 'sample', 89.0,
  '{"Timing cover oil leak (transverse, $4.5-8K)": 3, "VVT-i oil line rupture (2007-08, LSC fix)": 2, "Water pump (60-120K)": 1, "Evaporator core leak (2007-09)": 2, "Dashboard melt (2007-08)": 1}',
  468.0, 5,
  'Excellent (Toyota Camry shared platform)',
  'High',
  '{"2GR-FE V6": "Port-injected NA V6. Same as Camry V6, Avalon, RX 350, Highlander, Sienna. Millions made. Parts everywhere.", "Timing cover leak": "THE big 2GR issue. On transverse mount, engine removed with subframe. $4.5-8K. Manageable with heavier oil for slow seeps.", "VVT-i oil line": "2007-2008 rubber hose degrades, can burst. LSC replaced with metal line free. Check records. Fixed = non-issue.", "U660E 6-speed": "Proven Aisin unit. No known issues.", "Platform": "XXV40 = Camry platform. Every part is a Toyota part."}'
);


-- ============================================================
-- 2. COST TO OWN UPDATES (fill missing maintenance + fuel econ)
-- ============================================================

-- LS 600h (id 24): fuel economy + maintenance
-- EPA 19/22 for 5.0L V8 hybrid AWD (2008 methodology)
UPDATE cost_to_own SET
  fuel_econ_city_mpg = 19.0,
  fuel_econ_hwy_mpg = 22.0,
  annual_maintenance_est = 1200.0
WHERE car_id = 24;

-- LS 400 (id 63): maintenance only
-- Simple old V8, cheap parts, age-related items
UPDATE cost_to_own SET
  annual_maintenance_est = 400.0
WHERE car_id = 63;

-- LS 430 (id 39): maintenance only
-- Reliable but luxury pricing on some items
UPDATE cost_to_own SET
  annual_maintenance_est = 450.0
WHERE car_id = 39;

-- LS 460 (id 40): maintenance only
-- 8-speed valve body risk, air suspension, D-4S complexity
UPDATE cost_to_own SET
  annual_maintenance_est = 800.0
WHERE car_id = 40;

-- GS 350 (id 35): maintenance only
-- RepairPal: $592/yr
UPDATE cost_to_own SET
  annual_maintenance_est = 590.0
WHERE car_id = 35;

-- ES 350 (id 86): maintenance only
-- RepairPal: $468/yr
UPDATE cost_to_own SET
  annual_maintenance_est = 468.0
WHERE car_id = 86;


-- ============================================================
-- 3. POWERTRAIN DATA FIXES
-- ============================================================

-- ES 350 (id 86): Fix transmission from generic 'automatic'
UPDATE powertrain_ice SET
  transmission_type = '6-speed automatic (U660E)'
WHERE car_id = 86 AND transmission_type = 'automatic';

-- LS 600h (id 24): Fix hybrid flag — this IS a hybrid
UPDATE powertrain_ice SET
  is_hybrid = 1
WHERE car_id = 24 AND is_hybrid = 0;

-- LS 430 (id 39): Fix engine code — 3UZ-FE, not 1UZ-FE
-- LS430 uses 3UZ-FE 4.3L. 1UZ-FE is the 4.0L in LS400.
UPDATE powertrain_ice SET
  engine_layout = 'front longitudinal'
WHERE car_id = 39 AND engine_layout = '4.3L V8 (1UZ-FE)';

-- LS 400 (id 63): Fill missing engine_layout
UPDATE powertrain_ice SET
  engine_layout = 'front longitudinal'
WHERE car_id = 63 AND (engine_layout IS NULL OR engine_layout = '');

-- LS 600h (id 24): Fill missing gear_count for CVT
UPDATE powertrain_ice SET
  gear_count = NULL
WHERE car_id = 24 AND gear_count IS NULL;

-- ============================================================
-- MotorGeek DB: Cleanup duplicate rows from failed SQL inserts
-- Date: 2026-06-08
-- ============================================================

-- POWERTRAIN: Delete wrong rows (Mercedes data that leaked in)
DELETE FROM powertrain_ice WHERE id = 182;  -- car 151 with 2996cc/9G = wrong
DELETE FROM powertrain_ice WHERE id = 183;  -- car 152 with 2999cc/9G = wrong
DELETE FROM powertrain_ice WHERE id = 185;  -- car 151 duplicate of id 151

-- RELIABILITY: Delete lower-ID duplicates (keep the v2 IDs 168-180)
DELETE FROM reliability WHERE id = 165;  -- car 8
DELETE FROM reliability WHERE id = 160;  -- car 29
DELETE FROM reliability WHERE id = 163;  -- car 32
DELETE FROM reliability WHERE id = 164;  -- car 33
DELETE FROM reliability WHERE id = 161;  -- car 38
DELETE FROM reliability WHERE id = 166;  -- car 44
DELETE FROM reliability WHERE id = 167;  -- car 45
DELETE FROM reliability WHERE id = 162;  -- car 54

-- New cars reliability: delete first-file rows (some have wrong scores)
DELETE FROM reliability WHERE id = 25;   -- car 151, score 68 = WRONG
DELETE FROM reliability WHERE id = 151;  -- car 151, duplicate of 168
DELETE FROM reliability WHERE id = 26;   -- car 152, score 75 = WRONG
DELETE FROM reliability WHERE id = 152;  -- car 152, duplicate of 169
DELETE FROM reliability WHERE id = 153;  -- car 153, duplicate of 170
DELETE FROM reliability WHERE id = 154;  -- car 154, duplicate of 171
DELETE FROM reliability WHERE id = 155;  -- car 155, duplicate of 172

-- COST_TO_OWN: Delete wrong rows (Mercedes MPG/maint data)
DELETE FROM cost_to_own WHERE id = 184;  -- car 151, 21/29 mpg $1100 = WRONG
DELETE FROM cost_to_own WHERE id = 185;  -- car 152, 22/30 mpg $1000 = WRONG

-- MARKET_HISTORY: Delete duplicates/wrong pricing
DELETE FROM market_history WHERE id = 144;  -- car 151, $22K-42K = wrong
DELETE FROM market_history WHERE id = 145;  -- car 152, $38K-60K = wrong
DELETE FROM market_history WHERE id = 153;  -- car 153, duplicate of 158
DELETE FROM market_history WHERE id = 154;  -- car 154, duplicate of 159
DELETE FROM market_history WHERE id = 155;  -- car 155, duplicate of 160

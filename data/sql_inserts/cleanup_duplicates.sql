-- ============================================================
-- CLEANUP: Remove duplicate rows from failed SQL executions
-- ============================================================

-- POWERTRAIN: delete wrong data rows (Mercedes data in Genesis slots)
DELETE FROM powertrain_ice WHERE id = 182 AND car_id = 151;  -- 2996cc/9G = wrong
DELETE FROM powertrain_ice WHERE id = 183 AND car_id = 152;  -- 2999cc/9G = wrong

-- POWERTRAIN: delete duplicate from first file (keep v2 row at 185)
-- car 151 has rows at id 151 AND 185 (both correct 3342/8-speed). Keep 185 (latest), delete 151.
DELETE FROM powertrain_ice WHERE id = 151 AND car_id = 151;

-- RELIABILITY: delete earlier-file duplicates for backfilled cars
DELETE FROM reliability WHERE id = 165 AND car_id = 8;
DELETE FROM reliability WHERE id = 160 AND car_id = 29;
DELETE FROM reliability WHERE id = 163 AND car_id = 32;
DELETE FROM reliability WHERE id = 164 AND car_id = 33;
DELETE FROM reliability WHERE id = 161 AND car_id = 38;
DELETE FROM reliability WHERE id = 166 AND car_id = 44;
DELETE FROM reliability WHERE id = 167 AND car_id = 45;
DELETE FROM reliability WHERE id = 162 AND car_id = 54;

-- RELIABILITY: delete earlier-file duplicates for new cars (151-155)
-- car 151: has ids 25, 151, 168. Keep 168 (v2)
DELETE FROM reliability WHERE id = 25 AND car_id = 151;
DELETE FROM reliability WHERE id = 151 AND car_id = 151;
-- car 152: has ids 26, 152, 169. Keep 169 (v2)
DELETE FROM reliability WHERE id = 26 AND car_id = 152;
DELETE FROM reliability WHERE id = 152 AND car_id = 152;
-- car 153: has ids 153, 170. Keep 170 (v2)
DELETE FROM reliability WHERE id = 153 AND car_id = 153;
-- car 154: has ids 154, 171. Keep 171 (v2)
DELETE FROM reliability WHERE id = 154 AND car_id = 154;
-- car 155: has ids 155, 172. Keep 172 (v2)
DELETE FROM reliability WHERE id = 155 AND car_id = 155;

-- COST_TO_OWN: delete earlier-file duplicates
-- car 151: has ids 184, 189. Keep 189 (17/25/700/55250 = correct)
DELETE FROM cost_to_own WHERE id = 184 AND car_id = 151;
-- car 152: has ids 185, 190. Keep 190 (21/29/550/39000 = correct)
DELETE FROM cost_to_own WHERE id = 185 AND car_id = 152;

-- MARKET_HISTORY: delete earlier-file duplicates
-- car 151: has ids 144, 156. Keep 156 (v2)
DELETE FROM market_history WHERE id = 144 AND car_id = 151;
-- car 152: has ids 145, 157. Keep 157 (v2)
DELETE FROM market_history WHERE id = 145 AND car_id = 152;
-- car 153: has ids 153, 158. Keep 158 (v2)
DELETE FROM market_history WHERE id = 153 AND car_id = 153;
-- car 154: has ids 154, 159. Keep 159 (v2)
DELETE FROM market_history WHERE id = 154 AND car_id = 154;
-- car 155: has ids 155, 160. Keep 160 (v2)
DELETE FROM market_history WHERE id = 155 AND car_id = 155;

-- ============================================================
-- DONE
-- ============================================================

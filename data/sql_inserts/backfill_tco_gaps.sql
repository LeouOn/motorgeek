-- Phase 1: INSERT cost_to_own for 8 cars that have no row at all
INSERT INTO cost_to_own (car_id, source, msrp_original, msrp_currency, fuel_econ_city_mpg, fuel_econ_hwy_mpg, annual_maintenance_est)
VALUES
  (166, 'librarian-estimate', 32000.0, 'USD', 16.0, 25.0, 700.0),
  (167, 'librarian-estimate', 42000.0, 'USD', 18.0, 27.0, 750.0),
  (169, 'librarian-estimate', 44000.0, 'USD', 19.0, 28.0, 650.0),
  (171, 'librarian-estimate', 76000.0, 'USD', 16.0, 21.0, 900.0),
  (172, 'librarian-estimate', 55000.0, 'USD', 17.0, 24.0, 850.0),
  (173, 'librarian-estimate', 48000.0, 'USD', 18.0, 25.0, 800.0),
  (174, 'librarian-estimate', 38000.0, 'USD', 21.0, 28.0, 700.0),
  (175, 'librarian-estimate', 75000.0, 'USD', 15.0, 22.0, 900.0);

-- Phase 2: Fill missing MSRP values
UPDATE cost_to_own SET msrp_original = 25000.0 WHERE car_id = 81 AND msrp_original IS NULL;
UPDATE cost_to_own SET msrp_original = 55000.0 WHERE car_id = 163 AND msrp_original IS NULL;

-- Phase 3: Fill missing maintenance estimates by brand/reliability tier
-- Porsche: $1,400-2,000
UPDATE cost_to_own SET annual_maintenance_est = 1500.0 WHERE car_id IN (17,18,104) AND annual_maintenance_est IS NULL;
UPDATE cost_to_own SET annual_maintenance_est = 2000.0 WHERE car_id IN (21,49) AND annual_maintenance_est IS NULL;

-- BMW: $750-1,300 (B58 era cheaper, older V8 more expensive)
UPDATE cost_to_own SET annual_maintenance_est = 1300.0 WHERE car_id = 41 AND annual_maintenance_est IS NULL;
UPDATE cost_to_own SET annual_maintenance_est = 800.0 WHERE car_id IN (13,19) AND annual_maintenance_est IS NULL;
UPDATE cost_to_own SET annual_maintenance_est = 1200.0 WHERE car_id = 65 AND annual_maintenance_est IS NULL;
UPDATE cost_to_own SET annual_maintenance_est = 1000.0 WHERE car_id IN (37,23,51,50,52) AND annual_maintenance_est IS NULL;

-- Mercedes: $800-1,500
UPDATE cost_to_own SET annual_maintenance_est = 1400.0 WHERE car_id = 42 AND annual_maintenance_est IS NULL;
UPDATE cost_to_own SET annual_maintenance_est = 1000.0 WHERE car_id IN (82,79,67,53) AND annual_maintenance_est IS NULL;

-- Audi: $800-1,400
UPDATE cost_to_own SET annual_maintenance_est = 1200.0 WHERE car_id = 66 AND annual_maintenance_est IS NULL;

-- Honda/Acura: $450-600
UPDATE cost_to_own SET annual_maintenance_est = 500.0 WHERE car_id IN (48,88,28) AND annual_maintenance_est IS NULL;
UPDATE cost_to_own SET annual_maintenance_est = 800.0 WHERE car_id = 80 AND annual_maintenance_est IS NULL;
UPDATE cost_to_own SET annual_maintenance_est = 3000.0 WHERE car_id = 118 AND annual_maintenance_est IS NULL;

-- Toyota/Lexus: $400-600
UPDATE cost_to_own SET annual_maintenance_est = 500.0 WHERE car_id = 16 AND annual_maintenance_est IS NULL;

-- Subaru: $550-800
UPDATE cost_to_own SET annual_maintenance_est = 600.0 WHERE car_id IN (131,60,61,84) AND annual_maintenance_est IS NULL;

-- Nissan: $600-800
UPDATE cost_to_own SET annual_maintenance_est = 800.0 WHERE car_id IN (58,59,57) AND annual_maintenance_est IS NULL;

-- Ford: $550-800
UPDATE cost_to_own SET annual_maintenance_est = 800.0 WHERE car_id = 11 AND annual_maintenance_est IS NULL;

-- Mazda: $450-550
UPDATE cost_to_own SET annual_maintenance_est = 500.0 WHERE car_id = 14 AND annual_maintenance_est IS NULL;

-- Cadillac: $650-900
UPDATE cost_to_own SET annual_maintenance_est = 800.0 WHERE car_id IN (27,26,36) AND annual_maintenance_est IS NULL;

-- VW: $600-800
UPDATE cost_to_own SET annual_maintenance_est = 700.0 WHERE car_id IN (12,62) AND annual_maintenance_est IS NULL;

-- Land Rover: $1,500+
UPDATE cost_to_own SET annual_maintenance_est = 1800.0 WHERE car_id = 55 AND annual_maintenance_est IS NULL;

-- Alpine: $1,000+
UPDATE cost_to_own SET annual_maintenance_est = 1000.0 WHERE car_id = 15 AND annual_maintenance_est IS NULL;

-- Infiniti: $600-800
UPDATE cost_to_own SET annual_maintenance_est = 700.0 WHERE car_id IN (64,34) AND annual_maintenance_est IS NULL;

-- Peugeot: $800
UPDATE cost_to_own SET annual_maintenance_est = 800.0 WHERE car_id = 68 AND annual_maintenance_est IS NULL;

-- Genesis: $600-900
UPDATE cost_to_own SET annual_maintenance_est = 800.0 WHERE car_id = 163 AND annual_maintenance_est IS NULL;

-- Tesla/EVs: $600-800
UPDATE cost_to_own SET annual_maintenance_est = 700.0 WHERE car_id IN (71,70,72,73,75,76,74) AND annual_maintenance_est IS NULL;

-- Phase 4: Fill missing MPG for gas cars
-- BMW M3 CSL
UPDATE cost_to_own SET fuel_econ_city_mpg = 15.0, fuel_econ_hwy_mpg = 22.0 WHERE car_id = 19 AND fuel_econ_city_mpg IS NULL;
-- Toyota Supra SZ (NA 2JZ)
UPDATE cost_to_own SET fuel_econ_city_mpg = 18.0, fuel_econ_hwy_mpg = 23.0 WHERE car_id = 20 AND fuel_econ_city_mpg IS NULL;
-- Honda Civic Type R FK8
UPDATE cost_to_own SET fuel_econ_city_mpg = 22.0, fuel_econ_hwy_mpg = 28.0 WHERE car_id = 80 AND fuel_econ_city_mpg IS NULL;
-- Ford Focus ST
UPDATE cost_to_own SET fuel_econ_city_mpg = 19.0, fuel_econ_hwy_mpg = 26.0 WHERE car_id = 81 AND fuel_econ_city_mpg IS NULL;

-- Phase 5: Set MPG to 0 (marker) for EVs that shouldn't have gas MPG
UPDATE cost_to_own SET fuel_econ_city_mpg = 0.0, fuel_econ_hwy_mpg = 0.0 WHERE car_id IN (71,70,72,73,75,76,74) AND fuel_econ_city_mpg IS NULL;

-- Phase 6: Verify coverage
SELECT 'cost_to_own rows' AS metric, COUNT(*) FROM cost_to_own
UNION ALL SELECT 'missing MSRP', COUNT(*) FROM cost_to_own WHERE msrp_original IS NULL
UNION ALL SELECT 'missing city MPG', COUNT(*) FROM cost_to_own WHERE fuel_econ_city_mpg IS NULL
UNION ALL SELECT 'missing maintenance', COUNT(*) FROM cost_to_own WHERE annual_maintenance_est IS NULL;

-- ============================================================
-- Fill remaining lacunas for Genesis G90/G70 and Audi A6 C8
-- ============================================================

-- POWERTRAIN: Fill missing details for G70/G90 entries

-- id 8: G90 5.0 V8 — Tau V8
UPDATE powertrain_ice SET cylinders = 8, aspiration = 'Naturally aspirated', transmission_type = '8-speed automatic', gear_count = 8, drivetrain = 'RWD standard / AWD optional', fuel_system = 'MPI (port injection)' WHERE car_id = 8;

-- id 38: G70 3.3T — Lambda II
UPDATE powertrain_ice SET cylinders = 6, aspiration = 'Twin-turbocharged', transmission_type = '8-speed automatic', gear_count = 8, drivetrain = 'RWD standard / AWD optional', fuel_system = 'GDI (direct injection only)' WHERE car_id = 38;

-- id 44: G90 1st gen 3.3T — Lambda II
UPDATE powertrain_ice SET cylinders = 6, aspiration = 'Twin-turbocharged', transmission_type = '8-speed automatic', gear_count = 8, drivetrain = 'RWD standard / AWD optional', fuel_system = 'GDI (direct injection only)' WHERE car_id = 44;

-- id 45: G90 2nd gen 3.5T — Smartstream Lambda III
UPDATE powertrain_ice SET cylinders = 6, aspiration = 'Twin-turbocharged', transmission_type = '8-speed automatic', gear_count = 8, drivetrain = 'AWD standard', fuel_system = 'Dual injection (GDi + MPi)' WHERE car_id = 45;

-- COST_TO_OWN: Fill missing maintenance estimates

-- id 8: G90 5.0 V8
UPDATE cost_to_own SET annual_maintenance_est = 900.0 WHERE car_id = 8 AND annual_maintenance_est IS NULL;

-- id 32: A6 C8 55 TFSI
UPDATE cost_to_own SET annual_maintenance_est = 1100.0 WHERE car_id = 32 AND annual_maintenance_est IS NULL;

-- id 44: G90 1st gen 3.3T
UPDATE cost_to_own SET annual_maintenance_est = 800.0 WHERE car_id = 44 AND annual_maintenance_est IS NULL;

-- id 45: G90 2nd gen 3.5T
UPDATE cost_to_own SET annual_maintenance_est = 800.0 WHERE car_id = 45 AND annual_maintenance_est IS NULL;

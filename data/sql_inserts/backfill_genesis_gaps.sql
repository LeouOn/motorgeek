-- Fill thin powertrain rows for existing Genesis entries
UPDATE powertrain_ice SET cylinders = 8, aspiration = 'Naturally aspirated', fuel_system = 'MPI (port injection)', transmission_type = '8-speed automatic', gear_count = 8, drivetrain = 'RWD standard / AWD optional' WHERE car_id = 8;
UPDATE powertrain_ice SET cylinders = 6, aspiration = 'Twin-turbo', fuel_system = 'GDI (direct injection only)', transmission_type = '8-speed automatic', gear_count = 8, drivetrain = 'RWD standard / AWD optional' WHERE car_id = 38;
UPDATE powertrain_ice SET cylinders = 6, aspiration = 'Twin-turbo', fuel_system = 'GDI (direct injection only)', transmission_type = '8-speed automatic', gear_count = 8, drivetrain = 'RWD standard / AWD optional' WHERE car_id = 44;
UPDATE powertrain_ice SET cylinders = 6, aspiration = 'Twin-turbo', fuel_system = 'Dual injection (GDi + MPi)', transmission_type = '8-speed automatic', gear_count = 8, drivetrain = 'AWD standard (HTRAC)' WHERE car_id = 45;

-- Fill missing maintenance estimates
UPDATE cost_to_own SET annual_maintenance_est = 900.0 WHERE car_id = 8 AND annual_maintenance_est IS NULL;
UPDATE cost_to_own SET annual_maintenance_est = 1100.0 WHERE car_id = 32 AND annual_maintenance_est IS NULL;
UPDATE cost_to_own SET annual_maintenance_est = 800.0 WHERE car_id = 44 AND annual_maintenance_est IS NULL;
UPDATE cost_to_own SET annual_maintenance_est = 800.0 WHERE car_id = 45 AND annual_maintenance_est IS NULL;

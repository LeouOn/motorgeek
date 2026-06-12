-- Update car entry to reflect 2007-2011 N52 328i (not generic 2005 E90)
UPDATE cars SET
  year_start = 2007,
  year_end = 2011,
  variant = '328i 6MT N52',
  description = 'BMW 328i E90 with the N52B30 naturally aspirated 3.0L inline-6. The last naturally aspirated I6 BMW ever produced — after this, every BMW I6 was turbocharged (N54, N55, B58). Magnesium/aluminum composite block, Valvetronic variable valve lift, 230hp. Available with 6-speed manual. The thesis: last analog BMW driver experience.'
WHERE id = 37;

-- Fix powertrain to N52 328i specs
UPDATE powertrain_ice SET
  engine_layout = '3.0L NA I6 N52B30',
  displacement_cc = 2996.0,
  cylinders = 6,
  aspiration = 'naturally aspirated',
  horsepower_bhp = 230.0,
  horsepower_rpm = 6500,
  torque_nm = 270.0,
  torque_rpm = 2750,
  redline_rpm = 7000,
  compression_ratio = 10.7,
  fuel_system = 'direct injection',
  transmission_type = '6-speed manual',
  gear_count = 6,
  drivetrain = 'RWD',
  curb_weight_kg = 1490.0,
  fuel_tank_capacity_l = 60.0,
  fuel_consumption_mixed_l_100km = 8.4
WHERE car_id = 37;

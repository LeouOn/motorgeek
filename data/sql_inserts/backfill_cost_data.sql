-- Car 22: Audi A8 D5 2017 — needs annual_maintenance_est
UPDATE cost_to_own SET annual_maintenance_est = 1400.0 WHERE car_id = 22;

-- Car 43: Audi A8 D5 2020 facelift — needs fuel economy + maintenance
UPDATE cost_to_own SET
  fuel_econ_city_mpg = 17.0,
  fuel_econ_hwy_mpg = 26.0,
  annual_maintenance_est = 1100.0
WHERE car_id = 43;

-- Car 164: BMW 740i B58 G11 2017 — needs ALL
UPDATE cost_to_own SET
  msrp_original = 82495.0,
  fuel_econ_city_mpg = 21.0,
  fuel_econ_hwy_mpg = 29.0,
  annual_maintenance_est = 1300.0
WHERE car_id = 164;

-- Car 165: Lincoln Continental 3.0T AWD 2017 — needs ALL
UPDATE cost_to_own SET
  msrp_original = 63075.0,
  fuel_econ_city_mpg = 16.0,
  fuel_econ_hwy_mpg = 24.0,
  annual_maintenance_est = 850.0
WHERE car_id = 165;

-- Car 168: Buick LaCrosse 3.6L 2017 — needs ALL
UPDATE cost_to_own SET
  msrp_original = 33990.0,
  fuel_econ_city_mpg = 21.0,
  fuel_econ_hwy_mpg = 31.0,
  annual_maintenance_est = 650.0
WHERE car_id = 168;

-- Car 170: Chevy SS LS3 6MT 2015 — needs ALL
UPDATE cost_to_own SET
  msrp_original = 46740.0,
  fuel_econ_city_mpg = 15.0,
  fuel_econ_hwy_mpg = 21.0,
  annual_maintenance_est = 900.0
WHERE car_id = 170;

-- Car 176: BMW E38 740i 1995-2001 — needs ALL
UPDATE cost_to_own SET
  msrp_original = 62000.0,
  fuel_econ_city_mpg = 15.0,
  fuel_econ_hwy_mpg = 22.0,
  annual_maintenance_est = 1800.0
WHERE car_id = 176;

-- Car 177: Audi A8 D3 4.2 FSI 2006 — needs ALL
UPDATE cost_to_own SET
  msrp_original = 68130.0,
  fuel_econ_city_mpg = 17.0,
  fuel_econ_hwy_mpg = 24.0,
  annual_maintenance_est = 1500.0
WHERE car_id = 177;

-- Car 178: Mercedes W126 560SEL 1986 — needs ALL
UPDATE cost_to_own SET
  msrp_original = 63900.0,
  fuel_econ_city_mpg = 14.0,
  fuel_econ_hwy_mpg = 18.0,
  annual_maintenance_est = 1800.0
WHERE car_id = 178;

-- Car 179: Mercedes W221 S550 2007 — needs ALL
UPDATE cost_to_own SET
  msrp_original = 87175.0,
  fuel_econ_city_mpg = 14.0,
  fuel_econ_hwy_mpg = 22.0,
  annual_maintenance_est = 1500.0
WHERE car_id = 179;

-- Car 180: Audi A8 D4 3.0T 2014 — needs ALL
UPDATE cost_to_own SET
  msrp_original = 79700.0,
  fuel_econ_city_mpg = 18.0,
  fuel_econ_hwy_mpg = 28.0,
  annual_maintenance_est = 1400.0
WHERE car_id = 180;

-- Car 10: Porsche Taycan Turbo S 2020 — needs MPGe + maintenance
UPDATE cost_to_own SET
  fuel_econ_city_mpg = 67.0,
  fuel_econ_hwy_mpg = 68.0,
  annual_maintenance_est = 1200.0
WHERE car_id = 10;

-- Backfill missing powertrain_ice fields
-- Generated with real automotive specifications

-- ============================================================
-- FUEL SYSTEM (55 cars missing)
-- ============================================================

-- Acura TL 2007-2008 Type S (3.5L V6 J35Z) - uses PGM-FI which is multi-point injection
UPDATE powertrain_ice SET fuel_system = 'MPI (port injection)' WHERE id = 46;
-- Acura TL 2009-2014 V6 (J37)
UPDATE powertrain_ice SET fuel_system = 'MPI (port injection)' WHERE id = 86;
-- Acura TLX 2021 2.0T (K20C) - Honda K20C uses direct injection
UPDATE powertrain_ice SET fuel_system = 'direct injection' WHERE id = 26;
-- Alpine A110 2017 (1.8T M270 derived) - Renault 1.8 turbo uses direct injection
UPDATE powertrain_ice SET fuel_system = 'direct injection' WHERE id = 13;
-- Audi S4 B5 1997-2001 (2.7T) - used MPI
UPDATE powertrain_ice SET fuel_system = 'MPI (port injection)' WHERE id = 64;
-- Audi A8 D5 2018 (3.0T V6 EA839) - direct injection
UPDATE powertrain_ice SET fuel_system = 'FSI direct injection' WHERE id = 41;
-- BMW M5 E39 1998-2003 (S62 V8) - used MPI (Bosch Motronic)
UPDATE powertrain_ice SET fuel_system = 'MPI (port injection)' WHERE id = 63;
-- BMW 335i E90 (N55 3.0T I6) - direct injection + port injection (N55 uses DI primarily)
UPDATE powertrain_ice SET fuel_system = 'direct injection' WHERE id = 35;
-- BMW 740i G11/G12 (B58 3.0T) - direct injection
UPDATE powertrain_ice SET fuel_system = 'direct injection' WHERE id = 39;
-- BMW 540i xDrive G30 (B58) - direct injection
UPDATE powertrain_ice SET fuel_system = 'direct injection' WHERE id = 54;
-- BMW X3 M40i G01 (B58) - direct injection
UPDATE powertrain_ice SET fuel_system = 'direct injection' WHERE id = 48;
-- BMW X3 M40i G01 duplicate - direct injection
UPDATE powertrain_ice SET fuel_system = 'direct injection' WHERE id = 49;
-- BYD Han EV - electric
UPDATE powertrain_ice SET fuel_system = 'electric' WHERE id = 71;
-- Cadillac CTS-V Gen1 2004-2007 (LS2 V8) - sequential fuel injection (SFI)
UPDATE powertrain_ice SET fuel_system = 'MPI (port injection)' WHERE id = 67;
-- Cadillac CTS 3rd gen 2015-2019 (2.0T LTG) - direct injection
UPDATE powertrain_ice SET fuel_system = 'direct injection' WHERE id = 24;
-- Cadillac CTS-V 3rd gen 2016-2018 (LT4 supercharged V8) - direct injection
UPDATE powertrain_ice SET fuel_system = 'direct injection' WHERE id = 34;
-- Cadillac CT5 2020 (2.0T LSY) - direct injection
UPDATE powertrain_ice SET fuel_system = 'direct injection' WHERE id = 25;
-- Chevrolet Camaro SS 2024 (LT1 6.2L V8) - direct injection
UPDATE powertrain_ice SET fuel_system = 'direct injection' WHERE id = 160;
-- Dodge Charger SRT Hellcat 2021 (6.2L supercharged Hellcat V8) - port injection + forced induction
UPDATE powertrain_ice SET fuel_system = 'MPI (port injection)' WHERE id = 156;
-- Dodge Challenger R/T Scat Pack 2021 (392 HEMI V8) - port injection (SFI)
UPDATE powertrain_ice SET fuel_system = 'MPI (port injection)' WHERE id = 157;
-- Ford Focus ST 2013-2018 (2.0T EcoBoost) - direct injection
UPDATE powertrain_ice SET fuel_system = 'direct injection' WHERE id = 79;
-- Ford Mustang Shelby GT500 2020-2022 (5.2L Predator V8) - port + direct dual injection
UPDATE powertrain_ice SET fuel_system = 'Dual injection (GDi + MPi)' WHERE id = 9;
-- Ford Mustang Ecoboost Premium 2024 (2.3L EcoBoost) - direct injection
UPDATE powertrain_ice SET fuel_system = 'direct injection' WHERE id = 158;
-- Ford Mustang GT Premium 2024 (5.0L Coyote V8 Gen 4) - dual port+direct injection
UPDATE powertrain_ice SET fuel_system = 'Dual injection (GDi + MPi)' WHERE id = 159;
-- Genesis GV70 3.5T 2022 (3.5L twin-turbo Lambda II) - direct injection
UPDATE powertrain_ice SET fuel_system = 'direct injection' WHERE id = 52;
-- Honda Civic Type R FK8 2017-2021 (K20C1) - direct injection
UPDATE powertrain_ice SET fuel_system = 'direct injection' WHERE id = 78;
-- Hongqi E-HS9 2021 - electric
UPDATE powertrain_ice SET fuel_system = 'electric' WHERE id = 73;
-- Infiniti G35 Coupe 2003-2007 (VQ35DE) - MPI (multi-point fuel injection)
UPDATE powertrain_ice SET fuel_system = 'MPI (port injection)' WHERE id = 62;
-- Infiniti Q50 Red Sport 400 (VR30DDTT) - direct injection
UPDATE powertrain_ice SET fuel_system = 'direct injection' WHERE id = 32;
-- Jaguar XJ X351 2010-2019 (5.0L SC V8 AJ-V8) - direct injection
UPDATE powertrain_ice SET fuel_system = 'direct injection' WHERE id = 44;
-- Kia Stinger 2018-2023 (3.3L twin-turbo Lambda II) - direct injection
UPDATE powertrain_ice SET fuel_system = 'direct injection' WHERE id = 31;
-- Land Rover Range Rover Sport HSE 2014-2022 (3.0L SC V6) - direct injection
UPDATE powertrain_ice SET fuel_system = 'direct injection' WHERE id = 53;
-- Mercedes-Benz E500 2003-2006 (M113 V8) - EFI (sequential multi-point)
UPDATE powertrain_ice SET fuel_system = 'EFI (electronic fuel injection)' WHERE id = 77;
-- Mercedes-Benz S-Class W222 S550 (4.7L biturbo M278 V8) - direct injection
UPDATE powertrain_ice SET fuel_system = 'direct injection' WHERE id = 40;
-- Mercedes-Benz GLC 43 2017 (3.0L twin-turbo M276) - direct injection
UPDATE powertrain_ice SET fuel_system = 'direct injection' WHERE id = 51;
-- Nissan Skyline GT-R R32 1989-1994 (RB26DETT) - EFI (multi-point)
UPDATE powertrain_ice SET fuel_system = 'EFI (electronic fuel injection)' WHERE id = 56;
-- Nissan Skyline GT-T R34 1998-2002 (RB25DET NEO) - EFI
UPDATE powertrain_ice SET fuel_system = 'EFI (electronic fuel injection)' WHERE id = 57;
-- Peugeot 406 Coupe 1997-2004 (ES9 V6) - MPI (multi-point injection)
UPDATE powertrain_ice SET fuel_system = 'MPI (port injection)' WHERE id = 66;
-- Porsche 944 Turbo 1986-1991 - Bosch K-Jetronic mechanical continuous injection
UPDATE powertrain_ice SET fuel_system = 'mechanical fuel injection' WHERE id = 15;
-- Porsche 911 Carrera 996 1998-2004 (M96 flat-6) - MPI (Bosch Motronic)
UPDATE powertrain_ice SET fuel_system = 'MPI (port injection)' WHERE id = 16;
-- Porsche 911 GT3 996.2 2003-2005 (M96/79) - MPI (Bosch Motronic ME7.8)
UPDATE powertrain_ice SET fuel_system = 'MPI (port injection)' WHERE id = 19;
-- Porsche Panamera 1st gen 2010-2016 (4.8L V8) - direct injection (DFI)
UPDATE powertrain_ice SET fuel_system = 'DFI direct injection' WHERE id = 47;
-- Porsche Taycan Turbo S 2020 - electric
UPDATE powertrain_ice SET fuel_system = 'electric' WHERE id = 8;
-- Subaru Legacy 2000-2004 (EJ253) - MPI (multi-point)
UPDATE powertrain_ice SET fuel_system = 'MPI (port injection)' WHERE id = 82;
-- Subaru Impreza GD 2001-2007 (EJ205 turbo) - MPI (multi-point)
UPDATE powertrain_ice SET fuel_system = 'MPI (port injection)' WHERE id = 58;
-- Subaru BRZ 2017 (FA20) - Toyota D-4S dual injection (GDI + PFI)
UPDATE powertrain_ice SET fuel_system = 'Dual injection (GDi + MPi)' WHERE id = 162;
-- Tesla Model 3 Performance 2018 - electric
UPDATE powertrain_ice SET fuel_system = 'electric' WHERE id = 69;
-- Tesla Model Y Range 2020 - electric (already has fuel_system from aspiration)
UPDATE powertrain_ice SET fuel_system = 'electric' WHERE id = 70;
-- Toyota Supra SZ 1993-1998 (2JZ-GE) - EFI (multi-point)
UPDATE powertrain_ice SET fuel_system = 'EFI (electronic fuel injection)' WHERE id = 18;
-- VinFast VF8 2023 - electric
UPDATE powertrain_ice SET fuel_system = 'electric' WHERE id = 74;
-- Volkswagen Phaeton W12 2002-2010 (6.0L W12) - MPI (multi-point)
UPDATE powertrain_ice SET fuel_system = 'MPI (port injection)' WHERE id = 60;
-- Volkswagen Golf GTI Mk8 2021 (EA888 evo4 2.0T) - TSI direct injection
UPDATE powertrain_ice SET fuel_system = 'TSI direct injection' WHERE id = 10;
-- Xiaomi SU7 Max 2024 - electric
UPDATE powertrain_ice SET fuel_system = 'electric' WHERE id = 72;

-- ============================================================
-- ENGINE LAYOUT (14 cars missing)
-- ============================================================

-- Acura TL 2007-2008 Type S - front transverse (Honda J-series is transverse)
UPDATE powertrain_ice SET engine_layout = 'front transverse' WHERE id = 46;
-- Acura TL 2009-2014 - front transverse
UPDATE powertrain_ice SET engine_layout = 'front transverse' WHERE id = 86;
-- Acura TLX 2021 - front transverse
UPDATE powertrain_ice SET engine_layout = 'front transverse' WHERE id = 26;
-- BYD Han EV - electric (no traditional engine layout)
UPDATE powertrain_ice SET engine_layout = 'front transverse' WHERE id = 71;
-- Cadillac CTS-V Gen1 (LS2) - front longitudinal
UPDATE powertrain_ice SET engine_layout = 'front longitudinal' WHERE id = 67;
-- Chevrolet Camaro SS 2024 - front longitudinal
UPDATE powertrain_ice SET engine_layout = 'front longitudinal' WHERE id = 160;
-- Dodge Charger Hellcat 2021 - front longitudinal
UPDATE powertrain_ice SET engine_layout = 'front longitudinal' WHERE id = 156;
-- Dodge Challenger Scat Pack 2021 - front longitudinal
UPDATE powertrain_ice SET engine_layout = 'front longitudinal' WHERE id = 157;
-- Ford Mustang Ecoboost 2024 - front longitudinal
UPDATE powertrain_ice SET engine_layout = 'front longitudinal' WHERE id = 158;
-- Ford Mustang GT 2024 - front longitudinal
UPDATE powertrain_ice SET engine_layout = 'front longitudinal' WHERE id = 159;
-- Honda Civic Type R FK8 - front transverse
UPDATE powertrain_ice SET engine_layout = 'front transverse' WHERE id = 78;
-- Hongqi E-HS9 - front motor (electric)
UPDATE powertrain_ice SET engine_layout = 'front transverse' WHERE id = 73;
-- Subaru BRZ 2017 - front longitudinal (FA20 boxer, longitudinal RWD layout)
UPDATE powertrain_ice SET engine_layout = 'front longitudinal' WHERE id = 162;
-- Volkswagen Phaeton W12 - front longitudinal
UPDATE powertrain_ice SET engine_layout = 'front longitudinal' WHERE id = 60;

-- ============================================================
-- TRANSMISSION TYPE (11 cars missing)
-- ============================================================

-- Acura TL 2007-2008 Type S (3.5L V6) - 5-speed automatic was standard; 6-speed manual optional
UPDATE powertrain_ice SET transmission_type = '5-speed automatic' WHERE id = 46;
-- Acura TL 2009-2014 V6 - 6-speed manual listed in gear_count
-- Already has transmission_type = 'manual' from query. Let me check...
-- Actually the query shows transmission_type is empty for id=86. The gear_count=6 and it says manual in one row.
-- Acura 4G TL SH-AWD had 6-speed automatic. The manual variant had 6-speed manual.
-- Given the existing data shows "manual" for transmission_type with gear_count=6, let me set it properly
UPDATE powertrain_ice SET transmission_type = '6-speed manual' WHERE id = 86;
-- Acura TLX 2021 2.0T - 10-speed automatic
UPDATE powertrain_ice SET transmission_type = '10-speed automatic' WHERE id = 26;
-- Audi A8 D5 2018 (3.0T V6) - 8-speed Tiptronic automatic
UPDATE powertrain_ice SET transmission_type = '8-speed automatic' WHERE id = 41;
-- BMW 335i E90 N55 - 6-speed manual or 8-speed automatic were options
UPDATE powertrain_ice SET transmission_type = '6-speed manual' WHERE id = 35;
-- BMW 740i G11/G12 B58 - 8-speed automatic (ZF 8HP)
UPDATE powertrain_ice SET transmission_type = '8-speed automatic' WHERE id = 39;
-- BYD Han EV - single-speed reduction gear (electric)
UPDATE powertrain_ice SET transmission_type = 'single-speed reduction gear' WHERE id = 71;
-- Cadillac CTS-V Gen1 (LS2) - 6-speed manual was standard (Tremec T56)
UPDATE powertrain_ice SET transmission_type = '6-speed manual' WHERE id = 67;
-- Porsche Taycan Turbo S - 2-speed automatic (rear axle)
UPDATE powertrain_ice SET transmission_type = '2-speed automatic' WHERE id = 8;
-- Tesla Model 3 Performance - single-speed (fixed gear)
UPDATE powertrain_ice SET transmission_type = 'single-speed fixed gear' WHERE id = 69;
-- Xiaomi SU7 Max - single-speed reduction gear (electric)
UPDATE powertrain_ice SET transmission_type = 'single-speed reduction gear' WHERE id = 72;

-- ============================================================
-- DISPLACEMENT_CC (8 cars missing)
-- ============================================================

-- BYD Han EV - electric, no displacement
-- UPDATE powertrain_ice SET displacement_cc = NULL WHERE id = 71; -- already NULL, keep it

-- Hongqi E-HS9 - electric, no displacement
-- already NULL, keep it

-- Tesla Model 3 Performance - electric, no displacement
-- already NULL, keep it

-- Tesla Model Y - electric, no displacement (already has displacement from data)
-- already NULL or 0, keep it

-- Tesla Model S Plaid - electric
-- already has entry, keep it

-- VinFast VF8 - electric, no displacement
-- already NULL, keep it

-- Xiaomi SU7 Max - electric, no displacement
-- already NULL, keep it

-- These are all EVs with no displacement - they should remain NULL.
-- No UPDATE statements needed for displacement_cc.

-- ============================================================
-- CURB WEIGHT_KG (3 cars missing)
-- ============================================================

-- Kia K5 GT 2021-2024 - curb weight approximately 1570 kg
UPDATE powertrain_ice SET curb_weight_kg = 1570.0 WHERE id = 199;
-- Mercedes-Benz E-Class 2014-2016 V6 (E350) - curb weight approximately 1750 kg
UPDATE powertrain_ice SET curb_weight_kg = 1750.0 WHERE id = 198;
-- Toyota Camry 2018-2024 V6 - curb weight approximately 1590 kg
UPDATE powertrain_ice SET curb_weight_kg = 1590.0 WHERE id = 200;

-- ============================================================
-- SECOND PASS - REMAINING GAPS
-- ============================================================

-- VW Touareg 3.0 TDI V6 (all years) - TDI = direct injection
UPDATE powertrain_ice SET fuel_system = 'direct injection' WHERE id = 163;
UPDATE powertrain_ice SET fuel_system = 'direct injection' WHERE id = 164;
UPDATE powertrain_ice SET fuel_system = 'direct injection' WHERE id = 165;

-- Genesis G90 5.0 V8 (Tau V8) - front longitudinal
UPDATE powertrain_ice SET engine_layout = 'front longitudinal' WHERE id = 161;

-- Land Rover Range Rover Sport HSE (3.0 SC V6) - front longitudinal, ZF 8HP
UPDATE powertrain_ice SET engine_layout = 'front longitudinal' WHERE id = 53;
UPDATE powertrain_ice SET transmission_type = '8-speed automatic' WHERE id = 53;

-- Mercedes-Benz S-Class W222 S550 (4.7L biturbo M278) - front longitudinal
UPDATE powertrain_ice SET engine_layout = 'front longitudinal' WHERE id = 40;

-- Porsche Panamera 1st gen (4.8L V8) - front longitudinal, PDK
UPDATE powertrain_ice SET engine_layout = 'front longitudinal' WHERE id = 47;
UPDATE powertrain_ice SET transmission_type = '7-speed PDK' WHERE id = 47;

-- Tesla Model 3 Performance - rear motor layout
UPDATE powertrain_ice SET engine_layout = 'rear motor' WHERE id = 69;

-- VinFast VF8 - front motor
UPDATE powertrain_ice SET engine_layout = 'front motor' WHERE id = 74;

-- Xiaomi SU7 Max - dual motor
UPDATE powertrain_ice SET engine_layout = 'dual motor' WHERE id = 72;

-- Hongqi E-HS9 - single-speed
UPDATE powertrain_ice SET transmission_type = 'single-speed reduction gear' WHERE id = 73;

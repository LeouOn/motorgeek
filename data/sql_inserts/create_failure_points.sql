-- Failure Points Database — structured reliability failure data
-- Extracted from 15+ hours of librarian research across 194 cars

CREATE TABLE IF NOT EXISTS failure_points (
    id INTEGER PRIMARY KEY,
    car_id INTEGER NOT NULL REFERENCES cars(id),
    failure_name VARCHAR(100) NOT NULL,
    component VARCHAR(50) NOT NULL DEFAULT 'engine',  -- engine, transmission, chassis, electronics, suspension, body
    severity INTEGER NOT NULL DEFAULT 3,  -- 1=cosmetic, 2=nuisance, 3=moderate, 4=major, 5=catastrophic
    typical_mileage_mi INTEGER,           -- approximate mileage when failure occurs
    repair_cost_low FLOAT,                -- USD
    repair_cost_high FLOAT,               -- USD
    is_preventive BOOLEAN DEFAULT 0,      -- can this failure be prevented?
    prevention_cost FLOAT,               -- cost of prevention (USD)
    prevention_desc TEXT,                 -- how to prevent
    description TEXT,                     -- detailed failure description
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for fast queries
CREATE INDEX IF NOT EXISTS idx_fp_car ON failure_points(car_id);
CREATE INDEX IF NOT EXISTS idx_fp_component ON failure_points(component);
CREATE INDEX IF NOT EXISTS idx_fp_severity ON failure_points(severity);
CREATE INDEX IF NOT EXISTS idx_fp_preventive ON failure_points(is_preventive);

-- ============================================================================
-- LEXUS LS430 (car_id=39) — 3 key failures
-- ============================================================================
INSERT INTO failure_points (car_id, failure_name, component, severity, typical_mileage_mi, repair_cost_low, repair_cost_high, is_preventive, prevention_cost, prevention_desc, description) VALUES
(39, 'timing_belt_service', 'engine', 5, 90000, 800, 1200, 1, 800, 'Replace timing belt at 90K mi intervals. Non-negotiable — interference engine.', '3UZ-FE uses timing belt (not chain). Must replace every 90K mi. Interference engine — belt failure = bent valves. $800-1200 at shop, $300 DIY.'),
(39, 'air_suspension_ul', 'suspension', 4, 100000, 6000, 8000, 1, 1500, 'Coil spring conversion (RS-R T284D). Only affects Ultra Luxury trim.', 'Ultra Luxury Package has full 4-corner air suspension. Air bags crack at 100K+. OEM replacement $6-8K. Coil conversion $1,500 all-in. Custom Luxury trim has coil springs — no issue.'),
(39, 'valve_cover_gasket', 'engine', 2, 120000, 400, 600, 0, NULL, NULL, 'Minor oil seepage from valve cover gaskets. Common at 120K+. $400-600 shop. Not catastrophic.'),

-- ============================================================================
-- LEXUS LS400 (car_id=63) — 2 key failures
-- ============================================================================
(63, 'ecu_capacitor_leak', 'electronics', 4, 180000, 200, 400, 1, 200, 'ECU capacitor recap kit. Install proactively if car sat unused.', 'ECU capacitors leak after 15-20 years, especially in cars that sat unused. Symptoms: rough idle, stalling, erratic behavior. Fix: $200-400 recap kit. Keeping prices down on otherwise bulletproof car.'),
(63, 'timing_belt_service', 'engine', 5, 90000, 800, 1200, 1, 800, 'Replace timing belt at 90K mi intervals. Same as LS430.', '1UZ-FE timing belt service. Interference engine. $800-1200.'),

-- ============================================================================
-- MERCEDES W126 560SEL (car_id=178) — 3 key failures
-- ============================================================================
(178, 'rust_structural', 'body', 5, 200000, 1000, 5000, 0, NULL, NULL, 'The W126 killer. Rockers, wheel arches, jack points, trunk floor. Post-1986 galvanizing helps. Pre-facelift cars worse. Must inspect before purchase — structural rust is existential.'),
(178, 'timing_chain_single_row', 'engine', 5, 100000, 800, 1500, 1, 800, 'Preventive timing chain replacement at 100K mi.', 'M117 uses single-row timing chain known to stretch and skip at 100K+. Preventive replacement prevents engine destruction. $800-1500.'),
(178, 'hydropneumatic_spheres', 'suspension', 3, 100000, 200, 400, 0, NULL, NULL, 'Rear self-leveling nitrogen spheres lose pressure at 80-120K mi. Car sits low, harsh ride. $200-400 each + labor. Not catastrophic but degrades ride quality.'),

-- ============================================================================
-- AUDI A8 D5 FACELIFT (car_id=43) — 4 key failures
-- ============================================================================
(43, 'ea839_piston_ringland', 'engine', 4, 80000, 3000, 8000, 0, NULL, NULL, 'EA839 3.0T V6 piston ringland fracture risk. 034Motorsport documented stress risers at oil drain holes. 3 piston revisions exist. A8 340hp tune is milder than S4/SQ5 — reduces stress. Failure rate <5% but real.'),
(43, 'air_suspension_struts', 'suspension', 4, 90000, 800, 2000, 0, NULL, NULL, 'Adaptive air suspension struts crack at 80-100K mi. $800-2000 per corner. Compressor $700-1200. Standard air suspension (not predictive active) shares compressor/valve block with Q7/Cayenne.'),
(43, 'bsg_48v_failure', 'electronics', 3, 80000, 1500, 3000, 0, NULL, NULL, '48V Belt Starter Generator failure. TSB 27-23-55, campaign 27BQ. Shared with A6/A7/Q7/Q8. Rebuild market exists ($200-800 vs Audi $1500-2500). Audi extended warranty to ~10 years.'),
(43, 'timing_chain_tensioner', 'engine', 3, 100000, 4000, 8000, 0, NULL, NULL, 'EA839 rear-mounted timing chain tensioner. Cam roller issue resolved pre-2018. Piston risk remains. Engine pull required for full service. $4-8K.'),

-- ============================================================================
-- AUDI A8 D5 2017 (car_id=22) — same as facelift minus MIB3
-- ============================================================================
(22, 'ea839_cam_roller', 'engine', 4, 60000, 3000, 6000, 1, 0, 'Buy 2019+ production — cam roller resolved pre-06/08/2018.', 'Early EA839 (pre-June 2018) has undersized needle bearings in roller rockers. Can fail, releasing needles into engine. Resolved part 0P2109417 from Aug 2018. 2017 model at risk.'),
(22, 'air_suspension_struts', 'suspension', 4, 90000, 800, 2000, 0, NULL, NULL, 'Same as D5 facelift. Air struts at 80-100K mi.'),
(22, 'bsg_48v_failure', 'electronics', 3, 80000, 1500, 3000, 0, NULL, NULL, 'Same BSG issue as facelift. TSB 27-23-55 applies.'),

-- ============================================================================
-- CHEVY SS LS3 6MT (car_id=170) — 3 key failures
-- ============================================================================
(170, 'ls3_water_pump', 'engine', 3, 80000, 300, 600, 1, 300, 'Replace water pump preventively at 80K mi.', 'LS3 water pump failure 60-100K mi. Most commonly reported LS3 issue. $300-600. Not catastrophic if caught — just overheating. Replace preventively.'),
(170, 'eps_connector_recall', 'electronics', 4, 60000, 0, 0, 1, 0, 'Verify NHTSA recall 17V-382 completed. Free dealer fix.', 'Electric Power Steering connector fretting corrosion causes loss of power steering while driving. NHTSA 17V-382. 2014-2016 affected. 2017 NOT included despite reports. Free dealer fix — gold-plated terminals.'),
(170, 'mylink_touchscreen', 'electronics', 2, 80000, 200, 400, 0, NULL, NULL, 'Chevy MyLink 8-inch touchscreen digitizer degradation. Ghost touch, dead zones, delamination. DIY digitizer replacement $200-400. Underlying infotainment module is fine.'),

-- ============================================================================
-- MERCEDES 500E (car_id=7) — 2 key failures
-- ============================================================================
(7, 'wiring_harness_degradation', 'electronics', 4, 150000, 1500, 3000, 0, NULL, NULL, 'Biodegradable wiring harness insulation (1990-1995 Mercedes era). Crumbles with age. Engine harness $1500-3000. Check insulation flexibility before purchase.'),
(7, 'timing_chain_v8', 'engine', 4, 100000, 2000, 4000, 0, NULL, NULL, 'M119 5.0L V8 timing chain guide rails. Plastic guides degrade. Preemptive replacement at 100K mi. $2-4K. Not as urgent as M62 but still important.'),

-- ============================================================================
-- BMW 740i B58 (car_id=164) — 3 key failures
-- ============================================================================
(164, 'b58_ofhg', 'engine', 3, 80000, 500, 700, 1, 80, 'Replace OFHG gasket at first sign of weep. DIY $80.', 'B58 Oil Filter Housing Gasket leak at 60-90K. CRITICAL: leaking oil on serpentine belt can cause belt to slip into crank seal, destroying engine. Do not ignore. $500-700 shop.'),
(164, 'b58_water_pump', 'engine', 3, 80000, 600, 800, 1, 600, 'Replace electric water pump preventively at 80-100K mi.', 'B58 electric water pump fails without warning at 70-100K. No serpentine belt drive. Sudden overheating triggers limp mode. $600-800. Replace with thermostat (labor overlaps).'),
(164, 'b58_pcv_valve', 'engine', 2, 90000, 400, 600, 0, NULL, NULL, 'B58 PCV valve diaphragm failure. Rough idle, unmetered air. SIB extended warranty on some. Age-related, not design flaw.'),

-- ============================================================================
-- BMW E38 740i (car_id=176) — 3 key failures
-- ============================================================================
(176, 'm62_timing_chain_guides', 'engine', 5, 100000, 3000, 6000, 1, 3000, 'Preemptive timing chain guide replacement at 80-100K mi. Verify service history before purchase.', 'THE E38 killer. M62 plastic timing chain guides degrade and fail. Chain jumps = engine destruction. $3-6K. Pre-buy inspection mandatory. Must verify done or budget immediately.'),
(176, 'm62_valve_stem_seals', 'engine', 3, 120000, 2000, 3500, 0, NULL, NULL, 'Blue smoke on cold start, oil consumption. Valve stem seals harden with age. $2-3.5K. Not catastrophic but annoying and progressive.'),
(176, 'cooling_system_plastic', 'engine', 3, 80000, 800, 1500, 1, 800, 'Preventive cooling system refresh: radiator, expansion tank, water pump, thermostat at 80K.', 'M62 cooling system is all plastic — radiator, expansion tank, water pump, thermostat housing. All fail at 60-100K. Preventive refresh $800-1500. Ignore = overheating = head gasket.'),

-- ============================================================================
-- BMW E90 328i N52 (car_id=37) — 4 key failures
-- ============================================================================
(37, 'n52_valve_cover_gasket', 'engine', 3, 90000, 400, 600, 0, NULL, NULL, 'Most common N52 issue. Oil weep from VCG at 60-120K. Post-2007 plastic covers crack. $400-600 shop, $150 DIY.'),
(37, 'n52_electric_water_pump', 'engine', 4, 80000, 600, 800, 1, 600, 'Replace preventively at 80-100K mi WITH thermostat.', 'Fails WITHOUT WARNING at 60-100K. No serpentine belt. Sudden overheating, limp mode. $600-800. Replace thermostat at same time (labor overlaps). Most important preventive item on N52.'),
(37, 'n52_ofhg', 'engine', 3, 90000, 500, 700, 1, 80, 'Replace OFHG at first sign of leak. DIY $80.', 'Oil Filter Housing Gasket leaks at 60-120K. CRITICAL: oil on serpentine belt = belt into crank seal = engine death. $500-700 shop, $80 DIY.'),
(37, 'n52_hydraulic_lifter_tick', 'engine', 2, 90000, 2000, 3000, 0, NULL, NULL, 'Pre-November 2008 N52 engines prone to cold-start ticking. Post-Nov 2008 resolved with improved lifters. Requires camshaft removal for full fix. $2-3K.'),

-- ============================================================================
-- MERCEDES W222 PRE-FACELIFT S550 M278 (car_id=42) — 4 key failures
-- ============================================================================
(42, 'm278_cam_sensor_ecu', 'electronics', 5, 90000, 100, 5000, 1, 100, 'Install sacrificial cam sensor pigtails ($100). FIRST THING on any M278.', 'THE #1 S550 KILLER. Oil wicks from cam sensors through wiring harness into ECU. Random misfires, O2 codes, transmission issues. $100 pigtail fix prevents $5K+ ECU death. CHECK ALL 4 CONNECTORS at PPI.'),
(42, 'm278_oil_cooler_leak', 'engine', 4, 90000, 1500, 3000, 0, NULL, NULL, 'Oil filter housing/oil cooler leaks cause oil+coolant mix at 80K+. $1500-3000 indie. Pressure test at PPI. Part of every pre-purchase checklist.'),
(42, 'w222_airmatic_struts', 'suspension', 4, 90000, 500, 2500, 0, NULL, NULL, 'AIRMATIC struts crack at 80K+. Arnott rebuilt $500/corner. Dealer $1400/corner. Compressor burns out from overwork. $1200-2500 per corner. Can coil-convert (destroys ride quality).'),
(42, 'w222_aluminum_body_repair', 'body', 5, 0, 0, 0, 0, NULL, NULL, 'W222 is 50% aluminum hybrid bodyshell. MUST be repaired by Mercedes Elite Certified Collision Center — only ~10 in USA. Improper repair = galvanic corrosion, lost torsional rigidity. Accident history = walk away.'),

-- ============================================================================
-- MERCEDES W222 FACELIFT S560 M176 (car_id=181) — 3 key failures
-- ============================================================================
(181, 'm176_p06da00_oil_pump', 'engine', 5, 90000, 5500, 9500, 0, NULL, NULL, 'M176 defining failure. Oil pump solenoid inside oil pan. On 4MATIC, oil pan bolted to bell housing = engine+trans removal. $5500-9500. No prevention. The M176 version of the M278 cam sensor problem — but 55x more expensive to fix.'),
(181, 'm176_cyl_deactivation_lifters', 'engine', 3, 100000, 5000, 7500, 0, NULL, NULL, 'Cylinder deactivation lifters (cylinders 2,3,5,8) fail causing rough idle and ticking. Up to $7500. Same VCM-style problem as Honda but more expensive.'),
(181, 'm176_valve_cover_gasket', 'engine', 3, 80000, 1500, 3000, 0, NULL, NULL, 'Front end of car must be removed for valve cover gasket service. Hot-V turbo layout makes access terrible. $1500-3000.'),

-- ============================================================================
-- CHRYSLER PACIFICA (car_id=195) — 2 key failures
-- ============================================================================
(195, 'pentastar_oil_cooler', 'engine', 4, 80000, 1000, 1500, 1, 300, 'Replace plastic oil cooler with aluminum aftermarket preemptively.', 'Plastic oil cooler/filter housing cracks at 60-100K. Near-universal. $1000-1500 OEM. Aluminum aftermarket ~$300 fixes permanently. Near-universal on Pentastar V6.'),
(195, 'zf_9speed_valve_body', 'transmission', 4, 80000, 2000, 3000, 0, NULL, NULL, 'ZF 948TE 9-speed: rough shifts, hesitation, valve body failure. Problematic in every vehicle installed. Software reflashes partial fix. Valve body $2-3K. Full rebuild $4K+.'),

-- ============================================================================
-- CHRYSLER PACIFICA PHEV (car_id=196) — 1 key failure
-- ============================================================================
(196, 'phev_battery_replacement', 'electronics', 5, 100000, 7000, 17000, 0, NULL, NULL, 'PHEV HV battery replacement $7,000-17,000. Only 8yr/100k warranty (NOT 10yr like Toyota). Battery bricked failures reported at under 9K miles. One out-of-warranty failure = total loss scenario for most owners.'),

-- ============================================================================
-- HONDA ODYSSEY (car_id=194) — 2 key failures
-- ============================================================================
(194, 'vcm_mount_oil_consumption', 'engine', 4, 100000, 400, 1500, 1, 130, 'Install VCMuzzler II / S-VCM controller ($130). Disables VCM, prevents mount wear and oil consumption.', 'VCM (Variable Cylinder Management) causes active engine mount failure every 50K mi ($800-1200/set), oil consumption from piston ring wear, spark plug fouling. VCMuzzler II $130 disables VCM. 2013 class action covered 1.6M vehicles.'),
(194, 'honda_9speed_zf', 'transmission', 3, 60000, 800, 1500, 0, NULL, NULL, '2018-2019 EX-L and below got ZF 9HP 9-speed. Hesitation, rough shifts, lurching. 2020+ all trims got Honda 10-speed (much better). Push-button park recall.'),

-- ============================================================================
-- TOYOTA TUNDRA 5.7L (car_id=200) — 2 key failures
-- ============================================================================
(200, 'tundra_air_pump', 'electronics', 4, 80000, 200, 3500, 1, 200, 'Install HewittTech AIR pump bypass kit ($200-400 DIY). Prevents $2500-3500 dealer bill.', 'Air Injection Pump (AIR) failure — P0410, loud vacuum noise on cold start. Affects 2007-2021. Dealer $2500-3500. HewittTech bypass kit $200-400 DIY. Install preemptively.'),
(200, 'tundra_water_pump', 'engine', 2, 80000, 400, 800, 0, NULL, NULL, '3UR-FE water pump at 60-100K mi. $400-800. Cheap and easy. Not catastrophic — just coolant leak.'),

-- ============================================================================
-- TOYOTA 4RUNNER (car_id=198) — 2 key failures
-- ============================================================================
(198, 'lower_ball_joints', 'chassis', 5, 100000, 1400, 1400, 1, 1400, 'Preemptive lower ball joint replacement at 100K mi. Failure is catastrophic.', 'Lower ball joint failure = wheel collapses. Catastrophic. Preemptive replacement at 100K mi. $1400 OEM for all 4. Non-negotiable on 100K+ mi 4Runner.'),
(198, 'rear_axle_seal', 'chassis', 3, 100000, 300, 600, 0, NULL, NULL, 'Rear axle seal leaks contaminate rear brakes. $300-600. Common at 100K+ mi. Inspect during tire rotations.'),

-- ============================================================================
-- LEXUS RX350 (car_id=199) — 2 key failures
-- ============================================================================
(199, 'melting_dashboard', 'interior', 2, 120000, 1500, 2500, 0, NULL, NULL, 'Sticky/melting dashboard and door panels 2010-2015. Infamous. Some Lexus warranty programs on other models but RX350 dash generally NOT covered. $1500-2500 replacement.'),
(199, 'vvt_oil_control_valve', 'engine', 3, 120000, 40, 120, 0, NULL, NULL, 'VVT oil control valve failure (P0014/P0012 codes). $40-120 part + labor. 2GR-FE shared issue across all Toyota V6 cars.'),

-- ============================================================================
-- SUBARU LEGACY GT EJ255 (car_id=188) — 2 key failures
-- ============================================================================
(188, 'ej255_banjo_bolt_filter', 'engine', 4, 80000, 1200, 2000, 1, 0, 'Remove banjo bolt filters in AVCS oil lines (2005-2006). Free DIY.', 'Banjo bolt filters in AVCS oil lines clog and starve turbo of oil = turbo failure. Pre-emptive removal is standard practice. 2005-2006 specific. Free DIY.'),
(188, 'ej255_head_gasket', 'engine', 3, 120000, 1500, 2000, 0, NULL, NULL, 'EJ255 turbo HG less severe than NA EJ251 (stiffer heads, MLS gasket). External leak, not internal. $1500-2000. Monitor coolant level.'),

-- ============================================================================
-- SUBARU LEGACY EJ22 (car_id=189) — 1 key failure
-- ============================================================================
(189, 'rust_body', 'body', 5, 200000, 0, 0, 0, NULL, NULL, 'Subaru thin paint + 30-year-old car. Rust is existential — rockers, wheel arches, floor pans. Engine (EJ22) will outlast the body. Find rust-free example or accept it as a parts car eventually.'),

-- ============================================================================
-- HONDA ACCORD 1.5T (car_id not individual but document the issue)
-- Using car_id=185 (Accord 2.0T) as reference for the 1.5T issue documentation
-- ============================================================================
(185, 'k20c4_oil_control_rings', 'engine', 3, 80000, 400, 800, 0, NULL, NULL, 'K20C4 oil control ring sticking at 80K+ mi. Oil consumption slowly increases. Well-documented. Monitor oil level, change every 5K mi. Not catastrophic, just progressive.'),

-- ============================================================================
-- KIA CARNIVAL (car_id=197) — 1 key failure (too new for more data)
-- ============================================================================
(197, 'lambda_coolant_loss', 'engine', 3, 60000, 200, 500, 0, NULL, NULL, 'Coolant loss emerging pattern on Lambda II 3.5L Smartstream. Top up once/twice yearly. Root cause TBD. Not catastrophic but monitor. Too new for definitive 200K+ mi data.');


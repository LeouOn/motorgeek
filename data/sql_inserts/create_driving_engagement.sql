-- Driving Engagement Score (DES) — 6 dimensions capturing driving joy
-- Each dimension scored 0-10. DES = average. EPD = DES * 100 / price_K.

CREATE TABLE IF NOT EXISTS driving_engagement (
    id INTEGER PRIMARY KEY,
    car_id INTEGER NOT NULL REFERENCES cars(id),
    steering_feel FLOAT,           -- 0-10: communication, feedback, precision
    chassis_balance FLOAT,         -- 0-10: adjustability, drivetrain layout, rotation
    transmission_engagement FLOAT, -- 0-10: manual > DCT > auto. clutch/shifter quality
    powertrain_character FLOAT,    -- 0-10: NA > turbo. sound, response, rev range
    lightness_agility FLOAT,       -- 0-10: lower weight = more responsive
    limit_accessibility FLOAT,     -- 0-10: can you reach 8/10ths safely on public roads?
    des_score FLOAT,               -- average of 6 dimensions (0-10 scale)
    des_notes TEXT,
    source VARCHAR(100) DEFAULT 'manual',
    UNIQUE(car_id)
);

CREATE INDEX IF NOT EXISTS idx_des_car ON driving_engagement(car_id);
CREATE INDEX IF NOT EXISTS idx_des_score ON driving_engagement(des_score);

-- Score the cars we've discussed, using current market prices for EPD

INSERT INTO driving_engagement (car_id, steering_feel, chassis_balance, transmission_engagement, powertrain_character, lightness_agility, limit_accessibility, des_score, des_notes, source) VALUES

-- E90 328i N52 6MT — the benchmark
(37, 9.0, 9.0, 9.0, 9.0, 7.0, 8.0, 8.5,
'Hydraulic steering. 50:50 RWD. NA I6 to 7000rpm. 6MT. 230hp limits accessible. The last pure BMW sedan.',
'manual+analysis'),

-- Mazda3 2.5 Skyactiv 6MT — the sensible fun car
(187, 7.0, 6.0, 7.0, 7.0, 8.0, 8.0, 7.2,
'Good EPAS for the era. FWD but well-sorted. 6MT is precise. NA I4 revs freely. 1320kg very light. 184hp limits very accessible.',
'manual+analysis'),

-- Subaru Legacy EJ22 — the momentum car
(189, 6.0, 6.0, 7.0, 5.0, 8.0, 9.0, 6.8,
'Boxer steering has character. AWD balance. 5MT robust. EJ22 NA but slow — rev it to redline. 1340kg light. 137hp = ALL limits reachable. Slow car fast = maximum engagement.',
'manual+analysis'),

-- Chevy SS LS3 6MT — the V8 hammer
(170, 7.0, 8.0, 7.0, 10.0, 5.0, 4.0, 6.8,
'Good steering. RWD Holden Zeta platform near 50:50. Tremec 6MT robust. LS3 NA V8 = best engine sound in database. 1805kg heavy. 415hp limits unreachable on public roads.',
'manual+analysis'),

-- Civic Type R FK8 — the hot hatch
(80, 7.0, 7.0, 8.0, 7.0, 7.0, 5.0, 6.8,
'Good EPAS despite FWD. LSD + adaptive dampers allow rotation. Best FWD 6MT. VTEC turbo aggressive. 1400kg OK. 306hp limits high but chassis communicative.',
'manual+analysis'),

-- WRX 2015 — the rally car
(93, 6.0, 7.0, 7.0, 7.0, 7.0, 6.0, 6.7,
'Decent steering through AWD. Adjustable with throttle. 5MT robust. Turbo boxer has character. 1470kg. 265hp fun but can get you in trouble.',
'manual+analysis'),

-- Accord 2.0T 6MT — the sleeper
(185, 6.0, 5.0, 8.0, 7.0, 5.0, 5.0, 6.0,
'Acceptable steering. FWD limits. K20C4 + 6MT = Type R-adjacent engagement. Turbo has lag. 1530kg heavy. 252hp moderate.',
'manual+analysis'),

-- LS430 — the sensory deprivation chamber
(39, 3.0, 2.0, 1.0, 5.0, 2.0, 2.0, 2.5,
'Over-assisted steering zero feedback. Soft wallowy chassis. Auto only. V8 smooth but silent. 1660kg heavy. 290hp but soft suspension = not fun at limit. Comfort car not driver car.',
'manual+analysis'),

-- Genesis G90 5.0 — the land yacht
(8, 3.0, 2.0, 1.0, 4.0, 1.0, 2.0, 2.2,
'Luxury-tuned EPAS. Soft air suspension. Auto only. V8 tuned for silence. 2150kg very heavy. 420hp unreachable safely. Barge not canyon carver.',
'manual+analysis'),

-- Hyundai Equus — same as G90
(394, 3.0, 2.0, 1.0, 4.0, 1.0, 2.0, 2.2,
'Same as G90. Land yacht. Beautiful inside but zero driving engagement.',
'manual+analysis'),

-- A8 D5 facelift — stealth Q-car but not a driver's car
(43, 4.0, 4.0, 1.0, 5.0, 3.0, 3.0, 3.3,
'Quattro AWD competent but numb. Air suspension isolates. Auto only. V6 refined but characterless. 1960kg heavy. Predictable but not engaging.',
'manual+analysis'),

-- BMW 540i xDrive — better than A8 but still a cruiser
(150, 5.0, 6.0, 2.0, 6.0, 4.0, 4.0, 4.5,
'Decent steering for EPS. RWD-based. Auto only (no manual in US). B58 turbo has lag but torquey. 1810kg. 335hp adequate but not exciting.',
'manual+analysis'),

-- Mazda MX-5 ND2 — the pure driving machine
(14, 8.0, 10.0, 9.0, 6.0, 10.0, 10.0, 8.8,
'Excellent steering. Perfect 50:50 RWD. 6MT sublime. 2.0L revs but slow. 1060kg featherweight. 181hp = every limit reachable. The definition of slow car fast.',
'manual+analysis'),

-- Subaru BRZ — the momentum RWD
(131, 8.0, 9.0, 8.0, 6.0, 9.0, 10.0, 8.3,
'Excellent steering. RWD designed for drifting. 6MT excellent. FA20 torque dip annoying but revs. 1240kg very light. 200hp = all limits always accessible.',
'manual+analysis'),

-- Golf GTI Mk8 — the benchmark hot hatch
(12, 6.0, 6.0, 6.0, 6.0, 7.0, 7.0, 6.3,
'Versatile steering. FWD competent. 6MT available but DSG more common. 2.0T generic. 1470kg. 241hp practical fun.',
'manual+analysis'),

-- Porsche 718 Cayman — the mid-engine benchmark
(104, 9.0, 10.0, 8.0, 7.0, 9.0, 7.0, 8.3,
'Porsche steering benchmark. Mid-engine perfection. 6MT or PDK. 2.0T flat-4 sounds bad (base model). 1355kg light. 300hp limits high but chassis communicates everything.',
'manual+analysis'),

-- Mercedes 500E — the 1990 Q-ship (not a canyon carver but has character)
(7, 4.0, 5.0, 1.0, 8.0, 4.0, 3.0, 4.2,
'1990s steering has some feel. Heavy but balanced. Auto only. M119 NA V8 sounds incredible. 1710kg. 322hp for the era but soft suspension.',
'manual+analysis'),

-- Toyota GR Supra 3.0 — the modern sports car
(118, 7.0, 8.0, 2.0, 7.0, 7.0, 5.0, 6.0,
'Good EPS. RWD balanced. Auto only in early years (manual added 2020+). B58 turbo torquey but generic sound. 1520kg. 382hp limits unreachable safely.',
'manual+analysis'),

-- Lexus ES 350 — the appliance
(86, 2.0, 2.0, 1.0, 4.0, 3.0, 4.0, 2.7,
'Numb steering. FWD floaty. CVT/auto only. V6 smooth but silent. 1620kg. 302hp but zero feedback. Transportation not driving.',
'manual+analysis'),

-- W126 560SEL — the classic land yacht (but with analog feel)
(178, 5.0, 4.0, 2.0, 7.0, 3.0, 3.0, 4.0,
'1980s recirculating ball has some feel. Heavy but RWD. 4-speed auto. M117 NA V8 sounds good. 1745kg. 238hp for the era. Analog character but not sporty.',
'manual+analysis');

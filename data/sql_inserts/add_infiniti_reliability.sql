-- ============================================================
-- Infiniti dimensional reliability inserts
-- G35 V35 Coupe (id 64) — backfill missing dimensions
-- Q50 Red Sport 400 (id 34) — full insert
-- ============================================================

-- 1) G35 V35 Coupe (2005-07 Rev-Up 6MT) — UPDATE existing row id=193
-- Already has: engine=85, trans=80. Backfill: chassis, electronics, ease, notes.
UPDATE reliability SET
    score_chassis = 75,
    score_electronics = 72,
    score_ease_of_repair = 88,
    common_failures = '["VQ35DE Rev-Up oil consumption (1qt/1-2K mi)","6MT 1-2 synchro grind","Subframe bushing cracking 60-80K","Door actuator failure","Bose amplifier failure","Window regulator failure"]',
    known_issues = '["Rev-up VQ35DE (2005-07 MT only) burns oil due to revised valve timing","Synchro grind on 1-2 shift under hard driving","Dash cracking in hot climates","Catalytic converter precats disintegrate — debris ingestion risk"]',
    avg_repair_cost = 850,
    recall_count = 3,
    part_availability = 'excellent',
    diy_friendliness = 'high',
    source = 'sample',
    score_notes = 'VQ35DE Rev-Up is the problematic variant — non-rev-up 2003-04 is better. Oil consumption is the defining flaw but engine itself rarely catastrophically fails. 6MT synchros are a known weak point. Chassis is simple and well-understood. Electronics are aging but not complex. Aftermarket support is massive — parts cheap, community knowledge deep. Ease of repair is the standout at 88 — this is why G35 still has cult following despite engine issues.'
WHERE id = 193 AND car_id = 64;

-- 2) Q50 Red Sport 400 (2016+) VR30DDTT — INSERT new row
INSERT INTO reliability (
    car_id,
    reliability_score,
    source,
    score_engine,
    score_transmission,
    score_chassis,
    score_electronics,
    score_ease_of_repair,
    common_failures,
    known_issues,
    avg_repair_cost,
    recall_count,
    part_availability,
    diy_friendliness,
    score_notes
) VALUES (
    34,
    NULL,   -- will be computed by recompute_aggregates.py
    'sample',
    65,     -- engine: VR30DDTT wastegate rattle, HPFP, boost solenoid failures
    58,     -- transmission: 7AT (RE7R01A) valve body, harsh shifting, torque converter shudder
    68,     -- chassis: suspension bushings premature wear, brake rotor warpage, steering rack
    42,     -- electronics: DAS steer-by-wire failure (SAFETY RECALL), infotainment black screen, ECU crashes
    45,     -- ease_of_repair: twin-turbo + DAS complexity, dealer-only diagnostics, expensive OEM parts
    '["VR30DDTT wastegate rattle","High-pressure fuel pump failure","DAS steer-by-wire failure (recall PC16/PC17)","Infotainment black screen freeze","7AT valve body harsh shifting","Boost control solenoid failure","Suspension bushing premature wear","Battery drain from always-on modules"]',
    '["7 NHTSA recalls — among highest for any luxury sedan","DAS steering can fail completely while driving — 6 associated deaths","VR30DDTT twin turbos difficult to access for service","Early 2014-16 models have ATTESA E-TS AWD module failures","2018+ facelift improved infotainment but DAS issues persist","2.0t variant (Mercedes M274) significantly more reliable than VR30"]',
    2200,
    7,
    'limited',
    'low',
    'A reliability step DOWN from the G37 it replaced. The VR30DDTT is Infiniti''s first twin-turbo V6 — wastegate rattle and HPFP issues are endemic. The real catastrophe is DAS steer-by-wire: NHTSA recall PC16/PC17 for steering failure while driving, 6 deaths linked to loss of control. This alone drags electronics to 42 and triggers catastrophe penalty. Ease of repair is poor at 45 — twin-turbo packaging is tight, DAS requires dealer calibration, and OEM parts are expensive with limited aftermarket. The 2.0t Mercedes-powered variant is notably better. Red Sport 400 is the worst Q50 variant for reliability.'
);

# MotorGeek Session Handoff — 2026-06-10

## Project Status: 169 Cars Scored (100%) ✅

### What We Built
A cross-brand luxury car comparison database with two scoring systems:
- **Reliability** (5 dims): engine 25%, transmission 25%, chassis 15%, electronics 15%, ease_of_repair 20% — with catastrophe penalty if any dim < 50
- **Build Quality / Q-Factor** (6 dims): body construction 25%, NVH 10%, interior 20%, paint 15%, electrical aging 15%, cosmetic aging 15% — no penalty

Plus TCO analysis, Q-factor calibration, deep-dive research documents, and depreciation modeling.

### User Preferences
- **Combined score weight**: **40/60 (Rel/Q)** — user prefers build quality weighted heavier than reliability for ranking purposes
- **User profile**: Bottom buyer — buys deep-depreciation cars, drives 30K more miles
- **Cars of interest**: Audi A8 D5 (primary target — deep analysis complete), LS430 (GOAT), LS400, Civic Type R (buy new), Chevy SS 6MT (sleeper hero), 500E (dream car — "money no object")

---

## DB State

- **169 total cars** in `cars` table (up from 158 last session)
- **169 cars scored** (both reliability + build_quality) — **0 gaps**
- **Reliability dimensions**: All 169 have 5-dim breakdowns (engine/trans/chassis/electronics/ease_of_repair)
- **Powertrain gaps**: All NULLs resolved (fuel_system, engine_layout, transmission_type, curb_weight_kg all 0 NULL)
- **DB path**: `C:\Users\llama\OneDrive\proj\motorgeek\data\motorgeek.db`

---

## Top 10 (40/60 Combined)

| # | Car | Rel | Q | Combined |
|---|-----|-----|---|----------|
| 1 | Lexus LS430 | 88.5 | 92.3 | 90.8 |
| 2 | Lexus LS400 | 92.0 | 88.3 | 89.8 |
| 3 | Porsche Taycan Turbo S | 77.5 | 86.7 | 83.0 |
| 4 | Audi A8 D5 facelift 2020 | 76.5 | 86.8 | 82.7 |
| 5 | Audi A8 D5 2017 | 75.8 | 86.5 | 82.2 |
| 6 | Lexus ES 350 | 87.8 | 78.0 | 81.9 |
| 7 | Chevrolet SS LS3 6MT | 85.6 | 79.2 | 81.8 |
| 8 | Honda Civic Type R 2023 | 83.8 | 78.5 | 80.6 |
| 9 | Mercedes 500E | 75.0 | 83.5 | 80.1 |
| 10 | BMW 7 Series 740i B58 | 77.8 | 81.5 | 80.0 |

---

## This Session's Work

### 1. A8 D5 Facelift Entry (car_id=43 → 2020-2021)
- Replaced 2018 A8 D5 with post-facelift 2020-2021 model
- Researched MHEV evolution, EA839 cam roller fix (resolved pre-06/2018), piston vulnerability
- Recalculated: Rel 76.5 (+0.3), Q 86.8 (+0.1), Combined 82.7 (+0.2)
- Key deltas: Engine +3 (cam roller fix), Electronics +1 (MIB3), Ease -2 (more complexity)

### 2. BMW 7 Series Audit & 740i Addition
- Audited 750i (N63TU2) vs A8 D5 — found 750i scores were systemically too low
- Recalibrated 750i (car_id=41): electronics 55→65, ease 42→46, paint 80→83, body 86→88, interior 85→87, elec_aging 58→64, cosmetic 72→77 → combined moved from 73.4 to 76.8
- Fixed engine_layout field (was "3.0L turbo I6 B58 (740i)" but data showed N63TU2 numbers → "4.4L twin-turbo V8 N63TU2 (750i)")
- Added BMW 740i B58 (car_id=164): Rel 77.8, Q 81.5, Combined 80.0 → #10
- Key insight: B58 is dramatically better than N63 (EngineScope 93 vs 42), making 740i a legitimate alternative to the A8

### 3. American Cars Expansion (+12 new entries, ids 164-175)
- **Chevy SS LS3 6MT** (170): Rel 85.6, Q 79.2, Combined 81.8 → #7 (!)
- **Buick LaCrosse 3.6L** (168): Rel 76.8, Q 80.5, Combined 79.0
- **Lincoln Continental 3.0T** (165): Rel 75.4, Q 80.3, Combined 78.3
- **Lincoln MKZ 3.0T** (167): Rel 74.2, Q 78.5, Combined 76.8
- **Cadillac ATS 3.6L LGX** (169): Rel 74.4, Q 75.3, Combined 74.9
- **Lincoln Navigator 3.5T** (171): Rel 67.4, Q 79.7, Combined 74.8
- **Chrysler 300 5.7L HEMI** (166): Rel 77.2, Q 71.0, Combined 73.5
- **Lincoln Aviator 3.0T** (172): Rel 66.4, Q 76.8, Combined 72.6
- **Lincoln Nautilus 2.7T** (173): Rel 67.2, Q 75.3, Combined 72.1
- **Lincoln Corsair 2.3T** (174): Rel 70.0, Q 73.2, Combined 71.9
- **Cadillac Escalade 6.2L** (175): Rel 66.0, Q 72.5, Combined 69.9

### 4. A8 D5 Deep-Dive Research
- **Depreciation schedule**: 20-year curve with three zones (Sweet Spot $24-30K at age 7-9, Caution $14-19K at age 10-12, Too Risky <$12K at 13+)
- **US sales data**: 21-year annual table (A8 vs S-Class vs 7 Series vs Panamera). Segment down 53% from peak. A8 collapsed from ~6K to ~1.6K. Only ~15K D5s sold in US total.
- **VAG parts-sharing map**: Engine (EA839) shared across 300-400K+ US vehicles. Transmission (ZF 8HP65) across 500K+. BSG 48V, MIB3, Virtual Cockpit all widely shared. Body panels are A8-exclusive risk.
- **Research doc**: `docs/research/2026-06-10-a8-d5-bottom-buyer-deep-dive.md` (211 lines)

---

## Key Decisions & Insights

- **A8 D5 is the #1 bottom-buyer target**: #4 overall, 30% cheaper than comparable S-Class, 80%+ shared parts, aluminum body, standard AWD. Optimal buy window: 2026-2028 at $25-30K.
- **Chevy SS is the American hero**: #7 overall with the LS3 6MT. Engine 90, Ease 88 — elite scores. Only ~3,000 manuals imported.
- **740i B58 closes the gap on the A8**: 80.0 vs 82.7. B58 engine is actually more reliable than EA839 (85 vs 82 engine score) but A8 wins on build quality.
- **Q-score calibration matters**: Genesis, Mercedes, BMW all needed upward calibration. The scoring agent systematically underestimated interiors, paint, and electrical aging by 5-15 points on non-German brands.
- **The flagship sedan is dying**: Segment down 53% from 2006 peak. SUVs killed the category. This makes bottom-buyer economics even better — falling new sales = shrinking used supply = long-term value floor.

---

## Critical Car IDs

| Car | ID | Notes |
|-----|-----|-------|
| LS430 | 39 | GOAT, #1 |
| LS400 | 63 | #2 |
| A8 D5 facelift | 43 | #4, primary target |
| A8 D5 2017 | 22 | #5 |
| Chevy SS 6MT | 170 | #7, American hero |
| 740i B58 | 164 | #10 |
| 750i N63TU2 | 41 | Recalibrated, fixed engine_layout |
| Continental 3.0T | 165 | Best Lincoln |
| LaCrosse 3.6L | 168 | Sleeper pick |
| EQS 580 | 122 | Rel 72.7, Q 80.9 |

---

## Research Documents

| File | Lines | Content |
|------|-------|---------|
| `docs/research/2026-06-10-a8-d5-bottom-buyer-deep-dive.md` | 211 | Depreciation curve, sales data, parts sharing, buy recommendation |
| `docs/research/2026-06-08-bottom-buyer-analysis.md` | — | Original bottom-buyer framework |
| `docs/research/2026-06-08-leno-act-smog-exemption-analysis.md` | 416 | CA smog exemption for 1975+ cars |
| `docs/research/2026-06-08-mercedes-engineering-deep-dive.md` | 732 | Mercedes brand analysis |
| `docs/research/2026-06-08-na-vs-turbo-brand-tier-analysis.md` | 466 | NA vs turbo engine reliability |

---

## SQL Files (This Session)

| File | Purpose |
|------|---------|
| `data/sql_inserts/update_a8_2020_reliability.sql` | A8 facelift reliability scores |
| `data/sql_inserts/update_a8_2020_build_quality.sql` | A8 facelift Q scores |
| `data/sql_inserts/insert_740i_car.sql` | BMW 740i car entry |
| `data/sql_inserts/insert_740i_powertrain.sql` | 740i powertrain |
| `data/sql_inserts/insert_740i_reliability.sql` | 740i reliability |
| `data/sql_inserts/insert_740i_build_quality.sql` | 740i build quality |
| `data/sql_inserts/fix_750i_recalibration.sql` | 750i recalibration + engine_layout fix |
| `data/sql_inserts/insert_american_cars.sql` | 11 American cars |
| `data/sql_inserts/insert_american_powertrain.sql` | Powertrain data |
| `data/sql_inserts/insert_american_reliability.sql` | Reliability scores |
| `data/sql_inserts/insert_american_build_quality.sql` | Build quality scores |

---

## Next Steps

1. **Regenerate DB dump** (`data/motorgeek_dump.sql`) — all changes since last dump
2. **Git commit** — all scoring changes, calibration SQL, new cars, research docs, updated HANDOFF
3. **Potential follow-ups**:
   - TCO comparison: A8 D5 vs 740i vs LS430 at same price point
   - EQS depreciation analysis (EV curve is brutal)
   - Electronics table analysis for high-scoring cars
   - "Last of the ICE" collector thesis for A8 D5
   - Specific car deep-dives per user interest

---

## Agent Sessions (This Session)

| Agent | Task | Session |
|-------|------|---------|
| Librarian | A8 D5 2020 facelift research | ses_14ce51442ffev1Ed2eBlzYpR7A |
| Librarian | BMW 740i B58 research | ses_14c3722f3ffeEaVd1ol50nQhm8 |
| Librarian | American luxury sedans research | ses_14c29ff6fffe5IMZwFjW05lz2W |
| Librarian | Lincoln/Cadillac SUV research | ses_14c29b0acffe12IVFxe53KbipM |
| Librarian | Chevy SS research | ses_14c2962aafferq2a2mQ4jQEMeZ |
| Librarian | A8 D5 depreciation research | ses_14bb7b5e8ffe6RAqfQDAYJFvvO |
| Librarian | A8 vs S-Class vs 7 Series sales | ses_14bab8609ffewXUGh9h55TLBj5 |
| Librarian | VAG parts-sharing research | ses_14b9bba94ffeBlh4pGvPchpxsJ |
| Sisyphus-Junior (deep) | 32-car reliability backfill | ses_14d079560ffejMmJrBl7lvbeuE |
| Sisyphus-Junior (deep) | 55-car powertrain backfill | ses_14d072835ffe3XXsWOQ70CTYeC |
| Sisyphus-Junior (deep) | 11 American cars DB insert | ses_14c22b77effeZLSH1iqX8O254f |
| Sisyphus-Junior (writing) | A8 D5 research doc | ses_14b91e798ffeL1LvcIRVUJ9E8j |

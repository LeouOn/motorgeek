# Bottom-Buyer Analysis: LS430 vs G90 5.0 Tau vs The Market

**Date**: 2026-06-08
**Methodology**: MotorGeek database (157 cars, 57 with reliability + Q-factor scores), TCO modeling, California smog research, market analysis.
**Buyer Profile**: California-based, looking for a "last 30K car" — a deeply depreciated luxury sedan to drive 30,000 miles over 3-5 years. Values engineering over badge, reliability over flash.

---

## Table of Contents

1. [The Database](#1-the-database)
2. [Single Metric Rankings](#2-single-metric-rankings)
3. [Q-Factor Build Quality Deep Dive](#3-q-factor-build-quality-deep-dive)
4. [Composite Scores](#4-composite-scores)
5. [LS430 vs G90 Tau: Head to Head](#5-ls430-vs-g90-tau-head-to-head)
6. [California Smog Analysis](#6-california-smog-analysis)
7. [5-Year Deferral Scenario](#7-5-year-deferral-scenario)
8. [Final Verdict](#8-final-verdict)

---

## 1. The Database

The MotorGeek database contains **157 cars** with varying levels of scoring:

| Data Layer | Cars Covered |
|---|---|
| Basic specs (hp, weight, engine) | 157 |
| Reliability scores (5-dimension) | 57 |
| Q-Factor build quality (6-dimension) | 57 |
| Performance data (0-60, top speed) | ~50 |
| Cost-to-own (MSRP, fuel, maintenance) | ~45 |
| Full cross-dimensional data | 39 |

### Scoring Systems

**Reliability** (5 dimensions, weighted):
- Engine (25%), Transmission (25%), Chassis (15%), Electronics (15%), Serviceability (20%)
- Catastrophe penalty: if any dimension < 50, overall score penalized
- Score range: 39.6 (Infiniti Q50) to 92.0 (Lexus LS 400)

**Q-Factor Build Quality** (6 dimensions, weighted):
- Body Construction (25%), NVH Isolation (10%), Interior Materials (20%), Paint/Corrosion (15%), Electrical Aging (15%), Cosmetic Aging (15%)
- No catastrophe penalty — build quality doesn't "catastrophically" fail like reliability
- Score range: 39.6 (Infiniti Q50) to 92.3 (Lexus LS430)
- All scores verified against `compute_build_aggregate()` — zero mismatches

### Design Tension in Q-Factor

The Q-factor as designed contains two sub-clusters:
- **Pure build quality** (how it was assembled): body, NVH, interior materials
- **Long-term durability** (how it ages): paint/corrosion, electrical aging, cosmetic aging

The durability dimensions function as proxy reliability scores. The ES 350 gets electrical=85 not because its electronics are sophisticated, but because they're simple and don't fail. The G90 gets electrical=64 not because the screens are poorly assembled, but because Hyundai electronics have more failure modes over 10 years.

This conflation is arguably a feature, not a bug — for a bottom buyer, a car that ages poorly *feels* like bad build quality regardless of cause. But it's worth noting that the G90's actual assembly quality (body, NVH, interior) may equal or exceed the ES 350 while the durability dimensions drag the overall score down.

---

## 2. Single Metric Rankings

### Reliability King: Lexus LS 400 — 92.0

| Rank | Car | Score |
|---|---|---|
| 1 | Lexus LS 400 (1st gen) | 92.0 |
| 2 | Lexus LS430 (3rd gen) | 88.5 |
| 3 | Toyota Supra A80 | 88.0 |
| 4 | Lexus ES 350 | 87.8 |
| 5 | Lexus GS 4th gen | 85.0 |
| 6 | Toyota Camry V6 | 83.9 |
| 7 | Mercedes 280 SL Pagoda | 82.0 |
| 8 | Mercedes C300 W205 | 82.0 |
| 9 | BMW 540i G30 LCI | 81.6 |
| 10 | Infiniti G35 | 80.9 |

Toyota/Lexus dominance is total. The only non-Japanese car in the top 10 is the Mercedes 280 SL — a hand-built 1960s roadster with zero electronics to fail.

### Q-Factor King: Lexus LS430 — 92.3

| Rank | Car | Score |
|---|---|---|
| 1 | Lexus LS430 | 92.3 |
| 2 | Lexus LS 400 | 88.3 |
| 3 | Lexus LS460 | 83.7 |
| 4 | Mercedes 500E W124 | 83.5 |
| 5 | Lexus LS 600h | 79.5 |
| 6 | Lexus ES 350 | 78.0 |
| 7 | BMW 540i G30 LCI | 77.2 |
| 8 | Audi A6 C8 | 77.0 |
| 9 | Mercedes SL 63 R232 | 77.0 |
| 10 | Mercedes E-Class W213 | 75.5 |

The 500E W124 at #4 is the only non-Lexus in the top 5. Porsche-assembled, hand-fitted, legendary overengineering. The LS460 at #3 has a notable electrical score of 55 — the 8-speed transmission ECU is a known weakness.

### Acceleration King: Mercedes SL 63 R232 — 3.0s

| Rank | Car | Time |
|---|---|---|
| 1 | Mercedes SL 63 R232 | 3.0s |
| 2 | Mercedes SL63 AMG R231 | 3.5s |
| 3 | Porsche 911 Turbo 996 | 4.2s |
| 4 | Volvo V60 Polestar | 4.4s |
| 5 | Ferrari F355 | 4.5s |

Mercedes owns raw performance. But none of these cars score above 77 on reliability or Q-factor.

### Horsepower King: Mercedes SL63 R231 — 577 hp

| Rank | Car | HP |
|---|---|---|
| 1 | Mercedes SL63 R231 | 577 |
| 2 | Mercedes SL 63 R232 | 577 |
| 3 | Mercedes SL55 AMG R230 | 493 |
| 4 | Lexus LS 600h | 445 |
| 5 | Genesis G90 5.0 Tau | 420 |

The Tau 5.0 at 420 hp is the highest-rated naturally aspirated V8 in the database — no turbos, no superchargers, just displacement. Also notable: it runs on **87 octane regular unleaded**, not premium.

### Cheapest MSRP: Mercedes 190 SL — $4,000

Historical MSRPs for context. The G90 5.0 Tau launched at ~$70K, now trades at ~$25K used. The LS430 launched at ~$55-65K, now trades at ~$8-12K used.

### Lowest Maintenance: Lexus LS 400 / Toyota Camry — $400/yr

| Rank | Car | Annual Cost |
|---|---|---|
| 1 | Lexus LS 400 | $400/yr |
| 2 | Toyota Camry V6 | $400/yr |
| 3 | Lexus LS430 | $450/yr |
| 4 | Kia K5 GT | $450/yr |
| 5 | Lexus ES 350 | $468/yr |

---

## 3. Q-Factor Build Quality Deep Dive

### The G90 Adjustment

Initial scoring placed the G90 5.0 Tau at Q=70.2, which was below the ES 350 at Q=78.0. This didn't pass the sniff test — the G90 has hydraulic engine mounts, acoustic laminated glass, active noise cancellation, semi-aniline leather, and V8 smoothness that the ES 350 lacks.

After adjustment:

| Variant | Old Q | New Q | NVH Change | Interior Change |
|---|---|---|---|---|
| G90 5.0 Tau | 70.2 | **72.4** | 72→82 | 74→80 |
| G90 1st gen 3.3T | 70.3 | **71.9** | 70→78 | 74→78 |
| G90 2nd gen | 71.0 | **72.7** | 73→80 | 75→80 |

**Rationale**: The G90 has hydraulic engine mounts, acoustic laminated glass, active noise cancellation, and semi-aniline leather — all absent from the ES 350. The V8 Tau is inherently smoother than any V6. Previous scores penalized NVH/interior too aggressively for shared platform origin without accounting for flagship-specific isolation.

The remaining gap (G90 Tau 72.4 vs ES 350 78.0) is now driven by the legitimate long-term aging differences:
- Electrical: G90 64 vs ES 85 (Hyundai electronics vs Toyota simplicity)
- Paint: G90 66 vs ES 78 (Korean paint vs Toyota paint)
- Cosmetic: G90 68 vs ES 82 (materials aging over 10+ years)

### Full Q-Factor Ranking (57 cars)

| Rank | Car | Q | Body | NVH | Interior | Paint | Elec | Cosmetic |
|---|---|---|---|---|---|---|---|---|
| 1 | Lexus LS430 | 92.3 | 97 | 95 | 94 | 93 | 82 | 90 |
| 2 | Lexus LS 400 | 88.3 | 94 | 89 | 87 | 84 | 90 | 83 |
| 3 | Lexus LS460 | 83.7 | 94 | 92 | 90 | 90 | 55 | 75 |
| 4 | Mercedes 500E W124 | 83.5 | 95 | 88 | 88 | 85 | 65 | 72 |
| 5 | Lexus LS 600h | 79.5 | 94 | 94 | 92 | 90 | 30 | 68 |
| 6 | Lexus ES 350 | 78.0 | 72 | 80 | 76 | 78 | 85 | 82 |
| 7 | BMW 540i G30 LCI | 77.2 | 82 | 80 | 80 | 78 | 68 | 72 |
| 8 | Audi A6 C8 | 77.0 | 82 | 80 | 85 | 78 | 62 | 70 |
| 9 | Mercedes SL 63 R232 | 77.0 | 82 | 78 | 80 | 78 | 68 | 72 |
| 10 | Mercedes E-Class W213 | 75.5 | 78 | 78 | 80 | 75 | 68 | 72 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 21 | Genesis G90 2nd gen | 72.7 | 76 | 80 | 80 | 66 | 62 | 70 |
| 22 | **Genesis G90 5.0 Tau** | **72.4** | 74 | 82 | 80 | 66 | 64 | 68 |
| 24 | Genesis G90 1st gen 3.3T | 71.9 | 74 | 78 | 78 | 66 | 66 | 68 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |
| 56 | Infiniti G35 | 48.8 | 72 | 42 | 48 | 38 | 35 | 40 |
| 57 | Infiniti Q50 | 39.6 | 58 | 40 | 32 | 35 | 28 | 35 |

### Key Observations

- **LS430 dominance**: The LS430 scores 92.3 on Q-factor — the highest of any car in the database. Its body construction (97) and interior materials (94) are unmatched. Laser welding world-first, Tahara assembly, semi-aniline leather.
- **500E W124**: The only non-Lexus in the top 5. Porsche-assembled at Zuffenhausen, hand-fitted body panels. At 83.5, it's the best-built German car in the database.
- **LS460 electrical penalty**: Despite being newer than the LS430, the LS460's electrical score is 55 (vs LS430's 82). The 8-speed transmission ECU is a known weakness. This is the clearest example of "more tech ≠ better quality."
- **LS600h hybrid penalty**: Electrical score of 30 — the hybrid system is a nightmare. Body/NVH/interior are all 90+ but the electrical system drags the overall score to 79.5.
- **Genesis cluster**: All Genesis cars cluster 63-73. Consistent but not exceptional. Shared platform penalty applied across the board.
- **G90 Tau NVH advantage**: At NVH=82, the G90 Tau now sits above the ES 350 (80), reflecting the V8 smoothness, hydraulic mounts, and acoustic glass.
- **Infiniti basement**: G35 (48.8) and Q50 (39.6) are the worst-scored cars. The Q50 is Infiniti's worst era — DAS steer-by-wire, interior materials disgraceful for a $40-50K car.

---

## 4. Composite Scores

### Bottom Buyer Score (Reliability 35%, Q-Factor 25%, Performance 15%, Value 25%)

| Rank | Car | Score | R | Q | P | V |
|---|---|---|---|---|---|---|
| 1 | **Lexus LS 400** | **79.3** | 92 | 88 | 18 | 89 |
| 2 | **Lexus LS430** | **78.0** | 88 | 92 | 29 | 78 |
| 3 | Lexus ES 350 | 76.2 | 88 | 78 | 24 | 90 |
| 4 | Toyota Supra A80 | 75.5 | 88 | 63 | 62 | 78 |
| 5 | Toyota Camry V6 | 74.7 | 84 | 68 | 40 | 90 |
| 6 | BMW 540i G30 | 74.4 | 80 | 74 | 58 | 77 |
| 7 | Lexus GS 4th gen | 74.2 | 85 | 76 | 36 | 81 |
| 8 | Kia Stinger | 73.4 | 80 | 61 | 51 | 90 |
| 9 | Audi A6 C8 | 72.5 | 75 | 77 | 53 | 76 |
| 10 | Volvo V60 Polestar | 71.9 | 68 | 58 | 65 | 96 |

**Boring wins.** The LS 400 and LS430 dominate because they score 88-92 on both reliability AND Q-factor while being cheap enough to score well on value. The Supra A80 makes a surprise appearance at #4 — 88 reliability, strong performance, and depreciated to reasonable prices.

### Enthusiast Score (Performance 35%, Reliability 20%, Q-Factor 15%, Value 30%)

| Rank | Car | Score | R | Q | P | V |
|---|---|---|---|---|---|---|
| 1 | Volvo V60 Polestar | 73.8 | 68 | 58 | 65 | 96 |
| 2 | Toyota Supra A80 | 72.3 | 88 | 63 | 62 | 78 |
| 3 | BMW 540i G30 | 70.6 | 80 | 74 | 58 | 77 |
| 4 | Kia Stinger | 70.0 | 80 | 61 | 51 | 90 |
| 5 | Genesis G70 3.3T | 69.7 | 70 | 63 | 60 | 84 |

The V60 Polestar wins enthusiast because it's deeply depreciated ($23K MSRP now cheaper used) with 350hp AWD and Ohlins dampers. It's terrible on Q-factor (57.5) but the value proposition is enormous.

### Quality Purist Score (Q-Factor 40%, Reliability 40%, Value 20%)

| Rank | Car | Score | R | Q | V |
|---|---|---|---|---|---|
| 1 | **Lexus LS 400** | **90.0** | 92 | 88 | 89 |
| 2 | **Lexus LS430** | **88.0** | 88 | 92 | 78 |
| 3 | Lexus ES 350 | 84.3 | 88 | 78 | 90 |
| 4 | Lexus GS 4th gen | 80.3 | 85 | 76 | 81 |
| 5 | Mercedes 280 SL Pagoda | 78.8 | 82 | 65 | 100 |

Lexus sweeps the top 4. The 280 SL Pagoda at #5 is an artifact of its $6,900 original MSRP inflating the value score — it's a museum piece, not a daily driver.

---

## 5. LS430 vs G90 Tau: Head to Head

### The Cars

| | Lexus LS430 (2004-2006) | Genesis G90 5.0 Tau (2017-2020) |
|---|---|---|
| **Engine** | 3UZ-FE 4.3L V8, port injection, 290hp | Tau 5.0 V8, GDI, 420hp |
| **Transmission** | 6-speed auto | 8-speed auto |
| **Fuel** | 87 octane regular | 87 octane regular |
| **Assembly** | Tahara, Japan (hand-finished) | Ulsan, South Korea |
| **MSRP new** | ~$55-65K | ~$70K |
| **Used price (2026)** | ~$8-12K (appreciating) | ~$20-28K (bottomed) |
| **Reliability** | 88.5 | 75.7 |
| **Q-Factor** | 92.3 | 72.4 |

### The Used Price Paradox

Despite a $35K MSRP gap when new, the LS430 and G90 5.0 Tau now trade at similar used prices (~$10K vs ~$25K). This is telling:

- The LS430 has **stopped depreciating and started appreciating** — it bottomed ~3 years ago and clean examples are now climbing. It's become a recognized "future classic" — the last truly overengineered Lexus.
- The G90 Tau has **reached its depreciation floor** — at $20-28K, you're buying $70K of car for pennies. The Tau 5.0 V8 is discontinued; there will never be another one. But the market hasn't recognized its rarity yet.

### Why the Market Values Them Similarly

1. **Brand perception**: Lexus badge holds value. Genesis badge is still earning credibility.
2. **Parts network**: Toyota/Lexus has 30+ years of aftermarket support. Genesis Tau 5.0 parts are already getting scarce.
3. **Fear of the unknown**: A 2005 LS430 at 150K miles is a known quantity. A 2018 G90 at 80K miles has uncertain longevity.
4. **Enthusiast community**: The LS430 has a cult following (r/LS430, ClubLexus). The G90 Tau has almost no community.

### The Emotional Argument

The LS430 is like buying a Rolex Submariner — it's been "the answer" for so long that the market has priced in its correctness. You buy it and everyone nods. Safe. Boring. Correct.

The G90 Tau is like buying a Grand Seiko Snowflake — it's arguably as good or better in specific dimensions, it's more interesting, more rare, more of a statement. But you have to explain it to people. And the resale market doesn't have your back the same way.

### The Data Argument

On pure numbers, the LS430 wins decisively:
- Reliability: 88.5 vs 75.7 (13-point gap)
- Q-Factor: 92.3 vs 72.4 (20-point gap)
- Maintenance: $450/yr vs $550-700/yr
- Depreciation: Appreciating vs Flat
- Parts availability: Excellent vs Questionable

The G90 Tau's advantages are:
- 420hp vs 290hp (45% more power)
- Modern safety tech (blind spot, adaptive cruise, lane keep)
- 8-speed transmission (2 more gears)
- Significantly newer (12-16 years newer)
- Better interior materials at the touch-point level

---

## 6. California Smog Analysis

### The Regulatory Framework

California requires biennial smog checks for all 1976+ gasoline vehicles. The test is **OBD2 scan only** for 2000+ vehicles — no tailpipe sniffer. The inspector checks:
1. No active Check Engine Light
2. No stored or permanent diagnostic trouble codes
3. All readiness monitors complete (except EVAP)
4. Visual inspection for tampered/missing emissions equipment

### LS430 Smog Risk: MODERATE-HIGH

**The #1 issue: Catalytic converter efficiency (P0420/P0430)**

The LS430 has **3 catalytic converters**: two front pre-cats (one per bank) and one rear main cat. At 150K+ miles, the front pre-cats commonly degrade below the OBD2 efficiency threshold.

- Typical failure mileage: 120K-180K
- Some LS430s pass at 200K+ on original cats (one ClubLexus member: 403K, original cats, passes CA smog)
- It's not guaranteed failure, but it's a **known, predictable risk**

**California-specific pain:**
- Federal/EPA aftermarket cats are **ILLEGAL** in California
- Must use CARB-compliant cats with Executive Order (EO) number
- Must match specific Engine Family Number (EFN): 5TYXV04.3WMA
- CARB-compliant aftermarket cat (MagnaFlow): $350-600 per cat
- OEM Lexus cats: $1,600-1,900 per cat
- Full 3-cat replacement at a shop: **$4,000-6,000**

**O2 sensors:**
- 4 sensors total (2 upstream, 2 downstream)
- OEM Denso strongly recommended — aftermarket sensors cause persistent codes
- Part numbers: Denso #234-4138, 234-4139 (front), #234-4151 (rear)
- Cost: ~$200-280 per sensor at a shop, ~$60-120 DIY

**Other failure modes:**
- EVAP leaks (P0455) — often just a bad gas cap ($5)
- Readiness monitors not set after battery disconnect — requires specific drive cycle
- Permanent DTCs (PDTCs) — checked since July 2019, cannot be cleared by tools

**Pre-purchase checklist for LS430 in CA:**
1. Demand current smog certificate (< 90 days) — it's legally the seller's responsibility
2. Plug in OBD2 scanner: check for stored codes, readiness monitor status
3. Check for P0420/P0430 specifically — if present, negotiate $4K off or walk away
4. Visually inspect Y-pipe for rust/leaks
5. Verify underhood emissions sticker says "California" or "50-State"
6. Be wary of recent battery disconnect — monitors may not be ready

**No exemption coming soon:**
- Current law: 1975 and older exempt
- Leno's Law (SB 712/SB 1392): 35-year rolling exemption proposed but stalled
- LS430 (2001-2006) won't hit 35 years until 2036-2041
- Even if passed, may require collector car insurance, not daily driver use

### G90 5.0 Tau Smog Risk: LOW

**Window sticker confirms 50-state certification.** The car was built to California standards from the factory. Zero CARB-specific hurdles.

- Model years 2017-2020: 6-9 years old, emissions equipment barely degraded
- No emissions-specific TSBs or recalls for the 5.0 V8
- The turbo oil pipe fire recall (24V-191) only affects the 3.3T
- Naturally aspirated = simpler emissions system than turbo variants

**Warranty coverage on emissions:**
- Federal: 8yr/80K on catalytic converters, ECM, OBD
- 2019-2020 models may still have active coverage — check by VIN
- 2017-2018 models: coverage likely expired

**One smog-adjacent risk: GDI carbon buildup**
- The Tau 5.0 is GDI-only (not dual-injection like Lexus's D-4S)
- At 75K+ miles, carbon on intake valves can cause rough idle, misfires, emissions codes
- Walnut blast service: ~$300-500
- The LS430's port injection is self-cleaning — no carbon buildup issue

**Registration costs:**
- At $25K purchase price: ~$300-400 Year 1, dropping to ~$24/yr by Year 11
- VLF is tax-deductible on federal returns
- Out-of-state purchase: zero barriers (50-state certified)

### Smog Comparison Summary

| Factor | LS430 | G90 5.0 Tau |
|---|---|---|
| Smog risk level | Moderate-High | Low |
| Primary concern | Cat converter degradation at 150K+ | GDI carbon buildup at 75K+ |
| Worst-case repair | $4-6K (cat replacement, CA-compliant) | $300-500 (walnut blast) |
| Emissions warranty | None | Maybe (2019-2020) |
| Smog exemption timeline | 2036-2041 earliest | N/A (still new) |

---

## 7. Five-Year Deferral Scenario (2031)

### LS430 in 2031

- **Age**: 25-30 years old
- **Price**: Estimated $13-15K (continuing 5-8% annual appreciation)
- **Smog**: Harder. Cats continue degrading with age regardless of mileage. A car that passes today may not pass in 2031.
- **Parts**: Excellent. Toyota/Lexus aftermarket is 30 years deep.
- **Exemption**: Still 5-10 years away from any smog exemption.
- **Wildcard**: If Leno's Law passes, the 2001 LS430 becomes smog-exempt in 2036. That could drive a significant price jump — the "smog-exempt LS430" premium.

### G90 5.0 Tau in 2031

- **Age**: 14-19 years old
- **Price**: Estimated $10-15K (flat, possibly starting to appreciate as rarity recognized)
- **Smog**: Starting to get harder. Federal emissions warranty expired. GDI carbon buildup more likely at higher mileages. Cats beginning to age.
- **Parts**: **Questionable**. Tau 5.0 is orphaned — no longer in production, low volume. Genesis already struggles with Tau parts backordering in 2026. In 2031, it could be much worse.
- **Warranty**: All emissions coverage expired.

### Financial Comparison

| | Buy LS430 Now ($10K) | Buy G90 Now ($25K) | Invest $25K |
|---|---|---|---|
| 2031 value | ~$15K (appreciating) | ~$12K (depreciating) | ~$40K (10% avg) |
| 5yr ownership cost | ~$2-3K net (after resale) | ~$13K net (depreciation) | N/A |
| Smog costs (5yr) | $0-6K (cat risk) | $0-1K (low risk) | N/A |
| **Net position in 2031** | **+$10-13K** | **-$12-14K** | **+$15K** |

**The LS430 is the financially rational purchase right now** because it's a depreciated asset that's stopped depreciating. You drive it for 5 years and sell it for roughly what you paid. It's like living in a house for free while it appreciates.

**Deferring 5 years and investing is the financially optimal play** — but it means not having the car for 5 years, and the LS430 will be more expensive and harder to find in 2031.

---

## 8. Final Verdict

### The Data Says

The LS430 wins on every measurable dimension except horsepower and modernity. It's more reliable, better built, cheaper to maintain, appreciating in value, and has bulletproof parts support. For a bottom buyer in California, it's the rational choice.

### The Heart Says

The G90 5.0 Tau is the more interesting car. 420hp V8 on 87 octane. Hydraulic mounts. Acoustic glass. Active noise cancellation. A $70K interior for $25K. And it's the only Korean V8 luxury sedan ever made — there will never be another. It's a Grand Seiko in a world of Rolexes.

### The Math Says

Put the $25K in the market. In 5 years it's $40K. Then decide.

Or buy the LS430 for $10K — it's a free car. You'll drive it for 3 years, sell it for what you paid, and the only real cost is gas and insurance. Meanwhile your remaining $15K is still compounding.

### The California Factor

The LS430's smog risk is a hidden $4-6K liability on a $10K car. If the cats are marginal, it's really a $14-16K car. The G90 passes smog with its eyes closed for the next decade. This is the one dimension where "boring" doesn't win — the newer car wins.

### Bottom Line

If you're going to buy now: **LS430**, but only if it has a clean smog certificate and healthy cats. Budget $4K for potential cat replacement.

If you're going to buy for the heart: **G90 5.0 Tau**, but accept that it's a $25K toy that won't appreciate and may have parts availability issues in 10 years.

If you're going to be rational: **Neither. Invest the money. The market always wins.**

---

*Analysis generated using MotorGeek database v1.0, 157 cars, 57 with full scoring. All Q-factor scores verified against `compute_build_aggregate()` with zero mismatches. California smog research sourced from BAR, CARB, NHTSA, ClubLexus forums, and Genesis warranty documentation.*

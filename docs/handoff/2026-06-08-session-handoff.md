# MotorGeek Session Handoff — 2026-06-08

## Status: IN PROGRESS — Paused Mid-Backfill

**DB State**: 112/157 cars scored (71.3%). 45 cars remaining.
**Tests**: 22/22 passing. Alembic head: `212f51617bb3`.

---

## What Was Done

### Completed
1. **Q-factor Build Quality system** — fully implemented, migrated, tested (6 dimensions, weighted aggregate)
2. **Original 57 cars** — Q-factor + reliability scored and verified
3. **Stream 1 partial backfill** — 55 new cars loaded into DB:
   - Mercedes+AMG (7) ✅ — `add_scores_mercedes_amg.sql`
   - Mazda (6) ✅ — `add_scores_mazda.sql`
   - BMW (12) ✅ — `add_scores_bmw.sql`
   - American (16) ✅ — `add_scores_american.sql`
   - Exotics+EVs+Misc (14) ✅ — `add_scores_exotics_evs_misc.sql`
4. **Stream 2 TCO upgrade** ✅ — `scripts/bottom_buyer_tco.py` updated with Q-factor adjustments
5. **Stream 3 Leno Act research** ✅ — `docs/research/2026-06-08-leno-act-smog-exemption-analysis.md` (416 lines)
6. **Stream 4 Mercedes deep dive** ✅ — `docs/research/2026-06-08-mercedes-engineering-deep-dive.md` (732 lines)

### Remaining Work
**45 cars still need scoring** across 3 groups:

| Group | Cars | Status | Agent Session ID |
|-------|------|--------|-----------------|
| Toyota+Honda+Acura | 13 | Agent timed out, needs retry | `ses_1568df92dffepKlaqSERtLw1Dw` |
| Nissan+Mitsubishi+Subaru | 14 | Agent timed out, needs retry | `ses_1568157eeffeNCygCTAraDFfS3` |
| Audi+Porsche+VW | 18 | Agent timed out, needs retry | `ses_1568d4010ffeG4BewQ2X64tmxx` |

**After backfill completes:**
- Run full verification (aggregate scores match DB values)
- Stream 5: NA vs Turbo reliability gap analysis + brand tier rankings
- Run updated TCO script on all 157 cars
- Final commit

---

## Database State

### Tables & Counts
- `cars`: 157 total
- `reliability`: 112 entries (IDs 1-301, gaps exist for unscored cars)
- `build_quality`: 112 entries (IDs 1-158, gaps exist for unscored cars)

### ID Ranges Used
| Group | Reliability IDs | Build Quality IDs |
|-------|----------------|-------------------|
| Original 57 | 1-57 | 1-58 |
| BMW | 202-213 | 59-70 |
| Mercedes+AMG | 241-247 | 98-104 |
| Mazda | 282-287 | 139-144 |
| Exotics+EVs | 288-301 | 145-158 |
| American | 266-281 | 123-138 |

### ID Ranges RESERVED (not yet loaded)
| Group | Reliability IDs | Build Quality IDs |
|-------|----------------|-------------------|
| Toyota+Honda+Acura (13) | 214-226 | 71-83 |
| Nissan+Mitsu+Subaru (14) | 227-240 | 84-97 |
| Audi+Porsche+VW (18) | 254-265* | 105-122 |

*Note: These IDs were planned but agents timed out before writing SQL files. Verify no conflicts before inserting.

---

## Key Formulas

### Reliability (5 dimensions, catastrophe penalty)
```
weights = {engine: 0.25, transmission: 0.25, chassis: 0.15, electronics: 0.15, ease_of_repair: 0.20}
raw = weighted sum
if any dimension < 50:
    penalty = 0.85 + (min_dimension / 50) * 0.15
    score = raw * penalty
else:
    score = raw
```

### Build Quality / Q-factor (6 dimensions, NO penalty)
```
weights = {body_construction: 0.25, nvh_isolation: 0.10, interior_materials: 0.20, paint_corrosion: 0.15, electrical_aging: 0.15, cosmetic_aging: 0.15}
q_score = weighted sum (no penalty ever)
```

### TCO Q-factor Adjustments (in `bottom_buyer_tco.py`)
- Maintenance: Q≥80 ×0.90, Q<70 ×1.15
- Depreciation: Q≥80 +0.05 pct, Q<60 -0.05 pct
- Risk buffer: Q≥80 -0.03 prob, Q<60 +0.05 prob

---

## Important Files

### Code
- `motorgeek/core/scoring.py` — Reliability aggregate
- `motorgeek/core/scoring_build.py` — Q-factor aggregate
- `motorgeek/core/models.py` — ORM classes
- `scripts/bottom_buyer_tco.py` — TCO analyzer (Q-factor integrated)

### SQL (already loaded into DB)
- `data/sql_inserts/add_scores_mercedes_amg.sql` — 7 cars
- `data/sql_inserts/add_scores_mazda.sql` — 6 cars
- `data/sql_inserts/add_scores_bmw.sql` — 12 cars
- `data/sql_inserts/add_scores_american.sql` — 16 cars
- `data/sql_inserts/add_scores_exotics_evs_misc.sql` — 14 cars

### SQL (NOT YET GENERATED — need agent retries)
- `data/sql_inserts/add_scores_toyota_honda_acura.sql` — 13 cars (PENDING)
- `data/sql_inserts/add_scores_nissan_mitsu_subaru.sql` — 14 cars (PENDING)
- `data/sql_inserts/add_scores_audi_porsche_vw.sql` — 18 cars (PENDING)

### Research Documents
- `docs/research/2026-06-08-bottom-buyer-analysis.md` — Original analysis (443 lines)
- `docs/research/2026-06-08-leno-act-smog-exemption-analysis.md` — Leno Act / CARB (416 lines)
- `docs/research/2026-06-08-mercedes-engineering-deep-dive.md` — Mercedes engineering (732 lines)

### Plans
- `docs/superpowers/plans/2026-06-08-full-backfill-and-research.md` — Implementation plan

---

## How to Resume

### Step 1: Retry the 3 remaining agent groups
For each group, spawn a `deep` agent with this prompt template:

```
[CONTEXT]: MotorGeek car database backfill. We're scoring the last batch of cars
for reliability (5 dimensions) and build quality/Q-factor (6 dimensions). The DB
is at data/motorgeek.db. 112/157 cars are already scored.

[GOAL]: Score [GROUP_NAME] cars and write SQL file to data/sql_inserts/add_scores_[filename].sql

[INSTRUCTIONS]:
1. Read motorgeek/core/scoring.py and motorgeek/core/scoring_build.py for aggregate formulas
2. Read any existing SQL file (e.g., add_scores_american.sql) for INSERT format reference
3. Read the cars table to get car_id values: sqlite3 data/motorgeek.db "SELECT id, make, model FROM cars WHERE make IN ([makes]) ORDER BY id"
4. Research each car and assign dimensional scores (0-100)
5. Compute aggregates using the exact formulas
6. Write SQL file with INSERT statements
7. Verify the SQL loads: sqlite3 data/motorgeek.db ".read data/sql_inserts/add_scores_[filename].sql"

[RELIABILITY DIMENSIONS]: engine(0.25), transmission(0.25), chassis(0.15), electronics(0.15), ease_of_repair(0.20)
Catastrophe penalty if any dimension < 50: penalty = 0.85 + (min/50)*0.15

[Q-FACTOR DIMENSIONS]: body_construction(0.25), nvh_isolation(0.10), interior_materials(0.20), paint_corrosion(0.15), electrical_aging(0.15), cosmetic_aging(0.15)
No penalty.

[COLUMN NAMES]: reliability uses score_ease_of_repair (NOT ease_of_repair)
build_quality uses score_body_construction, score_nvh_isolation, score_interior_materials, score_paint_corrosion, score_electrical_aging, score_cosmetic_aging

[CARS TO SCORE]:
[List car IDs and models]

[ID RANGES]:
Reliability: [start]-[end]
Build Quality: [start]-[end]

[CALIBRATION REFERENCE]: LS430 Rel=88.5 Q=92.3 (best). Infiniti Q50 Rel=39.6 Q=39.6 (worst).
```

#### Group Details:

**Toyota+Honda+Acura (13 cars)**
```
sqlite3 data/motorgeek.db "SELECT id, make, model FROM cars WHERE make IN ('Toyota','Honda','Acura') AND id NOT IN (SELECT car_id FROM reliability) ORDER BY id"
```
Reliability IDs: 214-226, Build Quality IDs: 71-83

**Nissan+Mitsubishi+Subaru (14 cars)**
```
sqlite3 data/motorgeek.db "SELECT id, make, model FROM cars WHERE make IN ('Nissan','Mitsubishi','Subaru') AND id NOT IN (SELECT car_id FROM reliability) ORDER BY id"
```
Reliability IDs: 227-240, Build Quality IDs: 84-97

**Audi+Porsche+VW (18 cars)**
```
sqlite3 data/motorgeek.db "SELECT id, make, model FROM cars WHERE make IN ('Audi','Porsche','Volkswagen') AND id NOT IN (SELECT car_id FROM reliability) ORDER BY id"
```
Reliability IDs: 254-265*, Build Quality IDs: 105-122
*Verify these IDs don't conflict before use.

### Step 2: Verify all 157 cars
```sql
-- Check for cars missing reliability scores
SELECT c.id, c.make, c.model FROM cars c
LEFT JOIN reliability r ON c.id = r.car_id
WHERE r.id IS NULL;

-- Check for cars missing build quality scores
SELECT c.id, c.make, c.model FROM cars c
LEFT JOIN build_quality b ON c.id = b.car_id
WHERE b.id IS NULL;
```

### Step 3: Run verification
```bash
pytest  # Should still be 22/22
python scripts/bottom_buyer_tco.py  # Should show all 157 cars with Q scores
```

### Step 4: Stream 5 research
- NA vs Turbo reliability gap analysis
- Brand tier rankings across all dimensions

### Step 5: Final commit

---

## User Context
- California-based "bottom buyer" — buys deeply depreciated luxury cars, drives 30K more miles
- Engineering enthusiast — cares about metallurgy, bearing specs, failure modes
- Q-factor weights favor body structure (25%) over NVH (10%) per user preference
- All data sourced as `source='sample'`
- EV mapping: engine→motor/drivetrain, transmission→reduction gear
- Fuel prices: NA 87 octane $3.20, turbo 91 octane $3.80

# Full Backfill & Research Expansion Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Backfill all 100 unscored cars with reliability + Q-factor, upgrade TCO with Q-factor, and produce 4 research documents.

**Architecture:** 8 parallel backfill agents (grouped by manufacturer), each producing SQL files with both reliability and build_quality INSERTs. 4 additional agents for TCO upgrade + research docs. Final verification sweep across all new data.

**Tech Stack:** Python, SQLite, SQL INSERTs, `motorgeek/core/scoring.py`, `motorgeek/core/scoring_build.py`

---

## Stream 1: 100-Car Backfill (8 parallel agents)

### Scoring Systems

**Reliability (5 dimensions, weighted):**
- Engine: 25% (`score_engine`)
- Transmission: 25% (`score_transmission`)
- Chassis: 15% (`score_chassis`)
- Electronics: 15% (`score_electronics`)
- Ease of Repair: 20% (`score_ease_of_repair`)
- Catastrophe penalty: if any dimension < 50, `penalty = 0.85 + (min/50) * 0.15`, then `raw * penalty`
- Aggregate function: `compute_reliability_aggregate()` in `motorgeek/core/scoring.py`

**Q-Factor Build Quality (6 dimensions, weighted):**
- Body Construction: 25% (`score_body_construction`)
- NVH Isolation: 10% (`score_nvh_isolation`)
- Interior Materials: 20% (`score_interior_materials`)
- Paint/Corrosion: 15% (`score_paint_corrosion`)
- Electrical Aging: 15% (`score_electrical_aging`)
- Cosmetic Aging: 15% (`score_cosmetic_aging`)
- NO catastrophe penalty
- Aggregate function: `compute_build_aggregate()` in `motorgeek/core/scoring_build.py`

**EV Adaptations:** For electric vehicles, map:
- Engine → Motor/Drivetrain (same weight)
- Transmission → Reduction Gear (same weight)

### ID Ranges

- Reliability: starts at ID 202 (max existing = 201)
- Build Quality: starts at ID 59 (max existing = 58)

### Group Assignments

| Group | Manufacturer | Cars | IDs | Rel IDs | BQ IDs | SQL File |
|---|---|---|---|---|---|---|
| 1 | BMW | 12 | 37,41,23,106,19,13,65,120,51,50,52,123 | 202-213 | 59-70 | `add_scores_bmw.sql` |
| 2 | Toyota+Honda+Acura | 13 | 80,103,119,108,97,16,20,118,99,113,48,88,28 | 214-226 | 71-83 | `add_scores_toyota_honda_acura.sql` |
| 3 | Nissan+Mitsu+Subaru | 14 | 110,121,111,58,59,57,102,131,60,61,84,93,95,94 | 227-240 | 84-97 | `add_scores_nissan_mitsu_subaru.sql` |
| 4 | Mercedes-Benz+AMG | 7 | 82,79,67,122,53,42,117 | 241-247 | 98-104 | `add_scores_mercedes_amg.sql` |
| 5 | Audi+Porsche+VW | 18 | 22,43,114,66,101,125,104,18,21,17,49,10,96,12,62,132,133,134 | 248-265 | 105-122 | `add_scores_audi_porsche_vw.sql` |
| 6 | American | 16 | 107,81,128,129,112,11,130,105,85,27,100,26,36,69,127,126 | 266-281 | 123-138 | `add_scores_american.sql` |
| 7 | Mazda | 6 | 92,14,91,89,109,90 | 282-287 | 139-144 | `add_scores_mazda.sql` |
| 8 | Exotics+EVs+Misc | 14 | 15,46,55,68,71,70,72,73,75,115,116,124,76,74 | 288-301 | 145-158 | `add_scores_exotics_evs_misc.sql` |

### SQL Templates

**Reliability INSERT pattern:**
```sql
-- [Car Name] (id [car_id]) — Score: [score]
-- [Brief justification]
INSERT INTO reliability (id, car_id, source, reliability_score,
    score_engine, score_transmission, score_chassis, score_electronics, score_ease_of_repair,
    common_failures, avg_repair_cost, recall_count, part_availability, diy_friendliness, known_issues)
VALUES (
  [rel_id], [car_id], 'sample', [reliability_score],
  [engine], [transmission], [chassis], [electronics], [ease],
  '{"failure1": severity, "failure2": severity}', [avg_cost], [recall_count],
  '[availability]', '[diy_friendly]',
  '{"key": "value"}'
);
```

**Build Quality INSERT pattern:**
```sql
-- [Car Name] (id [car_id]) — Q-Score: [q_score]
-- [Brief justification]
INSERT INTO build_quality (
    car_id, q_score,
    score_body_construction, score_nvh_isolation, score_interior_materials,
    score_paint_corrosion, score_electrical_aging, score_cosmetic_aging,
    body_construction_notes, nvh_isolation_notes, interior_materials_notes,
    paint_corrosion_notes, electrical_aging_notes, cosmetic_aging_notes,
    q_score_notes,
    platform_type, assembly_plant, weld_technology, panel_gap_mm,
    engine_mount_type, glass_type, leather_grade, wood_type,
    paint_stages, sound_deadening_rating, source
) VALUES (
    [car_id], [q_score],
    [body], [nvh], [interior],
    [paint], [electrical], [cosmetic],
    '[body notes]', '[nvh notes]', '[interior notes]',
    '[paint notes]', '[electrical notes]', '[cosmetic notes]',
    '[overall notes]',
    '[platform_type]', '[assembly_plant]', '[weld_tech]', [panel_gap],
    '[mount_type]', '[glass_type]', '[leather_grade]', '[wood_type]',
    [paint_stages], '[sound_deadening]', 'sample'
);
```

### Verification Protocol

After each agent produces SQL:
1. Run `.read data/sql_inserts/add_scores_[group].sql` against `data/motorgeek.db`
2. Verify all Q-factor scores match `compute_build_aggregate()` output
3. Verify all reliability scores match `compute_reliability_aggregate()` output (including catastrophe penalty)
4. Check for: 0 orphan rows, 0 out-of-range scores (0-100), 0 NULL dimensions

---

## Stream 2: TCO Upgrade — Q-Factor Integration

**File:** `scripts/bottom_buyer_tco.py`

### Changes:
1. Add LEFT JOIN to `build_quality` table in SQL query
2. Pull `q_score` into car data dict
3. Add Q-factor column to output table
4. **Maintenance adjustment:** High Q (>80) → reduce age escalation from 1.3x to 1.15x. Low Q (<60) → increase to 1.5x
5. **Depreciation adjustment:** High Q → add 5% to `base_pct` (better value retention). Low Q → subtract 5%
6. **Risk buffer adjustment:** High Q → reduce probability by 3pp. Low Q → increase by 5pp
7. **New "Q-Adjusted $/mile" metric** that incorporates build quality into the cost projection

---

## Stream 3: Leno Act Smog Exemption Analysis

**File:** `docs/research/2026-06-08-leno-act-smog-exemption-analysis.md`

### Structure:
1. Current CA smog law (1975 cutoff, biennial OBD2 for 2000+)
2. Leno's Law (SB 712/SB 1392) — history, current status, prospects
3. 3 scenarios: Never passes / Passes 2028 / Passes 2030
4. LS430 price modeling under each scenario
5. G90 Tau implications (newer car, no exemption benefit)
6. Collector car market parallels (Porsche 964/993 smog exemption price jumps)

---

## Stream 4: Mercedes Engineering Deep Dive

**File:** `docs/research/2026-06-08-mercedes-engineering-deep-dive.md`

### Structure:
1. Platform timeline: W124 → W210 → W211 → W212 → W213
2. Engine evolution: M112 → M272 → M276 → M256
3. M256 48V ISG — engineering deep dive (belt starter-generator, EQ Boost)
4. Transmission wars: 722.6 (5G) → 722.9 (7G) → 9G-Tronic
5. C-Class: W204 vs W205 (the complexity cliff)
6. E-Class: W212 vs W213 (the software-defined car)
7. AMG evolution: C450 → C43 → C63 S E-Performance (the electrification trap)
8. Bottom-buyer implications per model

---

## Stream 5: Expanded Research Docs

### Doc 1: `docs/research/2026-06-08-na-vs-turbo-reliability-gap.md`
- Statistical analysis: NA vs turbo reliability scores across all 157 cars
- By manufacturer, by era, by displacement
- Carbon buildup, heat soak, boost pressure as failure multipliers

### Doc 2: `docs/research/2026-06-08-brand-tier-rankings.md`
- Aggregate scores by manufacturer
- Tier classification (S/A/B/C/D)
- Best/worst car per brand
- Cross-dimensional radar charts (text-based)

---

## Execution Order

All streams run in **parallel**:
- 8 backfill agents (Stream 1) — dispatched simultaneously
- TCO upgrade agent (Stream 2) — dispatched immediately
- Leno Act research agent (Stream 3) — dispatched with librarian background research
- Mercedes deep dive agent (Stream 4) — dispatched with session history search
- Research docs agents (Stream 5) — dispatched after enough data exists

**Final step:** After all backfill agents complete:
1. Run full verification across all 157 cars
2. Run updated TCO script
3. Commit everything

# Q-Factor (Build Quality) Table Design

## Problem

Our 5-dimensional reliability scoring (engine, transmission, chassis, electronics, ease_of_repair) captures **mechanical reliability** well. But it completely misses **how a car is built and how it ages cosmetically**.

Example: The LS430 (88.5) and ES 350 (87.8) are only 0.7 points apart mechanically, but the LS has:
- Laser welding (world first production car)
- Hydraulic engine mounts ("mini suspension for the engine")
- Sandwich steel bulkheads with sound-insulating resin cores
- Semi-aniline leather, real walnut wood
- Acoustic laminated glass standard
- 10x tighter body digitization (0.001mm vs 0.01mm)
- Tahara plant Takumi inspection (~60 inspectors per car)

None of this shows up in our data. Similarly, the G35 Coupe (80.9) scores close to the ES 350 (87.8) mechanically, but the G35 has endemic dash cracking, universal Bose radio failure, clear coat epidemics, and seat bolsters that collapse at 40K miles. Our scoring system is blind to all of it.

## Solution

Add a `build_quality` table with 6 dimensional subscores (0-100), text evidence fields for agent defensibility, and structural metadata columns for queryable comparisons. Composite Q-score computed via custom weights that reflect the user's engineering-geek bias.

## Design Decisions

### Separate table (not extending `reliability`)
- Reliability and build quality are fundamentally different concepts
- `reliability` already has 12 columns; adding 20+ more violates SRP
- Separate table = separate scoring logic, separate agent prompts, cleaner queries
- Follows existing pattern: each domain gets its own table + scoring module

### Hybrid scoring (numeric + text evidence)
- Numeric 0-100 subscores for each dimension (computable, sortable, aggregatable)
- Text notes per dimension for agent defensibility: "LS430 has laser welding world first, welds 1.5x stronger than industry standard"
- Future agents can read the text, verify the score, and add their own evidence

### Two score groups: Build Precision vs Aging Durability
- **Build Precision**: body_construction, nvh_isolation, interior_materials
- **Aging Durability**: paint_corrosion, electrical_aging, cosmetic_aging
- The composite aggregates both, but the groups are distinct for analysis

### Custom weights with engineering bias
```python
BUILD_WEIGHTS = {
    'body_construction':   0.25,  # engineering geek priority
    'nvh_isolation':       0.10,  # nice but not critical for user
    'interior_materials':  0.20,
    'paint_corrosion':     0.15,
    'electrical_aging':    0.15,
    'cosmetic_aging':      0.15,
}
```

## Schema

### Table: `build_quality`

```
id                          INTEGER PK
car_id                      INTEGER FK → cars (UNIQUE)

-- Composite score
q_score                     FLOAT          -- weighted aggregate 0-100

-- Build Precision subscores (factory quality)
score_body_construction     FLOAT          -- panel gaps, welds, platform, structural rigidity
score_nvh_isolation         FLOAT          -- engine mounts, acoustic glass, sound deadening, cabin dB
score_interior_materials    FLOAT          -- leather grade, wood type, soft-touch, gauges, fitting tolerance

-- Aging Durability subscores (how it holds up)
score_paint_corrosion       FLOAT          -- clear coat durability, rust resistance, paint stages
score_electrical_aging      FLOAT          -- radio failures, sensor gremlins, wiring degradation
score_cosmetic_aging        FLOAT          -- dash cracking, seat wear, trim detachment, headliner sag

-- Text evidence (agent-defensible scoring justification)
body_construction_notes     TEXT
nvh_isolation_notes         TEXT
interior_materials_notes    TEXT
paint_corrosion_notes       TEXT
electrical_aging_notes      TEXT
cosmetic_aging_notes        TEXT
q_score_notes               TEXT           -- overall justification

-- Structural metadata (queryable, comparison-useful)
platform_type               VARCHAR(50)    -- bespoke / shared / derived
assembly_plant              VARCHAR(100)   -- e.g. "Tahara (Aichi, Japan)"
weld_technology             VARCHAR(50)    -- laser / spot / mixed
panel_gap_mm                FLOAT          -- approximate, e.g. 3.5
engine_mount_type           VARCHAR(50)    -- hydraulic / rubber / polyurethane / active
glass_type                  VARCHAR(100)   -- acoustic_laminated / laminated / standard
leather_grade               VARCHAR(50)    -- semi_aniline / full_aniline / standard / synthetic
wood_type                   VARCHAR(50)    -- real_wood / wood_grain / plastic / none
paint_stages                INTEGER        -- number of paint stages (3-6 typical)
sound_deadening_rating      VARCHAR(50)    -- ENUM: extensive / above_average / standard / minimal
                                          -- extensive = dedicated NVH engineering (LS430, S-Class)
                                          -- above_average = enhanced over base (ES 350, 5 Series)
                                          -- standard = platform-standard (Camry, 3 Series)
                                          -- minimal = performance-first, NVH sacrificed (G35, F355)

-- Metadata
source                      VARCHAR(200)
extra                       JSON

created_at                  DATETIME
updated_at                  DATETIME
```

### New files

1. **`motorgeek/core/models.py`** — Add `BuildQuality` ORM class + relationship on `Car`
2. **`motorgeek/core/scoring_build.py`** — New scoring module:
   ```python
   BUILD_DIMENSIONS = ['body_construction', 'nvh_isolation', 'interior_materials',
                       'paint_corrosion', 'electrical_aging', 'cosmetic_aging']
   BUILD_WEIGHTS = {
       'body_construction':   0.25,
       'nvh_isolation':       0.10,
       'interior_materials':  0.20,
       'paint_corrosion':     0.15,
       'electrical_aging':    0.15,
       'cosmetic_aging':      0.15,
   }
   ```
   Same pattern as `scoring.py`: `compute_build_aggregate()`, `get_build_score_dict()`, `recompute_build_aggregate()`

3. **Alembic migration** — Create `build_quality` table

### Scoring anchors (calibration reference)

These are the known-reference cars that anchor the 0-100 scale for each dimension:

| Dimension | 100 reference | 80 reference | 60 reference | 40 reference |
|---|---|---|---|---|
| body_construction | LS430 (laser welding, 0.001mm, bespoke platform) | 540i LCI (good, shared CLAR) | G80 3.8L (adequate, shared) | Q50 Red Sport (cost-cut structure) |
| nvh_isolation | LS430 (hydraulic mounts, sandwich steel, acoustic glass) | ES 350 (quiet but rubber mounts) | G35 Coupe (noisy by design) | F355 (race car with plates) |
| interior_materials | LS430 (semi-aniline, real walnut, 1mm tolerance) | ES 350 (standard leather, real wood some trims) | G80 5.0 (good but Hyundai-grade plastics) | G35 Coupe (printed wood, mediocre leather) |
| paint_corrosion | LS400 (20+ year paint still factory-fresh) | ES 350 (good, no rust issues) | E-Class W212 (average, some clear coat) | G35 Coupe (clear coat epidemic, rear quarter rust) |
| electrical_aging | ES 350 (everything works at 150K+) | LS430 (reliable, some air susp sensors) | G80 3.8L (typical Hyundai electronics) | G35 Coupe (universal Bose failure, AC integration) |
| cosmetic_aging | LS430 (still looks new at 20 years) | ES 350 (graceful aging, minor wear) | 540i LCI (typical BMW plastics age) | G35 Coupe (dash cracks, seat collapse, trim falls off) |

### Integration with bottom-buyer TCO

The Q-score should feed into the bottom-buyer analysis:
- Cars with high Q-scores will **look and feel better** at high mileage, improving the ownership experience
- Cars with low Q-scores may need cosmetic investment ($2-4K deferred maintenance) that the TCO script should account for
- A future `depreciation_quality_penalty` could adjust used-price estimates: "this car will look rough at 130K, reducing resale/scrap value"

### Backfill priority

Cars to score first (by research availability and bottom-buyer relevance):
1. **LS430** — we have extensive research, benchmark car
2. **ES 350** — direct comparison, research available
3. **G35 Coupe** — contrast case, research available from this session
4. **G80 5.0 Tau** — user interest, research available
5. **540i pre-LCI / LCI** — comparison anchors
6. **W212 E-Class** — mid-pack reference
7. **G90 5.0 Tau** — comparison with G80

## Out of Scope

- Modifying the existing `reliability` table or scoring
- Adding Q-factor to the web UI (backend only for now)
- Auto-scoring from data sources (manual + agent-assisted only)
- Paint/corrosion as a separate maintenance tracking table

# Q-Factor Build Quality Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `build_quality` table with 6 dimensional subscores (body_construction, nvh_isolation, interior_materials, paint_corrosion, electrical_aging, cosmetic_aging), text evidence fields, structural metadata, and a composite Q-score with custom weights.

**Architecture:** New `BuildQuality` ORM model mirroring the existing `Reliability` pattern. New `scoring_build.py` module mirroring `scoring.py`. Alembic migration creates the table. No changes to existing `reliability` table or `scoring.py`.

**Tech Stack:** SQLAlchemy (existing ORM), Alembic (existing migrations), SQLite (existing DB)

---

### Task 1: Write failing tests for scoring_build.py

**Files:**
- Create: `tests/test_scoring_build.py`

- [ ] **Step 1: Write the test file**

```python
"""Tests for build quality dimensional scoring."""
from motorgeek.core.scoring_build import (
    compute_build_aggregate,
    get_build_score_dict,
    BUILD_DIMENSIONS,
    BUILD_WEIGHTS,
)


class TestBuildWeights:
    """Weights must sum to 1.0 and cover all dimensions."""

    def test_weights_sum_to_one(self):
        assert sum(BUILD_WEIGHTS.values()) == 1.0

    def test_all_dimensions_have_weights(self):
        for dim in BUILD_DIMENSIONS:
            assert dim in BUILD_WEIGHTS

    def test_six_dimensions(self):
        assert len(BUILD_DIMENSIONS) == 6


class TestComputeBuildAggregate:
    """Aggregate computation mirrors reliability scoring pattern."""

    def test_all_scores_present(self):
        scores = {
            'body_construction': 90,
            'nvh_isolation': 85,
            'interior_materials': 88,
            'paint_corrosion': 82,
            'electrical_aging': 80,
            'cosmetic_aging': 78,
        }
        result = compute_build_aggregate(scores)
        # 90*0.25 + 85*0.10 + 88*0.20 + 82*0.15 + 80*0.15 + 78*0.15
        # = 22.5 + 8.5 + 17.6 + 12.3 + 12.0 + 11.7 = 84.6
        assert result == 84.6

    def test_min_three_dimensions_required(self):
        scores = {
            'body_construction': 90,
            'nvh_isolation': 85,
        }
        result = compute_build_aggregate(scores)
        assert result is None

    def test_three_dimensions_ok(self):
        scores = {
            'body_construction': 90,
            'nvh_isolation': 85,
            'interior_materials': 88,
        }
        result = compute_build_aggregate(scores)
        assert result is not None
        assert isinstance(result, float)

    def test_null_dimensions_excluded(self):
        scores = {
            'body_construction': 90,
            'nvh_isolation': None,
            'interior_materials': 88,
            'paint_corrosion': 82,
            'electrical_aging': 80,
            'cosmetic_aging': 78,
        }
        result = compute_build_aggregate(scores)
        # Should redistribute nvh_isolation weight among remaining 5
        assert result is not None

    def test_perfect_score(self):
        scores = {dim: 100 for dim in BUILD_DIMENSIONS}
        result = compute_build_aggregate(scores)
        assert result == 100.0

    def test_zero_score(self):
        scores = {dim: 0 for dim in BUILD_DIMENSIONS}
        result = compute_build_aggregate(scores)
        assert result == 0.0

    def test_rounded_to_one_decimal(self):
        scores = {
            'body_construction': 92,
            'nvh_isolation': 77,
            'interior_materials': 85,
            'paint_corrosion': 90,
            'electrical_aging': 88,
            'cosmetic_aging': 83,
        }
        result = compute_build_aggregate(scores)
        # Check it's rounded to 1 decimal
        assert result == round(result, 1)

    def test_extra_keys_ignored(self):
        scores = {
            'body_construction': 90,
            'nvh_isolation': 85,
            'interior_materials': 88,
            'paint_corrosion': 82,
            'electrical_aging': 80,
            'cosmetic_aging': 78,
            'not_a_real_dimension': 50,
        }
        result = compute_build_aggregate(scores)
        assert result == 84.6  # same as without extra key


class TestGetBuildScoreDict:
    """Extract scores from a mock BuildQuality object."""

    def test_extracts_all_dimensions(self):
        class MockBQ:
            score_body_construction = 90
            score_nvh_isolation = 85
            score_interior_materials = 88
            score_paint_corrosion = 82
            score_electrical_aging = 80
            score_cosmetic_aging = 78
        result = get_build_score_dict(MockBQ())
        assert len(result) == 6
        assert result['body_construction'] == 90

    def test_none_scores_preserved(self):
        class MockBQ:
            score_body_construction = 90
            score_nvh_isolation = None
            score_interior_materials = 88
            score_paint_corrosion = None
            score_electrical_aging = 80
            score_cosmetic_aging = 78
        result = get_build_score_dict(MockBQ())
        assert result['nvh_isolation'] is None
        assert result['body_construction'] == 90
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_scoring_build.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'motorgeek.core.scoring_build'`

---

### Task 2: Create scoring_build.py module

**Files:**
- Create: `motorgeek/core/scoring_build.py`

- [ ] **Step 1: Write the scoring module**

```python
"""Build quality dimensional scoring — aggregate Q-factor computation."""

BUILD_DIMENSIONS = [
    'body_construction',
    'nvh_isolation',
    'interior_materials',
    'paint_corrosion',
    'electrical_aging',
    'cosmetic_aging',
]

# Custom weights: engineering-geek bias toward body_construction,
# lower weight on nvh_isolation (user preference).
BUILD_WEIGHTS = {
    'body_construction':  0.25,
    'nvh_isolation':      0.10,
    'interior_materials': 0.20,
    'paint_corrosion':    0.15,
    'electrical_aging':   0.15,
    'cosmetic_aging':     0.15,
}

MIN_DIMENSIONS_FOR_AGGREGATE = 3


def compute_build_aggregate(scores: dict[str, float | None]) -> float | None:
    """Compute weighted aggregate Q-score from dimensional subscores.

    Requires at least 3 of 6 dimensions to be non-NULL.
    Weights are redistributed proportionally for NULL dimensions.
    """
    present = {k: v for k, v in scores.items()
               if v is not None and k in BUILD_WEIGHTS}
    if len(present) < MIN_DIMENSIONS_FOR_AGGREGATE:
        return None

    weight_sum = sum(BUILD_WEIGHTS[k] for k in present)
    adjusted = {k: BUILD_WEIGHTS[k] / weight_sum for k in present}
    raw = sum(present[k] * adjusted[k] for k in present)

    return round(raw, 1)


def get_build_score_dict(bq) -> dict[str, float | None]:
    """Extract dimensional scores from a BuildQuality ORM object."""
    return {
        'body_construction': bq.score_body_construction,
        'nvh_isolation': bq.score_nvh_isolation,
        'interior_materials': bq.score_interior_materials,
        'paint_corrosion': bq.score_paint_corrosion,
        'electrical_aging': bq.score_electrical_aging,
        'cosmetic_aging': bq.score_cosmetic_aging,
    }


def recompute_build_aggregate(bq) -> float | None:
    """Recompute and update the q_score on a BuildQuality object."""
    scores = get_build_score_dict(bq)
    new_score = compute_build_aggregate(scores)
    if new_score is not None:
        bq.q_score = new_score
    return new_score
```

- [ ] **Step 2: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_scoring_build.py -v`
Expected: All 10 tests PASS

- [ ] **Step 3: Commit**

```bash
git add motorgeek/core/scoring_build.py tests/test_scoring_build.py
git commit -m "feat: add build quality scoring module with 6 dimensions and custom weights"
```

---

### Task 3: Add BuildQuality ORM model

**Files:**
- Modify: `motorgeek/core/models.py` (add class after `Reliability`, add relationship on `Car`)

- [ ] **Step 1: Add relationship on Car class**

In the `Car` class (around line 53, after the `reliability` relationship), add:

```python
    build_quality: Mapped[Optional["BuildQuality"]] = relationship(
        "BuildQuality", back_populates="car", uselist=False
    )
```

- [ ] **Step 2: Add BuildQuality class after Reliability class (after line 263)**

```python
class BuildQuality(Base):
    __tablename__ = "build_quality"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False, unique=True)

    # Composite Q-score
    q_score: Mapped[Optional[float]] = mapped_column(Float)

    # Build Precision subscores (factory quality)
    score_body_construction: Mapped[Optional[float]] = mapped_column(Float)
    score_nvh_isolation: Mapped[Optional[float]] = mapped_column(Float)
    score_interior_materials: Mapped[Optional[float]] = mapped_column(Float)

    # Aging Durability subscores (how it holds up)
    score_paint_corrosion: Mapped[Optional[float]] = mapped_column(Float)
    score_electrical_aging: Mapped[Optional[float]] = mapped_column(Float)
    score_cosmetic_aging: Mapped[Optional[float]] = mapped_column(Float)

    # Text evidence (agent-defensible scoring justification)
    body_construction_notes: Mapped[Optional[str]] = mapped_column(Text)
    nvh_isolation_notes: Mapped[Optional[str]] = mapped_column(Text)
    interior_materials_notes: Mapped[Optional[str]] = mapped_column(Text)
    paint_corrosion_notes: Mapped[Optional[str]] = mapped_column(Text)
    electrical_aging_notes: Mapped[Optional[str]] = mapped_column(Text)
    cosmetic_aging_notes: Mapped[Optional[str]] = mapped_column(Text)
    q_score_notes: Mapped[Optional[str]] = mapped_column(Text)

    # Structural metadata (queryable, comparison-useful)
    platform_type: Mapped[Optional[str]] = mapped_column(String(50))
    assembly_plant: Mapped[Optional[str]] = mapped_column(String(100))
    weld_technology: Mapped[Optional[str]] = mapped_column(String(50))
    panel_gap_mm: Mapped[Optional[float]] = mapped_column(Float)
    engine_mount_type: Mapped[Optional[str]] = mapped_column(String(50))
    glass_type: Mapped[Optional[str]] = mapped_column(String(100))
    leather_grade: Mapped[Optional[str]] = mapped_column(String(50))
    wood_type: Mapped[Optional[str]] = mapped_column(String(50))
    paint_stages: Mapped[Optional[int]] = mapped_column(Integer)
    sound_deadening_rating: Mapped[Optional[str]] = mapped_column(String(50))

    # Metadata
    source: Mapped[Optional[str]] = mapped_column(String(200))
    extra: Mapped[Optional[Any]] = mapped_column(JSON, default=dict)

    car: Mapped["Car"] = relationship("Car", back_populates="build_quality")
```

Note: `Text`, `JSON`, `Float`, `Integer`, `String` are already imported at the top of models.py. `Optional` and `Any` from typing are also already imported.

- [ ] **Step 3: Verify no import errors**

Run: `python3 -c "from motorgeek.core.models import BuildQuality; print('OK')"`
Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add motorgeek/core/models.py
git commit -m "feat: add BuildQuality ORM model with 6 dimensions + metadata"
```

---

### Task 4: Generate and run Alembic migration

**Files:**
- Create: `alembic/versions/<auto>_add_build_quality_table.py` (auto-generated)

- [ ] **Step 1: Generate migration**

Run: `cd C:\Users\llama\OneDrive\proj\motorgeek; alembic revision --autogenerate -m "add build_quality table"`

Expected: New migration file created in `alembic/versions/`

- [ ] **Step 2: Inspect the generated migration**

Open the new migration file. Verify it contains:
- `op.create_table('build_quality', ...)` with all columns
- `downgrade()` has `op.drop_table('build_quality')`

- [ ] **Step 3: Run migration**

Run: `alembic upgrade head`
Expected: No errors

- [ ] **Step 4: Verify table exists**

Run: `sqlite3 data/motorgeek.db ".schema build_quality"`
Expected: Full CREATE TABLE statement with all columns

- [ ] **Step 5: Commit**

```bash
git add alembic/versions/
git commit -m "feat: add Alembic migration for build_quality table"
```

---

### Task 5: Seed first build quality data (LS430)

**Files:**
- Create: `data/sql_inserts/add_ls430_build_quality.sql`

- [ ] **Step 1: Write the SQL insert**

Using data from our librarian research for the LS430 (car_id=39):

```sql
-- LS430 Build Quality Q-factor (car_id=39)
-- Based on extensive librarian research from bg_ee00e560

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
    39,
    94.7,
    -- Build Precision
    97, 95, 94,
    -- Aging Durability
    93, 82, 90,
    -- Text evidence
    'LS430 bespoke F1 platform. World-first laser welding on LS400 (carried forward). Welds 1.5x stronger than industry standard. Body digitization 0.001mm (10x industry). High-tensile steel cabin cage. Double-wishbone suspension all corners. Sandwich steel bulkheads with sound-insulating resin cores.',
    'Hydraulic fluid-filled engine mounts (mini suspension for engine). Sandwich steel bulkheads. Acoustic laminated glass front+rear standard. Hollow-spoke wheels for road noise. Helmholtz resonators in door cavities. Aerodynamic underbody with flat engine cover. 58dB at 100km/h (LS400 benchmark).',
    'Semi-aniline leather (highest automotive grade). Real California walnut, antique walnut, bird''s eye maple. Optitron electroluminescent gauges. Interior tolerance 1mm. 24 woods and multiple leathers evaluated for 2 years during development.',
    'LS400/430 paint holds 20+ years. Multi-stage Toyota paint process. Corrosion-resistant galvanized steel. Wax and hemming sealers. No known clear coat epidemics. Owners report factory-fresh appearance at 15+ years.',
    'Generally excellent electrical reliability. Air suspension sensors can fail (40% of UL owners). Motorized features add complexity. No systemic electrical gremlins like G35 Bose failure. Mark Levinson audio holds up well.',
    'Interior holds up remarkably at 20+ years. Semi-aniline leather ages gracefully (patina vs cracking). Real wood doesn''t delaminate. Tighter panel gaps prevent squeaks/rattles. Air suspension can sag if not maintained. Rubber components softer for NVH = degrade faster than ES.',
    'LS430 Q-score 94.7. The benchmark car for build quality in our database. Bespoke platform, world-first engineering, highest material grades, Tahara Takumi assembly. Deductions: air suspension aging (-3 electrical), softer rubber aging (-5 cosmetic), motorized features add failure points.',
    -- Structural metadata
    'bespoke', 'Tahara (Aichi, Japan)', 'laser', 3.5,
    'hydraulic', 'acoustic_laminated', 'semi_aniline', 'real_wood',
    5, 'extensive', 'sample'
);
```

- [ ] **Step 2: Execute the insert**

Run: `cd C:\Users\llama\OneDrive\proj\motorgeek; sqlite3 data/motorgeek.db ".read data/sql_inserts/add_ls430_build_quality.sql"`

- [ ] **Step 3: Verify the data**

Run: `sqlite3 -header -column data/motorgeek.db "SELECT car_id, printf('%.1f',q_score) as q_score, score_body_construction as body, score_nvh_isolation as nvh, score_interior_materials as interior, score_paint_corrosion as paint, score_electrical_aging as elec, score_cosmetic_aging as cosmetic, platform_type, assembly_plant, leather_grade, wood_type FROM build_quality WHERE car_id=39"`

Expected: One row with q_score=94.7, all scores filled, metadata populated.

- [ ] **Step 4: Commit**

```bash
git add data/sql_inserts/add_ls430_build_quality.sql
git commit -m "feat: add LS430 build quality Q-factor data"
```

---

### Task 6: Seed contrast data (ES 350, G35 Coupe)

**Files:**
- Create: `data/sql_inserts/add_es350_g35_build_quality.sql`

- [ ] **Step 1: Write the SQL**

```sql
-- ES 350 Build Quality Q-factor (car_id=86)
-- Good but not LS-tier: Camry platform, rubber mounts, standard leather

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
    86,
    76.3,
    -- Build Precision
    72, 80, 76,
    -- Aging Durability
    78, 85, 82,
    -- Text evidence
    'Camry K-platform derivative. MacPherson strut front (not double wishbone). Pressed steel subframes (not aluminum). Standard Toyota spot welding. Panel gaps 5-7mm (good but not LS-grade 3-4mm). Shared platform = shared tooling.',
    'Enhanced over Camry: additional sound deadening in floor pan, firewall, doors. 2GR-FE inherently smooth. But standard rubber engine mounts (not hydraulic). No acoustic laminated glass on base models. No sandwich steel bulkheads. Whisper-quiet but through insulation quantity, not engineering sophistication.',
    'Standard leather (not semi-aniline). Real wood on some trims, wood-grain plastic on lower trims. Standard backlit gauges (not Optitron). Good soft-touch surfaces. Panel fit tighter than G35 but not LS-level. Interior tolerance standard 3-5mm.',
    'Toyota paint of this era is average-to-good. No clear coat epidemics. Rust uncommon unless accident-damaged. Good galvanized steel. Some minor clear coat aging on horizontal surfaces at 15+ years but gradual.',
    'Stone-cold reliable electrically. Everything works at 150K+ miles. Mark Levinson optional system holds up. No systemic gremlins. 2007-2008 had floor mat recall. GPS dated but functional.',
    'Ages gracefully like a well-maintained Camry. 2007-2008 dash melting was addressed by Lexus warranty program ZLD (free replacement). 2010+ models avoided it. Leather holds up at 100K+. Softer plastics scratch more than LS. Faux wood can fade.',
    'ES 350 Q-score 76.3. Honest Camry-based luxury: mechanically bulletproof, cosmetically good but shared-platform DNA shows. 80-90% of LS NVH at 70% of the materials cost. Not bespoke engineering but efficient application of good fundamentals.',
    -- Structural metadata
    'shared', 'Multiple (Kyushu, Tsutsumi)', 'spot', 5.5,
    'rubber', 'laminated', 'standard', 'real_wood',
    4, 'above_average', 'sample'
);

-- G35 Coupe Build Quality Q-factor (car_id=64)
-- The contrast case: sports car chassis with cost-cut interior

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
    64,
    48.5,
    -- Build Precision
    72, 42, 48,
    -- Aging Durability
    38, 35, 40,
    -- Text evidence
    'FM platform (350Z-based) — genuinely good sports car architecture. 52:48 weight distribution. Double wishbone front. But: pressed steel everywhere, standard Nissan spot welding, no structural innovations. Body construction is the one bright spot.',
    'Minimal by design. No hydraulic mounts. No acoustic glass. No sound deadening beyond minimum. Exhaust note prominent (intentional). Tire roar significant with wider tires. Coupe body creates resonance. At 80mph it feels like 80mph.',
    'The single most criticized aspect of long-term ownership. Endemic dashboard cracking (soft sticky mess in warm climates, Infiniti never recalled). Seat bolster foam collapses at 40-60K miles (TSB ITB07-006). Aluminum-look trim peels at 4-6K miles. Rosewood trim is wood-grain overlay on plastic. Leather is mediocre.',
    'Clear coat failure is epidemic. Facebook group Infiniti Paint Problems has ~1000 members. Hood, roof, trunk blister and flake. Rear quarter rust on wheel arches almost universal at 100K+. Paint thin and soft. Some 2003-2005 batches had defective clear coat per body shop reports.',
    'Bose head unit failure is nearly universal on 2003-2006. Internal amp circuit board cold solder joints = no sound. Repair shops report doing many per week. When radio dies, AC controls can stop working (integrated). Parasitic battery drain from faulty circuit. Window motor failures common.',
    'Dashboard cracks at 8-12 years. Seat bolster tears at 40-60K. Clear coat peels at 7-10 years. Interior trim detaches at 5-8 years. Steering wheel wear at 60-80K. Headliner pulls near sunroof. The G35 ages like an athlete — stays capable but everything shows.',
    'G35 Coupe Q-score 48.5. The driving experience is genuinely good (FM platform, VQ35DE, RWD, manual) but the construction quality is objectively poor. Nissan spent money on chassis engineering and cut corners on everything else. At $5K used it is what it is.',
    -- Structural metadata
    'shared', 'Multiple (Japan)', 'spot', 6.0,
    'rubber', 'standard', 'standard', 'plastic',
    3, 'minimal', 'sample'
);
```

- [ ] **Step 2: Execute the inserts**

Run: `cd C:\Users\llama\OneDrive\proj\motorgeek; sqlite3 data/motorgeek.db ".read data/sql_inserts/add_es350_g35_build_quality.sql"`

- [ ] **Step 3: Verify the data**

Run: `sqlite3 -header -column data/motorgeek.db "SELECT c.make || ' ' || c.model as car, printf('%.1f',bq.q_score) as q_score, bq.score_body_construction as body, bq.score_nvh_isolation as nvh, bq.score_interior_materials as interior, bq.score_paint_corrosion as paint, bq.score_electrical_aging as elec, bq.score_cosmetic_aging as cosmetic FROM build_quality bq JOIN cars c ON bq.car_id = c.id ORDER BY bq.q_score DESC"`

Expected: 3 rows: LS430 (94.7), ES 350 (76.3), G35 (48.5)

- [ ] **Step 4: Commit**

```bash
git add data/sql_inserts/add_es350_g35_build_quality.sql
git commit -m "feat: add ES 350 and G35 Coupe build quality Q-factor data"
```

---

### Task 7: Verify full system integration

**Files:** None (verification only)

- [ ] **Step 1: Run all tests**

Run: `python3 -m pytest tests/ -v`
Expected: All tests pass (existing + new scoring_build tests)

- [ ] **Step 2: Verify ORM relationship works**

Run: `python3 -c "from motorgeek.core.models import Car, BuildQuality; print('Relationship OK')" `
Expected: `Relationship OK`

- [ ] **Step 3: Verify Q-score ranking**

Run: `sqlite3 -header -column data/motorgeek.db "SELECT c.make || ' ' || c.model as car, printf('%.1f',r.reliability_score) as reliability, printf('%.1f',bq.q_score) as q_factor FROM cars c LEFT JOIN reliability r ON r.car_id = c.id LEFT JOIN build_quality bq ON bq.car_id = c.id WHERE bq.q_score IS NOT NULL ORDER BY bq.q_score DESC"`

Expected:
| Car | Reliability | Q-Factor |
|-----|------------|----------|
| LS 430 | 88.5 | 94.7 |
| ES 350 | 87.8 | 76.3 |
| G35 Coupe | 80.9 | 48.5 |

The 0.7-point reliability gap between LS430 and ES350 becomes an 18.4-point Q-factor gap. The G35's 80.9 reliability is decent but 48.5 Q-factor reveals the construction truth.

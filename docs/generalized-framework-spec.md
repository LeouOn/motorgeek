# DataForge — Generalized Data Exploration Framework

> Extracted from MotorGeek patterns. Domain-agnostic, API-only, agent-native.

## Origin Story

MotorGeek proved that the real interface wasn't the TUI or the web frontend — it was
the **agent tools + schema + data**. The user never opened the web UI once, driving
everything through OpenCode. The framework should reflect this: **the tools ARE the
product**.

---

## Core Patterns Extracted from MotorGeek

### Pattern 1: Entity + Attribute Groups

MotorGeek has `Car` as the core entity with ~18 related tables, each representing a
"dimension" of the car (performance, powertrain, reliability, cost, electronics, etc.).
Each attribute group has typed fields (numeric, text, enum, JSON) plus an `extra` JSON
catch-all.

**Generalization**: Configurable entity types with pluggable attribute group schemas
defined in YAML/JSON, not code.

```
MotorGeek:     Car → Performance, PowertrainICE, Reliability, CostToOwn, Electronics, ...
Generalized:   Entity → [AttributeGroup₁, AttributeGroup₂, ...]
```

Each attribute group is a collection of typed fields. The framework doesn't know or
care what the fields mean — it just stores, queries, and compares them.

### Pattern 2: Tool-Calling as Primary Interface

MotorGeek defined 12 tools (`search_cars`, `get_car_detail`, `compare_cars`, `enrich_car_data`,
etc.) that the agent calls. These tools ARE the API. OpenCode effectively used them
indirectly by reading the code, but the same tools could be exposed as MCP server tools.

**Generalization**: Auto-generate CRUD + domain tools from the schema definition.
Tools are the primary interface — no web UI needed.

The framework should produce these tool categories for ANY domain:
- **Search** — full-text + filtered queries across entities
- **Detail** — full attribute dump for one entity
- **Compare** — side-by-side across user-selected dimensions
- **Enrich** — gap detection + estimation from known values
- **Ingest** — raw text → structured data pipeline
- **Group** — aggregate queries (by era, category, family, etc.)
- **Rank** — sort/rank entities by any numeric dimension

### Pattern 3: Agentic Ingestion State Machine

MotorGeek's `ingest.py` implements a 5-state pipeline:

```
draft → processing → awaiting_response → enriched → saved
                                            ↓
                                      (can loop back to awaiting_response)
```

The LLM extracts structured data from raw pasted text, identifies gaps/conflicts,
asks the user questions, and iteratively refines. This is the most valuable pattern.

**Generalization**: Generic state machine with domain-specific extraction prompts.
The states and transitions are universal — only the prompt and output schema change.

```
State          | Universal Behavior                    | Domain-Specific
---------------|---------------------------------------|---------------------------
draft          | Store raw text                         | —
processing     | Send text to LLM with extraction prompt| The prompt template
awaiting       | Present gaps/questions to user         | What constitutes a "gap"
enriched       | All questions resolved, ready to save  | Validation rules
saved          | Write to DB                            | Entity/attribute mapping
```

### Pattern 4: Dimension Router

MotorGeek's `pipeline.py` has a `DimensionRouter` that classifies raw text to determine
which attribute groups it contains data for. A paste about engine specs routes to
"engineering_ice"; a paste about repair costs routes to "repair_catalog".

**Generalization**: Generic text → dimension classifier, auto-generated from the
schema definition. The prompt lists available dimensions; the LLM picks which ones
the text covers.

### Pattern 5: Family Inheritance

MotorGeek entities belong to families (e.g., "911", "M3") and inherit shared traits.
When ingesting a new 911 variant, the system pre-fills country, body style, drivetrain
from existing family members.

**Generalization**: Entity groups with configurable inheritance rules. When adding
a new entity to an existing group, specified fields auto-populate from group consensus.

### Pattern 6: Data Enrichment / Gap Filling

MotorGeek has two enrichment strategies:
1. **Heuristic estimation** — estimate 0-60 from power-to-weight ratio, weight from
   body style + displacement, fuel consumption from horsepower
2. **LLM-based** — ask the LLM to estimate missing fields by comparing to similar entities

**Generalization**: Pluggable enrichment rules per domain. Each rule is:
```
IF entity has [known_fields] AND missing [target_field]
THEN estimate [target_field] using [formula | llm_prompt]
WITH confidence_level = "estimated"
```

### Pattern 7: Confidence-Tagged Values

MotorGeek's extraction prompt assigns confidence levels to every extracted value:
- `high` — exact match in source text
- `medium` — inferred from context
- `low` — guessed

**Generalization**: Every field value in the system should optionally carry a confidence
tag. This enables queries like "show me all entities where X has low confidence" and
helps the enrichment engine prioritize which gaps to fill.

### Pattern 8: Provenance Tracking

MotorGeek tracks the source of every piece of data (`source` field on most tables,
`data_sources` table for raw text preservation, `agent_tool_calls` for audit).

**Generalization**: Universal provenance — every field value knows where it came from
(manual entry, LLM extraction, heuristic estimate, user correction) and when.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Domain Config (YAML)                │
│  entity name, attribute groups, fields, types,      │
│  families, enrichment rules, extraction prompts     │
└─────────────────────┬───────────────────────────────┘
                      │ loads
                      ▼
┌─────────────────────────────────────────────────────┐
│                  Schema Engine                        │
│  - Parse domain config                               │
│  - Generate SQLAlchemy models at runtime              │
│  - Generate DB migrations                            │
│  - Validate entity data against schema               │
└─────────────────────┬───────────────────────────────┘
                      │ provides models to
                      ▼
┌─────────────────────────────────────────────────────┐
│                  Tool Generator                       │
│  Auto-generates from schema:                         │
│  - search_entities (full-text + filter)              │
│  - get_entity_detail (all attributes)                │
│  - compare_entities (side-by-side)                   │
│  - rank_entities (sort by dimension)                 │
│  - enrich_entity (gap detection + estimation)        │
│  - ingest_raw (text → structured)                    │
│  - get_collection_overview (aggregate stats)         │
│  - list_entity_groups (families, categories)         │
└─────────────────────┬───────────────────────────────┘
                      │ registers as
                      ▼
┌─────────────────────────────────────────────────────┐
│             Interface Layer (pick one)                │
│                                                      │
│  Option A: MCP Server  (exposes tools to OpenCode)   │
│  Option B: REST API    (exposes tools as endpoints)  │
│  Option C: Python SDK  (direct import)               │
└─────────────────────────────────────────────────────┘
```

---

## Domain Config Schema

A single YAML file defines the entire domain. Here's what the MotorGeek domain
would look like if expressed in this format:

```yaml
domain:
  name: cars
  description: "Personal car collection and analysis"
  entity_label: "car"           # singular
  entity_label_plural: "cars"   # plural

  identity_fields:              # fields on the core entity
    - name: make
      type: string
      required: true
      searchable: true
    - name: model
      type: string
      required: true
      searchable: true
    - name: generation
      type: string
      searchable: true
    - name: year_start
      type: integer
      required: true
      filterable: true
    - name: year_end
      type: integer
    - name: era_tag
      type: enum
      values: [classic, malaise, 80s, 90s, 00s, modern, contemporary]
      filterable: true
    - name: body_style
      type: enum
      values: [sedan, coupe, hatchback, suv, roadster, wagon, truck, van]
      filterable: true
    - name: country
      type: string
      filterable: true
    - name: family
      type: string
      group_key: true            # entities with same family form a group
    - name: variant
      type: string

  attribute_groups:
    - name: performance
      cardinality: one           # one row per entity
      fields:
        - name: accel_0_60
          type: float
          unit: seconds
          lower_is_better: true
        - name: quarter_mile_time
          type: float
          unit: seconds
          lower_is_better: true
        - name: top_speed_mph
          type: float
          unit: mph
        - name: lateral_g
          type: float
          unit: g
          higher_is_better: true
        - name: power_to_weight
          type: float
          unit: hp/tonne
          derived: true          # auto-computed
          higher_is_better: true

    - name: powertrain
      cardinality: one
      fields:
        - name: engine_layout
          type: string
        - name: displacement_cc
          type: float
          unit: cc
        - name: cylinders
          type: integer
        - name: aspiration
          type: enum
          values: [na, turbo, twin-turbo, supercharged, twin-charged]
        - name: horsepower_bhp
          type: float
          unit: bhp
        - name: torque_nm
          type: float
          unit: Nm
        - name: transmission_type
          type: enum
          values: [manual, automatic, dct, cvt, automated_manual]
        - name: drivetrain
          type: enum
          values: [FWD, RWD, AWD, 4WD]
        - name: curb_weight_kg
          type: float
          unit: kg
        - name: fuel_consumption_mixed_l_100km
          type: float
          unit: L/100km
          lower_is_better: true

    - name: reliability
      cardinality: one
      fields:
        - name: reliability_score
          type: float
          unit: "/10"
          higher_is_better: true
        - name: common_failures
          type: json              # list of strings
        - name: avg_repair_cost
          type: float
          unit: USD

    - name: market
      cardinality: many          # time-series — many rows per entity
      fields:
        - name: date_recorded
          type: date
        - name: price_low
          type: float
          unit: USD
        - name: price_high
          type: float
          unit: USD
        - name: source_site
          type: string
        - name: trend
          type: enum
          values: [rising, falling, stable]

    - name: dimensions
      cardinality: one
      fields:
        - name: length_mm
          type: integer
          unit: mm
        - name: width_mm
          type: integer
          unit: mm
        - name: height_mm
          type: integer
          unit: mm
        - name: wheelbase_mm
          type: integer
          unit: mm

  # Derived metrics — computed from other fields
  derived_metrics:
    - name: power_to_weight
      formula: "powertrain.horsepower_bhp / (powertrain.curb_weight_kg / 1000)"
      unit: hp/tonne
      stored_in: performance.power_to_weight

    - name: hp_per_liter
      formula: "powertrain.horsepower_bhp / (powertrain.displacement_cc / 1000)"
      unit: hp/L

  # Family inheritance — which fields are inherited from group consensus
  family_inheritance:
    group_key: family            # the field that defines the group
    inherited_fields:
      - make
      - country
      - body_style
    check_consistency:           # warn if these vary within a group
      - powertrain.drivetrain
      - powertrain.engine_layout

  # Enrichment rules — fill gaps from known data
  enrichment_rules:
    - target: powertrain.curb_weight_kg
      when_missing: true
      estimate_from:
        - powertrain.horsepower_bhp
        - powertrain.displacement_cc
        - identity.body_style
      method: heuristic
      formula: |
        base = {"sedan": 1550, "coupe": 1500, "suv": 2000, "roadster": 1200}.get(body_style, 1600)
        weight = base + displacement_cc * 0.15
      confidence: low

    - target: performance.accel_0_60
      when_missing: true
      estimate_from:
        - powertrain.horsepower_bhp
        - powertrain.curb_weight_kg
      method: heuristic
      formula: |
        ptw = horsepower_bhp / (curb_weight_kg / 1000)
        if ptw > 300: return 3.0
        elif ptw > 200: return 4.0 + (300 - ptw) * 0.01
        elif ptw > 150: return 5.0 + (200 - ptw) * 0.015
        else: return 6.5 + (150 - ptw) * 0.02
      confidence: low

  # Extraction prompt template (for agentic ingestion)
  extraction_prompt: |
    You are a {domain.entity_label} data extraction agent.
    Analyze the provided text and produce structured JSON.

    Extract ALL numeric values with units. Convert to canonical units.
    Assign confidence: "high" (exact match), "medium" (inferred), "low" (guessed).
    Identify GAPS, CONFLICTS, and generate QUESTIONS.

    Output format:
    {schema_json}

    Text to analyze:
    {raw_text}
```

---

## Auto-Generated Tools

Given a domain config, the framework generates these tools:

### Universal Tools (every domain gets these)

| Tool | Parameters | Returns |
|------|-----------|---------|
| `search_{entity_label_plural}` | `query: str`, `filters: dict` | Matching entities with identity fields |
| `get_{entity_label}_detail` | `id: int` | Full attribute dump |
| `list_all_{entity_label_plural}` | — | All entities with key stats |
| `compare_{entity_label_plural}` | `ids: list[int]`, `dimensions: list[str]` | Side-by-side comparison |
| `rank_{entity_label_plural}` | `field: str`, `direction: asc\|desc`, `limit: int` | Ranked list |
| `get_collection_overview` | — | Counts, distributions, ranges |
| `enrich_{entity_label}` | `id: int`, `mode: auto\|ask_user` | Gap analysis + estimates |
| `ingest_raw` | `text: str`, `source: str` | Ingest session with extracted data |
| `list_{entity_label}_groups` | `group_key: str` | All families/categories |
| `compare_group` | `group_key: str`, `group_value: str` | Compare all entities in a group |
| `save_ingest_session` | `session_id: int` | Persist extracted data to DB |
| `respond_to_ingest` | `session_id: int`, `message: str` | Answer agent questions |

### Comparison Intelligence

The `compare_{entity_label_plural}` tool should automatically:
- Highlight which entity "wins" each dimension (green/red)
- Compute derived metrics on the fly if source data exists
- Flag dimensions where data is missing or low-confidence
- Suggest "interesting" comparisons (entities in same group, similar price, similar spec)

---

## Ingestion Pipeline (Generalized)

```
User pastes raw text
        │
        ▼
┌──────────────┐
│    draft      │  Raw text stored
└──────┬───────┘
       │ process_session()
       ▼
┌──────────────┐
│  processing   │  LLM extracts structured data using domain prompt
└──────┬───────┘
       │ Extraction complete
       ▼
┌──────────────────┐
│ awaiting_response │  Agent presents gaps/conflicts/questions
└──────┬───────────┘
       │ User responds (or loop back with more questions)
       ▼
┌──────────────┐
│   enriched    │  All critical gaps resolved
└──────┬───────┘
       │ User confirms
       ▼
┌──────────────┐
│    saved      │  Data written to entity + attribute tables
└──────────────┘
```

### What's Generic vs Domain-Specific

| Component | Generic | Domain-Specific |
|-----------|---------|-----------------|
| State machine | States + transitions | — |
| Gap detection | Framework asks "which fields are missing?" | Schema defines which fields are expected |
| Extraction prompt | Template structure | The actual prompt text + output schema |
| Follow-up handling | Merge user answers into parsed data | Which fields to merge, validation rules |
| Save logic | Create entity + attribute rows | Field-to-table mapping (from schema) |

---

## Data Model (Framework-Level)

The framework uses a small set of generic tables:

```sql
-- Every domain gets these tables
entities (
    id, domain, created_at, updated_at
)

entity_identity (
    entity_id, field_name, value_str, value_int, value_float, confidence, source
)

attribute_groups (
    id, entity_id, group_name, source, created_at
)

attribute_values (
    id, group_id, field_name,
    value_str, value_int, value_float, value_bool, value_json,
    confidence,   -- "high", "medium", "low", "estimated"
    source,        -- "manual", "llm-extract", "heuristic", "user-correction"
    source_detail,  -- "ZePerfs", "KBB", "estimated from PTW"
    extracted_at
)

entity_groups (
    id, group_key, group_value, entity_id
)

ingest_sessions (
    id, domain, raw_text, source_url, source_site,
    status,          -- draft/processing/awaiting/enriched/saved
    parsed_data,     -- JSON
    gaps_and_questions, -- JSON
    agent_messages,  -- JSON array
    created_at, updated_at
)

tool_call_log (
    id, session_id, tool_name, arguments, result,
    status, error_message, duration_ms, created_at
)
```

**Trade-off**: The generic schema is less query-efficient than MotorGeek's dedicated
tables (e.g., you can't index `attribute_values` on a specific field as easily).
For a personal data exploration tool, this is acceptable. For production scale, you'd
generate dedicated tables from the schema (which the framework could also do).

### Alternative: Generated Tables Mode

For domains that need query performance, the framework could generate actual
SQLAlchemy models from the domain config (like MotorGeek has now). This is a
build-time choice — use generic tables for prototyping, generated tables for production.

---

## MCP Server Interface

The primary interface for the framework is an MCP server. This lets OpenCode (or any
MCP-compatible agent) discover and call the tools directly.

```python
# Conceptual usage
from dataforge import DataForgeServer

server = DataForgeServer("path/to/domain-config.yaml")

# Server auto-registers all tools from the schema
# When OpenCode connects, it sees:
#   - search_cars("porsche 911")
#   - get_car_detail(id=5)
#   - compare_cars(ids=[2,3,4,5])
#   - enrich_car(id=5, mode="auto")
#   - ingest_raw(text="...", source="ZePerfs")
#   - etc.
```

---

## What MotorGeek Got Right (Keep)

1. **Agentic ingestion with state machine** — the most valuable pattern. Don't lose it.
2. **Confidence-tagged values** — enables smart gap prioritization.
3. **Family/group inheritance** — reduces repetitive data entry.
4. **Enrichment with estimation fallbacks** — keeps the collection usable even with partial data.
5. **Provenance on every value** — you always know where data came from.
6. **Tool-calling architecture** — the right abstraction for agent interaction.

## What MotorGeek Got Wrong (Fix)

1. **Tight domain coupling** — can't reuse for anything except cars.
2. **Web UI nobody used** — dead weight. Drop it. Agent is the interface.
3. **Embedded agent loop** — OpenCode is a better agent than anything you'll build.
   The framework should expose tools, not run its own agent.
4. **Monolithic tools.py** — 840 lines, all domain-specific. Should be generated.
5. **No type safety on field access** — lots of `if ice and ice.horsepower_bhp` guarding.
   The schema should handle nullability.

---

## Implementation Priorities

If/when we build this:

1. **Schema Engine** — parse domain config, generate models (generic or specific tables)
2. **Tool Generator** — auto-generate search/compare/enrich/ingest tools from schema
3. **Ingestion Pipeline** — port the state machine, make prompts configurable
4. **MCP Server** — expose tools to OpenCode
5. **Enrichment Engine** — generic rule evaluator from domain config
6. **Export/Import** — dump/load domain data as JSON (MotorGeek already has this)

---

## Open Questions

1. **Generic tables vs generated tables?** Generic is simpler but slower. Generated
   matches MotorGeek's performance. Maybe support both modes?

2. **How to handle multi-entity ingestion?** MotorGeek's batch comparison ingest is
   complex (extracts multiple cars + qualitative analysis from one document). The
   generic version needs a concept of "multi-entity extraction."

3. **Derived metrics as config?** The formulas in `enrichment_rules` use Python-like
   expressions. Need a safe evaluator or restrict to simple arithmetic.

4. **Relationships between entities?** MotorGeek has `predecessor_id`/`successor_id`
   on `HistoricalContext`. The generic framework needs some way to express entity-
   entity relationships (competitors, predecessors, variants, etc.).

5. **Time-series attributes?** MotorGeek's `market_history` is time-series data.
   The generic framework needs to distinguish between "current state" attributes
   and "historical record" attributes. The `cardinality: many` hint in the config
   is a start but doesn't capture the time dimension fully.

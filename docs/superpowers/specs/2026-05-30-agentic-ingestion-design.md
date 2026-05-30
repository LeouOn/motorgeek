# MotorGeek — Agentic Ingestion + Exploration Tool
**Spec**: `docs/superpowers/specs/2026-05-30-agentic-ingestion-design.md`
**Date**: 2026-05-30
**Status**: Draft

---

## 1. Overview

**What we're building:**

A web-first car research and collection tool where you paste raw spec data from any source (ZePerfs, KBB, Wikipedia, manufacturer specs), an LLM agent parses and analyzes it, identifies gaps and conflicts, asks you clarifying questions, enriches the data, and saves it to your collection.

A companion **explore mode** lets you chat with your collection — the agent proactively surfaces comparisons, missing specs, market anomalies, and interesting patterns across your cars.

**Design principles:**
- Web is primary interface; CLI is for power users
- All LLM interactions are visible and editable — no black boxes
- Agentic, not automatic — the agent assists, you decide
- Data is stored properly once, not as free text blobs

---

## 2. Schema Changes

### 2.1 New Table: `Dimensions`

Canonical physical measurements for a car. One row per car.

```sql
CREATE TABLE dimensions (
    id INTEGER PRIMARY KEY,
    car_id INTEGER NOT NULL REFERENCES cars(id) ON DELETE CASCADE,
    length_mm INTEGER,
    width_mm INTEGER,
    height_mm INTEGER,
    wheelbase_mm INTEGER,
    track_front_mm INTEGER,
    track_rear_mm INTEGER,
    ground_clearance_mm INTEGER,
    front_overhang_mm INTEGER,
    rear_overhang_mm INTEGER,
    drag_coefficient FLOAT,
    front_tire_size VARCHAR(30),
    rear_tire_size VARCHAR(30),
    source VARCHAR(200),
    extra JSON,
    UNIQUE(car_id)
);
```

### 2.2 New Table: `PerformanceMeasurements`

Individual test result rows — each source's actual measurement with metadata. Replaces aggregated-only approach.

```sql
CREATE TABLE performance_measurements (
    id INTEGER PRIMARY KEY,
    car_id INTEGER NOT NULL REFERENCES cars(id) ON DELETE CASCADE,
    metric_name VARCHAR(50) NOT NULL,   -- 'accel_0_60', 'brake_100_0', 'top_speed', etc.
    value FLOAT NOT NULL,
    unit VARCHAR(20) NOT NULL,           -- 's', 'mph', 'km/h', 'g', 'm/s2'
    source_site VARCHAR(100),            -- 'ZePerfs', 'Car & Driver', 'MotorTrend', 'manufacturer'
    test_date DATE,
    sample_size INTEGER,                -- number of runs averaged
    conditions VARCHAR(200),             -- 'dry asphalt', 'manufacturer test', etc.
    notes TEXT,
    extra JSON,
    UNIQUE(car_id, metric_name, source_site, test_date)
);
```

**Metric name vocabulary:**
- `accel_0_60`, `accel_0_80`, `accel_0_100`, `accel_0_120`, `accel_0_130`, `accel_0_160`, `accel_0_180`
- `accel_40_80`, `accel_40_100`, `accel_40_120`, `accel_40_140`, `accel_80_120`, `accel_80_140`, `accel_80_160`, `accel_80_180`
- `quarter_mile_time`, `quarter_mile_speed`
- `brake_60_0`, `brake_80_0`, `brake_100_0`, `brake_120_0`
- `top_speed_measured`, `top_speed_claimed`
- `lateral_g`
- `motortrend_figure8`, ` Nürburgring_lap`

### 2.3 New Table: `ZePerfsIndices`

ZePerfs proprietary indices stored per car.

```sql
CREATE TABLE zeperfs_indices (
    id INTEGER PRIMARY KEY,
    car_id INTEGER NOT NULL REFERENCES cars(id) ON DELETE CASCADE,
    zeperfs_index FLOAT,          -- e.g. 154
    sportivity_index FLOAT,      -- e.g. 103
    perfs_prix_ratio FLOAT,      -- e.g. 90
    source VARCHAR(100),
    recorded_date DATE,
    UNIQUE(car_id)
);
```

### 2.4 New Table: `CarReviews`

Consumer and expert reviews, ratings.

```sql
CREATE TABLE car_reviews (
    id INTEGER PRIMARY KEY,
    car_id INTEGER NOT NULL REFERENCES cars(id) ON DELETE CASCADE,
    source_site VARCHAR(100),     -- 'KBB', 'ConsumerReports', 'ZePerfs', 'C&D', etc.
    rating_overall FLOAT,        -- e.g. 4.8 / 5
    rating_reliability FLOAT,    -- e.g. 4.5 / 5
    rating_performance FLOAT,    -- e.g. 4.2 / 5
    rating_comfort FLOAT,
    rating_value FLOAT,
    review_excerpt TEXT,
    review_url VARCHAR(500),
    reviewer_name VARCHAR(100),
    review_date DATE,
    extra JSON,
    UNIQUE(car_id, source_site)
);
```

### 2.5 New Table: `IngestSessions`

Tracks the state of each paste-to-save ingestion flow.

```sql
CREATE TABLE ingest_sessions (
    id INTEGER PRIMARY KEY,
    car_id INTEGER REFERENCES cars(id),    -- NULL if new car
    raw_paste TEXT NOT NULL,
    source_url VARCHAR(500),
    source_site VARCHAR(100),
    status VARCHAR(20) NOT NULL DEFAULT 'draft',  -- draft|processing|awaiting_response|enriched|saved|discarded
    llm_model VARCHAR(50),
    parsed_data JSON,               -- LLM's structured interpretation
    gaps_and_questions JSON,        -- what agent is asking about
    agent_messages JSON,            -- full message thread (agent + user)
    final_car_data JSON,            -- ready-to-save merged data
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
);
```

### 2.6 Additions to Existing Tables

**cars table additions:**
- `price_new_eur` (float) — MSRP in euros for cross-car comparison
- `fuel_type` (varchar: petrol/diesel/hybrid/phev/electric) — classification
- `market_segment` (varchar: city_car, compact, midsize, executive, full-size, luxury, sports, supercar)
- `source_url` (varchar) — canonical source for this car

**powertrain_ice additions:**
- `power_kw` (float) — kW alongside HP
- `specific_power_per_cylinder_w_cm2` (float)
- `bmep_bar` (float) — brake mean effective pressure
- `mean_piston_speed_m_s` (float)
- `engine_torque_nm` (float) — secondary torque value
- `fuel_consumption_mixed_l_100km` (float)
- `fuel_consumption_sport_l_100km` (float)
- `co2_emissions_g_km` (float)
- `fuel_tank_capacity_l` (float)
- `reserve_fuel_l` (float)
- `top_speed_claimed_km_h` (float)
- `power_reserve_pct` (float) — torque reserve as percentage

**market_history additions:**
- `currency` (varchar: EUR, USD, GBP) — per record
- `price_eur` (float) — normalized to EUR for comparison

**data_sources changes:**
- Add `car_id` FK to link sources to specific cars (was missing)
- Change `dimension` to `dimension_tag` (varchar) — what the source covers

---

## 3. Agentic Ingestion Workflow

### 3.1 State Machine

```
draft → processing → awaiting_response → enriched → saved
                   ↘ discarded
```

**State transitions:**

1. **draft**: User pastes raw text, submits. Session created with raw_paste.
2. **processing**: LLM parses the raw text into structured JSON, identifies gaps.
3. **awaiting_response**: Agent presents parsed data + questions to user. User responds.
4. **enriched**: User responses incorporated. Data is complete enough to save.
5. **saved**: Car data written to DB. Session archived.
6. **discarded**: User abandons the session.

### 3.2 Processing Prompt Strategy

When raw text enters **processing**:

```
You are a car data extraction agent. Parse the provided text about a car and produce structured JSON.

Rules:
- Extract ALL numeric values with their units
- Note any conflicting values (e.g., manufacturer claims vs measured)
- Flag fields that are missing but expected (e.g., no weight given)
- Infer the car identity (make, model, generation, year) if not explicit
- Preserve the source URL if provided

Output format:
{
  "identity": { "make": "...", "model": "...", "generation": "...", "year_start": N, "year_end": N },
  "dimensions": { ... },
  "performance": { "measurements": [...], "indices": {...} },
  "powertrain": { ... },
  "market": { ... },
  "reliability": { ... },
  "reviews": { ... },
  "gaps": ["gap1", "gap2", ...],   -- fields that were expected but not found
  "conflicts": ["conflict1", ...],  -- values that contradict each other
  "questions": ["What units are the tire sizes in?", ...]  -- agent's questions
}
```

### 3.3 Awaiting Response UX

The web UI shows:
- Left panel: parsed structured data (editable fields)
- Right panel: chat-style Q&A between agent and user
- Each question is a discrete card with answer input
- User can type responses or click suggested answers
- Agent responses highlighted differently from user responses

### 3.4 Enrichment

After user responds to questions, LLM enriches:
- Fills in inferred values with confidence scores
- Marks low-confidence fields with `?` so user can verify
- Produces final `final_car_data` JSON ready to save

---

## 4. Web UI Components

### 4.1 Route: `GET /ingest` — Paste Page

- Large textarea for pasting raw text
- Optional source URL field
- Source site selector (ZePerfs, KBB, Wikipedia, Other)
- Submit button → creates IngestSession → redirects to `/ingest/{session_id}`

### 4.2 Route: `GET /ingest/{session_id}` — Ingest Review Page

Two-column layout:

**Left: Structured Data Review**
- Collapsible sections per dimension (Identity, Dimensions, Performance, Powertrain, Market, Reviews)
- Each field shows: field name, parsed value, confidence indicator (high/medium/low/?), source
- Inline editing: click any field to override
- Missing fields highlighted in yellow

**Right: Agent Chat Panel**
- Scrollable chat thread
- Agent messages in blue/left bubbles
- User responses in green/right bubbles
- "Suggested responses" chips for quick answers
- Overall status badge (draft → processing → awaiting_response → enriched → saved)

**Bottom bar:**
- "Ask Agent" button — send free-text follow-up to agent
- "Looks Good, Save" button — only active when status is `enriched`
- "Discard" button — abandons session

### 4.3 Route: `POST /ingest/{session_id}/message` — Send Message

- User sends a text response to the agent
- LLM processes, updates `parsed_data` and `gaps_and_questions`
- Returns updated chat thread + structured data diff
- HTMX partial update (no full page reload)

### 4.4 Route: `POST /ingest/{session_id}/save` — Save Session

- Validates `final_car_data` is complete enough
- If `car_id` is NULL: creates new Car row, generates ID
- Upserts all child dimension tables
- Sets session status to `saved`
- Redirects to `/cars/{new_car_id}`

### 4.5 Route: `GET /explore` — Exploration Page

- Chat interface (like `/query` but with session history)
- Left panel: quick stats for entire collection (car count, HP range, era breakdown)
- Chat input at bottom
- Agent can suggest: comparisons, cars with missing data, market anomalies
- Previous exploration sessions listed in sidebar (saved to `ingest_sessions` with `status=saved`)

### 4.6 Route: `GET /cars/{id}` — Car Detail (Updated)

- All existing sections (Performance, Powertrain, etc.)
- NEW: "Data Sources" section listing all raw sources used
- NEW: "Indices" section (ZePerfs, sportivity, etc.)
- NEW: "Reviews" section
- NEW: "Ingest Sessions" link showing history of how data was added/enriched

---

## 5. CLI Equivalents

### 5.1 `motorgeek ingest paste`

```
motorgeek ingest paste
```

Opens default editor ($EDITOR) with blank textarea → user pastes raw text → saves as draft session → returns session ID + URL.

### 5.2 `motorgeek ingest status <session_id>`

Shows session state, parsed fields, agent questions.

### 5.3 `motorgeek ingest respond <session_id> "<answer>"`

Send a text answer to the agent's question.

### 5.4 `motorgeek ingest save <session_id>`

Save the enriched data to DB.

### 5.5 `motorgeek ingest list`

List all ingest sessions with status.

---

## 6. Key Implementation Details

### 6.1 LLM Provider Fallback

- If `OPENAI_API_KEY` not set: show friendly error with setup instructions
- If LLM call fails: session stays in `awaiting_response`, error shown in chat panel
- No auto-retry; user can click "Retry" in UI

### 6.2 Message History in Sessions

Each `IngestSession` stores `agent_messages` as JSON array:
```json
[
  {"role": "agent", "text": "I found these values from your paste...", "timestamp": "..."},
  {"role": "user", "text": "Yes that's correct, but the top speed is 280km/h", "timestamp": "..."},
  ...
]
```

### 6.3 Conflict Resolution

- If ZePerfs says 0-100 in 5.7s but manufacturer says 5.5s: store both with source attribution
- `performance.accel_0_60` becomes the "consensus" value (user picks or LLM recommends)
- Individual measurements live in `performance_measurements`

### 6.4 Confidence Scoring

LLM assigns confidence to each extracted field:
- `high` — exact match in source text
- `medium` — inferred or calculated from related values
- `low` — single source, could be error
- `?` — user needs to verify

Displayed as color-coded badges in the review UI.

---

## 7. Testing Strategy

- Unit tests for each extraction field parser (LLM-agnostic)
- Integration test for full paste → save flow with mocked LLM
- Session state machine tests: verify valid transitions only
- UI tests: verify HTMX partial updates render correctly
- LLM-independent: mock LLM responses in tests

---

## 8. Out of Scope (Future)

- Web scraping / URL fetching
- Real-time streaming (SSE) for agent responses
- Multi-user / accounts
- Comparison auto-generation from agent exploration
- Browser extension for one-click capture

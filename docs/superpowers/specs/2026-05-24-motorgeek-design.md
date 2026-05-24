# MotorGeek Design Spec

## Overview

MotorGeek is a personal car analysis and comparison tool that lets you deeply explore, ingest, and compare cars across eras and perspectives. The primary workflow is manual copy-paste of raw data from sites like ZePerfs, forums, and manufacturer spec sheets, which an LLM pipeline parses into structured fields. The CLI handles data ingestion and quick queries; the web app provides rich visualizations and interactive comparisons.

### Core Principles

- **LLM-first data ingestion**: Paste raw text, LLM extracts structured fields, you review and accept.
- **Curated collection**: Dozens of cars with deep, high-quality data per car.
- **Five comparison dimensions**: Performance, Engineering, Reliability, Cost-to-Own, Historical Context.
- **Hybrid SQL + JSON schema**: Rigid columns for queryable fields, JSON escape hatches for messy reality.
- **CLI-first, web-second**: CLI is the primary interface; web app adds visualization on top.

---

## Schema

All tables are 1:N from CARS unless noted. SQLite database.

### CARS (core identity)

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | Auto-increment |
| make | TEXT | e.g. "Porsche" |
| model | TEXT | e.g. "911 Turbo" |
| generation | TEXT | e.g. "996" |
| year_start | INTEGER | First model year |
| year_end | INTEGER | Last model year (nullable for ongoing) |
| era_tag | TEXT | e.g. "90s", "00s", "modern" |
| body_style | TEXT | coupe, sedan, convertible, etc. |
| country | TEXT | Country of origin |
| production_units | INTEGER | Total production (nullable) |
| description | TEXT | Free-text summary |
| image_paths | JSON | Array of local/URL image paths |
| created_at | DATETIME | Auto-set |

### PERFORMANCE

| Column | Type | Notes |
|--------|------|-------|
| car_id | INTEGER FK | References CARS |
| source | TEXT | Where this data came from |
| accel_0_60 | REAL | Seconds |
| accel_0_100 | REAL | Seconds |
| quarter_mile_time | REAL | Seconds |
| quarter_mile_speed | REAL | MPH trap speed |
| top_speed_mph | REAL | |
| power_to_weight | REAL | HP/kg (auto-calculated) |
| lateral_g | REAL | Skidpad |
| braking_60_0_ft | REAL | Feet |
| lap_times | JSON | `{ "nurburgring": "7:32", "laguna_seca": "1:35.2" }` |
| extra | JSON | Unrecognized performance fields |

### POWERTRAIN_ICE

| Column | Type | Notes |
|--------|------|-------|
| car_id | INTEGER FK | References CARS |
| source | TEXT | |
| engine_layout | TEXT | e.g. "front longitudinal", "rear transverse" |
| displacement_cc | INTEGER | |
| cylinders | INTEGER | |
| aspiration | TEXT | NA, turbo, supercharger, twin-turbo, etc. |
| horsepower_bhp | REAL | |
| horsepower_rpm | INTEGER | RPM at peak HP |
| torque_nm | REAL | |
| torque_rpm | INTEGER | RPM at peak torque |
| redline_rpm | INTEGER | |
| compression_ratio | REAL | e.g. 11.5 |
| fuel_system | TEXT | port injection, direct injection, carburetor, etc. |
| transmission_type | TEXT | manual, auto, DCT, CVT |
| gear_count | INTEGER | |
| drivetrain | TEXT | FWD, RWD, AWD |
| curb_weight_kg | REAL | |
| weight_dist_pct | REAL | Front weight distribution % |
| suspension_fr | TEXT | Front and rear suspension type |
| brakes_fr | TEXT | Front and rear brake type |
| drag_coefficient | REAL | Cd |
| is_hybrid | BOOLEAN | True if this ICE car has hybrid assist |
| hybrid_system_id | INTEGER FK | References HYBRID_SYSTEM (nullable) |
| ground_clearance_mm | REAL | Driveway scrape check |
| cargo_volume_liters | REAL | Practicality metric |
| extra | JSON | |

### POWERTRAIN_EV

| Column | Type | Notes |
|--------|------|-------|
| car_id | INTEGER FK | References CARS |
| source | TEXT | |
| battery_capacity_kwh | REAL | |
| chemistry_type | TEXT | NMC, NCA, LFP, solid-state |
| charge_arch_volts | INTEGER | 400V, 800V, etc. |
| motor_layout | TEXT | single front, dual AWD, tri-motor, etc. |
| motor_count | INTEGER | |
| horsepower_bhp | REAL | |
| torque_nm | REAL | |
| range_mi_epa | REAL | EPA-rated range |
| charge_rate_peak_kw | REAL | Max DC fast charge rate |
| battery_degradation_curve | JSON | `{ "1yr": "2%", "5yr": "8%", "100k_mi": "12%" }` |
| motor_longevity_notes | TEXT | |
| ground_clearance_mm | REAL | |
| cargo_volume_liters | REAL | |
| extra | JSON | |

### HYBRID_SYSTEM

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| car_id | INTEGER FK | References CARS |
| hybrid_type | TEXT | mild, full, plug_in, series, power_split |
| system_name | TEXT | e.g. "Toyota Hybrid Synergy Drive Gen 4" |
| system_generation | INTEGER | Normalized generation number |
| power_split_ratio | JSON | Sun/ring/carrier gearing if PSD |
| battery_capacity_kwh | REAL | |
| battery_chemistry | TEXT | NiMH, Li-Ion NCA, LiFePO4 |
| battery_voltage_nominal | REAL | |
| battery_cooling_type | TEXT | air, liquid, refrigerant |
| battery_module_count | INTEGER | |
| battery_supplier | TEXT | Panasonic, CATL, in-house |
| battery_warranty_years | INTEGER | |
| battery_warranty_miles | INTEGER | |
| motor_count | INTEGER | |
| motor_type | TEXT | PMSM, induction, wound-rotor |
| motor_power_kw_total | REAL | |
| motor_torque_nm_total | REAL | |
| motor_position | TEXT | front, rear, front+rear, in-transmission |
| combined_system_power_bhp | REAL | Engine + motor(s) peak |
| combined_system_torque_nm | REAL | |
| ev_only_power_bhp | REAL | Motor-only sustained output |
| ev_only_range_mi | REAL | EPA electric range (PHEV) |
| ev_only_top_speed_mph | REAL | |
| fuel_econ_combined_mpg | REAL | Hybrid mode |
| electric_consumption_wh_pm | REAL | Watt-hours per mile (PHEV/EV mode) |
| regen_braking_power_kw | REAL | |
| can_lock_ev_mode | BOOLEAN | |
| has_charge_sustain_mode | BOOLEAN | |
| charge_rate_max_kw | REAL | Max AC/DC charging (PHEV) |
| engine_engagement_strategy | TEXT | load-based, speed-based, etc. |
| cold_weather_behavior | TEXT | |
| cvt_behavior_notes | TEXT | |
| typical_degradation_5yr_pct | REAL | |
| degradation_knee_miles | INTEGER | |
| common_failure_modes | JSON | |
| system_idiosyncrasies | JSON | |
| extra | JSON | |

### RELIABILITY

| Column | Type | Notes |
|--------|------|-------|
| car_id | INTEGER FK | References CARS |
| source | TEXT | |
| reliability_score | REAL | Normalized 0-100 |
| common_failures | JSON | Array of failure descriptions |
| avg_repair_cost | REAL | Average across common repairs |
| recall_count | INTEGER | |
| part_availability | TEXT | excellent, good, poor, discontinued |
| diy_friendliness | TEXT | easy, moderate, difficult, specialist |
| known_issues | JSON | Detailed known issues |
| extra | JSON | |

### CONSUMABLES_AND_SPECS

| Column | Type | Notes |
|--------|------|-------|
| car_id | INTEGER FK | References CARS |
| source | TEXT | |
| tire_sizes | JSON | `{ "front": "225/45R17", "rear": "255/40R17", "staggered": true }` |
| bulb_types | JSON | `{ "headlight_low": "H7", "headlight_high": "H1", "turn": "7440" }` |
| fluid_capacities | JSON | `{ "engine_oil": "6.5L", "coolant": "8.2L", "transmission": "4.0L" }` |
| obd_protocol | TEXT | |
| lug_nut_torque_nm | REAL | |
| known_spec_conflicts | JSON | `{ "headlight_bulb": "manual says H11, reality is H7" }` |
| technical_diagram_notes | TEXT | |
| extra | JSON | |

### COST_TO_OWN

| Column | Type | Notes |
|--------|------|-------|
| car_id | INTEGER FK | References CARS |
| source | TEXT | |
| msrp_original | REAL | Original MSRP |
| msrp_currency | TEXT | USD, GBP, EUR, etc. |
| msrp_inflation_adj | REAL | Auto-calculated to today's dollars |
| fuel_econ_city_mpg | REAL | |
| fuel_econ_hwy_mpg | REAL | |
| annual_maintenance_est | REAL | Estimated annual maintenance |
| insurance_group | INTEGER | |
| depreciation_5yr_pct | REAL | 5-year depreciation percentage |
| extra | JSON | |

### MARKET_HISTORY (append-only time-series)

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| car_id | INTEGER FK | References CARS |
| date_recorded | DATE | |
| price_low | REAL | |
| price_high | REAL | |
| volume_sold_est | INTEGER | Estimated units sold in period |
| market_trend_indicator | TEXT | rising, stable, falling |
| source_site | TEXT | BringATrailer, CarsBids, Hagerty, etc. |

### REPAIR_COSTS (1:N per car, individual repair events)

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| car_id | INTEGER FK | References CARS |
| date | DATE | When repair occurred |
| mileage_at_repair | INTEGER | |
| repair_category | TEXT | engine, transmission, electrical, suspension, brakes, cooling, exhaust, body, interior, electronics, other |
| repair_name | TEXT | e.g. "ECU capacitor replacement" |
| description | TEXT | |
| parts_cost | REAL | |
| labor_cost | REAL | |
| total_cost | REAL | |
| currency | TEXT | |
| shop_type | TEXT | dealer, independent, diy |
| source | TEXT | RepairPal, CarMD, personal, forum, warranty_claim |
| is_warranty_covered | BOOLEAN | |
| is_recall | BOOLEAN | |
| notes | TEXT | |
| extra | JSON | |

### REPAIR_CATALOG (1:N per car, reference baseline costs)

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| car_id | INTEGER FK | References CARS |
| repair_name | TEXT | e.g. "Timing chain tensioner" |
| repair_category | TEXT | Same categories as REPAIR_COSTS |
| avg_cost_low | REAL | |
| avg_cost_high | REAL | |
| currency | TEXT | |
| frequency | TEXT | common, occasional, rare |
| typical_mileage_range | TEXT | e.g. "80k-120k" |
| source | TEXT | RepairPal, CarMD, NHTSA, community |
| source_url | TEXT | |
| severity | TEXT | minor, moderate, major, critical |
| diy_difficulty | TEXT | easy, moderate, advanced, specialist |
| tools_required | JSON | Array of special tools needed |
| notes | TEXT | |
| extra | JSON | |

### HISTORICAL_CONTEXT

| Column | Type | Notes |
|--------|------|-------|
| car_id | INTEGER FK | References CARS |
| design_philosophy | TEXT | |
| designer_name | TEXT | |
| cultural_significance | TEXT | |
| racing_pedigree | TEXT | |
| innovations | JSON | Array of innovations introduced |
| direct_competitors | JSON | Array of competitor car names |
| predecessor_id | INTEGER FK | References CARS (self-join) |
| successor_id | INTEGER FK | References CARS (self-join) |
| extra | JSON | |

### MOD_POTENTIAL

| Column | Type | Notes |
|--------|------|-------|
| car_id | INTEGER FK | References CARS |
| platform_limits | JSON | `{ "transmission": "slips past 400nm", "cooling": "inadequate for track" }` |
| tuning_friendliness | TEXT | excellent, good, moderate, poor |
| ecu_lock_status | TEXT | open, partially locked, fully locked |
| common_mods | JSON | Array of common modifications |
| aftermarket_depth | TEXT | extensive, moderate, limited, none |
| known_gotchas | JSON | e.g. "head studs fail above 450hp" |
| extra | JSON | |

### ELECTRONICS

| Column | Type | Notes |
|--------|------|-------|
| car_id | INTEGER FK | References CARS |
| source | TEXT | |
| **ECU / Engine Management** | | |
| ecu_type | TEXT | Bosch Motronic 5.2, Denso, custom |
| ecu_bitness | TEXT | 8-bit, 16-bit, 32-bit |
| obd_generation | TEXT | OBD0, OBD1, OBD2, proprietary |
| flashable_ecu | BOOLEAN | Can reflash/tune via OBD |
| ecu_open_source_support | TEXT | Speeduino, RusEFI, ROMRaider, none |
| **Network Architecture** | | |
| bus_topology | TEXT | centralized, domain, zonal, hybrid |
| can_bus_present | BOOLEAN | |
| can_bus_generation | TEXT | CAN 2.0A, CAN 2.0B, CAN FD, CAN XL |
| can_bus_speed_kbps | INTEGER | 125, 250, 500, 1000, 2000 |
| can_bus_subnets | INTEGER | Number of separate CAN networks |
| lin_bus_count | INTEGER | LIN subnet count |
| flexray_present | BOOLEAN | BMW/Mercedes/Audi ~2005+ |
| most_bus_present | BOOLEAN | Fiber-optic media ring (older luxury) |
| ethernet_automotive | TEXT | 100BASE-T1, 1000BASE-T1 |
| gateway_module_count | INTEGER | |
| bus_diagrams_notes | TEXT | |
| **Sensor Suite** | | |
| sensor_count_total | INTEGER | Estimated total sensors |
| o2_sensors | TEXT | Narrowband vs wideband count |
| knock_sensors | TEXT | Count + type |
| camshaft_sensors | INTEGER | |
| crankshaft_sensors | TEXT | Count + type (VR/Hall) |
| map_sensors | INTEGER | |
| maf_sensors | TEXT | Count + type |
| wheel_speed_sensors | INTEGER | ABS sensors per corner |
| steering_angle_sensor | TEXT | Type |
| yaw_sensor | BOOLEAN | |
| accelerometers | INTEGER | Lateral + longitudinal |
| radar_sensors | TEXT | Front/rear/corner + range |
| lidar_sensors | TEXT | Count + type |
| ultrasonic_sensors | INTEGER | Parking sensor count |
| camera_sensors | INTEGER | Front/rear/side/360 |
| rain_light_sensor | BOOLEAN | |
| tpms_sensors | TEXT | Direct (in-wheel) vs indirect (ABS) |
| pressure_sensors | TEXT | Fuel, oil, boost, AC, brake count |
| temperature_sensors | TEXT | Coolant, oil, intake, ambient, etc. |
| exhaust_sensors | TEXT | NOx, particulate, ammonia |
| extra_sensors | JSON | |
| **Actuator Ecosystem** | | |
| electronic_throttle | BOOLEAN | Drive-by-wire |
| variable_valve_timing | TEXT | VTEC, VANOS, VVT-i, MIVEC |
| variable_valve_lift | TEXT | VTEC (lift), Valvetronic |
| active_exhaust_valves | BOOLEAN | |
| active_suspension | TEXT | Magnetic, air, hydraulic adaptive |
| active_aero | BOOLEAN | |
| electronic_diff | TEXT | eLSD or torque vectoring by braking |
| active_engine_mounts | TEXT | Vacuum or electromagnetic |
| active_grille_shutters | BOOLEAN | |
| steer_by_wire | BOOLEAN | |
| brake_by_wire | BOOLEAN | |
| **Power Electronics** | | |
| alternator_output_amps | INTEGER | |
| alternator_type | TEXT | Conventional, smart (variable voltage) |
| voltage_regulator | TEXT | Internal, ECU-controlled |
| battery_type_oe | TEXT | AGM, flooded lead-acid, Li-Ion |
| battery_capacity_ah | REAL | |
| battery_location | TEXT | Front, trunk, under-seat |
| dual_battery_setup | BOOLEAN | |
| dc_dc_converter_present | BOOLEAN | 48V mild hybrid or EV only |
| **Module Architecture** | | |
| total_ecu_count | INTEGER | All control modules |
| body_control_module | TEXT | BCM generation/complexity |
| transmission_tcu | TEXT | Separate or integrated in ECU |
| abs_module | TEXT | Standalone or integrated ESP |
| airbag_module | TEXT | SRS control unit location |
| instrument_cluster | TEXT | Analog, hybrid, full-digital |
| climate_control_module | TEXT | Manual, auto single, dual, tri |
| seat_control_modules | TEXT | Memory, massage, heating, etc. |
| lighting_control | TEXT | Halogen, xenon, LED, matrix LED |
| module_interop_notes | TEXT | |
| **Diagnostics & Access** | | |
| obd_connector_location | TEXT | |
| diagnostic_protocol | TEXT | KWP2000, ISO9141, CAN-ISO15765, J1850, DoIP |
| manufacturer_diag_tool | TEXT | Techstream, VCDS, INPA, STAR |
| can_bus_accessible | BOOLEAN | Can tap CAN from OBD port |
| immobilizer_type | TEXT | Transponder, rolling code, crypto |
| key_programming | TEXT | Dealer-only, diy-possible, nightmare |
| security_gateway | BOOLEAN | SGW present (FCA 2018+, etc.) |
| **Aging Vector** | | |
| capacitor_era | TEXT | Pre-RoHS, early-RoHS, modern |
| capacitor_known_issues | TEXT | |
| display_degradation | TEXT | Pixel rot, delamination, burn-in |
| wiring_harness_decay | TEXT | Biodegradable insulation, rodent |
| connector_corrosion | TEXT | |
| pcb_conformal_coating | BOOLEAN | |
| solder_whisker_risk | BOOLEAN | Lead-free solder tin whisker concern |
| known_replacement_ecus | TEXT | Are refurb/reman ECUs available |
| electronics_repairability | TEXT | Easy, moderate, board-level, FUBAR |
| extra | JSON | |

### DATA_SOURCES

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| car_id | INTEGER FK | References CARS |
| url | TEXT | Source URL |
| site_name | TEXT | ZePerfs, Wikipedia, etc. |
| raw_text | TEXT | Full raw pasted text (preserved for re-parsing) |
| parsed_at | DATETIME | When LLM parsed this |
| dimension | TEXT | Which dimension table was populated |

### LLM_ANALYSES

| Column | Type | Notes |
|--------|------|-------|
| car_id | INTEGER FK | References CARS |
| dimension | TEXT | Which dimension was analyzed |
| prompt_hash | TEXT | Hash of prompt for reproducibility |
| model_used | TEXT | e.g. "gpt-4o", "claude-3.5-sonnet" |
| generated_text | TEXT | LLM output |
| scores | JSON | Numeric scores extracted |
| created_at | DATETIME | |

### COMPARISON_SESSIONS

| Column | Type | Notes |
|--------|------|-------|
| id | INTEGER PK | |
| name | TEXT | e.g. "90s JDM Icons" |
| car_ids | JSON | Array of car IDs |
| created_at | DATETIME | |
| last_viewed | DATETIME | |

---

## Architecture

### Directory Structure

```
motorgeek/
  cli/                    # Typer CLI (data entry, quick queries)
    commands/
      car_cmds.py         # add, edit, list, delete cars
      ingest_cmds.py      # paste raw data -> LLM parse -> save
      compare_cmds.py     # quick terminal comparisons
      query_cmds.py       # natural language search
      calc_cmds.py        # derived calculations
      market_cmds.py      # market history tracking
      repair_cmds.py      # repair cost tracking
      scrape_cmds.py      # browser extension / Playwright scraping stub
    prompts/              # LLM prompt templates per dimension
  core/                   # Shared domain logic (no CLI/web deps)
    models.py             # SQLAlchemy ORM models (all tables)
    database.py           # SQLite connection, migrations (Alembic)
    llm.py                # LLM client abstraction
    pipeline.py           # Paste -> parse -> validate -> save pipeline
    analysis.py           # Comparison engine, scoring, rankings
    enrichment.py         # Gap-filling, inference logic
    calculations.py       # Derived metrics (power-to-weight, etc.)
  web/                    # FastAPI + Jinja2 + HTMX
    app.py                # FastAPI server entry
    routes/
      cars.py             # CRUD pages
      compare.py          # Multi-car comparison views
      query.py            # NL query interface
      insights.py         # Aggregate insights
    templates/            # Jinja2 HTML templates
    static/               # CSS, Chart.js, htmx
    charts.py             # Chart data generation helpers
  data/                   # SQLite DB lives here (gitignored)
  config.yaml             # LLM provider, API keys, preferences
  pyproject.toml
```

### Data Flow

```
You copy-paste raw specs
  |
  v
CLI (ingest_cmds.py)
  |
  v
LLM Pipeline (core/pipeline.py)
  1. Dimension Router: classify text -> ["performance", "engineering_ice"]
  2. Structured Extraction: prompt templates per table schema
  3. Entity Resolution: match to existing car or create new
  4. Enrichment (async): LLM fills gaps from similar cars
  |
  v
Review Step (CLI)
  - Review table with fields, values, confidence flags
  - Edit, accept, skip, or reject each dimension
  |
  v
SQLite DB (all tables)
  + DATA_SOURCES row (raw text saved)
  |
  +---> CLI queries (compare, query, calc, rank)
  +---> Web UI (browse, compare charts, NL chat)
```

### Technology Stack

| Layer | Choice | Why |
|-------|--------|-----|
| CLI framework | Typer | Rich terminal output, autocomplete, clean |
| ORM + migrations | SQLAlchemy + Alembic | Mature, schema migration support |
| Web framework | FastAPI | Async, native JSON, Jinja2 templates |
| Frontend | Jinja2 + HTMX + Chart.js | No JS build step, server-rendered |
| LLM client | LiteLLM or direct openai/anthropic SDKs | Provider flexibility |
| Config | YAML (PyYAML) | Human-readable |
| Testing | pytest | Standard, fast |

---

## CLI Design

### Command Tree

```
motorgeek
  car add <make> <model>        Create a new car entry
    --year-start, --year-end, --generation, --body-style, --country
  car list                      List all cars in DB
    --era, --make, --country
  car show <id|slug>            Show full car profile (all dimensions)
    --dimension perf|eng|rel|...
  car edit <id|slug>            Edit a car's core fields
  car delete <id|slug>          Remove a car and all its data

  ingest <id|slug>              Paste raw data for a car
    --dimension auto|perf|eng|...
  ingest batch                  Paste a block with multiple cars

  compare <car1> <car2> [...]   Side-by-side comparison
    --dimensions perf,eng,cost
    --format table|radar|narrative
  compare group <name>          Use a saved COMPARISON_SESSION

  query "<natural language>"    Ask anything about your car DB

  calc power-to-weight <car>    Auto-computed from HP / weight
  calc inflation <car>          Adjust MSRP to today's dollars
  calc depreciation <car>       Curve from MARKET_HISTORY data
  calc cost-per-hp <car>        Current market price / HP
  calc cost-per-lb <car>        Price / curb weight
  calc hp-per-liter <car>       Specific output (ICE only)
  calc range-anxiety <car>      EV range as % of nearest gas equivalent

  rank <metric>                 Rank all cars by any scalar field
  era compare <era1> <era2>     Aggregate era-vs-era stats
  lineage <car>                 Show predecessor/successor chain

  what-if <car>                 LLM-powered speculative analysis
  insight                       LLM scans your whole DB for patterns

  market add <car>              Log a new MARKET_HISTORY entry
    --price-low, --price-high, --source, --date
  market chart <car>            Show price trend over time

  repair add <car>              Log a repair event
    --cost, --category, --source
  repair catalog <car>          Show baseline repair costs from RepairPal etc.

  score <car>                   Generate LLM subjective scoring
    --dimension design|significance|soul

  export <car|compare>          Export data to JSON/CSV
  serve                         Launch the web UI
    --port, --host

  scrape <url>                  Stub: capture page via browser extension or Playwright
    --profile <name>            Browser profile to use (Playwright path)
    --extension                 Use browser extension companion instead
    (Falls back to manual copy-paste if neither available)

  config                        Manage LLM provider, API keys
    set llm.provider openai
```

### Ingest Review Flow

```
$ motorgeek ingest "porsche 911 turbo 996"

1. CLI resolves slug to existing car or offers to create it
2. Opens $EDITOR (or reads from stdin) with a blank buffer
3. You paste raw text from ZePerfs, forums, spec sheets
4. Save and exit. Pipeline kicks in:
   - Dimension router classifies the text
   - Structured extraction pulls fields
   - Shows review table with fields, values, confidence flags
5. Review table:

   Porsche 911 Turbo (996) - Performance
   +-------------+------------+--------------------------+
   | Field       | Value      | Confidence               |
   +-------------+------------+--------------------------+
   | 0-60 mph    | 4.2s       | high                     |
   | 0-100 mph   | 9.5s       | medium                   |
   | Top speed   | 189 mph    | high                     |
   | 1/4 mile    | 12.1s      | medium                   |
   | Power/wt    | (missing)  | missing                  |
   +-------------+------------+--------------------------+
   [E]dit specific values  [A]ccept all  [S]kip  [R]eject

6. Accepted data writes to DB. Raw text saved to DATA_SOURCES.
```

### Natural Language Query

```
$ motorgeek query "show me all coupes from the 90s with a manual
                   transmission that cost under $20k today"
```

LLM translates to SQL, shows the generated query, asks confirm before running, formats results.

---

## Calculations & Derived Metrics

Auto-calculated when source fields change:

| Derived field | Stored in | Formula |
|---|---|---|
| power_to_weight | PERFORMANCE | horsepower_bhp / (curb_weight_kg / 1000) |
| hp_per_liter | POWERTRAIN_ICE | horsepower_bhp / (displacement_cc / 1000) |
| cost_per_hp | COST_TO_OWN | avg of most recent MARKET_HISTORY (price_low+price_high)/2 / horsepower_bhp |
| msrp_inflation_adj | COST_TO_OWN | msrp_original * CPI inflation multiplier (auto from year_start to current year) |
| reliability_normalized | RELIABILITY | Weighted composite: (1 - recall_count/avg_recalls) * 40 + part_availability_score * 30 + (1 - len(common_failures)/max_failures) * 30, clamped 0-100 |
| combined_score | COMPARISON_SESSIONS | Weighted avg of dimension scores from LLM_ANALYSES (weights configurable per session) |

---

## Web App Design

### Pages

- **Garage**: Card grid of all cars, click to expand detail panel. Filters: era, make, drivetrain.
- **Compare**: Select 2-6 cars. Tabs: Radar Chart, Spec Table, Market Timeline, Narrative (LLM), Era Context.
- **Query**: Chat-style NL interface. Results as cards + charts.
- **Insights**: LLM scans your DB for non-obvious patterns. Depreciation curves by era. Market heatmap.

### Comparison View Tabs

1. **Radar Chart**: 5-axis spider chart (Performance, Engineering, Reliability, Cost-to-Own, Historical significance). Each car gets a colored polygon.
2. **Spec Table**: Sortable, filterable table with every scalar field. Winner per row gets subtle green highlight. Fields with known_spec_conflicts get a warning icon.
3. **Market Timeline**: Line chart of MARKET_HISTORY entries overlaid. Spot depreciation curve bottoms.
4. **Narrative**: LLM-generated prose comparing selected cars. Editable/regeneratable.
5. **Era Context**: Timeline visualization showing where each car sits in history, with predecessor/successor lines.

### Tech Specifics

- HTMX for partial page swaps (no SPA framework)
- Chart.js for all charts (radar, line, bar, scatter)
- Server-sent events via FastAPI for streaming LLM narrative generation
- Responsive design, mobile-usable
- Dark mode by default

---

## Data Scraping Approach

| Approach | Feasibility | For MotorGeek? |
|---|---|---|
| Direct HTTP scrape | Most sites block headless browsers, serve captchas | No - brittle, high maintenance |
| Browser extension capture | Extension sees the rendered DOM you're already browsing | Yes - one-click capture while you browse normally |
| Playwright with your real browser profile | Uses your logged-in browser session, looks like a human | Maybe - more setup, but powerful |
| Manual copy-paste + LLM | You browse, you select, you paste | Primary path - zero friction, always works |

The spec includes a `scrape` command stub that talks to a browser extension companion (or uses your real Chrome profile via Playwright) as an optional acceleration path. The system never depends on it - manual ingest is the guaranteed fallback. The extension's message format is documented but not blocking.

---

## LLM Pipeline Design

### Pipeline Steps

1. **Dimension Router**: Classify pasted text into one or more dimensions (performance, engineering_ice, engineering_ev, reliability, consumables, cost, historical, mod_potential, electronics, repair_catalog).
2. **Structured Extraction**: Use prompt templates matched to each table schema. Extract fields with confidence scores.
3. **Entity Resolution**: Match car name to existing CARS entry or prompt to create new one. Handle generation ambiguity.
4. **Enrichment (async/optional)**: LLM fills gaps by cross-referencing similar cars. "We have 0-60 and weight but no power. Can we estimate?"
5. **Review & Accept**: CLI shows review table. User edits, accepts, skips, or rejects.

### Prompt Templates

Each dimension has a dedicated prompt template that:
- Describes the target table schema
- Provides examples of good extractions
- Instructs the LLM to output structured JSON with confidence scores
- Handles edge cases (missing fields, ambiguous values, unit conversions)

### Caching

LLM-generated analyses are cached in LLM_ANALYSES with prompt_hash for reproducibility. Narratives, scores, and enrichments are stored and can be regenerated or replayed.

---

## Repair Cost Tracking

Two tables support repair cost analysis:

- **REPAIR_COSTS**: Individual repair events with actual costs, dates, mileage, shop type, and source.
- **REPAIR_CATALOG**: Baseline reference costs from RepairPal, CarMD, NHTSA, and community sources. Includes frequency, severity, DIY difficulty, and tools required.

Together they enable:
- "My actual costs vs. industry averages" comparisons
- "What repairs should I budget for at 100k miles?" queries
- "Which car has the cheapest long-term maintenance?" rankings
- Repair cost trend analysis over time

---

## Future Considerations

- **Browser extension**: One-click capture from ZePerfs, Wikipedia, forum threads while browsing.
- **Playwright integration**: Use your real browser profile for authenticated scraping.
- **RepairPal API integration**: If available, auto-populate REPAIR_CATALOG from RepairPal data.
- **CarMD integration**: Diagnostic trouble code database integration.
- **NHTSA recall API**: Auto-populate recall data.
- **Hagerty valuation data**: Market history from Hagerty's valuation tools.

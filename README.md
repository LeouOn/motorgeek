# 🔧 MotorGeek

**Your personal car analysis and comparison tool** — ingest specs from anywhere, compare cars across dimensions, and chat with an AI agent about your collection.

## Quick Start

```bash
# 1. Install
pip install -e .

# 2. Configure your LLM (pick one)
# Option A: Edit config.yaml (copy from config.example.yaml)
cp config.example.yaml config.yaml
# Then edit config.yaml to set your provider + API key

# Option B: Use environment variables
export DEEPSEEK_API_KEY=sk-...

# 3. Seed the database with sample cars
python seed_data.py

# 4. Start the web app
motorgeek serve

# 5. Open http://localhost:8765
```

## Features

### 🏎️ Car Collection
- **Add cars** via CLI: `motorgeek car add "Porsche" "911 Turbo" --year-start 1998 --generation 996`
- **Edit/delete** from web UI or CLI
- **Browse** your garage with filters by era, country, body style

### 🤖 Agentic Ingestion
Paste raw spec data from ZePerfs, KBB, Wikipedia, manufacturer sites — the AI agent extracts structured fields, identifies gaps, and asks you questions to fill in missing data.

```bash
# CLI
motorgeek ingest paste    # opens your editor, paste raw data, save

# Web
# Visit http://localhost:8765/ingest — paste in the browser
```

### 📊 Multi-Car Comparison
Compare 2-6 cars across performance, engineering, reliability, cost-to-own, and historical significance.

```bash
# CLI
motorgeek compare 2 3 4 5

# Web
# Visit http://localhost:8765/compare — enter car IDs
```

### 🧠 AI Agent Chat
Ask natural language questions about your collection. The agent uses **tool calling** to search, compare, and analyze your cars.

```bash
# CLI
motorgeek query "show me all coupes from the 90s with manual transmission"

# Web
# Visit http://localhost:8765/query — chat with the agent
```

### 📈 Rankings & Stats
```bash
motorgeek calc rank 0-60           # fastest by acceleration
motorgeek calc rank power-weight   # best power-to-weight
motorgeek calc rank reliability    # most reliable
motorgeek calc era-compare 90s 00s # era vs era stats
motorgeek calc inflation "porsche 911"  # MSRP adjusted to today
```

### 🔧 Maintenance Tracking
```bash
motorgeek repair add 2 --cost 1200 --category brakes --source "indy shop"
motorgeek repair catalog 2         # common repairs + costs
motorgeek market add 2 --price-low 45000 --price-high 85000
```

## Architecture

```
CLI (Typer)          Web (FastAPI + Jinja2 + HTMX)
     │                      │
     └──────────┬───────────┘
                │
          core/ (SQLAlchemy + Alembic)
                │
          SQLite DB (data/motorgeek.db)
                │
          ┌─────┴─────┐
     agent.py    tools.py    ingest.py
     (agent      (7 tools)   (paste→save
      loop)                   pipeline)
```

### Schema (23 tables)
- **cars** — core identity (make, model, generation, era, body, country)
- **performance** — 0-60, quarter mile, top speed, lateral G
- **powertrain_ice** / **powertrain_ev** — engine/motor specs
- **hybrid_systems** — detailed hybrid system data
- **reliability** — scores, common failures, repair costs
- **cost_to_own** — MSRP, fuel economy, depreciation
- **market_history** — price trends over time
- **repair_costs** / **repair_catalog** — maintenance tracking
- **dimensions** — L×W×H, wheelbase, tracks
- **performance_measurements** — individual test results per source
- **zeperfs_indices** — ZePerfs sportivity + performance indices
- **car_reviews** — consumer + expert ratings
- **historical_context** — design philosophy, innovations, competitors
- **mod_potential** — tuning potential, common mods
- **electronics** — ECU, sensors, bus architecture
- **consumables_and_specs** — tire sizes, fluid capacities
- **data_sources** — raw text preservation
- **llm_analyses** — cached LLM outputs
- **comparison_sessions** — saved comparisons
- **ingest_sessions** — paste-to-save state machine
- **agent_tool_calls** — tool call audit log

### Agent Tools
| Tool | Description |
|------|------------|
| `get_collection_overview` | Count, era/country/body breakdown, HP range |
| `list_all_cars` | All cars with key stats sorted by power-to-weight |
| `search_cars(query)` | Search by make, model, keyword |
| `get_car_detail(car_id)` | Full specs for one car |
| `compare_cars(car_ids)` | Side-by-side comparison |
| `suggest_comparisons(car_id)` | Find interesting cars to compare |
| `save_ingest_data()` | Save current ingest session to DB |

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run with coverage
pytest --cov=motorgeek --cov-report=term-missing

# Create migration after model changes
alembic revision --autogenerate -m "description"
alembic upgrade head

# Start dev server
motorgeek serve --port 8765
```

## Configuration

See `config.example.yaml` for all options. Supports OpenAI, Anthropic, and DeepSeek providers.

## License

MIT

# MotorGeek Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bootstrap a working MotorGeek CLI + web application from the spec at `docs/superpowers/specs/2026-05-24-motorgeek-design.md`.

**Architecture:** Python CLI (Typer) + web (FastAPI + Jinja2 + HTMX), SQLite (SQLAlchemy + Alembic), LLM pipeline for parsing pasted car data. CLI-first, web-second. All domain logic lives in `core/` with zero CLI/web dependencies.

**Tech Stack:** Python 3.11+, Typer, SQLAlchemy, Alembic, FastAPI, Jinja2, HTMX, Chart.js, LiteLLM

---

## Phase 1: Project Foundation

### Task 1: Scaffold project structure and pyproject.toml

**Files:**
- Create: `motorgeek/pyproject.toml`
- Create: `motorgeek/config.yaml`
- Create: `motorgeek/.gitignore`

- [ ] **Step 1: Create pyproject.toml**

```toml
[project]
name = "motorgeek"
version = "0.1.0"
description = "Car analysis and comparison tool"
requires-python = ">=3.11"
dependencies = [
    "typer[all]",
    "sqlalchemy>=2.0",
    "alembic",
    "pyyaml",
    "openai>=1.0",
    "anthropic>=0.20",
    "fastapi>=0.110",
    "jinja2>=3.1",
    "uvicorn[standard]",
    "httpx",
    "rich>=13.0",
    "click",
]

[project.optional-dependencies]
dev = ["pytest", "pytest-cov", "ruff"]

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```

- [ ] **Step 2: Create config.yaml**

```yaml
llm:
  provider: openai
  model: gpt-4o
  api_key: ""

database:
  path: data/motorgeek.db

scraping:
  browser_extension_port: 8765
  playwright_profile: null
```

- [ ] **Step 3: Create .gitignore**

```
data/*.db
__pycache__/
*.pyc
.pytest_cache/
.coverage
.ruff_cache/
.env
*.egg-info/
dist/
build/
```

- [ ] **Step 4: Commit**

```bash
git add pyproject.toml config.yaml .gitignore
git commit -m "feat: project scaffold"
```

---

### Task 2: Database models and migrations

**Files:**
- Create: `motorgeek/core/__init__.py`
- Create: `motorgeek/core/models.py`
- Create: `motorgeek/core/database.py`
- Create: `motorgeek/tests/test_models.py`

- [ ] **Step 1: Write failing test**

```python
# tests/test_models.py
from motorgeek.core.models import Car

def test_car_creation():
    car = Car(make="Porsche", model="911 Turbo", generation="996", year_start=1998, year_end=2005)
    assert car.make == "Porsche"
    assert car.generation == "996"

def test_car_slug():
    car = Car(make="Porsche", model="911 Turbo", generation="996", year_start=1998, year_end=2005)
    assert car.slug == "porsche-911-turbo-996"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_models.py -v`
Expected: FAIL — module not found

- [ ] **Step 3: Create core/models.py with all 13 tables**

Create the file with all SQLAlchemy models: Car, Performance, PowertrainICE, PowertrainEV, HybridSystem, Reliability, ConsumablesAndSpecs, CostToOwn, MarketHistory, RepairCosts, RepairCatalog, HistoricalContext, ModPotential, Electronics, DataSource, LLMAnalyses, ComparisonSession.

- [ ] **Step 4: Create core/database.py**

```python
# motorgeek/core/database.py
import yaml
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

_engine = None
_SessionLocal = None

def get_db_path() -> Path:
    config_path = Path("config.yaml")
    if config_path.exists():
        with open(config_path) as f:
            config = yaml.safe_load(f)
        return Path(config.get("database", {}).get("path", "data/motorgeek.db"))
    return Path("data/motorgeek.db")

def get_engine():
    global _engine
    if _engine is None:
        db_path = get_db_path()
        db_path.parent.mkdir(parents=True, exist_ok=True)
        _engine = create_engine(f"sqlite:///{db_path}", echo=False)
    return _engine

def get_session() -> Session:
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(bind=get_engine())
    return _SessionLocal()

def init_db():
    from motorgeek.core.models import Base
    engine = get_engine()
    Base.metadata.create_all(engine)
```

- [ ] **Step 5: Run test to verify it passes**

Run: `pytest tests/test_models.py -v`
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add motorgeek/core/ tests/test_models.py
git commit -m "feat: SQLAlchemy models for all 13 tables"
```

---

### Task 3: CLI scaffold — car commands and Typer app

**Files:**
- Create: `motorgeek/cli/__init__.py`
- Create: `motorgeek/cli/main.py`
- Create: `motorgeek/cli/commands/__init__.py`
- Create: `motorgeek/cli/commands/car_cmds.py`
- Create: `motorgeek/cli/commands/ingest_cmds.py` (stub)
- Create: `motorgeek/cli/commands/compare_cmds.py` (stub)
- Create: `motorgeek/cli/commands/query_cmds.py` (stub)
- Create: `motorgeek/cli/commands/calc_cmds.py` (stub)
- Create: `motorgeek/cli/commands/market_cmds.py` (stub)
- Create: `motorgeek/cli/commands/repair_cmds.py` (stub)
- Create: `motorgeek/tests/test_car_cmds.py`

- [ ] **Step 1: Write failing test**

```python
# tests/test_car_cmds.py
from click.testing import CliRunner
from motorgeek.cli.main import app

runner = CliRunner()

def test_car_list_empty():
    result = runner.invoke(app, ["car", "list"])
    assert result.exit_code == 0
    assert "No cars in database" in result.output

def test_car_add():
    result = runner.invoke(app, ["car", "add", "Porsche", "911 Turbo", "--year-start", "1998", "--generation", "996"])
    assert result.exit_code == 0
    assert "Created" in result.output
```

- [ ] **Step 2: Run test to verify it fails**
Expected: FAIL — module not found

- [ ] **Step 3: Create CLI main.py with Typer app**

```python
# motorgeek/cli/main.py
import typer
from motorgeek.core.database import init_db

app = typer.Typer(name="motorgeek", help="Car analysis and comparison tool")

@app.on_startup
def startup():
    init_db()

from motorgeek.cli.commands import car_cmds, ingest_cmds, compare_cmds, query_cmds, calc_cmds, market_cmds, repair_cmds

app.add_typer(car_cmds.app, name="car")
app.add_typer(ingest_cmds.app, name="ingest")
app.add_typer(compare_cmds.app, name="compare")
app.add_typer(query_cmds.app, name="query")
app.add_typer(calc_cmds.app, name="calc")
app.add_typer(market_cmds.app, name="market")
app.add_typer(repair_cmds.app, name="repair")

if __name__ == "__main__":
    app()
```

- [ ] **Step 4: Create car_cmds.py with add/list/show commands**

Implement `car_add`, `car_list`, `car_show` with Rich tables, database session, and slug resolution.

- [ ] **Step 5: Create stub files for all other command modules**

Each stub: `import typer; app = typer.Typer(name="...")`

- [ ] **Step 6: Run test to verify it passes**
Expected: PASS

- [ ] **Step 7: Commit**

```bash
git add motorgeek/cli/ motorgeek/__init__.py
git commit -m "feat: CLI scaffold with car add/list/show commands"
```

---

### Task 4: LLM client abstraction

**Files:**
- Create: `motorgeek/core/llm.py`
- Create: `motorgeek/tests/test_llm.py`

- [ ] **Step 1: Write failing test**

```python
# tests/test_llm.py
from motorgeek.core.llm import LLMClient

def test_llm_client_initializes():
    client = LLMClient(provider="openai", model="gpt-4o")
    assert client.provider == "openai"
```

- [ ] **Step 2: Run test to verify it fails**
Expected: FAIL

- [ ] **Step 3: Create core/llm.py**

LLMClient class with `complete(prompt)` and `complete_json(prompt)` methods, supporting OpenAI and Anthropic providers. Loads config from config.yaml.

- [ ] **Step 4: Run test to verify it passes**
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add motorgeek/core/llm.py tests/test_llm.py
git commit -m "feat: LLM client abstraction for OpenAI and Anthropic"
```

---

### Task 5: Ingest pipeline (paste → parse → review → save)

**Files:**
- Create: `motorgeek/core/pipeline.py`
- Create: `motorgeek/cli/commands/ingest_cmds.py` (real implementation)
- Create: `motorgeek/cli/prompts/performance.txt`
- Create: `motorgeek/cli/prompts/engineering_ice.txt`
- Create: `motorgeek/cli/prompts/reliability.txt`
- Create: `motorgeek/tests/test_pipeline.py`

- [ ] **Step 1: Write failing test**

```python
# tests/test_pipeline.py
from motorgeek.core.pipeline import DimensionRouter

def test_dimension_router():
    router = DimensionRouter()
    result = router.route("0-60 in 4.2 seconds, top speed 189 mph")
    assert "performance" in result
```

- [ ] **Step 2: Run test to verify it fails**
Expected: FAIL

- [ ] **Step 3: Create core/pipeline.py**

```python
# motorgeek/core/pipeline.py
from motorgeek.core.llm import LLMClient

class DimensionRouter:
    DIMENSIONS = [
        "performance", "engineering_ice", "engineering_ev",
        "reliability", "consumables", "cost_to_own",
        "historical_context", "mod_potential", "electronics",
        "repair_catalog", "hybrid_system"
    ]

    def route(self, text: str) -> list[str]:
        # Uses LLM to classify text into one or more dimensions
        # Returns list of dimension names
        pass

class StructuredExtractor:
    def extract(self, text: str, dimension: str) -> dict:
        # Uses LLM with dimension-specific prompt template
        # Returns dict with field values and _confidence scores
        pass

class IngestPipeline:
    def run(self, raw_text: str, car_id: int, dimension_hint: str = None):
        # Route → Extract → Return results dict
        pass
```

- [ ] **Step 4: Create ingest_cmds.py with real implementation**

Opens $EDITOR for paste, runs pipeline, displays review table with confidence flags using Rich.

- [ ] **Step 5: Create prompt template files**

Text files for performance, engineering_ice, reliability dimensions with extraction instructions.

- [ ] **Step 6: Run test to verify it passes**
Expected: PASS

- [ ] **Step 7: Commit**

```bash
git add motorgeek/core/pipeline.py motorgeek/cli/commands/ingest_cmds.py motorgeek/cli/prompts/
git commit -m "feat: LLM ingest pipeline with dimension routing and review table"
```

---

### Task 6: Compare, calc, and rank commands

**Files:**
- Create: `motorgeek/core/analysis.py`
- Create: `motorgeek/core/calculations.py`
- Modify: `motorgeek/cli/commands/compare_cmds.py`
- Modify: `motorgeek/cli/commands/calc_cmds.py`
- Create: `motorgeek/tests/test_analysis.py`

- [ ] **Step 1: Write failing test**

```python
# tests/test_analysis.py
from motorgeek.core.analysis import calculate_power_to_weight

def test_calculate_power_to_weight():
    result = calculate_power_to_weight(355, 1550)
    assert abs(result - 229.0) < 0.1
```

- [ ] **Step 2: Run test to verify it fails**
Expected: FAIL

- [ ] **Step 3: Create core/analysis.py**

```python
# motorgeek/core/analysis.py
def calculate_power_to_weight(hp: float, weight_kg: float) -> float:
    if not weight_kg:
        return 0.0
    return round(hp / (weight_kg / 1000), 2)

def calculate_hp_per_liter(hp: float, displacement_cc: int) -> float:
    if not displacement_cc:
        return 0.0
    return round(hp / (displacement_cc / 1000), 2)

def calculate_msrp_inflation_adj(msrp: float, year: int, current_year: int = 2026) -> float:
    # CPI multipliers lookup table for each year
    # Returns msrp * multiplier
    pass

def rank_cars(session, metric: str, limit: int = 20) -> list:
    # Query cars by metric (0-60, power-to-weight, reliability, etc.)
    # Returns [(car, value, label), ...]
    pass

def era_compare(session, era1: str, era2: str) -> dict:
    # Aggregate stats for two eras
    # Returns {era1: {avg_hp, avg_weight, avg_0_60, count}, era2: {...}}
    pass
```

- [ ] **Step 4: Replace compare_cmds.py**

`compare` command: takes car slugs/IDs, shows side-by-side table with metrics. `group` command: uses saved ComparisonSession.

- [ ] **Step 5: Replace calc_cmds.py**

Commands: `power-to-weight`, `hp-per-liter`, `inflation`, `cost-per-hp`, `range-anxiety`. Each calls analysis functions.

- [ ] **Step 6: Run test to verify it passes**
Expected: PASS

- [ ] **Step 7: Commit**

```bash
git add motorgeek/core/analysis.py motorgeek/cli/commands/compare_cmds.py motorgeek/cli/commands/calc_cmds.py
git commit -m "feat: compare and calc CLI commands with derived metrics"
```

---

### Task 7: Web app scaffold (FastAPI + Jinja2 + HTMX)

**Files:**
- Create: `motorgeek/web/app.py`
- Create: `motorgeek/web/routes/__init__.py`
- Create: `motorgeek/web/routes/cars.py`
- Create: `motorgeek/web/routes/compare.py`
- Create: `motorgeek/web/charts.py`
- Create: `motorgeek/web/templates/base.html`
- Create: `motorgeek/web/templates/cars/list.html`
- Create: `motorgeek/web/templates/cars/detail.html`
- Create: `motorgeek/web/templates/compare/index.html`
- Create: `motorgeek/web/static/css/main.css`
- Create: `motorgeek/tests/test_web.py`

- [ ] **Step 1: Write failing test**

```python
# tests/test_web.py
from motorgeek.web.app import app

def test_app_exists():
    assert app is not None
```

- [ ] **Step 2: Run test to verify it fails**
Expected: FAIL

- [ ] **Step 3: Create web/app.py**

FastAPI app with mount for static files, Jinja2 templates, startup init_db.

- [ ] **Step 4: Create routes**

`cars.py`: list and detail endpoints. `compare.py`: compare endpoint with radar chart data.

- [ ] **Step 5: Create charts.py**

```python
# motorgeek/web/charts.py
def build_radar_data(cars: list, perf_data: dict, rel_data: dict, cost_data: dict) -> dict:
    # Returns {labels: [...], datasets: [...]} for Chart.js radar chart
    pass

def build_market_chart_data(car_id: int, market_entries: list) -> dict:
    # Returns {labels: [...], datasets: [...]} for Chart.js line chart
    pass
```

- [ ] **Step 6: Create templates**

base.html with dark theme CSS, nav, Chart.js, HTMX. list.html: car grid. detail.html: specs. compare/index.html: radar chart + comparison table.

- [ ] **Step 7: Create main.css**

Dark theme (#0d1117 background), car grid, comparison table, spec grid.

- [ ] **Step 8: Run test to verify it passes**
Expected: PASS

- [ ] **Step 9: Commit**

```bash
git add motorgeek/web/
git commit -m "feat: FastAPI web app with garage browse, car detail, and compare views"
```

---

### Task 8: Market commands and repair commands

**Files:**
- Modify: `motorgeek/cli/commands/market_cmds.py`
- Modify: `motorgeek/cli/commands/repair_cmds.py`
- Create: `motorgeek/tests/test_market_repair.py`

- [ ] **Step 1: Write failing test**

```python
# tests/test_market_repair.py
from datetime import datetime
from motorgeek.core.models import MarketHistory

def test_market_history_fields():
    mh = MarketHistory(car_id=1, date_recorded=datetime(2026, 1, 1), price_low=15000, price_high=20000)
    assert mh.price_low == 15000
```

- [ ] **Step 2: Run test to verify it fails**
Expected: FAIL

- [ ] **Step 3: Replace market_cmds.py**

`market add`: log price entry with date, source, trend. `market chart`: display table of all market entries for a car.

- [ ] **Step 4: Replace repair_cmds.py**

`repair add`: log repair event with cost breakdown, category, shop type, recall flag. `repair catalog`: display RepairCatalog baseline costs.

- [ ] **Step 5: Run test to verify it passes**
Expected: PASS

- [ ] **Step 6: Commit**

```bash
git add motorgeek/cli/commands/market_cmds.py motorgeek/cli/commands/repair_cmds.py
git commit -m "feat: market and repair cost tracking commands"
```

---

### Task 9: Query command and enrichment

**Files:**
- Create: `motorgeek/core/enrichment.py`
- Modify: `motorgeek/cli/commands/query_cmds.py`

- [ ] **Step 1: Create core/enrichment.py**

```python
# motorgeek/core/enrichment.py
def fill_power_to_weight_gaps(session: Session) -> int:
    # Find all cars with missing power_to_weight but have HP and weight
    # Calculate and backfill. Return count of updated records.
    pass

def enrich_from_similar(session: Session, car: Car, dimension: str) -> dict:
    # Use LLM to estimate missing fields by comparing to similar era/segment cars
    pass
```

- [ ] **Step 2: Replace query_cmds.py**

`query` command: takes natural language question, builds context from car DB, calls LLM for answer, prints response.

- [ ] **Step 3: Commit**

```bash
git add motorgeek/core/enrichment.py motorgeek/cli/commands/query_cmds.py
git commit -m "feat: NL query command and data enrichment pipeline"
```

---

## Spec Coverage Checklist

| Spec Section | Task |
|---|---|
| Schema (all 13 tables) | Task 2 |
| Architecture / directory structure | Task 1 |
| CLI command tree (all commands) | Tasks 3, 5, 6, 8, 9 |
| Ingest review flow | Task 5 |
| Natural language query | Task 9 |
| Calculations & derived metrics | Task 6 |
| Web app pages and tabs | Task 7 |
| LLM pipeline | Tasks 4, 5 |
| Scraping approach (stub) | Task 1 (config) |
| Repair cost tracking | Task 8 |

**Gaps identified:** None. All major spec sections have a corresponding task.

---

**On completion:** Working MotorGeek CLI — `car add`, `ingest` pasted data, `compare` cars, `serve` web UI. `pip install -e .` then `motorgeek car add Porsche 911 --year-start 1998` should work end-to-end.

**Two execution options:**

1. **Subagent-Driven (recommended)** — Fresh subagent per task, review between tasks
2. **Inline Execution** — Execute in this session with checkpoints

Which approach?
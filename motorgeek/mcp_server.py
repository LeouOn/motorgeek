"""MCP server for MotorGeek — exposes all 15 agent tools via the Model Context Protocol.

Use with Claude Desktop, OpenCode, or any MCP-compatible agent.
Start with: motorgeek mcp serve
"""

import json
from typing import Optional

from mcp.server.fastmcp import FastMCP

from motorgeek.core.database import get_session, init_db
from motorgeek.core.tools import execute_tool

# ── Server setup ────────────────────────────────────────────────────────────

mcp = FastMCP(
    name="motorgeek",
    instructions="MotorGeek — car collection analysis and comparison. "
    "169 cars scored across reliability (5 dims) and build quality (6 dims). "
    "Use tools to search, compare, rank, enrich, and analyze cars.",
)


# ── DB helper ───────────────────────────────────────────────────────────────

def _tool(name: str, args: dict, session_id: Optional[int] = None) -> dict:
    """Run a tool by name with a fresh DB session."""
    init_db()
    db = get_session()
    try:
        result = execute_tool(name, args, db, ingest_session_id=session_id)
        # Convert any non-serializable values
        return _sanitize(result)
    finally:
        db.close()


def _sanitize(obj):
    """Ensure the result is JSON-safe."""
    return json.loads(json.dumps(obj, default=str))


# ── Tool: collection overview ────────────────────────────────────────────────

@mcp.tool(
    name="get_collection_overview",
    description="Get an overview of the entire car collection: how many cars, era breakdown, horsepower range, country distribution.",
)
def get_collection_overview() -> dict:
    return _tool("get_collection_overview", {})


# ── Tool: search cars ────────────────────────────────────────────────────────

@mcp.tool(
    name="search_cars",
    description="Search the car collection by make, model, generation, or keywords. Returns matching cars with basic info.",
)
def search_cars(query: str) -> dict:
    return _tool("search_cars", {"query": query})


# ── Tool: list all cars ──────────────────────────────────────────────────────

@mcp.tool(
    name="list_all_cars",
    description="List all cars in the collection with their key stats: ID, name, horsepower, 0-60, weight, price. Use to browse the collection.",
)
def list_all_cars() -> dict:
    return _tool("list_all_cars", {})


# ── Tool: get car detail ─────────────────────────────────────────────────────

@mcp.tool(
    name="get_car_detail",
    description="Get full specifications for a specific car: performance, powertrain, reliability, dimensions, market data, repair catalog.",
)
def get_car_detail(car_id: int) -> dict:
    return _tool("get_car_detail", {"car_id": car_id})


# ── Tool: compare cars ───────────────────────────────────────────────────────

@mcp.tool(
    name="compare_cars",
    description="Compare multiple cars side-by-side. Returns key specs (HP, 0-60, weight, price) for easy comparison. Provide 2-6 car IDs.",
)
def compare_cars(car_ids: list[int]) -> dict:
    return _tool("compare_cars", {"car_ids": car_ids})


# ── Tool: suggest comparisons ────────────────────────────────────────────────

@mcp.tool(
    name="suggest_comparisons",
    description="Suggest cars in the collection that would be interesting to compare with a given car, based on similar era, power, price, or body style.",
)
def suggest_comparisons(car_id: int) -> dict:
    return _tool("suggest_comparisons", {"car_id": car_id})


# ── Tool: compare family ─────────────────────────────────────────────────────

@mcp.tool(
    name="compare_family",
    description="Compare all variants/generations within a car family (e.g., '911', 'M3', 'Supra', 'S-Class'). Shows side-by-side specs.",
)
def compare_family(family: str) -> dict:
    return _tool("compare_family", {"family": family})


# ── Tool: qualitative analysis ───────────────────────────────────────────────

@mcp.tool(
    name="get_qualitative_analysis",
    description="Retrieve stored qualitative analysis, platform comparisons, reliability assessments, and recommendations from Perplexity deep-dives.",
)
def get_qualitative_analysis(car_id: Optional[int] = None, keyword: Optional[str] = None) -> dict:
    return _tool("get_qualitative_analysis", {"car_id": car_id, "keyword": keyword})


# ── Tool: market freshness ───────────────────────────────────────────────────

@mcp.tool(
    name="check_market_freshness",
    description="Audit market data freshness. Shows how many prices are stale (>6 months old) and how many cars are missing market data.",
)
def check_market_freshness() -> dict:
    return _tool("check_market_freshness", {})


# ── Tool: refresh market price ───────────────────────────────────────────────

@mcp.tool(
    name="refresh_market_price",
    description="Update market price for a specific car with a new price range. Use when you know current market values from research.",
)
def refresh_market_price(
    car_id: int,
    price_low: float,
    price_high: float,
    source_site: str,
) -> dict:
    return _tool("refresh_market_price", {
        "car_id": car_id,
        "price_low": price_low,
        "price_high": price_high,
        "source_site": source_site,
    })


# ── Tool: enrich car data ────────────────────────────────────────────────────

@mcp.tool(
    name="enrich_car_data",
    description="Fill missing performance data (0-60, weight, fuel economy, cargo) for a car using known specs. Mode: 'auto' for estimates, 'ask_user' to see what's missing.",
)
def enrich_car_data(car_id: int, mode: str = "auto") -> dict:
    return _tool("enrich_car_data", {"car_id": car_id, "mode": mode})


# ── Tool: depreciation projection ────────────────────────────────────────────

@mcp.tool(
    name="get_depreciation_projection",
    description="Project the 20-year depreciation curve for a car, identifying sweet spot, caution, and floor zones. Shows when to buy and projected value.",
)
def get_depreciation_projection(car_id: int, years: int = 20) -> dict:
    return _tool("get_depreciation_projection", {"car_id": car_id, "years": years})


# ── Tool: PPI checklist ──────────────────────────────────────────────────────

@mcp.tool(
    name="get_ppi_checklist",
    description="Generate a pre-purchase inspection checklist from known failure data. Shows severity-ranked failure points, repair costs, and preventive fixes with ROI.",
)
def get_ppi_checklist(car_id: int) -> dict:
    return _tool("get_ppi_checklist", {"car_id": car_id})


# ── Tool: origination story ──────────────────────────────────────────────────

@mcp.tool(
    name="get_origination_story",
    description="Generate a dependent origination story for a car — traces what the car actually IS as an assemblage of shared components, engine lineage, and engineering karma.",
)
def get_origination_story(car_id: int) -> dict:
    return _tool("get_origination_story", {"car_id": car_id})


# ── Tool: save ingest data (stateful — needs ingest session) ────────────────

@mcp.tool(
    name="save_ingest_data",
    description="Save the currently reviewed car data from an ingest session to the permanent collection. Requires an active ingest_session_id.",
)
def save_ingest_data(ingest_session_id: Optional[int] = None) -> dict:
    if not ingest_session_id:
        return {"error": "No ingest_session_id provided. This tool requires an active ingest session."}
    return _tool("save_ingest_data", {}, session_id=ingest_session_id)


# ── Bonus tool: run raw SQL (power users) ────────────────────────────────────

@mcp.tool(
    name="run_sql",
    description="Run a read-only SQL query against the MotorGeek database. Use for custom analysis beyond the built-in tools. Only SELECT queries allowed.",
)
def run_sql(query: str) -> dict:
    import sqlite3
    from pathlib import Path

    q = query.strip()
    if not q.lower().startswith("select"):
        return {"error": "Only SELECT queries are allowed"}

    db_path = Path("data/motorgeek.db")
    if not db_path.exists():
        return {"error": "Database not found"}

    try:
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(q)
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return {"rows": rows, "count": len(rows)}
    except Exception as e:
        return {"error": str(e)}


# ── Entry point ──────────────────────────────────────────────────────────────

def serve():
    """Start the MCP server on stdio (for Claude Desktop / OpenCode)."""
    init_db()
    mcp.run(transport="stdio")


if __name__ == "__main__":
    serve()

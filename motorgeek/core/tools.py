"""Tool definitions and executor for the MotorGeek agent."""

import json
from typing import Optional, Any

from sqlalchemy.orm import Session
from sqlalchemy import func

from motorgeek.core.database import get_session
from motorgeek.core.models import (
    Car,
    Performance,
    PowertrainICE,
    Reliability,
    CostToOwn,
    MarketHistory,
    Dimensions,
)
from motorgeek.core.analysis import calculate_power_to_weight, calculate_hp_per_liter

# ── Tool definitions (JSON schemas for the LLM) ─────────────────────────────

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_collection_overview",
            "description": "Get an overview of the entire car collection: how many cars, era breakdown, horsepower range, country distribution.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_cars",
            "description": "Search the car collection by make, model, generation, or keywords. Returns matching cars with basic info.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search term (make, model, or keyword like 'Porsche' or '90s')",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_car_detail",
            "description": "Get full specifications for a specific car: performance, powertrain, reliability, dimensions, market data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "car_id": {
                        "type": "integer",
                        "description": "The car ID to look up",
                    }
                },
                "required": ["car_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "compare_cars",
            "description": "Compare multiple cars side-by-side. Returns key specs (HP, 0-60, weight, price) for easy comparison.",
            "parameters": {
                "type": "object",
                "properties": {
                    "car_ids": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "List of car IDs to compare (2-6 cars)",
                    }
                },
                "required": ["car_ids"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "suggest_comparisons",
            "description": "Suggest cars in the collection that would be interesting to compare with a given car, based on similar era, power, price, or body style.",
            "parameters": {
                "type": "object",
                "properties": {
                    "car_id": {
                        "type": "integer",
                        "description": "Reference car ID to find comparison candidates for",
                    }
                },
                "required": ["car_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_all_cars",
            "description": "List all cars in the collection with their key stats: ID, name, horsepower, 0-60, weight, price. Use this to find cars to compare.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "save_ingest_data",
            "description": "Save the currently reviewed car data from the ingest session to the permanent collection. Only works during an active ingest session.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
]

# ── Tool executor ────────────────────────────────────────────────────────────


def execute_tool(
    tool_name: str,
    arguments: dict,
    db: Optional[Session] = None,
    ingest_session_id: Optional[int] = None,
) -> dict:
    """Execute a tool by name. Returns a dict with result data."""
    if db is None:
        db = get_session()

    handlers = {
        "get_collection_overview": _handle_overview,
        "search_cars": _handle_search,
        "get_car_detail": _handle_detail,
        "compare_cars": _handle_compare,
        "suggest_comparisons": _handle_suggest,
        "list_all_cars": _handle_list_all,
        "save_ingest_data": _handle_save,
    }

    handler = handlers.get(tool_name)
    if not handler:
        return {"error": f"Unknown tool: {tool_name}"}

    try:
        return handler(db, arguments, ingest_session_id)
    except Exception as e:
        return {"error": str(e)}


def _handle_overview(db: Session, args: dict, _session_id: Optional[int] = None) -> dict:
    cars = db.query(Car).all()
    if not cars:
        return {"count": 0, "message": "No cars in the collection yet."}

    eras = {}
    countries = {}
    bodies = {}
    min_hp = float("inf")
    max_hp = 0
    hp_count = 0

    for car in cars:
        era = car.era_tag or "unknown"
        eras[era] = eras.get(era, 0) + 1
        country = car.country or "unknown"
        countries[country] = countries.get(country, 0) + 1
        body = car.body_style or "unknown"
        bodies[body] = bodies.get(body, 0) + 1

        ice = (
            db.query(PowertrainICE)
            .filter(PowertrainICE.car_id == car.id)
            .first()
        )
        if ice and ice.horsepower_bhp:
            hp_count += 1
            if ice.horsepower_bhp < min_hp:
                min_hp = ice.horsepower_bhp
            if ice.horsepower_bhp > max_hp:
                max_hp = ice.horsepower_bhp

    return {
        "count": len(cars),
        "era_breakdown": eras,
        "country_breakdown": countries,
        "body_breakdown": bodies,
        "horsepower_range": f"{int(min_hp)}-{int(max_hp)} HP" if hp_count > 0 else "N/A",
    }


def _handle_search(db: Session, args: dict, _session_id: Optional[int] = None) -> dict:
    query = args.get("query", "").strip().lower()
    if not query:
        return {"results": [], "message": "Empty search query."}

    all_cars = db.query(Car).all()
    matches = []
    for car in all_cars:
        searchable = f"{car.make} {car.model} {car.generation or ''} {car.era_tag or ''} {car.country or ''} {car.body_style or ''}".lower()
        if query in searchable:
            ice = (
                db.query(PowertrainICE)
                .filter(PowertrainICE.car_id == car.id)
                .first()
            )
            hp = ice.horsepower_bhp if ice else None
            matches.append(
                {
                    "id": car.id,
                    "make": car.make,
                    "model": car.model,
                    "generation": car.generation or "",
                    "year_start": car.year_start,
                    "year_end": car.year_end,
                    "body_style": car.body_style or "",
                    "country": car.country or "",
                    "era_tag": car.era_tag or "",
                    "horsepower": hp,
                }
            )

    return {"results": matches, "count": len(matches)}


def _handle_detail(db: Session, args: dict, _session_id: Optional[int] = None) -> dict:
    car_id = args.get("car_id")
    if not car_id:
        return {"error": "car_id required"}

    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        return {"error": f"Car {car_id} not found"}

    perf = db.query(Performance).filter(Performance.car_id == car_id).first()
    ice = db.query(PowertrainICE).filter(PowertrainICE.car_id == car_id).first()
    rel = db.query(Reliability).filter(Reliability.car_id == car_id).first()
    cost = db.query(CostToOwn).filter(CostToOwn.car_id == car_id).first()
    market = (
        db.query(MarketHistory)
        .filter(MarketHistory.car_id == car_id)
        .order_by(MarketHistory.date_recorded.desc())
        .first()
    )
    dims = db.query(Dimensions).filter(Dimensions.car_id == car_id).first()

    ptw = None
    hpl = None
    if ice and ice.horsepower_bhp and ice.curb_weight_kg:
        ptw = round(ice.horsepower_bhp / (ice.curb_weight_kg / 1000), 1)
    if ice and ice.horsepower_bhp and ice.displacement_cc:
        hpl = round(ice.horsepower_bhp / (ice.displacement_cc / 1000), 1)

    return {
        "id": car.id,
        "make": car.make,
        "model": car.model,
        "generation": car.generation or "",
        "years": f"{car.year_start or '?'}-{car.year_end or 'present'}",
        "body": car.body_style or "",
        "country": car.country or "",
        "era": car.era_tag or "",
        "performance": {
            "accel_0_60": perf.accel_0_60 if perf else None,
            "accel_0_100": perf.accel_0_100 if perf else None,
            "top_speed_mph": perf.top_speed_mph if perf else None,
            "quarter_mile": perf.quarter_mile_time if perf else None,
            "power_to_weight_hp_per_tonne": ptw,
        }
        if perf or ptw
        else None,
        "powertrain": {
            "engine": f"{ice.engine_layout or ''} {ice.aspiration or ''}".strip() if ice else None,
            "displacement_cc": ice.displacement_cc if ice else None,
            "cylinders": ice.cylinders if ice else None,
            "horsepower_bhp": ice.horsepower_bhp if ice else None,
            "torque_nm": ice.torque_nm if ice else None,
            "transmission": ice.transmission_type if ice else None,
            "drivetrain": ice.drivetrain if ice else None,
            "curb_weight_kg": ice.curb_weight_kg if ice else None,
            "hp_per_liter": hpl,
        }
        if ice
        else None,
        "reliability": {
            "score": rel.reliability_score if rel else None,
            "common_failures": rel.common_failures if rel else None,
        }
        if rel
        else None,
        "cost": {
            "msrp_original": cost.msrp_original if cost else None,
            "msrp_currency": cost.msrp_currency if cost else None,
            "depreciation_5yr_pct": cost.depreciation_5yr_pct if cost else None,
        }
        if cost
        else None,
        "market": {
            "price_low": market.price_low if market else None,
            "price_high": market.price_high if market else None,
            "trend": market.market_trend_indicator if market else None,
            "source": market.source_site if market else None,
        }
        if market
        else None,
        "dimensions": {
            "length_mm": dims.length_mm if dims else None,
            "width_mm": dims.width_mm if dims else None,
            "height_mm": dims.height_mm if dims else None,
            "wheelbase_mm": dims.wheelbase_mm if dims else None,
        }
        if dims
        else None,
    }


def _handle_compare(db: Session, args: dict, _session_id: Optional[int] = None) -> dict:
    car_ids = args.get("car_ids", [])
    if not car_ids or len(car_ids) < 2:
        return {"error": "Need at least 2 car IDs to compare"}

    cars = db.query(Car).filter(Car.id.in_(car_ids)).all()
    if len(cars) < 2:
        return {"error": f"Found only {len(cars)} of the requested cars"}

    result = {"cars": []}
    for car in cars:
        ice = db.query(PowertrainICE).filter(PowertrainICE.car_id == car.id).first()
        perf = db.query(Performance).filter(Performance.car_id == car.id).first()
        market = (
            db.query(MarketHistory)
            .filter(MarketHistory.car_id == car.id)
            .order_by(MarketHistory.date_recorded.desc())
            .first()
        )
        ptw = None
        if ice and ice.horsepower_bhp and ice.curb_weight_kg:
            ptw = round(ice.horsepower_bhp / (ice.curb_weight_kg / 1000), 1)

        result["cars"].append(
            {
                "id": car.id,
                "name": f"{car.make} {car.model} ({car.generation or 'base'})",
                "year": car.year_start,
                "horsepower": ice.horsepower_bhp if ice else None,
                "torque_nm": ice.torque_nm if ice else None,
                "accel_0_60": perf.accel_0_60 if perf else None,
                "curb_weight_kg": ice.curb_weight_kg if ice else None,
                "power_to_weight": ptw,
                "market_price": (
                    f"${market.price_low:,.0f} - ${market.price_high:,.0f}" if market and market.price_low else None
                ),
            }
        )

    return result


def _handle_list_all(db: Session, args: dict, _session_id: Optional[int] = None) -> dict:
    """List all cars with key stats for quick comparison."""
    cars = db.query(Car).all()
    result = []
    for car in cars:
        ice = db.query(PowertrainICE).filter(PowertrainICE.car_id == car.id).first()
        perf = db.query(Performance).filter(Performance.car_id == car.id).first()
        market = (
            db.query(MarketHistory)
            .filter(MarketHistory.car_id == car.id)
            .order_by(MarketHistory.date_recorded.desc())
            .first()
        )
        ptw = None
        if ice and ice.horsepower_bhp and ice.curb_weight_kg:
            ptw = round(ice.horsepower_bhp / (ice.curb_weight_kg / 1000), 1)

        result.append({
            "id": car.id,
            "name": f"{car.make} {car.model} ({car.generation or 'base'})",
            "year": f"{car.year_start or '?'}-{car.year_end or '?'}",
            "era": car.era_tag or "",
            "body": car.body_style or "",
            "horsepower": ice.horsepower_bhp if ice else None,
            "torque_nm": ice.torque_nm if ice else None,
            "accel_0_60": perf.accel_0_60 if perf else None,
            "curb_weight_kg": ice.curb_weight_kg if ice else None,
            "power_to_weight": ptw,
            "market_price": f"${market.price_low:,.0f} - ${market.price_high:,.0f}" if market and market.price_low else None,
        })

    # Sort by power-to-weight descending (fastest first)
    result.sort(key=lambda x: x["power_to_weight"] or 0, reverse=True)
    return {"cars": result, "count": len(result)}


def _handle_suggest(db: Session, args: dict, _session_id: Optional[int] = None) -> dict:
    car_id = args.get("car_id")
    if not car_id:
        return {"error": "car_id required"}

    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        return {"error": f"Car {car_id} not found"}

    ice = db.query(PowertrainICE).filter(PowertrainICE.car_id == car_id).first()
    target_hp = ice.horsepower_bhp if ice else None
    target_era = car.era_tag
    target_body = car.body_style

    all_cars = db.query(Car).filter(Car.id != car_id).all()
    suggestions = []
    for other in all_cars:
        score = 0
        other_ice = (
            db.query(PowertrainICE)
            .filter(PowertrainICE.car_id == other.id)
            .first()
        )
        other_hp = other_ice.horsepower_bhp if other_ice else None

        if target_era and other.era_tag == target_era:
            score += 3
        if target_body and other.body_style == target_body:
            score += 2
        if target_hp and other_hp:
            hp_diff = abs(target_hp - other_hp) / max(target_hp, 1) * 100
            if hp_diff < 10:
                score += 4
            elif hp_diff < 25:
                score += 2
            elif hp_diff < 50:
                score += 1

        if score > 0:
            suggestions.append(
                {
                    "id": other.id,
                    "name": f"{other.make} {other.model} ({other.generation or 'base'})",
                    "reason": _reason(target_era, target_body, target_hp, other),
                    "score": score,
                }
            )

    suggestions.sort(key=lambda x: x["score"], reverse=True)
    return {"reference_car": f"{car.make} {car.model}", "suggestions": suggestions[:5]}


def _reason(target_era, target_body, target_hp, other):
    parts = []
    if target_era and other.era_tag == target_era:
        parts.append(f"same era ({target_era})")
    if target_body and other.body_style == target_body:
        parts.append(f"same body ({target_body})")
    if target_hp:
        other_ice = (
            get_session()
            .query(PowertrainICE)
            .filter(PowertrainICE.car_id == other.id)
            .first()
        )
        if other_ice and other_ice.horsepower_bhp:
            diff = abs(target_hp - other_ice.horsepower_bhp)
            parts.append(f"within {int(diff)} HP")
    return ", ".join(parts) if parts else "general interest"


def _handle_save(db: Session, args: dict, session_id: Optional[int] = None) -> dict:
    if not session_id:
        return {"error": "No active ingest session. You can only save during an ingest review."}

    from motorgeek.core.ingest import save_session, get_session_by_id

    session_obj = get_session_by_id(db, session_id)
    if not session_obj:
        return {"error": f"Ingest session {session_id} not found"}
    if session_obj.status != "enriched":
        return {
            "error": f"Ingest session is not ready to save (status: {session_obj.status}). Answer the agent's questions first."
        }

    try:
        car_id = save_session(db, session_id)
        car = db.query(Car).filter(Car.id == car_id).first()
        return {
            "success": True,
            "car_id": car_id,
            "message": f"Saved {car.make} {car.model} to your collection!",
        }
    except Exception as e:
        return {"error": f"Save failed: {e}"}

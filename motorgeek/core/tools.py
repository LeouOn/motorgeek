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
    RepairCatalog,
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
            "name": "compare_family",
            "description": "Compare all variants/generations within a car family (e.g., '911', 'M3', 'Supra'). Shows side-by-side specs across generations and trims. Use this when the user wants to see how a model evolved.",
            "parameters": {
                "type": "object",
                "properties": {
                    "family": {
                        "type": "string",
                        "description": "Car family name: '911', 'M3', 'Supra', 'Golf GTI', 'Mustang', etc.",
                    }
                },
                "required": ["family"],
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
    {
        "type": "function",
        "function": {
            "name": "get_qualitative_analysis",
            "description": "Retrieve stored qualitative analysis, platform comparisons, reliability assessments, and recommendations. Use this to access expert analysis from Perplexity comparisons. Search by car_id or keyword (e.g., 'platform', 'reliability', 'aging').",
            "parameters": {
                "type": "object",
                "properties": {
                    "car_id": {
                        "type": "integer",
                        "description": "Optional: car ID to get analysis for",
                    },
                    "keyword": {
                        "type": "string",
                        "description": "Optional: search term like 'platform', 'reliability', 'M276', 'Alpha II'",
                    },
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_market_freshness",
            "description": "Audit market data freshness. Shows how many prices are stale (>6 months old), how many cars are missing market data entirely. Use this to warn users when recommendations are based on old data.",
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
            "name": "enrich_car_data",
            "description": "Fill missing performance data (0-60, weight, fuel economy, cargo) for a car using known specs. The system will estimate values from horsepower, displacement, drivetrain, and body style. Use this when a car is missing key comparison data. Can also suggest what data to ask the user for ('go fish' mode).",
            "parameters": {
                "type": "object",
                "properties": {
                    "car_id": {
                        "type": "integer",
                        "description": "Car ID to enrich",
                    },
                    "mode": {
                        "type": "string",
                        "enum": ["auto", "ask_user"],
                        "description": "auto: fill using estimates. ask_user: return what data is missing and ask the user to provide it.",
                    },
                },
                "required": ["car_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "refresh_market_price",
            "description": "Update market price for a specific car with a new price range. Use when you know current market values from research. Always note the source (KBB, Hagerty, BaT, etc).",
            "parameters": {
                "type": "object",
                "properties": {
                    "car_id": {
                        "type": "integer",
                        "description": "Car ID to update",
                    },
                    "price_low": {
                        "type": "number",
                        "description": "Low end of current price range",
                    },
                    "price_high": {
                        "type": "number",
                        "description": "High end of current price range",
                    },
                    "source_site": {
                        "type": "string",
                        "description": "Source: KBB, Hagerty, BaT, Cars&Bids, etc.",
                    },
                },
                "required": ["car_id", "price_low", "price_high", "source_site"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_depreciation_projection",
            "description": "Project the 20-year depreciation curve for a car, identifying sweet spot, caution, and floor zones. Shows when to buy and projected value at each age.",
            "parameters": {
                "type": "object",
                "properties": {
                    "car_id": {"type": "integer", "description": "Car ID to project"},
                    "years": {"type": "integer", "description": "Number of years to project (default 20)"},
                },
                "required": ["car_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_ppi_checklist",
            "description": "Generate a pre-purchase inspection checklist from known failure data. Shows severity-ranked failure points, repair costs, and preventive fixes with ROI.",
            "parameters": {
                "type": "object",
                "properties": {
                    "car_id": {"type": "integer", "description": "Car ID to generate checklist for"},
                },
                "required": ["car_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_origination_story",
            "description": "Generate a dependent origination story for a car — traces what the car actually IS as an assemblage of shared components, engine lineage, family history, and engineering karma.",
            "parameters": {
                "type": "object",
                "properties": {
                    "car_id": {"type": "integer", "description": "Car ID to trace"},
                },
                "required": ["car_id"],
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
        "compare_family": _handle_compare_family,
        "get_qualitative_analysis": _handle_qualitative,
        "check_market_freshness": _handle_market_freshness,
        "refresh_market_price": _handle_refresh_price,
        "enrich_car_data": _handle_enrich,
        "save_ingest_data": _handle_save,
        "get_depreciation_projection": _handle_depreciation,
        "get_ppi_checklist": _handle_ppi,
        "get_origination_story": _handle_origination,
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
            "fuel_consumption_l_100km": ice.fuel_consumption_mixed_l_100km if ice else None,
            "cargo_volume_liters": ice.cargo_volume_liters if ice else None,
            "fuel_econ_city_mpg": cost.fuel_econ_city_mpg if cost else None,
            "fuel_econ_hwy_mpg": cost.fuel_econ_hwy_mpg if cost else None,
        }
        if ice
        else None,
        "reliability": {
            "score": rel.reliability_score if rel else None,
            "common_failures": rel.common_failures if rel else None,
            "dimensions": {
                "engine": rel.score_engine if rel else None,
                "transmission": rel.score_transmission if rel else None,
                "chassis": rel.score_chassis if rel else None,
                "electronics": rel.score_electronics if rel else None,
                "ease_of_repair": rel.score_ease_of_repair if rel else None,
            } if rel else None,
            "dimension_notes": rel.score_notes if rel else None,
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
        "repairs": [
            {
                "name": r.repair_name,
                "category": r.repair_category,
                "cost_low": r.avg_cost_low,
                "cost_high": r.avg_cost_high,
                "frequency": r.frequency,
                "mileage": r.typical_mileage_range,
                "severity": r.severity,
                "notes": r.notes,
            }
            for r in (db.query(RepairCatalog).filter(RepairCatalog.car_id == car_id).all() or [])
        ]
        if db.query(RepairCatalog).filter(RepairCatalog.car_id == car_id).count() > 0
        else [],
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


def _handle_compare_family(db: Session, args: dict, _session_id: Optional[int] = None) -> dict:
    """Compare all variants within a car family."""
    family = args.get("family", "").strip()
    if not family:
        return {"error": "Family name required, e.g. '911', 'M3', 'Supra'"}

    cars = db.query(Car).filter(Car.family == family).all()
    if not cars:
        # Try case-insensitive search
        cars = db.query(Car).filter(Car.family.ilike(f"%{family}%")).all()
    if not cars:
        return {"error": f"No cars found in family '{family}'. Available families: 911, M3, Supra, S-Class, G90, Taycan, Mustang, Golf GTI, 3 Series, MX-5, A110, Yaris, 944, S2000, F355"}

    result = {"family": family, "variants": [], "count": len(cars)}
    for car in cars:
        ice = db.query(PowertrainICE).filter(PowertrainICE.car_id == car.id).first()
        perf = db.query(Performance).filter(Performance.car_id == car.id).first()
        ptw = None
        if ice and ice.horsepower_bhp and ice.curb_weight_kg:
            ptw = round(ice.horsepower_bhp / (ice.curb_weight_kg / 1000), 1)

        result["variants"].append({
            "id": car.id,
            "name": f"{car.make} {car.model}",
            "generation": car.generation or "",
            "variant": car.variant or "",
            "years": f"{car.year_start or '?'}-{car.year_end or '?'}",
            "horsepower": ice.horsepower_bhp if ice else None,
            "torque_nm": ice.torque_nm if ice else None,
            "accel_0_60": perf.accel_0_60 if perf else None,
            "curb_weight_kg": ice.curb_weight_kg if ice else None,
            "power_to_weight": ptw,
            "displacement_cc": ice.displacement_cc if ice else None,
            "aspiration": ice.aspiration if ice else None,
            "drivetrain": ice.drivetrain if ice else None,
        })

    # Sort by year
    result["variants"].sort(key=lambda x: x["years"])
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


def _handle_qualitative(db: Session, args: dict, _session_id: Optional[int] = None) -> dict:
    """Handle get_qualitative_analysis tool."""
    from motorgeek.core.agent import get_qualitative_analysis
    car_id = args.get("car_id")
    keyword = args.get("keyword")
    return get_qualitative_analysis(db, car_id=car_id, keyword=keyword)


def _handle_market_freshness(db: Session, args: dict, _session_id: Optional[int] = None) -> dict:
    """Handle check_market_freshness tool."""
    from motorgeek.core.agent import check_market_freshness
    return check_market_freshness(db)


def _handle_refresh_price(db: Session, args: dict, _session_id: Optional[int] = None) -> dict:
    """Handle refresh_market_price tool."""
    from motorgeek.core.models import MarketHistory, Car
    from datetime import date

    car_id = args.get("car_id")
    price_low = args.get("price_low")
    price_high = args.get("price_high")
    source_site = args.get("source_site", "manual")

    if not car_id or not price_low or not price_high:
        return {"error": "car_id, price_low, and price_high are required"}

    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        return {"error": f"Car {car_id} not found"}

    # Update existing or create new
    existing = db.query(MarketHistory).filter(
        MarketHistory.car_id == car_id,
        MarketHistory.source_site == source_site,
    ).first()

    if existing:
        existing.price_low = float(price_low)
        existing.price_high = float(price_high)
        existing.date_recorded = date.today()
    else:
        mh = MarketHistory(
            car_id=car_id,
            date_recorded=date.today(),
            price_low=float(price_low),
            price_high=float(price_high),
            source_site=source_site,
            currency="USD",
            market_trend_indicator="updated",
        )
        db.add(mh)

    db.commit()
    return {
        "success": True,
        "car_id": car_id,
        "car": f"{car.make} {car.model}",
        "price_low": price_low,
        "price_high": price_high,
        "source": source_site,
        "message": f"Updated {car.make} {car.model} market price to ${price_low:,}-${price_high:,} ({source_site})",
    }


def _handle_enrich(db: Session, args: dict, _session_id: Optional[int] = None) -> dict:
    """Handle enrich_car_data tool — fill missing performance data."""
    car_id = args.get("car_id")
    mode = args.get("mode", "auto")

    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        return {"error": f"Car {car_id} not found"}

    ice = db.query(PowertrainICE).filter(PowertrainICE.car_id == car_id).first()
    perf = db.query(Performance).filter(Performance.car_id == car_id).first()
    cost = db.query(CostToOwn).filter(CostToOwn.car_id == car_id).first()

    hp = ice.horsepower_bhp if ice else None
    wt = ice.curb_weight_kg if ice else None
    disp = ice.displacement_cc if ice else None
    drv = ice.drivetrain if ice else ""
    body = car.body_style or "sedan"

    # What's missing?
    missing = []
    if not wt: missing.append("curb_weight_kg")
    if not (perf and perf.accel_0_60): missing.append("0-60 time")
    if not (ice and ice.fuel_consumption_mixed_l_100km): missing.append("fuel consumption")
    if not (ice and ice.cargo_volume_liters): missing.append("cargo volume")
    if not (perf and perf.top_speed_mph): missing.append("top speed")

    if mode == "ask_user":
        return {
            "car": f"{car.make} {car.model} ({car.generation or 'base'})",
            "known": {"horsepower": hp, "weight_kg": wt, "displacement_cc": disp, "drivetrain": drv, "body": body},
            "missing_fields": missing,
            "prompt": f"Please provide: {', '.join(missing)} for the {car.make} {car.model}. You can paste specs from auto-data.net, ZePerfs, or Wikipedia.",
        }

    # Auto mode: estimate missing values
    enriched = {}
    estimated_fields = []

    # Estimate weight from body style + displacement
    if not wt and hp:
        base = {"sedan": 1550, "coupe": 1500, "suv": 2000, "roadster": 1200, "hatchback": 1400}.get(body, 1600)
        wt = base + (disp or 3000) * 0.15
        estimated_fields.append(f"curb_weight_kg ≈ {wt:.0f} kg")
        if ice:
            ice.curb_weight_kg = wt
            db.add(ice)
            enriched["curb_weight_kg"] = round(wt)

    # Estimate 0-60 from power-to-weight
    if wt and hp and not (perf and perf.accel_0_60):
        ptw = hp / (wt / 1000)
        if ptw > 300: est_060 = 3.0
        elif ptw > 200: est_060 = 4.0 + (300 - ptw) * 0.01
        elif ptw > 150: est_060 = 5.0 + (200 - ptw) * 0.015
        elif ptw > 100: est_060 = 6.5 + (150 - ptw) * 0.02
        else: est_060 = 8.0
        est_060 = round(est_060, 1)
        estimated_fields.append(f"0-60 ≈ {est_060}s")
        if not perf:
            perf = Performance(car_id=car_id, accel_0_60=est_060, source="estimated")
            db.add(perf)
        else:
            perf.accel_0_60 = est_060
            perf.source = (perf.source or "") + " (estimated)"
        enriched["accel_0_60"] = est_060

    # Estimate fuel consumption
    if hp and not (ice and ice.fuel_consumption_mixed_l_100km):
        if "electric" in (ice.engine_layout or "").lower() or "ev" in (car.character or ""):
            est_fuel = 0
        elif hp > 500: est_fuel = 14
        elif hp > 350: est_fuel = 10 + (hp - 350) * 0.02
        elif hp > 200: est_fuel = 7 + (hp - 200) * 0.015
        else: est_fuel = 5 + hp * 0.01
        est_fuel = round(est_fuel, 1)
        estimated_fields.append(f"fuel ≈ {est_fuel} L/100km")
        if ice:
            ice.fuel_consumption_mixed_l_100km = est_fuel
            db.add(ice)
        enriched["fuel_consumption_l_100km"] = est_fuel

    # Estimate cargo
    if body and not (ice and ice.cargo_volume_liters):
        cargo_map = {"suv": 800, "hatchback": 400, "sedan": 480, "coupe": 300, "roadster": 150, "wagon": 600}
        est_cargo = cargo_map.get(body, 400)
        estimated_fields.append(f"cargo ≈ {est_cargo}L")
        if ice:
            ice.cargo_volume_liters = est_cargo
            db.add(ice)
        enriched["cargo_volume_liters"] = est_cargo

    if estimated_fields:
        db.commit()

    return {
        "car": f"{car.make} {car.model} ({car.generation or 'base'})",
        "known": {"horsepower": hp, "weight_kg": wt, "drivetrain": drv, "body": body},
        "missing_before": missing,
        "estimated": estimated_fields,
        "enriched_fields": enriched,
        "note": "Values are ESTIMATES based on HP, weight, and body style. For accuracy, provide real specs.",
    }


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


def _handle_depreciation(db: Session, args: dict, _session_id: Optional[int] = None) -> dict:
    """Project depreciation curve and buying window for a car."""
    import subprocess, json as _json
    car_id = args.get("car_id")
    if not car_id:
        return {"error": "car_id required"}

    try:
        result = subprocess.run(
            ["python", "scripts/depreciation_projection.py", str(car_id)],
            capture_output=True, text=True, timeout=30,
            cwd=str(Path(__file__).parent.parent.parent),
        )
        return {"output": result.stdout, "car_id": car_id}
    except Exception as e:
        return {"error": str(e)}


def _handle_ppi(db: Session, args: dict, _session_id: Optional[int] = None) -> dict:
    """Generate PPI checklist from failure_points data."""
    car_id = args.get("car_id")
    if not car_id:
        return {"error": "car_id required"}

    from motorgeek.core.models import Car
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        return {"error": f"Car {car_id} not found"}

    # Query failure_points directly
    from sqlalchemy import text
    failures = db.execute(text(
        "SELECT * FROM failure_points WHERE car_id = :cid ORDER BY severity DESC"
    ), {"cid": car_id}).fetchall()

    if not failures:
        return {"car": f"{car.make} {car.model}", "message": "No structured failure data yet."}

    result = []
    for f in failures:
        sev_labels = ['', 'cosmetic', 'nuisance', 'moderate', 'major', 'catastrophic']
        result.append({
            "name": f[1].replace('_', ' '),  # failure_name
            "component": f[3],  # component
            "severity": sev_labels[f[4]],  # severity
            "severity_num": f[4],
            "mileage": f[5],
            "cost_low": f[6],
            "cost_high": f[7],
            "preventive": bool(f[8]),
            "prevention_cost": f[9],
            "description": f[11],
        })

    preventive = [r for r in result if r["preventive"]]
    total_prev = sum(r["prevention_cost"] or 0 for r in preventive)
    total_risk = sum(r["cost_high"] or 0 for r in result if r["severity_num"] >= 4)

    return {
        "car": f"{car.make} {car.model} {car.variant or ''}",
        "failures": result,
        "summary": {
            "total_failures": len(result),
            "major_risks": len([r for r in result if r["severity_num"] >= 4]),
            "preventive_fixes": len(preventive),
            "total_prevention_cost": total_prev,
            "total_risk_mitigated": total_risk,
            "blended_roi": round(total_risk / total_prev, 1) if total_prev > 0 else 0,
        },
    }


def _handle_origination(db: Session, args: dict, _session_id: Optional[int] = None) -> dict:
    """Generate dependent origination story — what the car actually IS as an assemblage."""
    import subprocess
    car_id = args.get("car_id")
    if not car_id:
        return {"error": "car_id required"}

    try:
        result = subprocess.run(
            ["python", "scripts/origination_story.py", str(car_id)],
            capture_output=True, text=True, timeout=30,
            cwd=str(Path(__file__).parent.parent.parent),
        )
        return {"story": result.stdout, "car_id": car_id}
    except Exception as e:
        return {"error": str(e)}

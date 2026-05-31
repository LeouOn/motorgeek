"""Agent dashboard route."""

from fastapi import Request
from fastapi.responses import HTMLResponse

from motorgeek.core.database import get_session
from motorgeek.core.models import Car, AgentToolCallLog, PowertrainICE
from motorgeek.web.app import templates
from sqlalchemy import func


async def agent_dashboard(request: Request) -> HTMLResponse:
    """GET /agent — unified agent dashboard with stats, ingest, and chat."""
    db = get_session()

    # Stats
    car_count = db.query(func.count(Car.id)).scalar()
    hp_results = (
        db.query(
            func.min(PowertrainICE.horsepower_bhp),
            func.max(PowertrainICE.horsepower_bhp),
        )
        .filter(PowertrainICE.horsepower_bhp.isnot(None))
        .first()
    )
    hp_range = f"{int(hp_results[0] or 0)}–{int(hp_results[1] or 0)}" if hp_results else "N/A"

    era_count = db.query(func.count(func.distinct(Car.era_tag))).scalar() or 0
    tool_calls = db.query(func.count(AgentToolCallLog.id)).scalar()

    # Top suggestions: cars with highest power-to-weight
    cars = db.query(Car).all()
    suggestions = []
    for car in cars:
        ice = (
            db.query(PowertrainICE)
            .filter(PowertrainICE.car_id == car.id)
            .first()
        )
        if ice and ice.horsepower_bhp and ice.curb_weight_kg:
            ptw = ice.horsepower_bhp / (ice.curb_weight_kg / 1000)
            suggestions.append({"name": f"{car.make} {car.model}", "score": ptw})
    suggestions.sort(key=lambda x: x["score"], reverse=True)
    suggestions = suggestions[:6]

    # Show conversation history
    conversation = request.session.get("conversation", [])

    return templates.TemplateResponse(request, "agent.html", {
        "stats": {
            "car_count": car_count,
            "hp_range": hp_range,
            "era_count": era_count,
            "tool_calls": tool_calls,
        },
        "suggestions": suggestions,
        "conversation": conversation,
    })

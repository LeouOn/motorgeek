"""Performance brackets explorer route."""

from fastapi import Request
from fastapi.responses import HTMLResponse
from motorgeek.core.database import get_session
from motorgeek.core.models import Car, PowertrainICE, Performance
from motorgeek.web.app import templates


async def brackets_page(request: Request) -> HTMLResponse:
    """GET /brackets — visual performance bracket explorer."""
    db = get_session()
    cars = db.query(Car).all()

    brackets = [
        {"label": "Hypercar (300+ HP/t)", "emoji": "🔥", "min": 300, "max": 9999, "cars": []},
        {"label": "Hot (200–300 HP/t)", "emoji": "⚡", "min": 200, "max": 300, "cars": []},
        {"label": "Warm (150–200 HP/t)", "emoji": "🟡", "min": 150, "max": 200, "cars": []},
        {"label": "Eco (100–150 HP/t)", "emoji": "🍃", "min": 100, "max": 150, "cars": []},
        {"label": "Cruiser (<100 HP/t)", "emoji": "🚢", "min": 0, "max": 100, "cars": []},
    ]

    for car in cars:
        ice = db.query(PowertrainICE).filter(PowertrainICE.car_id == car.id).first()
        perf = db.query(Performance).filter(Performance.car_id == car.id).first()
        if ice and ice.horsepower_bhp and ice.curb_weight_kg:
            ptw = round(ice.horsepower_bhp / (ice.curb_weight_kg / 1000), 1)
            car._ptw = ptw
            car._hp = int(ice.horsepower_bhp)
            car._weight = int(ice.curb_weight_kg)
            car._accel = perf.accel_0_60 if perf else None

            for bracket in brackets:
                if bracket["min"] <= ptw < bracket["max"]:
                    bracket["cars"].append(car)
                    break

    # Sort each bracket by P/W descending
    for bracket in brackets:
        bracket["cars"].sort(key=lambda c: c._ptw, reverse=True)

    # Remove empty brackets
    brackets = [b for b in brackets if b["cars"]]

    return templates.TemplateResponse(request, "brackets.html", {"brackets": brackets})

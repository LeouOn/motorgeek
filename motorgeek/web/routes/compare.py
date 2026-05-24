# motorgeek/web/routes/compare.py
from fastapi import Request, Form
from fastapi.responses import HTMLResponse
from motorgeek.core.database import get_session
from motorgeek.core.models import Car, Performance, PowertrainICE, Reliability, CostToOwn
from motorgeek.web.app import templates
from motorgeek.web.charts import build_radar_data


def index(request: Request) -> HTMLResponse:
    session = get_session()
    cars = session.query(Car).all()
    return templates.TemplateResponse("compare/index.html", {"request": request, "cars": cars, "selected": []})


def compare_post(request: Request, car_ids: str = Form(...)) -> HTMLResponse:
    session = get_session()
    ids = [int(x.strip()) for x in car_ids.split(",") if x.strip().isdigit()]
    selected = session.query(Car).filter(Car.id.in_(ids)).all() if ids else []
    perf_data = {c.id: session.query(Performance).filter(Performance.car_id == c.id).first() for c in selected}
    rel_data = {c.id: session.query(Reliability).filter(Reliability.car_id == c.id).first() for c in selected}
    cost_data = {c.id: session.query(CostToOwn).filter(CostToOwn.car_id == c.id).first() for c in selected}
    radar = build_radar_data(selected, perf_data, rel_data, cost_data) if selected else {"labels": [], "datasets": []}
    all_cars = session.query(Car).all()
    return templates.TemplateResponse("compare/index.html", {
        "request": request, "cars": all_cars, "selected": selected, "radar": radar,
    })
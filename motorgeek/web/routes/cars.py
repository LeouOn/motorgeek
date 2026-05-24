# motorgeek/web/routes/cars.py
from fastapi import Request
from fastapi.responses import HTMLResponse
from motorgeek.core.database import get_session
from motorgeek.core.models import Car, Performance, PowertrainICE, MarketHistory
from motorgeek.web.app import templates


def list_cars(request: Request) -> HTMLResponse:
    session = get_session()
    cars = session.query(Car).all()
    return templates.TemplateResponse("cars/list.html", {"request": request, "cars": cars})


def detail_car(car_id: int, request: Request) -> HTMLResponse:
    session = get_session()
    car = session.query(Car).filter(Car.id == car_id).first()
    if not car:
        return HTMLResponse("Car not found", status_code=404)
    perf = session.query(Performance).filter(Performance.car_id == car.id).first()
    ice = session.query(PowertrainICE).filter(PowertrainICE.car_id == car.id).first()
    latest_market = (
        session.query(MarketHistory)
        .filter(MarketHistory.car_id == car.id)
        .order_by(MarketHistory.date_recorded.desc())
        .first()
    )
    return templates.TemplateResponse("cars/detail.html", {
        "request": request, "car": car, "perf": perf, "ice": ice, "market": latest_market,
    })
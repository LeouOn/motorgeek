# motorgeek/web/routes/cars.py
from fastapi import Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse

from motorgeek.core.database import get_session
from motorgeek.core.models import Car, Performance, PowertrainICE, MarketHistory, Reliability
from motorgeek.core.analysis import calculate_power_to_weight, calculate_hp_per_liter
from motorgeek.web.app import templates


def list_cars(request: Request) -> HTMLResponse:
    session = get_session()
    cars = session.query(Car).all()

    # Enrich cars with computed fields for the template
    for car in cars:
        ice = session.query(PowertrainICE).filter(PowertrainICE.car_id == car.id).first()
        perf = session.query(Performance).filter(Performance.car_id == car.id).first()
        car._hp = ice.horsepower_bhp if ice else None
        car._accel = perf.accel_0_60 if perf else None
        car._weight = ice.curb_weight_kg if ice else None

    # Collect filter options
    eras = sorted(set(c.era_tag for c in cars if c.era_tag))
    countries = sorted(set(c.country for c in cars if c.country))
    bodies = sorted(set(c.body_style for c in cars if c.body_style))
    characters = sorted(set(c.character for c in cars if c.character))

    return templates.TemplateResponse(request, "cars/list.html", {
        "cars": cars,
        "stats": {"car_count": len(cars)},
        "eras": eras,
        "countries": countries,
        "bodies": bodies,
        "characters": characters,
    })


def detail_car(car_id: int, request: Request) -> HTMLResponse:
    session = get_session()
    car = session.query(Car).filter(Car.id == car_id).first()
    if not car:
        return HTMLResponse("Car not found", status_code=404)
    perf = session.query(Performance).filter(Performance.car_id == car.id).first()
    ice = session.query(PowertrainICE).filter(PowertrainICE.car_id == car.id).first()
    rel = session.query(Reliability).filter(Reliability.car_id == car.id).first()
    market = (
        session.query(MarketHistory)
        .filter(MarketHistory.car_id == car.id)
        .order_by(MarketHistory.date_recorded.desc())
        .first()
    )
    market_all = session.query(MarketHistory).filter(MarketHistory.car_id == car.id).order_by(MarketHistory.date_recorded.asc()).all() if market else []

    ptw = calculate_power_to_weight(ice.horsepower_bhp, ice.curb_weight_kg) if ice and ice.horsepower_bhp and ice.curb_weight_kg else None
    hpl = calculate_hp_per_liter(ice.horsepower_bhp, ice.displacement_cc) if ice and ice.horsepower_bhp and ice.displacement_cc else None

    return templates.TemplateResponse(request, "cars/detail.html", {
        "car": car, "perf": perf, "ice": ice, "rel": rel, "market": market, "market_all": market_all,
        "ptw": ptw, "hpl": hpl,
    })


def edit_car_get(car_id: int, request: Request) -> HTMLResponse:
    session = get_session()
    car = session.query(Car).filter(Car.id == car_id).first()
    if not car:
        return HTMLResponse("Car not found", status_code=404)
    perf = session.query(Performance).filter(Performance.car_id == car.id).first()
    ice = session.query(PowertrainICE).filter(PowertrainICE.car_id == car.id).first()
    rel = session.query(Reliability).filter(Reliability.car_id == car.id).first()
    return templates.TemplateResponse(request, "cars/edit.html", {
        "car": car, "perf": perf, "ice": ice, "rel": rel,
    })


def edit_car_post(
    car_id: int,
    request: Request,
    make: str = Form(""),
    model: str = Form(""),
    generation: str = Form(""),
    year_start: str = Form(""),
    year_end: str = Form(""),
    body_style: str = Form(""),
    country: str = Form(""),
    era_tag: str = Form(""),
    accel_0_60: str = Form(""),
    accel_0_100: str = Form(""),
    top_speed_mph: str = Form(""),
    lateral_g: str = Form(""),
    horsepower_bhp: str = Form(""),
    torque_nm: str = Form(""),
    displacement_cc: str = Form(""),
    redline_rpm: str = Form(""),
    curb_weight_kg: str = Form(""),
    reliability_score: str = Form(""),
    score_engine: str = Form(""),
    score_transmission: str = Form(""),
    score_chassis: str = Form(""),
    score_electronics: str = Form(""),
    score_ease_of_repair: str = Form(""),
) -> HTMLResponse:
    session = get_session()
    car = session.query(Car).filter(Car.id == car_id).first()
    if not car:
        return HTMLResponse("Car not found", status_code=404)

    error = None
    if year_start:
        try:
            car.year_start = int(year_start)
        except ValueError:
            error = "year_start must be an integer"
    if year_end:
        try:
            car.year_end = int(year_end)
        except ValueError:
            error = "year_end must be an integer"

    if error:
        perf = session.query(Performance).filter(Performance.car_id == car.id).first()
        ice = session.query(PowertrainICE).filter(PowertrainICE.car_id == car.id).first()
        rel = session.query(Reliability).filter(Reliability.car_id == car.id).first()
        return templates.TemplateResponse(request, "cars/edit.html", {
            "car": car, "perf": perf, "ice": ice, "rel": rel, "error": error,
        })

    if make:
        car.make = make
    if model:
        car.model = model
    if generation:
        car.generation = generation
    if year_start:
        car.year_start = int(year_start)
    if year_end:
        car.year_end = int(year_end)
    if body_style:
        car.body_style = body_style
    if country:
        car.country = country
    if era_tag:
        car.era_tag = era_tag

    perf = session.query(Performance).filter(Performance.car_id == car.id).first()
    if perf:
        if accel_0_60:
            perf.accel_0_60 = float(accel_0_60)
        if accel_0_100:
            perf.accel_0_100 = float(accel_0_100)
        if top_speed_mph:
            perf.top_speed_mph = float(top_speed_mph)
        if lateral_g:
            perf.lateral_g = float(lateral_g)

    ice = session.query(PowertrainICE).filter(PowertrainICE.car_id == car.id).first()
    if ice:
        if horsepower_bhp:
            ice.horsepower_bhp = float(horsepower_bhp)
        if torque_nm:
            ice.torque_nm = float(torque_nm)
        if displacement_cc:
            ice.displacement_cc = float(displacement_cc)
        if redline_rpm:
            ice.redline_rpm = int(redline_rpm)
        if curb_weight_kg:
            ice.curb_weight_kg = float(curb_weight_kg)

    rel = session.query(Reliability).filter(Reliability.car_id == car.id).first()
    if rel:
        if reliability_score:
            rel.reliability_score = float(reliability_score)
        for dim_field in ['score_engine', 'score_transmission', 'score_chassis', 'score_electronics', 'score_ease_of_repair']:
            val = locals()[dim_field]
            if val:
                setattr(rel, dim_field, float(val))
        from motorgeek.core.scoring import recompute_aggregate
        recompute_aggregate(rel)

    session.commit()
    return RedirectResponse(url=f"/cars/{car_id}", status_code=303)


def delete_car_post(car_id: int, request: Request) -> HTMLResponse:
    session = get_session()
    car = session.query(Car).filter(Car.id == car_id).first()
    if not car:
        return HTMLResponse("Car not found", status_code=404)
    session.delete(car)
    session.commit()
    return RedirectResponse(url="/cars", status_code=303)
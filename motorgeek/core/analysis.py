from sqlalchemy.orm import Session
from sqlalchemy import func
from motorgeek.core.models import Car, Performance, PowertrainICE, Reliability

VALID_DIMENSIONS = ['engine', 'transmission', 'chassis', 'electronics', 'ease_of_repair']


def calculate_power_to_weight(hp: float, weight_kg: float) -> float:
    if not weight_kg:
        return 0.0
    return round(hp / (weight_kg / 1000), 2)


def calculate_hp_per_liter(hp: float, displacement_cc: int) -> float:
    if not displacement_cc:
        return 0.0
    return round(hp / (displacement_cc / 1000), 2)


def calculate_cost_per_hp(market_price: float, hp: float) -> float:
    if not hp:
        return 0.0
    return round(market_price / hp, 2)


def calculate_msrp_inflation_adj(msrp: float, year: int, current_year: int = 2026) -> float:
    CPI_MULTIPLIERS = {
        1990: 2.14, 1991: 2.08, 1992: 2.03, 1993: 1.98, 1994: 1.93,
        1995: 1.88, 1996: 1.84, 1997: 1.80, 1998: 1.75, 1999: 1.71,
        2000: 1.66, 2001: 1.62, 2002: 1.59, 2003: 1.55, 2004: 1.51,
        2005: 1.47, 2006: 1.43, 2007: 1.39, 2008: 1.35, 2009: 1.33,
        2010: 1.30, 2011: 1.28, 2012: 1.25, 2013: 1.23, 2014: 1.21,
        2015: 1.19, 2016: 1.17, 2017: 1.14, 2018: 1.11, 2019: 1.09,
        2020: 1.07, 2021: 1.05, 2022: 1.02, 2023: 1.00, 2024: 0.98,
        2025: 0.97, 2026: 0.96,
    }
    if not msrp or not year:
        return msrp or 0.0
    multiplier = CPI_MULTIPLIERS.get(year, 1.0)
    return round(msrp * multiplier, 2)


def rank_cars(session: Session, metric: str, limit: int = 20, ascending: bool = True) -> list:
    if metric == "0-60":
        results = (
            session.query(Car, Performance.accel_0_60)
            .join(Performance)
            .filter(Performance.accel_0_60.isnot(None))
            .order_by(Performance.accel_0_60 if ascending else Performance.accel_0_60.desc())
            .limit(limit)
            .all()
        )
        return [(car, perf, "fastest" if ascending else "slowest") for car, perf in results]
    elif metric == "power-to-weight":
        results = (
            session.query(Car, PowertrainICE.horsepower_bhp, PowertrainICE.curb_weight_kg)
            .join(PowertrainICE)
            .filter(PowertrainICE.horsepower_bhp.isnot(None), PowertrainICE.curb_weight_kg.isnot(None))
            .all()
        )
        scored = [(car, calculate_power_to_weight(hp, wt), "highest") for car, hp, wt in results]
        scored.sort(key=lambda x: x[1], reverse=not ascending)
        return scored[:limit]
    elif metric == "reliability":
        results = (
            session.query(Car, Reliability.reliability_score)
            .join(Reliability)
            .filter(Reliability.reliability_score.isnot(None))
            .order_by(Reliability.reliability_score if not ascending else Reliability.reliability_score.desc())
            .limit(limit)
            .all()
        )
        return [(car, score, "most reliable" if not ascending else "least reliable") for car, score in results]
    elif metric.startswith("reliability-"):
        dim = metric.split("-", 1)[1]
        if dim not in VALID_DIMENSIONS:
            return []
        col = getattr(Reliability, f'score_{dim}')
        results = (
            session.query(Car, col)
            .join(Reliability)
            .filter(col.isnot(None))
            .order_by(col if not ascending else col.desc())
            .limit(limit)
            .all()
        )
        return [(car, score, f"most reliable {dim}" if not ascending else f"least reliable {dim}") for car, score in results]
    return []


def era_compare(session: Session, era1: str, era2: str) -> dict:
    results = {}
    for era in [era1, era2]:
        cars = session.query(Car).filter(Car.era_tag == era).all()
        if not cars:
            results[era] = {"count": 0}
            continue
        ids = [c.id for c in cars]
        avg_hp = session.query(func.avg(PowertrainICE.horsepower_bhp)).filter(
            PowertrainICE.car_id.in_(ids), PowertrainICE.horsepower_bhp.isnot(None)
        ).scalar() or 0
        avg_weight = session.query(func.avg(PowertrainICE.curb_weight_kg)).filter(
            PowertrainICE.car_id.in_(ids), PowertrainICE.curb_weight_kg.isnot(None)
        ).scalar() or 0
        avg_0_60 = session.query(func.avg(Performance.accel_0_60)).filter(
            Performance.car_id.in_(ids), Performance.accel_0_60.isnot(None)
        ).scalar() or 0
        results[era] = {
            "count": len(cars),
            "avg_hp": round(avg_hp, 1),
            "avg_weight_kg": round(avg_weight, 1),
            "avg_0_60": round(avg_0_60, 2),
        }
    return results
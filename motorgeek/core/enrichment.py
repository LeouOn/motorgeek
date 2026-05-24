from sqlalchemy.orm import Session
from motorgeek.core.models import Car, Performance, PowertrainICE
from motorgeek.core.analysis import calculate_power_to_weight, calculate_hp_per_liter


def fill_power_to_weight_gaps(session: Session) -> int:
    """Fill missing power_to_weight in PERFORMANCE using powertrain data."""
    cars = session.query(Car).all()
    updated = 0
    for car in cars:
        perf = session.query(Performance).filter(Performance.car_id == car.id).first()
        if perf and perf.power_to_weight is None:
            ice = session.query(PowertrainICE).filter(PowertrainICE.car_id == car.id).first()
            if ice and ice.horsepower_bhp and ice.curb_weight_kg:
                ptw = calculate_power_to_weight(ice.horsepower_bhp, ice.curb_weight_kg)
                perf.power_to_weight = ptw
                session.add(perf)
                updated += 1
    session.commit()
    return updated


def fill_hp_per_liter_gaps(session: Session) -> int:
    """Fill missing hp_per_liter (stored in extra JSON or computed on demand)."""
    cars = session.query(Car).all()
    updated = 0
    for car in cars:
        ice = session.query(PowertrainICE).filter(PowertrainICE.car_id == car.id).first()
        if ice and ice.horsepower_bhp and ice.displacement_cc:
            hpl = round(ice.horsepower_bhp / (ice.displacement_cc / 1000), 2)
            updated += 1
    session.commit()
    return updated


def enrich_from_similar(session: Session, car: Car, dimension: str) -> dict:
    """Use LLM to estimate missing fields by referencing similar cars."""
    from motorgeek.core.llm import LLMClient
    llm = LLMClient()
    ice = session.query(PowertrainICE).filter(PowertrainICE.car_id == car.id).first()
    if not ice:
        return {}
    prompt = (
        f"A {car.year_start} {car.make} {car.model} ({car.generation or 'base'}) has "
        f"{ice.horsepower_bhp} HP, {ice.displacement_cc}cc, {ice.aspiration or 'NA'} aspiration. "
        f"Estimate the missing {dimension} data for this car by comparing to similar era/segment cars. "
        f"Return JSON with your best estimates."
    )
    try:
        return llm.complete_json(prompt)
    except Exception:
        return {}
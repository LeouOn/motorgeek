import typer
from rich.console import Console
from sqlalchemy.orm import Session

from motorgeek.core.database import get_session
from motorgeek.core.models import Car, Performance, PowertrainICE, MarketHistory
from motorgeek.core.analysis import (
    calculate_power_to_weight, calculate_hp_per_liter,
    calculate_cost_per_hp, calculate_msrp_inflation_adj
)

app = typer.Typer(name="calc")
console = Console()


@app.command("power-to-weight")
def calc_power_to_weight(car_ref: str = typer.Argument(...)):
    """Calculate power-to-weight ratio for a car."""
    session = get_session()
    car, ice = _resolve_with_ice(session, car_ref)
    if not car:
        console.print(f"[red]Car not found:[/red] {car_ref}")
        raise typer.Exit(1)
    if not ice or not ice.horsepower_bhp or not ice.curb_weight_kg:
        console.print("[yellow]Missing HP or weight data[/yellow]")
        raise typer.Exit(1)
    ptw = calculate_power_to_weight(ice.horsepower_bhp, ice.curb_weight_kg)
    console.print(f"{car.make} {car.model}: {ptw} HP/tonne")


@app.command("hp-per-liter")
def calc_hp_per_liter(car_ref: str = typer.Argument(...)):
    """Calculate specific output (HP per liter)."""
    session = get_session()
    car, ice = _resolve_with_ice(session, car_ref)
    if not car:
        console.print(f"[red]Car not found:[/red] {car_ref}")
        raise typer.Exit(1)
    if not ice or not ice.horsepower_bhp or not ice.displacement_cc:
        console.print("[yellow]Missing HP or displacement data[/yellow]")
        raise typer.Exit(1)
    hpl = calculate_hp_per_liter(ice.horsepower_bhp, ice.displacement_cc)
    console.print(f"{car.make} {car.model}: {hpl} HP/liter")


@app.command("inflation")
def calc_inflation(
    car_ref: str = typer.Argument(...),
    current_year: int = typer.Option(2026, "--current-year"),
):
    """Adjust MSRP to today's dollars."""
    session = get_session()
    car = _resolve_car(session, car_ref)
    if not car:
        console.print(f"[red]Car not found:[/red] {car_ref}")
        raise typer.Exit(1)
    from motorgeek.core.models import CostToOwn
    cost = session.query(CostToOwn).filter(CostToOwn.car_id == car.id).first()
    if not cost or not cost.msrp_original:
        console.print("[yellow]No MSRP data available[/yellow]")
        raise typer.Exit(1)
    adj = calculate_msrp_inflation_adj(cost.msrp_original, car.year_start, current_year)
    console.print(f"{car.make} {car.model} ({car.year_start}): ${cost.msrp_original:,.0f} → ${adj:,.0f} today")


@app.command("cost-per-hp")
def calc_cost_per_hp(car_ref: str = typer.Argument(...)):
    """Calculate cost per HP using latest market data."""
    session = get_session()
    car, ice = _resolve_with_ice(session, car_ref)
    if not car:
        console.print(f"[red]Car not found:[/red] {car_ref}")
        raise typer.Exit(1)
    latest_market = (
        session.query(MarketHistory)
        .filter(MarketHistory.car_id == car.id)
        .order_by(MarketHistory.date_recorded.desc())
        .first()
    )
    if not latest_market or not (latest_market.price_low and latest_market.price_high):
        console.print("[yellow]No market data available[/yellow]")
        raise typer.Exit(1)
    avg_price = (latest_market.price_low + latest_market.price_high) / 2
    if not ice or not ice.horsepower_bhp:
        console.print("[yellow]Missing HP data[/yellow]")
        raise typer.Exit(1)
    cph = calculate_cost_per_hp(avg_price, ice.horsepower_bhp)
    console.print(f"{car.make} {car.model}: ${cph:,.0f} per HP (market avg ${avg_price:,.0f}, {ice.horsepower_bhp:.0f} HP)")


def _resolve_car(session: Session, car_ref: str) -> Car | None:
    if car_ref.isdigit():
        return session.query(Car).filter(Car.id == int(car_ref)).first()
    parts = car_ref.split("-")
    query = session.query(Car)
    for part in parts:
        query = query.filter(Car.make.ilike(f"%{part}%") | Car.model.ilike(f"%{part}%"))
    return query.first()


def _resolve_with_ice(session: Session, car_ref: str):
    car = _resolve_car(session, car_ref)
    if not car:
        return None, None
    ice = session.query(PowertrainICE).filter(PowertrainICE.car_id == car.id).first()
    return car, ice
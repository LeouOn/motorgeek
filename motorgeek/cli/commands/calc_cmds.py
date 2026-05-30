import typer
from rich.console import Console
from rich.table import Table
from sqlalchemy.orm import Session

from motorgeek.core.database import get_session
from motorgeek.core.models import Car, Performance, PowertrainICE, MarketHistory, Reliability
from motorgeek.core.analysis import (
    calculate_power_to_weight, calculate_hp_per_liter,
    calculate_cost_per_hp, calculate_msrp_inflation_adj,
    era_compare,
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


@app.command("rank")
def calc_rank(
    metric: str = typer.Argument(..., help="Metric: 0-60, hp, hp-per-liter, power-weight, torque, displacement, weight, reliability"),
    limit: int = typer.Option(10, "--limit", "-n", help="Max results to show"),
    ascending: bool = typer.Option(False, "--ascending/--descending", help="Sort direction"),
):
    """Rank all cars by a metric."""
    session = get_session()
    cars = session.query(Car).all()
    if not cars:
        console.print("[yellow]No cars in database[/yellow]")
        raise typer.Exit(1)

    scored = []
    for car in cars:
        ice = session.query(PowertrainICE).filter(PowertrainICE.car_id == car.id).first()
        perf = session.query(Performance).filter(Performance.car_id == car.id).first()
        rel = session.query(Reliability).filter(Reliability.car_id == car.id).first()

        val = None
        if metric == "0-60" and perf and perf.accel_0_60:
            val = (perf.accel_0_60, "s", True)
        elif metric in ("hp", "horsepower") and ice and ice.horsepower_bhp:
            val = (ice.horsepower_bhp, "HP", False)
        elif metric in ("hp-per-liter", "hpl") and ice and ice.horsepower_bhp and ice.displacement_cc:
            val = (calculate_hp_per_liter(ice.horsepower_bhp, ice.displacement_cc), "HP/L", False)
        elif metric in ("power-weight", "ptw") and ice and ice.horsepower_bhp and ice.curb_weight_kg:
            val = (calculate_power_to_weight(ice.horsepower_bhp, ice.curb_weight_kg), "HP/t", False)
        elif metric == "torque" and ice and ice.torque_nm:
            val = (ice.torque_nm, "Nm", False)
        elif metric == "displacement" and ice and ice.displacement_cc:
            val = (ice.displacement_cc, "cc", False)
        elif metric == "weight" and ice and ice.curb_weight_kg:
            val = (ice.curb_weight_kg, "kg", True)
        elif metric == "reliability" and rel and rel.reliability_score:
            val = (rel.reliability_score, "/100", False)

        if val:
            scored.append((car, val[0], val[1], val[2]))

    if not scored:
        console.print(f"[yellow]No data for metric:[/yellow] {metric}")
        console.print("Available: 0-60, hp, hp-per-liter, power-weight, torque, displacement, weight")
        raise typer.Exit(1)

    scored.sort(key=lambda x: x[1], reverse=ascending)
    scored = scored[:limit]

    metric_labels = {
        "0-60": "0-60 (s)",
        "hp": "HP",
        "hp-per-liter": "HP/L",
        "power-weight": "HP/t",
        "torque": "Torque",
        "displacement": "Disp",
        "weight": "Weight",
        "reliability": "Score",
    }
    label = metric_labels.get(metric, metric)

    table = Table(title=f"Ranking by {label}")
    table.add_column("#", style="cyan", width=3)
    table.add_column("Car", style="magenta")
    table.add_column(label, justify="right")
    for i, (car, val, unit, is_bad) in enumerate(scored, 1):
        table.add_row(str(i), f"{car.make} {car.model} ({car.generation or 'base'})", f"{val:.1f} {unit}")
    console.print(table)


@app.command("era-compare")
def calc_era_compare(
    era1: str = typer.Argument(..., help="First era tag, e.g. '90s'"),
    era2: str = typer.Argument(..., help="Second era tag, e.g. '00s'"),
):
    """Compare aggregate stats between two eras."""
    session = get_session()
    results = era_compare(session, era1, era2)

    table = Table(title=f"Era Comparison: {era1} vs {era2}")
    table.add_column("Metric", style="cyan")
    table.add_column(era1, justify="right")
    table.add_column(era2, justify="right")

    r1 = results.get(era1, {})
    r2 = results.get(era2, {})

    if r1.get("count", 0) == 0 and r2.get("count", 0) == 0:
        console.print(f"[yellow]No cars found with era tags '{era1}' or '{era2}'[/yellow]")
        console.print("Set era tags with: motorgeek car edit <id>")
        raise typer.Exit(1)

    table.add_row("Cars", str(r1.get("count", 0)), str(r2.get("count", 0)))
    table.add_row("Avg HP", f'{r1.get("avg_hp", 0):,.0f}', f'{r2.get("avg_hp", 0):,.0f}')
    table.add_row("Avg Weight (kg)", f'{r1.get("avg_weight_kg", 0):,.0f}', f'{r2.get("avg_weight_kg", 0):,.0f}')
    table.add_row("Avg 0-60 (s)", f'{r1.get("avg_0_60", 0):.1f}', f'{r2.get("avg_0_60", 0):.1f}')
    console.print(table)


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
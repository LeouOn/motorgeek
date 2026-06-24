import typer
from rich.console import Console
from rich.table import Table
from sqlalchemy.orm import Session

from motorgeek.core.calculators.composite import compute_composite_for_car
from motorgeek.core.calculators.practicality import compute_practicality_for_car
from motorgeek.core.calculators.zeperfs import classify_zp, compute_zp_for_car
from motorgeek.core.database import get_session
from motorgeek.core.models import (
    BuildQuality,
    Car,
    Performance,
    PowertrainEV,
    PowertrainICE,
    MarketHistory,
    Reliability,
    ZePerfsIndices,
)
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
    metric: str = typer.Argument(..., help="Metric: 0-60, hp, hp-per-liter, power-weight, torque, displacement, weight, reliability, reliability-engine, reliability-transmission, reliability-chassis, reliability-electronics, reliability-ease_of_repair, zp, composite, practicality"),
    limit: int = typer.Option(10, "--limit", "-n", help="Max results to show"),
    ascending: bool = typer.Option(False, "--ascending/--descending", help="Sort direction"),
):
    """Rank all cars by a metric."""
    session = get_session()
    cars = session.query(Car).all()
    if not cars:
        console.print("[yellow]No cars in database[/yellow]")
        raise typer.Exit(1)

    # Composite and practicality need richer row shaping (breakdown strings,
    # extra ORM fetches) than the simple (value, unit, is_bad) tuple used by
    # the legacy branches. Handle them in dedicated handlers and then share
    # the same sort + render pipeline below.
    if metric == "composite":
        scored = _rank_composite(session, cars)
        if not scored:
            console.print("[yellow]No cars with enough data for a composite score[/yellow]")
            console.print("Need at least 2 of: build_quality, reliability, practicality, ZP.")
            raise typer.Exit(1)
        _render_rank_table("Composite", scored, limit, ascending, is_bad=False,
                           detail_field="breakdown")
        return
    if metric in ("practicality", "prac"):
        scored = _rank_practicality(session, cars)
        if not scored:
            console.print("[yellow]No cars with practicality data[/yellow]")
            raise typer.Exit(1)
        _render_rank_table("Practicality", scored, limit, ascending, is_bad=False)
        return

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
        elif metric.startswith("reliability-") and rel:
            dim = metric.split("-", 1)[1]
            dim_val = getattr(rel, f'score_{dim}', None)
            if dim_val is not None:
                val = (dim_val, f"/100 ({dim})", False)
        elif metric == "zp":
            # ZePerfs Index from the v4 ICE / v3 EV calculator. Skip cars
            # with insufficient data (None ZP). Show the class label inline.
            zp, _branch = compute_zp_for_car(car, ice, perf)
            if zp is not None:
                val = (zp, f"({classify_zp(zp)})", False)

        if val:
            scored.append((car, val[0], val[1], val[2]))

    if not scored:
        console.print(f"[yellow]No data for metric:[/yellow] {metric}")
        console.print("Available: 0-60, hp, hp-per-liter, power-weight, torque, displacement, weight, zp, composite, practicality")
        raise typer.Exit(1)

    _render_rank_table(metric, scored, limit, ascending, is_bad=scored[0][3])


def _rank_composite(session: Session, cars: list[Car]) -> list[tuple]:
    """Score every car with the composite index.

    Returns tuples shaped ``(car, composite, breakdown_str, is_bad=False)``
    where ``breakdown_str`` is a one-line summary of each dimension's
    contribution (e.g. ``"Q:85 R:88 P:50 ZP:79"``).
    """
    from motorgeek.core.models import Dimensions

    scored: list[tuple] = []
    for car in cars:
        ice = session.query(PowertrainICE).filter(PowertrainICE.car_id == car.id).first()
        ev = session.query(PowertrainEV).filter(PowertrainEV.car_id == car.id).first()
        perf = session.query(Performance).filter(Performance.car_id == car.id).first()
        rel = session.query(Reliability).filter(Reliability.car_id == car.id).first()
        bq = session.query(BuildQuality).filter(BuildQuality.car_id == car.id).first()
        zp_row = session.query(ZePerfsIndices).filter(ZePerfsIndices.car_id == car.id).first()
        dims_row = session.query(Dimensions).filter(Dimensions.car_id == car.id).first()

        # Prefer a previously-computed ZP value (avoids re-running the
        # formula for every rank invocation); fall back to live computation.
        zp_value = zp_row.zeperfs_index if zp_row is not None else None

        composite, dim_vals = compute_composite_for_car(
            car, ice, ev,
            performance=perf,
            build_quality=bq,
            reliability=rel,
            dimensions=dims_row,
            zp_value=zp_value,
        )
        if composite is None:
            continue

        breakdown = _format_composite_breakdown(dim_vals)
        scored.append((car, composite, breakdown, False))
    return scored


def _rank_practicality(session: Session, cars: list[Car]) -> list[tuple]:
    """Score every car by practicality alone."""
    scored: list[tuple] = []
    for car in cars:
        ice = session.query(PowertrainICE).filter(PowertrainICE.car_id == car.id).first()
        ev = session.query(PowertrainEV).filter(PowertrainEV.car_id == car.id).first()
        score = compute_practicality_for_car(car, ice, ev)
        scored.append((car, score, "/100", False))
    return scored


def _format_composite_breakdown(dims: dict) -> str:
    """Render the per-dimension dict as ``Q:85 R:88 P:50 ZP:79``.

    Missing dimensions are shown as ``--`` so the reader can see at a glance
    which inputs were redistributed.
    """
    def _fmt(value):
        return "--" if value is None else f"{value:.0f}"
    return (
        f"Q:{_fmt(dims.get('quality'))} "
        f"R:{_fmt(dims.get('reliability'))} "
        f"P:{_fmt(dims.get('practicality'))} "
        f"ZP:{_fmt(dims.get('performance'))}"
    )


def _render_rank_table(
    label: str,
    scored: list[tuple],
    limit: int,
    ascending: bool,
    is_bad: bool,
    detail_field: str | None = None,
) -> None:
    """Sort and render a ranking table.

    ``scored`` is a list of ``(car, value, unit_or_detail, is_bad)`` tuples.
    ``detail_field`` (when set) names the per-row field to render in a
    third column instead of the ``unit`` string -- used by ``composite``
    to show the per-dimension breakdown.
    """
    if ascending:
        scored.sort(key=lambda x: x[1])
    else:
        scored.sort(key=lambda x: x[1], reverse=not is_bad)
    scored = scored[:limit]

    label_lookup = {
        "0-60": "0-60 (s)",
        "hp": "HP",
        "hp-per-liter": "HP/L",
        "power-weight": "HP/t",
        "torque": "Torque",
        "displacement": "Disp",
        "weight": "Weight",
        "reliability": "Score",
        "reliability-engine": "Engine",
        "reliability-transmission": "Transmission",
        "reliability-chassis": "Chassis",
        "reliability-electronics": "Electronics",
        "reliability-ease_of_repair": "Ease of Repair",
        "zp": "ZP",
        "composite": "Composite",
        "practicality": "Score",
        "prac": "Score",
    }
    header = label_lookup.get(label, label)

    table = Table(title=f"Ranking by {header}")
    table.add_column("#", style="cyan", width=3)
    table.add_column("Car", style="magenta")
    table.add_column(header, justify="right")
    if detail_field is not None:
        table.add_column("Breakdown", style="dim")
    for i, row in enumerate(scored, 1):
        car = row[0]
        val = row[1]
        third = row[2]
        if detail_field is not None:
            table.add_row(
                str(i),
                f"{car.make} {car.model} ({car.generation or 'base'})",
                f"{val:.1f}",
                str(third),
            )
        else:
            unit = third
            table.add_row(
                str(i),
                f"{car.make} {car.model} ({car.generation or 'base'})",
                f"{val:.1f} {unit}",
            )
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
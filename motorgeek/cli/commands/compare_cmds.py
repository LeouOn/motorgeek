import typer
from rich.console import Console
from rich.table import Table
from sqlalchemy.orm import Session

from motorgeek.core.database import get_session
from motorgeek.core.models import Car, Performance, PowertrainICE
from motorgeek.core.analysis import calculate_power_to_weight, calculate_hp_per_liter

app = typer.Typer(name="compare")
console = Console()


@app.command("compare")
def compare(
    cars: list[str] = typer.Argument(..., help="Car IDs or slugs"),
    dimensions: str = typer.Option("perf,eng", "--dimensions", "-d", help="Comma-separated: perf,eng,rel,cost"),
    fmt: str = typer.Option("table", "--format", "-f", help="table|radar|narrative"),
):
    """Compare two or more cars side-by-side."""
    session = get_session()
    resolved = [_resolve_car(session, ref) for ref in cars]
    resolved = [c for c in resolved if c]
    if len(resolved) < 2:
        console.print("[red]Need at least 2 cars to compare[/red]")
        raise typer.Exit(1)

    dim_list = [d.strip() for d in dimensions.split(",")]
    table = Table(title="Comparison")
    table.add_column("Metric", style="cyan")
    for car in resolved:
        table.add_column(f"{car.make} {car.model}", style="magenta")

    if "perf" in dim_list:
        perf_data = {c.id: session.query(Performance).filter(Performance.car_id == c.id).first() for c in resolved}
        ice_data = {c.id: session.query(PowertrainICE).filter(PowertrainICE.car_id == c.id).first() for c in resolved}
        for label, attr, direction in [
            ("0-60 (s)", None, "min"),
            ("0-100 (s)", "accel_0_100", "min"),
            ("Top Speed (mph)", "top_speed_mph", "max"),
            ("Power/Weight", None, "max"),
            ("Lateral G", "lateral_g", "max"),
        ]:
            if attr:
                vals = [getattr(perf_data.get(c.id), attr, None) for c in resolved]
                row = [label] + [f"{v:.2f}" if v is not None else "-" for v in vals]
            else:
                if label == "0-60 (s)":
                    vals = [getattr(perf_data.get(c.id), "accel_0_60", None) for c in resolved]
                elif label == "Power/Weight":
                    vals = []
                    for c in resolved:
                        ice = ice_data.get(c.id)
                        if ice and ice.horsepower_bhp and ice.curb_weight_kg:
                            ptw = calculate_power_to_weight(ice.horsepower_bhp, ice.curb_weight_kg)
                            vals.append(ptw)
                        else:
                            vals.append(None)
                row = [label] + [f"{v:.2f}" if v is not None else "-" for v in vals]
            table.add_row(*row)

    if "eng" in dim_list:
        ice_data = {c.id: session.query(PowertrainICE).filter(PowertrainICE.car_id == c.id).first() for c in resolved}
        for label, attr, direction in [
            ("HP", "horsepower_bhp", "max"),
            ("Torque (Nm)", "torque_nm", "max"),
            ("Displacement (cc)", "displacement_cc", "max"),
            ("Redline (rpm)", "redline_rpm", "max"),
            ("Weight (kg)", "curb_weight_kg", "min"),
            ("HP/Liter", None, "max"),
        ]:
            if attr:
                vals = [getattr(ice_data.get(c.id), attr, None) for c in resolved]
                row = [label] + [f"{v}" if v is not None else "-" for v in vals]
            else:
                vals = [calculate_hp_per_liter(getattr(ice_data.get(c.id), "horsepower_bhp", 0) or 0, getattr(ice_data.get(c.id), "displacement_cc", 0) or 0) for c in resolved]
                row = [label] + [f"{v:.1f}" if v else "-" for v in vals]
            table.add_row(*row)

    console.print(table)


@app.command("group")
def compare_group(name: str = typer.Argument(..., help="Comparison session name")):
    """Use a saved COMPARISON_SESSION."""
    console.print(f"[cyan]Loading comparison group:[/cyan] {name}")


def _resolve_car(session: Session, car_ref: str) -> Car | None:
    if car_ref.isdigit():
        return session.query(Car).filter(Car.id == int(car_ref)).first()
    parts = car_ref.split("-")
    query = session.query(Car)
    for part in parts:
        query = query.filter(Car.make.ilike(f"%{part}%") | Car.model.ilike(f"%{part}%"))
    return query.first()
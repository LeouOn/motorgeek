import typer
from rich.console import Console
from rich.table import Table
from datetime import datetime
from sqlalchemy.orm import Session

from motorgeek.core.database import get_session
from motorgeek.core.models import Car, RepairCosts, RepairCatalog

app = typer.Typer(name="repair")
console = Console()


@app.command("add")
def repair_add(
    car_ref: str = typer.Argument(..., help="Car ID or slug"),
    repair_name: str = typer.Option(..., "--repair-name", help="Name of repair"),
    repair_category: str = typer.Option(..., "--category", help="Category: engine, transmission, electrical, etc."),
    parts_cost: float = typer.Option(0, "--parts"),
    labor_cost: float = typer.Option(0, "--labor"),
    total_cost: float = typer.Option(None, "--total"),
    mileage: int = typer.Option(0, "--mileage"),
    shop: str = typer.Option("diy", "--shop", help="dealer, independent, diy"),
    source: str = typer.Option("personal", "--source", help="RepairPal, CarMD, personal, forum, etc."),
    is_recall: bool = typer.Option(False, "--recall"),
):
    """Log a repair event for a car."""
    session = get_session()
    car = _resolve_car(session, car_ref)
    if not car:
        console.print(f"[red]Car not found:[/red] {car_ref}")
        raise typer.Exit(1)

    total = total_cost if total_cost is not None else (parts_cost + labor_cost)
    entry = RepairCosts(
        car_id=car.id,
        date=datetime.now(),
        mileage_at_repair=mileage,
        repair_category=repair_category,
        repair_name=repair_name,
        parts_cost=parts_cost,
        labor_cost=labor_cost,
        total_cost=total,
        currency="USD",
        shop_type=shop,
        source=source,
        is_warranty_covered=False,
        is_recall=is_recall,
    )
    session.add(entry)
    session.commit()
    console.print(f"[green]Logged repair for[/green] {car.make} {car.model}: {repair_name} — ${total:,.2f}")


@app.command("catalog")
def repair_catalog(car_ref: str = typer.Argument(...)):
    """Show baseline repair costs from catalog."""
    session = get_session()
    car = _resolve_car(session, car_ref)
    if not car:
        console.print(f"[red]Car not found:[/red] {car_ref}")
        raise typer.Exit(1)

    items = session.query(RepairCatalog).filter(RepairCatalog.car_id == car.id).all()
    if not items:
        console.print("[yellow]No catalog entries yet.[/yellow]")
        return

    table = Table(title=f"Repair Catalog: {car.make} {car.model}")
    table.add_column("Repair", style="cyan")
    table.add_column("Category", style="magenta")
    table.add_column("Cost Range", style="green")
    table.add_column("Frequency", style="yellow")
    table.add_column("DIY", style="dim")

    for item in items:
        cost_range = f"${item.avg_cost_low:,.0f}–${item.avg_cost_high:,.0f}" if item.avg_cost_low else "-"
        table.add_row(
            item.repair_name or "-",
            item.repair_category or "-",
            cost_range,
            item.frequency or "-",
            item.diy_difficulty or "-",
        )

    console.print(table)


def _resolve_car(session: Session, car_ref: str) -> Car | None:
    if car_ref.isdigit():
        return session.query(Car).filter(Car.id == int(car_ref)).first()
    parts = car_ref.split("-")
    query = session.query(Car)
    for part in parts:
        query = query.filter(Car.make.ilike(f"%{part}%") | Car.model.ilike(f"%{part}%"))
    return query.first()
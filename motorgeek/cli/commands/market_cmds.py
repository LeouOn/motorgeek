import typer
from rich.console import Console
from rich.table import Table
from datetime import datetime
from sqlalchemy.orm import Session

from motorgeek.core.database import get_session
from motorgeek.core.models import Car, MarketHistory

app = typer.Typer(name="market")
console = Console()


@app.command("add")
def market_add(
    car_ref: str = typer.Argument(..., help="Car ID or slug"),
    price_low: float = typer.Option(..., "--price-low", help="Low price"),
    price_high: float = typer.Option(..., "--price-high", help="High price"),
    source: str = typer.Option("", "--source", "-s", help="Source site name"),
    date: str = typer.Option(lambda: datetime.now().strftime("%Y-%m-%d"), "--date", help="Date YYYY-MM-DD"),
    trend: str = typer.Option("stable", "--trend", help="rising, stable, falling"),
):
    """Log a new MARKET_HISTORY entry."""
    session = get_session()
    car = _resolve_car(session, car_ref)
    if not car:
        console.print(f"[red]Car not found:[/red] {car_ref}")
        raise typer.Exit(1)

    parsed_date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
    entry = MarketHistory(
        car_id=car.id,
        date_recorded=parsed_date,
        price_low=price_low,
        price_high=price_high,
        volume_sold_est=None,
        market_trend_indicator=trend,
        source_site=source or "manual",
    )
    session.add(entry)
    session.commit()
    console.print(f"[green]Logged market data for[/green] {car.make} {car.model}: ${price_low:,.0f}–${price_high:,.0f}")


@app.command("chart")
def market_chart(car_ref: str = typer.Argument(...)):
    """Show price trend over time."""
    session = get_session()
    car = _resolve_car(session, car_ref)
    if not car:
        console.print(f"[red]Car not found:[/red] {car_ref}")
        raise typer.Exit(1)

    entries = (
        session.query(MarketHistory)
        .filter(MarketHistory.car_id == car.id)
        .order_by(MarketHistory.date_recorded)
        .all()
    )

    if not entries:
        console.print("[yellow]No market data yet. Run 'motorgeek market add' first.[/yellow]")
        raise typer.Exit(1)

    table = Table(title=f"Market History: {car.make} {car.model}")
    table.add_column("Date", style="cyan")
    table.add_column("Price Low", style="green")
    table.add_column("Price High", style="green")
    table.add_column("Trend", style="yellow")
    table.add_column("Source", style="dim")

    for e in entries:
        date_str = e.date_recorded.strftime("%Y-%m-%d") if e.date_recorded else "-"
        table.add_row(date_str, f"${e.price_low:,.0f}", f"${e.price_high:,.0f}", e.market_trend_indicator or "-", e.source_site or "-")

    console.print(table)


def _resolve_car(session: Session, car_ref: str) -> Car | None:
    if car_ref.isdigit():
        return session.query(Car).filter(Car.id == int(car_ref)).first()
    parts = car_ref.split("-")
    query = session.query(Car)
    for part in parts:
        query = query.filter(Car.make.ilike(f"%{part}%") | Car.model.ilike(f"%{part}%"))
    return query.first()
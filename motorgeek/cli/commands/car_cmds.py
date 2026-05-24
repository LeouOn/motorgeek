import typer
from rich.console import Console
from rich.table import Table
from sqlalchemy.orm import Session

from motorgeek.core.database import get_session
from motorgeek.core.models import Car

app = typer.Typer(name="car")
console = Console()


def _resolve_car(session: Session, car_ref: str) -> Car | None:
    try:
        car_id = int(car_ref)
        return session.get(Car, car_id)
    except ValueError:
        slug = car_ref.lower().replace(" ", "-")
        cars = session.query(Car).all()
        for car in cars:
            if slug in car.slug:
                return car
        return None


@app.command()
def add(
    make: str,
    model: str,
    year_start: int = typer.Option(..., "--year-start"),
    year_end: int = typer.Option(None, "--year-end"),
    generation: str = typer.Option(None, "--generation"),
    body_style: str = typer.Option(None, "--body-style"),
    country: str = typer.Option(None, "--country"),
):
    session = get_session()
    car = Car(
        make=make,
        model=model,
        year_start=year_start,
        year_end=year_end,
        generation=generation,
        body_style=body_style,
        country=country,
    )
    session.add(car)
    session.commit()
    console.print(f"[green]Created {make} {model} ({generation})[/green] — ID {car.id}")


@app.command()
def list():
    session = get_session()
    cars = session.query(Car).all()
    if not cars:
        console.print("No cars in database. Run [cyan]motorgeek car add[/cyan] to add one.")
        return

    table = Table(title="Cars")
    table.add_column("ID", style="cyan")
    table.add_column("Make")
    table.add_column("Model")
    table.add_column("Gen")
    table.add_column("Years")
    table.add_column("Body")
    table.add_column("Country")

    for car in cars:
        years = f"{car.year_start}" + (f"-{car.year_end}" if car.year_end else "")
        table.add_row(
            str(car.id),
            car.make,
            car.model,
            car.generation or "",
            years,
            car.body_style or "",
            car.country or "",
        )

    console.print(table)


@app.command()
def show(car_ref: str):
    session = get_session()
    car = _resolve_car(session, car_ref)
    if not car:
        console.print("[red]Car not found[/red]")
        raise typer.Exit(code=1)

    console.print(f"\n[bold]{car.make} {car.model}[/bold] (ID: {car.id})")
    if car.generation:
        console.print(f"Generation: {car.generation}")
    console.print(f"Years: {car.year_start}" + (f" - {car.year_end}" if car.year_end else ""))
    if car.body_style:
        console.print(f"Body: {car.body_style}")
    if car.country:
        console.print(f"Country: {car.country}")
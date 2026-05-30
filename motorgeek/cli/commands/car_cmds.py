import typer
from rich.console import Console
from rich.table import Table
from sqlalchemy.orm import Session

from motorgeek.core.database import get_session
from motorgeek.core.models import Car, Performance, PowertrainICE, Reliability

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


@app.command()
def edit(car_ref: str):
    session = get_session()
    car = _resolve_car(session, car_ref)
    if not car:
        console.print("[red]Car not found[/red]")
        raise typer.Exit(code=1)

    def prompt_field(label: str, current: str | None) -> str | None:
        default = f"[{current}]" if current else ""
        val = typer.prompt(f"{label} {default}", default="", show_default=False)
        return val if val else None

    def prompt_int_field(label: str, current: int | None) -> int | None:
        while True:
            default = f"[{current}]" if current else ""
            val = typer.prompt(f"{label} {default}", default="", show_default=False)
            if not val:
                return None
            try:
                return int(val)
            except ValueError:
                console.print(f"[red]Invalid integer: {val}[/red]")

    console.print(f"\nEditing car {car.id}. Press Enter to keep current value.\n")

    make = prompt_field("make", car.make)
    if make is not None:
        car.make = make

    model = prompt_field("model", car.model)
    if model is not None:
        car.model = model

    generation = prompt_field("generation", car.generation)
    if generation is not None:
        car.generation = generation

    year_start = prompt_int_field("year_start", car.year_start)
    if year_start is not None:
        car.year_start = year_start

    year_end = prompt_int_field("year_end", car.year_end)
    if year_end is not None:
        car.year_end = year_end

    body_style = prompt_field("body_style", car.body_style)
    if body_style is not None:
        car.body_style = body_style

    country = prompt_field("country", car.country)
    if country is not None:
        car.country = country

    era_tag = prompt_field("era_tag", car.era_tag)
    if era_tag is not None:
        car.era_tag = era_tag

    perf = session.query(Performance).filter(Performance.car_id == car.id).first()
    if perf:
        console.print("\n[bold]Performance fields[/bold]")
        val = prompt_field("accel_0_60", str(perf.accel_0_60) if perf.accel_0_60 else None)
        if val is not None:
            perf.accel_0_60 = float(val) if val else None
        val = prompt_field("accel_0_100", str(perf.accel_0_100) if perf.accel_0_100 else None)
        if val is not None:
            perf.accel_0_100 = float(val) if val else None
        val = prompt_field("top_speed_mph", str(perf.top_speed_mph) if perf.top_speed_mph else None)
        if val is not None:
            perf.top_speed_mph = float(val) if val else None
        val = prompt_field("lateral_g", str(perf.lateral_g) if perf.lateral_g else None)
        if val is not None:
            perf.lateral_g = float(val) if val else None

    ice = session.query(PowertrainICE).filter(PowertrainICE.car_id == car.id).first()
    if ice:
        console.print("\n[bold]Powertrain ICE fields[/bold]")
        val = prompt_field("horsepower_bhp", str(ice.horsepower_bhp) if ice.horsepower_bhp else None)
        if val is not None:
            ice.horsepower_bhp = float(val) if val else None
        val = prompt_field("torque_nm", str(ice.torque_nm) if ice.torque_nm else None)
        if val is not None:
            ice.torque_nm = float(val) if val else None
        val = prompt_field("displacement_cc", str(ice.displacement_cc) if ice.displacement_cc else None)
        if val is not None:
            ice.displacement_cc = float(val) if val else None
        val = prompt_field("redline_rpm", str(ice.redline_rpm) if ice.redline_rpm else None)
        if val is not None:
            ice.redline_rpm = int(val) if val else None
        val = prompt_field("curb_weight_kg", str(ice.curb_weight_kg) if ice.curb_weight_kg else None)
        if val is not None:
            ice.curb_weight_kg = float(val) if val else None

    rel = session.query(Reliability).filter(Reliability.car_id == car.id).first()
    if rel:
        console.print("\n[bold]Reliability fields[/bold]")
        val = prompt_field("reliability_score", str(rel.reliability_score) if rel.reliability_score else None)
        if val is not None:
            rel.reliability_score = float(val) if val else None

    session.commit()
    console.print(f"[green]Updated car {car.id}: {car.make} {car.model} ({car.generation})[/green]")


@app.command()
def delete(car_ref: str):
    session = get_session()
    car = _resolve_car(session, car_ref)
    if not car:
        console.print("[red]Car not found[/red]")
        raise typer.Exit(code=1)

    console.print(f"Delete {car.make} {car.model} (ID {car.id})? This will remove ALL associated data.")
    confirm = typer.prompt("Type 'yes' to confirm")
    if confirm != "yes":
        console.print("[yellow]Cancelled.[/yellow]")
        raise typer.Exit()

    session.delete(car)
    session.commit()
    console.print(f"[green]Deleted car {car.id}.[/green]")
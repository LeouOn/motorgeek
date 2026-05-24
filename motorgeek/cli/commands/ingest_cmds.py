import typer
from rich.console import Console
from rich.table import Table
from sqlalchemy.orm import Session

from motorgeek.core.database import get_session
from motorgeek.core.models import Car, DataSource
from motorgeek.core.pipeline import IngestPipeline
from motorgeek.core.llm import LLMClient

app = typer.Typer(name="ingest")
console = Console()

@app.command("ingest")
def ingest(
    car_ref: str = typer.Argument(..., help="Car ID or slug"),
    dimension: str = typer.Option("auto", "--dimension", "-d", help="Dimension: auto, perf, eng, rel, etc."),
    source: str = typer.Option("", "--source", "-s", help="Source URL or site name"),
):
    """Ingest raw data for a car. Opens editor for pasting raw text."""
    session = get_session()
    car = _resolve_car(session, car_ref)
    if not car:
        console.print(f"[red]Car not found:[/red] {car_ref}")
        raise typer.Exit(1)

    console.print(f"[cyan]Ingesting data for[/cyan] {car.make} {car.model} ({car.generation or 'base'})")
    console.print("[yellow]Paste raw data below. Save and close editor when done.[/yellow]")

    import tempfile, subprocess, os
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".txt", delete=False) as tmp:
        tmp.write(f"# Paste raw data for {car.make} {car.model}\n# Lines starting with # are comments\n\n")
        tmp_path = tmp.name

    try:
        editor = os.environ.get("EDITOR", "notepad" if os.name == "nt" else "nano")
        subprocess.call([editor, tmp_path])
        with open(tmp_path) as f:
            raw_text = f.read()
    finally:
        os.unlink(tmp_path)

    comments_removed = "\n".join(
        line for line in raw_text.split("\n")
        if line.strip() and not line.strip().startswith("#")
    )

    if not comments_removed.strip():
        console.print("[red]No data entered. Aborting.[/red]")
        raise typer.Exit(1)

    dim_hint = None if dimension == "auto" else dimension
    pipeline = IngestPipeline(LLMClient())
    results = pipeline.run(comments_removed, car.id, dimension_hint=dim_hint)

    _display_review_table(car, results)

    console.print(f"\n[green]Data ingested successfully[/green]")
    ds = DataSource(
        car_id=car.id,
        url=source or "manual",
        site_name=source or "manual paste",
        raw_text=raw_text,
        parsed_at=None,
        dimension=", ".join(results.keys()),
    )
    session.add(ds)
    session.commit()


def _resolve_car(session: Session, car_ref: str) -> Car | None:
    if car_ref.isdigit():
        return session.query(Car).filter(Car.id == int(car_ref)).first()
    parts = car_ref.split("-")
    query = session.query(Car)
    for part in parts:
        query = query.filter(Car.make.ilike(f"%{part}%") | Car.model.ilike(f"%{part}%"))
    return query.first()


def _display_review_table(car: Car, results: dict):
    console.print(f"\n[bold cyan]{car.make} {car.model}[/bold cyan] - Ingest Review\n")
    for dim, fields in results.items():
        table = Table(title=f"Dimension: {dim}")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")
        table.add_column("Confidence", style="yellow")
        if isinstance(fields, dict):
            conf = fields.get("_confidence", {})
            for field, value in fields.items():
                if field == "_confidence":
                    continue
                conf_val = conf.get(field, "-") if isinstance(conf, dict) else "-"
                table.add_row(field, str(value) if value is not None else "(missing)", conf_val)
        console.print(table)
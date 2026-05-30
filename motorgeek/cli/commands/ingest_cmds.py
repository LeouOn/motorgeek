import os
import subprocess
import tempfile
import typer
from rich.console import Console
from rich.table import Table
from sqlalchemy.orm import Session

from motorgeek.core.database import get_session
from motorgeek.core.models import Car, DataSource, IngestSessions
from motorgeek.core.pipeline import IngestPipeline
from motorgeek.core.ingest import (
    create_session,
    get_session_by_id as get_ingest_session,
    list_sessions,
    process_session,
    respond_to_session,
    save_session,
)
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

    import tempfile
    import subprocess
    import os
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

    console.print("\n[green]Data ingested successfully[/green]")
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


# ── Agentic Ingest Commands ───────────────────────────────────────────────────

@app.command()
def paste():
    """Open an editor to paste raw car data, then run the agentic ingestion pipeline."""

    with tempfile.NamedTemporaryFile(mode="w+", suffix=".txt", delete=False) as tmp:
        tmp.write("# Paste raw car data from ZePerfs, KBB, Wikipedia, etc.\n")
        tmp.write("# Lines starting with # are comments\n\n")
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

    db = get_session()
    session_obj = create_session(db, comments_removed)
    console.print(f"[cyan]Session {session_obj.id} created. Running agentic pipeline…[/cyan]")

    try:
        process_session(db, session_obj.id)
        console.print("[green]Agent analyzed your data![/green]")
        _display_session_status(session_obj)
        console.print(f"\n[yellow]Review at:[/yellow] http://localhost:8765/ingest/{session_obj.id}")
        console.print("[yellow]Or run:[/yellow] motorgeek ingest status " + str(session_obj.id))
    except Exception as e:
        console.print(f"[red]Pipeline failed:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def status(session_id: int):
    """Show the status and parsed data for an ingest session."""
    db = get_session()
    session_obj = get_ingest_session(db, session_id)
    if not session_obj:
        console.print(f"[red]Session {session_id} not found[/red]")
        raise typer.Exit(1)
    _display_session_status(session_obj)


@app.command()
def respond(session_id: int, message: str):
    """Send a response to the agent's questions."""
    db = get_session()
    session_obj = get_ingest_session(db, session_id)
    if not session_obj:
        console.print(f"[red]Session {session_id} not found[/red]")
        raise typer.Exit(1)

    console.print(f"[cyan]Sending:[/cyan] {message}")
    try:
        respond_to_session(db, session_id, message)
        db.refresh(session_obj)
        _display_session_status(session_obj)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def save(session_id: int):
    """Save the enriched session data to the database."""
    db = get_session()
    session_obj = get_ingest_session(db, session_id)
    if not session_obj:
        console.print(f"[red]Session {session_id} not found[/red]")
        raise typer.Exit(1)

    try:
        car_id = save_session(db, session_id)
        console.print(f"[green]Saved![/green] Car ID: {car_id}")
        console.print(f"[cyan]View:[/cyan] http://localhost:8765/cars/{car_id}")
    except Exception as e:
        console.print(f"[red]Save failed:[/red] {e}")
        raise typer.Exit(1)


@app.command("list")
def list_cmd():
    """List all ingest sessions with their status."""
    db = get_session()
    sessions = list_sessions(db)
    if not sessions:
        console.print("[yellow]No ingest sessions yet. Run [cyan]motorgeek ingest paste[/cyan] to create one.[/yellow]")
        return

    table = Table(title="Ingest Sessions")
    table.add_column("ID", style="cyan")
    table.add_column("Status", style="yellow")
    table.add_column("Source", style="green")
    table.add_column("Car", style="blue")
    table.add_column("Updated")

    for s in sessions:
        car_label = f"Car #{s.car_id}" if s.car_id else "—"
        status_color = {"draft": "white", "processing": "yellow", "awaiting_response": "yellow",
                        "enriched": "green", "saved": "cyan", "discarded": "red"}.get(s.status, "white")
        table.add_row(
            str(s.id),
            f"[{status_color}]{s.status}[/{status_color}]",
            s.source_site or "—",
            car_label,
            s.updated_at.strftime("%Y-%m-%d %H:%M") if s.updated_at else "—",
        )

    console.print(table)


def _display_session_status(session_obj: IngestSessions):
    """Pretty-print a session's status, gaps, and questions."""
    status_color = {"draft": "white", "processing": "yellow", "awaiting_response": "yellow",
                    "enriched": "green", "saved": "cyan", "discarded": "red"}
    color = status_color.get(session_obj.status, "white")
    console.print(f"\n[bold]Session #{session_obj.id}[/bold] — [{color}]{session_obj.status}[/{color}]")

    if session_obj.source_site:
        console.print(f"Source: {session_obj.source_site}")
    if session_obj.source_url:
        console.print(f"URL: {session_obj.source_url}")

    gq = session_obj.gaps_and_questions or {}
    gaps = gq.get("gaps", [])
    if gaps:
        console.print(f"\n[bold yellow]Gaps ({len(gaps)}):[/bold yellow]")
        for g in gaps:
            console.print(f"  • {g}")

    conflicts = gq.get("conflicts", [])
    if conflicts:
        console.print(f"\n[bold red]Conflicts ({len(conflicts)}):[/bold red]")
        for c in conflicts:
            if isinstance(c, dict):
                console.print(f"  • {c.get('field', '?')}: {', '.join(str(v) for v in c.get('values', []))}")

    questions = gq.get("questions", [])
    if questions:
        console.print(f"\n[bold cyan]Agent Questions ({len(questions)}):[/bold cyan]")
        for i, q in enumerate(questions, 1):
            console.print(f"  {i}. {q}")
        if session_obj.status == "awaiting_response":
            console.print(f"\n[dim]Respond with:[/dim] motorgeek ingest respond {session_obj.id} \"<your answer>\"")
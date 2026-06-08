import typer
from rich.console import Console
from rich.table import Table
from sqlalchemy.orm import Session

from motorgeek.core.database import get_session
from motorgeek.core.models import Car, Reliability
from motorgeek.core.scoring import DIMENSIONS, WEIGHTS, compute_reliability_aggregate, recompute_aggregate, get_score_dict

app = typer.Typer(name="reliability")
console = Console()


@app.command("show")
def reliability_show(
    car_ref: str = typer.Argument(..., help="Car ID or slug"),
    dimensions: bool = typer.Option(False, "--dimensions", "-d", help="Show dimensional breakdown"),
):
    """Show reliability data for a car."""
    session = get_session()
    car = _resolve_car(session, car_ref)
    if not car:
        console.print(f"[red]Car not found:[/red] {car_ref}")
        raise typer.Exit(1)

    rel = session.query(Reliability).filter(Reliability.car_id == car.id).first()
    if not rel:
        console.print(f"[yellow]No reliability data for {car.make} {car.model}[/yellow]")
        raise typer.Exit(1)

    if not dimensions:
        score = rel.reliability_score
        if score is not None:
            console.print(f"{car.make} {car.model}: reliability {score}/100")
        else:
            console.print(f"{car.make} {car.model}: no overall reliability score")
        return

    scores = get_score_dict(rel)
    computed = compute_reliability_aggregate(scores)
    stored = rel.reliability_score

    table = Table(title=f"Reliability Dimensions - {car.make} {car.model} ({car.generation or 'base'})")
    table.add_column("Dimension", style="cyan")
    table.add_column("Score", justify="right")
    table.add_column("Weight", justify="right")
    table.add_column("Note")

    for dim in DIMENSIONS:
        score_val = scores.get(dim)
        score_str = f"{score_val:.1f}" if score_val is not None else "-"
        weight_str = f"{WEIGHTS[dim]:.0%}"
        notes = rel.score_notes or {}
        note_str = notes.get(dim, "")
        table.add_row(dim.capitalize(), score_str, weight_str, note_str)

    table.add_section()
    stored_str = f"{stored:.1f}" if stored is not None else "-"
    computed_str = f"{computed:.1f}" if computed is not None else "-"
    table.add_row("[bold]Overall (stored)[/bold]", f"[bold]{stored_str}[/bold]", "", "")
    table.add_row("[bold]Overall (computed)[/bold]", f"[bold]{computed_str}[/bold]", "", "")

    if stored is not None and computed is not None and abs(stored - computed) > 0.5:
        console.print(f"[yellow]Note: stored ({stored:.1f}) differs from computed ({computed:.1f})[/yellow]")

    console.print(table)


@app.command("score")
def reliability_score(
    car_ref: str = typer.Argument(..., help="Car ID or slug"),
    engine: float = typer.Option(None, "--engine", help="Engine score (0-100)"),
    transmission: float = typer.Option(None, "--transmission", help="Transmission score (0-100)"),
    chassis: float = typer.Option(None, "--chassis", help="Chassis score (0-100)"),
    electronics: float = typer.Option(None, "--electronics", help="Electronics score (0-100)"),
    ease_of_repair: float = typer.Option(None, "--ease-of-repair", help="Ease of repair score (0-100)"),
    note_engine: str = typer.Option(None, "--note-engine", help="Note for engine dimension"),
    note_transmission: str = typer.Option(None, "--note-transmission", help="Note for transmission dimension"),
    note_chassis: str = typer.Option(None, "--note-chassis", help="Note for chassis dimension"),
    note_electronics: str = typer.Option(None, "--note-electronics", help="Note for electronics dimension"),
    note_ease_of_repair: str = typer.Option(None, "--note-ease-of-repair", help="Note for ease_of_repair dimension"),
):
    """Set dimensional reliability scores for a car."""
    session = get_session()
    car = _resolve_car(session, car_ref)
    if not car:
        console.print(f"[red]Car not found:[/red] {car_ref}")
        raise typer.Exit(1)

    rel = session.query(Reliability).filter(Reliability.car_id == car.id).first()
    if not rel:
        rel = Reliability(car_id=car.id)
        session.add(rel)
        session.flush()

    dim_scores = {
        'engine': engine,
        'transmission': transmission,
        'chassis': chassis,
        'electronics': electronics,
        'ease_of_repair': ease_of_repair,
    }
    dim_notes = {
        'engine': note_engine,
        'transmission': note_transmission,
        'chassis': note_chassis,
        'electronics': note_electronics,
        'ease_of_repair': note_ease_of_repair,
    }

    updated = []
    for dim, val in dim_scores.items():
        if val is not None:
            setattr(rel, f'score_{dim}', val)
            updated.append(dim)

    notes = rel.score_notes or {}
    notes_changed = False
    for dim, note in dim_notes.items():
        if note is not None:
            notes[dim] = note
            notes_changed = True
    if notes_changed:
        rel.score_notes = notes

    if not updated and not notes_changed:
        console.print("[yellow]No scores or notes provided. Use --engine, --transmission, etc.[/yellow]")
        raise typer.Exit(1)

    new_score = recompute_aggregate(rel)
    session.commit()

    console.print(f"[green]Updated {car.make} {car.model}:[/green]")
    for dim in updated:
        console.print(f"  {dim}: {dim_scores[dim]:.1f}")
    if new_score is not None:
        console.print(f"  [bold]Aggregate: {new_score:.1f}/100[/bold]")
    else:
        console.print("  [yellow]Aggregate: need at least 3 dimensions[/yellow]")


@app.command("compare")
def reliability_compare(
    car_refs: list[str] = typer.Argument(..., help="2+ car IDs or slugs"),
):
    """Compare dimensional reliability scores across cars."""
    if len(car_refs) < 2:
        console.print("[red]Need at least 2 cars to compare[/red]")
        raise typer.Exit(1)

    session = get_session()
    cars_rels = []
    for ref in car_refs:
        car = _resolve_car(session, ref)
        if not car:
            console.print(f"[red]Car not found:[/red] {ref}")
            raise typer.Exit(1)
        rel = session.query(Reliability).filter(Reliability.car_id == car.id).first()
        cars_rels.append((car, rel))

    table = Table(title="Reliability Comparison")
    table.add_column("Dimension", style="cyan")
    table.add_column("Weight", justify="right")
    for car, _ in cars_rels:
        table.add_column(f"{car.make} {car.model}", justify="right")

    for dim in DIMENSIONS:
        row = [dim.capitalize(), f"{WEIGHTS[dim]:.0%}"]
        for car, rel in cars_rels:
            if rel is not None:
                val = getattr(rel, f'score_{dim}', None)
                row.append(f"{val:.1f}" if val is not None else "-")
            else:
                row.append("-")
        table.add_row(*row)

    table.add_section()
    row = ["[bold]Overall[/bold]", ""]
    for car, rel in cars_rels:
        if rel is not None and rel.reliability_score is not None:
            row.append(f"[bold]{rel.reliability_score:.1f}[/bold]")
        else:
            row.append("-")
    table.add_row(*row)

    console.print(table)

    # Weakest dimension per car
    console.print()
    for car, rel in cars_rels:
        if rel is None:
            console.print(f"  {car.make} {car.model}: no reliability data")
            continue
        scores = get_score_dict(rel)
        present = {k: v for k, v in scores.items() if v is not None}
        if not present:
            console.print(f"  {car.make} {car.model}: no dimensional scores")
            continue
        weakest_dim = min(present, key=present.get)
        console.print(f"  {car.make} {car.model}: weakest = {weakest_dim} ({present[weakest_dim]:.1f})")


def _resolve_car(session: Session, car_ref: str) -> Car | None:
    if car_ref.isdigit():
        return session.query(Car).filter(Car.id == int(car_ref)).first()
    parts = car_ref.split("-")
    query = session.query(Car)
    for part in parts:
        query = query.filter(Car.make.ilike(f"%{part}%") | Car.model.ilike(f"%{part}%"))
    return query.first()

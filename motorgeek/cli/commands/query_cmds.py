import typer
from rich.console import Console
from sqlalchemy.orm import Session

from motorgeek.core.database import get_session
from motorgeek.core.models import Car
from motorgeek.core.llm import LLMClient

app = typer.Typer(name="query")
console = Console()


@app.command("query")
def query_nl(
    question: str = typer.Argument(..., help="Natural language question about your car database"),
):
    """Ask a natural language question about your car database."""
    console.print(f"[cyan]Asking:[/cyan] {question}")

    session = get_session()
    all_cars = session.query(Car).all()

    if not all_cars:
        console.print("[yellow]No cars in database yet. Add some cars first.[/yellow]")
        raise typer.Exit(1)

    car_summary = "\n".join(
        f"- {c.make} {c.model} ({c.generation or 'base'}, {c.year_start}{f'-{c.year_end}' if c.year_end else ''})"
        for c in all_cars
    )

    llm = LLMClient()
    prompt = (
        f"You are a car database query assistant. The user has a database of {len(all_cars)} cars:\n"
        f"{car_summary}\n\n"
        f"User question: {question}\n\n"
        f"Translate this into a clear, friendly answer based on the cars above. "
        f"If the question requires specific data you don't have, say so honestly."
    )

    try:
        answer = llm.complete(prompt)
        console.print(f"\n{answer}")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
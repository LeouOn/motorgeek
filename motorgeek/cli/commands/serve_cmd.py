import typer
import uvicorn
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command("serve")
def serve(
    port: int = typer.Option(8765, "--port", "-p", help="Port to listen on"),
    host: str = typer.Option("127.0.0.1", "--host", "-h", help="Host to bind to"),
    reload: bool = typer.Option(False, "--reload", "-r", help="Enable auto-reload"),
):
    """Start the MotorGeek web application."""
    console.print(f"[cyan]Starting MotorGeek web server on http://{host}:{port}[/cyan]")
    uvicorn.run(
        "motorgeek.web.app:app",
        host=host,
        port=port,
        reload=reload,
    )
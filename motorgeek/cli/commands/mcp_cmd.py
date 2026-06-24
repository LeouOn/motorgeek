import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command("serve")
def mcp_serve():
    """Start the MotorGeek MCP server (stdio transport).

    Use this to connect Claude Desktop, OpenCode, or any MCP-compatible agent.
    The server exposes 16 tools for searching, comparing, and analyzing your car collection.

    Claude Desktop config snippet:
      {
        "mcpServers": {
          "motorgeek": {
            "command": "python",
            "args": ["-m", "motorgeek.mcp_server"],
            "cwd": "/path/to/motorgeek"
          }
        }
      }
    """
    from motorgeek.mcp_server import serve
    console.print("[cyan]Starting MotorGeek MCP server (stdio)...[/cyan]")
    console.print("[dim]Connect with Claude Desktop or OpenCode using the motorgeek MCP server.[/dim]")
    serve()

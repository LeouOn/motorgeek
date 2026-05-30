import typer
from motorgeek.core.database import init_db

init_db()

app = typer.Typer(name="motorgeek", help="Car analysis and comparison tool")

from motorgeek.cli.commands import car_cmds, ingest_cmds, query_cmds, calc_cmds, market_cmds, repair_cmds  # noqa: E402
from motorgeek.cli.commands.serve_cmd import serve  # noqa: E402

app.add_typer(car_cmds.app, name="car")
app.add_typer(ingest_cmds.app, name="ingest")
app.add_typer(query_cmds.app, name="query")
app.add_typer(calc_cmds.app, name="calc")
app.add_typer(market_cmds.app, name="market")
app.add_typer(repair_cmds.app, name="repair")

from motorgeek.cli.commands.compare_cmds import compare as compare_func, compare_group  # noqa: E402
app.command("compare")(compare_func)
app.command("compare-group")(compare_group)
app.command("serve")(serve)

if __name__ == "__main__":
    app()
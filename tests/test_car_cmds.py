from typer.testing import CliRunner
from motorgeek.cli.main import app

runner = CliRunner()

def test_car_list_empty():
    result = runner.invoke(app, ["car", "list"], prog_name="motorgeek")
    assert result.exit_code == 0
    assert "No cars in database" in result.output

def test_car_add():
    result = runner.invoke(app, ["car", "add", "Porsche", "911 Turbo", "--year-start", "1998", "--generation", "996"], prog_name="motorgeek")
    assert result.exit_code == 0
    assert "Created" in result.output
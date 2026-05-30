import os
import pytest
from typer.testing import CliRunner
from motorgeek.cli.main import app

runner = CliRunner()

@pytest.fixture(autouse=True)
def clean_db(tmp_path):
    """Use a fresh temp database for each test."""
    db_path = str(tmp_path / "test.db")
    os.environ["MOTORGEEK_DB_PATH"] = db_path
    # Reset the global DB connection
    import motorgeek.core.database as db
    db._engine = None
    db._SessionLocal = None
    db.init_db()
    yield
    db._engine = None
    db._SessionLocal = None

def test_car_list_empty():
    result = runner.invoke(app, ["car", "list"], prog_name="motorgeek")
    assert result.exit_code == 0
    assert "No cars in database" in result.output

def test_car_add():
    result = runner.invoke(app, ["car", "add", "Porsche", "911 Turbo", "--year-start", "1998", "--generation", "996"], prog_name="motorgeek")
    assert result.exit_code == 0
    assert "Created" in result.output
    assert "Porsche" in result.output
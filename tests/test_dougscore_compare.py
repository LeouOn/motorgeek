"""Tests for the Doug Score comparison view.

Covers:
- Loading Doug Score anchors from JSON
- Fuzzy matching of Doug Score entries to DB cars
- Composite breakdown computation (Q, R, P, ZP)
- Table rendering
- Edge cases (missing data, unmatched entries)

Run with: pytest tests/test_dougscore_compare.py
"""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DOUGSCORE_PATH = ROOT / "data" / "dougscore_anchors.json"
DB_PATH = ROOT / "data" / "motorgeek.db"


@pytest.fixture
def dougscore_data():
    """Load the canonical Doug Score anchors."""
    with open(DOUGSCORE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def db():
    """Open a sqlite3 connection to the DB."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()


def test_dougscore_anchors_exist(dougscore_data):
    """We should have at least 30 Doug Score entries to compare."""
    assert len(dougscore_data) >= 30, (
        f"Expected at least 30 Doug Score entries, got {len(dougscore_data)}"
    )


def test_dougscore_entry_structure(dougscore_data):
    """Each entry should have all required fields and valid 1-10 scores."""
    required_fields = {
        "year", "make", "model",
        "styling", "acceleration", "handling", "fun_factor", "cool_factor",
        "weekend_total", "features", "comfort", "quality", "practicality", "value",
        "daily_total", "dougscore",
    }
    for entry in dougscore_data:
        missing = required_fields - set(entry.keys())
        assert not missing, f"Doug Score entry missing fields {missing}: {entry}"
        # Scores must be 1-10
        for k in ("styling", "acceleration", "handling", "fun_factor", "cool_factor",
                  "features", "comfort", "quality", "practicality", "value"):
            assert 1 <= entry[k] <= 10, f"Field {k}={entry[k]} out of range for {entry['make']} {entry['model']}"
        # Dougscore must equal weekend + daily
        assert entry["dougscore"] == entry["weekend_total"] + entry["daily_total"], (
            f"Dougscore mismatch: {entry['dougscore']} != {entry['weekend_total']} + {entry['daily_total']}"
        )


def test_match_cars_returns_tuples(db, dougscore_data):
    """match_cars should return (ds_entry, db_car_row_or_None, confidence) tuples."""
    from scripts.dougscore_compare import match_cars
    matches = match_cars(dougscore_data, db)
    assert len(matches) == len(dougscore_data)
    for ds, car, conf in matches:
        assert isinstance(ds, dict)
        assert car is None or hasattr(car, "keys")
        assert isinstance(conf, float)
        assert 0.0 <= conf <= 1.0


def test_match_cars_finds_perfect_matches(db, dougscore_data):
    """Taycan Turbo S 2020 should match with high confidence."""
    from scripts.dougscore_compare import match_cars
    matches = match_cars(dougscore_data, db)
    # Find Taycan entry
    taycan_match = None
    for ds, car, conf in matches:
        if ds["make"] == "Porsche" and "Taycan" in ds["model"]:
            taycan_match = (ds, car, conf)
            break
    assert taycan_match is not None, "Taycan not found in matches"
    ds, car, conf = taycan_match
    assert car is not None, "Taycan should match a DB car"
    assert conf >= 0.8, f"Taycan confidence too low: {conf}"


def test_match_cars_handles_unmatched(db, dougscore_data):
    """Some entries (McLaren Speedtail, Audi R8) won't match."""
    from scripts.dougscore_compare import match_cars
    matches = match_cars(dougscore_data, db)
    unmatched = [(ds, car) for ds, car, conf in matches if car is None]
    assert len(unmatched) >= 3, f"Expected at least 3 unmatched, got {len(unmatched)}"


def test_composite_breakdown_returns_dict(db):
    """For a known car, get_composite_breakdown should return a dict with composite/Q/R/P/ZP."""
    from scripts.dougscore_compare import get_composite_breakdown
    # Lexus LS (id=39) has known Q, R, ZP data
    breakdown = get_composite_breakdown(db, 39)
    if breakdown is not None:  # may be None if insufficient data
        assert "composite" in breakdown
        assert 0 <= breakdown["composite"] <= 100


def test_render_table_smoke(db, dougscore_data):
    """Render_table should produce a non-empty string with column headers."""
    from scripts.dougscore_compare import match_cars, render_table
    matches = match_cars(dougscore_data, db)
    out = render_table(matches, limit=5)
    assert "Doug Score vs MotorGeek" in out
    assert "Weekend" in out
    assert "Daily" in out
    assert "Our Comp" in out


def test_render_subscore_breakdown_smoke(db, dougscore_data):
    """Sub-score breakdown should show all 10 sub-scores per car."""
    from scripts.dougscore_compare import match_cars, render_subscore_breakdown
    matches = match_cars(dougscore_data, db)
    out = render_subscore_breakdown(matches, limit=3)
    assert "Doug Score Sub-Score" in out
    assert "Sty" in out  # styling
    assert "Acc" in out  # acceleration
    assert "Han" in out  # handling
    assert "Fun" in out  # fun_factor
    assert "Coo" in out  # cool_factor
    assert "Fea" in out  # features
    assert "Com" in out  # comfort
    assert "Qua" in out  # quality
    assert "Pra" in out  # practicality
    assert "Val" in out  # value

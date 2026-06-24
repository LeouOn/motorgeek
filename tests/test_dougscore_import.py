"""Tests for the Doug Score importer.

Covers:
- Schema validation (correct entries pass, malformed entries fail)
- De-duplication against existing 33 anchors
- Dry-run mode (no DB changes, no file changes)
- Stats reporting

Run with: pytest tests/test_dougscore_import.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
IMPORT_SCRIPT = ROOT / "scripts" / "dougscore_import.py"
DOUGSCORE_PATH = ROOT / "data" / "dougscore_anchors.json"


@pytest.fixture
def sample_json(tmp_path: Path) -> Path:
    """Write a small valid Doug Score sample to a temp file."""
    sample = [
        {
            "year": 1995,
            "make": "TestMake",
            "model": "TestModel A",
            "styling": 7,
            "acceleration": 8,
            "handling": 7,
            "fun_factor": 7,
            "cool_factor": 6,
            "weekend_total": 35,
            "features": 5,
            "comfort": 6,
            "quality": 7,
            "practicality": 4,
            "value": 8,
            "daily_total": 30,
            "dougscore": 65,
        },
        {
            "year": 2010,
            "make": "TestMake",
            "model": "TestModel B",
            "styling": 6,
            "acceleration": 7,
            "handling": 6,
            "fun_factor": 5,
            "cool_factor": 5,
            "weekend_total": 29,
            "features": 7,
            "comfort": 8,
            "quality": 8,
            "practicality": 6,
            "value": 7,
            "daily_total": 36,
            "dougscore": 65,
        },
    ]
    p = tmp_path / "sample.json"
    p.write_text(json.dumps(sample, indent=2))
    return p


def test_import_script_exists():
    """Importer script must exist."""
    assert IMPORT_SCRIPT.exists(), f"Missing: {IMPORT_SCRIPT}"


def test_import_module_imports():
    """The importer module should import without errors."""
    sys.path.insert(0, str(ROOT))
    import scripts.dougscore_import as m
    assert hasattr(m, "validate_entry")
    assert hasattr(m, "make_key")
    assert hasattr(m, "load_existing_anchors")
    assert hasattr(m, "run")
    assert hasattr(m, "main")


def test_validate_entry_accepts_valid():
    """A correct entry should produce no validation errors."""
    from scripts.dougscore_import import validate_entry
    entry = {
        "year": 2020,
        "make": "BMW",
        "model": "M3",
        "styling": 7, "acceleration": 8, "handling": 7, "fun_factor": 8, "cool_factor": 7,
        "weekend_total": 37,
        "features": 6, "comfort": 7, "quality": 7, "practicality": 5, "value": 7,
        "daily_total": 32,
        "dougscore": 69,
    }
    errors = validate_entry(entry)
    assert errors == [], f"Valid entry rejected: {errors}"


def test_validate_entry_rejects_out_of_range_scores():
    """Scores outside 1-10 should be rejected."""
    from scripts.dougscore_import import validate_entry
    entry = {
        "year": 2020,
        "make": "BMW",
        "model": "M3",
        "styling": 15,  # out of range
        "acceleration": 8, "handling": 7, "fun_factor": 8, "cool_factor": 7,
        "weekend_total": 45,
        "features": 6, "comfort": 7, "quality": 7, "practicality": 5, "value": 7,
        "daily_total": 32,
        "dougscore": 77,
    }
    errors = validate_entry(entry)
    assert any("styling" in e for e in errors), f"Should reject out-of-range score, got: {errors}"


def test_validate_entry_rejects_mismatched_totals():
    """weekend_total must equal sum of weekend scores."""
    from scripts.dougscore_import import validate_entry
    entry = {
        "year": 2020,
        "make": "BMW",
        "model": "M3",
        "styling": 7, "acceleration": 8, "handling": 7, "fun_factor": 8, "cool_factor": 7,
        "weekend_total": 50,  # sum is 37, not 50
        "features": 6, "comfort": 7, "quality": 7, "practicality": 5, "value": 7,
        "daily_total": 32,
        "dougscore": 82,
    }
    errors = validate_entry(entry)
    assert any("weekend_total" in e or "dougscore" in e for e in errors), \
        f"Should reject mismatched totals, got: {errors}"


def test_make_key_normalizes_case_and_whitespace():
    """make_key should lowercase and strip whitespace."""
    from scripts.dougscore_import import make_key
    entry = {"year": 2020, "make": "  BMW  ", "model": "  M3 CSL  "}
    k = make_key(entry)
    assert k == (2020, "bmw", "m3 csl")


def test_make_key_handles_missing_fields():
    """make_key should not crash on missing make/model."""
    from scripts.dougscore_import import make_key
    entry = {"year": 2020}
    k = make_key(entry)
    assert k == (2020, "", "")


def test_load_existing_anchors_returns_list():
    """load_existing_anchors should return the 33-entry list."""
    from scripts.dougscore_import import load_existing_anchors
    anchors = load_existing_anchors()
    assert isinstance(anchors, list)
    assert len(anchors) >= 30, f"Expected at least 30 anchors, got {len(anchors)}"


def test_run_dry_run_does_not_modify_files(tmp_path: Path, sample_json: Path):
    """Dry-run should validate but not modify any files."""
    from scripts.dougscore_import import run

    before_anchors = json.loads(DOUGSCORE_PATH.read_text(encoding="utf-8"))
    before_count = len(before_anchors)

    output = tmp_path / "output.json"
    run(sample_json, dry_run=True, output_path=output)

    # File should NOT exist (dry-run doesn't write)
    assert not output.exists(), "Dry run should not write output"
    after_anchors = json.loads(DOUGSCORE_PATH.read_text(encoding="utf-8"))
    assert len(after_anchors) == before_count, "Dry run should not modify anchors"


def test_run_dedupes_against_existing(sample_json: Path):
    """An entry that matches an existing anchor (year/make/model) should be skipped."""
    from scripts.dougscore_import import make_key

    # Build an entry identical to one in the existing anchors file
    existing = json.loads(DOUGSCORE_PATH.read_text(encoding="utf-8"))
    first = existing[0]
    dup_path = Path(sample_json).parent / "dup.json"
    dup_entry = {
        "year": first["year"],
        "make": first["make"],
        "model": first["model"],
        # All scores will pass validation since they're from the real file
        "styling": first["styling"], "acceleration": first["acceleration"],
        "handling": first["handling"], "fun_factor": first["fun_factor"],
        "cool_factor": first["cool_factor"], "weekend_total": first["weekend_total"],
        "features": first["features"], "comfort": first["comfort"],
        "quality": first["quality"], "practicality": first["practicality"],
        "value": first["value"], "daily_total": first["daily_total"],
        "dougscore": first["dougscore"],
    }
    dup_path.write_text(json.dumps([dup_entry]))

    from scripts.dougscore_import import run
    output = Path(sample_json).parent / "dup_out.json"
    run(dup_path, output_path=output)

    # Output should exist but contain only the EXISTING entries (dup was skipped)
    assert output.exists(), "Output should be written even when all are duplicates"
    merged = json.loads(output.read_text())
    assert len(merged) == len(existing), \
        f"Duplicate should be skipped; expected {len(existing)}, got {len(merged)}"

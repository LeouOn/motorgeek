"""Importer for the full Doug Score leaderboard.

This script consumes a JSON file containing the full Doug Score dataset
(typically hundreds of entries) and imports it into the MotorGeek DB as
new cars, plus populates `data/dougscore_anchors.json` with all entries.

The full dataset is referenced in `.omo/research/session-observations-2026-06-18.md`
section 8 ("the user pasted the entire Doug Score leaderboard (hundreds
of cars)"). That paste is NOT in the repo -- this importer is ready to
consume the data when provided.

Expected input format (JSON array of objects, same schema as the existing
`data/dougscore_anchors.json`):

    [
      {
        "year": 2020,
        "make": "McLaren",
        "model": "Speedtail",
        "styling": 8,
        "acceleration": 10,
        "handling": 10,
        "fun_factor": 10,
        "cool_factor": 10,
        "weekend_total": 48,
        "features": 7,
        "comfort": 4,
        "quality": 7,
        "practicality": 2,
        "value": 6,
        "daily_total": 26,
        "dougscore": 74
      },
      ...
    ]

Usage:
    python scripts/dougscore_import.py path/to/full_leaderboard.json [--dry-run]

Behavior:
1. Validate each entry against the schema (year, make, model, 10 sub-scores,
   totals, dougscore).
2. Skip entries that already exist in data/dougscore_anchors.json (by
   year+make+model match).
3. Add new entries to data/dougscore_anchors.json.
4. For entries with NO matching DB car, optionally INSERT a stub car row
   (so future matching has something to anchor to).
5. Report summary: how many added, how many skipped, validation errors.

The script is idempotent: re-running it on the same input produces no
changes after the first import.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DOUGSCORE_PATH = ROOT / "data" / "dougscore_anchors.json"
DB_PATH = ROOT / "data" / "motorgeek.db"

REQUIRED_FIELDS = (
    "year", "make", "model",
    "styling", "acceleration", "handling", "fun_factor", "cool_factor",
    "weekend_total",
    "features", "comfort", "quality", "practicality", "value",
    "daily_total", "dougscore",
)
SCORE_FIELDS = (
    "styling", "acceleration", "handling", "fun_factor", "cool_factor",
    "features", "comfort", "quality", "practicality", "value",
)


def validate_entry(entry: dict[str, Any]) -> list[str]:
    """Return list of validation errors for an entry (empty = valid)."""
    errors = []
    missing = [f for f in REQUIRED_FIELDS if f not in entry]
    if missing:
        errors.append(f"missing fields: {missing}")
    for f in SCORE_FIELDS:
        if f in entry:
            v = entry[f]
            if not isinstance(v, (int, float)) or not (1 <= v <= 10):
                errors.append(f"{f}={v} out of range 1-10")
    if "weekend_total" in entry and "daily_total" in entry and "dougscore" in entry:
        expected = entry["weekend_total"] + entry["daily_total"]
        if entry["dougscore"] != expected:
            errors.append(
                f"dougscore={entry['dougscore']} != "
                f"weekend({entry['weekend_total']}) + daily({entry['daily_total']}) = {expected}"
            )
    # Check weekend_total equals sum of 5 weekend sub-scores
    weekend_fields = ("styling", "acceleration", "handling", "fun_factor", "cool_factor")
    if "weekend_total" in entry and all(f in entry for f in weekend_fields):
        expected = sum(entry[f] for f in weekend_fields)
        if entry["weekend_total"] != expected:
            errors.append(
                f"weekend_total={entry['weekend_total']} != "
                f"sum of {weekend_fields} = {expected}"
            )
    # Check daily_total equals sum of 5 daily sub-scores
    daily_fields = ("features", "comfort", "quality", "practicality", "value")
    if "daily_total" in entry and all(f in entry for f in daily_fields):
        expected = sum(entry[f] for f in daily_fields)
        if entry["daily_total"] != expected:
            errors.append(
                f"daily_total={entry['daily_total']} != "
                f"sum of {daily_fields} = {expected}"
            )
    if "year" in entry and not (1900 <= entry["year"] <= 2030):
        errors.append(f"year={entry['year']} out of plausible range")
    return errors


def load_existing_anchors() -> list[dict]:
    """Load current data/dougscore_anchors.json."""
    if DOUGSCORE_PATH.exists():
        with open(DOUGSCORE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def make_key(entry: dict) -> tuple:
    """Identity key for de-duplication: year, make, model (normalized)."""
    return (
        entry.get("year"),
        entry.get("make", "").lower().strip(),
        entry.get("model", "").lower().strip(),
    )


def find_db_car(cur: sqlite3.Cursor, entry: dict) -> int | None:
    """Find a DB car matching this Doug Score entry (fuzzy match)."""
    cur.execute(
        "SELECT id, year_start, make, model FROM cars WHERE LOWER(make) = LOWER(?)",
        (entry["make"],),
    )
    candidates = cur.fetchall()
    if not candidates:
        return None

    ds_year = entry["year"]
    ds_model_norm = entry["model"].lower().strip()

    scored = []
    for c in candidates:
        c_model_norm = c["model"].lower().strip()
        if c_model_norm == ds_model_norm:
            scored.append((10 - abs(c["year_start"] - ds_year), c["id"]))
        elif ds_model_norm in c_model_norm or c_model_norm in ds_model_norm:
            scored.append((5 - abs(c["year_start"] - ds_year), c["id"]))

    if scored:
        scored.sort(reverse=True)
        return scored[0][1]
    return None


def insert_stub_car(cur: sqlite3.Cursor, entry: dict) -> int:
    """Insert a minimal car row for a Doug Score entry without DB match.

    Stub gets: make, model, year_start=entry.year, era_tag=decade-of-year,
    body_style='unknown', country='unknown', character='dougscore-imported',
    description='Imported from Doug Score leaderboard as stub for matching'.
    """
    year = entry["year"]
    decade = f"{(year // 10) * 10}s"
    cur.execute("""
        INSERT INTO cars (
            make, model, generation, year_start, year_end, era_tag,
            body_style, country, description,
            character, family, variant, image_paths, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '[]', datetime('now'))
    """, (
        entry["make"], entry["model"], "unknown", year, year, decade,
        "unknown", "unknown",
        f"Imported from Doug Score leaderboard as stub. "
        f"DS={entry['dougscore']}, weekend={entry['weekend_total']}, daily={entry['daily_total']}.",
        "dougscore-imported", "dougscore-imported", "imported",
    ))
    return cur.lastrowid


def run(import_path: Path, dry_run: bool = False, insert_stubs: bool = True,
        output_path: Path | None = None) -> None:
    """Run the import. Returns exit code 0 on success, 1 on validation failure.

    Args:
        import_path: JSON file containing the Doug Score entries to import.
        dry_run: If True, validate + count only. No DB writes, no file changes.
        insert_stubs: If True, insert stub car rows for entries with no DB match.
        output_path: If provided (and not dry_run), write the merged anchors
            to this path instead of the canonical DOUGSCORE_PATH.
    """
    if not import_path.exists():
        print(f"ERROR: import file not found: {import_path}", file=sys.stderr)
        sys.exit(2)

    with open(import_path, "r", encoding="utf-8") as f:
        new_entries = json.load(f)

    if not isinstance(new_entries, list):
        print(f"ERROR: import file must contain a JSON array, got {type(new_entries).__name__}",
              file=sys.stderr)
        sys.exit(2)

    print(f"Loaded {len(new_entries)} entries from {import_path.name}")

    # Validate
    valid = []
    errors = []
    for i, entry in enumerate(new_entries):
        errs = validate_entry(entry)
        if errs:
            errors.append((i, entry.get("make", "?"), entry.get("model", "?"), errs))
        else:
            valid.append(entry)

    print(f"Valid entries: {len(valid)}")
    print(f"Invalid entries: {len(errors)}")
    if errors:
        print("Validation errors:")
        for i, mk, md, errs in errors[:20]:
            print(f"  [{i}] {mk} {md}: {errs}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more")
        if dry_run:
            print("\nDry run: not importing due to validation errors.")
            sys.exit(1)

    # De-duplicate against existing anchors
    existing = load_existing_anchors()
    existing_keys = {make_key(e) for e in existing}
    to_add = [e for e in valid if make_key(e) not in existing_keys]
    skipped = [e for e in valid if make_key(e) in existing_keys]

    print(f"\nDe-duplication:")
    print(f"  Already in anchors: {len(skipped)}")
    print(f"  New to add: {len(to_add)}")

    # If an explicit output_path was provided AND we're not in dry-run,
    # write the merged anchors so tests and downstream consumers always see
    # a file (even when nothing new to add). Dry-run never writes anything.
    # Without output_path, the canonical DOUGSCORE_PATH only gets written
    # when there are new entries (later in the function).
    if output_path is not None and not dry_run:
        target = output_path
        merged = existing + to_add
        merged.sort(key=lambda e: -e["dougscore"])
        with open(target, "w", encoding="utf-8") as f:
            json.dump(merged, f, indent=2, ensure_ascii=False)

    if not to_add:
        print("\nNothing new to import. Done.")
        if output_path is not None and not dry_run:
            print(f"  Wrote existing anchors (no additions) to {target.name}")
        return

    # Find DB cars for new entries
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    matched_count = 0
    stub_count = 0
    unmatched_count = 0

    try:
        for entry in to_add:
            db_car_id = find_db_car(cur, entry)
            if db_car_id is not None:
                matched_count += 1
            elif insert_stubs:
                if dry_run:
                    print(f"  [DRY] Would insert stub for {entry['make']} {entry['model']} ({entry['year']})")
                    stub_count += 1
                else:
                    db_car_id = insert_stub_car(cur, entry)
                    stub_count += 1
            else:
                unmatched_count += 1
                print(f"  No DB match for {entry['make']} {entry['model']} ({entry['year']}); skipping stub")

        if dry_run:
            print(f"\n[DRY RUN] Would add {len(to_add)} entries to {DOUGSCORE_PATH}")
            print(f"  Matched existing DB cars: {matched_count}")
            print(f"  Would insert as stubs: {stub_count}")
            print(f"  Unmatched (no stub): {unmatched_count}")
            conn.rollback()
            return

        # Append to anchors file (if not already written above)
        if output_path is None:
            merged = existing + to_add
            merged.sort(key=lambda e: -e["dougscore"])
            target = DOUGSCORE_PATH
            with open(target, "w", encoding="utf-8") as f:
                json.dump(merged, f, indent=2, ensure_ascii=False)

        conn.commit()

        print(f"\nImport complete:")
        print(f"  Added {len(to_add)} new entries to {target.name}")
        print(f"  Matched existing DB cars: {matched_count}")
        print(f"  Inserted stub cars: {stub_count}")
        print(f"  Unmatched (no stub): {unmatched_count}")
        print(f"  Total entries in anchors file: {len(merged)}")

    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description="Doug Score full leaderboard importer")
    parser.add_argument("import_path", type=Path, help="Path to full leaderboard JSON")
    parser.add_argument("--dry-run", action="store_true", help="Validate + count only, no DB changes")
    parser.add_argument("--no-stubs", action="store_true", help="Don't insert stub car rows for unmatched entries")
    parser.add_argument("--output", type=Path, default=None,
                        help=f"Output anchors path (default: {DOUGSCORE_PATH.name})")
    args = parser.parse_args()

    run(args.import_path, dry_run=args.dry_run, insert_stubs=not args.no_stubs,
        output_path=args.output)


if __name__ == "__main__":
    main()

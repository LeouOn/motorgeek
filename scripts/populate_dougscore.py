"""Populate cars.dougscore from data/dougscore_anchors.json.

Uses fuzzy matching (year + make + normalized model) to match each DB car
against Doug Score entries. Writes matched dougscore values to the new
cars.dougscore column added in alembic migration 2b9c3d4e5f6a.

Usage:
    python scripts/populate_dougscore.py
    python scripts/populate_dougscore.py --dry-run  # preview only
    python scripts/populate_dougscore.py --unmatch-report  # show unmatched
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "motorgeek.db"
ANCHORS_PATH = ROOT / "data" / "dougscore_anchors.json"


def _normalize_model(model: str) -> str:
    """Strip generation tags and trim words for fuzzy comparison."""
    s = model.lower()
    s = re.sub(r"\([^)]*\)", "", s).strip()  # remove "(E46)" etc.
    trim_words = (
        "coupe", "sedan", "convertible", "spider", "widebody", "long",
        "competition", "performance", "edition", "package",
    )
    for w in trim_words:
        s = re.sub(rf"\b{w}\b", "", s).strip()
    return re.sub(r"\s+", " ", s)


def _fuzzy_match_db(cur: sqlite3.Cursor, ds_entry: dict) -> int | None:
    """Find a DB car matching the Doug Score entry via (year, make, model)."""
    ds_make = ds_entry["make"].lower()
    ds_model_norm = _normalize_model(ds_entry["model"])
    ds_year = ds_entry["year"]
    cur.execute(
        "SELECT id, year_start, make, model FROM cars WHERE LOWER(make) = ?",
        (ds_make,),
    )
    candidates = cur.fetchall()
    scored = []
    for c in candidates:
        c_model_norm = _normalize_model(c["model"])
        if c_model_norm == ds_model_norm:
            yr_diff = abs(c["year_start"] - ds_year)
            scored.append((10 - yr_diff, c["id"]))
        elif ds_model_norm in c_model_norm or c_model_norm in ds_model_norm:
            yr_diff = abs(c["year_start"] - ds_year)
            scored.append((5 - yr_diff, c["id"]))
    if scored:
        scored.sort(reverse=True)
        return scored[0][1]
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Populate cars.dougscore")
    parser.add_argument("--dry-run", action="store_true", help="Preview only, no writes")
    parser.add_argument("--unmatch-report", action="store_true",
                        help="List Doug Score entries that didn't match a DB car")
    args = parser.parse_args()

    with open(ANCHORS_PATH, "r", encoding="utf-8") as f:
        dougscore_list = json.load(f)
    print(f"Loaded {len(dougscore_list)} Doug Score entries from {ANCHORS_PATH.name}")

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    matched = 0
    unmatched = []
    updates = []  # (car_id, dougscore) pairs to apply

    for ds in dougscore_list:
        car_id = _fuzzy_match_db(cur, ds)
        if car_id is not None:
            updates.append((car_id, ds["dougscore"]))
            matched += 1
        else:
            unmatched.append(ds)

    print(f"Matched: {matched}/{len(dougscore_list)}")
    print(f"Unmatched: {len(unmatched)}")

    if args.unmatch_report and unmatched:
        print("\nUnmatched Doug Score entries (not in DB):")
        for ds in unmatched[:20]:
            print(f"  {ds['year']} {ds['make']} {ds['model']}")
        if len(unmatched) > 20:
            print(f"  ... and {len(unmatched) - 20} more")

    if args.dry_run:
        print("\n[DRY RUN] No writes applied.")
        conn.close()
        return 0

    # Apply updates (idempotent: skip duplicates)
    cur.execute("SELECT id, dougscore FROM cars WHERE dougscore IS NOT NULL")
    already_set = {row["id"]: row["dougscore"] for row in cur.fetchall()}

    new_writes = 0
    skipped_conflicts = 0
    for car_id, ds_value in updates:
        if car_id in already_set:
            if already_set[car_id] == ds_value:
                continue  # already correctly set, skip
            skipped_conflicts += 1
            print(f"  CONFLICT car_id={car_id}: existing={already_set[car_id]}, new={ds_value}")
            continue
        cur.execute("UPDATE cars SET dougscore = ? WHERE id = ?", (ds_value, car_id))
        new_writes += 1

    conn.commit()
    print(f"\nWrote {new_writes} dougscore values to cars table")
    if skipped_conflicts:
        print(f"Skipped {skipped_conflicts} conflicts (existing values didn't match new)")

    # Verify
    cur.execute("SELECT COUNT(*) FROM cars WHERE dougscore IS NOT NULL")
    print(f"Total cars with dougscore now: {cur.fetchone()[0]} / 215")

    conn.close()
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())

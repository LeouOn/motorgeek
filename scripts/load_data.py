#!/usr/bin/env python3
"""Load MotorGeek DB from a JSON seed file.

Usage:
    python scripts/load_data.py                  # loads from data/seed_data.json
    python scripts/load_data.py --input my.json  # custom input path

Run AFTER seed_data.py (which creates tables). This fills in the data.
"""
import json
import os
import sqlite3
import argparse
from pathlib import Path

DEFAULT_INPUT = Path(__file__).parent.parent / "data" / "seed_data.json"

CAR_TABLES = [
    "cars",
    "performance",
    "powertrain_ice",
    "reliability",
    "market_history",
    "cost_to_own",
    "dimensions",
    "performance_measurements",
    "electronics",
    "consumables_and_specs",
    "zeperfs_indices",
    "car_reviews",
    "ingest_sessions",
]


def get_db_path() -> Path:
    env = os.environ.get("MOTORGEEK_DB_PATH")
    if env:
        return Path(env)
    cfg = Path("config.yaml")
    if cfg.exists():
        import yaml
        with open(cfg) as f:
            config = yaml.safe_load(f)
        return Path(config.get("database", {}).get("path", "data/motorgeek.db"))
    return Path("data/motorgeek.db")


def clear_table(conn: sqlite3.Connection, table: str):
    try:
        conn.execute(f"DELETE FROM {table}")
    except sqlite3.OperationalError:
        pass


def load(input_path: Path, db_path: Path, clear: bool = True):
    if not input_path.exists():
        print(f"Seed file not found: {input_path}")
        print("Run 'python scripts/dump_data.py' first to create the seed file.")
        return

    if not db_path.exists():
        print(f"Database not found: {db_path}")
        print("Run 'python seed_data.py' first to create the database schema.")
        return

    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)

    conn = sqlite3.connect(db_path)
    loaded = 0

    for table in CAR_TABLES:
        if table not in data:
            continue
        rows = data[table]
        if not rows:
            continue

        if clear:
            clear_table(conn, table)

        # Get column names from first row
        cols = list(rows[0].keys())
        placeholders = ", ".join(["?" for _ in cols])
        col_names = ", ".join(cols)

        for row in rows:
            vals = [row.get(c) for c in cols]
            # Convert None strings back to None
            vals = [None if v == "None" or v == "NULL" else v for v in vals]
            try:
                conn.execute(
                    f"INSERT INTO {table} ({col_names}) VALUES ({placeholders})",
                    vals,
                )
                loaded += 1
            except Exception as e:
                print(f"  Warning: could not insert row in {table}: {e}")

        print(f"  {table}: {len(rows)} rows")

    conn.commit()
    conn.close()
    print(f"\nLoaded {loaded} rows into {db_path}")


def main():
    parser = argparse.ArgumentParser(description="Load MotorGeek DB from JSON seed file")
    parser.add_argument("--input", "-i", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--db", type=Path, default=None)
    parser.add_argument(
        "--no-clear",
        action="store_true",
        help="Append instead of replacing existing data",
    )
    args = parser.parse_args()

    db_path = args.db or get_db_path()
    load(args.input, db_path, clear=not args.no_clear)


if __name__ == "__main__":
    main()

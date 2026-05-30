#!/usr/bin/env python3
"""Dump the current MotorGeek database to a JSON seed file.

Usage:
    python scripts/dump_data.py                  # dumps to data/seed_data.json
    python scripts/dump_data.py --output my.json  # custom output path

The output file is git-friendly and can be committed.
"""
import json
import os
import sqlite3
import argparse
from pathlib import Path

DEFAULT_OUTPUT = Path(__file__).parent.parent / "data" / "seed_data.json"

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


def dump_table(conn: sqlite3.Connection, table: str) -> list[dict]:
    try:
        cursor = conn.execute(f"SELECT * FROM {table}")
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]
    except sqlite3.OperationalError:
        return []


def dump(db_path: Path, output: Path):
    if not db_path.exists():
        print(f"Database not found: {db_path}")
        print("Run 'python seed_data.py' first to create and seed the database.")
        return

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    data = {}
    for table in CAR_TABLES:
        rows = dump_table(conn, table)
        data[table] = rows
        print(f"  {table}: {len(rows)} rows")

    conn.close()

    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)

    print(f"\nDumped to {output}")
    print("Commit this file to preserve your data across clones/pushes.")


def main():
    parser = argparse.ArgumentParser(description="Dump MotorGeek DB to JSON seed file")
    parser.add_argument("--output", "-o", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--db", type=Path, default=None)
    args = parser.parse_args()

    db_path = args.db or get_db_path()
    dump(db_path, args.output)


if __name__ == "__main__":
    main()

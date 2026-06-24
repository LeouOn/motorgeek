"""Extract score_notes from the SQL dump and restore to live DB.
The dump (data/motorgeek_dump.sql, 11:14 AM today) predates the JSON corruption
fix. It contains the original prose notes that were NULLed out.
"""
import re
import sqlite3
import json

DUMP_PATH = r"data\motorgeek_dump.sql"
DB_PATH = "data/motorgeek.db"

# Parse all INSERT INTO reliability statements from the dump
# The score_notes column is the 17th (last before PRIMARY KEY) value
# Schema order: id, car_id, source, reliability_score, common_failures,
#   avg_repair_cost, recall_count, part_availability, diy_friendliness,
#   known_issues, extra, score_engine, score_transmission, score_chassis,
#   score_electronics, score_ease_of_repair, score_notes

with open(DUMP_PATH, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find reliability INSERTs and extract score_notes (17th column)
# We need to carefully parse SQL values, handling quoted strings with commas
recovery = {}  # car_id -> original score_notes value

for line in lines:
    if not line.startswith("INSERT INTO reliability VALUES"):
        continue
    # Extract the VALUES(...) part
    match = re.match(r"INSERT INTO reliability VALUES\((.+)\);$", line.strip())
    if not match:
        continue
    values_str = match.group(1)

    # Parse values carefully - we need the 17th field (score_notes)
    # SQL value parser: handles single-quoted strings with escaped quotes (''),
    # and unquoted numbers/NULL
    fields = []
    i = 0
    while i < len(values_str):
        # Skip whitespace
        while i < len(values_str) and values_str[i] in (" ", "\t"):
            i += 1
        if i >= len(values_str):
            break

        if values_str[i] == "'":
            # Quoted string - find matching close quote (handle '' escapes)
            i += 1
            start = i
            buf = []
            while i < len(values_str):
                if values_str[i] == "'" and i + 1 < len(values_str) and values_str[i+1] == "'":
                    buf.append("'")
                    i += 2
                elif values_str[i] == "'":
                    i += 1
                    break
                else:
                    buf.append(values_str[i])
                    i += 1
            fields.append(("string", "".join(buf)))
        else:
            # Unquoted value (number, NULL, etc)
            start = i
            while i < len(values_str) and values_str[i] != ",":
                i += 1
            val = values_str[start:i].strip()
            if val.upper() == "NULL":
                fields.append(("null", None))
            else:
                fields.append(("number", val))

        # Skip comma
        while i < len(values_str) and values_str[i] in (",", " ", "\t"):
            i += 1

    if len(fields) < 17:
        continue

    car_id = int(fields[1][1])  # 2nd column
    score_notes_raw = fields[16][1]  # 17th column (0-indexed = 16)

    if score_notes_raw is None:
        continue  # was NULL in dump too

    recovery[car_id] = score_notes_raw

print(f"Found {len(recovery)} car_ids with non-NULL score_notes in dump")

# Now check live DB: which of these are currently NULL?
con = sqlite3.connect(DB_PATH)
con.row_factory = sqlite3.Row

currently_null = []
currently_valid = []
currently_different = []

for car_id, dump_value in recovery.items():
    row = con.execute("SELECT score_notes FROM reliability WHERE car_id = ?", (car_id,)).fetchone()
    if row is None:
        continue  # no reliability row for this car
    live_value = row["score_notes"]
    if live_value is None:
        currently_null.append((car_id, dump_value))
    elif live_value == dump_value:
        currently_valid.append((car_id, dump_value))
    else:
        currently_different.append((car_id, live_value, dump_value))

print(f"\nBreakdown:")
print(f"  Currently NULL in live DB (recoverable):     {len(currently_null)}")
print(f"  Currently matches dump (no action needed):    {len(currently_valid)}")
print(f"  Currently different from dump (investigate):  {len(currently_different)}")

# Show samples of what we'd restore
print(f"\n--- Sample recoverable rows (first 5) ---")
for car_id, dump_val in currently_null[:5]:
    car = con.execute("SELECT make, model, generation FROM cars WHERE id = ?", (car_id,)).fetchone()
    if car:
        car_name = f"{car['make']} {car['model']} ({car['generation']})"
    else:
        car_name = f"car_id={car_id}"
    preview = dump_val[:100] + "..." if len(dump_val) > 100 else dump_val
    print(f"  car_id={car_id:>3} {car_name:45} notes: {preview}")

# Determine recovery strategy: is the dump value valid JSON or prose?
valid_json_count = 0
prose_count = 0
for car_id, dump_val in currently_null:
    try:
        json.loads(dump_val)
        valid_json_count += 1
    except (json.JSONDecodeError, TypeError):
        prose_count += 1

print(f"\nOf {len(currently_null)} recoverable rows:")
print(f"  Valid JSON in dump:    {valid_json_count}")
print(f"  Raw prose in dump:     {prose_count}")

# Recovery plan:
# - Valid JSON values: restore as-is
# - Raw prose values: wrap as {"_legacy_note": "prose text"} to preserve as valid JSON
to_restore = []
for car_id, dump_val in currently_null:
    try:
        json.loads(dump_val)
        to_restore.append((car_id, dump_val))  # valid JSON, restore as-is
    except (json.JSONDecodeError, TypeError):
        # Wrap prose as valid JSON to prevent future corruption
        wrapped = json.dumps({"_legacy_note": dump_val})
        to_restore.append((car_id, wrapped))

print(f"\nPrepared {len(to_restore)} rows for restore")
print(f"  Restoring as valid JSON (was already JSON): {valid_json_count}")
print(f"  Wrapping prose as {{'_legacy_note': '...'}}: {prose_count}")

# APPLY
print(f"\nApplying restore...")
for car_id, notes_json in to_restore:
    con.execute("UPDATE reliability SET score_notes = ? WHERE car_id = ?", (notes_json, car_id))
con.commit()
print(f"Restored score_notes for {len(to_restore)} cars")

# Verify
n_with = con.execute("SELECT COUNT(*) FROM reliability WHERE score_notes IS NOT NULL").fetchone()[0]
n_total = con.execute("SELECT COUNT(*) FROM reliability").fetchone()[0]
print(f"\nFinal state: {n_with} of {n_total} reliability rows have score_notes")

# Quick sanity: load via ORM
import subprocess
result = subprocess.run(
    ["python", "-c",
     "from motorgeek.core.database import get_session; from motorgeek.core.models import Reliability; s=get_session(); rows=s.query(Reliability).all(); print(f'ORM loaded {len(rows)} reliability rows OK')"],
    capture_output=True, text=True, cwd="."
)
print(f"\nORM verification: {result.stdout.strip()}")
if result.returncode != 0:
    print(f"STDERR: {result.stderr.strip()[:200]}")

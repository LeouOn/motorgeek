"""Parse the user-pasted Doug Score leaderboard (tab-separated text) into
structured entries that match the Doug Score JSON schema.

Input format (from dougdemuro.com/dougscore as a TSV):
    Year  Make  Model  Styling  Acceleration  Handling  Fun Factor  Cool Factor
    WEEKEND_TOTAL  Features  Comfort  Quality  Practicality  Value
    DAILY_TOTAL  DOUGSCORE  Video_Time  Filming_Location  Country

Output: list of dicts matching the schema in data/dougscore_anchors.json.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def parse_paste(text: str) -> list[dict]:
    """Parse tab-separated Doug Score paste into structured entries.

    Handles multi-line rows where filming_location can wrap to the next line.
    Splits on tab characters; rows are detected by having a 4-digit year at
    the start.
    """
    # Normalize: split into lines, then merge lines that are continuations
    # of the previous row (no leading year).
    raw_lines = text.splitlines()
    rows = []
    current_row: list[str] = []

    for line in raw_lines:
        line = line.strip()
        if not line:
            continue
        # A new row starts with a 4-digit year (1900-2030)
        if re.match(r"^(19|20)\d{2}\s", line):
            if current_row:
                rows.append(current_row)
            current_row = [line]
        else:
            # Continuation of the previous row (filming_location wrapped)
            if current_row:
                current_row.append(line)
            # else: stray continuation, skip
    if current_row:
        rows.append(current_row)

    entries = []
    for row in rows:
        # Join all parts with tab to handle continuations
        full = "\t".join(row)
        cells = full.split("\t")
        # Strip each cell
        cells = [c.strip() for c in cells if c.strip()]
        if len(cells) < 17:
            # Malformed row
            continue
        try:
            year = int(cells[0])
            make = cells[1]
            model = cells[2]
            styling = int(cells[3])
            acceleration = int(cells[4])
            handling = int(cells[5])
            fun_factor = int(cells[6])
            cool_factor = int(cells[7])
            weekend_total = int(cells[8])
            features = int(cells[9])
            comfort = int(cells[10])
            quality = int(cells[11])
            practicality = int(cells[12])
            value = int(cells[13])
            daily_total = int(cells[14])
            dougscore = int(cells[15])
        except (ValueError, IndexError):
            continue

        entry = {
            "year": year,
            "make": make,
            "model": model,
            "styling": styling,
            "acceleration": acceleration,
            "handling": handling,
            "fun_factor": fun_factor,
            "cool_factor": cool_factor,
            "weekend_total": weekend_total,
            "features": features,
            "comfort": comfort,
            "quality": quality,
            "practicality": practicality,
            "value": value,
            "daily_total": daily_total,
            "dougscore": dougscore,
        }
        # Optional: video_link (cell 16), filming_location (cell 17+),
        # country (last cell). We don't store these but could.
        entries.append(entry)

    return entries


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/parse_dougscore_paste.py <input_file>")
        print("Reads tab-separated Doug Score paste and writes JSON to data/dougscore_combined.json")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"ERROR: file not found: {input_path}")
        sys.exit(1)

    text = input_path.read_text(encoding="utf-8")
    entries = parse_paste(text)
    print(f"Parsed {len(entries)} entries from {input_path.name}")

    # Validation stats
    valid = 0
    invalid = 0
    for e in entries:
        try:
            if not (1 <= e["styling"] <= 10):
                continue
            if e["weekend_total"] != e["styling"] + e["acceleration"] + e["handling"] + e["fun_factor"] + e["cool_factor"]:
                continue
            if e["daily_total"] != e["features"] + e["comfort"] + e["quality"] + e["practicality"] + e["value"]:
                continue
            if e["dougscore"] != e["weekend_total"] + e["daily_total"]:
                continue
            if not (1900 <= e["year"] <= 2030):
                continue
            valid += 1
        except (KeyError, TypeError):
            invalid += 1

    print(f"Valid entries: {valid}")
    print(f"Invalid entries: {invalid}")

    # Write combined JSON
    output_path = ROOT / "data" / "dougscore_combined.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(entries)} entries to {output_path}")

    # Stats
    makes = sorted(set(e["make"] for e in entries))
    years = sorted(e["year"] for e in entries)
    print(f"Distinct makes: {len(makes)}")
    print(f"Year range: {years[0]} - {years[-1]}")
    print(f"Makes: {', '.join(makes)}")


if __name__ == "__main__":
    main()

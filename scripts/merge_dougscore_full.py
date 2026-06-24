"""Merge the parsed Doug Score full leaderboard with existing anchors.

Reads:
  - data/dougscore_combined.json (parsed from paste, 585 entries)
  - data/dougscore_anchors.json (existing 33 entries)

Writes:
  - data/dougscore_anchors.json (merged, deduplicated by year+make+model)
  - data/dougscore_combined.json (same content, kept for reference)

Stats:
  - total entries after merge
  - new entries added
  - duplicates skipped
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANCHORS_PATH = ROOT / "data" / "dougscore_anchors.json"
COMBINED_PATH = ROOT / "data" / "dougscore_combined.json"


def main() -> int:
    if not COMBINED_PATH.exists():
        print(f"ERROR: {COMBINED_PATH} not found. Run scripts/parse_dougscore_paste.py first.")
        return 1

    # Load both
    with open(COMBINED_PATH, "r", encoding="utf-8") as f:
        full = json.load(f)
    with open(ANCHORS_PATH, "r", encoding="utf-8") as f:
        existing = json.load(f)

    # Build set of existing keys (year, make.lower(), model.lower())
    def key_of(entry: dict) -> tuple:
        return (
            entry["year"],
            entry["make"].lower().strip(),
            entry["model"].lower().strip(),
        )

    existing_keys = {key_of(e) for e in existing}

    # Find new entries
    new_entries = []
    duplicates = 0
    for e in full:
        if key_of(e) in existing_keys:
            duplicates += 1
            continue
        # Normalize make to merge "Mercedes-Benz" / "Mercedes - Benz" / "Mercedes - Maybach" / "Mercedes-Maybach" / "Mercedes"
        # We keep them as-is (each is a unique make) but normalize whitespace in make
        e["make"] = " ".join(e["make"].split())
        e["model"] = " ".join(e["model"].split())
        if key_of(e) not in existing_keys:
            existing_keys.add(key_of(e))
            new_entries.append(e)

    # Merge: existing first (curated), then new
    merged = existing + new_entries

    # Sort by dougscore descending for readability
    merged.sort(key=lambda e: (-e["dougscore"], e["year"]))

    # Write
    with open(ANCHORS_PATH, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)

    print(f"Merged into {ANCHORS_PATH.name}")
    print(f"  Existing: {len(existing)}")
    print(f"  In parsed full leaderboard: {len(full)}")
    print(f"  Duplicates skipped: {duplicates}")
    print(f"  New entries added: {len(new_entries)}")
    print(f"  Total anchors: {len(merged)}")

    # Make breakdown
    makes = sorted(set(e["make"] for e in merged))
    print(f"\nDistinct makes: {len(makes)}")
    print(f"Year range: {min(e['year'] for e in merged)} - {max(e['year'] for e in merged)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Merge the parsed Doug Score entries (data/dougscore_combined.json) with
the existing canonical anchors (data/dougscore_anchors.json), deduplicating
on (year, make, model).

Outputs:
- data/dougscore_anchors.json -- updated with all merged entries
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    anchors_path = ROOT / "data" / "dougscore_anchors.json"
    combined_path = ROOT / "data" / "dougscore_combined.json"

    # Load existing anchors (canonical)
    with open(anchors_path, "r", encoding="utf-8") as f:
        anchors = json.load(f)

    # Load combined (parsed paste)
    with open(combined_path, "r", encoding="utf-8") as f:
        combined = json.load(f)

    # Build dedup index from existing anchors
    def key(e):
        return (e["year"], e["make"].lower().strip(), e["model"].lower().strip())

    seen = {key(e) for e in anchors}

    added = 0
    duplicates = 0
    for entry in combined:
        k = key(entry)
        if k in seen:
            duplicates += 1
            continue
        # Adopt the entry (paste is canonical source)
        anchors.append(entry)
        seen.add(k)
        added += 1

    # Sort by dougscore descending for readability
    anchors.sort(key=lambda e: (-e["dougscore"], e["year"]))

    # Write back
    with open(anchors_path, "w", encoding="utf-8") as f:
        json.dump(anchors, f, indent=2, ensure_ascii=False)

    print(f"Existing anchors: {len(anchors) - added}")
    print(f"New entries added: {added}")
    print(f"Duplicates skipped: {duplicates}")
    print(f"Total entries in anchors: {len(anchors)}")
    print(f"Wrote updated {anchors_path.name}")


if __name__ == "__main__":
    main()

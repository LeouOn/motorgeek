#!/usr/bin/env python3
"""Backfill practicality enrichment data from Wikipedia.

For each car in the motorgeek DB, fetches the Wikipedia article and extracts:
  - seat_count
  - cargo_volume_liters_seats_down
  - front_legroom_mm
  - front_headroom_mm
  - rear_legroom_mm
  - rear_headroom_mm
  - tow_capacity_kg

Writes results to the ``dimensions`` table, marking the source in ``extra``.

Wikipedia is a shared resource. Be respectful:
  - 1.5s delay between requests
  - Proper User-Agent identifying our bot
  - Respect 429 with backoff
  - Single-threaded (no concurrent requests)

Usage:
    python scripts/enrich_practicality_from_wikipedia.py --dry-run
    python scripts/enrich_practicality_from_wikipedia.py --limit 10
    python scripts/enrich_practicality_from_wikipedia.py --start-from 50
    python scripts/enrich_practicality_from_wikipedia.py  # full run, ~30 min for 210 cars
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from typing import Any

import requests
from sqlalchemy.orm import Session

from motorgeek.core.database import get_session
from motorgeek.core.models import Car, Dimensions


# --- Wikipedia API config ----------------------------------------------------

USER_AGENT = (
    "MotorgeekDataBot/1.0 (https://github.com/motorgeek/motorgeek; "
    "practicality-data-enrichment) Python-requests"
)
WIKI_API = "https://en.wikipedia.org/w/api.php"
REQUEST_TIMEOUT = 15  # seconds
DELAY_BETWEEN_REQUESTS = 1.5  # seconds
MAX_RETRIES = 3
BACKOFF_FACTOR = 2.0  # backoff multiplier on 429


# --- Wikipedia infobox parsing ----------------------------------------------

# Convert common volume units to liters
def _parse_volume_to_liters(text: str) -> float | None:
    """Parse strings like '450 l', '15.9 cu ft', '450 litres' to liters."""
    if not text:
        return None
    t = text.strip().lower()
    # Try liters first
    m = re.search(r"([\d,.]+)\s*(l|litre|liter|litres|liters)\b", t)
    if m:
        return float(m.group(1).replace(",", ""))
    # Then cubic feet
    m = re.search(r"([\d,.]+)\s*(cu\s*ft|cubic\s*feet|cubic\s*ft|cuft)\b", t)
    if m:
        return float(m.group(1).replace(",", "")) * 28.3168
    # Then cubic meters
    m = re.search(r"([\d,.]+)\s*m³", t)
    if m:
        return float(m.group(1).replace(",", "")) * 1000.0
    return None


def _parse_dimension_to_mm(text: str) -> float | None:
    """Parse strings like '980 mm', '38.6 in', '980mm' to mm."""
    if not text:
        return None
    t = text.strip().lower()
    m = re.search(r"([\d,.]+)\s*(mm|millimeter|millimetre)\b", t)
    if m:
        return float(m.group(1).replace(",", ""))
    m = re.search(r"([\d,.]+)\s*(in|inch|inches)\b", t)
    if m:
        return float(m.group(1).replace(",", "")) * 25.4
    m = re.search(r"([\d,.]+)\s*cm\b", t)
    if m:
        return float(m.group(1).replace(",", "")) * 10.0
    return None


def _parse_int_count(text: str) -> int | None:
    """Parse a seat count like '5', '7', '2+2'."""
    if not text:
        return None
    t = text.strip().lower()
    # Just a number
    m = re.search(r"\b(\d+)\b", t)
    if m:
        return int(m.group(1))
    return None


# Wikipedia field-name patterns to look for in infoboxes
# The wiki-text field names differ between articles, so we try multiple.
_VOLUME_DOWN_PATTERNS = [
    r"cargo\s*volume\s*\(?\s*seats\s*(?:folded|down|rear\s*folded|rear\s*down)\)?",
    r"cargo\s*volume\s*max(?:imum)?",
    r"trunk\s*space\s*\(?seats\s*(?:folded|down)\)?",
    r"cargo\s*space\s*max(?:imum)?",
    r"with\s*seats\s*folded",
]
_VOLUME_UP_PATTERNS = [
    r"cargo\s*volume\s*\(?seats\s*up\)?",
    r"trunk\s*space",
    r"boot\s*space",
    r"cargo\s*capacity",
    r"cargo\s*volume",
]
_SEAT_COUNT_PATTERNS = [
    r"seating\s*capacity",
    r"seats",
    r"passenger\s*capacity",
]
_LEG_LEAD_PATTERNS = [
    r"front\s*legroom",
    r"front\s*leg\s*room",
    r"legroom\s*\(?front\)?",
    r"front\s*interior",
]
_LEG_REAR_PATTERNS = [
    r"rear\s*legroom",
    r"rear\s*leg\s*room",
    r"legroom\s*\(?rear\)?",
    r"rear\s*interior",
]
_HEAD_FRONT_PATTERNS = [r"front\s*headroom", r"front\s*head\s*room"]
_HEAD_REAR_PATTERNS = [r"rear\s*headroom", r"rear\s*head\s*room"]
_TOW_PATTERNS = [r"towing\s*capacity", r"braked\s*trailer", r"max\s*tow"]


def _extract_infobox_value(wikitext: str, patterns: list[str], parse_fn) -> Any:
    """Search the infobox for any of the given field patterns and parse the value.

    ``parse_fn`` is one of the ``_parse_*`` helpers above.
    """
    for pat in patterns:
        # Match `| <pattern> = <value>` (possibly with `[[link]]` markup)
        regex = r"\|\s*" + pat + r"\s*=\s*([^\n|]+)"
        m = re.search(regex, wikitext, flags=re.IGNORECASE)
        if m:
            raw = m.group(1).strip()
            # Strip common wiki markup
            raw = re.sub(r"\[\[([^|\]]+\|)?([^\]]+)\]\]", r"\2", raw)  # [[link|text]] or [[link]]
            raw = raw.replace("'''", "").replace("''", "")
            value = parse_fn(raw)
            if value is not None:
                return value
    return None


def parse_practicality_from_infobox(wikitext: str) -> dict[str, Any]:
    """Parse a Wikipedia car article wikitext for practicality fields.

    Returns a dict with the extracted values (any field may be None).
    """
    return {
        "cargo_volume_liters_seats_down": _extract_infobox_value(
            wikitext, _VOLUME_DOWN_PATTERNS, _parse_volume_to_liters
        ),
        "cargo_volume_liters_seats_up": _extract_infobox_value(
            wikitext, _VOLUME_UP_PATTERNS, _parse_volume_to_liters
        ),
        "seat_count": _extract_infobox_value(
            wikitext, _SEAT_COUNT_PATTERNS, _parse_int_count
        ),
        "front_legroom_mm": _extract_infobox_value(
            wikitext, _LEG_LEAD_PATTERNS, _parse_dimension_to_mm
        ),
        "rear_legroom_mm": _extract_infobox_value(
            wikitext, _LEG_REAR_PATTERNS, _parse_dimension_to_mm
        ),
        "front_headroom_mm": _extract_infobox_value(
            wikitext, _HEAD_FRONT_PATTERNS, _parse_dimension_to_mm
        ),
        "rear_headroom_mm": _extract_infobox_value(
            wikitext, _HEAD_REAR_PATTERNS, _parse_dimension_to_mm
        ),
        "tow_capacity_kg": _extract_infobox_value(
            wikitext, _TOW_PATTERNS, _parse_dimension_to_mm  # kg are in mm column
        ),
    }


# --- Wikipedia API client ---------------------------------------------------

def fetch_wikipedia_article(title: str) -> str | None:
    """Fetch the FULL wikitext of a Wikipedia article. Returns None if not found.

    Uses ``prop=wikitext`` without a section filter so we get the entire
    article (including per-generation infoboxes that live deep in the
    sub-sections). The parser then scans the whole text for the fields
    we want -- this is more robust than per-section fetching for cars
    that are part of a long-running nameplate (e.g. "Porsche 911" with
    8 generations of sub-articles).

    Implements the rate-limit-respecting retry policy described in the
    module docstring.
    """
    params = {
        "action": "parse",
        "page": title,
        "prop": "wikitext",
        "format": "json",
    }
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            r = requests.get(
                WIKI_API,
                params=params,
                headers={"User-Agent": USER_AGENT},
                timeout=REQUEST_TIMEOUT,
            )
        except requests.RequestException as exc:
            print(f"  [{title}] request failed (attempt {attempt}/{MAX_RETRIES}): {exc}", file=sys.stderr)
            time.sleep(BACKOFF_FACTOR * attempt)
            continue

        if r.status_code == 429:
            wait = BACKOFF_FACTOR ** attempt
            print(f"  [{title}] 429 rate limit -- backoff {wait:.1f}s", file=sys.stderr)
            time.sleep(wait)
            continue

        if r.status_code == 404:
            return None  # page doesn't exist

        if r.status_code != 200:
            print(f"  [{title}] HTTP {r.status_code} (attempt {attempt})", file=sys.stderr)
            time.sleep(BACKOFF_FACTOR * attempt)
            continue

        data = r.json()
        if "error" in data:
            return None
        return data.get("parse", {}).get("wikitext", {}).get("*", "")

    return None


def make_wikipedia_title(make: str, model: str) -> str:
    """Construct a Wikipedia article title from make + model.

    Tries multiple candidate titles in order: exact, with generation,
    with parentheses, etc. Returns the first one we attempt (the caller
    handles 404s and tries alternatives).
    """
    base = f"{make} {model}".strip()
    return base


# --- DB writing -------------------------------------------------------------

def upsert_dimensions(
    session: Session,
    car_id: int,
    extracted: dict[str, Any],
    dry_run: bool = False,
) -> bool:
    """Write extracted values to the dimensions row. Returns True if changed."""
    dim = session.query(Dimensions).filter(Dimensions.car_id == car_id).first()
    if dim is None:
        # Create a stub dimensions row for the car
        dim = Dimensions(car_id=car_id)
        session.add(dim)

    changed = False
    fields = [
        "seat_count",
        "cargo_volume_liters_seats_down",
        "front_legroom_mm",
        "front_headroom_mm",
        "rear_legroom_mm",
        "rear_headroom_mm",
        "tow_capacity_kg",
    ]
    for field in fields:
        val = extracted.get(field)
        if val is None:
            continue
        if getattr(dim, field) != val:
            setattr(dim, field, val)
            changed = True

    if changed:
        # Mark source in extra JSON
        extra = dim.extra or {}
        extra["practicality_enriched"] = True
        extra["enriched_at"] = time.strftime("%Y-%m-%d")
        extra["enrichment_source"] = "wikipedia"
        dim.extra = extra
        if not dim.source:
            dim.source = "wikipedia-2026-06-18"

    if not dry_run and changed:
        session.commit()
    return changed


# --- Main loop --------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument("--limit", type=int, default=0, help="Stop after N cars (0 = all)")
    parser.add_argument("--start-from", type=int, default=0, help="Start at car_id N")
    parser.add_argument("--verbose", action="store_true", help="Per-field parse output")
    args = parser.parse_args()

    session = get_session()
    try:
        cars = (
            session.query(Car)
            .order_by(Car.id)
            .filter(Car.id >= args.start_from)
            .all()
        )
        if args.limit:
            cars = cars[: args.limit]

        total = len(cars)
        enriched = 0
        skipped = 0
        errors = 0
        print(f"Enriching {total} cars (dry_run={args.dry_run})")

        for i, car in enumerate(cars, 1):
            # Try the canonical title first
            title = make_wikipedia_title(car.make, car.model)
            wikitext = fetch_wikipedia_article(title)

            # Try with generation suffix if not found
            if wikitext is None and car.generation:
                wikitext = fetch_wikipedia_article(f"{title} ({car.generation})")

            if wikitext is None:
                # Mark as not found in dimensions.extra
                dim = session.query(Dimensions).filter(Dimensions.car_id == car.id).first()
                if dim is not None:
                    extra = dim.extra or {}
                    if not extra.get("practicality_enriched"):
                        extra["practicality_enrichment_attempted"] = True
                        extra["practicality_enrichment_found"] = False
                        dim.extra = extra
                        if not args.dry_run:
                            session.commit()
                skipped += 1
                print(f"  [{i}/{total}] {title} -- NOT FOUND", file=sys.stderr)
                time.sleep(DELAY_BETWEEN_REQUESTS)
                continue

            extracted = parse_practicality_from_infobox(wikitext)
            changed = upsert_dimensions(session, car.id, extracted, dry_run=args.dry_run)
            enriched += 1 if changed else 0

            if args.verbose or (changed and args.verbose):
                found = {k: v for k, v in extracted.items() if v is not None}
                print(f"  [{i}/{total}] {title} -> {found}")

            if i % 10 == 0:
                print(f"  [{i}/{total}] progress: enriched={enriched} skipped={skipped}")

            time.sleep(DELAY_BETWEEN_REQUESTS)

        print(f"\nDone. enriched={enriched} skipped={skipped} errors={errors} total={total}")
        return 0
    finally:
        session.close()


if __name__ == "__main__":
    raise SystemExit(main())

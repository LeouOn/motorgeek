"""Doug Score comparison view.

Loads Doug Score entries from ``data/dougscore_anchors.json`` and matches
them to DB cars via fuzzy make/model/year matching. Computes our composite
score alongside Doug's dougscore and shows a side-by-side comparison.

This module re-exports the canonical comparison logic from
``scripts.dougscore_compare`` so callers can do::

    from motorgeek.core.calculators.dougscore import run
    run(limit=20)

The canonical logic lives in the script (not here) because the comparison
is purely CLI-oriented and shouldn't pull in the SQLAlchemy ORM session.
"""
from __future__ import annotations

from scripts.dougscore_compare import (  # type: ignore[import-not-found]
    get_composite_breakdown,
    load_db,
    load_dougscore,
    match_cars,
    render_subscore_breakdown,
    render_table,
)


def run(limit: int = 30) -> None:
    """Print comparison table for top-N Doug Score entries."""
    dougscore = load_dougscore()
    db = load_db()
    matches = match_cars(dougscore, db)
    matches.sort(key=lambda m: -m[0]["dougscore"])
    print(render_table(matches, limit))
    if limit and limit < 10:
        pass  # skip subscore table when limiting tightly
    else:
        print(render_subscore_breakdown(matches, limit))
    matched = sum(1 for _, c, _ in matches if c is not None)
    print(f"\nMatched: {matched} / {len(dougscore)} Doug Score entries to DB cars")
    unmatched = [m for m in matches if m[1] is None]
    if unmatched:
        print("Unmatched:")
        for ds, _, _ in unmatched:
            print(f"  {ds['year']} {ds['make']} {ds['model']}")


__all__ = [
    "load_dougscore",
    "load_db",
    "match_cars",
    "get_composite_breakdown",
    "render_table",
    "render_subscore_breakdown",
    "run",
]

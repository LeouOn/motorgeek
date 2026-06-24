"""Backfill ``powertrain_ice.cargo_volume_liters`` from body-style estimates.

Per ``.omo/research/session-observations-2026-06-18.md`` section 3, 71 of
~210 cars have real cargo data; the remaining ~139 carry NULL and would
otherwise drop out of the practicality dimension's high-resolution path.
This script fills those NULLs with body-style midpoints so the practicality
calculator can use a real liters value rather than falling back at runtime.

Estimated values are flagged by storing ``{"cargo_estimated": true}`` in the
row's ``extra`` JSON column. This lets downstream tooling distinguish real
measurements from estimates and lets a future re-run skip rows that already
carry a real value.

The script is idempotent:

* Rows whose ``cargo_volume_liters`` is already a positive number are
  preserved (never overwritten).
* Rows previously backfilled by this script (extra.cargo_estimated == true)
  are skipped on subsequent runs by default. Pass ``--force`` to re-apply.

Usage::

    python scripts/backfill_cargo_estimates.py --dry-run    # preview
    python scripts/backfill_cargo_estimates.py              # apply
    python scripts/backfill_cargo_estimates.py --force      # re-apply estimates
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter

from motorgeek.core.calculators.practicality import (
    BODY_STYLE_CARGO_ESTIMATES,
    DEFAULT_CARGO_LITERS,
)
from motorgeek.core.database import get_session
from motorgeek.core.models import Car, PowertrainICE

ESTIMATE_FLAG_KEY = "cargo_estimated"


def _ensure_extra_dict(row: PowertrainICE) -> dict:
    """Return a mutable dict for ``row.extra``, initializing it if needed.

    SQLAlchemy's JSON column may return None or a non-dict value for legacy
    rows. We normalise to ``{}`` in place and return the reference so the
    caller can mutate.
    """
    if row.extra is None or not isinstance(row.extra, dict):
        row.extra = {}
    return row.extra


def _is_already_estimated(row: PowertrainICE) -> bool:
    extra = row.extra
    if not isinstance(extra, dict):
        return False
    return bool(extra.get(ESTIMATE_FLAG_KEY))


def _has_real_cargo(row: PowertrainICE) -> bool:
    return row.cargo_volume_liters is not None and row.cargo_volume_liters > 0


def _estimate_for_body_style(body_style: str | None) -> tuple[float, str]:
    """Return ``(liters, source_label)`` for the given body style."""
    bs = (body_style or "").lower()
    if bs in BODY_STYLE_CARGO_ESTIMATES:
        return BODY_STYLE_CARGO_ESTIMATES[bs], f"body-style:{bs or 'unknown'}"
    return DEFAULT_CARGO_LITERS, "body-style:unknown-default"


def _print_summary(
    total: int,
    preserved_real: int,
    skipped_existing_estimate: int,
    backfilled: int,
    no_body_style: int,
    body_style_counts: Counter,
    dry_run: bool,
) -> None:
    mode = "DRY RUN (no writes)" if dry_run else "APPLIED"
    print()
    print(f"=== Cargo-volume Backfill [{mode}] ===")
    print(f"PowertrainICE rows scanned     : {total}")
    print(f"Preserved (real cargo present) : {preserved_real}")
    print(f"Skipped (already estimated)    : {skipped_existing_estimate}")
    print(f"New estimates written          : {backfilled}")
    print(f"Backfilled with default (no bs): {no_body_style}")
    if backfilled:
        print()
        print("Estimates by body style (newly written):")
        for bs, count in sorted(body_style_counts.items()):
            print(f"  {bs:20s}: {count}")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Backfill powertrain_ice.cargo_volume_liters from body-style "
            "estimates for cars without real cargo data."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the planned changes without writing to the database.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help=(
            "Re-apply estimates even on rows previously backfilled by this "
            "script. Real (non-estimated) cargo values are always preserved."
        ),
    )
    args = parser.parse_args()

    session = get_session()
    ice_rows = session.query(PowertrainICE).all()
    cars_by_id = {c.id: c for c in session.query(Car).all()}

    total = len(ice_rows)
    preserved_real = 0
    skipped_existing_estimate = 0
    backfilled = 0
    no_body_style = 0
    body_style_counts: Counter = Counter()

    for row in ice_rows:
        # Always preserve real cargo data.
        if _has_real_cargo(row):
            preserved_real += 1
            continue

        # Skip rows we previously estimated unless --force.
        if _is_already_estimated(row) and not args.force:
            skipped_existing_estimate += 1
            continue

        car = cars_by_id.get(row.car_id)
        body_style = car.body_style if car is not None else None
        if not body_style:
            no_body_style += 1

        liters, _label = _estimate_for_body_style(body_style)
        bs_key = (body_style or "<unknown>").lower()

        if args.dry_run:
            backfilled += 1
            body_style_counts[bs_key] += 1
            continue

        # Apply.
        row.cargo_volume_liters = liters
        extra = _ensure_extra_dict(row)
        extra[ESTIMATE_FLAG_KEY] = True
        backfilled += 1
        body_style_counts[bs_key] += 1

    if not args.dry_run:
        session.commit()

    _print_summary(
        total=total,
        preserved_real=preserved_real,
        skipped_existing_estimate=skipped_existing_estimate,
        backfilled=backfilled,
        no_body_style=no_body_style,
        body_style_counts=body_style_counts,
        dry_run=args.dry_run,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

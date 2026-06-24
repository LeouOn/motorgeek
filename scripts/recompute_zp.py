"""Backfill ZePerfs Index (ZP) for every car in the database.

Uses the production calculator (`motorgeek.core.calculators.zeperfs`) which
applies the v4 ICE formula and v3 EV formula. The source tag
``formula-v4-2026-06-18`` identifies these computed values and distinguishes
them from user-confirmed fiches.

Usage::

    python scripts/recompute_zp.py --dry-run    # preview only
    python scripts/recompute_zp.py              # apply

Cars whose existing ``zeperfs_indices.source`` contains the word "user" are
skipped: those rows are ground truth copied from real ZePerfs fiches and
must not be overwritten by the formula.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from datetime import datetime, timezone

from motorgeek.core.calculators.zeperfs import classify_zp, compute_zp_for_car
from motorgeek.core.database import get_session
from motorgeek.core.models import Car, Performance, PowertrainICE, ZePerfsIndices

SOURCE_TAG = "formula-v4-2026-06-18"
USER_MARKER = "user"  # substring that marks ground-truth rows


def _is_user_confirmed(row: ZePerfsIndices | None) -> bool:
    """A row is ground truth when its source mentions 'user'."""
    if row is None or not row.source:
        return False
    return USER_MARKER in row.source.lower()


def _print_summary(
    total: int,
    computed: int,
    skipped_user: int,
    skipped_no_data: int,
    branch_counts: Counter,
    class_counts: Counter,
    dry_run: bool,
) -> None:
    mode = "DRY RUN (no writes)" if dry_run else "APPLIED"
    print()
    print(f"=== ZP Backfill [{mode}] ===")
    print(f"Total cars scanned      : {total}")
    print(f"New ZP computed         : {computed}")
    print(f"Skipped (user-confirmed): {skipped_user}")
    print(f"Skipped (insufficient)  : {skipped_no_data}")
    if computed:
        print()
        print("Branch usage (newly computed):")
        for branch in ("ICE", "EV"):
            print(f"  {branch:5s}: {branch_counts.get(branch, 0)}")
    print()
    print("Class distribution (computed + preserved user values):")
    for label in ("<C", "C", "B", "A", "S1", "S2/R", "Track"):
        print(f"  {label:7s}: {class_counts.get(label, 0)}")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Recompute ZePerfs Index for all cars using the v4 formula.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the planned changes without writing to the database.",
    )
    args = parser.parse_args()

    session = get_session()
    cars = session.query(Car).all()

    computed = 0
    skipped_user = 0
    skipped_no_data = 0
    branch_counts: Counter = Counter()
    class_counts: Counter = Counter()

    for car in cars:
        powertrain_ice = (
            session.query(PowertrainICE)
            .filter(PowertrainICE.car_id == car.id)
            .first()
        )
        performance = (
            session.query(Performance)
            .filter(Performance.car_id == car.id)
            .first()
        )
        existing = (
            session.query(ZePerfsIndices)
            .filter(ZePerfsIndices.car_id == car.id)
            .first()
        )

        # Preserve user-confirmed ground truth.
        if _is_user_confirmed(existing):
            skipped_user += 1
            if existing.zeperfs_index is not None:
                class_counts[classify_zp(existing.zeperfs_index)] += 1
            continue

        zp, branch = compute_zp_for_car(car, powertrain_ice, performance)

        if zp is None:
            skipped_no_data += 1
            continue

        computed += 1
        branch_counts[branch] += 1
        class_counts[classify_zp(zp)] += 1

        if args.dry_run:
            continue

        recorded = datetime.now(timezone.utc)
        if existing is not None:
            existing.zeperfs_index = zp
            existing.source = SOURCE_TAG
            existing.recorded_date = recorded
        else:
            session.add(
                ZePerfsIndices(
                    car_id=car.id,
                    zeperfs_index=zp,
                    source=SOURCE_TAG,
                    recorded_date=recorded,
                )
            )

    if not args.dry_run:
        session.commit()

    _print_summary(
        total=len(cars),
        computed=computed,
        skipped_user=skipped_user,
        skipped_no_data=skipped_no_data,
        branch_counts=branch_counts,
        class_counts=class_counts,
        dry_run=args.dry_run,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

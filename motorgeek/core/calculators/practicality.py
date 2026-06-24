"""Practicality dimension -- Doug Score-calibrated cargo-volume scoring (v2).

Implements a single-dimension practicality score (0-100) following Doug
DeMuro's published methodology, extended for the MotorGeek enrichment:

* **Cargo volume (seats-up)** is the primary driver (correlation 0.720
  with Doug's scores across our 13-car cross-reference -- see
  ``.omo/research/session-observations-2026-06-18.md`` section 3).
* **Body style** gets two adjustments:
    - Wagons/estates get +1 tier (user decision 2026-06-18:
      "only slight bonus to wagons").
    - Coupes/convertibles/roadsters get -0.5 tier (added 2026-06-18:
      a 2-door coupe with 400L cargo is materially less practical than
      a 4-door sedan with 400L cargo because rear access is limited).
      Floored at tier 1 (P=10) so we never score negative.
* **Enrichment bonuses (v2)** -- 4 SMALL additive bonuses, each +0.5
  tier, capped at 10 total:
    - cargo_volume_liters_seats_down > 1500L  (significant cargo flexibility)
    - seat_count >= 7  (3-row / family hauler)
    - rear_legroom_mm > 950  (adults sit comfortably in back)
    - tow_capacity_kg > 2000  ("a little benefit for towing")

The conversion pipeline is:

    liters -> cubic feet (liters / 28.32)
           -> Doug tier (1-10, discrete breakpoints)
           -> wagon bonus (+1 tier) OR coupe penalty (-0.5 tier)
           -> enrichment bonuses (4 x +0.5 tier)
           -> cap at 10 (or floor at 1 for coupe penalty)
           -> score (tier * 10, so 1-10 maps to 10-100)

When real cargo data is missing we fall back to a body-style midpoint
estimate. The estimate is imprecise but provides 100% coverage for a
15%-weight composite dimension.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # avoid runtime import cycle; annotations are strings
    from motorgeek.core.models import (
        Car,
        Dimensions,
        PowertrainEV,
        PowertrainICE,
    )


# --- Doug Score practicality tiers -----------------------------------------
#
# Cargo volume in cubic feet -> tier (1-10). Breakpoints are Doug DeMuro's
# published methodology. Evaluated as "less than upper bound" -- the first
# matching tier wins. Anything >= 72 cf returns 10.
_CARGO_CF_TIERS: tuple[tuple[float, int], ...] = (
    (3.0, 1),
    (6.5, 2),
    (11.0, 3),
    (16.0, 4),
    (24.0, 5),
    (34.0, 6),
    (48.0, 7),
    (64.0, 8),
    (72.0, 9),
)
_TIER_MAX = 10  # anything >= the largest breakpoint above


def cargo_cf_to_doug_tier(cargo_cf: float) -> int:
    """Map cargo volume in cubic feet to a Doug Score practicality tier (1-10).

    Tiers come from Doug DeMuro's published methodology. Evaluated in order;
    the first ``(upper_exclusive, tier)`` row whose upper bound is greater
    than ``cargo_cf`` wins. Volumes at or above the largest breakpoint (72 cf)
    return the maximum tier (10).
    """
    for upper, tier in _CARGO_CF_TIERS:
        if cargo_cf < upper:
            return tier
    return _TIER_MAX


# --- Body style adjustments ------------------------------------------------
#
# User decision 2026-06-18: "only slight bonus to wagons". The bonus is
# +1 tier, capped at 10. Applies to wagon and estate body styles.
WAGON_BONUS_STYLES: frozenset[str] = frozenset({"wagon", "estate"})

# 2-door cars (coupes, convertibles, roadsters) get a small penalty because
# rear-seat access is limited regardless of cargo volume. A 2-door coupe
# with 400L trunk space is materially less practical than a 4-door sedan
# with the same 400L -- you can't easily load people or large items.
# The penalty is -0.5 tier, floored at tier 1 (P=10).
COUPE_PENALTY_STYLES: frozenset[str] = frozenset({"coupe", "convertible", "roadster"})
COUPE_PENALTY_INCREMENT = -0.5


# --- Body style cargo estimates (for cars without real cargo data) ---------
#
# Generic midpoints for seats-up configuration. Used as a fallback when
# neither powertrain_ice nor powertrain_ev carries a real cargo_volume_liters
# value. Values are in liters and match
# ``.omo/research/session-observations-2026-06-18.md`` section 3 table.
BODY_STYLE_CARGO_ESTIMATES: dict[str, float] = {
    "sedan": 430.0,
    "coupe": 300.0,
    "hatchback": 350.0,
    "suv": 550.0,
    "wagon": 580.0,
    "estate": 580.0,
    "convertible": 200.0,
    "roadster": 200.0,
    "minivan": 850.0,
    "van": 850.0,
    "truck": 700.0,
}

# Default estimate when body_style is itself unknown. Compact hatchback
# territory -- deliberately conservative.
DEFAULT_CARGO_LITERS = 350.0

# Liters -> cubic feet conversion factor (1 cf == 28.32 L).
LITERS_PER_CUBIC_FOOT = 28.32

# --- v2 Enrichment thresholds ---------------------------------------------
#
# Each bonus is +0.5 tier when the condition is met. The four bonuses together
# can add up to +2.0 tiers, but the final tier is capped at 10.
CARGO_DOWN_BONUS_THRESHOLD_L = 1500.0   # seats-down cargo > 1500L -> +0.5
SEAT_COUNT_BONUS_THRESHOLD = 7          # 3-row / 7+ seats -> +0.5
REAR_LEGROOM_BONUS_THRESHOLD_MM = 950.0  # adults sit comfortably -> +0.5
TOW_CAPACITY_BONUS_THRESHOLD_KG = 2000  # "a little benefit for towing" -> +0.5
ENRICHMENT_BONUS_INCREMENT = 0.5        # each bonus is +0.5 tier


def compute_practicality_score(
    cargo_liters: float | None,
    body_style: str | None,
) -> float:
    """Compute v1 practicality score (0-100) from cargo volume and body style.

    Backward-compatible API. Does NOT apply the v2 enrichment bonuses
    (cargo-down, seat count, legroom, tow). Use ``compute_practicality_v2``
    for the enriched version.

    Pipeline:
        1. Resolve cargo volume -- real value when available, otherwise
           estimated from body_style.
        2. Convert liters to cubic feet.
        3. Map cubic feet to a Doug Score tier (1-10).
        4. Apply body_style adjustments:
           - wagon/estate: +1 tier (capped at 10)
           - coupe/convertible/roadster: -0.5 tier (floored at 1)
        5. Scale tier to score: ``tier * 10`` (so tiers map to 10-100).
    """
    # Step 1: resolve cargo volume (real or estimated).
    if cargo_liters is None or cargo_liters <= 0:
        bs = (body_style or "").lower()
        cargo_liters = BODY_STYLE_CARGO_ESTIMATES.get(bs, DEFAULT_CARGO_LITERS)

    # Step 2: liters -> cubic feet.
    cargo_cf = cargo_liters / LITERS_PER_CUBIC_FOOT

    # Step 3: cubic feet -> Doug tier.
    tier = cargo_cf_to_doug_tier(cargo_cf)

    # Step 4: body_style adjustments.
    bs = (body_style or "").lower()
    if bs in WAGON_BONUS_STYLES:
        tier = min(_TIER_MAX, tier + 1)
    elif bs in COUPE_PENALTY_STYLES:
        # Coupe penalty: -0.5 tier, floored at tier 1.
        tier = max(1, tier + COUPE_PENALTY_INCREMENT)

    # Step 5: scale tier (1-10) to score (10-100).
    return float(tier * 10)


def compute_practicality_v2(
    cargo_liters_seats_up: float | None,
    body_style: str | None,
    cargo_liters_seats_down: float | None = None,
    seat_count: int | None = None,
    rear_legroom_mm: float | None = None,
    tow_capacity_kg: int | None = None,
) -> tuple[float, dict[str, bool]]:
    """Compute v2 practicality score (0-100) with enrichment bonuses.

    Returns a tuple of (score, bonuses_dict) where bonuses_dict shows
    which of the 4 enrichment bonuses were applied.

    Pipeline:
        1. Same base computation as v1 (cargo + wagon/coupe adjustment).
        2. Apply 4 enrichment bonuses (each +0.5 tier):
            - cargo_seats_down > 1500L
            - seat_count >= 7
            - rear_legroom_mm > 950
            - tow_capacity_kg > 2000
        3. Cap total tier at 10.
        4. Scale to score (tier * 10, so 10-100).
    """
    # Steps 1-4 from v1 (gives us the base tier as a float so the
    # coupe penalty's half-tier is preserved).
    score = compute_practicality_score(cargo_liters_seats_up, body_style)
    base_tier = score / 10  # reverse: score -> tier (preserves half-tiers)
    new_tier = base_tier

    # Step 5: apply the 4 enrichment bonuses.
    bonuses: dict[str, bool] = {
        "cargo_seats_down": False,
        "seat_count": False,
        "rear_legroom": False,
        "tow_capacity": False,
        "coupe_penalty": False,
    }

    # Record coupe penalty application (informational only; already applied
    # in the base score via compute_practicality_score).
    bs = (body_style or "").lower()
    if bs in COUPE_PENALTY_STYLES:
        bonuses["coupe_penalty"] = True

    if cargo_liters_seats_down is not None and cargo_liters_seats_down > CARGO_DOWN_BONUS_THRESHOLD_L:
        new_tier += ENRICHMENT_BONUS_INCREMENT
        bonuses["cargo_seats_down"] = True

    if seat_count is not None and seat_count >= SEAT_COUNT_BONUS_THRESHOLD:
        new_tier += ENRICHMENT_BONUS_INCREMENT
        bonuses["seat_count"] = True

    if rear_legroom_mm is not None and rear_legroom_mm > REAR_LEGROOM_BONUS_THRESHOLD_MM:
        new_tier += ENRICHMENT_BONUS_INCREMENT
        bonuses["rear_legroom"] = True

    if tow_capacity_kg is not None and tow_capacity_kg > TOW_CAPACITY_BONUS_THRESHOLD_KG:
        new_tier += ENRICHMENT_BONUS_INCREMENT
        bonuses["tow_capacity"] = True

    # Step 6: cap at 10 and scale to score.
    new_tier = min(_TIER_MAX, new_tier)
    final_score = float(new_tier * 10)
    return final_score, bonuses


def compute_practicality_for_car(
    car: "Car",
    powertrain_ice: "PowertrainICE | None" = None,
    powertrain_ev: "PowertrainEV | None" = None,
) -> float:
    """Compute v1 practicality score for a car from ORM objects.

    Prefers a real ``cargo_volume_liters`` from ``powertrain_ice`` and falls
    back to ``powertrain_ev``; if neither carries a positive value the
    body-style midpoint estimate is used.

    Always returns a value (the underlying primitive never returns None).
    """
    cargo: float | None = None
    if (
        powertrain_ice is not None
        and powertrain_ice.cargo_volume_liters
        and powertrain_ice.cargo_volume_liters > 0
    ):
        cargo = powertrain_ice.cargo_volume_liters
    elif (
        powertrain_ev is not None
        and powertrain_ev.cargo_volume_liters
        and powertrain_ev.cargo_volume_liters > 0
    ):
        cargo = powertrain_ev.cargo_volume_liters

    return compute_practicality_score(cargo, car.body_style)


def compute_practicality_for_car_v2(
    car: "Car",
    powertrain_ice: "PowertrainICE | None" = None,
    powertrain_ev: "PowertrainEV | None" = None,
    dimensions: "Dimensions | None" = None,
) -> tuple[float, dict[str, bool]]:
    """Compute v2 practicality score for a car using enrichment data.

    Returns (score, bonuses_dict) where bonuses_dict shows which
    enrichment bonuses were applied.

    Falls back to v1 (cargo only) when enrichment fields are missing.
    The cargo_seats_up and body_style are always present (real or estimated).
    """
    # Resolve seats-up cargo (real or estimated)
    cargo_up: float | None = None
    if (
        powertrain_ice is not None
        and powertrain_ice.cargo_volume_liters
        and powertrain_ice.cargo_volume_liters > 0
    ):
        cargo_up = powertrain_ice.cargo_volume_liters
    elif (
        powertrain_ev is not None
        and powertrain_ev.cargo_volume_liters
        and powertrain_ev.cargo_volume_liters > 0
    ):
        cargo_up = powertrain_ev.cargo_volume_liters

    # Read enrichment fields from dimensions if available
    cargo_down: float | None = None
    seat_ct: int | None = None
    legroom: float | None = None
    tow: int | None = None
    if dimensions is not None:
        cargo_down = dimensions.cargo_volume_liters_seats_down
        seat_ct = dimensions.seat_count
        legroom = dimensions.rear_legroom_mm
        tow = dimensions.tow_capacity_kg

    return compute_practicality_v2(
        cargo_liters_seats_up=cargo_up,
        body_style=car.body_style,
        cargo_liters_seats_down=cargo_down,
        seat_count=seat_ct,
        rear_legroom_mm=legroom,
        tow_capacity_kg=tow,
    )

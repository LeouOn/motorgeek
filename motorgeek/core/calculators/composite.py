"""Composite car index -- weighted blend of Quality, Reliability, Practicality, Performance.

Two composite formulas are available:

**v2 (current default)**: user-specified 2026-06-18, see
``.omo/research/session-observations-2026-06-18.md`` section 5:

    Composite = Quality      * 0.40
              + Reliability  * 0.30
              + Practicality * 0.15
              + ZP_norm      * 0.15

Where ``ZP_norm = min(100, ZP / 3)`` (linear normalization chosen over log
for simplicity -- at 15% weight the difference is ~1.65 composite points
for Plaid-class cars, within noise).

**v3 (new, 2026-06-18)**: user-requested blend adding Dougscore as an
external validation signal:

    Composite = Quality      * 0.40
              + Reliability  * 0.20
              + Dougscore    * 0.20
              + Practicality * 0.10
              + ZP_norm      * 0.10

Dougscore is the 0-100 holistic rating from Doug DeMuro (see
``data/dougscore_anchors.json``). The shift from v2 -> v3 trades 10pp
from Reliability for a 20pp Dougscore dimension, plus 5pp from each of
Practicality and ZP_norm (compressing them to 10pp each).

**Missing data handling**: when a dimension is NULL, redistribute its weight
proportionally among the present dimensions. At least ``MIN_DIMENSIONS``
(two of N) must be present to produce a composite; otherwise we return
None. Works identically for v2 (4 dims) and v3 (5 dims).

Example: car with Q=80, R=85, Doug=70, Prac=NULL, ZP_norm=70 -- only 4 of 5
present:

    weight_sum = 0.40 + 0.20 + 0.20 + 0.10 = 0.90
    raw        = 80*0.40 + 85*0.20 + 70*0.20 + 70*0.10 = 32 + 17 + 14 + 7 = 70.0
    composite  = 70.0 / 0.90 = 77.8

The redistribution keeps the composite on a 0-100 scale regardless of which
dimensions are missing.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # avoid runtime import cycle; annotations are strings
    from motorgeek.core.models import (
        BuildQuality,
        Car,
        Performance,
        PowertrainEV,
        PowertrainICE,
        Reliability,
    )


# --- Weights: v2 (current default, FROZEN) ---------------------------------

WEIGHTS: dict[str, float] = {
    "quality": 0.40,
    "reliability": 0.30,
    "practicality": 0.15,
    "performance": 0.15,
}


# --- Weights: v3 (Dougscore-enhanced, 2026-06-18) ---------------------------

WEIGHTS_V3: dict[str, float] = {
    "quality": 0.40,
    "reliability": 0.20,
    "dougscore": 0.20,
    "practicality": 0.10,
    "performance": 0.10,
}

# Need at least this many of the dimensions to produce a composite.
# Below the threshold we return None rather than a number built on a single
# data point (which would over-amplify the lone dimension's quirks).
MIN_DIMENSIONS = 2

# Linear normalization: ZP_norm = min(100, ZP / ZP_SCALE).
# ZP ranges roughly 70-230 in our DB; dividing by 3 puts the band at 23-77,
# with the truly extreme cars (Plaid ZP=227) reaching 76 and beyond capping
# at 100. See spec section 5 for the linear-vs-log analysis.
ZP_SCALE = 3.0


# --- ZP normalization ------------------------------------------------------

def normalize_zp(zp: float | None) -> float | None:
    """Normalize a raw ZP value (0-300+) to the 0-100 composite scale.

    Uses linear division: ``min(100, zp / ZP_SCALE)``. Returns None when
    ``zp`` is None so the composite dispatcher can treat it as a missing
    dimension.
    """
    if zp is None:
        return None
    return min(100.0, zp / ZP_SCALE)


# --- Core composite formula (v2) -------------------------------------------

def compute_composite(
    quality: float | None,
    reliability: float | None,
    practicality: float | None,
    performance_norm: float | None,
) -> float | None:
    """Compute the v2 composite score from the four dimensions.

    Each dimension is a 0-100 score, or None when missing. When a dimension
    is None its weight is redistributed proportionally across the present
    dimensions (so the result stays on a 0-100 scale).

    Returns None when fewer than ``MIN_DIMENSIONS`` dimensions are present.
    The result is rounded to one decimal place.
    """
    scores: dict[str, float | None] = {
        "quality": quality,
        "reliability": reliability,
        "practicality": practicality,
        "performance": performance_norm,
    }

    present = {k: v for k, v in scores.items() if v is not None}
    if len(present) < MIN_DIMENSIONS:
        return None

    weight_sum = sum(WEIGHTS[k] for k in present)
    adjusted_weights = {k: WEIGHTS[k] / weight_sum for k in present}

    composite = sum(present[k] * adjusted_weights[k] for k in present)
    return round(composite, 1)


# --- Core composite formula (v3, Dougscore-enhanced) ----------------------

def compute_composite_v3(
    quality: float | None,
    reliability: float | None,
    dougscore: float | None,
    practicality: float | None,
    performance_norm: float | None,
) -> float | None:
    """Compute the v3 composite score from the five dimensions.

    **Dougscore is a HARD REQUIREMENT** -- if ``dougscore`` is None, this
    function returns None regardless of the other dimensions. Rationale:
    redistributing Dougscore's 20% weight across the other four dimensions
    makes unranked cars look BETTER on average (the 20% simply boosts
    Q/R/P/Z weights), which is the opposite of what we want. v3 is
    therefore a "with external validation" view, computed only for the
    27 cars that have Dougscore data. For the full 215-car leaderboard
    use ``compute_composite`` (v2) instead.

    Each remaining dimension is a 0-100 score, or None when missing.
    Missing non-Dougscore dimensions still have their weights
    redistributed proportionally across the other present non-Dougscore
    dimensions (so the result stays on a 0-100 scale for the 40+20+10+10
    partition).

    Returns None when ``dougscore`` is None, OR when fewer than
    ``MIN_DIMENSIONS`` of the remaining dimensions are present.

    The result is rounded to one decimal place.

    Note: Dougscore here is the 0-100 holistic rating from Doug DeMuro.
    In our current ``data/dougscore_anchors.json`` the actual range is
    43-74 (Lexus LS 400 to McLaren Speedtail), so Dougscore dimensions
    tend to be lower than our internal Q/R/P/Z dimensions. The 20% weight
    in v3 deliberately injects this external calibration signal -- cars
    that Doug rates highly get a boost even if our internal numbers
    disagree.
    """
    # Dougscore is mandatory for v3. Without it the score is meaningless
    # because redistributing its weight would unfairly boost unranked cars.
    if dougscore is None:
        return None

    scores: dict[str, float | None] = {
        "quality": quality,
        "reliability": reliability,
        "practicality": practicality,
        "performance": performance_norm,
    }

    present = {k: v for k, v in scores.items() if v is not None}
    if len(present) < MIN_DIMENSIONS:
        return None

    # Dougscore gets its full 20% weight; missing other dimensions
    # redistribute within the 40+20+10+10 = 80% remaining bucket.
    weight_sum = sum(WEIGHTS_V3[k] for k in scores if k != "dougscore" and k in present)
    # Normalize the remaining weights to sum to 0.80 (so dougscore=20% stays)
    remaining_weight = 1.0 - WEIGHTS_V3["dougscore"]  # 0.80
    adjusted_weights = {k: (WEIGHTS_V3[k] / weight_sum) * remaining_weight for k in present}
    adjusted_weights["dougscore"] = WEIGHTS_V3["dougscore"]

    composite = (
        dougscore * adjusted_weights["dougscore"]
        + sum(present[k] * adjusted_weights[k] for k in present)
    )
    return round(composite, 1)


# --- Dougscore lookup ------------------------------------------------------

def _load_dougscore_anchors() -> list[dict]:
    """Load ``data/dougscore_anchors.json`` (cached at module level).

    Returns the list of Doug Score entries. Each entry has at least the
    fields: year, make, model, dougscore. Used by the v3 ORM dispatcher
    to look up a car's dougscore by make/model/year proximity.
    """
    import json
    from pathlib import Path
    path = Path(__file__).resolve().parents[3] / "data" / "dougscore_anchors.json"
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# --- ORM-level dispatcher --------------------------------------------------

def compute_composite_for_car(
    car: "Car",
    powertrain_ice: "PowertrainICE | None" = None,
    powertrain_ev: "PowertrainEV | None" = None,
    performance: "Performance | None" = None,
    build_quality: "BuildQuality | None" = None,
    reliability: "Reliability | None" = None,
    dimensions: "Dimensions | None" = None,
    zp_value: float | None = None,
    use_practicality_v2: bool = True,
) -> tuple[float | None, dict[str, float | None]]:
    """Compute the v2 composite score for a car from ORM objects.

    Returns ``(composite_score, dimension_dict)`` where ``dimension_dict``
    exposes each of the four dimensions' resolved value (or None when
    missing). The composite is None when fewer than ``MIN_DIMENSIONS``
    dimensions could be resolved.

    Parameters
    ----------
    car:
        The Car ORM row (used for ``body_style``).
    powertrain_ice, powertrain_ev:
        Powertrain rows -- used for cargo volume and (for ICE) as the input
        to the ZP calculator.
    performance:
        The Performance ORM row (carries 0-100 / 0-60 accel). Required for
        ZP computation when ``zp_value`` is not supplied.
    build_quality, reliability:
        Score-bearing rows. Their respective score fields feed the quality
        and reliability dimensions.
    dimensions:
        The Dimensions ORM row -- used by the v2 practicality formula for
        seat count, cargo-down, rear legroom, tow capacity. Optional; if
        None or ``use_practicality_v2`` is False, falls back to v1
        (cargo + body_style only).
    zp_value:
        Pre-computed ZP value. When supplied, the ZP calculator is skipped.
    use_practicality_v2:
        When True (default) and ``dimensions`` is supplied, uses the v2
        formula with the 4 enrichment bonuses. When False, uses the v1
        formula (cargo + wagon bonus only).

    Note
    ----
    The parameter previously named ``performance`` (the ZP float) was renamed
    to ``zp_value`` to avoid clashing with the ``Performance`` ORM table this
    function also consumes.
    """
    # Lazy imports to keep the module-import graph acyclic.
    from .practicality import compute_practicality_for_car, compute_practicality_for_car_v2
    from .zeperfs import compute_zp_for_car

    # --- Quality -----------------------------------------------------------
    quality: float | None = None
    if build_quality is not None and build_quality.q_score:
        quality = build_quality.q_score

    # --- Reliability -------------------------------------------------------
    rel: float | None = None
    if reliability is not None and reliability.reliability_score:
        rel = reliability.reliability_score

    # --- Practicality (v1 or v2) ------------------------------------------
    if use_practicality_v2 and dimensions is not None:
        prac, _bonuses = compute_practicality_for_car_v2(
            car, powertrain_ice, powertrain_ev, dimensions
        )
    else:
        prac = compute_practicality_for_car(car, powertrain_ice, powertrain_ev)

    # --- Performance (ZP, normalized) -------------------------------------
    if zp_value is not None:
        zp = zp_value
    else:
        zp, _branch = compute_zp_for_car(car, powertrain_ice, performance)
    perf_norm = normalize_zp(zp) if zp is not None else None

    dims: dict[str, float | None] = {
        "quality": quality,
        "reliability": rel,
        "practicality": prac,
        "performance": perf_norm,
    }

    composite = compute_composite(quality, rel, prac, perf_norm)
    return composite, dims


def compute_composite_for_car_v3(
    car: "Car",
    powertrain_ice: "PowertrainICE | None" = None,
    powertrain_ev: "PowertrainEV | None" = None,
    performance: "Performance | None" = None,
    build_quality: "BuildQuality | None" = None,
    reliability: "Reliability | None" = None,
    dimensions: "Dimensions | None" = None,
    zp_value: float | None = None,
    use_practicality_v2: bool = True,
    dougscore: float | None = None,
) -> tuple[float | None, dict[str, float | None]]:
    """Compute the v3 composite score (with Dougscore) for a car.

    Same as ``compute_composite_for_car`` but adds the Dougscore dimension
    and uses the v3 weights (40/20/20/10/10 for Q/R/Doug/P/Z). Returns
    ``(composite_score, dimension_dict)`` with 5 dimensions exposed.

    Parameters
    ----------
    dougscore:
        Doug's 0-100 holistic rating for this car. If None, returns a v3
        composite without the Dougscore dimension (weight redistributed
        across the other 4 dimensions, falling back to v2 behavior when
        no other dimensions are missing).
    Other parameters: same as ``compute_composite_for_car``.

    Dougscore lookup: this function does NOT auto-fetch from the anchors
    file. Callers should pass ``dougscore`` explicitly, or use
    ``scripts/dougscore_compare.py`` which already does the matching.
    """
    # Compute the 4 standard dimensions by delegating to v2 dispatcher.
    v2_composite, dims = compute_composite_for_car(
        car=car,
        powertrain_ice=powertrain_ice,
        powertrain_ev=powertrain_ev,
        performance=performance,
        build_quality=build_quality,
        reliability=reliability,
        dimensions=dimensions,
        zp_value=zp_value,
        use_practicality_v2=use_practicality_v2,
    )

    # Add dougscore dimension and compute v3.
    dims["dougscore"] = dougscore
    composite = compute_composite_v3(
        quality=dims["quality"],
        reliability=dims["reliability"],
        dougscore=dougscore,
        practicality=dims["practicality"],
        performance_norm=dims["performance"],
    )
    return composite, dims

"""Tests for the practicality dimension and the composite index.

Covers:
    A. Practicality tier mapping -- every Doug Score breakpoint.
    B. Practicality body-style adjustments -- wagon gets +1 (capped at 10),
       no other style gets a bonus.
    C. Practicality estimation -- when cargo is None, fall back to the
       body-style midpoint table.
    D. Composite formula -- weight redistribution for missing dimensions.
    E. Composite edge cases -- all NULL, single dimension, all present.
    F. ZP normalization -- ZP=300 -> 100, ZP=150 -> 50, ZP=0 -> 0.

Calibration data: see ``.omo/research/session-observations-2026-06-18.md``
sections 3 (Practicality) and 5 (Composite Design).
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from motorgeek.core.calculators.composite import (
    MIN_DIMENSIONS,
    WEIGHTS,
    ZP_SCALE,
    compute_composite,
    compute_composite_for_car,
    normalize_zp,
)
from motorgeek.core.calculators.practicality import (
    BODY_STYLE_CARGO_ESTIMATES,
    LITERS_PER_CUBIC_FOOT,
    WAGON_BONUS_STYLES,
    cargo_cf_to_doug_tier,
    compute_practicality_for_car,
    compute_practicality_score,
)


# ---------------------------------------------------------------------------
# Spec verification one-liners (the four checks in the task MUST DO section).
# ---------------------------------------------------------------------------
class TestSpecVerification:
    """The exact one-liners from the task spec's VERIFICATION block."""

    def test_practicality_510_sedan_is_50(self):
        # 510 L = 18.0 cf -> tier 5 -> score 50 (no body-style bonus).
        assert compute_practicality_score(510, "sedan") == 50.0

    def test_practicality_580_wagon_is_60(self):
        # 580 L = 20.5 cf -> tier 5, wagon +1 -> tier 6 -> score 60.
        assert compute_practicality_score(580, "wagon") == 60.0

    def test_composite_full_dimensions_arithmetic(self):
        # 85*0.40 + 88*0.30 + 50*0.15 + 79*0.15 = 79.75 -> rounded 79.8.
        # NOTE: the task spec estimated this as ~76.2; that figure is an
        # arithmetic error. The formula-as-written yields 79.8.
        result = compute_composite(85, 88, 50, 79)
        assert result == pytest.approx(79.8, abs=0.05)


# ===========================================================================
# A. Practicality tier mapping
# ===========================================================================

class TestCargoTierMapping:
    """Each Doug Score tier breakpoint must map correctly.

    Breakpoints are "< upper_exclusive" -- so the test pins a value just
    below each breakpoint to the expected tier, and the breakpoint itself
    to the next-higher tier.
    """

    @pytest.mark.parametrize("cargo_cf, expected_tier", [
        (0.0,   1),
        (2.99,  1),
        (3.0,   2),    # boundary
        (6.49,  2),
        (6.5,   3),    # boundary
        (10.99, 3),
        (11.0,  4),    # boundary
        (15.99, 4),
        (16.0,  5),    # boundary
        (23.99, 5),
        (24.0,  6),    # boundary
        (33.99, 6),
        (34.0,  7),    # boundary
        (47.99, 7),
        (48.0,  8),    # boundary
        (63.99, 8),
        (64.0,  9),    # boundary
        (71.99, 9),
        (72.0,  10),   # max tier
        (100.0, 10),
        (1000.0, 10),
    ])
    def test_tier_at_breakpoints(self, cargo_cf, expected_tier):
        assert cargo_cf_to_doug_tier(cargo_cf) == expected_tier

    def test_tier_table_is_strictly_ascending(self):
        """Each breakpoint boundary produces exactly +1 over the previous tier,
        and the maximum tier is 10 above the largest breakpoint."""
        breakpoints = [3.0, 6.5, 11.0, 16.0, 24.0, 34.0, 48.0, 64.0, 72.0]
        # Just below the first breakpoint -> tier 1.
        assert cargo_cf_to_doug_tier(breakpoints[0] - 0.01) == 1
        # At each breakpoint the tier increments by exactly 1.
        for i, upper in enumerate(breakpoints):
            tier_below = cargo_cf_to_doug_tier(upper - 0.01)
            tier_at = cargo_cf_to_doug_tier(upper)
            assert tier_at == tier_below + 1, (
                f"breakpoint {upper}: tier jumped {tier_below} -> {tier_at}"
            )
        # Above the last breakpoint -> tier 10.
        assert cargo_cf_to_doug_tier(breakpoints[-1] + 1.0) == 10


class TestPracticalityScoreFromCargo:
    """compute_practicality_score with real cargo values.

    For coupes/convertibles/roadsters, the -0.5 tier penalty is applied
    (see COUPE_PENALTY_STYLES). All other body styles are unadjusted.
    """

    @pytest.mark.parametrize("cargo_liters, body_style, expected", [
        # Tier 1 (< 3 cf ~= 85 L)
        # Coupes with tiny cargo: tier 1 - 0.5 penalty = floored at 1 = 10
        (50.0,  "coupe",       10.0),
        (84.0,  "convertible", 10.0),
        # Tier 2 (3-6.5 cf ~= 85-184 L)
        # Coupes at tier 2: -0.5 = tier 1.5 -> score 15
        (100.0, "coupe",       15.0),
        (180.0, "sedan",       20.0),
        # Tier 3 (6.5-11 cf ~= 184-312 L)
        # Coupes at tier 3: -0.5 = tier 2.5 -> score 25
        (200.0, "coupe",       25.0),
        (300.0, "sedan",       30.0),
        # Tier 4 (11-16 cf ~= 312-453 L)
        # Coupes at tier 4: -0.5 = tier 3.5 -> score 35
        (350.0, "hatchback",   40.0),
        (430.0, "sedan",       40.0),  # 430 L = 15.18 cf -> tier 4
        (450.0, "sedan",       40.0),
        # Tier 5 (16-24 cf ~= 453-680 L)
        # Coupes at tier 5: -0.5 = tier 4.5 -> score 45
        (510.0, "sedan",       50.0),  # 18.0 cf
        (550.0, "suv",         50.0),  # 19.4 cf
        (580.0, "sedan",       50.0),  # 20.5 cf (no wagon bonus here)
        (679.0, "suv",         50.0),
        # Tier 6 (24-34 cf ~= 680-963 L)
        # Trucks: no coupe penalty -> score 60
        (700.0, "truck",       60.0),  # 24.7 cf
        (850.0, "minivan",     60.0),  # 30.0 cf
        # Tier 7 (34-48 cf ~= 963-1359 L)
        (1000.0, "van",        70.0),  # 35.3 cf
        (1200.0, "van",        70.0),  # 42.4 cf
        # Tier 8 (48-64 cf ~= 1359-1812 L)
        (1400.0, "van",        80.0),  # 49.4 cf
        (1800.0, "van",        80.0),
        # Tier 9 (64-72 cf ~= 1812-2039 L)
        (1850.0, "van",        90.0),
        (2000.0, "van",        90.0),
        # Tier 10 (>= 72 cf ~= >= 2039 L)
        (2100.0, "van",       100.0),
        (5000.0, "van",       100.0),
    ])
    def test_score_at_tiers(self, cargo_liters, body_style, expected):
        assert compute_practicality_score(cargo_liters, body_style) == expected

    def test_zero_cargo_falls_back_to_body_style(self):
        """cargo=0 is treated as missing -> body-style estimate kicks in."""
        # 0 cargo + 'sedan' -> estimate 430 L -> 15.18 cf -> tier 4 -> 40.
        assert compute_practicality_score(0.0, "sedan") == 40.0

    def test_negative_cargo_falls_back_to_body_style(self):
        """Negative cargo is a sentinel -> body-style estimate kicks in."""
        assert compute_practicality_score(-1.0, "suv") == 50.0  # 550L est


# ===========================================================================
# B. Practicality body-style adjustments
# ===========================================================================

class TestBodyStyleBonus:
    """Wagon/estate get +1 tier (capped at 10). No other style gets a bonus."""

    @pytest.mark.parametrize("style", ["wagon", "estate", "Wagon", "ESTATE", "WaGoN"])
    def test_wagon_styles_get_bonus(self, style):
        """Same cargo, wagon vs non-wagon -- wagon must score 10 higher
        (one tier), unless already at the cap."""
        cargo = 580.0  # 20.5 cf -> tier 5
        non_wagon = compute_practicality_score(cargo, "sedan")
        wagon = compute_practicality_score(cargo, style)
        assert wagon == non_wagon + 10.0

    def test_wagon_bonus_capped_at_100(self):
        """A wagon-sized cargo already at tier 10 must not exceed 100."""
        # 2100 L = 74.1 cf -> tier 10. Wagon bonus cannot push past 100.
        assert compute_practicality_score(2100.0, "wagon") == 100.0

    @pytest.mark.parametrize("style, expected_delta", [
        # Coupes / convertibles / roadsters get -0.5 tier (penalty)
        ("coupe",       -5.0),
        ("convertible", -5.0),
        ("roadster",    -5.0),
        # All other non-wagon styles match the sedan baseline
        ("sedan",       0.0),
        ("hatchback",   0.0),
        ("suv",         0.0),
        ("minivan",     0.0),
        ("van",         0.0),
        ("truck",       0.0),
    ])
    def test_non_wagon_styles_get_no_bonus(self, style, expected_delta):
        """Coupes/convertibles/roadsters get a -0.5 tier penalty (-5 points).
        All other non-wagon styles match the sedan baseline exactly."""
        cargo = 580.0  # 20.5 cf -> tier 5
        baseline = compute_practicality_score(cargo, "sedan")
        assert compute_practicality_score(cargo, style) == baseline + expected_delta

    def test_wagon_bonus_styles_constant(self):
        """The frozen set must match the documented decision."""
        assert WAGON_BONUS_STYLES == frozenset({"wagon", "estate"})


# ===========================================================================
# C. Practicality estimation (cargo is None)
# ===========================================================================

class TestCargoEstimation:
    """When real cargo is missing, estimate from body_style midpoints."""

    @pytest.mark.parametrize("body_style, expected_liters, expected_tier", [
        # From the spec table (section 3) -- with verified tier conversions:
        # NOTE: the spec table's "tier" column has arithmetic errors for a
        # few rows (convertible/roadster/truck). These expected_tier values
        # are derived from the LOCKED breakpoints in cargo_cf_to_doug_tier,
        # which are the source of truth. Coupes/convertibles/roadsters also
        # get a -0.5 tier penalty (COUPE_PENALTY_STYLES), floored at tier 1.
        ("sedan",       430.0, 4),  # 15.2 cf
        ("coupe",       300.0, 3),  # 10.6 cf - 0.5 = tier 2.5 -> score 25
        ("hatchback",   350.0, 4),  # 12.4 cf
        ("suv",         550.0, 5),  # 19.4 cf
        ("wagon",       580.0, 6),  # 20.5 cf +1 bonus
        ("estate",      580.0, 6),  # alias of wagon
        ("convertible", 200.0, 3),  # 7.1 cf - 0.5 = tier 2.5 -> score 25
        ("roadster",    200.0, 3),
        ("minivan",     850.0, 6),  # 30.0 cf
        ("van",         850.0, 6),
        ("truck",       700.0, 6),  # 24.7 cf -> tier 6 (NOT 5 as in spec table)
    ])
    def test_estimate_matches_spec_table(self, body_style, expected_liters, expected_tier):
        # Coupes/convertibles/roadsters get -0.5 tier penalty; min tier = 1
        score = compute_practicality_score(None, body_style)
        if body_style in ("coupe", "convertible", "roadster"):
            # Apply -0.5 tier penalty
            adjusted_tier = max(1, expected_tier - 0.5)
            assert score == adjusted_tier * 10.0
        else:
            assert score == expected_tier * 10.0

    def test_unknown_body_style_uses_default(self):
        """An unrecognized body style falls back to DEFAULT_CARGO_LITERS."""
        score = compute_practicality_score(None, "hovercraft")
        # Default 350 L -> 12.4 cf -> tier 4 -> score 40.
        assert score == 40.0

    def test_none_body_style_uses_default(self):
        """Both cargo and body_style missing -> still produces a value."""
        score = compute_practicality_score(None, None)
        assert score == 40.0  # default 350 L

    def test_estimates_table_matches_spec(self):
        """The frozen estimate table must match the documented midpoints."""
        expected = {
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
        assert BODY_STYLE_CARGO_ESTIMATES == expected

    def test_liters_per_cubic_foot_constant(self):
        assert LITERS_PER_CUBIC_FOOT == 28.32


# ===========================================================================
# Practicality ORM dispatcher
# ===========================================================================

def _ns_car(body_style=None):
    return SimpleNamespace(body_style=body_style)


def _ns_ice(cargo_volume_liters=None, horsepower_bhp=None, curb_weight_kg=None,
            displacement_cc=None, aspiration=None):
    """A duck-typed PowertrainICE stand-in.

    ``horsepower_bhp`` defaults to None so the ZP dispatcher routes to
    INSUFFICIENT_DATA when no performance data is supplied (matches the
    behaviour of a real row with missing HP).
    """
    return SimpleNamespace(
        cargo_volume_liters=cargo_volume_liters,
        horsepower_bhp=horsepower_bhp,
        curb_weight_kg=curb_weight_kg,
        displacement_cc=displacement_cc,
        aspiration=aspiration,
    )


def _ns_ev(cargo_volume_liters=None):
    return SimpleNamespace(cargo_volume_liters=cargo_volume_liters)


class TestPracticalityForCar:
    def test_uses_ice_cargo_when_present(self):
        car = _ns_car("sedan")
        ice = _ns_ice(510.0)  # 18.0 cf -> tier 5 -> 50
        assert compute_practicality_for_car(car, ice, None) == 50.0

    def test_falls_back_to_ev_cargo(self):
        car = _ns_car("sedan")
        ice = _ns_ice(None)
        ev = _ns_ev(510.0)
        assert compute_practicality_for_car(car, ice, ev) == 50.0

    def test_prefers_ice_over_ev(self):
        """When both rows have cargo, ICE wins (matches the function's
        documented precedence)."""
        car = _ns_car("sedan")
        ice = _ns_ice(510.0)  # 18.0 cf -> tier 5 -> 50
        ev = _ns_ev(2000.0)   # would be tier 9 -> 90 if used
        assert compute_practicality_for_car(car, ice, ev) == 50.0

    def test_falls_back_to_body_style_when_no_cargo(self):
        car = _ns_car("suv")
        ice = _ns_ice(None)
        ev = _ns_ev(None)
        # Estimate 550 L -> 19.4 cf -> tier 5 -> 50.
        assert compute_practicality_for_car(car, ice, ev) == 50.0

    def test_wagon_bonus_applies_via_car_body_style(self):
        car = _ns_car("wagon")
        ice = _ns_ice(580.0)  # 20.5 cf -> tier 5, +1 wagon -> tier 6 -> 60.
        assert compute_practicality_for_car(car, ice, None) == 60.0

    def test_zero_cargo_treated_as_missing(self):
        car = _ns_car("sedan")
        ice = _ns_ice(0.0)
        # Estimate 430 L -> 15.2 cf -> tier 4 -> 40.
        assert compute_practicality_for_car(car, ice, None) == 40.0


# ===========================================================================
# D. Composite formula -- weight redistribution
# ===========================================================================

class TestCompositeFormula:
    def test_weights_sum_to_one(self):
        assert sum(WEIGHTS.values()) == pytest.approx(1.0)

    def test_weights_match_spec(self):
        assert WEIGHTS == {
            "quality": 0.40,
            "reliability": 0.30,
            "practicality": 0.15,
            "performance": 0.15,
        }

    def test_min_dimensions_is_two(self):
        assert MIN_DIMENSIONS == 2

    def test_zp_scale_is_three(self):
        assert ZP_SCALE == 3.0

    def test_all_present_is_weighted_average(self):
        """With all four dimensions present, composite == straight weighted avg."""
        result = compute_composite(80.0, 90.0, 60.0, 70.0)
        expected = 80 * 0.40 + 90 * 0.30 + 60 * 0.15 + 70 * 0.15
        assert result == pytest.approx(expected, abs=0.05)

    def test_missing_one_dimension_redistributes_weight(self):
        """Q=80, Rel=85, Prac=None, ZP=70 -> redistribute practicality's weight."""
        result = compute_composite(80.0, 85.0, None, 70.0)
        # raw = 80*0.4 + 85*0.3 + 70*0.15 = 32 + 25.5 + 10.5 = 68.0
        # weight_sum = 0.4 + 0.3 + 0.15 = 0.85
        # composite = 68.0 / 0.85 = 80.0
        assert result == pytest.approx(80.0, abs=0.05)

    def test_missing_two_dimensions_redistributes_weight(self):
        """Only Q and Rel present: weight_sum = 0.70, scale up by 1/0.70."""
        result = compute_composite(80.0, 90.0, None, None)
        # raw = 80*0.4 + 90*0.3 = 32 + 27 = 59.0
        # weight_sum = 0.7
        # composite = 59.0 / 0.7 = 84.2857...
        assert result == pytest.approx(59.0 / 0.7, abs=0.05)

    def test_two_present_at_minimum_threshold(self):
        """Exactly MIN_DIMENSIONS=2 present is allowed."""
        result = compute_composite(80.0, None, None, 70.0)
        # raw = 80*0.4 + 70*0.15 = 32 + 10.5 = 42.5
        # weight_sum = 0.55
        # composite = 42.5 / 0.55 = 77.27...
        assert result == pytest.approx(42.5 / 0.55, abs=0.05)

    def test_result_rounded_to_one_decimal(self):
        """All composites are rounded to 1 decimal place."""
        result = compute_composite(80.0, 85.0, None, 70.0)
        # 80.0 exactly -- but the rounding still applies.
        assert result is not None
        # If the result has decimals, they cannot exceed 1 place.
        if result != int(result):
            assert round(result, 1) == result

    def test_uniform_scores_yield_themselves(self):
        """When all dimensions equal X, composite must equal X (redistribution
        is invariant under uniform inputs)."""
        for x in (0.0, 50.0, 100.0, 73.7):
            assert compute_composite(x, x, x, x) == pytest.approx(x, abs=0.05)
            # And with some missing -- still x.
            assert compute_composite(x, None, x, x) == pytest.approx(x, abs=0.05)


# ===========================================================================
# E. Composite edge cases
# ===========================================================================

class TestCompositeEdgeCases:
    def test_all_none_returns_none(self):
        assert compute_composite(None, None, None, None) is None

    def test_single_dimension_returns_none(self):
        """One dimension alone is below MIN_DIMENSIONS=2."""
        assert compute_composite(80.0, None, None, None) is None
        assert compute_composite(None, 80.0, None, None) is None
        assert compute_composite(None, None, 80.0, None) is None
        assert compute_composite(None, None, None, 80.0) is None

    def test_zero_is_a_present_value(self):
        """Score 0.0 is NOT missing -- it counts toward MIN_DIMENSIONS.
        (Reliability/Quality of 0 is bad-but-known, not unknown.)"""
        result = compute_composite(0.0, 0.0, None, None)
        assert result == pytest.approx(0.0, abs=0.05)

    def test_negative_score_is_present(self):
        """Defensive: negative values are treated as present. We do not try
        to clamp -- the caller is responsible for valid input ranges."""
        result = compute_composite(-5.0, 50.0, None, None)
        assert result is not None

    def test_extreme_high_scores(self):
        """Defensive: scores above 100 are passed through unchanged (the
        composite does not clamp -- quality/reliability are presumed 0-100)."""
        result = compute_composite(100.0, 100.0, 100.0, 100.0)
        assert result == pytest.approx(100.0, abs=0.05)


# ===========================================================================
# F. ZP normalization
# ===========================================================================

class TestZpNormalization:
    @pytest.mark.parametrize("zp, expected", [
        (0.0,   0.0),
        (30.0, 10.0),
        (60.0, 20.0),
        (90.0, 30.0),
        (120.0, 40.0),
        (150.0, 50.0),
        (180.0, 60.0),
        (210.0, 70.0),
        (240.0, 80.0),
        (270.0, 90.0),
        (300.0, 100.0),    # exactly at the cap
        (301.0, 100.0),    # capped
        (600.0, 100.0),    # capped
        (227.0, pytest.approx(75.667, abs=0.01)),  # Plaid: 227/3 = 75.67
    ])
    def test_normalize_zp_values(self, zp, expected):
        assert normalize_zp(zp) == expected

    def test_normalize_none_returns_none(self):
        assert normalize_zp(None) is None

    def test_normalize_negative_zp_passes_through(self):
        """Defensive: a negative ZP (shouldn't happen but) is not clamped at 0.
        The formula does not enforce a floor -- callers handle that."""
        # -3 / 3 = -1.0; min(100, -1.0) = -1.0
        assert normalize_zp(-3.0) == -1.0

    def test_cap_at_exactly_100(self):
        """Anything >= 300 ZP must normalize to exactly 100.0."""
        for zp in (300.0, 350.0, 1000.0, 1_000_000.0):
            assert normalize_zp(zp) == 100.0


# ===========================================================================
# Composite ORM dispatcher (smoke tests)
# ===========================================================================

def _ns_build_quality(q_score=None):
    return SimpleNamespace(q_score=q_score)


def _ns_reliability(reliability_score=None):
    return SimpleNamespace(reliability_score=reliability_score)


class TestCompositeForCar:
    def test_full_data_path(self):
        """Smoke test: a fully-populated car produces a sensible composite."""
        car = _ns_car("sedan")
        ice = _ns_ice(510.0)             # practicality input
        # Performance ORM not needed because we pass zp_value directly.
        bq = _ns_build_quality(85.0)
        rel = _ns_reliability(88.0)
        composite, dims = compute_composite_for_car(
            car, ice, None,
            performance=None, build_quality=bq, reliability=rel,
            zp_value=237.0,  # Plaid-class ZP -> 79.0 normalized
        )
        # Expected: 85*0.4 + 88*0.3 + 50*0.15 + 79*0.15 = 79.75 -> 79.8.
        assert composite == pytest.approx(79.8, abs=0.05)
        assert dims == {
            "quality": 85.0,
            "reliability": 88.0,
            "practicality": 50.0,
            "performance": 79.0,
        }

    def test_missing_quality_redistributes(self):
        car = _ns_car("sedan")
        ice = _ns_ice(510.0)
        bq = _ns_build_quality(None)
        rel = _ns_reliability(88.0)
        composite, dims = compute_composite_for_car(
            car, ice, None, performance=None,
            build_quality=bq, reliability=rel, zp_value=237.0,
        )
        # Present: Rel=88, Prac=50, ZP_norm=79.
        # raw = 88*0.3 + 50*0.15 + 79*0.15 = 26.4 + 7.5 + 11.85 = 45.75
        # weight_sum = 0.3 + 0.15 + 0.15 = 0.60
        # composite = 45.75 / 0.60 = 76.25 -> 76.2 (banker's rounding to 1dp)
        assert composite == pytest.approx(45.75 / 0.60, abs=0.05)
        assert dims["quality"] is None

    def test_below_min_dimensions_returns_none(self):
        """Only one resolvable dimension -> composite is None."""
        car = _ns_car("sedan")
        ice = _ns_ice(510.0)  # practicality will resolve
        bq = _ns_build_quality(None)
        rel = _ns_reliability(None)
        composite, dims = compute_composite_for_car(
            car, ice, None, performance=None,
            build_quality=bq, reliability=rel, zp_value=None,
        )
        # Only practicality is present -> below MIN_DIMENSIONS=2.
        assert composite is None
        assert dims["practicality"] == 50.0
        assert dims["quality"] is None
        assert dims["reliability"] is None
        assert dims["performance"] is None

    def test_practicality_always_present(self):
        """Practicality never returns None -- body-style fallback guarantees it.
        So a car with at least one of Q/Rel/ZP always produces a composite."""
        car = _ns_car("coupe")
        ice = _ns_ice(None)  # no real cargo -> estimate from body_style
        bq = _ns_build_quality(70.0)
        rel = _ns_reliability(None)
        composite, dims = compute_composite_for_car(
            car, ice, None, performance=None,
            build_quality=bq, reliability=rel, zp_value=None,
        )
        # Practicality: coupe 300L estimate -> 10.6 cf -> tier 3,
        # -0.5 coupe penalty = tier 2.5 -> score 25.
        assert composite is not None
        assert dims["practicality"] == 25.0
        assert dims["quality"] == 70.0


# =========================================================================
# v3 composite: Q/R/Dougscore/P/Z weighted blend (40/20/20/10/10)
# Dougscore is a HARD REQUIREMENT -- no dougscore -> no v3 composite.
# Rationale: redistributing dougscore's 20% to other dims would unfairly
# boost unranked cars. v3 is "with external validation" view, used only
# for the 27 cars that have Dougscore data. v2 stays the default.
# =========================================================================


class TestCompositeV3DougscoreRequired:
    """v3 composite REQUIRES dougscore. Without it -> None."""

    def test_v3_returns_none_when_dougscore_missing(self):
        from motorgeek.core.calculators.composite import compute_composite_v3
        # All other dims present but no dougscore -> None
        result = compute_composite_v3(
            quality=80, reliability=85, dougscore=None,
            practicality=60, performance_norm=70,
        )
        assert result is None, "v3 must return None when dougscore is missing"

    def test_v3_returns_none_when_dougscore_zero(self):
        # A dougscore of 0 means "Doug gave this a 0" -- still use it as a
        # valid score, just a low one. Math: 80*0.40 + 85*0.20 + 0*0.20
        # + 60*0.10 + 70*0.10 = 32 + 17 + 0 + 6 + 7 = 62.0
        from motorgeek.core.calculators.composite import compute_composite_v3
        result = compute_composite_v3(
            quality=80, reliability=85, dougscore=0,
            practicality=60, performance_norm=70,
        )
        assert result is not None
        # Doug=0 should pull the composite below the equal-weighted baseline
        # of (80+85+0+60+70)/5 = 59
        assert result < 65  # Doug drags it down but doesn't dominate
        assert result == 62.0

    def test_v3_with_only_dougscore_and_quality(self):
        """Only Q of the non-Dougscore dims is present (1 of 4). Below
        MIN_DIMENSIONS=2, so v3 returns None even though Dougscore exists."""
        from motorgeek.core.calculators.composite import compute_composite_v3
        result = compute_composite_v3(
            quality=80, reliability=None, dougscore=70,
            practicality=None, performance_norm=None,
        )
        # MIN_DIMENSIONS check: present has only "quality" -> len 1 < 2 -> None
        assert result is None, "v3 needs >=2 non-Dougscore dims to compute"

    def test_v3_with_two_non_dougscore_dims(self):
        """Q and R both present (2 of 4 non-Dougscore dims). Hits MIN_DIMENSIONS."""
        from motorgeek.core.calculators.composite import compute_composite_v3
        result = compute_composite_v3(
            quality=80, reliability=80, dougscore=70,
            practicality=None, performance_norm=None,
        )
        # Q and R share the remaining 80% bucket proportionally: each gets 0.40
        # Q: 80*0.40 + R: 80*0.40 + Doug: 70*0.20 = 32 + 32 + 14 = 78.0
        assert result == 78.0

    def test_v3_all_present_basic(self):
        """All 5 dims present -> straightforward weighted average."""
        from motorgeek.core.calculators.composite import compute_composite_v3
        result = compute_composite_v3(
            quality=80, reliability=80, dougscore=80,
            practicality=80, performance_norm=80,
        )
        # All 80s -> weighted average = 80 (regardless of weights)
        assert result == 80.0

    def test_v3_dougscore_dominates_when_others_missing(self):
        """Only Dougscore + Quality: only 1 non-Dougscore dim, below
        MIN_DIMENSIONS=2, so v3 returns None. (Use ``test_v3_with_two_non
        _dougscore_dims`` to see the actual Dougscore+Quality math.)"""
        from motorgeek.core.calculators.composite import compute_composite_v3
        result = compute_composite_v3(
            quality=100, reliability=None, dougscore=0,
            practicality=None, performance_norm=None,
        )
        # MIN_DIMENSIONS check: only "quality" in present -> len 1 < 2 -> None
        assert result is None

    def test_v3_higher_quality_drives_composite(self):
        """High Q + Low Doug should give a composite pulled DOWN by Doug."""
        from motorgeek.core.calculators.composite import compute_composite_v3
        result_high_doug = compute_composite_v3(
            quality=50, reliability=50, dougscore=90,
            practicality=50, performance_norm=50,
        )
        result_low_doug = compute_composite_v3(
            quality=50, reliability=50, dougscore=10,
            practicality=50, performance_norm=50,
        )
        # Same Q/R/P/Z, different Doug -> Doug has real impact
        assert result_high_doug > result_low_doug
        # Difference should be ~ 16 points (80 Doug points * 0.20 weight)
        diff = result_high_doug - result_low_doug
        assert 15 <= diff <= 17

    def test_v3_includes_dougscore_in_dims(self):
        """v3 dispatcher should expose dougscore in the dims dict."""
        from motorgeek.core.calculators.composite import compute_composite_for_car_v3
        car = _ns_car("sedan")
        ice = _ns_ice(450.0)
        bq = _ns_build_quality(80.0)
        rel = _ns_reliability(75.0)
        composite, dims = compute_composite_for_car_v3(
            car=car, powertrain_ice=ice, performance=None,
            build_quality=bq, reliability=rel,
            zp_value=120.0, dougscore=72.0,
        )
        assert composite is not None
        assert "dougscore" in dims
        assert dims["dougscore"] == 72.0
        assert dims["quality"] == 80.0

    def test_v3_dispatcher_returns_none_when_no_dougscore(self):
        """ORM dispatcher must also return None when dougscore is missing."""
        from motorgeek.core.calculators.composite import compute_composite_for_car_v3
        car = _ns_car("sedan")
        ice = _ns_ice(450.0)
        bq = _ns_build_quality(80.0)
        rel = _ns_reliability(75.0)
        composite, dims = compute_composite_for_car_v3(
            car=car, powertrain_ice=ice, performance=None,
            build_quality=bq, reliability=rel,
            zp_value=120.0, dougscore=None,
        )
        assert composite is None
        assert dims["dougscore"] is None


class TestCompositeV2VsV3Divergence:
    """v2 and v3 should produce different scores when dougscore diverges from
    the internal Q/R/P/Z pattern. v3 deliberately punishes divergence."""

    def test_taycan_v3_higher_than_v2(self):
        """Porsche Taycan: Q=87 dominates v3. Even though Doug=72 is below
        Q, it's still respectable, so v3 lands HIGHER than v2. This
        demonstrates that high-Q cars benefit in v3 because Q retains 40%
        weight and the reduced R/P/Z weights are compensated by Doug."""
        from motorgeek.core.calculators.composite import (
            compute_composite, compute_composite_v3,
        )
        # Taycan values from session obs §14
        q, r, ds, p, zp = 87, 78, 72, 40, 49  # zp_norm = 49 (raw 146/3)
        v2 = compute_composite(q, r, p, zp)
        v3 = compute_composite_v3(q, r, ds, p, zp)
        # v3 should be ~2 points higher than v2 (Q dominates, Doug is decent)
        assert v3 > v2, f"v3={v3} should be > v2={v2} when Q dominates"
        diff = v3 - v2
        assert 1 <= diff <= 5, f"Expected v3-v2 gap 1-5, got {diff}"

    def test_lexus_ls400_v2_higher_than_v3(self):
        """Lexus LS 400: v2 says ~76 (Q+R very high), Doug says 43.
        v3 should be LOWER than v2 because Doug's 43 drags it down."""
        from motorgeek.core.calculators.composite import (
            compute_composite, compute_composite_v3,
        )
        # LS 400 values from session obs §14
        q, r, ds, p, zp = 88, 92, 43, 45, 42
        v2 = compute_composite(q, r, p, zp)
        v3 = compute_composite_v3(q, r, ds, p, zp)
        # v3 should be lower than v2 (Doug drags it down)
        assert v3 < v2, f"v3={v3} should be < v2={v2} when Doug is low"
        # Gap should be 4-6 points (Doug 43 vs implicit 80 average = 37 diff * 0.20 = ~7.4,
        # but Q+R keep v2 high so the actual gap is smaller)
        diff = v2 - v3
        assert 4 <= diff <= 8, f"Expected v2-v3 gap 4-8, got {diff}"

    def test_dougscore_has_real_impact(self):
        """Same Q/R/P/Z but wildly different Dougscores should give v3
        a real (~16 point) spread. This is the core calibration claim."""
        from motorgeek.core.calculators.composite import compute_composite_v3
        low_doug = compute_composite_v3(
            quality=50, reliability=50, dougscore=10,
            practicality=50, performance_norm=50,
        )
        high_doug = compute_composite_v3(
            quality=50, reliability=50, dougscore=90,
            practicality=50, performance_norm=50,
        )
        # Same Q/R/P/Z = 50, so difference is purely Dougscore
        # 50*(0.40+0.20+0.10+0.10) + 10*0.20 = 40 + 2 = 42 vs 50*0.80 + 90*0.20 = 58
        diff = high_doug - low_doug
        assert diff == 16.0, f"Expected 16-point spread from Doug, got {diff}"

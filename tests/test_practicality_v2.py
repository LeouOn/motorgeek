"""Tests for the v2 practicality formula with enrichment bonuses.

The v2 formula extends the v1 (cargo + wagon bonus + coupe penalty) with
4 small additive bonuses (each +0.5 tier, capped at 10):
  - cargo_volume_liters_seats_down > 1500L  (significant cargo flexibility)
  - seat_count >= 7  (3-row / family hauler)
  - rear_legroom_mm > 950  (adults sit comfortably in back)
  - tow_capacity_kg > 2000  ("a little benefit for towing")

Plus a body-style penalty (-0.5 tier, floored at 1) for 2-door cars:
  - coupe, convertible, roadster  (limited rear-seat access)
"""
from __future__ import annotations

import pytest

from motorgeek.core.calculators.practicality import (
    BODY_STYLE_CARGO_ESTIMATES,
    CARGO_DOWN_BONUS_THRESHOLD_L,
    COUPE_PENALTY_INCREMENT,
    COUPE_PENALTY_STYLES,
    REAR_LEGROOM_BONUS_THRESHOLD_MM,
    SEAT_COUNT_BONUS_THRESHOLD,
    TOW_CAPACITY_BONUS_THRESHOLD_KG,
    WAGON_BONUS_STYLES,
    _TIER_MAX,
    cargo_cf_to_doug_tier,
    compute_practicality_for_car,
    compute_practicality_for_car_v2,
    compute_practicality_score,
    compute_practicality_v2,
)


# --- Tier mapping -----------------------------------------------------------

class TestCargoCfToDougTier:
    """The Doug Score tier breakpoints in cubic feet."""

    def test_zero_cargo_is_tier_1(self):
        assert cargo_cf_to_doug_tier(0) == 1

    def test_just_under_first_breakpoint(self):
        # Just under 3 cf -> tier 1
        assert cargo_cf_to_doug_tier(2.99) == 1

    def test_at_3_cf_is_tier_2(self):
        assert cargo_cf_to_doug_tier(3.0) == 2

    def test_6_5_cf_boundary(self):
        # 6.4 -> tier 2; 6.5 -> tier 3
        assert cargo_cf_to_doug_tier(6.4) == 2
        assert cargo_cf_to_doug_tier(6.5) == 3

    def test_midrange_tiers(self):
        # 11 cf = tier 3 boundary, 11.1 = tier 4
        assert cargo_cf_to_doug_tier(10.99) == 3
        assert cargo_cf_to_doug_tier(11.0) == 4
        # 16 cf boundary
        assert cargo_cf_to_doug_tier(15.99) == 4
        assert cargo_cf_to_doug_tier(16.0) == 5

    def test_top_end_uses_max_tier(self):
        # Anything at or above the largest breakpoint (72 cf) -> tier 10
        assert cargo_cf_to_doug_tier(72.0) == _TIER_MAX
        assert cargo_cf_to_doug_tier(100.0) == _TIER_MAX
        assert cargo_cf_to_doug_tier(1000.0) == _TIER_MAX

    def test_real_car_examples(self):
        # Sanity-check known cars:
        # Honda S2000: 143L = 5.05 cf -> tier 2
        assert cargo_cf_to_doug_tier(143 / 28.32) == 2
        # Mazda MX-5: 130L = 4.59 cf -> tier 2
        assert cargo_cf_to_doug_tier(130 / 28.32) == 2
        # Ford F-150: 1700L = 60.0 cf -> tier 8 (in [48, 64))
        assert cargo_cf_to_doug_tier(1700 / 28.32) == 8
        # Honda Civic: 440L = 15.5 cf -> tier 4 (in [11, 16))
        assert cargo_cf_to_doug_tier(440 / 28.32) == 4


# --- v1 backwards compatibility --------------------------------------------

class TestV1BackwardsCompatible:
    """v1 formula: cargo + wagon bonus only, no enrichment bonuses."""

    def test_cargo_only_no_bonuses(self):
        # 500L = 17.66 cf -> tier 5, no wagon -> tier 5, score 50
        assert compute_practicality_score(500, "sedan") == 50

    def test_wagon_bonus_applied(self):
        # 580L = 20.5 cf -> tier 5, wagon bonus +1 -> tier 6, score 60
        assert compute_practicality_score(580, "wagon") == 60

    def test_estate_also_gets_bonus(self):
        assert compute_practicality_score(580, "estate") == 60

    def test_wagon_bonus_caps_at_10(self):
        # 2832L = 100 cf -> tier 10, +1 wagon = capped at 10
        assert compute_practicality_score(2832, "wagon") == 100

    def test_no_other_body_style_adjustments(self):
        # Sedan, SUV, hatchback -- no tier adjustments beyond wagon/coupe
        # 500L = 17.66 cf -> tier 5, no bonus
        assert compute_practicality_score(500, "sedan") == 50
        assert compute_practicality_score(500, "suv") == 50
        assert compute_practicality_score(500, "hatchback") == 50
        # Coupe/convertible/roadster get -0.5 tier penalty
        # 500L = 17.66 cf -> tier 5, -0.5 = tier 4.5 -> score 45
        assert compute_practicality_score(500, "coupe") == 45
        # 200L = 7.06 cf -> tier 3, -0.5 = tier 2.5 -> score 25
        assert compute_practicality_score(200, "convertible") == 25
        assert compute_practicality_score(200, "roadster") == 25

    def test_falls_back_to_body_style_estimate(self):
        # cargo_liters=None -> use body_style estimate
        # sedan default = 430L = 15.2 cf -> tier 4
        assert compute_practicality_score(None, "sedan") == 40
        # suv default = 550L = 19.4 cf -> tier 5
        assert compute_practicality_score(None, "suv") == 50
        # wagon default = 580L = 20.5 cf -> tier 5 +1 = tier 6
        assert compute_practicality_score(None, "wagon") == 60

    def test_unknown_body_style_falls_back_to_compact(self):
        # None body_style -> 350L default (compact) = 12.36 cf -> tier 4
        assert compute_practicality_score(None, None) == 40

    def test_zero_or_negative_cargo_falls_back(self):
        # 0 or negative cargo -> use body_style estimate
        assert compute_practicality_score(0, "sedan") == 40
        assert compute_practicality_score(-10, "sedan") == 40


# --- v2 enrichment bonuses --------------------------------------------------

class TestV2EnrichmentBonuses:
    """The 4 small additive bonuses, each +0.5 tier."""

    def test_cargo_seats_down_bonus(self):
        # Tier 5 base (500L = 17.66 cf), no cargo_down -> no bonus
        score, bonuses = compute_practicality_v2(
            cargo_liters_seats_up=500, body_style="sedan",
        )
        assert score == 50
        assert bonuses["cargo_seats_down"] is False

        # cargo_down > 1500 -> bonus
        score, bonuses = compute_practicality_v2(
            cargo_liters_seats_up=500, body_style="sedan",
            cargo_liters_seats_down=1600,
        )
        assert score == 55
        assert bonuses["cargo_seats_down"] is True

        # cargo_down = 1500 (boundary) -> no bonus (must be STRICTLY greater)
        score, bonuses = compute_practicality_v2(
            cargo_liters_seats_up=500, body_style="sedan",
            cargo_liters_seats_down=1500,
        )
        assert score == 50
        assert bonuses["cargo_seats_down"] is False

    def test_seat_count_bonus(self):
        # 5 seats -> no bonus
        score, bonuses = compute_practicality_v2(
            cargo_liters_seats_up=500, body_style="sedan", seat_count=5,
        )
        assert score == 50
        assert bonuses["seat_count"] is False

        # 7 seats -> bonus
        score, bonuses = compute_practicality_v2(
            cargo_liters_seats_up=500, body_style="sedan", seat_count=7,
        )
        assert score == 55
        assert bonuses["seat_count"] is True

        # 8 seats -> bonus
        score, bonuses = compute_practicality_v2(
            cargo_liters_seats_up=500, body_style="sedan", seat_count=8,
        )
        assert score == 55

        # 6 seats -> no bonus
        score, bonuses = compute_practicality_v2(
            cargo_liters_seats_up=500, body_style="sedan", seat_count=6,
        )
        assert score == 50

    def test_rear_legroom_bonus(self):
        # 940mm -> no bonus
        score, bonuses = compute_practicality_v2(
            cargo_liters_seats_up=500, body_style="sedan", rear_legroom_mm=940,
        )
        assert score == 50
        assert bonuses["rear_legroom"] is False

        # 951mm -> bonus
        score, bonuses = compute_practicality_v2(
            cargo_liters_seats_up=500, body_style="sedan", rear_legroom_mm=951,
        )
        assert score == 55
        assert bonuses["rear_legroom"] is True

        # 950mm (boundary) -> no bonus
        score, bonuses = compute_practicality_v2(
            cargo_liters_seats_up=500, body_style="sedan", rear_legroom_mm=950,
        )
        assert score == 50

    def test_tow_capacity_bonus(self):
        # 1999kg -> no bonus
        score, bonuses = compute_practicality_v2(
            cargo_liters_seats_up=500, body_style="sedan", tow_capacity_kg=1999,
        )
        assert score == 50
        assert bonuses["tow_capacity"] is False

        # 2001kg -> bonus
        score, bonuses = compute_practicality_v2(
            cargo_liters_seats_up=500, body_style="sedan", tow_capacity_kg=2001,
        )
        assert score == 55
        assert bonuses["tow_capacity"] is True

    def test_all_four_bonuses_combine(self):
        # Tier 5 base (500L) + 4 bonuses = tier 7 = 70
        score, bonuses = compute_practicality_v2(
            cargo_liters_seats_up=500, body_style="sedan",
            cargo_liters_seats_down=2000, seat_count=7,
            rear_legroom_mm=1000, tow_capacity_kg=3000,
        )
        assert score == 70
        # All 4 enrichment bonuses should be applied. coupe_penalty is False
        # because body_style="sedan".
        assert bonuses["cargo_seats_down"] is True
        assert bonuses["seat_count"] is True
        assert bonuses["rear_legroom"] is True
        assert bonuses["tow_capacity"] is True
        assert bonuses["coupe_penalty"] is False

    def test_caps_at_10(self):
        # Tier 10 base + 4 bonuses = capped at 10 = 100
        score, bonuses = compute_practicality_v2(
            cargo_liters_seats_up=2832, body_style="sedan",  # 100 cf = tier 10
            cargo_liters_seats_down=2000, seat_count=7,
            rear_legroom_mm=1000, tow_capacity_kg=3000,
        )
        assert score == 100

    def test_wagon_bonus_plus_enrichment(self):
        # Wagon base bonus: tier 5 + 1 = 6
        # Plus cargo_down bonus: 6 + 0.5 = 6.5 -> score 65
        score, bonuses = compute_practicality_v2(
            cargo_liters_seats_up=580, body_style="wagon",  # 20.5 cf = tier 5
            cargo_liters_seats_down=2000,
        )
        assert score == 65
        assert bonuses["cargo_seats_down"] is True


# --- v2 missing-field behavior --------------------------------------------

class TestV2MissingFields:
    """When enrichment data is missing, v2 falls back to v1 behavior."""

    def test_none_fields_no_bonuses(self):
        score, bonuses = compute_practicality_v2(
            cargo_liters_seats_up=550, body_style="suv",
        )
        assert score == 50
        assert all(v is False for v in bonuses.values())

    def test_partial_enrichment(self):
        # Only one of the 4 enrichment fields is set
        score, bonuses = compute_practicality_v2(
            cargo_liters_seats_up=500, body_style="sedan",
            seat_count=7,
        )
        assert score == 55
        assert bonuses["seat_count"] is True
        assert bonuses["cargo_seats_down"] is False
        assert bonuses["rear_legroom"] is False
        assert bonuses["tow_capacity"] is False

    def test_cargo_seats_up_none_uses_body_style(self):
        # No real cargo data -> falls back to body_style estimate
        # sedan default = 430L = 15.2 cf -> tier 4
        score, bonuses = compute_practicality_v2(
            cargo_liters_seats_up=None, body_style="sedan",
            seat_count=7,
        )
        assert score == 45  # tier 4 + 0.5 bonus
        assert bonuses["seat_count"] is True


# --- Real car integration (v2 should match v2 published expectations) -----

class TestRealCarScenarios:
    """End-to-end scenarios matching the top-30 leaderboard changes."""

    def test_lexus_ls400_with_enrichment(self):
        """LS400: tier 3 cargo + rear legroom bonus."""
        # LS400: 430L = 15.2 cf = tier 4, rear_legroom 970mm
        # No wagon (sedan), cargo_down NULL, seat 5, tow 0
        score, bonuses = compute_practicality_v2(
            cargo_liters_seats_up=430, body_style="sedan",
            cargo_liters_seats_down=None, seat_count=5,
            rear_legroom_mm=970, tow_capacity_kg=0,
        )
        assert score == 45  # tier 4 + 0.5 (rear_legroom)
        assert bonuses["rear_legroom"] is True
        assert bonuses["cargo_seats_down"] is False
        assert bonuses["seat_count"] is False
        assert bonuses["tow_capacity"] is False

    def test_bmw_x5_g05_double_bonus(self):
        """X5 G05: cargo_down + rear legroom + tow all qualify."""
        # X5: tier 6 cargo (818L = 28.9 cf) + cargo_down 1870L (bonus)
        # + rear_legroom 980 (bonus) + tow 2700 (bonus) = tier 7.5 = 75
        score, bonuses = compute_practicality_v2(
            cargo_liters_seats_up=818, body_style="suv",  # tier 6
            cargo_liters_seats_down=1870,  # > 1500 -> bonus
            seat_count=5,
            rear_legroom_mm=980,  # > 950 -> bonus
            tow_capacity_kg=2700,  # > 2000 -> bonus
        )
        assert score == 75  # tier 6 + 0.5 + 0.5 + 0.5 = 7.5
        assert bonuses["cargo_seats_down"] is True
        assert bonuses["rear_legroom"] is True
        assert bonuses["tow_capacity"] is True
        assert bonuses["seat_count"] is False

    def test_civic_type_r_no_bonuses(self):
        """Civic Type R: tight rear legroom, no tow, no bonus."""
        # 4 seats, 818mm legroom (well under 950), no tow
        # 504L = 17.8 cf = tier 5 (in [16, 24))
        score, bonuses = compute_practicality_v2(
            cargo_liters_seats_up=504, body_style="hatchback",
            cargo_liters_seats_down=1308,
            seat_count=4,
            rear_legroom_mm=818,  # NO bonus
            tow_capacity_kg=0,
        )
        assert score == 50  # tier 5 only, no bonuses qualify
        assert all(v is False for v in bonuses.values())


# --- Coupe penalty (2026-06-18) ---------------------------------------------

class TestCoupePenalty:
    """2-door cars (coupe/convertible/roadster) get -0.5 tier penalty.

    Rationale: a 2-door with 400L cargo is materially less practical than
    a 4-door sedan with 400L -- rear-seat access is limited. The penalty
    is small (-0.5 tier = -5 P-points) and floored at tier 1 so even tiny
    2-door cars score at least 10.
    """

    def test_coupe_penalty_applied(self):
        # 500L = 17.66 cf -> tier 5, -0.5 = tier 4.5 -> score 45
        assert compute_practicality_score(500, "coupe") == 45

    def test_convertible_penalty_applied(self):
        # Same as coupe
        assert compute_practicality_score(500, "convertible") == 45

    def test_roadster_penalty_applied(self):
        assert compute_practicality_score(500, "roadster") == 45

    def test_coupe_floor_at_tier_1(self):
        # 130L (Porsche 911 Turbo-like) = 4.59 cf -> tier 2, -0.5 = tier 1.5 -> score 15
        assert compute_practicality_score(130, "coupe") == 15
        # 50L (tiny 2-seat roadster) = 1.77 cf -> tier 1, -0.5 = tier 0.5 -> floored at 1 -> score 10
        assert compute_practicality_score(50, "roadster") == 10
        # 0L with body_style=coupe -> falls back to body estimate 300L = 10.6 cf -> tier 3
        # -0.5 = tier 2.5 -> score 25
        assert compute_practicality_score(None, "coupe") == 25

    def test_coupe_penalty_with_enrichment(self):
        # Porsche 911 with seats_down bonus? Unlikely but possible
        # 400L = 14.1 cf -> tier 4, -0.5 = tier 3.5, + cargo_down bonus = tier 4.0 -> score 40
        score, bonuses = compute_practicality_v2(
            cargo_liters_seats_up=400, body_style="coupe",
            cargo_liters_seats_down=1600,
        )
        assert score == 40  # tier 4 - 0.5 + 0.5 = tier 4
        assert bonuses["cargo_seats_down"] is True
        assert bonuses["coupe_penalty"] is True

    def test_wagon_takes_precedence_over_coupe(self):
        # An "estate" body style should get the wagon bonus, not the coupe penalty.
        # A 2-door estate is unusual but if the body_style says estate, wagon wins.
        # 580L = 20.5 cf -> tier 5, wagon +1 = tier 6, score 60
        assert compute_practicality_score(580, "estate") == 60

    def test_sedan_no_penalty(self):
        # Sedan doesn't get the coupe penalty
        # 500L = tier 5 = score 50
        assert compute_practicality_score(500, "sedan") == 50

    def test_suv_no_penalty(self):
        # SUV doesn't get the coupe penalty
        assert compute_practicality_score(500, "suv") == 50

    def test_hatchback_no_penalty(self):
        # Hatchback doesn't get the coupe penalty (it has 4 doors + tailgate)
        assert compute_practicality_score(500, "hatchback") == 50


# --- Module-level sanity ---------------------------------------------------

class TestThresholds:
    """The bonus thresholds are frozen -- verify they match the design."""

    def test_thresholds_match_design(self):
        # From the design doc:
        assert CARGO_DOWN_BONUS_THRESHOLD_L == 1500.0
        assert SEAT_COUNT_BONUS_THRESHOLD == 7
        assert REAR_LEGROOM_BONUS_THRESHOLD_MM == 950.0
        assert TOW_CAPACITY_BONUS_THRESHOLD_KG == 2000

    def test_wagon_bonus_styles_frozen(self):
        assert WAGON_BONUS_STYLES == frozenset({"wagon", "estate"})

    def test_coupe_penalty_styles_frozen(self):
        assert COUPE_PENALTY_STYLES == frozenset({"coupe", "convertible", "roadster"})

    def test_coupe_penalty_increment_is_negative_half(self):
        assert COUPE_PENALTY_INCREMENT == -0.5

    def test_body_style_estimates_cover_main_types(self):
        required = {"sedan", "coupe", "hatchback", "suv", "wagon",
                    "estate", "convertible", "roadster", "minivan", "van", "truck"}
        assert required.issubset(BODY_STYLE_CARGO_ESTIMATES.keys())

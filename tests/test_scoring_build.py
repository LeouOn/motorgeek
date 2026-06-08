"""Tests for build quality scoring module."""

from types import SimpleNamespace

import pytest

from motorgeek.core.scoring_build import (
    BUILD_DIMENSIONS,
    BUILD_WEIGHTS,
    MIN_DIMENSIONS_FOR_AGGREGATE,
    compute_build_aggregate,
    get_build_score_dict,
    recompute_build_aggregate,
)


# --- Constants ---

class TestBuildWeights:
    """Validate weight configuration."""

    def test_weights_sum_to_one(self):
        assert sum(BUILD_WEIGHTS.values()) == pytest.approx(1.0)

    def test_six_dimensions_have_weights(self):
        assert len(BUILD_WEIGHTS) == 6
        for dim in BUILD_DIMENSIONS:
            assert dim in BUILD_WEIGHTS

    def test_dimensions_list_matches_weights_keys(self):
        assert set(BUILD_DIMENSIONS) == set(BUILD_WEIGHTS.keys())


# --- compute_build_aggregate ---

class TestComputeBuildAggregate:
    """Validate weighted aggregate computation."""

    def test_all_scores_present(self):
        scores = {
            'body_construction': 90,
            'nvh_isolation': 85,
            'interior_materials': 88,
            'paint_corrosion': 82,
            'electrical_aging': 80,
            'cosmetic_aging': 78,
        }
        # 90*0.25 + 85*0.10 + 88*0.20 + 82*0.15 + 80*0.15 + 78*0.15
        # = 22.5 + 8.5 + 17.6 + 12.3 + 12.0 + 11.7 = 84.6
        assert compute_build_aggregate(scores) == 84.6

    def test_min_three_dimensions_required(self):
        """Two dimensions should return None."""
        scores = {
            'body_construction': 90,
            'nvh_isolation': 85,
        }
        assert compute_build_aggregate(scores) is None

    def test_three_dimensions_ok(self):
        scores = {
            'body_construction': 100,
            'nvh_isolation': 100,
            'interior_materials': 100,
        }
        # weights: 0.25 + 0.10 + 0.20 = 0.55
        # adjusted: 0.25/0.55=0.4545..., 0.10/0.55=0.1818..., 0.20/0.55=0.3636...
        # 100 * sum(adjusted) = 100.0
        assert compute_build_aggregate(scores) == 100.0

    def test_null_dimensions_excluded_weights_redistributed(self):
        scores = {
            'body_construction': 80,
            'nvh_isolation': None,
            'interior_materials': 90,
            'paint_corrosion': None,
            'electrical_aging': 70,
            'cosmetic_aging': 60,
        }
        # Present: body=80(0.25), interior=90(0.20), electrical=70(0.15), cosmetic=60(0.15)
        # weight_sum = 0.75
        # adjusted: 0.25/0.75, 0.20/0.75, 0.15/0.75, 0.15/0.75
        # raw = 80*(1/3) + 90*(0.2667) + 70*(0.2) + 60*(0.2)
        result = compute_build_aggregate(scores)
        assert result is not None
        assert isinstance(result, float)

    def test_perfect_score(self):
        scores = {dim: 100.0 for dim in BUILD_DIMENSIONS}
        assert compute_build_aggregate(scores) == 100.0

    def test_zero_score(self):
        scores = {dim: 0.0 for dim in BUILD_DIMENSIONS}
        assert compute_build_aggregate(scores) == 0.0

    def test_rounded_to_one_decimal(self):
        scores = {
            'body_construction': 91,
            'nvh_isolation': 83,
            'interior_materials': 77,
            'paint_corrosion': 85,
            'electrical_aging': 72,
            'cosmetic_aging': 68,
        }
        result = compute_build_aggregate(scores)
        assert result is not None
        # Verify result has at most 1 decimal place
        assert result == round(result, 1)

    def test_extra_keys_ignored(self):
        scores = {
            'body_construction': 100,
            'nvh_isolation': 100,
            'interior_materials': 100,
            'paint_corrosion': 100,
            'electrical_aging': 100,
            'cosmetic_aging': 100,
            'extra_dimension': 50,
            'another_extra': 0,
        }
        assert compute_build_aggregate(scores) == 100.0

    def test_empty_scores_returns_none(self):
        assert compute_build_aggregate({}) is None

    def test_all_none_returns_none(self):
        scores = {dim: None for dim in BUILD_DIMENSIONS}
        assert compute_build_aggregate(scores) is None


# --- get_build_score_dict ---

class TestGetBuildScoreDict:
    """Validate extraction from ORM-like object."""

    def _make_bq(self, **kwargs):
        defaults = {
            'score_body_construction': 85,
            'score_nvh_isolation': 80,
            'score_interior_materials': 90,
            'score_paint_corrosion': 75,
            'score_electrical_aging': 70,
            'score_cosmetic_aging': 65,
        }
        defaults.update(kwargs)
        return SimpleNamespace(**defaults)

    def test_extracts_all_six_dimensions(self):
        bq = self._make_bq()
        result = get_build_score_dict(bq)
        assert set(result.keys()) == set(BUILD_DIMENSIONS)
        assert result['body_construction'] == 85
        assert result['nvh_isolation'] == 80
        assert result['interior_materials'] == 90
        assert result['paint_corrosion'] == 75
        assert result['electrical_aging'] == 70
        assert result['cosmetic_aging'] == 65

    def test_preserves_none_values(self):
        bq = self._make_bq(
            score_nvh_isolation=None,
            score_electrical_aging=None,
        )
        result = get_build_score_dict(bq)
        assert result['nvh_isolation'] is None
        assert result['electrical_aging'] is None
        assert result['body_construction'] == 85


# --- recompute_build_aggregate ---

class TestRecomputeBuildAggregate:
    """Validate recomputation and ORM update."""

    def test_recomputes_and_sets_q_score(self):
        bq = SimpleNamespace(
            score_body_construction=90,
            score_nvh_isolation=85,
            score_interior_materials=88,
            score_paint_corrosion=82,
            score_electrical_aging=80,
            score_cosmetic_aging=78,
            q_score=None,
        )
        result = recompute_build_aggregate(bq)
        assert result == 84.6
        assert bq.q_score == 84.6

    def test_returns_none_when_insufficient(self):
        bq = SimpleNamespace(
            score_body_construction=90,
            score_nvh_isolation=85,
            score_interior_materials=None,
            score_paint_corrosion=None,
            score_electrical_aging=None,
            score_cosmetic_aging=None,
            q_score=None,
        )
        result = recompute_build_aggregate(bq)
        assert result is None

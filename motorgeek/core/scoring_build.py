"""Dimensional build quality scoring — aggregate computation."""

BUILD_DIMENSIONS = [
    'body_construction',
    'nvh_isolation',
    'interior_materials',
    'paint_corrosion',
    'electrical_aging',
    'cosmetic_aging',
]

BUILD_WEIGHTS = {
    'body_construction':  0.25,
    'nvh_isolation':      0.10,
    'interior_materials': 0.20,
    'paint_corrosion':    0.15,
    'electrical_aging':   0.15,
    'cosmetic_aging':     0.15,
}

MIN_DIMENSIONS_FOR_AGGREGATE = 3


def compute_build_aggregate(scores: dict[str, float | None]) -> float | None:
    """Compute weighted aggregate build quality score from dimensional subscores.

    Requires at least 3 of 6 dimensions to be non-NULL.
    Weights are redistributed proportionally for NULL dimensions.
    """
    present = {k: v for k, v in scores.items() if v is not None and k in BUILD_WEIGHTS}
    if len(present) < MIN_DIMENSIONS_FOR_AGGREGATE:
        return None

    weight_sum = sum(BUILD_WEIGHTS[k] for k in present)
    adjusted = {k: BUILD_WEIGHTS[k] / weight_sum for k in present}
    raw = sum(present[k] * adjusted[k] for k in present)
    return round(raw, 1)


def get_build_score_dict(bq) -> dict[str, float | None]:
    """Extract dimensional scores from a BuildQuality ORM-like object."""
    return {
        'body_construction': bq.score_body_construction,
        'nvh_isolation': bq.score_nvh_isolation,
        'interior_materials': bq.score_interior_materials,
        'paint_corrosion': bq.score_paint_corrosion,
        'electrical_aging': bq.score_electrical_aging,
        'cosmetic_aging': bq.score_cosmetic_aging,
    }


def recompute_build_aggregate(bq) -> float | None:
    """Recompute and update the q_score on a BuildQuality object."""
    scores = get_build_score_dict(bq)
    new_score = compute_build_aggregate(scores)
    if new_score is not None:
        bq.q_score = new_score
    return new_score

"""Dimensional reliability scoring — aggregate computation."""

DIMENSIONS = ['engine', 'transmission', 'chassis', 'electronics', 'ease_of_repair']

WEIGHTS = {
    'engine': 0.25,
    'transmission': 0.25,
    'chassis': 0.15,
    'electronics': 0.15,
    'ease_of_repair': 0.20,
}

MIN_DIMENSIONS_FOR_AGGREGATE = 3
CATASTROPHE_THRESHOLD = 50.0


def compute_reliability_aggregate(scores: dict[str, float | None]) -> float | None:
    """Compute weighted aggregate reliability score from dimensional subscores.

    Requires at least 3 of 5 dimensions to be non-NULL.
    Applies a catastrophe penalty if any dimension < 50.
    Weights are redistributed proportionally for NULL dimensions.
    """
    present = {k: v for k, v in scores.items() if v is not None and k in WEIGHTS}
    if len(present) < MIN_DIMENSIONS_FOR_AGGREGATE:
        return None

    weight_sum = sum(WEIGHTS[k] for k in present)
    adjusted = {k: WEIGHTS[k] / weight_sum for k in present}
    raw = sum(present[k] * adjusted[k] for k in present)

    min_score = min(present.values())
    if min_score < CATASTROPHE_THRESHOLD:
        penalty = 0.85 + (min_score / CATASTROPHE_THRESHOLD) * 0.15
        return round(raw * penalty, 1)
    return round(raw, 1)


def get_score_dict(rel) -> dict[str, float | None]:
    """Extract dimensional scores from a Reliability ORM object."""
    return {
        'engine': rel.score_engine,
        'transmission': rel.score_transmission,
        'chassis': rel.score_chassis,
        'electronics': rel.score_electronics,
        'ease_of_repair': rel.score_ease_of_repair,
    }


def recompute_aggregate(rel) -> float | None:
    """Recompute and update the reliability_score on a Reliability object."""
    scores = get_score_dict(rel)
    new_score = compute_reliability_aggregate(scores)
    if new_score is not None:
        rel.reliability_score = new_score
    return new_score

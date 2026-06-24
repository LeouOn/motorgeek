"""Production calculators package.

Modules:
    zeperfs -- ZePerfs Index (ZP) formula calculator (ICE v4 + EV v3).
    practicality -- Doug Score-calibrated practicality dimension (0-100).
    composite -- Weighted blend of Quality/Reliability/Practicality/Performance.
"""

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
    DEFAULT_CARGO_LITERS,
    LITERS_PER_CUBIC_FOOT,
    WAGON_BONUS_STYLES,
    cargo_cf_to_doug_tier,
    compute_practicality_for_car,
    compute_practicality_score,
)
from motorgeek.core.calculators.zeperfs import (
    EV_COEFFICIENTS,
    ICE_COEFFICIENTS,
    ZP_CLASSES,
    classify_zp,
    compute_ch_L,
    compute_ch_T,
    compute_tpu,
    compute_zp_ev,
    compute_zp_for_car,
    compute_zp_ice,
    is_ev_car,
)

__all__ = [
    # zeperfs
    "EV_COEFFICIENTS",
    "ICE_COEFFICIENTS",
    "ZP_CLASSES",
    "classify_zp",
    "compute_ch_L",
    "compute_ch_T",
    "compute_tpu",
    "compute_zp_ev",
    "compute_zp_for_car",
    "compute_zp_ice",
    "is_ev_car",
    # practicality
    "BODY_STYLE_CARGO_ESTIMATES",
    "DEFAULT_CARGO_LITERS",
    "LITERS_PER_CUBIC_FOOT",
    "WAGON_BONUS_STYLES",
    "cargo_cf_to_doug_tier",
    "compute_practicality_for_car",
    "compute_practicality_score",
    # composite
    "MIN_DIMENSIONS",
    "WEIGHTS",
    "ZP_SCALE",
    "compute_composite",
    "compute_composite_for_car",
    "normalize_zp",
]

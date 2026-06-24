"""ZePerfs Index (ZP) calculator -- production module.

Implements the ZP formula in two branches:

* ICE v4 (refit 2026-06-18 on 22 anchors, MAE 2.99):
    ZP_ice = 0.3924 * ch_T
           - 0.4383 * sqrt(ch_L)
           + 56.1399 * tpu
           - 10.4664 * (ch_T * tpu / 100)
           + 13.3050

* EV v3 (log(ch_T), fit 2026-06-18 on 11 anchors, MAE 4.56):
    ZP_ev = 55.48 * ln(ch_T) + 12.28 * tpu - 162.24

Variable definitions (per spec .omo/research/zeperfs-zp-formula.md,
section 0.A "ch_L correction"):

    ch_T = horsepower_bhp / (curb_weight_kg / 1000)   # power per tonne
    ch_L = horsepower_bhp / (displacement_cc / 1000)  # specific output (hp/L)
    tpu  = 10.0 / accel_0_100_seconds                 # s^-1; 0 when accel unknown

The accel monotonicity bug in the ICE branch is mild at v4 (threshold
ch_T > 536); only ~1 car in the DB is affected (McLaren 765LT). The EV
branch is monotonic everywhere (dZP/dtpu = 12.28 > 0).

Coefficients are FINAL -- do not refit without explicit approval.
See `.omo/research/zeperfs-zp-formula.md` for the full calibration history.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # avoid runtime import cycle; annotations are strings
    from motorgeek.core.models import Car, Performance, PowertrainICE


# --- Coefficients (FROZEN -- do not modify without re-fitting) -------------

ICE_COEFFICIENTS: dict[str, float] = {
    "ch_T": 0.3924,
    "sqrt_ch_L": -0.4383,
    "tpu": 56.1399,
    "ch_T_tpu_interaction": -10.4664,  # multiplies (ch_T * tpu / 100)
    "bias": 13.3050,
}

EV_COEFFICIENTS: dict[str, float] = {
    "log_ch_T": 55.48,
    "tpu": 12.28,
    "bias": -162.24,
}

# (upper_bound_exclusive, label). Evaluated in order; first match wins.
ZP_CLASSES: list[tuple[float, str]] = [
    (120.0, "<C"),
    (135.0, "C"),
    (150.0, "B"),
    (170.0, "A"),
    (200.0, "S1"),
    (230.0, "S2/R"),
    (float("inf"), "Track"),
]


# --- Primitive variables ----------------------------------------------------

def compute_ch_T(horsepower_bhp: float, curb_weight_kg: float) -> float:
    """Power per metric tonne (ch/T = chevaux par tonne)."""
    return horsepower_bhp / (curb_weight_kg / 1000.0)


def compute_ch_L(horsepower_bhp: float, displacement_cc: float | None) -> float | None:
    """Specific output in hp per litre (ch/L = chevaux par litre).

    Returns None when displacement is missing or zero (covers EVs, which
    have no displacement and must route through the EV branch).
    """
    if displacement_cc is None or displacement_cc == 0:
        return None
    return horsepower_bhp / (displacement_cc / 1000.0)


def compute_tpu(accel_0_100_s: float | None) -> float:
    """Inverse-acceleration metric in s^-1. Returns 0.0 when accel is unknown.

    The ICE branch tolerates unknown accel (car still gets ch_T + ch_L score).
    The EV branch refuses unknown accel at a higher layer (see compute_zp_ev).
    """
    if accel_0_100_s is None or accel_0_100_s <= 0:
        return 0.0
    return 10.0 / accel_0_100_s


# --- Branch formulas --------------------------------------------------------

def compute_zp_ice(
    horsepower_bhp: float | None,
    curb_weight_kg: float | None,
    displacement_cc: float | None,
    accel_0_100_s: float | None,
) -> float | None:
    """Apply the v4 ICE formula.

    Returns None when horsepower or weight is missing, or when displacement
    is missing/zero (the caller should route such cars through compute_zp_ev).
    Unknown accel is acceptable: tpu collapses to 0 and the car is scored on
    ch_T + ch_L alone.
    """
    if horsepower_bhp is None or curb_weight_kg is None or curb_weight_kg == 0:
        return None
    ch_L = compute_ch_L(horsepower_bhp, displacement_cc)
    if ch_L is None:
        return None  # displacement missing -> caller should use EV branch
    ch_T = compute_ch_T(horsepower_bhp, curb_weight_kg)
    tpu = compute_tpu(accel_0_100_s)
    zp = (
        ICE_COEFFICIENTS["ch_T"] * ch_T
        + ICE_COEFFICIENTS["sqrt_ch_L"] * math.sqrt(ch_L)
        + ICE_COEFFICIENTS["tpu"] * tpu
        + ICE_COEFFICIENTS["ch_T_tpu_interaction"] * (ch_T * tpu / 100.0)
        + ICE_COEFFICIENTS["bias"]
    )
    return round(zp, 1)


def compute_zp_ev(
    horsepower_bhp: float | None,
    curb_weight_kg: float | None,
    accel_0_100_s: float | None,
) -> float | None:
    """Apply the v3 EV formula using ln(ch_T).

    Returns None when horsepower or weight is missing, or when accel is
    missing (the EV branch has no ch_L fallback, so tpu is mandatory).
    """
    if horsepower_bhp is None or curb_weight_kg is None or curb_weight_kg == 0:
        return None
    if accel_0_100_s is None or accel_0_100_s <= 0:
        return None
    ch_T = compute_ch_T(horsepower_bhp, curb_weight_kg)
    tpu = compute_tpu(accel_0_100_s)
    zp = (
        EV_COEFFICIENTS["log_ch_T"] * math.log(ch_T)
        + EV_COEFFICIENTS["tpu"] * tpu
        + EV_COEFFICIENTS["bias"]
    )
    return round(zp, 1)


# --- Classification ---------------------------------------------------------

def classify_zp(zp: float) -> str:
    """Map a ZP value to its class label ('<C', 'C', 'B', 'A', 'S1', 'S2/R', 'Track')."""
    for upper, label in ZP_CLASSES:
        if zp < upper:
            return label
    return ZP_CLASSES[-1][1]


# --- High-level dispatcher --------------------------------------------------

def is_ev_car(car: Car) -> bool:
    """Heuristic: route to the EV branch when any of these hold.

    * ``car.character == 'ev'``
    * aspiration (via car.powertrain_ice) is 'electric'
    * displacement_cc is None or 0 (no ICE data -> likely EV)
    * car.powertrain_ice itself is None (no ICE row at all)
    """
    if car.character == "ev":
        return True
    pi = car.powertrain_ice
    if pi is None:
        return True
    if pi.aspiration and pi.aspiration.lower() == "electric":
        return True
    if not pi.displacement_cc:  # None or 0
        return True
    return False


def _resolve_accel_0_100(performance: Performance | None) -> float | None:
    """Pull 0-100 km/h accel, falling back to 0-60 mph when 0-100 is absent.

    0-60 mph ~= 0-96 km/h, so it is a slight optimism -- but it is the best
    available signal when the European figure is missing.
    """
    if performance is None:
        return None
    if performance.accel_0_100 is not None:
        return performance.accel_0_100
    return performance.accel_0_60


def compute_zp_for_car(
    car: Car,
    powertrain_ice: PowertrainICE | None,
    performance: Performance | None,
) -> tuple[float | None, str]:
    """End-to-end dispatcher for one car.

    Returns ``(zp_value, branch_used)`` where branch_used is one of:
    * ``'ICE'``                    -- v4 ICE formula applied
    * ``'EV'``                     -- v3 EV formula applied
    * ``'INSUFFICIENT_DATA'``      -- inputs missing or formula returned None
    """
    if powertrain_ice is None:
        return None, "INSUFFICIENT_DATA"

    horsepower_bhp = powertrain_ice.horsepower_bhp
    curb_weight_kg = powertrain_ice.curb_weight_kg
    displacement_cc = powertrain_ice.displacement_cc
    aspiration = powertrain_ice.aspiration

    if horsepower_bhp is None or curb_weight_kg is None:
        return None, "INSUFFICIENT_DATA"

    accel = _resolve_accel_0_100(performance)

    is_ev = (
        car.character == "ev"
        or (aspiration is not None and aspiration.lower() == "electric")
        or not displacement_cc  # None or 0
    )

    if is_ev:
        zp = compute_zp_ev(horsepower_bhp, curb_weight_kg, accel)
    else:
        zp = compute_zp_ice(horsepower_bhp, curb_weight_kg, displacement_cc, accel)

    if zp is None:
        return None, "INSUFFICIENT_DATA"
    return zp, "EV" if is_ev else "ICE"

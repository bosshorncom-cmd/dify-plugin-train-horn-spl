"""Free-field train-horn sound pressure level estimate.

The calculation uses spherical inverse-square spreading,

    L2 = L1 - 20 * log10(r2 / r1) - alpha * (r2 - r1) / 1000

with distances in metres and alpha in dB/km. The result is a free-field
estimate only. ISO 9613-1 and ISO 9613-2 are background references for
outdoor sound propagation; this module does not implement those
standards and does not supply their tabulated absorption coefficients.
"""

from __future__ import annotations

import math
from typing import Any, Mapping


class SplCalculationError(ValueError):
    """Raised when an input cannot be used in the free-field estimate."""


def _as_finite_float(name: str, value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise SplCalculationError(f"{name} must be a finite number.") from exc
    if not math.isfinite(number):
        raise SplCalculationError(f"{name} must be a finite number.")
    return number


def predict_spl(
    reference_spl_db: Any,
    reference_distance_m: Any,
    target_distance_m: Any,
    attenuation_db_per_km: Any = 0.0,
) -> dict[str, Any]:
    """Return a free-field SPL prediction and its component terms.

    Parameters
    ----------
    reference_spl_db:
        Sound pressure level L1, in decibels, at the reference distance.
    reference_distance_m:
        Reference distance r1 from the source, in metres. Must be > 0.
    target_distance_m:
        Target distance r2 from the source, in metres. Must be > 0.
    attenuation_db_per_km:
        Optional user-supplied linear atmospheric or ground attenuation
        coefficient alpha, in dB/km. Defaults to 0 (spreading only).
    """
    level_ref = _as_finite_float("reference_spl_db", reference_spl_db)
    distance_ref = _as_finite_float("reference_distance_m", reference_distance_m)
    distance_target = _as_finite_float("target_distance_m", target_distance_m)
    alpha = _as_finite_float("attenuation_db_per_km", attenuation_db_per_km)

    if distance_ref <= 0 or distance_target <= 0:
        raise SplCalculationError("Distances must be greater than zero metres.")

    geometric_spreading_db = 20.0 * math.log10(distance_target / distance_ref)
    atmospheric_absorption_db = alpha * (distance_target - distance_ref) / 1000.0
    predicted_spl_db = level_ref - geometric_spreading_db - atmospheric_absorption_db

    return {
        "predicted_spl_db": predicted_spl_db,
        "geometric_spreading_db": geometric_spreading_db,
        "atmospheric_absorption_db": atmospheric_absorption_db,
        "reference_spl_db": level_ref,
        "reference_distance_m": distance_ref,
        "target_distance_m": distance_target,
        "attenuation_db_per_km": alpha,
        "model": (
            "free-field estimate: "
            "L2 = L1 - 20*log10(r2/r1) - alpha*(r2-r1)/1000"
        ),
        "note": (
            "Free-field estimate only. It does not include ground "
            "reflections, barriers, source directivity, or meteorology "
            "beyond the optional linear absorption term. ISO 9613-1 and "
            "ISO 9613-2 are cited as background for outdoor sound "
            "propagation; this tool does not implement those standards "
            "or their tabulated coefficients."
        ),
    }


def format_prediction(result: Mapping[str, Any]) -> str:
    """Render a short human-readable summary of a successful prediction."""
    return (
        "Free-field train horn SPL estimate: "
        f"{result['predicted_spl_db']:.2f} dB at {result['target_distance_m']:g} m "
        f"(reference {result['reference_spl_db']:.2f} dB at "
        f"{result['reference_distance_m']:g} m; geometric spreading "
        f"{result['geometric_spreading_db']:.2f} dB; linear absorption "
        f"{result['atmospheric_absorption_db']:.2f} dB). {result['note']}"
    )

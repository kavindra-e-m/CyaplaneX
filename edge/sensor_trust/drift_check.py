"""Sensor drift detection module.

Identifies potential calibration drift or baseline shift across a rolling window of values.
"""
from collections.abc import Sequence


def drift_suspected(values: Sequence[float], threshold: float) -> bool:
    """Return whether values exhibit drift exceeding the threshold.

    Calculates the difference between the recent window mean and earlier window mean,
    or peak-to-peak variation exceeding baseline tolerance.
    """
    if not values or len(values) < 2 or threshold <= 0:
        return False

    n = len(values)
    if n >= 6:
        half = n // 2
        early_mean = sum(values[:half]) / half
        late_mean = sum(values[half:]) / (n - half)
        return abs(late_mean - early_mean) > threshold

    return (max(values) - min(values)) > threshold

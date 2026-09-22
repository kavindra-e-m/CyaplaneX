"""Sensor drift detection placeholder."""

def drift_suspected(values: list[float], threshold: float) -> bool:
    """Return a placeholder result until a calibrated drift method is selected."""
    # TODO: Define a statistically justified drift detector.
    return bool(values) and max(values) - min(values) > threshold

"""Range validation for sensor readings."""


def is_in_range(value: float, minimum: float, maximum: float) -> bool:
    """Return whether a reading is within inclusive engineering limits."""
    return minimum <= value <= maximum


def validate_range(value: float, limits: tuple[float, float]) -> bool:
    """Validate a value against a ``(minimum, maximum)`` tuple."""
    return is_in_range(value, *limits)

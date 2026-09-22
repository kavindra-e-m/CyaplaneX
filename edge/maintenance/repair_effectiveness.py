"""Repair-effectiveness calculation boundary."""


def improvement(pre_health_score: float, post_health_score: float) -> float:
    """Return normalized score improvement, clamped to the contract range."""
    if not 0 <= pre_health_score <= 100 or not 0 <= post_health_score <= 100:
        raise ValueError("health scores must be between 0 and 100")
    return max(0.0, min(1.0, (post_health_score - pre_health_score) / 100))

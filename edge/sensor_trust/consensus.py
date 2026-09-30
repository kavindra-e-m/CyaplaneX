"""Cross-sensor consensus and consistency checking."""
from collections.abc import Sequence


def consensus_score(values: Sequence[float], max_allowed_spread: float = 1.0) -> float:
    """Return a normalized consensus score between 0.0 and 1.0.

    Higher scores indicate strong agreement between redundant sensor readings.
    A score of 1.0 represents perfect agreement, while high divergence drops towards 0.0.
    """
    if not values:
        return 0.0
    if len(values) == 1:
        return 1.0

    spread = max(values) - min(values)
    if max_allowed_spread <= 0:
        return 1.0 if spread == 0 else 0.0

    # Linear penalty scaled to allowed spread, clamped [0.0, 1.0]
    score = 1.0 - (spread / max_allowed_spread)
    return round(max(0.0, min(1.0, score)), 4)

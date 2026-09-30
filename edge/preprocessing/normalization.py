"""Signal normalization utilities for edge preprocessing."""
from collections.abc import Sequence


def normalize_samples(
    samples: Sequence[float],
    min_val: float | None = None,
    max_val: float | None = None,
) -> list[float]:
    """Normalize samples to [0.0, 1.0] range using min-max scaling.

    If min_val and max_val are None, samples are scaled relative to local bounds.
    If samples are constant or empty, returns original or zero-centered list.
    """
    if not samples:
        return []
    low = min_val if min_val is not None else min(samples)
    high = max_val if max_val is not None else max(samples)

    if high <= low:
        return [0.5] * len(samples)

    spread = high - low
    return [round(max(0.0, min(1.0, (x - low) / spread)), 5) for x in samples]

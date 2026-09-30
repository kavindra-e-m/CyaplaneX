"""Signal filtering utilities for edge preprocessing."""
from collections.abc import Sequence


def filter_samples(samples: Sequence[float], window_size: int = 1) -> list[float]:
    """Filter raw signal samples using a simple moving-average finite impulse response (FIR).

    When window_size == 1, returns the samples unchanged.
    """
    if not samples:
        return []
    if window_size <= 1:
        return list(samples)

    result: list[float] = []
    for i in range(len(samples)):
        start = max(0, i - window_size + 1)
        sub = samples[start:i + 1]
        result.append(round(sum(sub) / len(sub), 5))
    return result

"""Signal windowing placeholder."""

def make_windows(samples: list[float], size: int) -> list[list[float]]:
    """Split samples into complete windows."""
    if size <= 0:
        raise ValueError("size must be positive")
    return [samples[index:index + size] for index in range(0, len(samples) - size + 1, size)]

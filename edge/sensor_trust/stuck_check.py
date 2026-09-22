"""Detection of unchanged sensor values."""
from collections.abc import Sequence


def is_stuck(values: Sequence[float], minimum_repeated: int = 3) -> bool:
    """Return true when the latest values repeat at least the threshold."""
    if minimum_repeated <= 1:
        raise ValueError("minimum_repeated must be greater than one")
    return len(values) >= minimum_repeated and len(set(values[-minimum_repeated:])) == 1

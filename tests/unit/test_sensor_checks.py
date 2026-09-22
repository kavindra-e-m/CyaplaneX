"""Unit tests for sensor trust primitives."""
from edge.sensor_trust.range_check import is_in_range
from edge.sensor_trust.stuck_check import is_stuck


def test_range_check_accepts_boundaries_and_rejects_outliers() -> None:
    assert is_in_range(10, 10, 20)
    assert not is_in_range(21, 10, 20)


def test_stuck_check_detects_repeated_tail() -> None:
    assert is_stuck([1.0, 2.0, 2.0, 2.0])
    assert not is_stuck([1.0, 2.0, 2.1, 2.0])

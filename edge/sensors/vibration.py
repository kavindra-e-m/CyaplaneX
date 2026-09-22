"""Vibration acquisition interface placeholder."""
from typing import Protocol


class VibrationSensor(Protocol):
    """Interface for a vibration sensor adapter."""
    def read(self) -> float: ...

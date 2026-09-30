"""Vibration acquisition interface and adapters."""
import math
from collections.abc import Sequence
from typing import Protocol


class VibrationSensor(Protocol):
    """Interface for a vibration sensor adapter."""
    def read(self) -> float: ...


class SimulatedVibrationSensor:
    """Configurable simulated vibration sensor producing acceleration in g."""

    def __init__(self, baseline: float = 0.35, noise: float = 0.05) -> None:
        self.baseline = baseline
        self.noise = noise
        self._step = 0

    def read(self) -> float:
        self._step += 1
        return round(self.baseline + self.noise * math.sin(self._step * 0.5), 4)


class ReplayVibrationSensor:
    """Replays pre-recorded vibration readings."""

    def __init__(self, sequence: Sequence[float], loop: bool = True) -> None:
        if not sequence:
            raise ValueError("sequence cannot be empty")
        self._sequence = list(sequence)
        self._index = 0
        self._loop = loop

    def read(self) -> float:
        if self._index >= len(self._sequence):
            if self._loop:
                self._index = 0
            else:
                return self._sequence[-1]
        val = self._sequence[self._index]
        self._index += 1
        return val

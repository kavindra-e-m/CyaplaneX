"""Temperature acquisition interface and adapters."""
import math
from collections.abc import Sequence
from typing import Protocol


class TemperatureSensor(Protocol):
    """Interface for a temperature sensor adapter."""
    def read(self) -> float: ...


class SimulatedTemperatureSensor:
    """Configurable simulated temperature sensor producing °C readings."""

    def __init__(self, baseline: float = 52.0, drift_rate: float = 0.0) -> None:
        self.baseline = baseline
        self.drift_rate = drift_rate
        self._step = 0

    def read(self) -> float:
        self._step += 1
        return round(self.baseline + (self._step * self.drift_rate) + 0.2 * math.cos(self._step * 0.3), 2)


class ReplayTemperatureSensor:
    """Replays pre-recorded temperature readings."""

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

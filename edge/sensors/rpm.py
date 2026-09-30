"""RPM acquisition interface and adapters."""
from collections.abc import Sequence
from typing import Protocol


class RpmSensor(Protocol):
    """Interface for an RPM sensor adapter."""
    def read(self) -> float: ...


class SimulatedRpmSensor:
    """Configurable simulated RPM sensor producing shaft rotations per minute."""

    def __init__(self, target_rpm: float = 3600.0, variance: float = 15.0) -> None:
        self.target_rpm = target_rpm
        self.variance = variance
        self._step = 0

    def read(self) -> float:
        import math
        self._step += 1
        return round(self.target_rpm + self.variance * math.sin(self._step * 0.2), 1)


class ReplayRpmSensor:
    """Replays pre-recorded RPM readings."""

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

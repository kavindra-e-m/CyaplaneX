"""Temperature acquisition interface placeholder."""
from typing import Protocol


class TemperatureSensor(Protocol):
    """Interface for a temperature sensor adapter."""
    def read(self) -> float: ...

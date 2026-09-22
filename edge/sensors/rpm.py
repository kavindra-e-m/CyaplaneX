"""RPM acquisition interface placeholder."""
from typing import Protocol


class RpmSensor(Protocol):
    """Interface for an RPM sensor adapter."""
    def read(self) -> float: ...

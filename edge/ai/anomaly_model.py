"""Anomaly model adapter placeholder."""
from typing import Protocol


class AnomalyModel(Protocol):
    """Interface implemented by an exported edge model."""
    def score(self, features: list[float]) -> float: ...

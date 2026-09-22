"""Typed health-result value object and conservative scaffold logic."""
from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class HealthResult:
    """Model output contract; model inference is intentionally out of scope."""

    condition: str
    anomaly_score: float
    health_score: float
    confidence: float
    severity: str
    model_id: str
    model_version: str
    model_hash: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize the result for APIs and provenance manifests."""
        return asdict(self)

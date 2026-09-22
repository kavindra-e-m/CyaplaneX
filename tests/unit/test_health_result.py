"""Health contract serialization tests."""
from edge.ai.health_engine import HealthResult


def test_health_result_serializes_expected_fields() -> None:
    result = HealthResult("healthy", 0.02, 98.0, 0.9, "HEALTHY", "demo", "0.1", "hash")
    assert result.to_dict()["health_score"] == 98.0
    assert set(result.to_dict()) == {"condition", "anomaly_score", "health_score", "confidence", "severity", "model_id", "model_version", "model_hash"}

"""Unit tests for preprocessing feature pipeline and Edge ML adapter."""
from datetime import UTC, datetime

from edge.ai.adapter import EdgeMLAdapter
from edge.preprocessing.pipeline import FeaturePipeline
from shared.contracts import HealthSeverity, SchemaName, validate_contract


def make_window_samples(vib: float, temp: float, rpm: float) -> list[dict]:
    ts = datetime.now(UTC).isoformat()
    return [
        {"device_id": "d1", "sensor_id": "v1", "sensor_type": "vibration", "value": vib, "sequence": 0, "timestamp": ts, "unit": "g", "calibration_version": "v1"},
        {"device_id": "d1", "sensor_id": "v1", "sensor_type": "vibration", "value": vib * 1.1, "sequence": 1, "timestamp": ts, "unit": "g", "calibration_version": "v1"},
        {"device_id": "d1", "sensor_id": "t1", "sensor_type": "temperature", "value": temp, "sequence": 2, "timestamp": ts, "unit": "degC", "calibration_version": "v1"},
        {"device_id": "d1", "sensor_id": "r1", "sensor_type": "rpm", "value": rpm, "sequence": 3, "timestamp": ts, "unit": "rpm", "calibration_version": "v1"},
    ]


def test_feature_pipeline_extracts_features_and_hash() -> None:
    pipeline = FeaturePipeline()
    samples = make_window_samples(vib=0.35, temp=50.0, rpm=3000.0)

    window = pipeline.process_window(samples)

    assert len(window.features) == 6
    assert window.feature_names == pipeline.FEATURE_NAMES
    assert len(window.sensor_window_hash) == 64
    assert window.sample_count == 4


def test_edge_ml_adapter_evaluates_healthy_condition() -> None:
    adapter = EdgeMLAdapter()
    # Features: [vib_rms, vib_p2p, temp_mean, temp_max, rpm_mean, rpm_std]
    healthy_features = [0.35, 0.1, 50.0, 52.0, 3000.0, 10.0]

    result = adapter.infer(healthy_features)

    assert result.condition == "HEALTHY"
    assert result.severity == HealthSeverity.HEALTHY.value
    assert result.health_score >= 80.0
    assert result.anomaly_score < 0.2

    valid, err = validate_contract(result.to_dict(), SchemaName.HEALTH_RESULT)
    assert valid, err


def test_edge_ml_adapter_evaluates_vibration_anomaly() -> None:
    adapter = EdgeMLAdapter()
    # High vibration features
    fault_features = [1.85, 0.9, 52.0, 54.0, 3000.0, 15.0]

    result = adapter.infer(fault_features)

    assert result.condition == "HIGH_VIBRATION"
    assert result.severity in (HealthSeverity.WARNING.value, HealthSeverity.CRITICAL.value)
    assert result.health_score < 50.0

    valid, err = validate_contract(result.to_dict(), SchemaName.HEALTH_RESULT)
    assert valid, err


def test_edge_ml_adapter_evaluates_overheating() -> None:
    adapter = EdgeMLAdapter()
    # Overheating features
    overheat_features = [0.4, 0.1, 88.0, 95.0, 3000.0, 10.0]

    result = adapter.infer(overheat_features)

    assert result.condition == "OVERHEATING"
    assert result.severity == HealthSeverity.CRITICAL.value

    valid, err = validate_contract(result.to_dict(), SchemaName.HEALTH_RESULT)
    assert valid, err

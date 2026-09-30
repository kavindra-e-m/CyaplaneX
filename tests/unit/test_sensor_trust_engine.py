"""Unit tests for sensor trust engine and aggregation."""
from datetime import UTC, datetime, timedelta

import pytest

from edge.sensor_trust.engine import SensorTrustEngine
from shared.contracts import SchemaName, TrustStatus, validate_contract


@pytest.fixture
def trust_engine() -> SensorTrustEngine:
    return SensorTrustEngine()


def make_sample(value: float, sensor_id: str = "vib-01", sensor_type: str = "vibration", age_seconds: float = 0.0) -> dict:
    ts = (datetime.now(UTC) - timedelta(seconds=age_seconds)).isoformat()
    return {
        "device_id": "test-device",
        "sensor_id": sensor_id,
        "timestamp": ts,
        "sequence": 1,
        "sensor_type": sensor_type,
        "value": value,
        "unit": "g",
        "calibration_version": "v1.0",
    }


def test_healthy_sample_is_trusted(trust_engine: SensorTrustEngine) -> None:
    sample = make_sample(0.35)
    result = trust_engine.evaluate_sample(sample)

    assert result["trust_status"] == TrustStatus.TRUSTED.value
    assert result["range_valid"] is True
    assert result["fresh"] is True
    assert result["stuck"] is False
    assert result["drift_suspected"] is False
    assert result["consensus_score"] >= 0.5

    valid, err = validate_contract(result, SchemaName.SENSOR_TRUST)
    assert valid, err


def test_out_of_range_fails_trust(trust_engine: SensorTrustEngine) -> None:
    # Limit for vibration is [-5.0, 5.0]
    sample = make_sample(12.5)
    result = trust_engine.evaluate_sample(sample)

    assert result["trust_status"] == TrustStatus.FAILED.value
    assert result["range_valid"] is False


def test_stale_sample_fails_trust(trust_engine: SensorTrustEngine) -> None:
    # Max age is 10.0 seconds
    sample = make_sample(0.35, age_seconds=30.0)
    result = trust_engine.evaluate_sample(sample)

    assert result["trust_status"] == TrustStatus.FAILED.value
    assert result["fresh"] is False


def test_stuck_sensor_degrades_trust(trust_engine: SensorTrustEngine) -> None:
    # Stuck threshold is 4 identical values
    for _ in range(4):
        res = trust_engine.evaluate_sample(make_sample(0.35, sensor_id="stuck-vib"))

    assert res["stuck"] is True
    assert res["trust_status"] == TrustStatus.DEGRADED.value


def test_divergent_consensus_degrades_trust(trust_engine: SensorTrustEngine) -> None:
    sample = make_sample(0.35, sensor_id="vib-01")
    # Redundant sensor reads 2.0g while primary reads 0.35g (spread 1.65 > 0.5)
    res = trust_engine.evaluate_sample(sample, redundant_values=[0.35, 2.0])

    assert res["consensus_score"] < 0.5
    assert res["trust_status"] == TrustStatus.DEGRADED.value


def test_aggregate_trust_logic(trust_engine: SensorTrustEngine) -> None:
    r1 = trust_engine.evaluate_sample(make_sample(0.35, sensor_id="s1"))
    r2 = trust_engine.evaluate_sample(make_sample(0.40, sensor_id="s2"))
    comp = trust_engine.aggregate_trust([r1, r2])
    assert comp["trust_status"] == TrustStatus.TRUSTED.value

    # Adding a degraded sensor makes composite DEGRADED
    r_deg = trust_engine.evaluate_sample(make_sample(0.35, sensor_id="s3"), redundant_values=[0.35, 2.0])
    comp_deg = trust_engine.aggregate_trust([r1, r2, r_deg])
    assert comp_deg["trust_status"] == TrustStatus.DEGRADED.value

    # Adding a failed sensor makes composite FAILED
    r_fail = trust_engine.evaluate_sample(make_sample(99.0, sensor_id="s4"))
    comp_fail = trust_engine.aggregate_trust([r1, r2, r_deg, r_fail])
    assert comp_fail["trust_status"] == TrustStatus.FAILED.value

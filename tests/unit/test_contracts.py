"""Unit tests for shared JSON schema contracts and validator."""
from datetime import UTC, datetime

from shared.contracts import (
    SchemaName,
    load_schema,
    validate_contract,
)


def sample_sensor_payload() -> dict:
    return {
        "device_id": "rpi5-edge-01",
        "sensor_id": "vib-accel-01",
        "timestamp": datetime.now(UTC).isoformat(),
        "sequence": 101,
        "sensor_type": "vibration",
        "value": 0.42,
        "unit": "g",
        "calibration_version": "cal-2026.1",
    }


def sample_trust_payload() -> dict:
    return {
        "sensor_id": "vib-accel-01",
        "trust_status": "TRUSTED",
        "range_valid": True,
        "fresh": True,
        "stuck": False,
        "drift_suspected": False,
        "consensus_score": 0.98,
    }


def sample_health_payload() -> dict:
    return {
        "condition": "HEALTHY",
        "anomaly_score": 0.05,
        "health_score": 95.0,
        "confidence": 0.92,
        "severity": "HEALTHY",
        "model_id": "cyaplanex-anomaly-v1",
        "model_version": "1.0.0",
        "model_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    }


def sample_maintenance_event_payload() -> dict:
    return {
        "report_id": "rep-2026-001",
        "asset_id": "aircraft-wing-lh",
        "component_id": "bearing-thrust-01",
        "sensor_window_hash": "9f83c60517b4a02aca02648667232e7568b5e618e6d5da50e02fb8f54279ac4f",
        "sensor_trust": sample_trust_payload(),
        "health_result": sample_health_payload(),
        "maintenance_reason": "Baseline operational check",
        "recommended_action": "Standard periodic visual check",
        "priority": "P3",
        "device_id": "rpi5-edge-01",
        "sequence_no": 1,
        "nonce": "n-550e8400-e29b-41d4-a716-446655440000",
        "timestamp": datetime.now(UTC).isoformat(),
        "previous_record_hash": "0000000000000000000000000000000000000000000000000000000000000000",
        "manifest_hash": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
        "digital_signature": "mock-signature-evidence",
    }


def sample_closure_payload() -> dict:
    return {
        "closure_id": "clo-2026-001",
        "report_id": "rep-2026-001",
        "maintenance_action": "Replaced thrust bearing assembly",
        "pre_health_score": 45.0,
        "post_health_score": 92.0,
        "repair_effectiveness": 0.47,
        "closure_status": "REPAIR_VERIFIED",
        "timestamp": datetime.now(UTC).isoformat(),
        "digital_signature": "mock-closure-signature",
    }


def test_all_schemas_load() -> None:
    for name in SchemaName:
        schema = load_schema(name)
        assert isinstance(schema, dict)
        assert "title" in schema


def test_sensor_sample_valid() -> None:
    valid, err = validate_contract(sample_sensor_payload(), SchemaName.SENSOR_SAMPLE)
    assert valid, err


def test_sensor_sample_rejects_missing_field() -> None:
    payload = sample_sensor_payload()
    del payload["value"]
    valid, err = validate_contract(payload, SchemaName.SENSOR_SAMPLE)
    assert not valid
    assert "value" in (err or "")


def test_sensor_sample_rejects_negative_sequence() -> None:
    payload = sample_sensor_payload()
    payload["sequence"] = -1
    valid, _err = validate_contract(payload, SchemaName.SENSOR_SAMPLE)
    assert not valid


def test_sensor_sample_rejects_additional_properties() -> None:
    payload = sample_sensor_payload()
    payload["unexpected_extra"] = 123
    valid, _err = validate_contract(payload, SchemaName.SENSOR_SAMPLE)
    assert not valid


def test_sensor_trust_valid() -> None:
    valid, err = validate_contract(sample_trust_payload(), SchemaName.SENSOR_TRUST)
    assert valid, err


def test_sensor_trust_rejects_invalid_enum() -> None:
    payload = sample_trust_payload()
    payload["trust_status"] = "INVALID_STATUS"
    valid, _err = validate_contract(payload, SchemaName.SENSOR_TRUST)
    assert not valid


def test_health_result_valid() -> None:
    valid, err = validate_contract(sample_health_payload(), SchemaName.HEALTH_RESULT)
    assert valid, err


def test_health_result_rejects_out_of_range_score() -> None:
    payload = sample_health_payload()
    payload["health_score"] = 150.0  # Max is 100
    valid, _err = validate_contract(payload, SchemaName.HEALTH_RESULT)
    assert not valid


def test_maintenance_event_valid() -> None:
    valid, err = validate_contract(sample_maintenance_event_payload(), SchemaName.MAINTENANCE_EVENT)
    assert valid, err


def test_maintenance_event_rejects_missing_signature() -> None:
    payload = sample_maintenance_event_payload()
    del payload["digital_signature"]
    valid, _err = validate_contract(payload, SchemaName.MAINTENANCE_EVENT)
    assert not valid


def test_closure_record_valid() -> None:
    valid, err = validate_contract(sample_closure_payload(), SchemaName.CLOSURE_RECORD)
    assert valid, err


def test_closure_record_rejects_out_of_range_repair_effectiveness() -> None:
    payload = sample_closure_payload()
    payload["repair_effectiveness"] = 1.5  # Max is 1.0
    valid, _err = validate_contract(payload, SchemaName.CLOSURE_RECORD)
    assert not valid


def test_lifecycle_field_linkage() -> None:
    event = sample_maintenance_event_payload()
    closure = sample_closure_payload()

    # Linkage: closure report_id references maintenance event report_id
    assert event["report_id"] == closure["report_id"]

    # Embedded sub-schemas validate against individual schemas
    assert validate_contract(event["health_result"], SchemaName.HEALTH_RESULT)[0]
    assert validate_contract(event["sensor_trust"], SchemaName.SENSOR_TRUST)[0]

    # Pre-health score in closure corresponds to pre-maintenance health score
    assert isinstance(closure["pre_health_score"], (int, float))
    assert isinstance(closure["post_health_score"], (int, float))
    assert closure["post_health_score"] > closure["pre_health_score"]

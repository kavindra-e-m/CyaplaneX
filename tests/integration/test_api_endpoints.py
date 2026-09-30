"""Integration tests for verification and maintenance API endpoints."""
import json

import pytest

from cloud.api.app import wsgi_app
from edge.provenance.manifest import assemble_maintenance_event, build_manifest
from edge.provenance.signer import DeviceLocalSigner


def call_api(path: str, method: str = "GET", body: dict | None = None) -> tuple[str, dict]:
    environ = {
        "PATH_INFO": path,
        "REQUEST_METHOD": method,
    }
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        environ["wsgi.input"] = pytest.importorskip("io").BytesIO(data)
        environ["CONTENT_LENGTH"] = str(len(data))

    response_status = ""
    response_headers = []

    def start_response(status, headers):
        nonlocal response_status, response_headers
        response_status = status
        response_headers = headers

    chunks = wsgi_app(environ, start_response)
    raw_output = b"".join(chunks).decode("utf-8")
    return response_status, json.loads(raw_output)


def make_valid_event(seq: int = 1, score: float = 35.0, cond: str = "HIGH_VIBRATION") -> dict:
    manifest = build_manifest(
        report_id=f"rep-api-{seq}",
        asset_id="asset-wing-lh",
        component_id="bearing-01",
        sensor_window_hash="c" * 64,
        sensor_trust={
            "sensor_id": "v1",
            "trust_status": "TRUSTED",
            "range_valid": True,
            "fresh": True,
            "stuck": False,
            "drift_suspected": False,
            "consensus_score": 1.0,
        },
        health_result={
            "condition": cond,
            "anomaly_score": 0.65,
            "health_score": score,
            "confidence": 0.92,
            "severity": "CRITICAL" if score < 40 else "WARNING",
            "model_id": "m1",
            "model_version": "1.0",
            "model_hash": "d" * 64,
        },
        maintenance_reason="High vibration detected",
        recommended_action="Inspect thrust bearing",
        priority="P1",
        device_id="dev-api-test",
        sequence_no=seq,
        previous_record_hash="0" * 64,
        timestamp="2026-09-30T10:00:00Z",
        nonce=f"nonce-api-{seq}",
    )
    sig = DeviceLocalSigner().sign_manifest(manifest)
    return assemble_maintenance_event(manifest, sig)


def test_api_health_endpoint() -> None:
    status, body = call_api("/health")
    assert status == "200 OK"
    assert body["status"] == "ok"


def test_api_end_to_end_maintenance_workflow() -> None:
    # 1. Ingest event
    event = make_valid_event(seq=1, score=35.0)
    status, body = call_api("/verification/events", method="POST", body=event)
    assert status == "200 OK"
    assert body["verified"] is True
    assert body["report_id"] == "rep-api-1"

    # 2. Check report verification status
    status, body = call_api("/verification/rep-api-1")
    assert status == "200 OK"
    assert body["status"] == "PROVENANCE_VERIFIED"
    assert body["verified"] is True

    # 3. Check asset maintenance state
    status, body = call_api("/maintenance/asset-wing-lh")
    assert status == "200 OK"
    assert body["state"] == "MAINTENANCE_REQUIRED"
    assert body["active_report_id"] == "rep-api-1"

    # 4. Start maintenance
    status, body = call_api("/maintenance/rep-api-1/start", method="POST")
    assert status == "200 OK"
    assert body["status"] == "MAINTENANCE_STARTED"

    # 5. Perform fresh re-test (with healthy post-maintenance features)
    healthy_features = [0.35, 0.1, 48.0, 50.0, 3000.0, 10.0]
    status, body = call_api("/maintenance/retest", method="POST", body={
        "report_id": "rep-api-1",
        "fresh_features": healthy_features,
    })
    assert status == "200 OK"
    assert body["outcome"] == "REPAIR_VERIFIED"
    assert body["repair_effectiveness"] > 0.4
    assert body["post_health_score"] >= 80.0

    # 6. Close maintenance
    status, body = call_api("/maintenance/closure", method="POST", body={
        "report_id": "rep-api-1",
        "maintenance_action": "Replaced thrust bearing and re-torqued shaft",
        "post_health_score": body["post_health_score"],
    })
    assert status == "200 OK"
    assert body["closure_status"] == "REPAIR_VERIFIED"
    assert "digital_signature" in body

    # 7. Check component passport history
    status, body = call_api("/passport/bearing-01")
    assert status == "200 OK"
    assert body["total_records"] >= 2
    types = [r["record_type"] for r in body["records"]]
    assert "DIAGNOSTIC_EVENT" in types
    assert "MAINTENANCE_CLOSURE" in types


def test_api_rejects_replay_sequence() -> None:
    event = make_valid_event(seq=5)
    call_api("/verification/events", method="POST", body=event)

    # Submitting same or lower sequence must fail with 400
    duplicate_event = make_valid_event(seq=5)
    status, body = call_api("/verification/events", method="POST", body=duplicate_event)
    assert status == "400 Bad Request"
    assert body["status"] == "REPLAY_REJECTED"


def test_api_rejects_tampered_signature() -> None:
    event = make_valid_event(seq=10)
    event["health_result"]["health_score"] = 99.0  # Tampering with protected field
    status, body = call_api("/verification/events", method="POST", body=event)
    assert status == "400 Bad Request"
    assert body["status"] == "PROVENANCE_VIOLATION"

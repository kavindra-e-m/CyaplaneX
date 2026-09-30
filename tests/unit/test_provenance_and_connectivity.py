"""Unit tests for provenance manifest, local signing, offline queue, and sync."""
import pytest

from cloud.verification.signature_verifier import verify_event
from edge.connectivity.mqtt_client import MockCloudTransport
from edge.connectivity.queue import OfflineQueue, QueueCapacityExceededError
from edge.connectivity.sync import SyncCoordinator
from edge.provenance.manifest import assemble_maintenance_event, build_manifest
from edge.provenance.signer import DeviceLocalSigner
from shared.contracts import SchemaName, validate_contract


def sample_manifest() -> dict:
    return build_manifest(
        report_id="rep-101",
        asset_id="asset-wing",
        component_id="bearing-01",
        sensor_window_hash="a" * 64,
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
            "condition": "HEALTHY",
            "anomaly_score": 0.05,
            "health_score": 95.0,
            "confidence": 0.95,
            "severity": "HEALTHY",
            "model_id": "m1",
            "model_version": "1.0",
            "model_hash": "b" * 64,
        },
        maintenance_reason="Routine observation",
        recommended_action="Continue monitoring",
        priority="P3",
        device_id="dev-01",
        sequence_no=1,
        previous_record_hash="0" * 64,
        timestamp="2026-09-30T00:00:00Z",
        nonce="nonce-001",
    )


def test_manifest_building_is_deterministic() -> None:
    m1 = sample_manifest()
    m2 = sample_manifest()
    assert m1["manifest_hash"] == m2["manifest_hash"]
    assert len(m1["manifest_hash"]) == 64


def test_local_signing_and_verification() -> None:
    manifest = sample_manifest()
    signer = DeviceLocalSigner()

    signature = signer.sign_manifest(manifest)
    assert signature.startswith("hmac-sha256:")

    event = assemble_maintenance_event(manifest, signature)
    valid, err = validate_contract(event, SchemaName.MAINTENANCE_EVENT)
    assert valid, err

    # Cryptographic verification succeeds
    assert verify_event(event)

    # Tampering test: modify one protected field
    tampered_event = dict(event)
    tampered_event["health_result"] = dict(tampered_event["health_result"])
    tampered_event["health_result"]["health_score"] = 20.0

    assert not verify_event(tampered_event)


def test_offline_queue_fifo_and_capacity() -> None:
    queue = OfflineQueue(max_capacity=3)
    assert queue.is_empty

    queue.put({"id": 1})
    queue.put({"id": 2})
    queue.put({"id": 3})

    assert len(queue) == 3
    assert queue.peek() == {"id": 1}

    # Overflow raises
    with pytest.raises(QueueCapacityExceededError):
        queue.put({"id": 4})

    drained = queue.drain(max_batch_size=2)
    assert drained == [{"id": 1}, {"id": 2}]
    assert len(queue) == 1

    remaining = queue.drain()
    assert remaining == [{"id": 3}]
    assert queue.is_empty


def test_sync_coordinator_online_and_offline_flow() -> None:
    queue = OfflineQueue()
    transport = MockCloudTransport(connected=False)
    coordinator = SyncCoordinator(queue=queue, transport=transport)

    event1 = {"event": 1}
    event2 = {"event": 2}

    # Offline buffering
    res1 = coordinator.handle_event(event1)
    res2 = coordinator.handle_event(event2)
    assert res1["status"] == "OFFLINE_BUFFERED"
    assert res2["queue_depth"] == 2
    assert len(queue) == 2

    # Reconnect and synchronize
    transport.connect()
    sync_report = coordinator.synchronize()
    assert sync_report["synced_count"] == 2
    assert sync_report["remaining_depth"] == 0
    assert sync_report["status"] == "COMPLETED"
    assert len(transport.delivered_messages) == 2

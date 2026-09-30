"""Maintenance manifest builder and provenance record assembler."""
from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from edge.provenance.hashing import sha256_hex
from shared.contracts import SchemaName, ensure_valid


def build_manifest(
    report_id: str,
    asset_id: str,
    component_id: str,
    sensor_window_hash: str,
    sensor_trust: dict[str, Any],
    health_result: dict[str, Any],
    maintenance_reason: str,
    recommended_action: str,
    priority: str,
    device_id: str,
    sequence_no: int,
    previous_record_hash: str,
    timestamp: str | None = None,
    nonce: str | None = None,
) -> dict[str, Any]:
    """Build a deterministic, canonical manifest dictionary before signing."""
    ts = timestamp or datetime.now(UTC).isoformat()
    n = nonce or f"n-{uuid.uuid4()}"

    manifest_content = {
        "report_id": report_id,
        "asset_id": asset_id,
        "component_id": component_id,
        "sensor_window_hash": sensor_window_hash,
        "sensor_trust": sensor_trust,
        "health_result": health_result,
        "maintenance_reason": maintenance_reason,
        "recommended_action": recommended_action,
        "priority": priority,
        "device_id": device_id,
        "sequence_no": sequence_no,
        "nonce": n,
        "timestamp": ts,
        "previous_record_hash": previous_record_hash,
    }

    # Compute deterministic hash of the manifest content
    m_hash = sha256_hex(manifest_content)
    manifest_content["manifest_hash"] = m_hash
    return manifest_content


def assemble_maintenance_event(manifest: dict[str, Any], digital_signature: str) -> dict[str, Any]:
    """Combine manifest with digital signature and validate against MaintenanceEvent schema."""
    event = dict(manifest)
    event["digital_signature"] = digital_signature
    ensure_valid(event, SchemaName.MAINTENANCE_EVENT)
    return event

"""Maintenance workflow and closure API."""
from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import Any

from cloud.storage.store import EvidenceStore, get_default_store
from edge.ai.adapter import EdgeMLAdapter
from edge.maintenance.repair_effectiveness import improvement
from edge.provenance.signer import DeviceLocalSigner
from shared.contracts import ClosureStatus, SchemaName, ensure_valid


def get_maintenance_state(asset_id: str, store: EvidenceStore | None = None) -> dict[str, Any]:
    """Retrieve current maintenance workflow state for an asset."""
    st = store or get_default_store()
    state = st.get_maintenance_state(asset_id) if hasattr(st, "get_maintenance_state") else None
    if not state:
        return {"asset_id": asset_id, "state": "HEALTHY", "active_report_id": None}
    return dict(state)


def mark_maintenance_started(report_id: str, store: EvidenceStore | None = None) -> dict[str, Any]:
    """Record maintenance-start state while preserving the original diagnostic event intact."""
    st = store or get_default_store()
    event = st.get_event(report_id)
    if not event:
        raise KeyError(f"Diagnostic report not found: {report_id}")

    asset_id = str(event["asset_id"])
    new_state = {
        "asset_id": asset_id,
        "active_report_id": report_id,
        "state": "MAINTENANCE_IN_PROGRESS",
        "started_at": datetime.now(UTC).isoformat(),
        "original_event": dict(event),
    }

    if hasattr(st, "set_maintenance_state"):
        st.set_maintenance_state(asset_id, new_state)

    return {
        "status": "MAINTENANCE_STARTED",
        "report_id": report_id,
        "asset_id": asset_id,
        "prompt": "Maintenance started for this report. The original diagnostic evidence will remain unchanged.",
    }


def perform_retest(
    report_id: str,
    fresh_features: list[float],
    store: EvidenceStore | None = None,
    ml_adapter: EdgeMLAdapter | None = None,
) -> dict[str, Any]:
    """Execute fresh post-maintenance re-test and compute repair effectiveness."""
    st = store or get_default_store()
    event = st.get_event(report_id)
    if not event:
        raise KeyError(f"Diagnostic report not found: {report_id}")

    pre_health_score = float(event.get("health_result", {}).get("health_score", 0.0))

    # Run inference on fresh sensor window
    adapter = ml_adapter or EdgeMLAdapter()
    post_health = adapter.infer(fresh_features)
    post_health_score = post_health.health_score

    # Compute repair effectiveness improvement
    eff = improvement(pre_health_score=pre_health_score, post_health_score=post_health_score)

    # Verification threshold: post health >= 75 and improvement > 0
    if post_health_score >= 75.0 and eff > 0.0:
        outcome = ClosureStatus.VERIFIED.value
        prompt = "Post-maintenance evidence meets the configured repair-verification rule. Closure record can be created."
    else:
        outcome = ClosureStatus.RE_INSPECTION_REQUIRED.value
        prompt = "Post-maintenance evidence did not meet the configured closure rule. Keep the case open for further inspection."

    return {
        "report_id": report_id,
        "pre_health_score": pre_health_score,
        "post_health_score": post_health_score,
        "repair_effectiveness": eff,
        "outcome": outcome,
        "post_condition": post_health.condition,
        "prompt": prompt,
    }


def close_maintenance(
    report_id: str,
    maintenance_action: str,
    post_health_score: float,
    store: EvidenceStore | None = None,
    signer: DeviceLocalSigner | None = None,
) -> dict[str, Any]:
    """Generate signed ClosureRecord and update asset state to closed."""
    st = store or get_default_store()
    event = st.get_event(report_id)
    if not event:
        raise KeyError(f"Diagnostic report not found: {report_id}")

    pre_score = float(event.get("health_result", {}).get("health_score", 0.0))
    eff = improvement(pre_health_score=pre_score, post_health_score=post_health_score)
    closure_status = ClosureStatus.VERIFIED.value if post_health_score >= 75.0 else ClosureStatus.RE_INSPECTION_REQUIRED.value

    closure_id = f"clo-{uuid.uuid4().hex[:8]}"
    ts = datetime.now(UTC).isoformat()

    closure_payload = {
        "closure_id": closure_id,
        "report_id": report_id,
        "maintenance_action": maintenance_action,
        "pre_health_score": pre_score,
        "post_health_score": post_health_score,
        "repair_effectiveness": eff,
        "closure_status": closure_status,
        "timestamp": ts,
    }

    # Cryptographic signature over closure record
    sig_util = signer or DeviceLocalSigner()
    sig = sig_util.sign_manifest(closure_payload)
    closure_payload["digital_signature"] = sig

    ensure_valid(closure_payload, SchemaName.CLOSURE_RECORD)
    st.save_closure(closure_payload)

    # Update asset maintenance state
    asset_id = str(event["asset_id"])
    if hasattr(st, "set_maintenance_state"):
        st.set_maintenance_state(asset_id, {
            "asset_id": asset_id,
            "active_report_id": None,
            "state": "CLOSED" if closure_status == ClosureStatus.VERIFIED.value else "RE_INSPECTION_REQUIRED",
            "last_closure_id": closure_id,
            "closed_at": ts,
        })

    return closure_payload

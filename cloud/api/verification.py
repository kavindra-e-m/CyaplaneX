"""Verification API implementation."""
from __future__ import annotations

from typing import Any

from cloud.ingestion.pipeline import EventIngestionPipeline
from cloud.storage.store import EvidenceStore, get_default_store
from cloud.verification.signature_verifier import verify_event


def verification_status(report_id: str, store: EvidenceStore | None = None) -> dict[str, Any]:
    """Retrieve the verified status and evidence summary for an event report."""
    st = store or get_default_store()
    event = st.get_event(report_id)
    if not event:
        return {"report_id": report_id, "status": "NOT_FOUND", "verified": False}

    is_verified = verify_event(event)
    return {
        "report_id": report_id,
        "status": "PROVENANCE_VERIFIED" if is_verified else "PROVENANCE_VIOLATION",
        "verified": is_verified,
        "asset_id": event.get("asset_id"),
        "component_id": event.get("component_id"),
        "manifest_hash": event.get("manifest_hash"),
        "sequence_no": event.get("sequence_no"),
        "timestamp": event.get("timestamp"),
    }


def ingest_and_verify(event: dict[str, Any], store: EvidenceStore | None = None) -> dict[str, Any]:
    """Submit an event payload through the cloud ingestion and verification pipeline."""
    pipeline = EventIngestionPipeline(store=store)
    return pipeline.ingest_event(event)

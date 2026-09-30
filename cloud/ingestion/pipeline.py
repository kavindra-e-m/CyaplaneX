"""Cloud event ingestion and verification pipeline."""
from __future__ import annotations

from typing import Any

from cloud.storage.store import EvidenceStore, get_default_store
from cloud.verification.replay_checker import accepts_sequence
from cloud.verification.signature_verifier import verify_event
from shared.contracts import SchemaName, validate_contract


class IngestionOutcome:
    INGESTED = "INGESTED"
    REJECTED_INVALID_SCHEMA = "REJECTED_INVALID_SCHEMA"
    REPLAY_REJECTED = "REPLAY_REJECTED"
    PROVENANCE_VIOLATION = "PROVENANCE_VIOLATION"


class EventIngestionPipeline:
    """Ingests incoming diagnostic and maintenance events through verification gates."""

    def __init__(self, store: EvidenceStore | None = None) -> None:
        self.store = store or get_default_store()

    def ingest_event(self, event: dict[str, Any]) -> dict[str, Any]:
        """Process event through schema, replay, and cryptographic verification."""
        # Gate 1: Contract / Schema Validation
        valid, err = validate_contract(event, SchemaName.MAINTENANCE_EVENT)
        if not valid:
            return {
                "status": IngestionOutcome.REJECTED_INVALID_SCHEMA,
                "verified": False,
                "error": err,
            }

        device_id = str(event["device_id"])
        seq_no = int(event["sequence_no"])
        report_id = str(event["report_id"])
        asset_id = str(event["asset_id"])

        # Gate 2: Replay Protection Check
        last_seq = self.store.get_last_sequence(device_id)
        if not accepts_sequence(seq_no, last_seq):
            return {
                "status": IngestionOutcome.REPLAY_REJECTED,
                "verified": False,
                "report_id": report_id,
                "sequence_no": seq_no,
                "last_sequence": last_seq,
                "error": f"Sequence {seq_no} is not strictly greater than previous sequence {last_seq}",
            }

        # Gate 3: Cryptographic / Provenance Signature Verification
        if not verify_event(event):
            return {
                "status": IngestionOutcome.PROVENANCE_VIOLATION,
                "verified": False,
                "report_id": report_id,
                "error": "Digital signature does not match canonical event payload",
            }

        # Gate 4: Persistence
        self.store.set_last_sequence(device_id, seq_no)
        self.store.save_event(event)

        # Update initial maintenance state for asset
        condition = event.get("health_result", {}).get("condition", "HEALTHY")
        state_name = "MAINTENANCE_REQUIRED" if condition != "HEALTHY" else "HEALTHY"
        if hasattr(self.store, "set_maintenance_state"):
            self.store.set_maintenance_state(asset_id, {
                "asset_id": asset_id,
                "active_report_id": report_id,
                "state": state_name,
                "condition": condition,
                "priority": event.get("priority", "P3"),
                "timestamp": event.get("timestamp"),
            })

        return {
            "status": IngestionOutcome.INGESTED,
            "verified": True,
            "report_id": report_id,
            "sequence_no": seq_no,
            "asset_id": asset_id,
        }

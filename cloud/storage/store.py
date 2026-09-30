"""Storage interfaces and in-memory evidence store for local development and demos."""
from __future__ import annotations

from typing import Any, Protocol


class EvidenceStore(Protocol):
    """Protocol for persisting and retrieving verified evidence records."""
    def save_event(self, event: dict[str, Any]) -> None: ...
    def get_event(self, report_id: str) -> dict[str, Any] | None: ...
    def list_events_for_asset(self, asset_id: str) -> list[dict[str, Any]]: ...
    def save_closure(self, closure: dict[str, Any]) -> None: ...
    def get_closure(self, closure_id: str) -> dict[str, Any] | None: ...
    def get_passport_records(self, component_id: str) -> list[dict[str, Any]]: ...
    def get_last_sequence(self, device_id: str) -> int | None: ...
    def set_last_sequence(self, device_id: str, seq: int) -> None: ...


class InMemoryEvidenceStore:
    """Thread-safe in-memory store for development, demonstration, and tests."""

    def __init__(self) -> None:
        self.events: dict[str, dict[str, Any]] = {}
        self.closures: dict[str, dict[str, Any]] = {}
        self.last_sequences: dict[str, int] = {}
        self.maintenance_states: dict[str, dict[str, Any]] = {}

    def save_event(self, event: dict[str, Any]) -> None:
        report_id = str(event["report_id"])
        self.events[report_id] = dict(event)

    def get_event(self, report_id: str) -> dict[str, Any] | None:
        item = self.events.get(report_id)
        return dict(item) if item else None

    def list_events_for_asset(self, asset_id: str) -> list[dict[str, Any]]:
        return [dict(e) for e in self.events.values() if e.get("asset_id") == asset_id]

    def save_closure(self, closure: dict[str, Any]) -> None:
        closure_id = str(closure["closure_id"])
        self.closures[closure_id] = dict(closure)

    def get_closure(self, closure_id: str) -> dict[str, Any] | None:
        item = self.closures.get(closure_id)
        return dict(item) if item else None

    def get_passport_records(self, component_id: str) -> list[dict[str, Any]]:
        records: list[dict[str, Any]] = []
        for e in self.events.values():
            if e.get("component_id") == component_id:
                records.append({
                    "record_type": "DIAGNOSTIC_EVENT",
                    "report_id": e.get("report_id"),
                    "timestamp": e.get("timestamp"),
                    "condition": e.get("health_result", {}).get("condition"),
                    "health_score": e.get("health_result", {}).get("health_score"),
                    "sensor_trust": e.get("sensor_trust", {}).get("trust_status"),
                    "manifest_hash": e.get("manifest_hash"),
                })
        for c in self.closures.values():
            rep = self.events.get(c.get("report_id", ""))
            if rep and rep.get("component_id") == component_id:
                records.append({
                    "record_type": "MAINTENANCE_CLOSURE",
                    "closure_id": c.get("closure_id"),
                    "report_id": c.get("report_id"),
                    "timestamp": c.get("timestamp"),
                    "action": c.get("maintenance_action"),
                    "repair_effectiveness": c.get("repair_effectiveness"),
                    "closure_status": c.get("closure_status"),
                })
        # Sort chronologically
        return sorted(records, key=lambda r: str(r.get("timestamp", "")))

    def get_last_sequence(self, device_id: str) -> int | None:
        return self.last_sequences.get(device_id)

    def set_last_sequence(self, device_id: str, seq: int) -> None:
        self.last_sequences[device_id] = seq

    def set_maintenance_state(self, asset_id: str, state: dict[str, Any]) -> None:
        self.maintenance_states[asset_id] = dict(state)

    def get_maintenance_state(self, asset_id: str) -> dict[str, Any] | None:
        item = self.maintenance_states.get(asset_id)
        return dict(item) if item else None


_GLOBAL_STORE = InMemoryEvidenceStore()


def get_default_store() -> InMemoryEvidenceStore:
    return _GLOBAL_STORE

"""Component digital passport and maintenance history API."""
from __future__ import annotations

from typing import Any

from cloud.storage.store import EvidenceStore, get_default_store


def get_passport(component_id: str, store: EvidenceStore | None = None) -> dict[str, Any]:
    """Return verified historical records and digital passport for a component."""
    st = store or get_default_store()
    records = st.get_passport_records(component_id)
    return {
        "component_id": component_id,
        "total_records": len(records),
        "records": records,
    }

"""Maintenance manifest boundary."""
from typing import Any


def build_manifest(**fields: Any) -> dict[str, Any]:
    """Build a transparent manifest; signing is handled by a separate boundary."""
    return dict(fields)

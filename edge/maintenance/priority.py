"""Maintenance prioritization placeholder."""

def prioritize(severity: str) -> str:
    """Map known severity labels to draft priorities."""
    return {"CRITICAL": "P1", "WARNING": "P2", "HEALTHY": "P3"}.get(severity, "UNSET")

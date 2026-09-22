"""Health API placeholder with a framework-neutral smoke-test function."""
from typing import Any


def get_health() -> dict[str, Any]:
    """Return the service health response."""
    return {"status": "ok", "service": "aerotrust-verification-api"}

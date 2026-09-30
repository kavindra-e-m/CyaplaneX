"""Framework-neutral API smoke test."""
from cloud.api.health import get_health


def test_health_endpoint_contract() -> None:
    assert get_health() == {"status": "ok", "service": "cyaplanex-verification-api"}

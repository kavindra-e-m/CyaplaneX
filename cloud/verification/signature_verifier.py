"""Deterministic scaffold verifier for signed event fixtures."""
from typing import Any

from edge.provenance.hashing import sha256_hex


def event_payload(event: dict[str, Any]) -> dict[str, Any]:
    """Remove the signature field before computing the expected digest."""
    return {key: value for key, value in event.items() if key != "digital_signature"}


def verify_event(event: dict[str, Any]) -> bool:
    """Verify a fixture signature represented by a SHA-256 digest.

    Production asymmetric signing is intentionally deferred; this keeps the contract
    testable without private keys while making tampering behavior explicit.
    """
    signature = event.get("digital_signature")
    return isinstance(signature, str) and signature == sha256_hex(event_payload(event))

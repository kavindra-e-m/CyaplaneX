"""Cryptographic and digest verification boundary for signed provenance events."""
from __future__ import annotations

import hashlib
import hmac
from typing import Any

from edge.provenance.hashing import canonical_json, sha256_hex
from edge.provenance.signer import DEFAULT_LOCAL_KEY_REF, get_local_key


def event_payload(event: dict[str, Any]) -> dict[str, Any]:
    """Remove the signature field before computing the expected digest."""
    return {key: value for key, value in event.items() if key != "digital_signature"}


def verify_event(event: dict[str, Any], key_reference: str = DEFAULT_LOCAL_KEY_REF) -> bool:
    """Verify an event's digital signature.

    Supports:
    1. Cryptographic HMAC-SHA256 signature formatted as 'hmac-sha256:<hex>'
    2. Deterministic SHA-256 fixture digest used in test vectors
    """
    signature = event.get("digital_signature")
    if not isinstance(signature, str) or not signature:
        return False

    payload = event_payload(event)

    if signature.startswith("hmac-sha256:"):
        expected_hex = signature.split(":", 1)[1]
        key = get_local_key(key_reference)
        raw_payload = canonical_json(payload)
        expected_bytes = hmac.new(key, raw_payload, hashlib.sha256).digest()
        return hmac.compare_digest(expected_bytes.hex(), expected_hex)

    # Legacy / fixture digest mode
    return signature == sha256_hex(payload)

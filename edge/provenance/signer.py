"""Device-local cryptographic signing boundary.

Produces cryptographic signatures over canonical manifests using local key references
without requiring live cloud or KMS connectivity.
"""
from __future__ import annotations

import hashlib
import hmac
import os
from typing import Any

from edge.provenance.hashing import canonical_json, sha256_hex

# Default local demonstrator signing secret; overridden by env or HSM reference in production
DEFAULT_LOCAL_KEY_REF = "cyaplanex-edge-dev-key-01"
_LOCAL_KEY_STORE: dict[str, bytes] = {
    DEFAULT_LOCAL_KEY_REF: b"cyaplanex-prototype-device-secret-2026",
    "aerotrust-edge-dev-key-01": b"cyaplanex-prototype-device-secret-2026",
}


def get_local_key(key_reference: str) -> bytes:
    """Resolve local key material from key reference or environment."""
    env_key = os.environ.get("CYAPLANEX_DEVICE_KEY") or os.environ.get("AEROTRUST_DEVICE_KEY")
    if env_key:
        return env_key.encode("utf-8")
    if key_reference in _LOCAL_KEY_STORE:
        return _LOCAL_KEY_STORE[key_reference]
    # Derive deterministic device key from reference name for demonstrator
    return hashlib.sha256(key_reference.encode("utf-8")).digest()


def sign_locally(payload: bytes, private_key_reference: str) -> bytes:
    """Generate an HMAC-SHA256 signature bytes over raw payload using a local key reference."""
    if not private_key_reference:
        raise ValueError("a local key reference is required")
    key = get_local_key(private_key_reference)
    sig = hmac.new(key, payload, hashlib.sha256).digest()
    return sig


class DeviceLocalSigner:
    """Manages offline-capable device signature generation for provenance manifests."""

    def __init__(self, key_reference: str = DEFAULT_LOCAL_KEY_REF) -> None:
        self.key_reference = key_reference

    def sign_manifest(self, manifest: dict[str, Any]) -> str:
        """Sign a canonical manifest dictionary and return a formatted signature string."""
        # Clean signature if present
        clean = {k: v for k, v in manifest.items() if k != "digital_signature"}
        raw_bytes = canonical_json(clean)
        raw_sig = sign_locally(raw_bytes, self.key_reference)
        return f"hmac-sha256:{raw_sig.hex()}"

    def sign_fixture_digest(self, manifest: dict[str, Any]) -> str:
        """Generate a SHA-256 fixture digest signature for legacy test fixtures."""
        clean = {k: v for k, v in manifest.items() if k != "digital_signature"}
        return sha256_hex(clean)

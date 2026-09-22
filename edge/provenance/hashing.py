"""Canonical hashing helpers for provenance evidence."""
import hashlib
import json
from typing import Any


def canonical_json(value: Any) -> bytes:
    """Encode JSON deterministically for hashing and signing boundaries."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def sha256_hex(value: Any) -> str:
    """Return a SHA-256 digest of a JSON-compatible value."""
    return hashlib.sha256(canonical_json(value)).hexdigest()

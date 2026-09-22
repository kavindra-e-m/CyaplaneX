"""Provenance determinism and tamper detection tests."""
from cloud.verification.signature_verifier import verify_event
from edge.provenance.hashing import sha256_hex


def test_hash_is_deterministic_for_key_order() -> None:
    assert sha256_hex({"b": 2, "a": 1}) == sha256_hex({"a": 1, "b": 2})


def test_valid_and_modified_event_verification() -> None:
    event = {"report_id": "r-1", "sequence_no": 1}
    event["digital_signature"] = sha256_hex({"report_id": "r-1", "sequence_no": 1})
    assert verify_event(event)
    event["sequence_no"] = 2
    assert not verify_event(event)

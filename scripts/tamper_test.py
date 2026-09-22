"""Demonstrate expected rejection after changing a signed event field."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cloud.verification.signature_verifier import verify_event
from edge.provenance.hashing import sha256_hex


def sample_event() -> dict[str, object]:
    event: dict[str, object] = {"report_id": "demo-1", "sequence_no": 1}
    event["digital_signature"] = sha256_hex({"report_id": "demo-1", "sequence_no": 1})
    return event


if __name__ == "__main__":
    event = sample_event()
    print(f"before modification: {verify_event(event)}")
    event["sequence_no"] = 2
    print(f"after modification: {verify_event(event)} (expected False)")

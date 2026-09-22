"""Replay-protection tests."""
from cloud.verification.replay_checker import accepts_sequence


def test_newer_sequence_is_accepted() -> None:
    assert accepts_sequence(4, 3)


def test_duplicate_and_old_sequences_are_rejected() -> None:
    assert not accepts_sequence(3, 3)
    assert not accepts_sequence(2, 3)

"""Replay protection boundary for sequence-numbered edge events."""


def accepts_sequence(sequence_no: int, last_sequence: int | None) -> bool:
    """Accept only a strictly newer sequence number."""
    return sequence_no >= 0 and (last_sequence is None or sequence_no > last_sequence)

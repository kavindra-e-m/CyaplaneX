"""Freshness check placeholder."""
from datetime import UTC, datetime


def is_fresh(timestamp: datetime, max_age_seconds: float, now: datetime | None = None) -> bool:
    """Return whether a timestamp is within an allowed age window."""
    reference = now or datetime.now(UTC)
    return 0 <= (reference - timestamp).total_seconds() <= max_age_seconds

"""Freshness check placeholder."""
from datetime import datetime, timezone


def is_fresh(timestamp: datetime, max_age_seconds: float, now: datetime | None = None) -> bool:
    """Return whether a timestamp is within an allowed age window."""
    reference = now or datetime.now(timezone.utc)
    return 0 <= (reference - timestamp).total_seconds() <= max_age_seconds

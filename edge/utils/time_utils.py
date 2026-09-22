"""Time utilities boundary."""
from datetime import datetime, timezone


def utc_now() -> datetime:
    """Return an aware UTC timestamp."""
    return datetime.now(timezone.utc)

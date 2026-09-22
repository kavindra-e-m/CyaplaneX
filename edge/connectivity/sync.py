"""Store-and-forward synchronization placeholder."""

def sync_pending() -> int:
    """Return zero until a durable queue and cloud client are configured."""
    # TODO: Preserve ordering and idempotency during reconnect.
    return 0

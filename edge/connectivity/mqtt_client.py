"""MQTT client boundary placeholder."""

def publish(topic: str, payload: bytes) -> None:
    """Publish nothing until broker and authentication configuration exist."""
    # TODO: Integrate AWS IoT authentication and retry policy.
    raise NotImplementedError(f"MQTT publish not configured for {topic}")

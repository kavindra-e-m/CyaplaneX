"""MQTT client and cloud transport boundary."""
from __future__ import annotations

import json
from typing import Any, Protocol


class CloudTransport(Protocol):
    """Protocol for cloud telemetry and event delivery."""
    def send(self, topic: str, payload: dict[str, Any]) -> bool: ...
    def is_connected(self) -> bool: ...


class MockCloudTransport:
    """In-memory transport for local development, simulation, and tests."""

    def __init__(self, connected: bool = True) -> None:
        self.connected = connected
        self.delivered_messages: list[tuple[str, dict[str, Any]]] = []

    def send(self, topic: str, payload: dict[str, Any]) -> bool:
        if not self.connected:
            return False
        self.delivered_messages.append((topic, dict(payload)))
        return True

    def is_connected(self) -> bool:
        return self.connected

    def disconnect(self) -> None:
        self.connected = False

    def connect(self) -> None:
        self.connected = True


_DEFAULT_TRANSPORT: CloudTransport = MockCloudTransport()


def get_default_transport() -> CloudTransport:
    return _DEFAULT_TRANSPORT


def set_default_transport(transport: CloudTransport) -> None:
    global _DEFAULT_TRANSPORT
    _DEFAULT_TRANSPORT = transport


def publish(topic: str, payload: bytes | dict[str, Any]) -> None:
    """Publish to configured transport. Raises ConnectionError if unreachable."""
    transport = get_default_transport()
    if isinstance(payload, bytes):
        data = json.loads(payload.decode("utf-8"))
    else:
        data = payload

    success = transport.send(topic, data)
    if not success:
        raise ConnectionError(f"Cloud transport offline; could not publish to {topic}")

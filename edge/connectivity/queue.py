"""Offline store-and-forward queue placeholder."""
from collections import deque
from typing import Any


class OfflineQueue:
    """Small in-memory queue used until durable edge storage is selected."""

    def __init__(self) -> None:
        self._items: deque[dict[str, Any]] = deque()

    def put(self, event: dict[str, Any]) -> None:
        self._items.append(event)

    def drain(self) -> list[dict[str, Any]]:
        items = list(self._items)
        self._items.clear()
        return items

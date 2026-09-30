"""Offline store-and-forward queue with deterministic ordering and bounded capacity."""
from __future__ import annotations

from collections import deque
from typing import Any


class QueueCapacityExceededError(Exception):
    """Raised when queue exceeds configured capacity to prevent silent event drop."""


class OfflineQueue:
    """Store-and-forward queue buffering signed events during offline operation."""

    def __init__(self, max_capacity: int = 1000) -> None:
        self.max_capacity = max_capacity
        self._items: deque[dict[str, Any]] = deque()

    def put(self, event: dict[str, Any]) -> None:
        """Enqueue an event. Raises QueueCapacityExceededError if full."""
        if len(self._items) >= self.max_capacity:
            raise QueueCapacityExceededError(f"Offline queue reached maximum capacity: {self.max_capacity}")
        self._items.append(dict(event))

    def peek(self) -> dict[str, Any] | None:
        """Inspect the oldest queued event without removing it."""
        return dict(self._items[0]) if self._items else None

    def drain(self, max_batch_size: int | None = None) -> list[dict[str, Any]]:
        """Drain up to max_batch_size events in FIFO order."""
        if not self._items:
            return []

        if max_batch_size is None or max_batch_size >= len(self._items):
            items = [dict(e) for e in self._items]
            self._items.clear()
            return items

        items = []
        for _ in range(max_batch_size):
            items.append(dict(self._items.popleft()))
        return items

    def re_enqueue_front(self, events: list[dict[str, Any]]) -> None:
        """Prepend events back to the front of the queue after a transient delivery failure."""
        for e in reversed(events):
            self._items.appendleft(dict(e))

    def __len__(self) -> int:
        return len(self._items)

    @property
    def is_empty(self) -> bool:
        return len(self._items) == 0

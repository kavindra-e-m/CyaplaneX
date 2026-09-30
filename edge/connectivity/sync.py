"""Store-and-forward synchronization coordinator."""
from __future__ import annotations

from typing import Any

from edge.connectivity.mqtt_client import CloudTransport, get_default_transport
from edge.connectivity.queue import OfflineQueue

_DEFAULT_QUEUE = OfflineQueue()


def get_default_queue() -> OfflineQueue:
    return _DEFAULT_QUEUE


def sync_pending(
    queue: OfflineQueue | None = None,
    transport: CloudTransport | None = None,
    topic: str = "aerotrust/events/maintenance",
    batch_size: int = 50,
) -> int:
    """Drain queued events and synchronize them across the transport.

    Returns the number of events successfully synchronized.
    If the transport is offline or fails, pending events are safely re-enqueued.
    """
    q = queue or get_default_queue()
    tp = transport or get_default_transport()

    if not tp.is_connected() or q.is_empty:
        return 0

    batch = q.drain(max_batch_size=batch_size)
    delivered = 0

    for i, event in enumerate(batch):
        sent = tp.send(topic, event)
        if not sent:
            # Re-enqueue undelivered events back to the front of queue
            unreached = batch[i:]
            q.re_enqueue_front(unreached)
            break
        delivered += 1

    return delivered


class SyncCoordinator:
    """Coordinates offline queuing and online synchronization."""

    def __init__(self, queue: OfflineQueue, transport: CloudTransport) -> None:
        self.queue = queue
        self.transport = transport

    def handle_event(self, event: dict[str, Any], topic: str = "aerotrust/events/maintenance") -> dict[str, Any]:
        """Dispatch event immediately if online, otherwise buffer locally."""
        if self.transport.is_connected():
            sent = self.transport.send(topic, event)
            if sent:
                return {"status": "ONLINE_PUBLISHED", "queue_depth": len(self.queue)}

        # Buffer offline
        self.queue.put(event)
        return {"status": "OFFLINE_BUFFERED", "queue_depth": len(self.queue)}

    def synchronize(self, topic: str = "aerotrust/events/maintenance", batch_size: int = 100) -> dict[str, Any]:
        """Synchronize buffered records upon connectivity restoration."""
        initial_depth = len(self.queue)
        synced = sync_pending(queue=self.queue, transport=self.transport, topic=topic, batch_size=batch_size)
        return {
            "initial_depth": initial_depth,
            "synced_count": synced,
            "remaining_depth": len(self.queue),
            "status": "COMPLETED" if len(self.queue) == 0 else "PARTIAL",
        }

"""Sensor acquisition service.

Acquires readings across registered sensor adapters (physical, simulated, or replay)
and packages them into contract-compliant SensorSample records.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Protocol

from shared.contracts import SchemaName, ensure_valid


class SensorReader(Protocol):
    """Protocol satisfied by any sensor adapter."""
    def read(self) -> float: ...


class SensorDescriptor:
    """Metadata describing a sensor channel."""

    def __init__(
        self,
        sensor_id: str,
        sensor_type: str,
        unit: str,
        calibration_version: str,
        reader: SensorReader,
    ) -> None:
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.unit = unit
        self.calibration_version = calibration_version
        self.reader = reader
        self.sequence: int = 0


class SensorAcquisitionService:
    """Manages sensor acquisition channels and produces validated SensorSample payloads."""

    def __init__(self, device_id: str = "rpi5-edge-01") -> None:
        self.device_id = device_id
        self._channels: dict[str, SensorDescriptor] = {}

    def register_sensor(
        self,
        sensor_id: str,
        sensor_type: str,
        unit: str,
        calibration_version: str,
        reader: SensorReader,
    ) -> None:
        """Register a sensor reader channel."""
        self._channels[sensor_id] = SensorDescriptor(
            sensor_id=sensor_id,
            sensor_type=sensor_type,
            unit=unit,
            calibration_version=calibration_version,
            reader=reader,
        )

    def acquire_sample(self, sensor_id: str, timestamp: datetime | None = None) -> dict[str, Any]:
        """Read a single sensor and return a validated SensorSample dictionary."""
        if sensor_id not in self._channels:
            raise KeyError(f"Sensor not registered: {sensor_id}")

        descriptor = self._channels[sensor_id]
        raw_val = descriptor.reader.read()
        ts = (timestamp or datetime.now(UTC)).isoformat()
        seq = descriptor.sequence
        descriptor.sequence += 1

        sample: dict[str, Any] = {
            "device_id": self.device_id,
            "sensor_id": descriptor.sensor_id,
            "timestamp": ts,
            "sequence": seq,
            "sensor_type": descriptor.sensor_type,
            "value": float(raw_val),
            "unit": descriptor.unit,
            "calibration_version": descriptor.calibration_version,
        }

        ensure_valid(sample, SchemaName.SENSOR_SAMPLE)
        return sample

    def acquire_all(self, timestamp: datetime | None = None) -> list[dict[str, Any]]:
        """Acquire samples from all registered channels."""
        ts = timestamp or datetime.now(UTC)
        return [self.acquire_sample(s_id, timestamp=ts) for s_id in self._channels]

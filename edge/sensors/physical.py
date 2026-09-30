"""Physical Hardware-in-the-Loop (HIL) sensor streaming adapter.

Provides a SerialStreamSensorReader that ingests telemetry from an ESP32 or
microcontroller over serial UART/USB CDC and satisfies the SensorReader protocol.
Permits seamless transition from simulated/replay sensors to physical hardware.
"""
from __future__ import annotations

import json
import logging
from collections import deque
from typing import TextIO

logger = logging.getLogger("cyaplanex.edge.sensors.physical")


class SerialStreamSensorReader:
    """Reads sensor measurements from a serial stream or text buffer.

    Implements the SensorReader protocol (`read() -> float`).
    Can be connected to a real serial port (e.g., PySerial `serial.Serial`)
    or fed via an in-memory buffer/stream for testing.
    """

    def __init__(
        self,
        sensor_id: str,
        stream: TextIO | None = None,
        default_fallback: float = 0.0,
    ) -> None:
        self.sensor_id = sensor_id
        self.stream = stream
        self.default_fallback = default_fallback
        self._buffered_readings: deque[float] = deque()
        self._last_reading: float = default_fallback

    def feed_line(self, line: str) -> None:
        """Feed an incoming stream line (CSV or JSON format) into the buffer."""
        clean = line.strip()
        if not clean:
            return

        # Attempt JSON parsing: {"sensor_id": "vib-01", "value": 0.35}
        if clean.startswith("{") and clean.endswith("}"):
            try:
                data = json.loads(clean)
                if data.get("sensor_id") == self.sensor_id:
                    self._buffered_readings.append(float(data["value"]))
                    return
            except (json.JSONDecodeError, KeyError, ValueError) as err:
                logger.debug("Failed to parse JSON packet: %s", err)

        # Attempt CSV parsing: "vib-01,0.35" or just "0.35"
        parts = clean.split(",")
        if len(parts) == 2 and parts[0].strip() == self.sensor_id:
            try:
                self._buffered_readings.append(float(parts[1].strip()))
                return
            except ValueError as err:
                logger.debug("Failed to parse CSV numeric value: %s", err)
        elif len(parts) == 1:
            try:
                self._buffered_readings.append(float(parts[0].strip()))
            except ValueError as err:
                logger.debug("Failed to parse single numeric line: %s", err)

    def read(self) -> float:
        """Read the next available measurement from the stream or buffer."""
        # Drain line from active text stream if attached
        if self.stream is not None:
            try:
                line = self.stream.readline()
                if line:
                    self.feed_line(line)
            except (OSError, UnicodeDecodeError) as err:
                logger.warning("Stream read error on sensor %s: %s", self.sensor_id, err)

        if self._buffered_readings:
            self._last_reading = self._buffered_readings.popleft()
            return self._last_reading

        # Return last known reading if buffer is temporarily dry
        return self._last_reading


"""Application-side feature extraction and windowing pipeline.

Aggregates SensorSample streams into windowed feature vectors and computes
the deterministic sensor_window_hash for cryptographic provenance binding.
"""
from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, ClassVar

from edge.provenance.hashing import sha256_hex


@dataclass(frozen=True)
class PreprocessedWindow:
    """Preprocessed window ready for the ML adapter and provenance engine."""
    feature_names: list[str]
    features: list[float]
    sensor_window_hash: str
    sample_count: int
    timestamp_start: str
    timestamp_end: str


class FeaturePipeline:
    """Extracts baseline statistical features from grouped sensor samples."""

    FEATURE_NAMES: ClassVar[list[str]] = [
        "vib_rms",
        "vib_p2p",
        "temp_mean",
        "temp_max",
        "rpm_mean",
        "rpm_std",
    ]

    def process_window(self, samples: Sequence[dict[str, Any]]) -> PreprocessedWindow:
        """Process a collection of SensorSample dictionaries into a feature vector and window hash."""
        if not samples:
            raise ValueError("samples sequence cannot be empty")

        # Sort samples deterministically by sequence & timestamp for consistent window hashing
        ordered_samples = sorted(samples, key=lambda s: (s.get("sequence", 0), s.get("timestamp", "")))

        # Group values by sensor_type
        vib_vals: list[float] = []
        temp_vals: list[float] = []
        rpm_vals: list[float] = []

        for s in ordered_samples:
            stype = s.get("sensor_type", "")
            val = float(s["value"])
            if stype == "vibration":
                vib_vals.append(val)
            elif stype == "temperature":
                temp_vals.append(val)
            elif stype == "rpm":
                rpm_vals.append(val)

        # Statistical calculations
        vib_rms = math.sqrt(sum(x ** 2 for x in vib_vals) / len(vib_vals)) if vib_vals else 0.0
        vib_p2p = (max(vib_vals) - min(vib_vals)) if vib_vals else 0.0

        temp_mean = (sum(temp_vals) / len(temp_vals)) if temp_vals else 0.0
        temp_max = max(temp_vals) if temp_vals else 0.0

        rpm_mean = (sum(rpm_vals) / len(rpm_vals)) if rpm_vals else 0.0
        if rpm_vals and len(rpm_vals) > 1:
            rpm_std = math.sqrt(sum((x - rpm_mean) ** 2 for x in rpm_vals) / (len(rpm_vals) - 1))
        else:
            rpm_std = 0.0

        features = [
            round(vib_rms, 4),
            round(vib_p2p, 4),
            round(temp_mean, 2),
            round(temp_max, 2),
            round(rpm_mean, 1),
            round(rpm_std, 2),
        ]

        # Compute deterministic window hash from canonical samples
        window_hash = sha256_hex(ordered_samples)

        return PreprocessedWindow(
            feature_names=list(self.FEATURE_NAMES),
            features=features,
            sensor_window_hash=window_hash,
            sample_count=len(ordered_samples),
            timestamp_start=str(ordered_samples[0]["timestamp"]),
            timestamp_end=str(ordered_samples[-1]["timestamp"]),
        )

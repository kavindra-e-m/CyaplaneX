"""Stable ML inference adapter boundary.

Translates preprocessed sensor feature vectors into contract-compliant HealthResult
objects. Provides a pluggable runtime interface for Monhit's exported ML artifacts.
"""
from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Protocol

from edge.ai.health_engine import HealthResult
from edge.provenance.hashing import sha256_hex
from shared.contracts import HealthSeverity, SchemaName, ensure_valid


class InferenceModel(Protocol):
    """Callable interface expected from an exported model artifact."""
    def predict(self, features: Sequence[float]) -> dict[str, Any]: ...


class BaselineDemonstratorModel:
    """Explicit development baseline model used prior to Monhit's artifact handoff.

    Calculates physics-informed vibration and temperature anomaly scores.
    """

    MODEL_ID = "cyaplanex-baseline-eval-v1"
    MODEL_VERSION = "1.0.0"
    MODEL_HASH = sha256_hex({"id": MODEL_ID, "version": MODEL_VERSION, "owner": "Monhit-Raju-ML"})

    def predict(self, features: Sequence[float]) -> dict[str, Any]:
        """Predict condition and health scores from [vib_rms, vib_p2p, temp_mean, temp_max, rpm_mean, rpm_std]."""
        if len(features) < 6:
            raise ValueError(f"Expected at least 6 features, received {len(features)}")

        vib_rms, _vib_p2p, _temp_mean, temp_max, _rpm_mean, rpm_std = features[:6]

        # Anomaly score calculation
        vib_penalty = max(0.0, min(1.0, (vib_rms - 0.4) / 1.6)) if vib_rms > 0.4 else 0.0
        temp_penalty = max(0.0, min(1.0, (temp_max - 60.0) / 40.0)) if temp_max > 60.0 else 0.0
        rpm_penalty = max(0.0, min(1.0, rpm_std / 50.0)) if rpm_std > 20.0 else 0.0

        raw_anomaly = max(vib_penalty, temp_penalty, rpm_penalty * 0.5)
        anomaly_score = round(max(0.0, min(1.0, raw_anomaly)), 4)
        health_score = round(max(0.0, min(100.0, 100.0 * (1.0 - anomaly_score))), 1)

        # Condition diagnosis
        if vib_rms > 1.4:
            condition = "HIGH_VIBRATION"
        elif temp_max > 85.0:
            condition = "OVERHEATING"
        elif rpm_std > 40.0:
            condition = "SPEED_INSTABILITY"
        elif anomaly_score > 0.25:
            condition = "MECHANICAL_WEAR"
        else:
            condition = "HEALTHY"

        # Severity
        if health_score < 40.0:
            severity = HealthSeverity.CRITICAL.value
        elif health_score < 75.0:
            severity = HealthSeverity.WARNING.value
        else:
            severity = HealthSeverity.HEALTHY.value

        confidence = 0.94 if condition == "HEALTHY" else 0.91

        return {
            "condition": condition,
            "anomaly_score": anomaly_score,
            "health_score": health_score,
            "confidence": confidence,
            "severity": severity,
            "model_id": self.MODEL_ID,
            "model_version": self.MODEL_VERSION,
            "model_hash": self.MODEL_HASH,
        }


class EdgeMLAdapter:
    """Manages model lifecycle and executes inference against preprocessed features."""

    def __init__(self, model: InferenceModel | None = None) -> None:
        self.model = model or BaselineDemonstratorModel()

    def infer(self, features: Sequence[float]) -> HealthResult:
        """Execute inference and return a validated HealthResult value object."""
        raw = self.model.predict(features)

        result = HealthResult(
            condition=str(raw["condition"]),
            anomaly_score=float(raw["anomaly_score"]),
            health_score=float(raw["health_score"]),
            confidence=float(raw["confidence"]),
            severity=str(raw["severity"]),
            model_id=str(raw["model_id"]),
            model_version=str(raw["model_version"]),
            model_hash=str(raw["model_hash"]),
        )

        ensure_valid(result.to_dict(), SchemaName.HEALTH_RESULT)
        return result

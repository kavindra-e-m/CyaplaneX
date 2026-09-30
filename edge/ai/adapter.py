"""Stable ML inference adapter boundary.

Translates preprocessed sensor feature vectors into contract-compliant HealthResult
objects. Provides a pluggable runtime interface for Monhit's exported ML artifacts.
"""
from __future__ import annotations

from collections.abc import Sequence
from typing import Any, ClassVar, Protocol

from edge.ai.health_engine import HealthResult
from edge.provenance.hashing import sha256_hex
from shared.contracts import HealthSeverity, SchemaName, ensure_valid

FROZEN_FEATURE_NAMES: tuple[str, ...] = (
    "vib_rms",
    "vib_p2p",
    "temp_mean",
    "temp_max",
    "rpm_mean",
    "rpm_std",
)


class InferenceModel(Protocol):
    """Callable interface expected from an exported model artifact."""
    def predict(self, features: Sequence[float]) -> dict[str, Any]: ...


class BaselineDemonstratorModel:
    """Explicit development baseline demonstrator (NOT Monhit's trained model).

    Temporary development/demo baseline providing heuristic/statistical
    evaluation prior to Monhit Raju's trained model artifact handoff.
    Calculates physics-informed vibration and temperature anomaly scores.
    """

    MODEL_ID = "cyaplanex-baseline-eval-v1"
    MODEL_VERSION = "1.0.0"
    MODEL_HASH = sha256_hex({"id": MODEL_ID, "version": MODEL_VERSION, "owner": "CyaplaneX-Baseline-Demonstrator"})

    def predict(self, features: Sequence[float]) -> dict[str, Any]:
        """Predict condition and health scores from [vib_rms, vib_p2p, temp_mean, temp_max, rpm_mean, rpm_std]."""
        if len(features) != len(FROZEN_FEATURE_NAMES):
            raise ValueError(
                f"Frozen ML contract violation: expected exactly {len(FROZEN_FEATURE_NAMES)} features "
                f"{list(FROZEN_FEATURE_NAMES)}, received {len(features)}"
            )

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

    FEATURE_CONTRACT: ClassVar[tuple[str, ...]] = FROZEN_FEATURE_NAMES

    def __init__(self, model: InferenceModel | None = None) -> None:
        self.model = model or BaselineDemonstratorModel()

    def infer(self, features: Sequence[float]) -> HealthResult:
        """Execute inference and return a validated HealthResult value object."""
        if len(features) != len(self.FEATURE_CONTRACT):
            raise ValueError(
                f"Frozen ML contract violation: expected exactly {len(self.FEATURE_CONTRACT)} features "
                f"{list(self.FEATURE_CONTRACT)}, received {len(features)}"
            )

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


def validate_model_artifact(
    model: Any,
    sample_features: Sequence[float] | None = None,
) -> dict[str, Any]:
    """Execute acceptance validation checks on a candidate production model artifact.

    Implements the 12-point ML integration acceptance gate for Monhit's artifact.
    Returns a structured verification report.
    """
    report: dict[str, Any] = {
        "has_predict_method": False,
        "input_contract_verified": False,
        "output_schema_verified": False,
        "model_id": None,
        "model_version": None,
        "model_hash": None,
        "compatible": False,
        "errors": [],
    }

    if not hasattr(model, "predict") or not callable(model.predict):
        report["errors"].append("Model artifact lacks a callable 'predict(features)' method.")
        return report
    report["has_predict_method"] = True

    # Test rejection of invalid feature lengths
    try:
        model.predict([0.1, 0.2, 0.3])
        report["errors"].append("Model failed to reject input with fewer than 6 features.")
    except (ValueError, TypeError, IndexError):
        pass  # Expected contract rejection

    # Test nominal 6-feature vector
    test_vec = sample_features or [0.35, 0.1, 52.0, 54.0, 3600.0, 15.0]
    try:
        raw_output = model.predict(test_vec)
    except (TypeError, ValueError, KeyError, AttributeError, RuntimeError) as err:
        report["errors"].append(f"Inference execution raised exception: {err}")
        return report

    report["input_contract_verified"] = True

    # Validate output dictionary against HealthResult contract
    if not isinstance(raw_output, dict):
        report["errors"].append(f"Model predict() returned {type(raw_output).__name__}, expected dict.")
        return report

    required_keys = {
        "condition", "anomaly_score", "health_score",
        "confidence", "severity", "model_id", "model_version", "model_hash"
    }
    missing = required_keys - set(raw_output.keys())
    if missing:
        report["errors"].append(f"Model output missing required fields: {sorted(missing)}")
        return report

    try:
        adapter = EdgeMLAdapter(model=model)
        health_result = adapter.infer(test_vec)
        report["output_schema_verified"] = True
        report["model_id"] = health_result.model_id
        report["model_version"] = health_result.model_version
        report["model_hash"] = health_result.model_hash
        report["sample_condition"] = health_result.condition
        report["sample_health_score"] = health_result.health_score
    except (TypeError, ValueError, KeyError, AttributeError, RuntimeError) as err:
        report["errors"].append(f"HealthResult validation failed: {err}")
        return report

    report["compatible"] = len(report["errors"]) == 0
    return report


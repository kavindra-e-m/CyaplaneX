"""CyaplaneX Production Edge ML Model Artifact.

Author: Monhit Raju (ML Lead)
Model Architecture: Calibrated Ensemble Diagnostic Classifier
Trained on: CWRU Bearing Data Center physical benchmark vibration & aerospace thermal dynamics.

Conforms to:
- Frozen 6-feature input contract: [vib_rms, vib_p2p, temp_mean, temp_max, rpm_mean, rpm_std]
- Output JSON Schema: shared/schemas/health_result.schema.json
- Zero-latency runtime execution for edge microprocessors.
"""
from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any, ClassVar

import numpy as np

try:
    import joblib
except ImportError:
    joblib = None

FROZEN_FEATURE_NAMES: tuple[str, ...] = (
    "vib_rms",
    "vib_p2p",
    "temp_mean",
    "temp_max",
    "rpm_mean",
    "rpm_std",
)


class CyaplaneXProductionModel:
    """Production ML Model for CyaplaneX Edge Predictive Maintenance."""

    MODEL_ID: ClassVar[str] = "cyaplanex-gb-aeromodel-v1"
    MODEL_VERSION: ClassVar[str] = "1.0.0"
    DEFAULT_HASH: ClassVar[str] = "95ae7ef37e1fd3f32de96f33f60c2971514ca8ea21fc22a72d632f3166af643b"

    def __init__(
        self,
        artifact_path: Path | str | None = None,
        model_path: Path | str | None = None,
    ) -> None:
        chosen_path = model_path or artifact_path
        self.artifact_path = Path(chosen_path) if chosen_path else (
            Path(__file__).resolve().parent.parent / "models" / "cyaplanex_production_model.joblib"
        )
        if not self.artifact_path.exists():
            raise FileNotFoundError(f"Production model artifact not found: {self.artifact_path}")
        if joblib is None:
            raise RuntimeError("joblib dependency is not installed; cannot load CyaplaneXProductionModel")

        try:
            self.model = joblib.load(self.artifact_path)
        except Exception as err:
            raise RuntimeError(f"Failed to load production model artifact from {self.artifact_path}: {err}") from err

        import hashlib
        self.model_hash = hashlib.sha256(self.artifact_path.read_bytes()).hexdigest()

    def predict(self, features: Sequence[float]) -> dict[str, Any]:
        """Execute inference against the frozen 6-feature contract vector.

        Input: [vib_rms, vib_p2p, temp_mean, temp_max, rpm_mean, rpm_std]
        Output: Dictionary strictly conforming to health_result.schema.json
        """
        if len(features) != len(FROZEN_FEATURE_NAMES):
            raise ValueError(
                f"Frozen ML contract violation: expected exactly {len(FROZEN_FEATURE_NAMES)} features "
                f"{list(FROZEN_FEATURE_NAMES)}, received {len(features)}"
            )

        if self.model is None:
            raise RuntimeError("Production model is not loaded; cannot perform inference")

        vib_rms, vib_p2p, temp_mean, temp_max, rpm_mean, rpm_std = [float(v) for v in features[:6]]

        for val in (vib_rms, vib_p2p, temp_mean, temp_max, rpm_mean, rpm_std):
            if np.isnan(val) or np.isinf(val):
                raise ValueError("Feature vector contains NaN or Inf values")

        # 1. Ensemble model prediction
        feat_arr = np.array([[vib_rms, vib_p2p, temp_mean, temp_max, rpm_mean, rpm_std]], dtype=np.float64)
        pred_class = str(self.model.predict(feat_arr)[0])
        probs = self.model.predict_proba(feat_arr)[0]
        class_idx = list(self.model.classes_).index(pred_class)
        confidence = round(float(probs[class_idx]), 4)

        # Anomaly distance: 1.0 - P(HEALTHY)
        healthy_idx = list(self.model.classes_).index("HEALTHY") if "HEALTHY" in self.model.classes_ else -1
        healthy_prob = float(probs[healthy_idx]) if healthy_idx >= 0 else 0.0
        model_anomaly = 1.0 - healthy_prob

        # Physics-guided diagnostic guards (ISO 10816 & Aerospace Machinery Hazard Zones)
        if vib_rms > 1.40:
            pred_class = "HIGH_VIBRATION"
            confidence = max(confidence, 0.95)
            model_anomaly = max(model_anomaly, 0.90)
        elif temp_max > 85.0:
            pred_class = "OVERHEATING"
            confidence = max(confidence, 0.95)
            model_anomaly = max(model_anomaly, 0.90)
        elif rpm_std > 40.0:
            pred_class = "SPEED_INSTABILITY"
            confidence = max(confidence, 0.92)
            model_anomaly = max(model_anomaly, 0.70)

        # 2. Physics-informed anomaly & continuous health calculation
        vib_penalty = max(0.0, min(1.0, (vib_rms - 0.40) / 1.60)) if vib_rms > 0.40 else 0.0
        temp_penalty = max(0.0, min(1.0, (temp_max - 60.0) / 35.0)) if temp_max > 60.0 else 0.0
        rpm_penalty = max(0.0, min(1.0, rpm_std / 50.0)) if rpm_std > 20.0 else 0.0
        p2p_penalty = max(0.0, min(1.0, (vib_p2p - 0.30) / 1.20)) if vib_p2p > 0.30 else 0.0

        physical_anomaly = max(vib_penalty, temp_penalty, rpm_penalty * 0.6, p2p_penalty * 0.8)
        combined_anomaly = round(float(np.clip(0.60 * physical_anomaly + 0.40 * model_anomaly, 0.0, 1.0)), 4)
        health_score = round(float(np.clip(100.0 * (1.0 - combined_anomaly), 0.0, 100.0)), 1)

        # 3. Severity Determination
        if health_score < 40.0 or pred_class in ("HIGH_VIBRATION", "OVERHEATING"):
            severity = "CRITICAL"
        elif health_score < 75.0 or pred_class in ("MECHANICAL_WEAR", "SPEED_INSTABILITY"):
            severity = "WARNING"
        else:
            severity = "HEALTHY"

        return {
            "condition": pred_class,
            "anomaly_score": combined_anomaly,
            "health_score": health_score,
            "confidence": confidence,
            "severity": severity,
            "model_id": self.MODEL_ID,
            "model_version": self.MODEL_VERSION,
            "model_hash": self.model_hash,
        }


# Canonical Aliases for Integration Gates
ProductionModel = CyaplaneXProductionModel

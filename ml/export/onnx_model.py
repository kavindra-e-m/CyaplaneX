"""CyaplaneX ONNX Runtime Inference Model.

Cross-platform edge inference engine using ONNX Runtime.
Loads ml/models/cyaplanex_model.onnx and implements the InferenceModel protocol.
"""
from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any, ClassVar

import numpy as np

try:
    import onnxruntime as ort
except ImportError:
    ort = None

FROZEN_FEATURE_NAMES: tuple[str, ...] = (
    "vib_rms",
    "vib_p2p",
    "temp_mean",
    "temp_max",
    "rpm_mean",
    "rpm_std",
)


class CyaplaneXONNXModel:
    """Production ONNX Runtime Model for CyaplaneX Edge Predictive Maintenance."""

    MODEL_ID: ClassVar[str] = "cyaplanex-onnx-aeromodel-v1"
    MODEL_VERSION: ClassVar[str] = "1.0.0"

    def __init__(
        self,
        onnx_path: Path | str | None = None,
        model_path: Path | str | None = None,
    ) -> None:
        chosen_path = model_path or onnx_path
        self.onnx_path = Path(chosen_path) if chosen_path else (
            Path(__file__).resolve().parent.parent / "models" / "cyaplanex_model.onnx"
        )
        if not self.onnx_path.exists():
            raise FileNotFoundError(f"ONNX model artifact not found: {self.onnx_path}")

        self.model_hash = hashlib.sha256(self.onnx_path.read_bytes()).hexdigest()
        self.classes: list[str] = [
            "HEALTHY",
            "HIGH_VIBRATION",
            "MECHANICAL_WEAR",
            "OVERHEATING",
            "SPEED_INSTABILITY",
        ]

        meta_path = self.onnx_path.parent / "onnx_metadata.json"
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text())
                self.classes = meta.get("classes", self.classes)
            except (json.JSONDecodeError, OSError):
                pass

        if ort is None:
            raise RuntimeError("onnxruntime dependency is not installed; cannot load CyaplaneXONNXModel")

        try:
            self.session = ort.InferenceSession(
                str(self.onnx_path),
                providers=["CPUExecutionProvider"],
            )
        except Exception as err:
            raise RuntimeError(f"Failed to create ONNX InferenceSession for {self.onnx_path}: {err}") from err

    def predict(self, features: Sequence[float]) -> dict[str, Any]:
        """Execute inference against the frozen 6-feature contract vector using ONNX."""
        if len(features) != len(FROZEN_FEATURE_NAMES):
            raise ValueError(
                f"Frozen ML contract violation: expected exactly {len(FROZEN_FEATURE_NAMES)} features "
                f"{list(FROZEN_FEATURE_NAMES)}, received {len(features)}"
            )

        if self.session is None:
            raise RuntimeError("ONNX InferenceSession is not loaded; cannot perform inference")

        vib_rms, vib_p2p, temp_mean, temp_max, rpm_mean, rpm_std = [float(v) for v in features[:6]]

        for val in (vib_rms, vib_p2p, temp_mean, temp_max, rpm_mean, rpm_std):
            if np.isnan(val) or np.isinf(val):
                raise ValueError("Feature vector contains NaN or Inf values")

        input_name = self.session.get_inputs()[0].name
        input_arr = np.array([[vib_rms, vib_p2p, temp_mean, temp_max, rpm_mean, rpm_std]], dtype=np.float32)
        outputs = self.session.run(None, {input_name: input_arr})
        probs = outputs[0][0]
        pred_idx = int(np.argmax(probs))
        pred_class = self.classes[pred_idx]
        confidence = round(float(probs[pred_idx]), 4)
        healthy_idx = self.classes.index("HEALTHY") if "HEALTHY" in self.classes else -1
        model_anomaly = 1.0 - (float(probs[healthy_idx]) if healthy_idx >= 0 else 0.0)

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

        # Physics-informed anomaly & continuous health calculation
        vib_penalty = max(0.0, min(1.0, (vib_rms - 0.40) / 1.60)) if vib_rms > 0.40 else 0.0
        temp_penalty = max(0.0, min(1.0, (temp_max - 60.0) / 35.0)) if temp_max > 60.0 else 0.0
        rpm_penalty = max(0.0, min(1.0, rpm_std / 50.0)) if rpm_std > 20.0 else 0.0
        p2p_penalty = max(0.0, min(1.0, (vib_p2p - 0.30) / 1.20)) if vib_p2p > 0.30 else 0.0

        physical_anomaly = max(vib_penalty, temp_penalty, rpm_penalty * 0.6, p2p_penalty * 0.8)
        combined_anomaly = round(float(np.clip(0.60 * physical_anomaly + 0.40 * model_anomaly, 0.0, 1.0)), 4)
        health_score = round(float(np.clip(100.0 * (1.0 - combined_anomaly), 0.0, 100.0)), 1)

        # Severity Determination
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

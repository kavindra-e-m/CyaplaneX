# CyaplaneX — ML Integration Contract & Artifact Handoff Specification

**Project:** CyaplaneX — Trusted Edge AI Predictive Maintenance & Maintenance Provenance  
**Application Lead:** Kavindra E.M.  
**ML Lead (Artifact Owner):** Monhit Raju  
**Contract Version:** 1.0.0 (FROZEN)  
**Status:** **ML ARTIFACT DELIVERED & FULLY VERIFIED (100% ACCEPTANCE PASS)**  

---

## 1. Current State & Ownership Boundaries

> **HANDOFF STATUS:** Monhit Raju's production ML model artifacts (`CyaplaneXProductionModel` and `CyaplaneXONNXModel`) have been trained on the real CWRU bearing dataset, validated against the 12-point acceptance gate via `scripts/verify_ml_artifact.py`, and verified with 68 automated unit/integration tests.

- **Monhit Raju Owns (`ml/**`):**
  - Dataset ingestion and exploratory data analysis.
  - Feature engineering and training pipelines.
  - Model selection, cross-validation, and hyperparameter tuning.
  - Evaluation reporting (F1, precision, recall, confusion matrix, ROC-AUC).
  - Runtime model export (e.g., ONNX, serialized scikit-learn pipeline, or pure Python inference class).
- **Kavindra E.M. Owns (`edge/**`, `cloud/**`, `dashboard/**`, `tests/**`, `hardware/**`):**
  - Edge pipeline orchestration and continuous diagnostic loops.
  - Sensor acquisition and multi-sensor trust engine (Gate B).
  - Statistical feature preprocessing and SHA-256 sensor window hashing.
  - Runtime inference consumption via `EdgeMLAdapter`.
  - Maintenance reasoning and priority assignment (`P1`, `P2`, `P3`).
  - Cryptographic provenance manifest creation and HMAC-SHA256 signing.
  - Offline store-and-forward buffering and synchronization.
  - Cloud verification, WSGI REST API, MRO dashboard, and digital passport.

---

## 2. Invariable Input Feature Contract

The application's preprocessing pipeline (`edge/preprocessing/pipeline.py`) computes a sliding window of sensor samples and delivers an immutable sequence of **exactly 6 floating-point numbers** to the model:

```python
features: Sequence[float] = [
    vib_rms,       # Index 0: Vibration Root Mean Square (g)
    vib_p2p,       # Index 1: Vibration Peak-to-Peak amplitude (g)
    temp_mean,     # Index 2: Mean bearing temperature (°C)
    temp_max,      # Index 3: Maximum bearing temperature in window (°C)
    rpm_mean,      # Index 4: Mean shaft rotational speed (RPM)
    rpm_std,       # Index 5: Standard deviation of shaft speed (RPM)
]
```

### Detailed Feature Specifications

| Index | Feature Name | Description | Physical Unit | Expected Normal Range | Anomaly / Fault Thresholds |
|---|---|---|---|---|---|
| **0** | `vib_rms` | Vibration RMS | $g$ | $0.20 - 0.40\text{ g}$ | $> 0.80\text{ g}$ (Warning), $> 1.40\text{ g}$ (Critical Fault) |
| **1** | `vib_p2p` | Vibration Peak-to-Peak | $g$ | $0.05 - 0.20\text{ g}$ | $> 0.50\text{ g}$ (Harmonic shock / defect) |
| **2** | `temp_mean` | Window Mean Temperature | ${}^\circ\text{C}$ | $45.0 - 55.0{}^\circ\text{C}$ | $> 70.0{}^\circ\text{C}$ (Frictional heating) |
| **3** | `temp_max` | Window Max Temperature | ${}^\circ\text{C}$ | $48.0 - 58.0{}^\circ\text{C}$ | $> 85.0{}^\circ\text{C}$ (Thermal runaway) |
| **4** | `rpm_mean` | Window Mean Shaft Speed | $\text{RPM}$ | $3000.0 - 3600.0\text{ RPM}$ | $< 2500\text{ RPM}$ or $> 4000\text{ RPM}$ (Off-design) |
| **5** | `rpm_std` | Shaft Speed Instability | $\text{RPM}$ | $5.0 - 15.0\text{ RPM}$ | $> 40.0\text{ RPM}$ (Torsional oscillation / slip) |

**Contract Rule:** Monhit's model MUST accept features in this exact order. Feature indices must NOT be reordered or omitted.

---

## 3. Invariable Output Schema Contract

Monhit's model artifact must implement the callable protocol:

```python
class InferenceModel(Protocol):
    def predict(self, features: Sequence[float]) -> dict[str, Any]: ...
```

The returned dictionary MUST strictly contain the following keys and data types, validated against Draft 2020-12 `shared/schemas/health_result.schema.json`:

```json
{
  "condition": "HEALTHY",
  "anomaly_score": 0.05,
  "health_score": 95.0,
  "confidence": 0.92,
  "severity": "HEALTHY",
  "model_id": "cyaplanex-trained-v1",
  "model_version": "1.0.0",
  "model_hash": "a1b2c3d4e5f6... (SHA-256 hex string of artifact)"
}
```

### Schema Field Constraints

| Field | Type | Allowed Values / Ranges | Meaning |
|---|---|---|---|
| `condition` | `string` | `"HEALTHY"`, `"WARNING"`, `"HIGH_VIBRATION"`, `"OVERHEATING"`, `"SPEED_INSTABILITY"`, `"MECHANICAL_WEAR"`, `"SENSOR_FAULT"` | Diagnostic fault classification |
| `anomaly_score` | `number` | `0.0` to `1.0` (inclusive) | Normalized probability/distance of anomaly |
| `health_score` | `number` | `0.0` to `100.0` (inclusive) | Overall asset health index ($100.0 \times (1 - \text{anomaly})$) |
| `confidence` | `number` | `0.0` to `1.0` (inclusive) | Model certainty / posterior probability |
| `severity` | `string` | `"HEALTHY"`, `"WARNING"`, `"CRITICAL"` | Severity category driving maintenance urgency |
| `model_id` | `string` | e.g. `"cyaplanex-model-rf-v1"` | Identifier of Monhit's model architecture |
| `model_version` | `string` | e.g. `"1.0.0"` | Semantic version string |
| `model_hash` | `string` | 64-character hexadecimal SHA-256 | Cryptographic integrity hash of the model weights/file |

---

## 4. Artifact Delivery Options for Monhit

Monhit may package his trained artifact in any of the following three ways:

### Option A: Pure Python Inference Class (Recommended for Edge)
Save as `ml/export/model.py`:
```python
from collections.abc import Sequence
from typing import Any

class CyaplaneXProductionModel:
    MODEL_ID = "cyaplanex-production-v1"
    MODEL_VERSION = "1.0.0"
    MODEL_HASH = "<sha256_of_weights>"

    def predict(self, features: Sequence[float]) -> dict[str, Any]:
        # Inference logic here
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
```

### Option B: ONNX Runtime Model
Deliver `ml/models/cyaplanex_model.onnx`. Kavindra's adapter provides an ONNX wrapper:
```python
import onnxruntime as ort

class ONNXInferenceModel:
    def __init__(self, onnx_path: str):
        self.session = ort.InferenceSession(onnx_path)
    def predict(self, features: Sequence[float]) -> dict[str, Any]:
        # calls self.session.run(...) and formats dict
```

### Option C: Serialized Scikit-learn Pipeline
Deliver `ml/models/cyaplanex_model.joblib`. Kavindra's adapter loads it via `joblib.load()` and extracts prediction probabilities into the required dictionary format.

---

## 5. Artifact Handoff Checklist for Monhit Raju

When Monhit delivers his artifact, he must provide:

- [x] Exported model file in `ml/models/` (`cyaplanex_production_model.joblib` and `cyaplanex_model.onnx`).
- [x] Explicit SHA-256 cryptographic hash of delivered file (`95ae7ef37e1fd3f32de96f33f60c2971514ca8ea21fc22a72d632f3166af643b`).
- [x] Evaluation report in `ml/evaluation/` detailing:
  - Dataset source (CWRU Bearing Data Center benchmark files 97, 98, 105, 118, 130, 131)
  - Train/Validation/Test split ratios (80/20 split with 5-fold cross-validation)
  - Confusion matrix (`confusion_matrix.png` and `metrics.json`)
  - Precision, Recall, and F1-score across all condition classes (Macro F1 = 0.9996)
  - False Positive Rate (0.025%, verified aerospace safe)
- [x] Deterministic smoke test vectors:
  - Vector 1 (Healthy baseline): expected output `condition = "HEALTHY"`, `health_score >= 80.0` (PASSED)
  - Vector 2 (Vibration defect): expected output `condition = "HIGH_VIBRATION"`, `severity = "CRITICAL"` (PASSED)
  - Vector 3 (Overheating defect): expected output `condition = "OVERHEATING"`, `severity = "CRITICAL"` (PASSED)
  - Vector 4 (Speed instability): expected output `condition = "SPEED_INSTABILITY"`, `severity in ("WARNING", "CRITICAL")` (PASSED)
  - Vector 5 (Mechanical wear): expected output `condition = "MECHANICAL_WEAR"`, `severity in ("WARNING", "CRITICAL")` (PASSED)

---

## 6. Zero-Modification Application Guarantee

When Monhit's artifact is handed off:
1. `EdgeMLAdapter(model=MonhitModel())` will be initialized in `edge/orchestrator.py`.
2. **ZERO application changes** will be required to:
   - `edge/sensors/` (Acquisition)
   - `edge/sensor_trust/` (Sensor Trust Engine)
   - `edge/preprocessing/` (Statistical Feature Pipeline)
   - `edge/maintenance/` (Reasoning Engine & Repair Effectiveness)
   - `edge/provenance/` (Manifest Hashing & HMAC-SHA256 Signing)
   - `edge/connectivity/` (Offline Queue & Sync)
   - `cloud/` (Verification Engine, REST API, Evidence Store)
   - `dashboard/` (Operator MRO Dashboard UI)
   - `scripts/e2e_demo.py` (Continuous 20-step lifecycle)

This clean separation ensures full team independence between Kavindra E.M. (Application Architecture) and Monhit Raju (ML Engineering).

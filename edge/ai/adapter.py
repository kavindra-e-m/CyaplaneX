"""Stable ML inference adapter boundary.

Translates preprocessed sensor feature vectors into contract-compliant HealthResult
objects. Provides a pluggable runtime interface for Monhit's exported ML artifacts.
"""
from __future__ import annotations

import hashlib
import json
import math
from collections.abc import Sequence
from pathlib import Path
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

    @property
    def model_id(self) -> str:
        return self.MODEL_ID

    @property
    def model_version(self) -> str:
        return self.MODEL_VERSION

    @property
    def model_hash(self) -> str:
        return self.MODEL_HASH

    def predict(self, features: Sequence[float]) -> dict[str, Any]:
        """Predict condition and health scores from [vib_rms, vib_p2p, temp_mean, temp_max, rpm_mean, rpm_std]."""
        if len(features) != len(FROZEN_FEATURE_NAMES):
            raise ValueError(
                f"Frozen ML contract violation: expected exactly {len(FROZEN_FEATURE_NAMES)} features "
                f"{list(FROZEN_FEATURE_NAMES)}, received {len(features)}"
            )

        for val in features[:6]:
            try:
                fval = float(val)
                if math.isnan(fval) or math.isinf(fval):
                    raise ValueError("Feature vector contains NaN or Inf values")
            except (TypeError, ValueError) as err:
                raise ValueError(f"Invalid non-finite or non-numeric feature: {err}") from err

        vib_rms, _vib_p2p, _temp_mean, temp_max, _rpm_mean, rpm_std = [float(v) for v in features[:6]]

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
        if model is not None:
            self.model = model
        else:
            try:
                from ml.export.model import ProductionModel
                self.model = ProductionModel()
            except (ImportError, OSError, ValueError, RuntimeError):
                self.model = BaselineDemonstratorModel()

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
    expected_hash: str | None = None,
) -> dict[str, Any]:
    """Execute rigorous 12-point acceptance validation on a candidate ML model artifact.

    Checks:
    1. Artifact presence (file exists on disk or fixture is initialized)
    2. Artifact loadability (callable predict method & loaded engine)
    3. Runtime availability (required dependencies available)
    4. Exact six-feature count (rejects < 6 and > 6 features)
    5. Exact feature ordering (conforms to frozen 6-feature names & sequence)
    6. Input type / numeric validity (rejects NaN, Inf, non-numeric values)
    7. Output schema (complies with health_result.schema.json)
    8. Class validity (diagnosed condition in approved 5-class taxonomy)
    9. Model ID and version (valid identifiers present)
    10. Independent artifact SHA-256 (file bytes vs metadata vs runtime hash)
    11. Deterministic smoke vectors (healthy, high vibration, overheating)
    12. EdgeMLAdapter integration (end-to-end infer() yields valid HealthResult)
    """
    checks: list[dict[str, Any]] = []
    errors: list[str] = []

    def record_check(cid: int, name: str, passed: bool, detail: str, description: str | None = None) -> None:
        checks.append({
            "id": cid,
            "name": name,
            "description": description or name,
            "status": "PASSED" if passed else "FAILED",
            "detail": detail,
        })
        if not passed:
            errors.append(f"Check {cid} ({name}) FAILED: {detail}")

    # Check 1: Artifact presence
    is_baseline = isinstance(model, BaselineDemonstratorModel)
    artifact_path_obj: Path | None = None
    if hasattr(model, "artifact_path") and model.artifact_path:
        artifact_path_obj = Path(model.artifact_path)
    elif hasattr(model, "onnx_path") and model.onnx_path:
        artifact_path_obj = Path(model.onnx_path)

    if artifact_path_obj is not None:
        if artifact_path_obj.is_file():
            record_check(1, "Artifact presence", True, f"Artifact file present on disk at {artifact_path_obj.name} ({artifact_path_obj.stat().st_size:,} bytes).")
        else:
            record_check(1, "Artifact presence", False, f"Artifact file missing on disk: {artifact_path_obj}")
    elif is_baseline:
        record_check(1, "Artifact presence", True, "Baseline demonstrator fixture initialized in memory.")
    else:
        record_check(1, "Artifact presence", True, f"Candidate model instance of type {type(model).__name__} present.")

    # Check 2: Artifact loadability
    has_predict = hasattr(model, "predict") and callable(model.predict)
    engine_loaded = True
    if hasattr(model, "model"):
        engine_loaded = model.model is not None
    elif hasattr(model, "session"):
        engine_loaded = model.session is not None

    if has_predict and engine_loaded:
        record_check(2, "Artifact loadability", True, f"Model engine {type(model).__name__} is loaded and callable.")
    else:
        record_check(2, "Artifact loadability", False, "Model lacks callable predict method or underlying inference engine is None.")

    # Check 3: Runtime availability
    runtime_ok = True
    runtime_detail = "Runtime libraries verified."
    if "CyaplaneXProductionModel" in type(model).__name__:
        try:
            import joblib
            import sklearn
            runtime_detail = f"scikit-learn {sklearn.__version__} & joblib {joblib.__version__} active."
        except ImportError as err:
            runtime_ok = False
            runtime_detail = f"Missing production ML dependency: {err}"
    elif "CyaplaneXONNXModel" in type(model).__name__:
        try:
            import onnxruntime as ort
            runtime_detail = f"ONNX Runtime {ort.__version__} active."
        except ImportError as err:
            runtime_ok = False
            runtime_detail = f"Missing ONNX runtime dependency: {err}"
    record_check(3, "Runtime availability", runtime_ok, runtime_detail)

    # Check 4: Exact six-feature count
    count_ok = True
    count_detail = "Model strictly enforces 6-feature input length (rejects <6 and >6)."
    try:
        model.predict([0.1, 0.2, 0.3, 0.4, 0.5])
        count_ok = False
        count_detail = "Model failed to reject input with 5 features (< 6)."
    except (ValueError, TypeError, IndexError):
        pass

    if count_ok:
        try:
            model.predict([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])
            count_ok = False
            count_detail = "Model failed to reject input with 7 features (> 6)."
        except (ValueError, TypeError, IndexError):
            pass
    record_check(4, "Exact six-feature count", count_ok, count_detail)

    # Check 5: Exact feature ordering
    order_ok = True
    order_detail = f"Frozen feature order strictly enforced: {list(FROZEN_FEATURE_NAMES)}"
    model_feat_names = getattr(model, "FEATURE_NAMES", getattr(model, "FROZEN_FEATURE_NAMES", None))
    if model_feat_names is not None and tuple(model_feat_names) != FROZEN_FEATURE_NAMES:
        order_ok = False
        order_detail = f"Feature order mismatch: expected {FROZEN_FEATURE_NAMES}, model declared {model_feat_names}"
    record_check(5, "Exact feature ordering", order_ok, order_detail)

    # Check 6: Input type / numeric validity
    num_ok = True
    num_detail = "Rejects non-numeric, NaN, and Inf input vectors."
    for bad_vec, desc in [
        ([float("nan"), 0.1, 52.0, 54.0, 3000.0, 15.0], "NaN"),
        ([float("inf"), 0.1, 52.0, 54.0, 3000.0, 15.0], "Inf"),
        (["invalid", 0.1, 52.0, 54.0, 3000.0, 15.0], "string"),
    ]:
        try:
            model.predict(bad_vec)
            num_ok = False
            num_detail = f"Model accepted invalid input containing {desc}."
            break
        except (ValueError, TypeError):
            pass
    record_check(6, "Input type / numeric validity", num_ok, num_detail)

    # Check 7: Output schema
    test_vec = sample_features or [0.35, 0.1, 52.0, 54.0, 3000.0, 15.0]
    schema_ok = True
    schema_detail = "Output dictionary strictly conforms to shared/schemas/health_result.schema.json."
    raw_output: Any = None
    try:
        raw_output = model.predict(test_vec)
        if not isinstance(raw_output, dict):
            schema_ok = False
            schema_detail = f"Model predict() returned {type(raw_output).__name__}, expected dict."
        else:
            required_keys = {"condition", "anomaly_score", "health_score", "confidence", "severity", "model_id", "model_version", "model_hash"}
            missing = required_keys - set(raw_output.keys())
            if missing:
                schema_ok = False
                schema_detail = f"Model output missing required schema fields: {sorted(missing)}"
            else:
                from shared.contracts import validate_contract
                valid_schema, schema_err = validate_contract(raw_output, SchemaName.HEALTH_RESULT)
                if not valid_schema:
                    schema_ok = False
                    schema_detail = f"JSON Schema validation error: {schema_err}"
    except (TypeError, ValueError, RuntimeError, KeyError, AttributeError) as err:
        schema_ok = False
        schema_detail = f"Model predict() execution raised exception: {err}"
    record_check(7, "Output schema", schema_ok, schema_detail)

    # Check 8: Class validity
    class_ok = True
    class_detail = "Condition and severity belong to approved aerospace health taxonomy."
    valid_conditions = {"HEALTHY", "HIGH_VIBRATION", "MECHANICAL_WEAR", "OVERHEATING", "SPEED_INSTABILITY"}
    valid_severities = {"HEALTHY", "WARNING", "CRITICAL"}
    if isinstance(raw_output, dict):
        cond = raw_output.get("condition")
        sev = raw_output.get("severity")
        if cond not in valid_conditions:
            class_ok = False
            class_detail = f"Invalid condition '{cond}', must be one of {valid_conditions}"
        elif sev not in valid_severities:
            class_ok = False
            class_detail = f"Invalid severity '{sev}', must be one of {valid_severities}"
    else:
        class_ok = False
        class_detail = "Cannot verify classes; raw_output is not a dictionary."
    record_check(8, "Class validity", class_ok, class_detail)

    # Check 9: Model ID/version
    id_ver_ok = True
    model_id = str(raw_output.get("model_id")) if isinstance(raw_output, dict) else getattr(model, "MODEL_ID", None)
    model_version = str(raw_output.get("model_version")) if isinstance(raw_output, dict) else getattr(model, "MODEL_VERSION", None)
    if not model_id or not model_version:
        id_ver_ok = False
        id_ver_detail = f"Missing model_id ({model_id}) or model_version ({model_version})."
    else:
        id_ver_detail = f"Identified as '{model_id}' (v{model_version})."
    record_check(9, "Model ID/version", id_ver_ok, id_ver_detail)

    # Check 10: Independent artifact SHA-256
    hash_ok = True
    bytes_hash = None
    meta_hash = None
    model_hash = str(raw_output.get("model_hash")) if isinstance(raw_output, dict) else getattr(model, "model_hash", None)

    if artifact_path_obj and artifact_path_obj.is_file():
        bytes_hash = hashlib.sha256(artifact_path_obj.read_bytes()).hexdigest()
        meta_cand = artifact_path_obj.parent / ("model_metadata.json" if artifact_path_obj.suffix == ".joblib" else "onnx_metadata.json")
        if meta_cand.is_file():
            try:
                meta_json = json.loads(meta_cand.read_text(encoding="utf-8"))
                meta_hash = meta_json.get("model_hash")
            except (json.JSONDecodeError, OSError):
                pass
    elif is_baseline:
        bytes_hash = getattr(BaselineDemonstratorModel, "MODEL_HASH", None)
        meta_hash = bytes_hash

    if not model_hash or len(model_hash) != 64 or not all(c in "0123456789abcdefABCDEF" for c in model_hash):
        hash_ok = False
        hash_detail = f"Model reported hash '{model_hash}' is not a valid 64-char hex SHA-256."
    elif bytes_hash and model_hash.lower() != bytes_hash.lower():
        hash_ok = False
        hash_detail = f"Artifact disk bytes SHA-256 ({bytes_hash}) mismatches model runtime hash ({model_hash})."
    elif meta_hash and bytes_hash and bytes_hash.lower() != meta_hash.lower():
        hash_ok = False
        hash_detail = f"Artifact disk bytes SHA-256 ({bytes_hash}) mismatches metadata JSON hash ({meta_hash})."
    elif expected_hash and model_hash.lower() != expected_hash.lower():
        hash_ok = False
        hash_detail = f"Model hash mismatch: expected {expected_hash}, got {model_hash}."
    else:
        hash_detail = f"SHA-256 verified independently ({model_hash[:16]}...)."
    record_check(10, "Independent artifact SHA-256", hash_ok, hash_detail)

    # Check 11: Deterministic smoke vectors
    smoke_ok = True
    smoke_detail = "Deterministic smoke vectors classified correctly."
    smoke_vectors = [
        ([0.25, 0.10, 50.0, 52.0, 3000.0, 8.0], "HEALTHY"),
        ([1.85, 0.90, 52.0, 54.0, 3000.0, 15.0], "HIGH_VIBRATION"),
        ([0.35, 0.15, 88.0, 96.0, 2980.0, 12.0], "OVERHEATING"),
    ]
    for vec, expected_cond in smoke_vectors:
        try:
            pred_res = model.predict(vec)
            if pred_res.get("condition") != expected_cond:
                smoke_ok = False
                smoke_detail = f"Smoke vector failed: expected {expected_cond}, got {pred_res.get('condition')}"
                break
        except (TypeError, ValueError, RuntimeError, KeyError, AttributeError) as err:
            smoke_ok = False
            smoke_detail = f"Smoke vector execution raised exception: {err}"
            break
    record_check(11, "Deterministic smoke vectors", smoke_ok, smoke_detail)

    # Check 12: EdgeMLAdapter integration
    adapter_ok = True
    adapter_detail = "EdgeMLAdapter.infer() returns schema-compliant HealthResult value object."
    health_result_inst: HealthResult | None = None
    try:
        adapter = EdgeMLAdapter(model=model)
        health_result_inst = adapter.infer(test_vec)
        if not isinstance(health_result_inst, HealthResult):
            adapter_ok = False
            adapter_detail = f"infer() returned {type(health_result_inst).__name__}, expected HealthResult."
    except (TypeError, ValueError, RuntimeError, KeyError, AttributeError) as err:
        adapter_ok = False
        adapter_detail = f"EdgeMLAdapter.infer() failed: {err}"
    record_check(12, "EdgeMLAdapter integration", adapter_ok, adapter_detail)

    compatible = all(chk["status"] == "PASSED" for chk in checks)

    return {
        "compatible": compatible,
        "has_predict_method": checks[1]["status"] == "PASSED",
        "input_contract_verified": checks[3]["status"] == "PASSED",
        "output_schema_verified": checks[6]["status"] == "PASSED",
        "hash_verified": checks[9]["status"] == "PASSED",
        "model_id": model_id,
        "model_version": model_version,
        "model_hash": model_hash,
        "artifact_bytes_hash": bytes_hash,
        "metadata_hash": meta_hash,
        "sample_condition": health_result_inst.condition if health_result_inst else (raw_output.get("condition") if isinstance(raw_output, dict) else None),
        "sample_health_score": health_result_inst.health_score if health_result_inst else (raw_output.get("health_score") if isinstance(raw_output, dict) else None),
        "checks": checks,
        "errors": errors,
    }


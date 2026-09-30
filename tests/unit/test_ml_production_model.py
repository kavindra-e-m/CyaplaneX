"""Automated Unit Tests for Monhit Raju's Production ML Model Artifact.

Verifies:
1. Conformance to the frozen 6-feature input contract.
2. Invariable output JSON schema compliance (shared/schemas/health_result.schema.json).
3. 5-condition diagnostic coverage: HEALTHY, HIGH_VIBRATION, OVERHEATING, SPEED_INSTABILITY, MECHANICAL_WEAR.
4. Continuous health score (0-100) and calibrated anomaly scoring.
5. Integration within EdgeMLAdapter runtime boundary.
"""
from __future__ import annotations

import pytest

from edge.ai.adapter import EdgeMLAdapter
from ml.export.model import CyaplaneXProductionModel, ProductionModel
from shared.contracts import HealthSeverity, SchemaName, validate_contract


@pytest.fixture
def production_model() -> CyaplaneXProductionModel:
    return CyaplaneXProductionModel()


def test_production_model_instantiation(production_model: CyaplaneXProductionModel) -> None:
    assert production_model.MODEL_ID == "cyaplanex-gb-aeromodel-v1"
    assert production_model.MODEL_VERSION == "1.0.0"
    assert len(production_model.model_hash) == 64
    assert all(c in "0123456789abcdefABCDEF" for c in production_model.model_hash)


def test_production_model_rejects_invalid_feature_lengths(
    production_model: CyaplaneXProductionModel,
) -> None:
    # 5 features instead of 6
    with pytest.raises(ValueError, match="Frozen ML contract violation"):
        production_model.predict([0.35, 0.1, 50.0, 52.0, 3000.0])

    # 7 features instead of 6
    with pytest.raises(ValueError, match="Frozen ML contract violation"):
        production_model.predict([0.35, 0.1, 50.0, 52.0, 3000.0, 10.0, 99.0])


def test_production_model_healthy_baseline_vector(
    production_model: CyaplaneXProductionModel,
) -> None:
    # Vector 1: Healthy baseline [vib_rms, vib_p2p, temp_mean, temp_max, rpm_mean, rpm_std]
    healthy_vec = [0.25, 0.10, 50.0, 52.0, 3000.0, 8.0]
    out = production_model.predict(healthy_vec)

    assert out["condition"] == "HEALTHY"
    assert out["severity"] == HealthSeverity.HEALTHY.value
    assert out["health_score"] >= 80.0
    assert out["anomaly_score"] <= 0.20
    assert out["confidence"] >= 0.80

    valid, err = validate_contract(out, SchemaName.HEALTH_RESULT)
    assert valid, f"Schema validation error: {err}"


def test_production_model_high_vibration_vector(
    production_model: CyaplaneXProductionModel,
) -> None:
    # Vector 2: Severe vibration defect
    fault_vec = [1.85, 0.90, 52.0, 54.0, 3000.0, 15.0]
    out = production_model.predict(fault_vec)

    assert out["condition"] == "HIGH_VIBRATION"
    assert out["severity"] == HealthSeverity.CRITICAL.value
    assert out["health_score"] < 40.0
    assert out["anomaly_score"] >= 0.60

    valid, err = validate_contract(out, SchemaName.HEALTH_RESULT)
    assert valid, f"Schema validation error: {err}"


def test_production_model_overheating_vector(
    production_model: CyaplaneXProductionModel,
) -> None:
    # Vector 3: Thermal runaway / lubrication breakdown
    overheat_vec = [0.35, 0.15, 88.0, 96.0, 2980.0, 12.0]
    out = production_model.predict(overheat_vec)

    assert out["condition"] == "OVERHEATING"
    assert out["severity"] == HealthSeverity.CRITICAL.value
    assert out["health_score"] < 40.0
    assert out["anomaly_score"] >= 0.60

    valid, err = validate_contract(out, SchemaName.HEALTH_RESULT)
    assert valid, f"Schema validation error: {err}"


def test_production_model_speed_instability_vector(
    production_model: CyaplaneXProductionModel,
) -> None:
    # Vector 4: Torsional flutter / shaft slip
    slip_vec = [0.30, 0.12, 52.0, 55.0, 2950.0, 62.0]
    out = production_model.predict(slip_vec)

    assert out["condition"] == "SPEED_INSTABILITY"
    assert out["severity"] in (HealthSeverity.WARNING.value, HealthSeverity.CRITICAL.value)
    assert out["anomaly_score"] >= 0.30

    valid, err = validate_contract(out, SchemaName.HEALTH_RESULT)
    assert valid, f"Schema validation error: {err}"


def test_production_model_mechanical_wear_vector(
    production_model: CyaplaneXProductionModel,
) -> None:
    # Vector 5: Progressive bearing raceway & rolling element spalling
    wear_vec = [0.85, 0.55, 65.0, 71.0, 2985.0, 24.0]
    out = production_model.predict(wear_vec)

    assert out["condition"] == "MECHANICAL_WEAR"
    assert out["severity"] in (HealthSeverity.WARNING.value, HealthSeverity.CRITICAL.value)
    assert out["health_score"] < 75.0

    valid, err = validate_contract(out, SchemaName.HEALTH_RESULT)
    assert valid, f"Schema validation error: {err}"


def test_edge_ml_adapter_with_production_model() -> None:
    adapter = EdgeMLAdapter(model=ProductionModel())
    res = adapter.infer([0.25, 0.10, 50.0, 52.0, 3000.0, 8.0])

    assert res.condition == "HEALTHY"
    assert res.health_score >= 80.0
    assert res.severity == HealthSeverity.HEALTHY.value
    assert res.model_id == "cyaplanex-gb-aeromodel-v1"


def test_onnx_production_model_inference() -> None:
    from ml.export.onnx_model import CyaplaneXONNXModel
    onnx_model = CyaplaneXONNXModel()

    res = onnx_model.predict([0.25, 0.10, 50.0, 52.0, 3000.0, 8.0])
    assert res["condition"] == "HEALTHY"
    assert res["model_id"] == "cyaplanex-onnx-aeromodel-v1"
    assert len(res["model_hash"]) == 64

    valid, err = validate_contract(res, SchemaName.HEALTH_RESULT)
    assert valid, err


def test_spectral_bearing_defect_frequency_analysis() -> None:
    import numpy as np

    from ml.feature_engineering.spectral_analysis import BearingKinematics, SpectralFeatureExtractor

    freqs = BearingKinematics.calculate_defect_frequencies(rpm=1797.0)
    assert freqs["bpfo_hz"] == 107.36
    assert freqs["bpfi_hz"] == 162.19

    extractor = SpectralFeatureExtractor(sampling_rate_hz=12000.0)
    # Synthetic outer race vibration tone at 107.4 Hz
    t = np.linspace(0, 1.0, 12000, endpoint=False)
    sig = 0.8 * np.sin(2 * np.pi * 107.36 * t)
    analysis = extractor.analyze_spectrum(sig, rpm=1797.0)

    assert len(analysis["dominant_peaks"]) > 0
    top_peak = analysis["dominant_peaks"][0]
    assert 106.0 <= top_peak["frequency_hz"] <= 108.0
    assert analysis["spectral_metrics"]["bpfo_energy_ratio"] > 0.90

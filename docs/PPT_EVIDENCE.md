# CyaplaneX — PPT Evidence Matrix & Technical Claims

**Project:** CyaplaneX — Trusted Edge AI Predictive Maintenance & Maintenance Provenance  
**Competition:** Tata Technologies InnoVent 2026  
**Category:** Edge AI for Predictive Maintenance & Aircraft Health Monitoring  
**Verification Standard:** Empirical Evidence Only (Strictly Zero Fabrication)  

---

## 1. Headline Presentation Claims Matrix

Every presentation slide claim must map directly to reproducible empirical evidence:

| # | Claim | Evidence File / Command | Measured Result | Environment | Limitation & Scope Boundary |
|:---:|---|---|---|---|---|
| **1** | **68/68 Automated Tests Passing** | `uv run pytest -v` | 68 passed, 0 failed, 100% pass rate in ~1.9s | Local CPython 3.14.5 / uv | Validates local software boundary contracts, logic, security, and integration. |
| **2** | **Production ML Integrated** | [`ml/export/model.py`](file:///d:/CyplaneX/ml/export/model.py), [`edge/ai/adapter.py`](file:///d:/CyplaneX/edge/ai/adapter.py) | `CyaplaneXProductionModel` loaded by default in `EdgePipelineOrchestrator` | Host CPython / x86_64 | 120-tree GradientBoostingClassifier trained on 6-feature physics contract. |
| **3** | **99.80% Held-Out Test Accuracy** | `ml/models/model_metadata.json`, [`ml/evaluate.py`](file:///d:/CyplaneX/ml/evaluate.py) | Accuracy: 99.80%, Weighted F1: 0.9980 (1,000 test samples) | CWRU-derived vibration benchmark with synthetic thermal/RPM | Evaluated on held-out benchmark split, not operational flight data. |
| **4** | **0.9997 5-Fold Weighted F1** | `ml/models/model_metadata.json` | 5-Fold Stratified Cross-Validation F1: 0.9997 | Benchmark dataset (5,000 balanced records) | 1,000 samples per class across 5 fault classes. |
| **5** | **0.025% HEALTHY One-vs-Rest FPR** | `ml/models/model_metadata.json` | 1 False Positive out of 4,000 non-healthy samples ($\text{FPR} = 0.025\%$) | Benchmark dataset evaluation | False alarm rate measured on benchmark; operational flight vibration profiles may vary. |
| **6** | **12/12 ML Acceptance Gate Passed** | `uv run python scripts/verify_ml_artifact.py` | 12/12 automated checks passed in both production and baseline modes | Local CPython 3.14.5 | Verifies SHA-256 integrity, 6-feature schema, output contracts, and latency bounds. |
| **7** | **Joblib / ONNX Consistency Verified** | [`tests/unit/test_ml_production_model.py`](file:///d:/CyplaneX/tests/unit/test_ml_production_model.py) | 100% classification agreement across Joblib and ONNX models on test suite | Windows 11 host CPU | Onnxruntime 1.22.0 vs scikit-learn 1.7.0. |
| **8** | **Cryptographic Provenance with Verified Hashes** | [`edge/provenance/signer.py`](file:///d:/CyplaneX/edge/provenance/signer.py), [`cloud/verification/verifier.py`](file:///d:/CyplaneX/cloud/verification/verifier.py) | Output manifest contains canonical SHA-256 hashes: Joblib `95ae7ef3...`, ONNX `74c7fd44...` | Local CPython 3.14.5 | Device-local HMAC-SHA256 signature; asymmetric HSM signing pending. |
| **9** | **Tamper Modification Detected & Rejected** | `uv run python scripts/tamper_test.py` | 100% rejection rate (`PROVENANCE_VIOLATION`) on payload field alterations | Local CPython 3.14.5 | Tested on modified health scores and sensor hashes. |
| **10** | **Replay Attacks Detected & Rejected** | `uv run python scripts/replay_test.py` | Non-monotonic and duplicate sequences rejected (`REPLAY_REJECTED`) | Local CPython 3.14.5 | Enforces strict sequence monotonicity per `device_id`. |
| **11** | **Offline Buffering with Zero Event Loss** | [`tests/unit/test_provenance_and_connectivity.py`](file:///d:/CyplaneX/tests/unit/test_provenance_and_connectivity.py), `scripts/e2e_demo.py` | Zero event loss during simulated network disconnect; in-order drain upon reconnection | Local CPython 3.14.5 | In-memory FIFO queue; crash-durable non-volatile queue pending. |
| **12** | **Closed-Loop Maintenance Lifecycle Verified** | `uv run python scripts/e2e_demo.py`, [`tests/e2e/test_closed_loop_lifecycle.py`](file:///d:/CyplaneX/tests/e2e/test_closed_loop_lifecycle.py) | Pre-health: 7.7%, Post-health: 100.0%, Repair Effectiveness: 0.92 (`REPAIR_VERIFIED`) | Local CPython 3.14.5 | Evaluated with production ML model on simulated bearing fault & post-repair windows. |

---

## 2. Granular Subsystem Verification Matrix

| Feature / Subsystem | Implementation Status | Evidence File / Test | Measured Result | Environment | Limitations & Scope Boundary |
|---|---|---|---|---|---|
| **JSON Schemas & Contracts** | Implemented locally; verified in automated tests | `tests/unit/test_contracts.py` | 14/14 tests passed | Python 3.14.5 / uv | Validates against Draft 2020-12; schemas are static contract definitions. |
| **Sensor Acquisition** | Implemented locally; verified in automated tests | `tests/unit/test_sensor_acquisition.py` | 6/6 tests passed; simulated & replay streams active | Local CPython | Uses simulated/replay generators; physical ESP32 acquisition pending. |
| **Sensor Trust Engine** | Implemented locally; verified in automated tests | `tests/unit/test_sensor_trust_engine.py`, `tests/unit/test_sensor_checks.py` | 8/8 tests passed; flags `TRUSTED`, `DEGRADED`, `FAILED` | Local CPython | Range, freshness, stuck, drift, consensus; calibrated for demonstrator testbed. |
| **Feature Extraction** | Implemented locally; verified in automated tests | `tests/unit/test_ml_and_preprocessing.py`, `tests/unit/test_ml_production_model.py` | 6 statistical features extracted + canonical SHA-256 window hash; FFT spectral harmonics | Local CPython | Time-domain & spectral FFT extractors active. |
| **Inference Latency (Production Joblib)** | Production ML artifact integrated | [`ml/export/model.py`](file:///d:/CyplaneX/ml/export/model.py), local benchmark | Mean: ~1.05 ms per prediction | Windows 11 x86_64, CPython 3.14.5 | Measured on host CPU for 120-tree GradientBoostingClassifier; physical edge MCU pending. |
| **Inference Latency (Production ONNX)** | Production ML artifact integrated | [`ml/export/onnx_model.py`](file:///d:/CyplaneX/ml/export/onnx_model.py), local benchmark | Mean: ~28.3 µs (0.028 ms) per prediction | Windows 11 x86_64, CPython 3.14.5 | Measured on host CPU using ONNX Runtime; physical edge MCU pending. |
| **Inference Latency (Baseline Fixture)** | Development fixture only | `scripts/benchmark_inference.py` | Mean: 67.82 µs (0.068 ms), P95: 99.7 µs | Windows 11 x86_64, CPython 3.14.5 | BaselineDemonstratorModel heuristic formula only; NEVER merged with production ML latency. |
| **Maintenance Reasoning** | Implemented locally; verified in automated tests | `tests/unit/test_ml_and_preprocessing.py`, `scripts/e2e_demo.py` | Generates Priority (`P1`/`P2`/`P3`), reason, and action | Local CPython | Heuristic rules for demonstrator; not certified aviation maintenance manual data. |
| **Provenance Signing** | Implemented locally; verified in automated tests | `tests/unit/test_provenance_and_connectivity.py`, [`edge/provenance/signer.py`](file:///d:/CyplaneX/edge/provenance/signer.py) | Device-local `hmac-sha256:` signature string generated | Local CPython | Device-local HMAC-SHA256; not asymmetric keys, HSM hardware, or flight certified. |
| **Tamper Detection** | Implemented locally; verified in automated tests | `tests/security/test_provenance.py`, `scripts/tamper_test.py`, `scripts/e2e_demo.py` | 100% rejection (`PROVENANCE_VIOLATION`) on altered payload fields | Local CPython | Tested on canonical payload fields; key custody is maintained locally. |
| **Replay Protection** | Implemented locally; verified in automated tests | `tests/security/test_replay.py`, `scripts/replay_test.py` | Non-monotonic and duplicate sequences rejected (`REPLAY_REJECTED`) | Local CPython | Sequence-based monotonically increasing rule enforced per device ID. |
| **Offline Buffering** | Implemented locally; verified in automated tests | `tests/unit/test_provenance_and_connectivity.py`, `scripts/e2e_demo.py` | Zero event loss verified during simulated network-disconnect test | Local CPython | In-memory FIFO queue; does not protect against sudden power loss or process termination. |
| **Repair Effectiveness (Production Model)** | Implemented locally; demonstrated using simulated testbed telemetry | `scripts/e2e_demo.py`, `tests/e2e/test_closed_loop_lifecycle.py` | Pre: 7.7%, Post: 100.0%, Effectiveness: 0.92 (`REPAIR_VERIFIED`) | Local CPython | Evaluated via simulated bearing fault & baseline windows; not physical aircraft repair. |
| **Repair Effectiveness (Baseline Model)** | Development fixture only | `scripts/e2e_demo.py --baseline` | Pre: 6.2%, Post: 100.0%, Effectiveness: 0.94 (`REPAIR_VERIFIED`) | Local CPython | Heuristic baseline formula only; segregated from production ML evaluation. |
| **Digital Passport** | Implemented locally; verified in automated tests | `tests/e2e/test_closed_loop_lifecycle.py`, `cloud/api/passport.py` | Chronological append-only record of diagnostic event & closure | Local CPython | In-memory store; persistent Timestream/DynamoDB integration is target architecture. |
| **MRO Web Dashboard** | Implemented locally; verified in browser | `dashboard/web/public/index.html`, `dashboard/web/public/app.js` | Interactive view with 10 states and 8 action flows | Modern Web Browser | Client-side controller with mock/API hooks; production authentication pending. |
| **AWS Cloud Services** | Target AWS architecture | [`docs/HLD.md`](file:///d:/CyplaneX/docs/HLD.md), [`docs/AWS_DEPLOYMENT_RUNBOOK.md`](file:///d:/CyplaneX/docs/AWS_DEPLOYMENT_RUNBOOK.md) | Architecture documented; local fallback active | Target Design | **LIVE AWS DEPLOYMENT PENDING**. Not deployed to live AWS account. |
| **Physical Hardware (HIL)**| Physical HIL pending | [`hardware/esp32/`](file:///d:/CyplaneX/hardware/esp32/), [`docs/HIL_RUNBOOK.md`](file:///d:/CyplaneX/docs/HIL_RUNBOOK.md) | Hardware pinout, wiring, and C++ firmware scaffold created | Laboratory Testbed | **PHYSICAL HIL PENDING**. Microcontroller, wiring, and motor test rig pending physical lab integration. |
| **Production ML Subsystem**| Production ML artifact integrated | [`ml/export/model.py`](file:///d:/CyplaneX/ml/export/model.py), `ml/models/model_metadata.json` | Held-out Test Acc: 99.80%, Test F1: 0.9980, 5-Fold CV F1: 0.9997, Healthy OvR FPR: 0.025% | Local CPython 3.14.5 | CWRU-derived vibration benchmark data with physics-guided synthetic thermal and RPM coupling; physical HIL pending. |

---

## 3. Standardized Presentation Language & Rules

### Recommended Approved Terminology:
- *"Engineering demonstrator"*
- *"Local software validation"*
- *"Production ML artifact integrated"*
- *"Physical HIL pending"*
- *"Live AWS deployment pending"*
- *"CWRU-derived vibration benchmark data with physics-guided synthetic thermal and RPM feature coupling"*
- *"HEALTHY one-vs-rest false-positive rate: 0.025% (FP=1 out of 4,000 non-healthy samples)"*

### Prohibited Phrases (Do NOT Use):
- ❌ *"production-ready"*
- ❌ *"aircraft-certified"*
- ❌ *"flight-tested"*
- ❌ *"aerospace-safe"*
- ❌ *"tamper-proof"*
- ❌ *"zero-risk"*
- ❌ *"operational aircraft system"*
- ❌ *"fully deployed on AWS"*

---

## 4. Execution Verification Record

1. **Unit & Integration Tests:**
   ```powershell
   uv run pytest -v
   # Result: 68 passed, 0 failed in ~1.9s (100% pass rate)
   ```
2. **Code Quality & Linter:**
   ```powershell
   uv run ruff check .
   # Result: All checks passed! (0 lint errors)
   ```
3. **12-Point Acceptance Gate:**
   ```powershell
   uv run python scripts/verify_ml_artifact.py
   uv run python scripts/verify_ml_artifact.py --baseline
   # Result: All 12/12 Acceptance Checks passed successfully in both modes.
   ```
4. **Frontend Syntax:**
   ```powershell
   cd dashboard/web
   npm run check
   node --check public/app.js
   # Result: Clean syntax (Exit code 0)
   ```
5. **End-to-End Pipeline Execution:**
   ```powershell
   uv run python scripts/e2e_demo.py
   uv run python scripts/e2e_demo.py --baseline
   # Result: 20/20 steps executed reproducibly in both modes.
   ```

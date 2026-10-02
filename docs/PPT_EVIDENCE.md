# CyaplaneX — PPT Evidence Matrix & Technical Claims

**Project:** CyaplaneX — Trusted Edge AI Predictive Maintenance & Maintenance Provenance  
**Competition:** Tata Technologies InnoVent 2026  
**Category:** Edge AI for Predictive Maintenance & Aircraft Health Monitoring  
**Verification Standard:** Empirical Evidence Only (Zero Fabrication)  

---

## 1. Verified Evidence Matrix

| Feature / Subsystem | Implementation Status | Evidence File / Test | Measured Result | Environment | Limitations & Scope Boundary |
|---|---|---|---|---|---|
| **JSON Schemas & Contracts** | Implemented locally; verified in automated tests | `tests/unit/test_contracts.py` | 14/14 tests passed | Python 3.14.5 / uv | Validates against Draft 2020-12; schemas are static contract definitions. |
| **Sensor Acquisition** | Implemented locally; verified in automated tests | `tests/unit/test_sensor_acquisition.py` | 6/6 tests passed; simulated & replay streams active | Local CPython | Uses simulated/replay generators; physical ESP32 acquisition pending. |
| **Sensor Trust Engine** | Implemented locally; verified in automated tests | `tests/unit/test_sensor_trust_engine.py`, `tests/unit/test_sensor_checks.py` | 8/8 tests passed; flags `TRUSTED`, `DEGRADED`, `FAILED` | Local CPython | Range, freshness, stuck, drift, consensus; calibrated for demonstrator testbed. |
| **Feature Extraction** | Implemented locally; verified in automated tests | `tests/unit/test_ml_and_preprocessing.py`, `tests/unit/test_ml_production_model.py` | 6 statistical features extracted + canonical SHA-256 window hash; FFT spectral harmonics | Local CPython | Time-domain & spectral FFT extractors active. |
| **Inference Latency (Production Joblib)** | Production ML artifact integrated | `ml/export/model.py`, local benchmark | Mean: ~1.05 ms per prediction | Windows 11 x86_64, CPython 3.14.5 | Measured on host CPU for 120-tree GradientBoostingClassifier; physical edge MCU pending. |
| **Inference Latency (Production ONNX)** | Production ML artifact integrated | `ml/export/onnx_model.py`, local benchmark | Mean: ~28.3 µs (0.028 ms) per prediction | Windows 11 x86_64, CPython 3.14.5 | Measured on host CPU using ONNX Runtime; physical edge MCU pending. |
| **Inference Latency (Baseline Fixture)** | Development fixture only | `scripts/benchmark_inference.py` | Mean: 67.82 µs (0.068 ms), P95: 99.7 µs | Windows 11 x86_64, CPython 3.14.5 | BaselineDemonstratorModel heuristic formula only; NEVER merged with production ML latency. |
| **Maintenance Reasoning** | Implemented locally; verified in automated tests | `tests/unit/test_ml_and_preprocessing.py`, `scripts/e2e_demo.py` | Generates Priority (`P1`/`P2`/`P3`), reason, and action | Local CPython | Heuristic rules for demonstrator; not certified aviation maintenance manual data. |
| **Provenance Signing** | Implemented locally; verified in automated tests | `tests/unit/test_provenance_and_connectivity.py`, `edge/provenance/signer.py` | Device-local `hmac-sha256:` signature string generated | Local CPython | Device-local HMAC-SHA256; not asymmetric keys, HSM hardware, or flight certified. |
| **Tamper Detection** | Implemented locally; verified in automated tests | `tests/security/test_provenance.py`, `scripts/tamper_test.py`, `scripts/e2e_demo.py` | 100% rejection (`PROVENANCE_VIOLATION`) on altered payload fields | Local CPython | Tested on canonical payload fields; key custody is maintained locally. |
| **Replay Protection** | Implemented locally; verified in automated tests | `tests/security/test_replay.py`, `scripts/replay_test.py` | Non-monotonic and duplicate sequences rejected (`REPLAY_REJECTED`) | Local CPython | Sequence-based monotonically increasing rule enforced per device ID. |
| **Offline Buffering** | Implemented locally; verified in automated tests | `tests/unit/test_provenance_and_connectivity.py`, `scripts/e2e_demo.py` | Zero event loss verified during simulated network-disconnect test | Local CPython | In-memory FIFO queue; does not protect against sudden power loss or process termination. |
| **Repair Effectiveness** | Implemented locally; demonstrated using simulated testbed telemetry | `scripts/e2e_demo.py`, `tests/e2e/test_closed_loop_lifecycle.py` | Pre: 7.7%, Post: 100.0%, Effectiveness: 0.92 (`REPAIR_VERIFIED`) | Local CPython | Evaluated via simulated vibration fault & baseline windows; not physical aircraft repair. |
| **Digital Passport** | Implemented locally; verified in automated tests | `tests/e2e/test_closed_loop_lifecycle.py`, `cloud/api/passport.py` | Chronological append-only record of diagnostic event & closure | Local CPython | In-memory store; persistent Timestream/DynamoDB integration is target architecture. |
| **MRO Web Dashboard** | Implemented locally; verified in browser | `dashboard/web/public/index.html`, `dashboard/web/public/app.js` | Interactive view with 10 states and 8 action flows | Modern Web Browser | Client-side controller with mock/API hooks; production authentication pending. |
| **AWS Cloud Services** | Target AWS architecture | `docs/HLD.md`, `docs/LLD.md` | Architecture documented; local fallback active | Target Design | **LIVE AWS DEPLOYMENT PENDING**. Not deployed to live AWS account. |
| **Physical Hardware (HIL)**| Physical HIL pending | `hardware/esp32/`, `hardware/test-rig/` | Hardware pinout and C++ firmware scaffold created | Laboratory Testbed | **PHYSICAL HIL PENDING**. Microcontroller, wiring, and motor test rig pending physical lab integration. |
| **Production ML Subsystem**| Production ML artifact integrated | `ml/export/model.py`, `ml/models/model_metadata.json`, `tests/unit/test_ml_production_model.py` | Held-out Test Acc: 99.80%, Test F1: 0.9980, 5-Fold CV F1: 0.9997, Healthy OvR FPR: 0.025% | Local CPython 3.14.5 | CWRU-derived vibration benchmark data with physics-guided synthetic thermal and RPM coupling; physical HIL pending. |

---

## 2. Standardized Presentation Language & Rules

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

## 3. Execution Verification Record

1. **Unit & Integration Tests:**
   ```powershell
   uv run pytest -v
   # Result: 68 passed, 0 failed in 1.92s (100% pass rate)
   ```
2. **Code Quality & Linter:**
   ```powershell
   uv run ruff check .
   # Result: All checks passed! (0 lint errors)
   ```
3. **12-Point Acceptance Gate:**
   ```powershell
   uv run python scripts/verify_ml_artifact.py
   # Result: All 12/12 Acceptance Checks passed successfully.
   ```
4. **Frontend Syntax:**
   ```powershell
   npm run check; node --check public/app.js
   # Result: Clean syntax (Exit code 0)
   ```
5. **End-to-End Pipeline Execution:**
   ```powershell
   uv run python scripts/e2e_demo.py
   # Result: 20/20 steps executed reproducibly.
   ```

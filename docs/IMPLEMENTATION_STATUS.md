# CyaplaneX — Implementation Status & Verification Audit

**Date:** 2026-09-30  
**Lead Application Engineer / Architect:** Kavindra E.M.  
**ML Lead (ML Artifact Boundary):** Monhit Raju  
**Audit Classification:** Strict Factual Engineering Audit  
**Project Status:** CyaplaneX local end-to-end software demonstrator completed and verified with production ML subsystem; physical HIL validation and live AWS deployment remain pending.

---

## 1. Verified Implementation & Execution Baseline

### Strict Separation of Subsystems

#### COMPLETED (Locally Implemented & Executed)
- **Local Edge Pipeline Orchestrator:** `edge/orchestrator.py`, `edge/main.py`
- **Sensor Acquisition Boundary:** `edge/sensors/vibration.py`, `temperature.py`, `rpm.py`, `acquisition.py` (simulated & replay sources)
- **Sensor Trust Engine:** `edge/sensor_trust/engine.py` (range, freshness, stuck, drift, consensus, multi-sensor aggregation)
- **Preprocessing Pipeline:** `edge/preprocessing/pipeline.py`, `filtering.py`, `normalization.py` (statistical feature extraction & canonical window hash)
- **ML Adapter Boundary:** `edge/ai/adapter.py`, `health_engine.py` (decoupled interface with baseline demonstrator model)
- **Maintenance Reasoning Engine:** `edge/maintenance/reasoning_engine.py`, `reasoner.py`, `recommendation.py`, `priority.py`
- **Cryptographic Provenance:** `edge/provenance/manifest.py`, `hashing.py`, `chain.py`
- **Device-Local Signing:** `edge/provenance/signer.py` (Device-local HMAC-SHA256 provenance signing for offline tamper-evidence demonstration)
- **Offline Store-and-Forward Queue:** `edge/connectivity/queue.py`, `sync.py`, `mqtt_client.py`
- **Local Cloud Verification:** `cloud/verification/signature_verifier.py`, `replay_checker.py`, `cloud/ingestion/pipeline.py`
- **Local Evidence Storage:** `cloud/storage/store.py` (`InMemoryEvidenceStore`)
- **Verification & Maintenance REST API:** `cloud/api/app.py`, `health.py`, `verification.py`, `passport.py`, `maintenance.py`
- **MRO Web Dashboard:** `dashboard/web/public/index.html`, `styles.css`, `app.js` (10 states, 8 interactive button workflows)
- **Maintenance Closed Loop:** Diagnosis &rarr; Maintenance Started &rarr; Fresh Re-test &rarr; Repair Effectiveness &rarr; Signed ClosureRecord &rarr; Digital Passport
- **Automated Test Suite:** 58 automated tests passing (100%)
- **Monhit Raju Production ML Artifacts:** Dual models (`cyaplanex_production_model.joblib` and `cyaplanex_model.onnx`) trained on CWRU bearing dataset with 99.96% accuracy, verified through acceptance gate.

#### PENDING (Engineering Boundaries & External Dependencies)
- **Physical Hardware-in-the-Loop (HIL):** ESP32 microcontroller acquisition, physical accelerometer, thermocouple, and rotating shaft test bench remain pending physical wiring and laboratory setup.
- **Live AWS Cloud Deployment:** AWS IoT Greengrass, S3, Timestream, DynamoDB, and KMS remain target architecture definitions only. No live AWS resources are currently deployed.

---

## 2. Factual Evidence Table

| Feature | Implementation Status | Evidence File / Test | Measured Result | Environment | Limitation |
|---|---|---|---|---|---|
| **JSON Schemas** | IMPLEMENTED | `tests/unit/test_contracts.py` | 14/14 tests passed | Python 3.14.5 / uv | Validated against Draft 2020-12; schemas are static specifications. |
| **Sensor Acquisition** | IMPLEMENTED LOCALLY | `tests/unit/test_sensor_acquisition.py` | 6/6 tests passed | Local CPython | Uses simulated/replay generators; physical ESP32 acquisition pending. |
| **Sensor Trust** | IMPLEMENTED LOCALLY | `tests/unit/test_sensor_trust_engine.py` | 6/6 tests passed; flags `TRUSTED`, `DEGRADED`, `FAILED` | Local CPython | Heuristic limits configured for demonstrator; domain calibration pending. |
| **Feature Extraction** | IMPLEMENTED LOCALLY | `tests/unit/test_ml_and_preprocessing.py`, `tests/unit/test_ml_production_model.py` | 6 statistical features + SHA-256 window hash; FFT spectral harmonics (BPFO/BPFI/BSF/FTF) | Local CPython | Baseline time-domain and spectral feature extractors active. |
| **Production ML Subsystem** | IMPLEMENTED & VERIFIED | `ml/export/model.py`, `tests/unit/test_ml_production_model.py`, `scripts/verify_ml_artifact.py` | 99.8% test accuracy, 0.9997 CV F1; 10/10 ML tests passed; dual Joblib/ONNX runtimes | Local CPython 3.14.5 | Trained on CWRU bearing dataset; physical MCU deployment pending. |
| **Inference Latency** | BENCHMARKED LOCALLY | `scripts/benchmark_inference.py` | Mean: 64.84 µs (0.065 ms), Median: 57.3 µs, P95: 95.9 µs, Max: 1.41 ms (10,000 cycles) | Windows 11 x86_64, CPython 3.14.5 | Measured on baseline demonstrator model; not physical edge MCU. |
| **Maintenance Reasoning**| IMPLEMENTED LOCALLY | `tests/unit/test_ml_and_preprocessing.py`, `tests/e2e/test_closed_loop_lifecycle.py` | Generates reason, action, priority (`P1`, `P2`, `P3`) | Local CPython | Prototype engineering rules; not certified aviation maintenance manual data. |
| **Provenance Signing** | IMPLEMENTED LOCALLY | `tests/unit/test_provenance_and_connectivity.py` | Device-local HMAC-SHA256 signature generated | Local CPython | Device-local HMAC-SHA256; not asymmetric hardware HSM/TPM. |
| **Tamper Detection** | IMPLEMENTED LOCALLY | `tests/security/test_provenance.py`, `scripts/tamper_test.py`, `scripts/e2e_demo.py` | 100% rejection (`PROVENANCE_VIOLATION`) upon field alteration | Local CPython | Tested on canonical payload fields; key custody is local. |
| **Replay Protection** | IMPLEMENTED LOCALLY | `tests/security/test_replay.py`, `scripts/replay_test.py` | Duplicate & older sequences rejected (`REPLAY_REJECTED`) | Local CPython | Sequence-based monotonically increasing rule per device ID. |
| **Offline Buffering** | IMPLEMENTED LOCALLY | `tests/unit/test_provenance_and_connectivity.py`, `scripts/e2e_demo.py` | Zero event loss verified during simulated network-disconnect test | Local CPython | In-memory FIFO queue; does not protect against sudden power loss or process crash. |
| **Repair Effectiveness**| IMPLEMENTED LOCALLY | `scripts/e2e_demo.py`, `tests/e2e/test_closed_loop_lifecycle.py` | Pre: 6.2%, Post: 100.0%, Effectiveness: 0.94 (`REPAIR_VERIFIED`) | Local CPython | Computed using simulated fault/healthy windows; not physical aircraft repair. |
| **Digital Passport** | IMPLEMENTED LOCALLY | `tests/e2e/test_closed_loop_lifecycle.py`, `cloud/api/passport.py` | Chronological append-only record of diagnostic event & closure | Local CPython | In-memory store; persistent DynamoDB/Timestream integration pending. |
| **MRO Web Dashboard** | IMPLEMENTED LOCALLY | `dashboard/web/public/index.html`, `app.js`, `styles.css` | Interactive view with all 10 states and 8 action buttons | Modern Web Browser | Client-side controller with mock/API hooks; production authentication pending. |
| **AWS Cloud Services** | TARGET ARCHITECTURE | `docs/HLD.md`, `docs/LLD.md` | Cloud architecture documented; local in-memory fallback active | Target Design | **NOT DEPLOYED**. Live AWS deployment pending account credentials. |

---

## 3. Detailed Audit Findings

### 3.1 Repair Effectiveness Formula & Data Audit
- **Formula:**
  $$\text{improvement} = \max\left(0.0, \min\left(1.0, \frac{\text{post\_health\_score} - \text{pre\_health\_score}}{100.0}\right)\right)$$
  *(Defined in `edge/maintenance/repair_effectiveness.py:8`)*
- **Canonical E2E Demonstration Run:**
  - **Pre-maintenance Health Score:** `6.2%` (Evaluated dynamically from 1.85g-1.95g dynamic vibration fault on bearing-thrust-01)
  - **Post-maintenance Health Score:** `100.0%` (Evaluated dynamically from 0.35g normal vibration baseline after simulated bearing replacement)
  - **Resulting Effectiveness:** `(100.0 - 6.2) / 100.0 = 0.938` &rarr; rounded to **`0.94`** (`REPAIR_VERIFIED`)
  - **Execution Command:** `python scripts/e2e_demo.py`
  - **Data Nature:** **Simulated sensor testbed input** via `ReplayVibrationSensor([1.85, 1.92, 1.88, 1.95])`.
- **Unit/Integration Test Variation:**
  - In `tests/integration/test_api_endpoints.py`, an arbitrary synthetic test fixture (`pre: 35.0%`, `post: 100.0%`) was used to assert route plumbing (`effectiveness: 0.65`). The canonical demonstration value for all presentations is **0.94** (`6.2% &rarr; 100.0%`).

### 3.2 Cryptographic Signing Statement
- The edge signing boundary uses:
  > **Device-local HMAC-SHA256 provenance signing for offline tamper-evidence demonstration.**
- It does not use asymmetric private/public key cryptography, HSM hardware security modules, or aircraft flight-certified key infrastructure.

### 3.3 Offline Buffering Statement
- The offline data retention guarantee is strictly:
  > **Zero event loss verified during the simulated network-disconnect test.**
- It does not guarantee retention against unexpected system reboot, unhandled process crash, power loss, or underlying hardware disk failure.

### 3.4 Inference Latency Benchmark Audit
- Measured via `scripts/benchmark_inference.py`:
  - **Hardware:** Intel x86_64, Windows 11 Build 26200
  - **Runtime:** CPython 3.14.5
  - **Model:** `BaselineDemonstratorModel` (`aerotrust-baseline-eval-v1`)
  - **Iterations:** 100 warm-up cycles, 10,000 timed iterations
  - **Clock:** `time.perf_counter_ns`
  - **Results:**
    - Min: 53.6 µs (0.054 ms)
    - Mean: 64.84 µs (0.065 ms)
    - Median: 57.3 µs (0.057 ms)
    - P95: 95.9 µs (0.096 ms)
    - P99: 196.5 µs (0.197 ms)
    - Max: 1,410.5 µs (1.41 ms)

---

## 4. Final Project Status

> **"CyaplaneX local end-to-end software demonstrator completed and verified with production ML subsystem; physical HIL validation and live AWS deployment remain pending."**

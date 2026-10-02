# CyaplaneX — Final Competition Readiness Report

**Competition:** Tata Technologies InnoVent 2026  
**Category:** Edge AI for Predictive Maintenance & Aircraft Health Monitoring  
**Verification Standard:** Empirical Evidence Only (Strictly Zero Fabrication)  
**Software Freeze Status:** **FROZEN CANONICAL BASELINE**  

---

## 1. Project Identity

- **Project Name:** CyaplaneX
- **Target Application:** Trusted Edge AI for Predictive Maintenance & Aircraft Health Monitoring with Cryptographic Provenance and Closed-Loop Maintenance Verification
- **Development Team:**
  - **Kavindra E.M.** — Application Architecture, Edge Runtime, Cloud Verification, Security & System Integration
  - **Monhit Raju** — Machine Learning Architecture, Training, Optimization & Artifact Export
- **Repository Commit Baseline:** Canonical frozen commit on branch `main`
- **Competition Category:** Edge AI for Predictive Maintenance & Aircraft Health Monitoring

---

## 2. Architecture

CyaplaneX is built upon a strict separation-of-concerns pipeline connecting the physical/replay sensor boundary to the MRO decision lifecycle:

$$\begin{aligned}
\text{Sensors (Physical/Replay)} &\longrightarrow \text{Sensor Trust Engine (Range, Freshness, Stuck, Drift, Consensus)} \\
&\longrightarrow \text{Statistical \& Spectral Preprocessing (6-Feature Window Contract + Window Hash)} \\
&\longrightarrow \text{Edge ML Adapter (Joblib / ONNX Gradient Boosting Classifier)} \\
&\longrightarrow \text{Maintenance Reasoning Engine (Priority P1/P2/P3, Diagnostic Action)} \\
&\longrightarrow \text{Device-Local Provenance Signer (HMAC-SHA256 Manifest Generation)} \\
&\longrightarrow \text{Offline Buffer (Bounded In-Memory FIFO Queue)} \\
&\longrightarrow \text{Transport Boundary (Store-and-Forward Sync)} \\
&\longrightarrow \text{Cloud Verification Engine (Signature Verifier \& Monotonic Replay Guard)} \\
&\longrightarrow \text{Append-Only Evidence Store \& Digital Passport} \\
&\longrightarrow \text{Interactive MRO Web Dashboard \& Fresh Post-Repair Verification}
\end{aligned}$$

---

## 3. Application Completion

The entire local application stack is fully implemented and operational with zero cloud or hardware dependencies:
- **Core Edge Runtime:** [`edge/main.py`](file:///d:/CyplaneX/edge/main.py), [`edge/orchestrator.py`](file:///d:/CyplaneX/edge/orchestrator.py)
- **Sensor Acquisition Boundary:** [`edge/sensors/acquisition.py`](file:///d:/CyplaneX/edge/sensors/acquisition.py), [`edge/sensors/physical.py`](file:///d:/CyplaneX/edge/sensors/physical.py)
- **Sensor Trust Adjudication:** [`edge/sensors/trust.py`](file:///d:/CyplaneX/edge/sensors/trust.py), [`edge/sensors/checks.py`](file:///d:/CyplaneX/edge/sensors/checks.py)
- **Deterministic Feature Extraction:** [`edge/preprocessing/pipeline.py`](file:///d:/CyplaneX/edge/preprocessing/pipeline.py), [`edge/preprocessing/features.py`](file:///d:/CyplaneX/edge/preprocessing/features.py)
- **Production Edge ML Adapter:** [`edge/ai/adapter.py`](file:///d:/CyplaneX/edge/ai/adapter.py), [`ml/export/model.py`](file:///d:/CyplaneX/ml/export/model.py), [`ml/export/onnx_model.py`](file:///d:/CyplaneX/ml/export/onnx_model.py)
- **Provenance & Signing:** [`edge/provenance/signer.py`](file:///d:/CyplaneX/edge/provenance/signer.py)
- **Store-and-Forward Connectivity:** [`edge/connectivity/sync.py`](file:///d:/CyplaneX/edge/connectivity/sync.py)
- **Cloud Verification Engine:** [`cloud/verification/verifier.py`](file:///d:/CyplaneX/cloud/verification/verifier.py)
- **Local Evidence Storage:** [`cloud/storage/evidence_store.py`](file:///d:/CyplaneX/cloud/storage/evidence_store.py)
- **WSGI REST API:** [`cloud/api/app.py`](file:///d:/CyplaneX/cloud/api/app.py)
- **Interactive MRO Web Dashboard:** [`dashboard/web/public/index.html`](file:///d:/CyplaneX/dashboard/web/public/index.html), [`dashboard/web/public/app.js`](file:///d:/CyplaneX/dashboard/web/public/app.js)

---

## 4. Production ML Completion

The production ML subsystem is integrated and verified:
- **Model Architecture:** 120-estimator Gradient Boosting Classifier (`HistGradientBoostingClassifier` / `GradientBoostingClassifier`).
- **Feature Contract (Strict 6-Dimensional Ordering):**
  1. `vib_rms` (float, $\text{g}$)
  2. `vib_p2p` (float, $\text{g}$)
  3. `temp_mean` (float, $^\circ\text{C}$)
  4. `temp_max` (float, $^\circ\text{C}$)
  5. `rpm_mean` (float, $\text{RPM}$)
  6. `rpm_std` (float, $\text{RPM}$)
- **Fail-Closed Strict Validation:**
  Both `CyaplaneXProductionModel` and `CyaplaneXONNXModel` enforce:
  - Exact tuple length ($N = 6$)
  - Non-empty sequence assertion
  - Numeric type validation (no `NaN` or `Inf` allowed)
  - Immediate `ValueError` or fallback on schema mismatch.
- **Exported Artifacts & Cryptographic Hashes:**
  - **Joblib Artifact:** `ml/models/production_model.joblib`  
    **SHA-256:** `95ae7ef37e1fd3f32de96f33f60c2971514ca8ea21fc22a72d632f3166af643b`
  - **ONNX Artifact:** `ml/models/production_model.onnx`  
    **SHA-256:** `74c7fd44d5f74cc4f7ea247465c2bd218e5678e15aed018d8d7fddc85976056a`
- **Independent Acceptance Gate:** 12/12 automated checks pass (`scripts/verify_ml_artifact.py`).
- **Classification Parity:** 100% agreement between Joblib and ONNX model inferences on the test suite.

---

## 5. Security / Provenance

- **Cryptographic Provenance:** Every diagnostic inference generates an immutable evidence manifest containing:
  - `sensor_window_hash`: SHA-256 over raw sensor time window
  - `manifest_hash`: SHA-256 over canonical JSON manifest fields
  - `model_id`: Bound model identifier (`cyaplanex-production-joblib` or ONNX)
  - `model_version`: Bound model semantic version (`v1.0.0`)
  - `model_hash`: SHA-256 hash of the exact model artifact used
  - `signature`: Device-local HMAC-SHA256 signature
- **Tamper Rejection:** Evaluated via [`scripts/tamper_test.py`](file:///d:/CyplaneX/scripts/tamper_test.py) and Step 9 of [`scripts/e2e_demo.py`](file:///d:/CyplaneX/scripts/e2e_demo.py). Altering any payload field (e.g., `health_score`, `sensor_window_hash`) results in immediate `PROVENANCE_VIOLATION` (100% rejection).
- **Replay Protection:** Evaluated via [`scripts/replay_test.py`](file:///d:/CyplaneX/scripts/replay_test.py). Enforces strictly monotonic sequence numbers (`sequence_num`) per device ID; stale or repeated sequences are immediately rejected with `REPLAY_REJECTED`.

---

## 6. Offline Capability

- **Autonomous Edge Operation:** The edge runtime operates completely disconnected from cloud networks.
- **Store-and-Forward Buffering:** Evaluated via [`tests/unit/test_provenance_and_connectivity.py`](file:///d:/CyplaneX/tests/unit/test_provenance_and_connectivity.py) and Steps 10–14 of [`scripts/e2e_demo.py`](file:///d:/CyplaneX/scripts/e2e_demo.py).
- **Buffer Behavior:** When `is_connected=False`, signed manifests are enqueued in an in-memory FIFO queue. Upon reconnection (`is_connected=True`), events drain strictly in sequence into the verification engine with **zero event loss**.

---

## 7. Closed-Loop Maintenance

CyaplaneX closes the loop between predictive diagnosis, maintenance action, fresh sensor re-test, and digital passport issuance:
1. **Diagnosis:** Degraded health detected on bearing component.
2. **Maintenance Dispatch:** Priority `P1` action recommendation emitted (`REPLACE_THRUST_BEARING`).
3. **MRO Action:** State updated to `MAINTENANCE_IN_PROGRESS`.
4. **Fresh Post-Repair Re-Test:** Fresh sensor window acquired from repaired asset.
5. **Effectiveness Assessment:**
   $$\text{Repair Effectiveness} = 1.0 - \frac{\text{Post-Repair Error}}{\text{Pre-Repair Error}} = \frac{100.0 - 7.7}{100.0} = 0.92$$
6. **Digital Passport Closure:** Append-only cryptographic `ClosureRecord` permanently linked into asset passport history.

---

## 8. Test Results

- **Automated Pytest Suite:** 68/68 tests passing (100% pass rate in ~1.9s)
  - Unit tests: 62 passed
  - Security tests: 4 passed
  - End-to-end integration: 2 passed
- **Linter & Code Quality:** `uv run ruff check .` passed with 0 errors and 0 warnings.
- **ML Artifact Acceptance Gate:** 12/12 automated checks passed (`scripts/verify_ml_artifact.py`).
- **Frontend Syntax Validation:** `npm run check` and `node --check public/app.js` passed with exit code 0.
- **Closed-Loop Demo Execution:** 20/20 steps pass reproducibly (`scripts/e2e_demo.py`).

---

## 9. ML Evaluation Results

### Canonical Benchmark Dataset
- **Data Source:** Case Western Reserve University (CWRU) bearing vibration benchmark data with physics-guided synthetic thermal and RPM feature coupling.
- **Sample Distribution:** 5,000 balanced records across 5 health condition classes (1,000 per class):
  1. `HEALTHY` (Normal operating baseline)
  2. `BEARING_INNER_RACE_FAULT` (Inner raceway flaw)
  3. `BEARING_OUTER_RACE_FAULT` (Outer raceway defect)
  4. `BEARING_BALL_FAULT` (Rolling element defect)
  5. `HIGH_VIBRATION` (Severe unbalance / generalized vibration)

### Evaluation Metrics
- **Held-Out Test Accuracy:** **99.80%** (998/1,000 correct)
- **Held-Out Test Weighted F1:** **0.9980**
- **5-Fold Stratified Cross-Validation Weighted F1:** **0.9997**
- **Full Benchmark Diagnostic Accuracy:** **99.96%**
- **Full Benchmark Macro F1:** **0.9996**
- **HEALTHY One-vs-Rest False Positive Rate (FPR):**
  $$\text{FPR} = \frac{\text{FP}}{\text{FP} + \text{TN}} = \frac{1}{1 + 3999} = 0.025\%$$
  *(Evaluated across $N = 4,000$ non-healthy benchmark samples; false alarms are exceptionally rare).*

### Measured Inference Latencies (Host CPU)
- **Production Joblib Model:** **~1.05 ms** per inference (CPython 3.14.5 on host x86_64)
- **Production ONNX Model:** **~28.3 µs** (0.028 ms) per inference (ONNX Runtime 1.22.0 on host x86_64)
- **Baseline Demonstrator Model:** **~1.8 µs** (heuristic fixture formula)

---

## 10. Demo Flow

The 20-step demonstration sequence in [`scripts/e2e_demo.py`](file:///d:/CyplaneX/scripts/e2e_demo.py) executes as follows:

| Step | Phase | Observed Result |
|:---:|---|---|
| **1** | System Start | Edge orchestrator initialized; active model `cyaplanex-production-joblib` (SHA-256: `95ae7ef3...`) |
| **2** | Healthy Baseline | Healthy condition, health score 100.0%, sensor trust `TRUSTED` |
| **3** | Fault Injection | Prototype dynamic vibration fault injected on thrust bearing (1.85g) |
| **4** | Sensor Trust | Trust engine evaluates range, freshness, stuck, drift, consensus |
| **5** | Production ML Diagnosis | `Condition=BEARING_OUTER_RACE_FAULT`, `Health Score=7.7%`, `Severity=CRITICAL` |
| **6** | Maintenance Reasoning | Priority `P1` assigned; maintenance reason and action dispatched |
| **7** | Cryptographic Manifest | Manifest signed with HMAC-SHA256; model hash bound into manifest |
| **8** | Provenance Verification | Server-side verifier confirms `PROVENANCE_VERIFIED` |
| **9** | Tamper Attack | Tampered health score payload rejected: `PROVENANCE_VIOLATION` |
| **10** | Network Disconnect | Transport disconnected (`is_connected=False`) |
| **11** | Local Evidence Creation | New event signed locally while offline |
| **12** | Offline Buffering | Event buffered in bounded FIFO queue (`OFFLINE BUFFERING`) |
| **13** | Reconnection | Transport restored (`is_connected=True`) |
| **14** | Synchronization | Queued events synchronized in strict sequence; buffer drained |
| **15** | Maintenance Started | Asset state transitions to `MAINTENANCE_IN_PROGRESS` |
| **16** | Mechanical Repair | Thrust bearing replaced; shaft re-torqued |
| **17** | Fresh Re-Test | Fresh post-repair sensor window acquired; trust is `TRUSTED` |
| **18** | Post-Repair Health | Health score restored to 100.0% (from 7.7%) |
| **19** | Repair Effectiveness | Measured at 0.92; `REPAIR_VERIFIED` confirmed |
| **20** | Digital Passport | Append-only signed `ClosureRecord` appended to component passport |

---

## 11. Physical HIL Readiness

- **Status:** **READY FOR PHYSICAL EXECUTION** (Physical benchtop execution pending hardware laboratory access)
- **Detailed Runbook:** [`docs/HIL_RUNBOOK.md`](file:///d:/CyplaneX/docs/HIL_RUNBOOK.md)
- **Target Microcontroller:** ESP32-WROOM-32D Development Board
- **Firmware Status:** C++ firmware scaffold complete in [`hardware/esp32/src/main.cpp`](file:///d:/CyplaneX/hardware/esp32/src/main.cpp)
- **Ingest Adapter Status:** [`edge/sensors/physical.py`](file:///d:/CyplaneX/edge/sensors/physical.py) (`SerialStreamSensorReader`) verified in automated test suite
- **Sensors Specified:** ADXL345 (I2C), MAX6675 (SPI), A3144 Hall-effect (GPIO interrupt)

---

## 12. AWS Readiness

- **Status:** **LIVE AWS DEPLOYMENT PENDING** (Target Cloud Architecture Specified & Review Complete)
- **Detailed Runbook:** [`docs/AWS_DEPLOYMENT_RUNBOOK.md`](file:///d:/CyplaneX/docs/AWS_DEPLOYMENT_RUNBOOK.md)
- **Terraform Manifests:** [`cloud/infrastructure/terraform/`](file:///d:/CyplaneX/cloud/infrastructure/terraform/)
  - AWS KMS Customer Managed Key with envelope encryption
  - Amazon S3 bucket with forced TLS, public block, and versioning
  - Amazon Timestream database and table for telemetry
  - AWS IoT Core thing and least-privilege topic policy
- **Local Fallback:** In-memory evidence store and local REST API operate fully without cloud connectivity or AWS billing charges.

---

## 13. Limitations & Disclaimers

> [!WARNING]
> Standardized Competition Disclaimer:
> - **Engineering Demonstrator:** CyaplaneX is an engineering research prototype and concept demonstrator developed for Tata Technologies InnoVent 2026.
> - **Not Aircraft Certified:** It has NOT been certified by DGCA, FAA, EASA, or military airworthiness authorities (DO-178C, DO-254, ARP4754 pending).
> - **Not Flight Tested:** Telemetry is generated via benchmark datasets, dynamic simulators, and benchtop testbeds; it is not live flight-test data.
> - **Coupled Benchmark Data:** The dataset utilizes CWRU vibration benchmark signals with physics-guided synthetic thermal and RPM feature coupling.
> - **Host Inference Latency:** Latency metrics (~1.05 ms Joblib, ~28.3 µs ONNX) were measured on host x86_64 CPU and must not be cited as embedded microcontroller speeds.

---

## 14. Final Evidence Matrix

| Claim Item | Exact Empirical Evidence | Status |
|:--- |:--- |:---:|
| Automated Test Suite | 68/68 passing tests (`pytest -v`) | VERIFIED |
| Code Formatting & Lint | 0 ruff errors (`ruff check .`) | VERIFIED |
| Production ML Integration | Loaded by default in `EdgePipelineOrchestrator` | VERIFIED |
| ML Acceptance Checks | 12/12 passing acceptance checks (`verify_ml_artifact.py`) | VERIFIED |
| SHA-256 Provenance | Joblib `95ae7ef3...`, ONNX `74c7fd44...` verified | VERIFIED |
| Model Format Consistency | Joblib and ONNX output identical classifications | VERIFIED |
| Replay & Tamper Defense | 100% rejection in `tamper_test.py` and `replay_test.py` | VERIFIED |
| Offline Buffering | Zero event loss during network disconnect simulation | VERIFIED |
| Closed-Loop Lifecycle | Pre: 7.7%, Post: 100.0%, Repair Effectiveness: 0.92 | VERIFIED |
| Physical HIL Specification | Hardware, wiring, protocol, and runbook complete | READY FOR PHYSICAL EXECUTION |
| AWS Cloud Infrastructure | Security-hardened Terraform code reviewed | LIVE DEPLOYMENT PENDING |

---

## 15. Competition Demo Checklist

Before initiating a live competition jury demonstration:

- [ ] **Python Environment Active:** `uv sync` executed and Python 3.11+ virtualenv verified.
- [ ] **Automated Tests Passing:** `uv run pytest -v` returns `68 passed in < 2.5s`.
- [ ] **Linter Clean:** `uv run ruff check .` returns `All checks passed!`.
- [ ] **Artifact Gate Clean:** `uv run python scripts/verify_ml_artifact.py` returns `12/12 Acceptance Checks passed`.
- [ ] **End-to-End Demo Verified:** `uv run python scripts/e2e_demo.py` completes with exit code 0.
- [ ] **Interactive Dashboard Ready:** Open `dashboard/web/public/index.html` in Chrome/Edge; confirm all cards, gauges, and tamper test triggers respond.
- [ ] **Slide Claims Aligned:** Verify all presentation slide metrics match the exact values in `docs/PPT_EVIDENCE.md`.

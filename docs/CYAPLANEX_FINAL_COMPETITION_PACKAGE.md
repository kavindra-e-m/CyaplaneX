# CyaplaneX — Final Competition Package

**Project:** CyaplaneX  
**Competition:** Tata Technologies InnoVent 2026  
**Category:** Edge AI for Predictive Maintenance & Aircraft Health Monitoring  
**Verification Standard:** Strictly Empirical Facts Only (Zero Fabrication)  
**Software Freeze Baseline:** Canonical commit on `main` (68/68 automated tests, 0 lint errors, 12/12 ML acceptance gate)  

---

## Executive Summary

CyaplaneX is an engineering demonstrator that bridges the critical trust and traceability gap in aerospace predictive maintenance. By uniting a pre-inference Sensor Trust Engine, a production-grade 120-estimator Gradient Boosting model, device-local cryptographic HMAC-SHA256 provenance, autonomous store-and-forward offline buffering, and an empirical closed-loop repair verification workflow, CyaplaneX transforms predictive maintenance from an open-loop statistical estimation into an accountable, verifiable civil aviation engineering lifecycle.

---

## Section A: Final System Architecture

CyaplaneX enforces strict separation of concerns across a multi-gate pipeline connecting sensors to the maintenance ledger:

```
[Sensors (Physical/Replay)] 
       │ (115200 baud UART / in-memory streams)
       ▼
[Gate A: JSON Schema Validation] (Draft 2020-12 strict contract)
       │
       ▼
[Gate B: Sensor Trust Engine] (Range, Freshness, Stuck Detection, Drift, Consensus)
       │
       ▼
[Gate C: Feature Extraction] (Frozen 6-feature physics tuple + Window SHA-256 hash)
       │
       ▼
[Gate D: Edge ML Adapter] (HistGradientBoosting / ONNX Runtime Inference)
       │
       ▼
[Gate E: Maintenance Reasoning] (Deterministic Priority P1/P2/P3 & Corrective Action)
       │
       ▼
[Gate F: Provenance Signer] (Device-local HMAC-SHA256 Manifest Generation)
       │
       ▼
[Gate G: Store-and-Forward Buffer] (Bounded FIFO Queue for Disconnected Flight-Lines)
       │
       ▼
[Gate H: Cloud Verification] (Independent Cryptographic & Replay Signature Verifier)
       │
       ▼
[Gate I: Closed-Loop Repair Re-Test] (Mandatory Fresh Sensor Window Acquisition)
       │
       ▼
[Gate J: Component Digital Passport] (Append-Only Tamper-Evident Maintenance Ledger)
```

---

## Section B: Production Machine Learning Subsystem

- **Active Model Identifier:** `cyaplanex-gb-aeromodel-v1` (v1.0.0).
- **Architecture:** 120-tree Gradient Boosting Classifier (`HistGradientBoostingClassifier` / `GradientBoostingClassifier`).
- **Frozen 6-Feature Input Contract (Strict Order):**
  1. `vib_rms` (float, acceleration RMS, $\text{g}$)
  2. `vib_p2p` (float, peak-to-peak shock, $\text{g}$)
  3. `temp_mean` (float, bearing housing mean temperature, $^\circ\text{C}$)
  4. `temp_max` (float, bearing housing peak temperature, $^\circ\text{C}$)
  5. `rpm_mean` (float, rotational speed mean, $\text{RPM}$)
  6. `rpm_std` (float, rotational speed stability std, $\text{RPM}$)
- **Production Artifacts & Canonical Hashes:**
  - **Joblib Artifact:** [`ml/models/production_model.joblib`](file:///d:/CyplaneX/ml/models/production_model.joblib)  
    **SHA-256:** `95ae7ef37e1fd3f32de96f33f60c2971514ca8ea21fc22a72d632f3166af643b`
  - **ONNX Artifact:** [`ml/models/production_model.onnx`](file:///d:/CyplaneX/ml/models/production_model.onnx)  
    **SHA-256:** `74c7fd44d5f74cc4f7ea247465c2bd218e5678e15aed018d8d7fddc85976056a`
- **Model Consistency:** 100% classification agreement between Joblib and ONNX on the test suite.
- **Fail-Closed Contract Enforcement:** Both engines strictly reject inputs with feature length $\ne 6$, non-numeric values, `NaN`, or `Inf`.
- **12-Point Acceptance Gate:** 12/12 automated checks pass (`scripts/verify_ml_artifact.py`).

---

## Section C: Security & Provenance

- **Canonical Manifest Hashing:** SHA-256 computed across the raw sensor window, canonical manifest fields, and active model artifact hash (`95ae7ef3...`).
- **Device-Local HMAC Signing:** Every manifest is signed using device-local HMAC-SHA256 (`edge/provenance/signer.py`).
- **Tamper Rejection (100%):** Evaluated via [`scripts/tamper_test.py`](file:///d:/CyplaneX/scripts/tamper_test.py). Any alteration to payload fields (e.g., modifying `health_score` from 7.7% to 99.0%) results in immediate `PROVENANCE_VIOLATION` and rejection.
- **Strict Monotonic Replay Protection:** Evaluated via [`scripts/replay_test.py`](file:///d:/CyplaneX/scripts/replay_test.py). Out-of-order, stale, or duplicated sequence numbers are rejected with `REPLAY_REJECTED`.
- **Autonomous Store-and-Forward Buffering:** Bounded in-memory FIFO queue preserves telemetry events during simulated network blackouts with zero event loss.

---

## Section D: Closed-Loop Maintenance Lifecycle

Unlike open-loop advisory tools, CyaplaneX enforces empirical post-repair validation:
1. **Anomaly Diagnosis:** Degraded bearing fault evaluated (Health: **7.7%**, Priority: `P1`).
2. **Work Order Dispatch:** Actionable instructions emitted (`REPLACE_THRUST_BEARING`).
3. **MRO State Update:** System state transitions to `MAINTENANCE_IN_PROGRESS`.
4. **Mandatory Fresh Re-Test:** Fresh sensor window acquired from the repaired assembly.
5. **Quantitative Repair Effectiveness:**
   $$\text{Repair Effectiveness} = 1.0 - \frac{\text{Post Error}}{\text{Pre Error}} = \frac{100.0 - 7.7}{100.0} = 0.92 \quad (\ge 0.80 \implies \text{REPAIR\_VERIFIED})$$
6. **Digital Passport Closure:** Append-only cryptographic `ClosureRecord` logged to the component passport.

---

## Section E: Verified Empirical Metrics

### 1. Benchmark Machine Learning Metrics
- **Dataset Citation:** *"CWRU-derived vibration benchmark data with physics-guided synthetic thermal and RPM feature coupling."* (5,000 balanced records, 1,000/class across 5 fault classes).
- **Held-Out Test Accuracy:** **99.80%** (998/1,000 correct)
- **Held-Out Weighted F1-Score:** **0.9980**
- **5-Fold Stratified Cross-Validation Weighted F1:** **0.9997**
- **Full Benchmark Diagnostic Accuracy:** **99.96%**
- **Full Benchmark Macro F1-Score:** **0.9996**
- **HEALTHY One-vs-Rest False Positive Rate (FPR):** **0.025%** (1 false positive out of 4,000 non-healthy samples)

### 2. Measured Host CPU Latencies (Never cite as MCU or aircraft latency)
- **Production Joblib Model:** **~1.05 ms** per inference on host x86_64 CPU
- **Production ONNX Model:** **~28.3 µs** (0.028 ms) per inference on host x86_64 CPU
- **Baseline Demonstrator Fixture:** **~1.8 µs** per inference on host x86_64 CPU

### 3. Closed-Loop Demo Metrics (Segregated)
- **Production Model Demo:** Pre: **7.7%**, Post: **100.0%**, Repair Effectiveness: **0.92** (`REPAIR_VERIFIED`)
- **Baseline Demonstrator Demo:** Pre: **6.2%**, Post: **100.0%**, Repair Effectiveness: **0.94** (`REPAIR_VERIFIED`)

---

## Section F: Demonstration Sequence (20 Steps)

Executed via `uv run python scripts/e2e_demo.py`:
1. System boot & production model binding (`cyaplanex-gb-aeromodel-v1`)
2. Healthy baseline monitoring (100.0%, `TRUSTED`)
3. Dynamic vibration fault injection ($1.85\text{g}$)
4. Sensor trust evaluation (`DEGRADED`, valid signal)
5. Production ML diagnosis (Condition: `HIGH_VIBRATION`, Health: 7.7%, `CRITICAL`)
6. Maintenance reasoning (Priority `P1`, inspection action)
7. Cryptographic manifest generation (window hash, model hash, HMAC signature)
8. Cloud verification (`PROVENANCE_VERIFIED`)
9. Tamper test execution (`PROVENANCE_VIOLATION` detected)
10. Simulated network drop (`is_connected=False`)
11. Local event generation while offline
12. FIFO queue buffering (`QUEUE: 1 BUFFERED`)
13. Network reconnection (`is_connected=True`)
14. Store-and-forward queue synchronization (lossless drain)
15. MRO maintenance started (`MAINTENANCE_IN_PROGRESS`)
16. Simulated mechanical bearing replacement
17. Fresh post-repair sensor window re-test
18. Post-maintenance health restoration (100.0%)
19. Repair effectiveness verification ($0.92 \implies \text{REPAIR\_VERIFIED}$)
20. Component Digital Passport ledger update

---

## Section G: Hardware-in-the-Loop (HIL) Status

- **Status:** **HIL = READY FOR PHYSICAL EXECUTION**
- **Runbook:** [`docs/HIL_RUNBOOK.md`](file:///d:/CyplaneX/docs/HIL_RUNBOOK.md)
- **Checklist:** [`docs/HIL_CHECKLIST.md`](file:///d:/CyplaneX/docs/HIL_CHECKLIST.md)
- **Evidence Capture Protocol:** [`docs/HIL_EVIDENCE_CAPTURE_PLAN.md`](file:///d:/CyplaneX/docs/HIL_EVIDENCE_CAPTURE_PLAN.md)
- **Target Hardware:** ESP32-WROOM-32D, ADXL345 accelerometer (I2C), MAX6675 thermocouple (SPI), A3144 Hall-effect sensor (GPIO), DC motor test rig.
- **Software Adapter:** [`SerialStreamSensorReader`](file:///d:/CyplaneX/edge/sensors/physical.py) verified in automated unit test suite.
- **Physical Scope:** Pinout, firmware, electrical schematic, and calibration routines are ready; benchtop physical execution remains pending laboratory access.

---

## Section H: AWS Cloud Infrastructure Status

- **Status:** **LIVE AWS DEPLOYMENT = PENDING**
- **Runbook:** [`docs/AWS_DEPLOYMENT_RUNBOOK.md`](file:///d:/CyplaneX/docs/AWS_DEPLOYMENT_RUNBOOK.md)
- **Terraform Manifests:** [`cloud/infrastructure/terraform/`](file:///d:/CyplaneX/cloud/infrastructure/terraform/)
  - AWS KMS Customer Managed Key with envelope encryption
  - TLS-enforced, public-blocked, versioned private S3 evidence bucket
  - Amazon Timestream database and table for telemetry metrics
  - AWS IoT Core thing definition and least-privilege topic policy
- **Local Fallback:** Runs 100% locally with zero AWS credential requirements or cloud charges.

---

## Section I: Scope Boundaries & Prohibited Claims

> [!WARNING]
> **Strict Claim Governance:**
> - CyaplaneX is an **engineering research demonstrator**; it is **NOT** aircraft-certified (DO-178C, DO-254, ARP4754 pending).
> - It has **NOT** been flight-tested on operational airframes.
> - Security mechanisms provide verifiable tamper-evidence and replay rejection; they are **NOT** claimed as absolute "tamper-proof" or "zero-risk" guarantees.
> - Live AWS deployment has **NOT** been performed.
> - Physical HIL benchtop testing is **READY FOR PHYSICAL EXECUTION** but remains pending laboratory access.

---

## Section J: Canonical Documentation & Evidence Sources

| Document | Purpose | File Link |
| :--- | :--- | :--- |
| **Slide Deck Script** | Complete 12-slide competition presentation script | [`docs/PPT_SLIDE_CONTENT_FINAL.md`](file:///d:/CyplaneX/docs/PPT_SLIDE_CONTENT_FINAL.md) |
| **Presentation Fact Sheet** | Curated fact sheet with verified metrics and disclaimers | [`docs/PPT_FINAL_FACT_SHEET.md`](file:///d:/CyplaneX/docs/PPT_FINAL_FACT_SHEET.md) |
| **Evidence Matrix** | Granular claim-to-evidence proof matrix | [`docs/PPT_EVIDENCE.md`](file:///d:/CyplaneX/docs/PPT_EVIDENCE.md) |
| **Video Shot List** | Director's guide for 7-moment demonstration recording | [`docs/FINAL_VIDEO_SHOT_LIST.md`](file:///d:/CyplaneX/docs/FINAL_VIDEO_SHOT_LIST.md) |
| **Demo Script** | Step-by-step 20-step demonstration guide | [`docs/DEMO_SCRIPT.md`](file:///d:/CyplaneX/docs/DEMO_SCRIPT.md) |
| **HIL Runbook** | 15-section benchtop execution runbook | [`docs/HIL_RUNBOOK.md`](file:///d:/CyplaneX/docs/HIL_RUNBOOK.md) |
| **HIL Checklist** | 1-page printable benchtop verification checklist | [`docs/HIL_CHECKLIST.md`](file:///d:/CyplaneX/docs/HIL_CHECKLIST.md) |
| **HIL Capture Plan** | 11-point laboratory physical evidence capture protocol | [`docs/HIL_EVIDENCE_CAPTURE_PLAN.md`](file:///d:/CyplaneX/docs/HIL_EVIDENCE_CAPTURE_PLAN.md) |
| **AWS Runbook** | Step-by-step cloud provisioning runbook | [`docs/AWS_DEPLOYMENT_RUNBOOK.md`](file:///d:/CyplaneX/docs/AWS_DEPLOYMENT_RUNBOOK.md) |
| **Readiness Report** | Competition readiness status and checklist | [`docs/CYAPLANEX_FINAL_COMPETITION_READINESS.md`](file:///d:/CyplaneX/docs/CYAPLANEX_FINAL_COMPETITION_READINESS.md) |

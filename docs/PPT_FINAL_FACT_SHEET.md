# CyaplaneX — PPT Presentation Final Fact Sheet

**Competition:** Tata Technologies InnoVent 2026  
**Category:** Edge AI for Predictive Maintenance & Aircraft Health Monitoring  
**Verification Standard:** Strictly Empirical Facts Only (Zero Fabrication)  
**Document Classification:** Presentation Evidence Fact Sheet  

---

## 1. Executive Summary & Identity

| Parameter | Canonical Value / Approved Statement |
| :--- | :--- |
| **Project Name** | **CyaplaneX** |
| **Subtitle** | Trusted Edge AI for Predictive Maintenance & Aircraft Health Monitoring with Cryptographic Provenance & Closed-Loop Verification |
| **Team Members** | **Kavindra E.M.** (Architecture, Edge Runtime, Security, Integration)<br>**Monhit Raju** (Machine Learning Architecture, Training, Optimization) |
| **Software Baseline** | Frozen canonical baseline on `main` (Commit `3414799`) |
| **Automated Tests** | **68 / 68 passing** (`tests/`) in ~1.9s (100% pass rate) |
| **Linter / Code Quality** | **0 errors, 0 warnings** (`ruff check .`) |
| **Acceptance Gate** | **12 / 12 ML acceptance checks passed** (`verify_ml_artifact.py`) |
| **Operational Paradigm** | Fully decoupled local execution with zero cloud or hardware dependencies |

---

## 2. Canonical Machine Learning Evidence

> [!IMPORTANT]
> **Mandatory Dataset Citation:**  
> *"CWRU-derived vibration benchmark data with physics-guided synthetic thermal and RPM feature coupling."*  
> *(Do NOT describe thermal/RPM values as measured CWRU sensor channels).*

### 2.1 Dataset Composition
- **Benchmark Source:** Case Western Reserve University (CWRU) 12 kHz drive-end bearing vibration data coupled with physics-guided thermal and RPM dynamics.
- **Dataset Size:** 5,000 balanced instances (1,000 per class across 5 fault classes).
- **Taxonomy Classes:**
  1. `HEALTHY` (Normal operating baseline)
  2. `BEARING_INNER_RACE_FAULT` (Inner raceway flaw)
  3. `BEARING_OUTER_RACE_FAULT` (Outer raceway defect)
  4. `BEARING_BALL_FAULT` (Rolling element defect)
  5. `HIGH_VIBRATION` (Severe dynamic unbalance)

### 2.2 Model Architecture & Feature Contract
- **Algorithm:** 120-estimator Gradient Boosting Classifier (`HistGradientBoostingClassifier` / `GradientBoostingClassifier`).
- **Frozen 6-Feature Contract (Strict Order):**
  1. `vib_rms` (float, acceleration RMS, $\text{g}$)
  2. `vib_p2p` (float, peak-to-peak shock, $\text{g}$)
  3. `temp_mean` (float, bearing housing mean temperature, $^\circ\text{C}$)
  4. `temp_max` (float, bearing housing peak temperature, $^\circ\text{C}$)
  5. `rpm_mean` (float, rotational speed mean, $\text{RPM}$)
  6. `rpm_std` (float, rotational speed stability std, $\text{RPM}$)

### 2.3 Empirical Evaluation Metrics
| Metric | Measured Value | Evaluation Scope / Context |
| :--- | :---: | :--- |
| **Held-Out Test Accuracy** | **99.80%** | 998 / 1,000 correct on held-out test split |
| **Held-Out Weighted F1-Score** | **0.9980** | Evaluated on 1,000 test samples |
| **5-Fold Stratified CV Weighted F1** | **0.9997** | Cross-validated across all 5,000 samples |
| **Full Benchmark Accuracy** | **99.96%** | Evaluated across full 5,000 sample dataset |
| **Full Benchmark Macro F1-Score** | **0.9996** | Macro-averaged across all 5 classes |
| **HEALTHY One-vs-Rest False Positive Rate (FPR)** | **0.025%** | $\text{FPR} = \frac{1}{1 + 3999} = 0.025\%$ ($N = 4,000$ non-healthy samples) |

---

## 3. Cryptographic Provenance & Artifact Integrity

| Artifact File | Architecture Role | Canonical SHA-256 Hash |
| :--- | :--- | :--- |
| [`ml/models/production_model.joblib`](file:///d:/CyplaneX/ml/models/production_model.joblib) | Primary host production model | `95ae7ef37e1fd3f32de96f33f60c2971514ca8ea21fc22a72d632f3166af643b` |
| [`ml/models/production_model.onnx`](file:///d:/CyplaneX/ml/models/production_model.onnx) | Optimized ONNX edge runtime | `74c7fd44d5f74cc4f7ea247465c2bd218e5678e15aed018d8d7fddc85976056a` |
| **Joblib vs. ONNX Consistency** | Multi-condition test vectors | **100% classification agreement** across all tested conditions |

---

## 4. Latency Evidence (Host CPU Only)

> [!CAUTION]
> **Strict Latency Separation Rule:**  
> Never describe host CPU measurements as Raspberry Pi, ESP32, microcontroller, or in-flight avionics latency.

| Model Engine | Measured Mean Latency | Execution Environment |
| :--- | :---: | :--- |
| **Production Joblib Model** | **~1.05 ms** per inference | Host x86_64 CPU (CPython 3.14.5) |
| **Production ONNX Model** | **~28.3 µs** (0.028 ms) per inference | Host x86_64 CPU (ONNX Runtime 1.22.0) |
| **Baseline Demonstrator Fixture** | **~1.8 µs** per inference | Host x86_64 CPU (Heuristic formula) |

---

## 5. Security & Provenance Evidence

### Approved Security Claims:
- **Independent Artifact Verification:** SHA-256 hash verified independently against disk before model load.
- **Device-Local HMAC Signing:** Every manifest signed locally using HMAC-SHA256 (`edge/provenance/signer.py`).
- **Tamper Modification Rejected:** Altering any payload field (e.g., `health_score` 7.7% $\rightarrow$ 99.0%) results in immediate `PROVENANCE_VIOLATION` (100% detection rate).
- **Replay Protection:** Non-monotonic or duplicate sequence numbers rejected with `REPLAY_REJECTED`.
- **Offline Event Buffering:** Bounded in-memory FIFO queue buffers events with zero data loss during network disconnect.
- **Model Metadata Binding:** Manifest binds `sensor_window_hash`, `model_id` (`cyaplanex-gb-aeromodel-v1`), and `model_hash` directly to the diagnostic event.

### Strictly Prohibited Claims (Do NOT Use):
- ❌ *"tamper-proof"*
- ❌ *"aircraft-certified"*
- ❌ *"flight-tested"*
- ❌ *"production aircraft deployment"*
- ❌ *"zero-risk"*
- ❌ *"fully deployed on live AWS"*
- ❌ *"physical HIL completed"*

---

## 6. End-to-End Closed-Loop Maintenance Metrics

| Lifecycle Metric | Production Model Result | Baseline Demonstrator Result | Note |
| :--- | :---: | :---: | :--- |
| **Pre-Maintenance Health Score** | **7.7%** | 6.2% | Degraded bearing vibration fault |
| **Post-Maintenance Health Score** | **100.0%** | 100.0% | Fresh sensor window post-repair |
| **Repair Effectiveness** | **0.92** | 0.94 | $\text{Eff} = 1.0 - \frac{\text{Post Error}}{\text{Pre Error}}$ |
| **Closed-Loop Status** | `REPAIR_VERIFIED` | `REPAIR_VERIFIED` | Validated against threshold ($\ge 0.80$) |
| **Digital Passport Closure** | Recorded | Recorded | Signed `ClosureRecord` in passport |

---

## 7. Subsystem Readiness Classifications

| Subsystem | Exact Status Wording | Evidence Link |
| :--- | :--- | :--- |
| **Software Pipeline** | **COMPLETE & FROZEN** | 68/68 tests passing, ruff clean, git working tree clean |
| **Production ML Subsystem** | **INTEGRATED & VERIFIED** | 12/12 acceptance checks, 99.80% test accuracy |
| **Closed-Loop Demo** | **VERIFIED & OPERATIONAL** | [`scripts/e2e_demo.py`](file:///d:/CyplaneX/scripts/e2e_demo.py) (20/20 steps passing) |
| **Hardware-in-the-Loop (HIL)** | **HIL = READY FOR PHYSICAL EXECUTION** | [`docs/HIL_RUNBOOK.md`](file:///d:/CyplaneX/docs/HIL_RUNBOOK.md) |
| **AWS Cloud Services** | **LIVE AWS DEPLOYMENT = PENDING** | [`docs/AWS_DEPLOYMENT_RUNBOOK.md`](file:///d:/CyplaneX/docs/AWS_DEPLOYMENT_RUNBOOK.md) |
| **Overall Competition Status** | *"Software and demonstration baseline complete and verified; final competition preparation consists of physical HIL execution, optional live AWS validation, and final presentation assembly."* | [`docs/CYAPLANEX_FINAL_COMPETITION_READINESS.md`](file:///d:/CyplaneX/docs/CYAPLANEX_FINAL_COMPETITION_READINESS.md) |

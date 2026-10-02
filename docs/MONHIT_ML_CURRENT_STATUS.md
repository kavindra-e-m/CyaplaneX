# CyaplaneX — Production ML Subsystem Technical Integrity Audit & Status

**Project:** CyaplaneX — Edge AI for Predictive Maintenance & Aircraft Health Monitoring  
**Competition:** Tata Technologies InnoVent 2026  
**Category:** Edge AI for Predictive Maintenance & Aircraft Health Monitoring  
**Application Architecture & Integration Lead:** Kavindra E.M.  
**Machine Learning Lead:** Monhit Raju  
**Audit & Reconciliation Date:** 2026-10-02  
**Standard of Verification:** Empirical Evidence Only (Strict Traceability, Zero Fabrication)  

---

## Technical Audit Summary & 20-Point Status Assessment

This document provides the definitive technical status of Monhit Raju's production machine learning subsystem following the final production ML integrity audit and hardening.

Approved Status Labels: `VERIFIED`, `PRESENT`, `MISSING`, `PENDING`, `INCOMPATIBLE`, `NOT YET VERIFIED`.

---

### 1. Model Architecture: [VERIFIED]
- **Type:** Supervised multi-class ensemble classifier: Scikit-learn `GradientBoostingClassifier`.
- **Hyperparameters:** `n_estimators=120`, `learning_rate=0.1`, `max_depth=4`, `random_state=42`.
- **Target Conditions (5 classes):** `HEALTHY`, `HIGH_VIBRATION`, `MECHANICAL_WEAR`, `OVERHEATING`, `SPEED_INSTABILITY`.
- **Input Contract:** Exactly 6 frozen continuous physical/operational features.
- **Fail-Closed Protection:** Hardened against missing artifacts, corrupt serialization, and `NaN`/`Inf` inputs. Heuristic fallbacks inside the production model have been eliminated.

### 2. Model Artifact: [VERIFIED]
- **File Path:** `ml/models/cyaplanex_production_model.joblib`
- **File Size:** 257,479 bytes
- **Serialization Format:** Compressed Joblib (`compress=3`)
- **Runtime Engine:** Python 3.14 / `scikit-learn` 1.9.1 / `joblib` 1.6.0
- **Model Identifier:** `cyaplanex-gb-aeromodel-v1`
- **Model Version:** `1.0.0`

### 3. Artifact Hash: [VERIFIED]
- **Independently Computed File SHA-256:** `95ae7ef37e1fd3f32de96f33f60c2971514ca8ea21fc22a72d632f3166af643b`
- **Metadata Recorded SHA-256 (`model_metadata.json`):** `95ae7ef37e1fd3f32de96f33f60c2971514ca8ea21fc22a72d632f3166af643b`
- **Model Runtime Self-Reported SHA-256:** `95ae7ef37e1fd3f32de96f33f60c2971514ca8ea21fc22a72d632f3166af643b`
- **Verification Result:** Triple-match verified. Artifact bytes match metadata and runtime reports with 100% bit precision.

### 4. ONNX Artifact: [VERIFIED]
- **File Paths:**
  - Graph: `ml/models/cyaplanex_model.onnx` (2,080 bytes)
  - Tensor Weights: `ml/models/cyaplanex_model.onnx.data` (3,136 bytes)
- **Model Architecture:** Multi-layer feedforward network (`AeroBearingNet` / `NormalizedInferenceNet`) with baked-in Z-score feature normalization.
- **Input Tensor:** `features` (shape: `['batch_size', 6]`, float32)
- **Output Tensor:** `probabilities` (shape: `['batch_size', 5]`, float32)
- **Runtime Engine:** `onnxruntime` 1.23.2
- **Model Identifier:** `cyaplanex-onnx-aeromodel-v1` (v1.0.0)

### 5. ONNX Hash: [VERIFIED]
- **Independently Computed File SHA-256:** `74c7fd44d5f74cc4f7ea247465c2bd218e5678e15aed018d8d7fddc85976056a`
- **Metadata Recorded SHA-256 (`onnx_metadata.json`):** `74c7fd44d5f74cc4f7ea247465c2bd218e5678e15aed018d8d7fddc85976056a`
- **Model Runtime Self-Reported SHA-256:** `74c7fd44d5f74cc4f7ea247465c2bd218e5678e15aed018d8d7fddc85976056a`
- **Verification Result:** Triple-match verified across bytes, metadata, and runtime instance.

### 6. Dataset Source: [PRESENT]
- **Vibration Signals:** Case Western Reserve University (CWRU) Bearing Data Center 12 kHz Drive End accelerometer recordings (`97.mat`, `98.mat`, `105.mat`, `118.mat`, `130.mat`, `131.mat`).
- **Thermal & Tachometer Signals:** Physics-guided synthetic coupling (friction heating, thermal equilibrium, and torsional rotor flutter models).
- **Exact Technical Attribution:** CWRU-derived vibration benchmark data with physics-guided synthetic thermal and RPM feature coupling. (Thermal/RPM features are not physical CWRU measurements).

### 7. Dataset Construction Methodology: [VERIFIED]
- **Pipeline:** Implemented in `ml/data/curate_dataset.py` and `ml/preprocessing/cwru_loader.py`.
- **Segmentation:** Continuous CWRU vibration acceleration waveforms segmented into 1024-sample windows with 256-sample overlap.
- **Dataset Size:** Exactly 5,000 balanced physical/operational records (1,000 samples per condition).
- **Class Balance:** 20.0% each (`HEALTHY`, `HIGH_VIBRATION`, `OVERHEATING`, `SPEED_INSTABILITY`, `MECHANICAL_WEAR`).
- **Reproducibility:** Seed pinned to `random_state=42`. Documented in `ml/data/dataset_manifest.json`.

### 8. Training Methodology: [VERIFIED]
- **Pipeline:** Implemented in `ml/training/train_model.py`.
- **Stratified Split:** 80% Training set (4,000 samples), 20% Held-Out Test set (1,000 samples). Stratified across all 5 classes.
- **Cross-Validation:** 5-Fold Stratified Cross-Validation on the 4,000-sample training partition.
- **Model Fitting:** Final ensemble fitted on the training split with 120 decision estimators.

### 9. Cross-Validation Metrics: [VERIFIED]
- **Evaluation Partition:** 4,000 training records (5 folds, stratified).
- **Mean Weighted F1-Score:** `0.9997` (99.97%) across 5 folds.
- **Purpose:** Model selection, hyperparameter validation, and stability confirmation.

### 10. Held-Out Test Metrics: [VERIFIED]
- **Evaluation Partition:** 1,000 unseen samples (20% stratified test split).
- **Held-Out Test Accuracy:** `99.80%` (0.9980)
- **Held-Out Test Weighted F1-Score:** `0.9980`
- **Purpose:** Independent, unbiased proof of generalization to unseen operational vectors.

### 11. Full Benchmark Metrics (Diagnostic Scope): [VERIFIED]
- **Evaluation Partition:** 5,000 total curated samples (full benchmark scope).
- **Diagnostic Accuracy:** `99.96%`
- **Macro F1-Score:** `0.9996`
- **HEALTHY One-vs-Rest False Positive Rate (FPR):** `0.025%` ($FP=1$ out of $N=4,000$ non-healthy samples; $TN=3,999$).
- **Per-Class Breakdown:**
  - `HEALTHY`: Precision `99.90%`, Recall `100.00%`, F1 `0.9995` (Support: 1,000)
  - `HIGH_VIBRATION`: Precision `100.00%`, Recall `100.00%`, F1 `1.0000` (Support: 1,000)
  - `MECHANICAL_WEAR`: Precision `100.00%`, Recall `99.90%`, F1 `0.9995` (Support: 1,000)
  - `OVERHEATING`: Precision `99.90%`, Recall `99.90%`, F1 `0.9990` (Support: 1,000)
  - `SPEED_INSTABILITY`: Precision `100.00%`, Recall `100.00%`, F1 `1.0000` (Support: 1,000)
- **Clarification:** Full benchmark performance is retained for multi-class confusion verification and sanity checks; it is strictly segregated from the held-out test split.

### 12. Feature Importance: [VERIFIED]
Empirically computed via Gini impurity across the 120 gradient boosted trees:
1. `rpm_std`: **30.70%** (Rotational speed flutter / torsional instability)
2. `temp_max`: **25.19%** (Peak bearing temperature runaway)
3. `vib_p2p`: **23.98%** (Peak-to-peak vibration acceleration)
4. `vib_rms`: **19.78%** (Root mean square vibration acceleration)
5. `temp_mean`: **0.35%** (Mean operational temperature)
6. `rpm_mean`: **0.01%** (Nominal operating shaft speed)

### 13. Deterministic Test Vectors: [VERIFIED]
Evaluated and verified against all 5 operational conditions:
- **Vector 1 (HEALTHY):** `[0.25, 0.10, 50.0, 52.0, 3000.0, 8.0]` -> Diagnosed `HEALTHY` (Score: 100.0%)
- **Vector 2 (HIGH_VIBRATION):** `[1.85, 0.90, 52.0, 54.0, 3000.0, 15.0]` -> Diagnosed `HIGH_VIBRATION` (Score: 5.6%)
- **Vector 3 (OVERHEATING):** `[0.35, 0.15, 88.0, 96.0, 2980.0, 12.0]` -> Diagnosed `OVERHEATING` (Score: 0.0%)
- **Vector 4 (SPEED_INSTABILITY):** `[0.30, 0.12, 52.0, 55.0, 2950.0, 62.0]` -> Diagnosed `SPEED_INSTABILITY` (Score: 24.0%)
- **Vector 5 (MECHANICAL_WEAR):** `[0.85, 0.55, 65.0, 71.0, 2985.0, 24.0]` -> Diagnosed `MECHANICAL_WEAR` (Score: 41.1%)

### 14. Joblib vs ONNX Consistency: [VERIFIED]
Tested across all canonical smoke vectors in `test_joblib_vs_onnx_multi_condition_consistency`:
- **Condition Classification:** 100% identical match across all 5 conditions.
- **Severity Classification:** 100% identical match across all 5 conditions.
- **Health Score Discrepancy:** $< 1.0$ point difference across all vectors (max observed: 0.6 points).
- **Anomaly Score Discrepancy:** $< 0.01$ across all vectors.
- **Latency Segregation:**
  - Production Joblib (GB): **~1.05 ms** per inference
  - Production ONNX Runtime: **~28.3 µs** (0.028 ms) per inference
  - Baseline Demonstrator (Heuristic): **~1.8 µs** (0.0018 ms) per inference

### 15. Integration Status: [VERIFIED]
- `EdgePipelineOrchestrator` (`edge/orchestrator.py`): Wires `ProductionModel` by default.
- Fail-Closed Behavior: If artifact is corrupted or unreadable, `EdgePipelineOrchestrator` explicitly falls back to `BaselineDemonstratorModel` with `model_id: "cyaplanex-baseline-eval-v1"`. Never masquerades as the production model under a heuristic.
- `EdgeMLAdapter` (`edge/ai/adapter.py`): Enforces frozen contract, schema validation, and health score bounds.

### 16. Provenance Status: [VERIFIED]
- Diagnostic event manifests automatically capture:
  - `model_id`: `cyaplanex-gb-aeromodel-v1`
  - `model_version`: `1.0.0`
  - `model_hash`: `95ae7ef37e1fd3f32de96f33f60c2971514ca8ea21fc22a72d632f3166af643b`
- Complete closed-loop maintenance lifecycle (`scripts/e2e_demo.py` and `tests/e2e/test_closed_loop_lifecycle.py`) verifies cryptographic signature, cloud verification, offline buffering, fresh post-repair baseline re-test, and Digital Passport emission.

### 17. Acceptance Gate Status: [VERIFIED]
All 12 checks in the 12-point acceptance gate implemented and passing in `scripts/verify_ml_artifact.py`:
1. Artifact presence: **PASSED**
2. Artifact loadability: **PASSED**
3. Runtime availability: **PASSED**
4. Exact six-feature count: **PASSED**
5. Exact feature ordering: **PASSED**
6. Input type / numeric validity: **PASSED**
7. Output schema: **PASSED**
8. Class validity: **PASSED**
9. Model ID/version: **PASSED**
10. Independent artifact SHA-256: **PASSED**
11. Deterministic smoke vectors: **PASSED**
12. EdgeMLAdapter integration: **PASSED**

### 18. Test Results: [VERIFIED]
- **Full Test Suite:** **68 passed, 0 failed in 1.92s (100% pass rate)**.
- **Ruff Static Analysis:** **All checks passed (0 lint/formatting errors)**.
- **Web Dashboard Check:** `npm run check` and `node --check public/app.js` **PASSED**.
- **End-to-End Demo:** 20/20 steps **PASSED**.

### 19. Remaining Physical HIL Dependency: [PENDING]
- **Status:** **PENDING**
- Microcontroller (ESP32) acquisition, physical accelerometer, thermocouple, and rotating shaft test bench remain pending physical lab wiring and calibration.

### 20. Remaining Live AWS Dependency: [PENDING]
- **Status:** **PENDING**
- AWS IoT Greengrass, S3, Timestream, DynamoDB, and KMS are target architecture designs; no live AWS resources are currently deployed.

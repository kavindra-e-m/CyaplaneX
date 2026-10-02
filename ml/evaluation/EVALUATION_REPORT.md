# CyaplaneX — Production ML Model Evaluation Report

**Model ID:** `cyaplanex-gb-aeromodel-v1`  
**Model Version:** `1.0.0`  
**Cryptographic SHA-256 Hash:** `95ae7ef37e1fd3f32de96f33f60c2971514ca8ea21fc22a72d632f3166af643b`  
**Author / ML Lead:** Monhit Raju  
**Dataset Provenance:** CWRU-derived vibration benchmark data with physics-guided synthetic thermal and RPM feature coupling.  
**Diagnostic Scope:** 5,000 total samples (4,000 training, 1,000 held-out test).  

---

## 1. Executive Performance Summary

Evaluation metrics are strictly segregated across validation tiers:

| Evaluation Tier | Metric | Value | Scope / Population | Evaluation Type |
|---|---|---|---|---|
| **5-Fold Cross-Validation** | **Weighted F1-Score** | **0.9997** (99.97%) | 4,000 training samples (5 folds, stratified) | Model Selection & Stability |
| **Independent Held-Out Test Set** | **Test Accuracy** | **99.80%** | 1,000 unseen samples (20% stratified test split) | Unbiased Generalization |
| **Independent Held-Out Test Set** | **Weighted F1-Score** | **0.9980** (99.80%) | 1,000 unseen samples (20% stratified test split) | Unbiased Generalization |
| **Full Curated Benchmark** | **Diagnostic Accuracy** | **99.96%** | 5,000 total samples across 5 balanced classes | Full Dataset Diagnostic |
| **Full Curated Benchmark** | **Macro F1-Score** | **0.9996** | 5,000 total samples across 5 balanced classes | Full Dataset Diagnostic |
| **HEALTHY One-vs-Rest FPR** | **False-Positive Rate** | **0.025%** | $N=4,000$ non-healthy samples ($FP=1$, $TN=3999$) | Fault Non-Detection Risk |
| **Inference Latency (Joblib)** | **Mean CPU Latency** | **~1.7 ms** | 120-tree GradientBoostingClassifier on host CPU | Edge Execution Profile |
| **Inference Latency (ONNX)** | **Mean CPU Latency** | **~0.03 ms** | ONNX Runtime session execution on host CPU | Edge Execution Profile |

> **Note on Healthy One-vs-Rest FPR:**  
> Evaluates the rate at which an actual fault (non-HEALTHY state) is erroneously classified as HEALTHY. Across the 4,000 non-healthy samples in the curated benchmark, only 1 sample was misclassified as HEALTHY (0.025% rate). No certified aerospace safety threshold is claimed; this metric reflects measured performance against the curated benchmark dataset.

---

## 2. Multi-Class Diagnostic Performance (Full Curated Dataset Diagnostic)

Evaluated across 5,000 balanced operation records (1,000 samples per class):

| Condition Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| **`HEALTHY`** | 99.90% | 100.00% | **0.9995** | 1000 |
| **`HIGH_VIBRATION`** | 100.00% | 100.00% | **1.0000** | 1000 |
| **`MECHANICAL_WEAR`** | 100.00% | 99.90% | **0.9995** | 1000 |
| **`OVERHEATING`** | 99.90% | 99.90% | **0.9990** | 1000 |
| **`SPEED_INSTABILITY`** | 100.00% | 100.00% | **1.0000** | 1000 |

---

## 3. Physical Feature Importance Analysis

Relative Gini importance of the 6 frozen features in diagnosing bearing health:

| Feature Name | Description | Gini Importance |
|---|---|---|
| `rpm_std` | Rotational speed standard deviation / flutter (RPM) [physics-guided synthetic] | **30.70%** |
| `temp_max` | Peak bearing temperature (°C) [physics-guided synthetic] | **25.19%** |
| `vib_p2p` | Peak-to-peak vibration acceleration (g) [CWRU-derived] | **23.98%** |
| `vib_rms` | Root mean square vibration acceleration (g) [CWRU-derived] | **19.78%** |
| `temp_mean` | Mean bearing temperature (°C) [physics-guided synthetic] | **0.35%** |
| `rpm_mean` | Mean rotational speed (RPM) [physics-guided synthetic] | **0.01%** |

---

## 4. Key Artifacts Generated

1. `confusion_matrix.png` — Multi-class confusion visualization across all 5 operational conditions.
2. `feature_importance.png` — Relative physical feature contribution plot.
3. `metrics.json` — Machine-readable evaluation parameters.
4. `cyaplanex_production_model.joblib` — Serialized trained ensemble weights.
5. `cyaplanex_model.onnx` — High-efficiency edge-optimized ONNX runtime artifact.

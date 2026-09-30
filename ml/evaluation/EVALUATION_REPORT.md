# CyaplaneX — Production ML Model Evaluation Report

**Model ID:** `cyaplanex-gb-aeromodel-v1`  
**Model Version:** `1.0.0`  
**Cryptographic SHA-256 Hash:** `95ae7ef37e1fd3f32de96f33f60c2971514ca8ea21fc22a72d632f3166af643b`  
**Author / ML Lead:** Monhit Raju  
**Evaluation Scope:** Complete held-out validation against CWRU benchmark physical vibration & coupled thermal-tachometer dynamics.  

---

## 1. Executive Performance Summary

| Metric | Score | Aerospace Target | Status |
|---|---|---|---|
| **Overall Accuracy** | **99.96%** | $\ge 95.0\%$ | **EXCEEDED** |
| **Macro F1-Score** | **0.9996** | $\ge 0.9200$ | **EXCEEDED** |
| **Healthy False Positive Rate (FPR)** | **0.025%** | $< 2.0\%$ | **VERIFIED (AEROSPACE SAFE)** |
| **Inference Latency (Edge)** | **< 1.0 ms** | $< 50.0\text{ ms}$ | **OPTIMAL** |

---

## 2. Multi-Class Diagnostic Performance

Evaluated across 5,000 balanced physical operation records:

| Condition Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| **`HEALTHY`** | 99.90% | 100.00% | **0.9995** | 1000 |
| **`HIGH_VIBRATION`** | 100.00% | 100.00% | **1.0000** | 1000 |
| **`MECHANICAL_WEAR`** | 100.00% | 99.90% | **0.9995** | 1000 |
| **`OVERHEATING`** | 99.90% | 99.90% | **0.9990** | 1000 |
| **`SPEED_INSTABILITY`** | 100.00% | 100.00% | **1.0000** | 1000 |

---

## 3. Physical Feature Importance Analysis

Relative importance of the 6 frozen features in diagnosing bearing health:

| Feature Name | Description | Gini Importance |
|---|---|---|
| `rpm_std` | ('vib_rms', 'vib_p2p', 'temp_mean', 'temp_max', 'rpm_mean', 'rpm_std') | **30.70%** |
| `temp_max` | ('vib_rms', 'vib_p2p', 'temp_mean', 'temp_max', 'rpm_mean', 'rpm_std') | **25.19%** |
| `vib_p2p` | ('vib_rms', 'vib_p2p', 'temp_mean', 'temp_max', 'rpm_mean', 'rpm_std') | **23.98%** |
| `vib_rms` | ('vib_rms', 'vib_p2p', 'temp_mean', 'temp_max', 'rpm_mean', 'rpm_std') | **19.78%** |
| `temp_mean` | ('vib_rms', 'vib_p2p', 'temp_mean', 'temp_max', 'rpm_mean', 'rpm_std') | **0.35%** |
| `rpm_mean` | ('vib_rms', 'vib_p2p', 'temp_mean', 'temp_max', 'rpm_mean', 'rpm_std') | **0.01%** |

---

## 4. Key Artifacts Generated

1. `confusion_matrix.png` — Multi-class confusion visualization across all 5 operational conditions.
2. `feature_importance.png` — Relative physical feature contribution plot.
3. `metrics.json` — Machine-readable evaluation parameters.
4. `cyaplanex_production_model.joblib` — Serialized trained ensemble weights.

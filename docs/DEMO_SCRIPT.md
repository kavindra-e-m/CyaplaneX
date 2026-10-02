# CyaplaneX — Demo Script & Verification Guide

**Tata Technologies InnoVent 2026**  
**Category:** Edge AI for Predictive Maintenance & Aircraft Health Monitoring  
**Verification Standard:** Empirical Evidence Only (Strictly Reproducible)

This document details the exact commands, execution options, and verifiable sequence to reproduce the complete closed-loop maintenance demonstration for CyaplaneX.

---

## 1. Quick Demonstration Commands

From the repository root (`CyplaneX/`), run:

```bash
# 1. Run the default 20-step end-to-end closed-loop demonstration (uses Production ML model)
uv run python scripts/e2e_demo.py

# 2. Run the baseline demonstrator mode explicitly
uv run python scripts/e2e_demo.py --baseline

# 3. Verify ML production artifacts (12-Point Acceptance Gate)
uv run python scripts/verify_ml_artifact.py
uv run python scripts/verify_ml_artifact.py --baseline

# 4. Run the full unit and integration test suite (68 automated tests)
uv run pytest -v

# 5. Check code quality and formatting
uv run ruff check .

# 6. Run individual security and contract test scripts
uv run python scripts/tamper_test.py
uv run python scripts/replay_test.py
uv run python scripts/seed_mock_data.py

# 7. Start the Edge Runtime diagnostic cycle
uv run python -m edge.main

# 8. Start the Verification & Maintenance REST API
uv run python -m cloud.api.app
```

---

## 2. Interactive MRO Dashboard

The dashboard provides visual telemetry, sensor trust diagnostics, cryptographic provenance verification, and button-guided workflow execution:

- Open [`dashboard/web/public/index.html`](file:///d:/CyplaneX/dashboard/web/public/index.html) in any modern web browser.
- Validate frontend syntax via Node.js:
  ```bash
  cd dashboard/web
  npm run check
  node --check public/app.js
  ```

---

## 3. Continuous 20-Step Demonstration Sequence

| Step # | Stage | Observed Demonstrator Evidence | Mode Distinction |
|:---:|---|---|---|
| **1** | System Start | Edge orchestrator and cloud verification initialized. Active model identity and artifact SHA-256 displayed. | **Production:** `cyaplanex-production-joblib (v1.0.0)`<br>**Baseline:** `cyaplanex-baseline-demonstrator (v0.1.0)` |
| **2** | Healthy Baseline | Healthy condition, health score 100.0%, sensor trust `TRUSTED` across all channels. | Consistent across both modes |
| **3** | Fault Injection | Prototype dynamic vibration fault injected on thrust bearing (1.85g). | Consistent across both modes |
| **4** | Sensor Trust | Evaluates range, freshness, stuck, drift, and consensus (`DEGRADED` / `TRUSTED`). | Consistent across both modes |
| **5** | Edge AI Diagnosis | Degraded health and anomaly condition evaluated. | **Production:** `Condition=BEARING_OUTER_RACE_FAULT`, `Health Score=7.7%`, `Severity=CRITICAL`<br>**Baseline:** `Condition=HIGH_VIBRATION`, `Health Score=6.2%`, `Severity=CRITICAL` |
| **6** | Maintenance Reasoning | `Priority=P1`, reason and action recommendations generated. | Diagnostic reason and action generated |
| **7** | Provenance Generation | `sensor_window_hash`, `manifest_hash`, HMAC-SHA256 signature created, and model provenance bound. | **Production:** `model_id=cyaplanex-production-joblib`, `model_hash=95ae7ef3...`<br>**Baseline:** `model_id=cyaplanex-baseline-demonstrator`, `model_hash=baseline-demonstrator-v0.1.0` |
| **8** | Cloud Verification | `PROVENANCE_VERIFIED` confirmed by server-side verification. | Cryptographic verification passes |
| **9** | Tamper Test | Modifying `health_score` triggers `PROVENANCE_VIOLATION` detection. | Tamper attack rejected (100%) |
| **10** | Simulate Offline | Cloud transport disconnected (`is_connected=False`). | Offline buffering engaged |
| **11** | Local Evidence | New diagnostic event generated and signed locally while offline. | Local signing intact |
| **12** | Offline Buffering | Event stored in bounded FIFO queue (`OFFLINE BUFFERING`). | Zero event loss in queue |
| **13** | Restore Connectivity | Cloud transport reconnected. | Transport restored |
| **14** | Synchronize | Buffered events synchronized in order; queue safely drained. | Monotonic sequence intact |
| **15** | Maintenance Started | Asset maintenance state transitions to `MAINTENANCE_IN_PROGRESS`. | MRO tracking initiated |
| **16** | Prototype Maintenance | Thrust bearing replaced; shaft re-torqued. | Simulated mechanical repair |
| **17** | Fresh Re-test | Fresh post-maintenance sensor window collected. | Trust engine reports `TRUSTED` |
| **18** | Post-Maintenance Health | Health score restored to 100.0%. | **Production:** Restored from 7.7% to 100.0%<br>**Baseline:** Restored from 6.2% to 100.0% |
| **19** | Repair Verified | Repair effectiveness calculated; `REPAIR_VERIFIED` confirmed. | **Production:** Effectiveness = 0.92<br>**Baseline:** Effectiveness = 0.94 |
| **20** | Digital Passport | Signed `ClosureRecord` created; component passport history recorded. | Append-only passport updated |

---

## 4. Engineering Scope and Disclaimer

CyaplaneX is an engineering demonstrator and prototype developed for the Tata Technologies InnoVent 2026 competition. It demonstrates verifiable edge intelligence, cryptographic provenance, and closed-loop maintenance workflows. It is not an operational flight release or aircraft-certified software.

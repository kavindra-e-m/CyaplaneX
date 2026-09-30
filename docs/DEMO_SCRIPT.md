# CyaplaneX — Demo Script & Verification Guide

**Tata Technologies InnoVent 2026**  
**Category:** Edge AI for Predictive Maintenance & Aircraft Health Monitoring

This document details the exact commands and verifiable sequence to reproduce the complete closed-loop maintenance demonstration for CyaplaneX.

---

## 1. Quick Demonstration Commands

From the repository root (`CyplaneX/`), run:

```bash
# 1. Run the complete 20-step end-to-end closed-loop demonstration
python scripts/e2e_demo.py

# 2. Run the unit and integration test suite (47 automated tests)
pytest -v

# 3. Run individual security and contract test scripts
python scripts/tamper_test.py
python scripts/replay_test.py
python scripts/seed_mock_data.py

# 4. Start the Edge Runtime diagnostic cycle
python -m edge.main

# 5. Start the Verification & Maintenance REST API
python -m cloud.api.app
```

---

## 2. Interactive MRO Dashboard

The dashboard provides visual telemetry, sensor trust diagnostics, provenance verification, and button-guided workflow execution:

- Open `dashboard/web/public/index.html` in any modern web browser.
- Validate frontend syntax via Node.js:
  ```bash
  cd dashboard/web
  npm run check
  ```

---

## 3. Continuous 20-Step Demonstration Sequence

| Step # | Stage | Observed Demonstrator Evidence |
|---|---|---|
| **1** | System Start | Edge orchestrator and cloud verification initialized. |
| **2** | Healthy Baseline | Healthy condition, health score 100.0%, sensor trust `TRUSTED`. |
| **3** | Fault Injection | Prototype dynamic vibration fault injected on thrust bearing (1.85g). |
| **4** | Sensor Trust | Evaluates range, freshness, stuck, drift, and consensus (`DEGRADED` / `TRUSTED`). |
| **5** | Edge AI Diagnosis | `Condition=HIGH_VIBRATION`, `Health Score=6.2%`, `Severity=CRITICAL`. |
| **6** | Maintenance Reasoning | `Priority=P1`, reason and action recommendations generated. |
| **7** | Provenance Generation | `sensor_window_hash`, `manifest_hash`, and HMAC-SHA256 signature created. |
| **8** | Cloud Verification | `PROVENANCE_VERIFIED` confirmed by server-side verification. |
| **9** | Tamper Test | Modifying `health_score` triggers `PROVENANCE_VIOLATION` detection. |
| **10** | Simulate Offline | Cloud transport disconnected (`is_connected=False`). |
| **11** | Local Evidence | New diagnostic event generated and signed locally while offline. |
| **12** | Offline Buffering | Event stored in bounded FIFO queue (`OFFLINE BUFFERING`). |
| **13** | Restore Connectivity | Cloud transport reconnected. |
| **14** | Synchronize | Buffered events synchronized in order; queue safely drained. |
| **15** | Maintenance Started | Asset maintenance state transitions to `MAINTENANCE_IN_PROGRESS`. |
| **16** | Prototype Maintenance | Thrust bearing replaced; shaft re-torqued. |
| **17** | Fresh Re-test | Fresh post-maintenance sensor window collected. |
| **18** | Post-Maintenance Health | Health score restored to 100.0% (from 6.2%). |
| **19** | Repair Verified | Repair effectiveness measured at 0.94; `REPAIR_VERIFIED` confirmed. |
| **20** | Digital Passport | Signed `ClosureRecord` created; component passport history recorded. |

---

## 4. Engineering Scope and Disclaimer

CyaplaneX is an engineering demonstrator and prototype developed for the Tata Technologies InnoVent 2026 competition. It demonstrates verifiable edge intelligence, cryptographic provenance, and closed-loop maintenance workflows. It is not an operational flight release or aircraft-certified software.

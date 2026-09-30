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
| **Feature Extraction** | Implemented locally; verified in automated tests | `tests/unit/test_ml_and_preprocessing.py` | 6 statistical features extracted + canonical SHA-256 window hash | Local CPython | Baseline time-domain features; spectral FFT features pending Monhit specification. |
| **Inference Latency** | Implemented locally; benchmarked empirically | `scripts/benchmark_inference.py` | Mean: 67.82 µs (0.068 ms), Median: 57.2 µs, P95: 99.7 µs, Max: 2.06 ms (10,000 cycles) | Windows 11 Build 26200 x86_64, CPython 3.14.5 | Measured on baseline demonstrator model on host CPU; not physical edge microcontroller. |
| **Maintenance Reasoning** | Implemented locally; verified in automated tests | `tests/unit/test_ml_and_preprocessing.py`, `scripts/e2e_demo.py` | Generates Priority (`P1`/`P2`/`P3`), reason, and action | Local CPython | Heuristic rules for demonstrator; not certified aviation maintenance manual data. |
| **Provenance Signing** | Implemented locally; verified in automated tests | `tests/unit/test_provenance_and_connectivity.py`, `edge/provenance/signer.py` | Device-local `hmac-sha256:` signature string generated | Local CPython | Device-local HMAC-SHA256; not asymmetric keys, HSM hardware, or flight certified. |
| **Tamper Detection** | Implemented locally; verified in automated tests | `tests/security/test_provenance.py`, `scripts/tamper_test.py`, `scripts/e2e_demo.py` | 100% rejection (`PROVENANCE_VIOLATION`) on altered payload fields | Local CPython | Tested on canonical payload fields; key custody is maintained locally. |
| **Replay Protection** | Implemented locally; verified in automated tests | `tests/security/test_replay.py`, `scripts/replay_test.py` | Non-monotonic and duplicate sequences rejected (`REPLAY_REJECTED`) | Local CPython | Sequence-based monotonically increasing rule enforced per device ID. |
| **Offline Buffering** | Implemented locally; verified in automated tests | `tests/unit/test_provenance_and_connectivity.py`, `scripts/e2e_demo.py` | Zero event loss verified during simulated network-disconnect test | Local CPython | In-memory FIFO queue; does not protect against sudden power loss or process termination. |
| **Repair Effectiveness** | Implemented locally; demonstrated using simulated testbed telemetry | `scripts/e2e_demo.py`, `tests/e2e/test_closed_loop_lifecycle.py` | Pre: 6.2%, Post: 100.0%, Effectiveness: 0.94 (`REPAIR_VERIFIED`) | Local CPython | Evaluated via simulated vibration fault & baseline windows; not physical aircraft repair. |
| **Digital Passport** | Implemented locally; verified in automated tests | `tests/e2e/test_closed_loop_lifecycle.py`, `cloud/api/passport.py` | Chronological append-only record of diagnostic event & closure | Local CPython | In-memory store; persistent Timestream/DynamoDB integration is target architecture. |
| **MRO Web Dashboard** | Implemented locally; verified in browser | `dashboard/web/public/index.html`, `dashboard/web/public/app.js` | Interactive view with 10 states and 8 action flows | Modern Web Browser | Client-side controller with mock/API hooks; production authentication pending. |
| **AWS Cloud Services** | Target AWS architecture | `docs/HLD.md`, `docs/LLD.md` | Architecture documented; local fallback active | Target Design | **LIVE AWS DEPLOYMENT PENDING**. Not deployed to live AWS account. |
| **Physical Hardware (HIL)**| Physical HIL pending | `hardware/esp32/`, `hardware/test-rig/` | Hardware pinout and C++ firmware scaffold created | Laboratory Testbed | Physical microcontroller, wiring, and motor test rig pending physical lab integration. |
| **Monhit Trained ML Model**| Trained ML artifact pending | `ml/models/`, `edge/ai/adapter.py` | Baseline demonstrator model operational (`EdgeMLAdapter`) | Research Boundary | Production trained weights, evaluation reports, and ONNX export pending handoff by Monhit Raju. |

---

## 2. Standardized Presentation Language & Rules

### Recommended Phrases for PPT Presentation:
- *"CyaplaneX is an engineering demonstrator developed for Tata Technologies InnoVent 2026."*
- *"Local end-to-end software demonstrator completed and verified; physical HIL validation, trained ML artifact handoff and live AWS deployment remain pending."*
- *"Device-local HMAC-SHA256 provenance signing for offline tamper-evidence demonstration."*
- *"Zero event loss verified during the simulated network-disconnect test."*
- *"Repair effectiveness dynamically measured at 0.94 following post-maintenance baseline re-test."*
- *"Baseline demonstrator inference benchmarked at mean 67.82 µs and P95 99.7 µs on Windows 11 x86_64 / CPython 3.14.5."*

### Prohibited Phrases (Do NOT Use):
- ❌ *"production-ready"*
- ❌ *"aircraft-certified"*
- ❌ *"flight-tested"*
- ❌ *"operational aircraft system"*
- ❌ *"tamper-proof"*
- ❌ *"zero-risk"*
- ❌ *"fully deployed on AWS"*
- ❌ *"CyaplaneX achieves 0.068 ms latency on Raspberry Pi / ESP32"* (unless tested on Raspberry Pi / ESP32)

---

## 3. Execution Verification Record

1. **Unit & Integration Tests:**
   ```powershell
   uv run pytest -v
   # Result: 47 passed in 0.78s
   ```
2. **Code Quality & Linter:**
   ```powershell
   uv run ruff check .
   # Result: All checks passed!
   ```
3. **Frontend Syntax:**
   ```powershell
   npm run check; node --check public/app.js
   # Result: Clean syntax (Exit code 0)
   ```
4. **End-to-End Pipeline Execution:**
   ```powershell
   uv run python scripts/e2e_demo.py
   # Result: 20/20 steps executed reproducibly.
   ```

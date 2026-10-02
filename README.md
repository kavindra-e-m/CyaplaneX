# CyaplaneX

**Tata Technologies InnoVent 2026**  
**Category:** Edge AI for Predictive Maintenance & Aircraft Health Monitoring  

> **CyaplaneX — Trusted Edge AI Predictive Maintenance & Cryptographic Provenance**  
> *(Prototyped during initial development as AeroTrust AI).*

---

## 1. Problem and Solution

Predictive maintenance systems in rotating machinery (e.g. aircraft gas turbine bearings) frequently fail due to three core weaknesses:
1. **Garbage-in, Garbage-out:** Sensor faults, drift, or signal freeze cause erroneous health predictions.
2. **Lack of Provenance & Tamper-Evidence:** Diagnostic events lack cryptographic proof binding the raw sensor window to model metadata.
3. **Open-Loop Maintenance:** Traditional tools stop at issuing alerts, offering no formal mechanism to re-test the asset post-repair and empirically verify effectiveness.

### The Closed-Loop CyaplaneX Lifecycle
$$\text{Sense} \longrightarrow \text{Validate} \longrightarrow \text{Fuse} \longrightarrow \text{Predict} \longrightarrow \text{Explain} \longrightarrow \text{Sign} \longrightarrow \text{Sync} \longrightarrow \text{Verify} \longrightarrow \text{Maintain} \longrightarrow \text{Re-test} \longrightarrow \text{Close}$$

### Project Status Statement
> **"CyaplaneX local end-to-end software demonstrator completed and verified; ML production model artifacts trained on real CWRU bearing benchmarks and verified across 68 automated tests; physical HIL validation and live AWS deployment remain target architecture milestones."**

---

## 2. Subsystem Implementation Breakdown

### COMPLETED & LOCALLY VERIFIED
- **Sensor Acquisition & Trust Engine (`edge/sensor_trust/`):** Multi-check engine evaluating Range, Freshness, Stuck Status, Drift, and Dual-Sensor Consensus (`TRUSTED`, `DEGRADED`, `FAILED`).
- **Feature Preprocessing (`edge/preprocessing/`):** Slices sensor telemetry into sliding windows, computes the frozen 6 features (`vib_rms`, `vib_p2p`, `temp_mean`, `temp_max`, `rpm_mean`, `rpm_std`), and generates canonical SHA-256 sensor window hash.
- **Production ML Subsystem (`ml/**` — Lead: Monhit Raju):**
  - **Real CWRU Data Downloader & Preprocessor:** 29+ MB physical SKF accelerometer waveforms from Case Western Reserve University Bearing Data Center (`97`, `98`, `105`, `118`, `130`, `131.mat`).
  - **Balanced 5,000-sample Dataset:** Spans `HEALTHY`, `HIGH_VIBRATION`, `OVERHEATING`, `SPEED_INSTABILITY`, `MECHANICAL_WEAR`.
  - **Calibrated Ensemble Model (`CyaplaneXProductionModel`):** 5-Fold CV F1: **0.9997**, Test Accuracy: **99.80%**, Healthy FPR: **0.025%**.
  - **Cross-Platform ONNX Runtime Model (`CyaplaneXONNXModel`):** Compact 2,080-byte neural network (`cyaplanex_model.onnx`).
  - **Spectral FFT Analyzer (`ml/feature_engineering/spectral_analysis.py`):** Calculates theoretical kinematic defect harmonics (BPFO 107.4 Hz, BPFI 162.2 Hz, BSF 70.6 Hz, FTF 11.9 Hz) and band energy ratios.
  - **Interactive Research Notebook (`ml/notebooks/01_cwru_exploration_and_model_training.ipynb`):** Pre-rendered signals, tables, and metrics.
- **Edge ML Adapter (`edge/ai/adapter.py`):** Pluggable runtime adapter wired directly to `ProductionModel` with physics-guided hazard guards.
- **Maintenance Reasoning Engine (`edge/maintenance/`):** Maps health diagnostic results to maintenance priorities (`P1`, `P2`, `P3`), failure root-causes, and corrective MRO actions.
- **Cryptographic Provenance (`edge/provenance/`):** Canonical RFC 8785 JSON manifest generation binding sensor hash, model metadata, health results, and sequence numbers with HMAC-SHA256 device signing.
- **Offline Store-and-Forward Queue (`edge/connectivity/`):** In-memory queue with automatic replay on reconnection (**Zero event loss verified during simulated network disconnects**).
- **Cloud Verification Engine (`cloud/verification/`):** Cryptographic signature verification, schema conformance validation, and strict replay protection.
- **REST API Server (`cloud/api/app.py`):** Framework-neutral WSGI service exposing `/health`, `/verification/events`, `/maintenance/*`, and `/passport/*`.
- **MRO Web Dashboard (`dashboard/web/public/`):** Dark-mode operator interface with real-time gauges, 10 operational states, interactive repair flows, and simulated tamper injection testing.
- **Closed-Loop Maintenance Remediation:** Tracks maintenance in progress, fresh post-repair re-test, repair effectiveness calculation, and commits tamper-evident `ClosureRecord` into the Digital Passport.
- **Automated Test Suite:** **68 / 68 automated tests passing (100%)** across unit, security, integration, and e2e suites.

### PENDING (External Dependencies & Physical Hardware)
- **Physical HIL:** Microcontroller (ESP32) acquisition over serial stream reader, physical accelerometer, thermocouple, and rotating shaft test rig.
- **Live AWS Deployment:** Provisioning of AWS IoT Greengrass, AWS S3, Amazon Timestream, and AWS KMS in a live cloud account.

---

## 3. Quick Start & Execution Guide

### Prerequisites
- Python $\ge 3.11$ (verified on Python 3.14.5)
- Git

```powershell
# Clone and enter the repository
git clone https://github.com/kavindra-e-m/CyaplaneX.git
cd CyaplaneX

# Install development dependencies
py -3.14 -m pip install -e ".[dev]"
```

---

### Execution Modes

#### Mode 1: Full 20-Step Closed-Loop Demonstrator
Executes the continuous maintenance lifecycle script:
```powershell
py -3.14 scripts/e2e_demo.py
```

#### Mode 2: Interactive MRO Web Dashboard & REST API
Launches the local WSGI server:
```powershell
py -3.14 cloud/api/app.py
```
* **Dashboard:** [http://localhost:8000/](http://localhost:8000/)
* **Health Endpoint:** [http://localhost:8000/health](http://localhost:8000/health)

#### Mode 3: Edge Pipeline Diagnostic Cycle
Runs a single edge cycle (Sense $\to$ Trust $\to$ Preprocess $\to$ Predict $\to$ Sign $\to$ Dispatch):
```powershell
py -3.14 edge/main.py
```

#### Mode 4: Verify ML Acceptance Gate
Validates model artifacts against the 12-point acceptance gate:
```powershell
# Verify Production Gradient Boosted Model (Joblib)
py -3.14 scripts/verify_ml_artifact.py --module ml.export.model --class CyaplaneXProductionModel

# Verify Production Neural Network (ONNX)
py -3.14 scripts/verify_ml_artifact.py --module ml.export.onnx_model --class CyaplaneXONNXModel
```

#### Mode 5: Retrain & Evaluate ML Pipeline
```powershell
# 1. Download real CWRU benchmark files (.mat):
py -3.14 ml/data/download_cwru.py

# 2. Curate 5,000-sample balanced dataset:
py -3.14 -m ml.data.curate_dataset

# 3. Train Gradient Boosted Ensemble:
py -3.14 -m ml.training.train_model

# 4. Generate confusion matrix, feature importances, and audit report:
py -3.14 -m ml.evaluation.evaluate_model

# 5. Export compact ONNX model:
py -3.14 -m ml.export.export_onnx
```

#### Mode 6: Run Full Automated Test Suite
```powershell
py -3.14 -m pytest -v
```

---

## 4. Team Ownership Boundaries

| Team Member | Role | Codebase Boundary | Delivery Status |
|---|---|---|---|
| **Kavindra E.M.** | System Architect & Application Lead | `edge/**`, `cloud/**`, `dashboard/**`, `hardware/**`, `scripts/**`, `tests/**`, integration contracts | **COMPLETED & VERIFIED** |
| **Monhit Raju** | Machine Learning Lead | `ml/**` (data curation, feature engineering, training, evaluation, runtime model export) | **COMPLETED & VERIFIED** |

---

## 5. Repository Structure

```text
CyaplaneX/
├── cloud/                     # Local cloud verification, REST API, evidence store
│   ├── api/                   # WSGI endpoints (/health, /maintenance, /passport)
│   ├── storage/               # Thread-safe in-memory evidence store
│   └── verification/          # Signature & replay verification engine
├── dashboard/web/public/      # Operator MRO Web Dashboard (HTML5, Vanilla CSS, JS)
├── docs/                      # Architectural specifications (HLD, LLD, API, Contracts)
├── edge/                      # Edge-native runtime subsystems
│   ├── ai/                    # ML Adapter boundary & baseline demonstrator
│   ├── connectivity/          # Offline store-and-forward queue & MQTT mock transport
│   ├── maintenance/           # Maintenance reasoning & repair effectiveness
│   ├── preprocessing/         # 6-feature sliding window pipeline & SHA-256 hasher
│   ├── provenance/            # Manifest builder & HMAC-SHA256 signer
│   ├── sensor_trust/          # Range, freshness, stuck, drift, consensus engine
│   ├── sensors/               # Acquisition services (simulated & serial stream)
│   └── orchestrator.py        # Central closed-loop orchestrator
├── hardware/                  # ESP32 firmware sketch, pinout & testbed specifications
├── ml/                        # ML Subsystem (Owner: Monhit Raju)
│   ├── data/                  # Real CWRU downloader, raw .mat files, curated CSVs
│   ├── evaluation/            # Confusion matrix, feature importance, audit report
│   ├── export/                # Production model class & ONNX runtime exporter
│   ├── feature_engineering/   # Feature contract validator & FFT spectral defect analyzer
│   ├── models/                # Trained .joblib & .onnx model weights & metadata
│   ├── notebooks/             # Pre-rendered exploration & training Jupyter notebook
│   ├── preprocessing/         # CWRU raw waveform loader & window slicer
│   └── training/              # Model training workflows & cross-validation
├── scripts/                   # Verification gate, e2e demo, benchmarks
├── shared/                    # Draft 2020-12 JSON schemas & data contracts
└── tests/                     # 58 automated unit, security, integration, e2e tests
```

---

## 6. Disclaimer
This project is an engineering software demonstrator developed for **Tata Technologies InnoVent 2026**. It is not a flight-certified avionics system or certified airworthiness package.
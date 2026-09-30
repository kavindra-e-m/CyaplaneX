# CyaplaneX

**Tata Technologies InnoVent 2026**  
**Category:** Edge AI for Predictive Maintenance & Aircraft Health Monitoring  

> **CyaplaneX — Trusted Edge AI Predictive Maintenance & Maintenance Provenance**  
> *(Prototyped under the historical working title AeroTrust AI during initial scaffolding).*

---

## Problem and Solution
CyaplaneX validates sensor trust before inference, performs local health intelligence, explains maintenance decisions, signs evidence offline, synchronizes through cloud transport when available, verifies provenance, and closes the loop with repair-effectiveness testing.

Core flow: **Sense -> Validate -> Fuse -> Predict -> Explain -> Sign -> Sync -> Verify -> Maintain -> Re-test -> Close**.

### Current Project Status
> **"CyaplaneX local end-to-end software demonstrator completed and verified; physical HIL validation, trained ML artifact handoff and live AWS deployment remain pending."**

---

## Subsystem Implementation Breakdown

### COMPLETED (Implemented, Tested & Verified Locally)
- **Local Edge Pipeline:** End-to-end orchestrator (`edge/orchestrator.py`, `edge/main.py`) running continuous diagnostic cycles.
- **Sensor Trust:** Multi-check engine (`edge/sensor_trust/`) validating range, freshness, stuck status, drift, and consensus (`TRUSTED`, `DEGRADED`, `FAILED`).
- **Preprocessing:** Pipeline (`edge/preprocessing/`) computing statistical features (`vib_rms`, `vib_p2p`, `temp_mean`, `temp_max`, `rpm_mean`, `rpm_std`) and canonical SHA-256 window hash.
- **ML Adapter Boundary:** Decoupled `EdgeMLAdapter` interface with baseline demonstrator model awaiting Monhit's artifact.
- **Maintenance Reasoning:** Explainable engine generating maintenance priority (`P1`, `P2`, `P3`), failure reasoning, and actionable corrective steps.
- **Provenance:** Cryptographic manifest and event lineage generation linking sensor hashes, model metadata, and sequence IDs.
- **HMAC Signing:** **Device-local HMAC-SHA256 provenance signing for offline tamper-evidence demonstration.**
- **Offline Queue:** Store-and-forward queue with automatic replay on reconnection (**Zero event loss verified during the simulated network-disconnect test**).
- **Local Cloud Verification:** Signature verification, schema conformance validation, and strict replay protection.
- **API:** Framework-neutral WSGI REST service on port 8000 exposing verification, maintenance lifecycle, and digital passport endpoints.
- **Dashboard:** Interactive dark-mode MRO dashboard (`dashboard/web/public/`) with 10 operational states and 8 action flows.
- **Maintenance / Re-test / Closure Flow:** Closed-loop flow evaluating repair effectiveness and generating tamper-evident `ClosureRecord`.
- **Tests:** 47 automated tests passing across unit, security, integration, and end-to-end suites.

### PENDING (External Dependencies & Physical Validation)
- **Monhit Trained Artifact:** Production ML model training, evaluation metrics, and runtime export (`ml/models/`) pending handoff by Monhit Raju.
- **Physical HIL:** Microcontroller (ESP32) acquisition, physical vibration accelerometer, thermocouple, and rotating shaft test bench.
- **Live AWS Deployment:** Provisioning of AWS IoT Greengrass, AWS S3, Amazon Timestream, and AWS KMS in a live cloud environment.

---

## Infrastructure & AWS Deployment Status
- **IMPLEMENTED LOCALLY:** In-memory evidence store, local WSGI REST API server, cryptographic verifier, and offline synchronization coordinator.
- **TARGET AWS ARCHITECTURE:** Greengrass edge deployment, AWS IoT Core MQTT broker, Amazon S3 evidence archive, Amazon Timestream metrics, and AWS KMS key governance.
- **LIVE AWS DEPLOYMENT:** **PENDING / NOT DEPLOYED.** Local demonstrator does not require or communicate with live AWS cloud instances.

---

## Cryptography & Offline Guarantees
- **Signing Implementation:** Device-local HMAC-SHA256 provenance signing for offline tamper-evidence demonstration. It does not use asymmetric public/private keys, hardware HSMs, or flight-certified avionics cryptography.
- **Offline Retention:** Zero event loss verified during the simulated network-disconnect test. It does not guarantee recovery against sudden power loss, process termination, filesystem corruption, or storage media failure.

---

## Architecture
`Sensors -> Sensor Trust -> Preprocessing/Fusion -> Edge AI -> Maintenance Reasoning -> Local Provenance -> Offline Queue -> Cloud Verification -> Evidence Store -> MRO Dashboard`

## Team Roles
- **Kavindra E.M.** — Application architecture, edge pipeline, sensor trust integration, preprocessing, ML adapter boundary, maintenance reasoning, provenance, local HMAC signing, offline queue, verification API, storage, tests, and MRO dashboard.
- **Monhit Raju** — ML only (`ml/**`). Model training, feature engineering, evaluation, and export of production inference artifact.

## Disclaimer
This project is an engineering demonstrator developed for Tata Technologies InnoVent 2026. It is not an aircraft-certified system, airworthiness release, or flight-certified avionics package. Live AWS deployment and physical HIL testing remain future milestones.

.github/
  CODEOWNERS
  pull_request_template.md
  workflows/backend.yml
  workflows/frontend.yml
cloud/
  alerts/
  api/
  ingestion/
  infrastructure/github_actions/
  infrastructure/terraform/
  storage/
  verification/
dashboard/web/
  package.json
  public/
  src/components/
  src/hooks/
  src/pages/
  src/services/
  src/types/
  src/utils/
docs/
  HLD.md
  LLD.md
  API_SPEC.md
  DATA_CONTRACTS.md
  THREAT_MODEL.md
  TEST_PLAN.md
  DEMO_SCRIPT.md
  architecture/
edge/
  ai/
  config/
  connectivity/
  maintenance/
  preprocessing/
  provenance/
  sensor_trust/
  sensors/
  utils/
hardware/
  calibration/
  esp32/
  test-rig/
  wiring/
ml/
  data/
  evaluation/
  export/
  feature_engineering/
  models/
  notebooks/
  preprocessing/
  training/
scripts/
shared/
  constants/
  schemas/
tests/
  e2e/
  hardware/
  integration/
  security/
  unit/
README.md
CONTRIBUTING.md
LICENSE
.env.example
.gitignore
docker-compose.yml
pyproject.toml

Install and test:
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest
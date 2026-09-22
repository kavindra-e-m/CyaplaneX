# AeroTrust AI

Trusted closed-loop Edge AI predictive maintenance for aerospace engineering demonstrators.

## Problem and solution
AeroTrust AI validates sensor trust before inference, performs local health intelligence, explains maintenance decisions, signs evidence offline, synchronizes through AWS when available, verifies provenance, and closes the loop with repair-effectiveness testing.

Core flow: **Sense -> Validate -> Fuse -> Predict -> Explain -> Sign -> Sync -> Verify -> Maintain -> Re-test -> Close**.

This repository is a production-style scaffold. Feature implementations, model performance, aircraft certification, and operational suitability are intentionally not claimed.

## Architecture
`Sensors -> Sensor Trust -> Preprocessing/Fusion -> Edge AI -> Maintenance Reasoning -> Local Provenance -> Offline Queue -> AWS IoT -> S3/Timestream/KMS -> Verification API -> MRO Dashboard`

AWS path: Greengrass -> IoT Core -> S3 + Timestream + KMS -> Verification API -> Dashboard. DynamoDB, Lambda, API Gateway, EventBridge, SNS, SiteWise, Grafana, and TwinMaker are documented extension points only.

## Innovations
- Sensor trust signals are explicit evidence alongside model results.
- Local signing works offline and does not require a live KMS call.
- Sequence, timestamp, nonce, window hash, model metadata, and previous hash support cryptographically verifiable lineage.
- Repair effectiveness is part of the maintenance lifecycle.
- A component maintenance digital passport can be assembled from verified records.

## Technology stack
Python 3.11+, pytest, JSON Schema contracts, optional AWS SDK integrations, and a lightweight web dashboard placeholder. No cloud credentials or private keys are stored in this repository.

## Repository structure
- `hardware/`: ESP32 and test-rig boundaries
- `edge/`: acquisition, trust, inference, maintenance, provenance, and connectivity
- `ml/`: datasets, notebooks, training, evaluation, and export boundaries
- `cloud/`: ingestion, verification, APIs, storage, alerts, and infrastructure
- `dashboard/`: web UI placeholder and dashboard states
- `shared/schemas/`: versionable data contracts
- `tests/`: unit, integration, security, hardware, and end-to-end tests
- `docs/`: design, interfaces, threat model, tests, and demo guidance

## Team roles
Kavindra owns architecture, security, provenance, integration, contracts, and cloud verification. Dhakshatha owns hardware, sensors, and sensor trust. Monhit Raju owns ML, signal processing, health intelligence, and repair effectiveness. Hari owns AWS, backend, connectivity, and DevOps. Ashwarya owns dashboard, MRO workflow, QA, and demos.

## Build phases
1. Contracts and repository foundations.
2. Sensor acquisition and trust checks.
3. Edge preprocessing and model integration.
4. Local provenance and offline synchronization.
5. Cloud verification and dashboard workflow.
6. Closed-loop repair verification and digital passport.

## Demo cases
Healthy, warning, critical, sensor failure, offline buffering, provenance verified, provenance violation, maintenance required, repair verified, and re-inspection required are represented as dashboard states. Use `python scripts/seed_mock_data.py`, `python scripts/tamper_test.py`, and `python scripts/replay_test.py` for local demonstrations.

## Security principles
Never hardcode credentials or private keys. Sign events locally. Treat KMS as cloud-side key governance, not an online prerequisite for edge signing. Include sequence, timestamp, nonce, sensor-window hash, and model metadata in provenance. Use the terms tamper-evident and cryptographically verifiable.

## Development
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
pytest
```

For the optional dashboard: `cd dashboard/web; npm install; npm run check`. For local mock services, read `scripts/run_demo.sh` and `docker-compose.yml`.

## Disclaimer
This is an engineering demonstrator scaffold, not an aircraft-certified system, maintenance release, safety case, or substitute for qualified engineering and regulatory processes.

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
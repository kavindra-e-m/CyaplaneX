# CyaplaneX — Complete Folder Structure
*(Historical Reference: AeroTrust AI)*

This file is the folder/file map for `kavindra-e-m/CyaplaneX`.

It is intended to be given to Antigravity together with `AeroTrust_AI_README.md`.

## 1. Repository root

```text
CyaplaneX/
│
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── AeroTrust_AI_README.md
├── CONTRIBUTING.md
├── docker-compose.yml
├── pyproject.toml
│
├── .github/
│   ├── CODEOWNERS
│   ├── pull_request_template.md
│   └── workflows/
│       ├── backend.yml
│       └── frontend.yml
│
├── cloud/
├── dashboard/
├── docs/
├── edge/
├── hardware/
├── ml/
├── scripts/
├── shared/
└── tests/
```

---

# 2. Detailed tree

```text
CyaplaneX/
│
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── AeroTrust_AI_README.md
├── CONTRIBUTING.md
├── docker-compose.yml
├── pyproject.toml
│
├── .github/
│   ├── CODEOWNERS
│   ├── pull_request_template.md
│   │
│   └── workflows/
│       ├── backend.yml
│       └── frontend.yml
│
├── cloud/
│   │
│   ├── alerts/
│   │   └── [alerting implementations]
│   │
│   ├── api/
│   │   ├── health.py
│   │   ├── passport.py
│   │   └── verification.py
│   │
│   ├── ingestion/
│   │   └── [cloud event ingestion]
│   │
│   ├── infrastructure/
│   │   │
│   │   ├── github_actions/
│   │   │   └── [deployment/CI helpers]
│   │   │
│   │   └── terraform/
│   │       └── [AWS infrastructure definitions]
│   │
│   ├── storage/
│   │   ├── s3_handler.py
│   │   ├── timestream_handler.py
│   │   └── dynamodb_handler.py
│   │
│   └── verification/
│       ├── signature_verifier.py
│       └── replay_checker.py
│
├── dashboard/
│   │
│   └── web/
│       ├── package.json
│       │
│       ├── public/
│       │   └── [static assets]
│       │
│       └── src/
│           ├── components/
│           │   └── [dashboard components]
│           ├── hooks/
│           │   └── [frontend hooks]
│           ├── pages/
│           │   └── [dashboard pages]
│           ├── services/
│           │   └── [API/service clients]
│           ├── types/
│           │   ├── index.js
│           │   └── states.js
│           └── utils/
│               └── [frontend utilities]
│
├── docs/
│   ├── HLD.md
│   ├── LLD.md
│   ├── API_SPEC.md
│   ├── DATA_CONTRACTS.md
│   ├── THREAT_MODEL.md
│   ├── TEST_PLAN.md
│   ├── DEMO_SCRIPT.md
│   │
│   └── architecture/
│       └── [architecture diagrams/assets]
│
├── edge/
│   │
│   ├── ai/
│   │   ├── anomaly_model.py
│   │   ├── fault_classifier.py
│   │   └── health_engine.py
│   │
│   ├── config/
│   │   └── [edge configuration]
│   │
│   ├── connectivity/
│   │   ├── mqtt_client.py
│   │   ├── queue.py
│   │   └── sync.py
│   │
│   ├── main.py
│   │
│   ├── maintenance/
│   │   └── [maintenance reasoning]
│   │
│   ├── preprocessing/
│   │   └── [windowing / feature preparation]
│   │
│   ├── provenance/
│   │   ├── manifest.py
│   │   ├── hashing.py
│   │   ├── signer.py
│   │   └── chain.py
│   │
│   ├── sensor_trust/
│   │   └── [sensor trust implementation]
│   │
│   ├── sensors/
│   │   ├── vibration.py
│   │   ├── temperature.py
│   │   └── rpm.py
│   │
│   └── utils/
│       └── [edge utilities]
│
├── hardware/
│   │
│   ├── calibration/
│   │   └── [calibration data/tools]
│   │
│   ├── esp32/
│   │   └── src/
│   │       └── main.cpp
│   │
│   ├── test-rig/
│   │   └── [motor/shaft/bearing test-rig assets]
│   │
│   └── wiring/
│       └── [wiring diagrams/assets]
│
├── ml/
│   │
│   ├── data/
│   │   └── [datasets / dataset manifests]
│   │
│   ├── evaluation/
│   │   └── [evaluation code/reports]
│   │
│   ├── export/
│   │   └── [model export / optimization]
│   │
│   ├── feature_engineering/
│   │   └── [feature generation/selection]
│   │
│   ├── models/
│   │   └── [trained model artifacts / metadata]
│   │
│   ├── notebooks/
│   │   └── [experiments]
│   │
│   ├── preprocessing/
│   │   └── [ML preprocessing]
│   │
│   └── training/
│       └── [training pipelines]
│
├── scripts/
│   ├── seed_mock_data.py
│   ├── tamper_test.py
│   ├── replay_test.py
│   ├── run_demo.sh
│   └── [additional automation scripts]
│
├── shared/
│   │
│   ├── constants/
│   │   └── [shared constants]
│   │
│   └── schemas/
│       ├── sensor_sample.schema.json
│       ├── sensor_trust.schema.json
│       ├── health_result.schema.json
│       ├── maintenance_event.schema.json
│       └── closure_record.schema.json
│
└── tests/
    │
    ├── e2e/
    │   └── [end-to-end tests]
    │
    ├── hardware/
    │   └── [hardware tests]
    │
    ├── integration/
    │   └── [cross-module integration tests]
    │
    ├── security/
    │   └── [tamper/replay/provenance/security tests]
    │
    └── unit/
        └── [unit tests]
```

---

# 3. Ownership map

```text
KAVINDRA — APPLICATION
│
├── edge/
│   ├── sensors/
│   ├── sensor_trust/
│   ├── preprocessing/
│   ├── ai/
│   ├── maintenance/
│   ├── provenance/
│   ├── connectivity/
│   ├── config/
│   └── main.py
│
├── cloud/
│   ├── api/
│   ├── ingestion/
│   ├── verification/
│   ├── storage/
│   ├── alerts/
│   └── infrastructure/
│
├── dashboard/
├── hardware/
├── scripts/
├── tests/
└── integration / deployment / CI
```

```text
MONHIT RAJU — ML ONLY
│
└── ml/
    ├── data/
    ├── preprocessing/
    ├── feature_engineering/
    ├── training/
    ├── evaluation/
    ├── models/
    ├── export/
    └── notebooks/
```

---

# 4. Shared boundary

```text
shared/
└── schemas/
    ├── sensor_sample.schema.json
    ├── sensor_trust.schema.json
    ├── health_result.schema.json
    ├── maintenance_event.schema.json
    └── closure_record.schema.json
```

Shared schemas are the contract between:

```text
Sensors
  ↓
Edge
  ↓
ML Adapter
  ↓
Cloud
  ↓
Dashboard
```

A contract change must be reviewed by both teammates.

---

# 5. Runtime data flow mapped to folders

```text
1. SENSOR INPUT
   hardware/
   edge/sensors/

        ↓

2. SENSOR TRUST
   edge/sensor_trust/

        ↓

3. WINDOW / PREPROCESSING
   edge/preprocessing/

        ↓

4. ML
   ml/
        ↓
   edge/ai/

        ↓

5. MAINTENANCE REASONING
   edge/maintenance/

        ↓

6. PROVENANCE
   edge/provenance/

        ↓

7A. ONLINE
   edge/connectivity/
        ↓
   cloud/ingestion/
        ↓
   cloud/verification/
        ↓
   cloud/storage/

7B. OFFLINE
   edge/connectivity/queue.py
        ↓
   edge/connectivity/sync.py
        ↓
   cloud/ingestion/
        ↓
   cloud/verification/

        ↓

8. API
   cloud/api/

        ↓

9. DASHBOARD
   dashboard/web/

        ↓

10. MAINTENANCE / RETEST / CLOSURE
    edge/maintenance/
    cloud/api/
    shared/schemas/

        ↓

11. TESTS
    tests/unit/
    tests/integration/
    tests/security/
    tests/e2e/
```

---

# 6. Current known executable/scaffold files

These files are important starting points in the existing repository.

```text
edge/main.py
edge/ai/anomaly_model.py
edge/ai/fault_classifier.py
edge/ai/health_engine.py

edge/connectivity/mqtt_client.py
edge/connectivity/queue.py
edge/connectivity/sync.py

edge/provenance/manifest.py
edge/provenance/hashing.py
edge/provenance/signer.py
edge/provenance/chain.py

edge/sensors/vibration.py
edge/sensors/temperature.py
edge/sensors/rpm.py

cloud/api/health.py
cloud/api/passport.py
cloud/api/verification.py

cloud/verification/signature_verifier.py
cloud/verification/replay_checker.py

cloud/storage/s3_handler.py
cloud/storage/timestream_handler.py
cloud/storage/dynamodb_handler.py

dashboard/web/src/index.js
dashboard/web/src/types/index.js
dashboard/web/src/types/states.js

hardware/esp32/src/main.cpp

scripts/seed_mock_data.py
scripts/tamper_test.py
scripts/replay_test.py

shared/schemas/sensor_sample.schema.json
shared/schemas/sensor_trust.schema.json
shared/schemas/health_result.schema.json
shared/schemas/maintenance_event.schema.json
shared/schemas/closure_record.schema.json
```

---

# 7. Important implementation note

Some directories above are already present as scaffolding while their implementation may still be incomplete.

Do not delete the existing architecture simply because a folder contains placeholders.

Antigravity should:

1. inspect the existing file;
2. preserve useful scaffolding;
3. replace TODO/placeholder logic with tested implementation;
4. avoid changing shared contracts casually;
5. update documentation after implementation.

---

# 8. Target dependency direction

```text
hardware
   ↓
edge/sensors
   ↓
edge/sensor_trust
   ↓
edge/preprocessing
   ↓
edge/ai
   ↓
edge/maintenance
   ↓
edge/provenance
   ↓
edge/connectivity
   ↓
cloud/ingestion
   ↓
cloud/verification
   ↓
cloud/storage
   ↓
cloud/api
   ↓
dashboard
```

The ML boundary is:

```text
ml/
   ↓
stable inference adapter
   ↓
edge/ai/
```

The edge/application should consume the ML component through a stable interface rather than importing notebooks or training code.

---

# 9. Final folder-structure rule

The most important ownership rule is:

```text
MONHIT:
ml/**
    ↓
    deployment-ready artifact + stable inference contract
    ↓
KAVINDRA:
edge/ai/**
    ↓
complete application
```

and:

```text
Kavindra:
edge + cloud + dashboard + hardware + scripts + tests + deployment

Monhit:
ml
```

The folder structure, shared schemas, actual code and tests together define the implementation boundary.

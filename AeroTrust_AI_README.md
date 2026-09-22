# AeroTrust AI

> **Trusted Closed-Loop Edge Intelligence for Aerospace Predictive Maintenance**  
> **Sense → Validate → Fuse → Predict → Explain → Sign → Verify → Repair → Re-test → Close**

AeroTrust AI is an Edge AI-based predictive-maintenance platform for aerospace component health monitoring. It validates sensor reliability, performs local multi-sensor health inference, explains why maintenance is required, cryptographically secures the maintenance evidence, synchronizes securely with AWS, verifies provenance, and finally re-tests the component after maintenance to confirm that the repair was effective.

---

## 1. Problem Statement

Conventional predictive-maintenance systems often focus only on detecting a fault:

`Sensor → AI → Fault`

AeroTrust AI addresses a broader trust problem:

1. **Can the sensor data itself be trusted?**
2. **Can the AI detect and explain the fault locally?**
3. **Can the maintenance record be proven authentic and unmodified?**
4. **Can the system continue to work during cloud/network loss?**
5. **After maintenance, can we verify that the repair actually solved the problem?**

The project therefore creates a complete closed-loop maintenance workflow:

`Sense → Validate → Predict → Explain → Secure → Verify → Maintain → Re-test → Close`

---

## 2. Core Innovations

### 2.1 Sensor Trust Engine
Checks whether sensor data is reliable before AI inference.

- Range validation
- Freshness check
- Stuck-value detection
- Drift detection
- Cross-sensor consistency
- Calibration/version tracking

### 2.2 Multi-Sensor Edge AI
Combines vibration, temperature, RPM and other available evidence.

Outputs:

- Anomaly score
- Fault class
- Health score
- Severity
- Confidence
- Maintenance recommendation

### 2.3 Explainable Maintenance Intelligence
The system answers:

- What failed?
- Why does the system think it failed?
- How severe is the condition?
- Why is maintenance required?
- What should be inspected or repaired?

### 2.4 Cryptographic Provenance
Every maintenance event contains:

- Sensor-window hash
- Device ID
- Sequence number
- Timestamp
- Nonce
- Sensor trust status
- AI model ID/version
- Model hash
- Prediction
- Severity
- Maintenance reason
- Recommended action
- Previous-record hash
- Manifest hash
- Local digital signature

The edge device signs locally so event creation does **not** depend on a live AWS KMS call.

### 2.5 Offline-First Operation
During network loss:

- Sensors continue
- Sensor trust continues
- Edge AI continues
- Maintenance events continue
- Local signatures continue
- Events are buffered

When connectivity returns, pending signed records synchronize securely.

### 2.6 Closed-Loop Repair Verification
After maintenance:

- The same sensors monitor the component again
- New health score is calculated
- Pre-maintenance and post-maintenance states are compared
- Repair effectiveness is evaluated
- A signed closure record is created

### 2.7 Component Maintenance Digital Passport
Maintains the trusted lifecycle history of each monitored component:

`Installed → Healthy → Anomaly → Fault → Maintenance → Repair Verification → Closure`

---

## 3. Final System Architecture

```text
AEROSPACE COMPONENT / PROTOTYPE TESTBED
                |
                v
        SENSOR ACQUISITION
   Vibration + Temperature + RPM
                |
                v
        SENSOR TRUST ENGINE
 Range | Drift | Stuck | Freshness
                |
                v
       MULTI-SENSOR FUSION
                |
                v
            EDGE AI
 Anomaly | Fault | Health | Severity
                |
                v
     MAINTENANCE INTELLIGENCE
  Why? | Priority | Recommended Action
                |
                v
        PROVENANCE ENGINE
 Data Hash | Device ID | Model Version
 Sequence | Nonce | Previous Hash
                |
                v
       LOCAL DIGITAL SIGNATURE
                |
                v
         OFFLINE EVENT QUEUE
                |
          When Online
                |
                v
          AWS IoT Core
                |
        +-------+-------+
        |               |
        v               v
       S3          Amazon Timestream
        |               |
        +-------+-------+
                |
                v
       VERIFICATION ENGINE
 Signature | Replay | Hash | Lineage
                |
        +-------+-------+
        |               |
        v               v
     VERIFIED       VIOLATION
        |
        v
       MRO DASHBOARD
        |
        v
    MAINTENANCE ACTION
        |
        v
 POST-MAINTENANCE TEST
        |
        v
 REPAIR EFFECTIVENESS
        |
   +----+----+
   |         |
   v         v
RESTORED  RE-INSPECT
   |
   v
SIGNED CLOSURE RECORD
   |
   v
COMPONENT DIGITAL PASSPORT
```

---

## 4. Prototype Scope

The first physical prototype uses a controlled rotating-machinery testbed.

### Hardware

- Motor
- Shaft
- Bearing
- ESP32
- Raspberry Pi 5 or NVIDIA Jetson
- Vibration sensor
- Temperature sensor
- RPM sensor

### Prototype-to-Aerospace Mapping

| Prototype | Aerospace Analogue |
|---|---|
| Rotating shaft | Rotating aircraft subsystem |
| Bearing | Engine/accessory/rotating-component bearing |
| Vibration sensor | Condition-monitoring evidence |
| Temperature sensor | Thermal health indicator |
| RPM sensor | Operating-state parameter |
| Controlled imbalance | Fault/degradation surrogate |

The prototype is an **engineering demonstrator**, not an aircraft-certified system.

---

## 5. Detectable Prototype Conditions

### Core implemented conditions

- Healthy
- Bearing degradation / imbalance surrogate
- Overheating-like condition
- RPM anomaly
- Sensor disconnected
- Sensor stuck
- Sensor invalid/out of range
- Sensor drift-like behavior
- Cloud/network loss
- Tampered maintenance record
- Replayed old event
- Model/version mismatch
- Repair successful
- Repair ineffective

### Future / advanced structural-health extension

- Strain-based structural stress
- Acoustic/ultrasonic crack indication
- Composite delamination indication

These advanced conditions require appropriate sensors and must not be claimed as solved by the basic motor-bearing testbed.

---

## 6. Technology Stack

### Hardware

- ESP32
- Raspberry Pi 5 / NVIDIA Jetson
- Vibration sensor
- Temperature sensor
- RPM sensor
- Motor-bearing test rig

### Edge

- Python
- C/C++
- AWS IoT Greengrass
- MQTT
- Linux

### AI / ML

- NumPy
- Pandas
- Scikit-learn
- XGBoost / Random Forest / LightGBM
- Isolation Forest
- ONNX / TFLite if required for deployment

### Security

- SHA-256
- Digital signatures
- Device-specific local private key
- Secure element / TPM where practical
- Sequence numbers
- Nonces
- Replay protection
- Model/version provenance

### AWS

Core:

- AWS IoT Greengrass
- AWS IoT Core
- Amazon S3
- AWS KMS
- Amazon Timestream

Advanced:

- AWS Lambda
- API Gateway
- DynamoDB
- EventBridge
- SNS
- IoT SiteWise
- Managed Grafana
- IoT TwinMaker
- CloudWatch
- CloudTrail
- IAM

### Dashboard

- React / Next.js
- TypeScript
- Chart.js / Plotly
- REST APIs

### DevOps

- Git
- GitHub
- GitHub Actions
- Docker
- Terraform/CDK optional

---

# 7. Repository Structure

```text
aerotrust-ai/
|
+-- README.md
+-- LICENSE
+-- .gitignore
+-- .env.example
+-- docker-compose.yml
|
+-- docs/
|   +-- HLD.md
|   +-- LLD.md
|   +-- API_SPEC.md
|   +-- DATA_CONTRACTS.md
|   +-- THREAT_MODEL.md
|   +-- TEST_PLAN.md
|   +-- DEMO_SCRIPT.md
|   +-- architecture/
|       +-- hld.png
|       +-- lld.png
|       +-- workflow.png
|
+-- hardware/
|   +-- esp32/
|   |   +-- src/
|   |   +-- include/
|   |   +-- platformio.ini
|   +-- wiring/
|   +-- calibration/
|   +-- test-rig/
|
+-- edge/
|   +-- main.py
|   +-- config/config.yaml
|   +-- sensors/
|   +-- sensor_trust/
|   +-- preprocessing/
|   +-- ai/
|   +-- maintenance/
|   +-- provenance/
|   +-- connectivity/
|   +-- utils/
|
+-- ml/
|   +-- data/raw/
|   +-- data/processed/
|   +-- data/labels/
|   +-- notebooks/
|   +-- preprocessing/
|   +-- feature_engineering/
|   +-- training/
|   +-- evaluation/
|   +-- models/
|   +-- export/
|
+-- cloud/
|   +-- ingestion/
|   +-- verification/
|   +-- api/
|   +-- storage/
|   +-- alerts/
|   +-- infrastructure/
|
+-- dashboard/
|   +-- web/
|
+-- shared/
|   +-- schemas/
|   +-- constants/
|
+-- tests/
|   +-- unit/
|   +-- integration/
|   +-- security/
|   +-- hardware/
|   +-- e2e/
|
+-- scripts/
|
+-- .github/
    +-- workflows/
    +-- pull_request_template.md
    +-- ISSUE_TEMPLATE/
```

---

# 8. Team Ownership

## Kavindra — System Architecture, Security & Integration Lead

### Owns

```text
docs/HLD.md
docs/LLD.md
docs/API_SPEC.md
docs/DATA_CONTRACTS.md
docs/THREAT_MODEL.md
edge/provenance/
shared/schemas/
cloud/verification/
tests/security/
tests/integration/
```

### Responsibilities

- HLD / LLD
- Common schemas
- Architecture decisions
- Cryptographic provenance
- Local digital signing
- Hash chain
- Sequence/nonce/replay protection
- Verification engine
- Model/device provenance
- End-to-end integration
- Security review
- Release approval

---

## Dhakshatha — Hardware, Sensors & Sensor Trust Lead

### Owns

```text
hardware/
edge/sensors/
edge/sensor_trust/
tests/hardware/
```

### Responsibilities

- Motor-bearing test rig
- ESP32 firmware
- Vibration sensor
- Temperature sensor
- RPM sensor
- Calibration
- Sensor acquisition
- Range validation
- Freshness
- Stuck sensor detection
- Drift detection
- Sensor failure simulations
- Controlled fault conditions

---

## Monhit Raju — AI/ML & Health Intelligence Lead

### Owns

```text
ml/
edge/preprocessing/
edge/ai/
edge/maintenance/repair_effectiveness.py
tests/unit/ml/
```

### Responsibilities

- Dataset
- Preprocessing
- Feature extraction
- Multi-sensor fusion
- Anomaly detection
- Fault classification
- Health score
- Severity
- Confidence
- Model versioning
- Model hash
- Repair effectiveness
- ML metrics

---

## Hari — AWS, Backend & DevOps Lead

### Owns

```text
cloud/
edge/connectivity/
.github/
docker-compose.yml
.env.example
```

### Responsibilities

- Greengrass
- IoT Core
- MQTT cloud path
- S3
- Timestream
- KMS
- IAM
- Backend APIs
- Cloud ingestion
- Offline synchronization
- Alerts
- CI/CD
- Deployment
- Monitoring
- Digital Passport cloud storage

---

## Ashwarya — Dashboard, MRO Workflow & QA Lead

### Owns

```text
dashboard/
docs/DEMO_SCRIPT.md
docs/TEST_PLAN.md
tests/e2e/
```

### Responsibilities

- MRO dashboard
- Health visualization
- Sensor Trust UI
- Fault explanation
- Maintenance recommendation
- Priority visualization
- Provenance status
- Tamper/replay alerts
- Offline state
- Repair verification
- Component Digital Passport
- QA
- End-to-end demo flow

---

# 9. Development Order

## Phase 0 — Architecture Freeze

Owner: **Kavindra**

Freeze:

- Folder structure
- Data contracts
- API paths
- MQTT topics
- Naming conventions
- Git workflow

After this, everybody starts in parallel.

## Phase 1 — Parallel Development

- Dhakshatha: Sensors → ESP32 → Edge sensor stream
- Monhit: Preprocessing → Features → Model using mock/public data
- Hari: IoT Core → Storage → API using mock events
- Ashwarya: Dashboard using mock API JSON
- Kavindra: Provenance → Signer → Verifier using fake events

## Sequential Integration

```text
Dhakshatha
Sensor Stream
    ↓
Monhit
AI Pipeline
    ↓
Kavindra
Provenance + Signer
    ↓
Hari
AWS Sync + Storage + APIs
    ↓
Kavindra + Hari
Verification
    ↓
Ashwarya
Live Dashboard
    ↓
All Five
End-to-End Testing
```

---

# 10. Git Strategy

```text
main
 |
develop
 |
+-- feature/kavindra/provenance
+-- feature/dhakshatha/sensors
+-- feature/monhit/fault-classifier
+-- feature/hari/iot-ingestion
+-- feature/ashwarya/dashboard
```

### Before starting work

```bash
git switch develop
git pull --rebase origin develop
git switch -c feature/<name>/<module>
```

### Before PR

```bash
git fetch origin
git rebase origin/develop
```

### Push regularly

```bash
git add .
git commit -m "feat(module): concise description"
git push origin feature/<name>/<module>
```

Never push directly to `main`.

---

# 11. PR Rules

Every module follows:

```text
Feature Branch
     ↓
Local Tests
     ↓
Push
     ↓
Pull Request
     ↓
Review
     ↓
CI
     ↓
develop
```

Architecture/security changes require **Kavindra review**.

Cloud/security changes require **Kavindra + Hari**.

Sensor/data-contract changes require **Kavindra + Dhakshatha + Monhit**.

Dashboard/API changes require **Hari + Ashwarya**.

---

# 12. Daily Team Rhythm

### Start of day
Pull latest `develop`.

### During development
Work independently using mocks where needed.

### Mid-day
Push progress.

### End of day
Push latest state and report blockers.

### Daily integration window
Review PRs, merge into `develop`, run smoke tests.

---

# 13. Recommended Tags

```text
v0.1-sensors
v0.2-sensor-trust
v0.3-edge-ai
v0.4-provenance
v0.5-cloud
v0.6-dashboard
v0.7-closed-loop
v0.8-security-tests
v1.0-demo
```

---

# 14. Acceptance Checklist

- [ ] Healthy operation
- [ ] Bearing/imbalance anomaly
- [ ] Overheat-like condition
- [ ] Sensor disconnect
- [ ] Sensor stuck
- [ ] Sensor trust status
- [ ] Edge AI offline
- [ ] Maintenance reason
- [ ] Maintenance recommendation
- [ ] Local event signature
- [ ] Offline buffering
- [ ] Reconnect synchronization
- [ ] Valid event verification
- [ ] Tampered event rejection
- [ ] Replay rejection
- [ ] Model/version mismatch detection
- [ ] Dashboard states
- [ ] Post-maintenance re-test
- [ ] Repair effectiveness
- [ ] Re-inspection on failed repair
- [ ] Signed closure record
- [ ] Digital Passport update

---

# 15. Security Rules

- Never commit private signing keys
- Never commit AWS credentials
- Use `.env.example` only for placeholders
- Use IAM least privilege
- Local signing must work offline
- KMS is cloud-side governance, not offline signer
- Validate timestamp/sequence/nonce
- Include model/version provenance
- Log verification failures
- Use **tamper-evident**, not **tamper-proof**

---

# 16. Final Project Message

> **AeroTrust AI does not simply detect a component fault. It validates the sensor evidence, predicts and explains the degradation at the edge, cryptographically secures the maintenance decision, and verifies after maintenance that the repair actually restored component health.**

### Tagline

**Detect. Verify. Repair. Prove.**

---

# 17. Team

| Member | Role |
|---|---|
| Kavindra | Architecture, Security & Integration |
| Dhakshatha | Hardware, Sensors & Sensor Trust |
| Monhit Raju | AI/ML & Health Intelligence |
| Hari | AWS, Backend & DevOps |
| Ashwarya | Dashboard, MRO UX & QA |

---

# 18. Disclaimer

AeroTrust AI is currently an engineering research/prototype platform. It is not an aircraft-certified flight-critical system. Any real aerospace deployment would require appropriate hardware/software qualification, safety assessment, cybersecurity validation and compliance with applicable aviation regulations.

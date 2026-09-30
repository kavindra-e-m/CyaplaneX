# AeroTrust AI

**Tata Technologies InnoVent 2026 — Aerospace**  
**Category:** Edge AI for Predictive Maintenance & Aircraft Health Monitoring

> Trusted closed-loop Edge AI predictive maintenance with provenance-verified maintenance evidence.

---

## 1. Purpose of this README

This README is the **single source of truth for the AeroTrust AI implementation workflow**.

It is written for the two-person implementation team:

- **Kavindra E.M.** — full application EXCEPT ML
- **Monhit Raju** — ML ONLY

This document defines:

- the problem and solution architecture;
- HLD and LLD boundaries;
- module ownership;
- shared data contracts;
- the end-to-end system workflow;
- exact dashboard/button flows;
- online/offline behavior;
- provenance and security behavior;
- ML-to-application handoff;
- prompts for Monhit and Kavindra/Antigravity;
- Git workflow;
- validation gates;
- prototype mapping;
- Tata InnoVent demo sequence;
- PPT evidence extraction guidance;
- definition of done.

### Evidence rule

The repository state is always more authoritative than an old chat message.

Do **not** claim that a feature is complete until the implementation, tests, execution evidence, or measured result actually exists.

Do **not** invent:

- ML accuracy/F1/recall;
- latency or memory numbers;
- AWS deployments;
- hardware results;
- cryptographic guarantees;
- aircraft certification or operational approval.

---

# 2. Fixed team ownership

Only two members are implementing AeroTrust AI.

## 2.1 Kavindra E.M. — complete application EXCEPT ML

Kavindra owns:

- system architecture;
- repository integration;
- frontend/dashboard;
- backend/API;
- AWS integration;
- edge orchestration;
- sensor acquisition integration;
- sensor-trust integration;
- preprocessing/application-side feature wiring;
- ML runtime integration;
- maintenance reasoning;
- provenance/security;
- local signing integration;
- offline queue;
- synchronization;
- cloud ingestion;
- cloud verification;
- cloud storage adapters;
- CI/CD;
- testing;
- end-to-end integration;
- deployment;
- final completion in **Antigravity**.

Kavindra does **not** own ML model training, experimentation, evaluation, or model-development decisions.

## 2.2 Monhit Raju — ML ONLY

Monhit owns:

- dataset preparation;
- ML preprocessing;
- feature engineering;
- model experimentation;
- model selection;
- model training;
- model evaluation;
- model export/optimization;
- model metadata;
- ML-specific tests;
- stable ML inference adapter/interface;
- handoff of deployment-ready ML artifacts.

Monhit does **not** own:

- frontend;
- backend;
- AWS;
- provenance;
- dashboard;
- device orchestration;
- application workflow;
- final application integration.

## 2.3 Non-negotiable ownership boundary

`ml/` is Monhit's primary implementation boundary.

The following are Kavindra's application boundary:

`edge/`, `cloud/`, `dashboard/`, `hardware/`, `scripts/`, shared integration contracts, application tests, deployment and final end-to-end workflow.

If a model requires a change to a shared schema or application interface, Monhit proposes the change with documentation; **Kavindra owns the application-side integration**.

---

# 3. Problem statement

Predictive maintenance depends not only on an AI prediction but also on confidence that the underlying evidence is trustworthy.

A sensor can produce values that are out of range, stale, stuck, drifting, inconsistent with other sensors, replayed, or associated with the wrong model/version context. Connectivity can also disappear while the edge system is operating.

AeroTrust AI addresses this with a closed-loop architecture that:

1. validates sensor trust before inference;
2. performs Edge AI health/fault analysis;
3. attaches model and sensor provenance to the diagnostic result;
4. supports offline-first evidence handling;
5. verifies received evidence in the backend;
6. exposes evidence and maintenance state through an MRO-style dashboard;
7. performs a fresh post-maintenance re-test;
8. records repair effectiveness and closure history.

### Core lifecycle

**Sense → Validate → Fuse → Predict → Explain → Sign → Sync → Verify → Maintain → Re-test → Close**

---

# 4. Solution overview

AeroTrust AI is an engineering demonstrator that combines:

- sensor trust validation;
- Edge AI predictive-maintenance intelligence;
- evidence-linked maintenance reasoning;
- deterministic provenance;
- local/offline signing;
- offline queueing;
- cloud-side verification;
- maintenance workflow;
- post-maintenance re-test;
- repair-effectiveness evidence;
- component maintenance history / digital passport.

The system is intentionally designed so that **the AI prediction is only one part of the evidence chain**.

---

# 5. High-level architecture (HLD)

```text
                    +----------------------+
                    | Sensors / Test Rig   |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Sensor Acquisition   |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Sensor Trust Engine  |
                    | range / fresh / stuck|
                    | drift / consensus    |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Preprocessing /      |
                    | Feature Fusion       |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Edge ML Adapter      |
                    | anomaly / fault /    |
                    | health inference     |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Maintenance          |
                    | Reasoning            |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Provenance Engine    |
                    | canonical manifest   |
                    | hash + local sign    |
                    +----------+-----------+
                               |
                    +----------+----------+
                    |                     |
               ONLINE PATH           OFFLINE PATH
                    |                     |
                    v                     v
              AWS IoT             Local Queue
                    |                     |
                    +----------+----------+
                               |
                               v
                    +----------------------+
                    | Cloud Verification  |
                    | + Storage            |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | MRO Dashboard       |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Maintenance Action  |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Fresh Re-test       |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Repair Effectiveness|
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    | Closure / Passport  |
                    +----------------------+
```

---

# 6. AWS target architecture

## 6.1 Intended path

```text
Edge Runtime
    |
    +--> AWS IoT Greengrass / IoT Core
                    |
                    +--> S3
                    +--> Timestream
                    +--> Cloud verification layer
                    +--> KMS-governed cloud controls
                    |
                    +--> Verification API
                                  |
                                  v
                              Dashboard
```

## 6.2 Future/extension integrations

The repository already documents the following as possible extensions:

- DynamoDB
- Lambda
- API Gateway
- EventBridge
- SNS
- IoT SiteWise
- Amazon Managed Service for Grafana
- AWS IoT TwinMaker

These must be described as **future/extension components until actually implemented and deployed**.

## 6.3 Important key-management rule

Edge signing must not depend on a live cloud request.

AWS KMS is treated as cloud-side key-governance / protected-cloud support, not as an online prerequisite for every offline event signature.

Use:

- **tamper-evident**
- **cryptographically verifiable**

Do not use:

- tamper-proof
- unconditionally secure
- aircraft-certified
- production-ready cryptography

unless those claims are supported by actual evidence.

---

# 7. Low-level architecture (LLD)

## 7.1 Edge modules

| Directory | Responsibility | Owner |
|---|---|---|
| `edge/sensors/` | Sensor acquisition adapters | Kavindra |
| `edge/sensor_trust/` | Range/freshness/stuck/drift/consensus checks | Kavindra |
| `edge/preprocessing/` | Windowing and application-side preparation | Kavindra |
| `edge/ai/` | Stable runtime adapter calling Monhit model | Kavindra |
| `edge/maintenance/` | Health-to-maintenance reasoning | Kavindra |
| `edge/provenance/` | Manifest/hash/signing/chain metadata | Kavindra |
| `edge/connectivity/` | Transport/queue/synchronization | Kavindra |
| `edge/config/` | Runtime configuration | Kavindra |

## 7.2 ML modules

| Directory | Responsibility | Owner |
|---|---|---|
| `ml/data/` | Dataset curation/manifests | Monhit |
| `ml/preprocessing/` | ML-specific preprocessing | Monhit |
| `ml/feature_engineering/` | Feature creation/selection | Monhit |
| `ml/training/` | Training workflows | Monhit |
| `ml/evaluation/` | Evaluation and reports | Monhit |
| `ml/models/` | Model artifacts/metadata | Monhit |
| `ml/export/` | Deployment/export pipeline | Monhit |
| `ml/notebooks/` | Experiments and analysis | Monhit |

## 7.3 Cloud modules

| Directory | Responsibility | Owner |
|---|---|---|
| `cloud/ingestion/` | Incoming event processing | Kavindra |
| `cloud/verification/` | Provenance/signature/replay verification | Kavindra |
| `cloud/api/` | Application API | Kavindra |
| `cloud/storage/` | S3/Timestream/DynamoDB boundaries | Kavindra |
| `cloud/alerts/` | Alerting/notifications | Kavindra |
| `cloud/infrastructure/` | Infrastructure/deployment definitions | Kavindra |

## 7.4 Dashboard rule

Dashboard components consume API-shaped records.

The dashboard must **not**:

- implement cryptographic signing;
- decide whether a sensor is trusted;
- modify immutable diagnostic evidence;
- silently rewrite a maintenance decision;
- replace backend verification logic.

---

# 8. Shared data contracts

Schemas live in:

`shared/schemas/`

Current contract families:

- `sensor_sample.schema.json`
- `sensor_trust.schema.json`
- `health_result.schema.json`
- `maintenance_event.schema.json`
- `closure_record.schema.json`

## 8.1 SensorSample

Current required fields include:

- `device_id`
- `sensor_id`
- `timestamp`
- `sequence`
- `sensor_type`
- `value`
- `unit`
- `calibration_version`

## 8.2 SensorTrustResult

Represents:

- `TRUSTED`
- `DEGRADED`
- `FAILED`

and includes fields such as:

- `range_valid`
- `fresh`
- `stuck`
- `drift_suspected`
- `consensus_score`

## 8.3 HealthResult

The application contract contains:

- `condition`
- `anomaly_score`
- `health_score`
- `confidence`
- `severity`
- `model_id`
- `model_version`
- `model_hash`

Severity values are defined by the existing schema as:

- `HEALTHY`
- `WARNING`
- `CRITICAL`

## 8.4 MaintenanceEvent

The maintenance event links:

- report ID;
- asset ID;
- component ID;
- sensor-window hash;
- sensor trust;
- health result;
- maintenance reason;
- recommended action;
- priority;
- device ID;
- sequence number;
- nonce;
- timestamp;
- previous-record hash;
- manifest hash;
- digital signature.

## 8.5 ClosureRecord

Closure contains:

- closure ID;
- report ID;
- maintenance action;
- pre-health score;
- post-health score;
- repair effectiveness;
- closure status;
- timestamp;
- digital signature.

## 8.6 Contract-change rule

A contract change is never considered a private change to one person's code.

It requires:

1. schema update;
2. compatibility review;
3. edge impact review;
4. cloud/API impact review;
5. dashboard impact review;
6. test update;
7. documentation update;
8. focused commit.

---

# 9. Exact end-to-end workflow

## Step 1 — Device/application boot

1. Device/runtime starts.
2. Runtime configuration is loaded.
3. Sensor adapters initialize.
4. Expected ML artifact/metadata is checked.
5. Local provenance state is initialized.
6. Connectivity state is checked.

### Output

A ready runtime with known sensor/model/configuration state.

---

## Step 2 — Sensor acquisition

1. Sensors generate samples.
2. Each sample receives:
   - device ID;
   - sensor ID;
   - timestamp;
   - sequence;
   - sensor type;
   - value;
   - unit;
   - calibration version.
3. Samples are grouped into a processing window.

### Output

A timestamped sensor window.

---

## Step 3 — Sensor trust validation

For the relevant window, run the applicable trust checks:

- range;
- freshness;
- stuck-value;
- drift suspicion;
- cross-sensor consistency/consensus.

The trust result becomes explicit evidence.

### Possible state

- TRUSTED
- DEGRADED
- FAILED

### Rule

A failed sensor must not silently become a normal input to downstream maintenance reasoning.

---

# 10. Step 4 — Preprocessing / feature preparation

The application prepares the exact representation expected by the ML integration contract.

The preprocessing boundary must be explicit about:

- feature names;
- feature order;
- units;
- expected ranges;
- normalization/scaling;
- window length;
- missing-value handling;
- model input format.

### Critical rule

**Do not invent or reorder ML features in the application after Monhit has delivered the model contract.**

---

# 11. Step 5 — ML inference

1. Kavindra's application invokes the stable ML adapter.
2. The adapter loads/uses Monhit's exported model.
3. The model returns the declared inference output.
4. The application normalizes the result into `HealthResult`.
5. The result includes model ID/version/hash.

### Ownership boundary

At this point:

**Monhit's ML work ends.**

Everything around inference, including maintenance reasoning, provenance, cloud transport, dashboard behavior and final workflow is Kavindra's responsibility.

---

# 12. Step 6 — Maintenance reasoning

The application combines:

- sensor trust;
- health result;
- severity;
- asset/component context;
- configured engineering rules.

The application produces:

- maintenance reason;
- recommended action;
- priority;
- evidence references.

No unsupported statement may be converted into an aircraft maintenance release or safety conclusion.

---

# 13. Step 7 — Provenance creation

The application creates a canonical evidence manifest.

The manifest may contain:

- report ID;
- asset ID;
- component ID;
- sensor-window hash;
- sensor-trust result;
- health result;
- model ID;
- model version;
- model hash;
- device ID;
- sequence number;
- timestamp;
- nonce;
- previous-record hash;
- manifest hash.

The canonical representation must be deterministic.

### Existing repository capability

The current scaffold already contains deterministic canonical JSON hashing using SHA-256.

### Signing rule

The final system should use a **device-local signing mechanism** so offline operation does not require a live cloud/KMS call.

---

# 14. Step 8 — Connectivity branching

## 14.1 Online path

```text
Signed Event
   ↓
Cloud Transport
   ↓
Cloud Ingestion
   ↓
Schema Validation
   ↓
Replay / Sequence Check
   ↓
Provenance / Signature Verification
   ↓
Persistence
   ↓
Dashboard
```

## 14.2 Offline path

```text
Signed Event
   ↓
Local Queue
   ↓
OFFLINE BUFFERING
   ↓
Connectivity Restored
   ↓
Queue Drain
   ↓
Cloud Validation
   ↓
Cloud Verification
   ↓
Persistence
   ↓
Dashboard
```

### Offline guarantees to implement

- no silent loss;
- no dependency on live KMS for local signing;
- queue visibility;
- controlled synchronization;
- verification before treating synced records as trusted cloud evidence.

---

# 15. Step 9 — Verification

Cloud-side verification should check the implemented rules for:

- contract structure;
- manifest integrity;
- signature validity;
- sequence/replay rules;
- previous-record linkage;
- model metadata consistency.

### Dashboard outcomes

**PROVENANCE VERIFIED**

or

**PROVENANCE VIOLATION**

A failed verification result must remain visible and must not silently become a healthy state.

---

# 16. Step 10 — Maintenance workflow

When the system reaches a maintenance-required state:

1. user selects the asset;
2. diagnostic evidence is opened;
3. provenance is verified;
4. maintenance is started;
5. physical/prototype maintenance action is performed.

The original diagnostic event must remain unchanged.

---

# 17. Step 11 — Re-test and repair effectiveness

1. User starts a fresh re-test.
2. New sensor samples are captured.
3. Sensor trust is recalculated.
4. The ML pipeline is rerun.
5. Post-maintenance health is produced.
6. Pre/post results are compared.
7. Repair effectiveness is calculated according to the implemented rule.

Possible application states:

- `REPAIR VERIFIED`
- `RE-INSPECTION REQUIRED`

---

# 18. Step 12 — Closure

1. User reviews the re-test.
2. Application creates the closure record.
3. The closure record receives the required provenance/signature handling.
4. Verified maintenance history is updated.
5. Component passport/history can show the complete lifecycle.

### Closed-loop concept

```text
Prediction
   ↓
Maintenance
   ↓
Re-test
   ↓
Repair effectiveness
   ↓
Closure
   ↓
Component history
```

---

# 19. Dashboard target UX and exact button behavior

These are **implementation targets**, not claims that every button already exists in the current scaffold.

## 19.1 Dashboard home

Display:

- asset;
- component;
- health score;
- confidence;
- severity;
- fault/condition;
- sensor trust;
- connectivity;
- provenance status;
- maintenance status;
- latest update time.

---

## 19.2 Button — Open Asset

### Action

1. Load selected asset/component.
2. Fetch latest health record.
3. Fetch latest provenance state.
4. Load current maintenance state.

### Prompt

> Asset selected. Review the latest health result, sensor trust state, and provenance status before taking maintenance action.

---

## 19.3 Button — View Diagnostic

### Action

1. Open diagnostic record.
2. Display sensor evidence.
3. Display model ID/version/hash.
4. Display maintenance reason/action.
5. Display timestamps and sequence information.

### Prompt

> Diagnostic evidence loaded. Confirm that the sensor window, model metadata, and maintenance recommendation correspond to the same report.

---

## 19.4 Button — Verify Provenance

### Action

1. Call the verification endpoint.
2. Validate event structure.
3. Verify integrity/signature.
4. Check replay/sequence rules.
5. Render verification status.

### Success

> Provenance verified. The available event evidence is consistent with the verification rules.

### Failure

> Provenance verification failed. Do not treat this record as verified evidence until the violation is investigated.

---

## 19.5 Button — Run Tamper Test

### Demo-only action

1. Select a known-good event.
2. Modify one protected field.
3. Re-run verification.
4. Show verification failure.

### Prompt

> Demo tamper test prepared. One protected event value will be changed to demonstrate detection. Continue?

### Expected result

Modified evidence is rejected by verification.

---

## 19.6 Button — Simulate Offline

### Demo-only action

1. Route around cloud connectivity.
2. Generate a new event.
3. Sign locally.
4. Add to local queue.
5. Display queue depth.

### Prompt

> Offline mode enabled. New signed events will remain locally buffered until connectivity is restored.

---

## 19.7 Button — Restore Connectivity

### Action

1. Restore connectivity.
2. Detect buffered records.
3. Send records in controlled sequence.
4. Verify successful synchronization.
5. Update queue depth/status.

### Prompt

> Connectivity restored. Synchronizing buffered evidence in sequence.

---

## 19.8 Button — Mark Maintenance Started

### Action

1. Require a selected report.
2. Record maintenance-start state.
3. Preserve the original diagnostic event unchanged.

### Prompt

> Maintenance started for this report. The original diagnostic evidence will remain unchanged.

---

## 19.9 Button — Start Re-test

### Action

1. Acquire a fresh sensor window.
2. Run sensor trust.
3. Run the ML adapter.
4. Generate post-maintenance health.
5. Compare against the pre-maintenance state.

### Prompt

> Re-test started. Collecting a fresh sensor window and running the post-maintenance verification path.

---

## 19.10 Result — Repair Verified

> Post-maintenance evidence meets the configured repair-verification rule. Closure record can be created.

---

## 19.11 Result — Re-inspection Required

> Post-maintenance evidence did not meet the configured closure rule. Keep the case open for further inspection.

---

# 20. ML handoff contract — Monhit → Kavindra

Monhit's handoff is complete only when the following are available.

## Required

1. trained model artifact;
2. model format;
3. runtime requirement;
4. exact feature names;
5. exact feature order;
6. preprocessing assumptions;
7. input schema;
8. output schema;
9. output ranges;
10. model ID;
11. model version;
12. model hash/checksum;
13. evaluation report;
14. known limitations;
15. ML-specific tests;
16. stable inference adapter;
17. deterministic integration example;
18. exact branch and commit.

## Why this matters

Kavindra must be able to integrate the model without opening or depending on a notebook.

---

# 21. Exact prompt for Monhit Raju

Copy the following into Monhit's ML work session:

```text
You are responsible ONLY for the ML component of AeroTrust AI.

Do NOT implement the frontend, backend, AWS integration, dashboard, provenance system, device orchestration, maintenance workflow, or final application integration.

Your responsibilities:
1. Prepare and document the dataset.
2. Perform ML-specific preprocessing.
3. Perform feature engineering.
4. Train candidate anomaly/fault/health models.
5. Evaluate them reproducibly.
6. Select the model using measured evidence only.
7. Export a deployment-ready model artifact.
8. Define the exact input feature contract, including names, order, units and preprocessing assumptions.
9. Define the exact output contract.
10. Create model_id, model_version and model_hash.
11. Provide a stable inference adapter/callable interface for Kavindra.
12. Add ML-specific tests.
13. Commit the artifact, adapter, metadata, evaluation evidence and documentation under the ml/ boundary.

NEVER fabricate:
- accuracy;
- F1;
- precision;
- recall;
- latency;
- memory use;
- benchmark values.

The final handoff must contain:
- artifact path;
- model format/runtime;
- input schema;
- output schema;
- preprocessing contract;
- model ID;
- model version;
- model hash/checksum;
- measured evaluation results;
- known limitations;
- deterministic integration example;
- exact branch and commit.

Keep shared contracts stable. If a schema or application interface must change, document the requested change for Kavindra to review.

The ML component is complete only when Kavindra can integrate the artifact without relying on notebooks.
```

---

# 22. Exact prompt for Kavindra / Antigravity

Copy the following into the Antigravity implementation session:

```text
You are responsible for the COMPLETE AeroTrust AI application EXCEPT ML training/model-development.

Use the repository README as the source of truth.

TEAM OWNERSHIP:
- Kavindra: everything except ML.
- Monhit Raju: ML only.

Kavindra owns:
frontend, backend/API, AWS integration, edge orchestration, sensor trust, application preprocessing wiring, ML runtime integration, maintenance reasoning, provenance/security, local signing integration, offline queue/synchronization, cloud ingestion, cloud verification, storage adapters, tests, CI/CD, deployment and final integration.

Implement in this order:

1. Inspect the repository and all current TODOs/placeholders.
2. Preserve existing shared schemas unless a real contract change is required.
3. Version/document every contract change.
4. Implement sensor acquisition boundaries.
5. Implement sensor-trust validation.
6. Implement application-side preprocessing/windowing.
7. Implement the stable ML adapter boundary.
8. Integrate Monhit's exported ML artifact using the documented ML handoff.
9. Implement maintenance reasoning.
10. Implement deterministic provenance manifest generation.
11. Implement actual local signing using an appropriate device-local mechanism.
12. Implement offline queue behavior.
13. Implement online synchronization.
14. Implement cloud ingestion/validation.
15. Implement replay/sequence verification.
16. Implement provenance/signature verification.
17. Implement cloud storage adapters.
18. Implement verification and maintenance APIs.
19. Implement dashboard states and target button flows.
20. Implement tamper/replay demonstrations.
21. Implement maintenance-start workflow.
22. Implement fresh re-test.
23. Implement repair-effectiveness calculation according to the implemented rule.
24. Implement closure record and maintenance history/passport.
25. Add unit/integration/security/e2e tests for every completed gate.
26. Run CI and local tests.
27. Record real execution evidence.
28. Update README/docs only after the implementation and tests support the claims.

Do NOT fabricate:
- ML metrics;
- cloud deployment status;
- hardware results;
- aircraft certification;
- safety approval;
- production cryptographic status;
- operational readiness.

At every milestone:
- show changed files;
- run relevant tests;
- report measured output;
- preserve unresolved TODOs;
- use small auditable commits.

FINAL ACCEPTANCE:
The application must provide one reproducible demo from controlled sensor/test-rig input through sensor trust, ML inference, maintenance reasoning, provenance, local signing, offline/online behavior, backend verification, dashboard review, maintenance start, fresh re-test, repair effectiveness and closure.
```

---

# 23. Git workflow

## Branches

```text
main
develop                # optional integration branch
feature/kavindra-*
feature/monhit-*
```

## Suggested commit style

```text
feat(edge): add sensor trust aggregation
feat(api): add provenance verification endpoint
feat(dashboard): add maintenance retest flow
feat(ml): export health model adapter
test(security): add replay rejection case
docs: update ML integration contract
```

## Rules

- Do not mix unrelated ML and application work.
- Monhit owns the ML commit.
- Kavindra owns integration of the ML artifact into the application.
- A model file in Git does not mean inference integration is complete.
- Every meaningful feature should have corresponding tests.
- Main should remain reproducible and demo-ready.

---

# 24. Validation gates

## Gate A — Contracts

Pass when:

- schemas load;
- required fields are understood;
- sample payloads validate;
- versions are consistent.

## Gate B — Sensor trust

Pass when:

- range checking works;
- freshness checking works;
- stuck detection has tests;
- trust states are represented correctly.

## Gate C — ML integration

Pass when:

- model artifact loads;
- runtime requirements are satisfied;
- feature order matches;
- preprocessing matches;
- output maps to `HealthResult`;
- metadata/hash is present;
- deterministic smoke test passes.

## Gate D — Provenance

Pass when:

- canonical hashing is deterministic;
- protected-field modification changes protected evidence;
- replay is rejected according to the implemented sequence rules;
- modified evidence is detected;
- actual signing exists before claiming signature verification.

## Gate E — Offline-first

Pass when:

- events can be generated and signed offline;
- events are stored locally;
- no event is silently discarded;
- queue depth is visible;
- restoration synchronizes buffered events;
- cloud verification runs after synchronization.

## Gate F — Dashboard

Pass when:

- health state is visible;
- sensor trust is visible;
- provenance state is visible;
- maintenance actions are visible;
- re-test is visible;
- closure state is visible.

## Gate G — Closed loop

Pass when:

**diagnosis → maintenance → re-test → repair effectiveness → closure**

can be reproduced with actual application records.

---

# 25. Current repository scaffold — verified structure vs future implementation

The current repository contains useful scaffolding and contracts, including:

- deterministic canonical SHA-256 hashing;
- sensor range/stuck checks;
- `HealthResult` serialization/value-object logic;
- replay sequence checking;
- API health smoke behavior;
- JSON Schema contracts;
- dashboard state definitions;
- demo/test scripts;
- CI workflows.

The current scaffold also contains explicit placeholders/TODOs for areas such as:

- production local signing;
- MQTT/cloud transport;
- cloud storage;
- complete inference orchestration;
- complete dashboard wiring;
- real hardware acquisition;
- complete end-to-end workflow integration.

This distinction must be preserved in all PPTs and demos.

---

# 26. Prototype hardware mapping

The intended engineering testbed can use:

- vibration sensor;
- temperature sensor;
- RPM sensor;
- motor/shaft/bearing assembly;
- ESP32-class acquisition/control hardware;
- Raspberry Pi 5 or equivalent edge compute.

## Example prototype conditions

- healthy operation;
- vibration increase;
- temperature increase;
- sensor failure;
- stuck sensor;
- intermittent/disconnected sensor;
- offline operation;
- tampered diagnostic evidence;
- maintenance action;
- post-maintenance re-test.

These represent **prototype engineering demonstrations**, not aircraft validation.

---

# 27. Security principles

1. Never hardcode AWS credentials.
2. Never commit private signing keys.
3. Keep edge signing independent of live cloud connectivity.
4. Bind provenance to the relevant sensor window.
5. Bind provenance to model identity/version/hash.
6. Use sequence, timestamp and nonce for replay/timeline evidence.
7. Verify evidence server-side.
8. Preserve original diagnostic records.
9. Use least-privilege cloud access.
10. Keep cryptographic implementation details documented and testable.
11. Document key rotation and incident-response procedures before any production claim.
12. Use “tamper-evident” and “cryptographically verifiable” unless stronger evidence exists.

---

# 28. API target

## Current scaffold endpoint

```text
GET /health
```

## Target endpoints

```text
POST /verification/events
GET  /verification/{report_id}
GET  /maintenance/{asset_id}
GET  /passport/{component_id}
```

The exact production authentication, framework, pagination, versioning and error envelope remain implementation decisions unless already committed in the repository.

---

# 29. Tata Technologies InnoVent demo sequence

The final demo should tell one continuous story.

```text
1. Start the system
        ↓
2. Show healthy input
        ↓
3. Inject a controlled prototype fault
        ↓
4. Show sensor trust
        ↓
5. Show Edge AI prediction
        ↓
6. Show maintenance reasoning
        ↓
7. Show provenance metadata
        ↓
8. Verify Provenance
        ↓
9. Run Tamper Test
        ↓
10. Simulate Offline
        ↓
11. Generate evidence
        ↓
12. Show OFFLINE BUFFERING
        ↓
13. Restore Connectivity
        ↓
14. Show synchronized verification
        ↓
15. Mark Maintenance Started
        ↓
16. Perform prototype maintenance
        ↓
17. Start Re-test
        ↓
18. Show post-maintenance evidence
        ↓
19. Show Repair Verified OR Re-inspection Required
        ↓
20. Show maintenance history/passport
```

Every result displayed in the final PPT or demo should come from actual execution evidence.

---

# 30. PPT evidence map

The PPT can extract implementation evidence from this repository.

| PPT section | Repository evidence |
|---|---|
| Introduction | Problem + solution sections |
| Problem statement | Problem statement |
| Market/future | External cited research, not invented repository numbers |
| Objective & approach | Core lifecycle + HLD |
| Solution overview | HLD + LLD |
| Novelty | Sensor trust + provenance + offline-first + closed loop |
| Challenges | Sensor quality, edge constraints, offline operation, key management, ML deployment |
| Technical implementation | HLD + LLD + contracts + source code |
| Results | Only actual measurements |
| Demo | Demo script + actual execution |
| Future enhancements | AWS/IoT TwinMaker/SiteWise/Grafana, stronger key management, richer HIL/datasets |
| Project plan | Actual implementation milestones |

---

# 31. What counts as a result

A result may be included in the PPT only when it is backed by one of:

- an executed test;
- an actual benchmark;
- a real model evaluation report;
- an actual hardware experiment;
- an actual cloud integration;
- an actual captured system output.

Do not create a result merely because the architecture predicts that it should occur.

---

# 32. Definition of Done

AeroTrust AI is not application-complete until the following chain is reproducible:

```text
Sensor/Test-rig input
        ↓
Sensor trust validation
        ↓
Preprocessing / feature contract
        ↓
Monhit ML inference
        ↓
Maintenance reasoning
        ↓
Provenance creation
        ↓
Local signing
        ↓
Offline queue OR cloud sync
        ↓
Backend verification
        ↓
Dashboard evidence review
        ↓
Maintenance start
        ↓
Fresh re-test
        ↓
Repair effectiveness
        ↓
Closure record
        ↓
Component maintenance history
```

And the repository must contain:

- working implementation;
- shared schemas;
- tests;
- reproducible demo commands;
- measured ML evaluation evidence;
- deployment/configuration documentation;
- current ownership information;
- actual integration/handoff evidence.

---

# 33. Final project rule

## Monhit Raju

**Build and hand off the ML component.**

## Kavindra E.M.

**Build and complete everything around the ML component.**

The source of truth is:

1. repository code;
2. shared schemas;
3. tests;
4. execution evidence;
5. this README.

Old conversations must not override a newer verified repository state.

---

# 34. Disclaimer

AeroTrust AI is an engineering demonstrator/prototype.

It is **not**:

- an aircraft-certified system;
- a maintenance release;
- a safety case;
- a regulatory approval;
- a substitute for qualified MRO engineering;
- a claim of operational aircraft deployment.

All aerospace claims must be supported by actual engineering evidence and presented within the scope of the prototype.

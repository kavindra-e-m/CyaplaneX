# CyaplaneX — Final Competition Slide Content & Deck Architecture

**Competition:** Tata Technologies InnoVent 2026  
**Category:** Edge AI for Predictive Maintenance & Aircraft Health Monitoring  
**Verification Standard:** Strictly Empirical Facts Only (Zero Fabrication)  
**Document Classification:** Competition Slide Deck Script & Content Architecture  

---

## Visual Narrative Arc

```
[1. PROBLEM]
Sensor uncertainty + Disconnected maintenance evidence + Open-loop unverified repairs
       │
       ▼
[2. SOLUTION]
CyaplaneX: Decoupled Edge AI Predictive Maintenance with Cryptographic Provenance
       │
       ▼
[3. EDGE INTELLIGENCE]
Sensor Trust Gating ──> Feature Extraction ──> Production ML ──> Maintenance Reasoning
       │
       ▼
[4. TRUSTED EVIDENCE]
Canonical Telemetry Hash ──> Model Artifact Binding ──> HMAC-SHA256 Signing ──> Independent Verifier
       │
       ▼
[5. OPERATIONAL RESILIENCE]
Autonomous Disconnected Operation ──> Bounded FIFO Buffering ──> Lossless In-Order Synchronization
       │
       ▼
[6. CLOSED-LOOP MRO]
Degraded Diagnosis ──> Mechanical Repair ──> Fresh Telemetry Re-test ──> Digital Passport Ledger
```

---

## Slide 1: Introduction & Project Identity

### Title
**CyaplaneX: Trusted Edge AI for Aircraft Predictive Maintenance**  
*Closing the Trust and Traceability Gap with Cryptographic Provenance & Verifiable MRO Lifecycle*

### Key Content Points
- **Category:** Edge AI for Predictive Maintenance & Aircraft Health Monitoring (Tata Technologies InnoVent 2026).
- **Core Value Proposition:** An autonomous, fail-closed edge intelligence pipeline combining physics-informed machine learning with cryptographic provenance and closed-loop post-repair verification.
- **Team Identity:**
  - **Kavindra E.M.** — System Architecture, Edge Runtime, Cloud Verification, Security & Integration
  - **Monhit Raju** — Machine Learning Architecture, Training, Optimization & Artifact Export
- **Software Baseline:** Canonical, frozen repository baseline (Commit `3414799`, 68/68 tests passing, 0 lint errors, 12/12 ML acceptance gate).

---

## Slide 2: Problem Statement

### Title
**The Aircraft Predictive Maintenance Dilemma: Black Boxes, Sensor Drift & Open Loops**

### Key Content Points
1. **Uncalibrated Sensor Drift & False Alarms:** Existing onboard monitoring algorithms blindly ingest raw sensor streams. Drift, noisy spikes, or stuck transducers trigger false maintenance removals, costing airlines billions in No-Fault-Found (NFF) delays.
2. **Untrusted Diagnostic Lineage:** Current predictive maintenance software emits opaque health scores without verifiable cryptographic lineage. Flight-line mechanics cannot prove which model version diagnosed an asset or whether telemetry was tampered with in transit.
3. **Open-Loop Maintenance:** Traditional MRO closes work orders via clerical sign-offs without objective, sensor-driven verification that the mechanical repair actually restored system health.
4. **Intermittent Flight-Line Connectivity:** Hangar and remote field deployments lack constant cloud connectivity, causing data dropouts and out-of-order event synchronization.

---

## Slide 3: Market & Future Need

### Title
**Aerospace MRO Transformation: The Trillion-Dollar Move to Verifiable Edge Intelligence**

### Key Content Points
- **Market Dynamics:** Commercial aviation MRO expenditure is projected to surpass $120B annually, with unscheduled maintenance and grounded aircraft (AOG) costing up to $150,000/hour.
- **Regulatory Pressure (Civil Aviation):** Aviation safety authorities (FAA, EASA, DGCA) increasingly mandate end-to-end data integrity, software component traceability, and tamper-evident maintenance logs under digital transformation directives.
- **The Modern Aircraft Architecture:** Next-generation airframes generate gigabytes of sensor data per flight hour. Centralized cloud architectures introduce unacceptable telemetry latency, bandwidth saturation, and vulnerability to network blackouts.
- **The Future Need:** Edge-native inference capable of evaluating multi-sensor trust locally, executing microsecond anomaly detection, maintaining cryptographic custody, and enforcing verified repair closures.

---

## Slide 4: Objective & Approach

### Title
**Our Technical Approach: Decentralized Trust, Physics Contracts & Strict Decoupling**

### Key Content Points
- **Primary Objective:** Build and validate an end-to-end engineering demonstrator that transforms predictive maintenance from an open-loop estimation into a verifiable, closed-loop engineering workflow.
- **Core Engineering Principles:**
  - **Decoupled Architecture:** Clean separation of concerns between Sensor Acquisition, Trust Adjudication, Feature Extraction, Model Inference, Cryptographic Provenance, Offline Buffering, and Verification.
  - **Fail-Closed Execution:** Zero silent fallbacks. Schema mismatches, non-numeric inputs, corrupted artifacts, or signature anomalies trigger immediate, safe rejection.
  - **Zero Fabrication Standard:** Real automated tests, real scikit-learn/ONNX artifacts, measured execution latencies, and explicit segregation between demonstrator modes.

---

## Slide 5: Solution Overview & Architecture

### Title
**CyaplaneX End-to-End Pipeline Architecture**

### Key Content Points
- **Pipeline Architecture:**
  $$\text{Sensors} \rightarrow \text{Trust Engine} \rightarrow \text{6-Feature Contract} \rightarrow \text{Production ML} \rightarrow \text{Reasoning} \rightarrow \text{HMAC Signer} \rightarrow \text{Buffer} \rightarrow \text{Sync} \rightarrow \text{Verifier} \rightarrow \text{Passport}$$
- **Multi-Gate Architecture:**
  - **Gate A (Contract Gate):** Draft 2020-12 JSON Schema validation on all telemetry and events.
  - **Gate B (Sensor Trust Engine):** Range, freshness, stuck detection, drift, and consensus score.
  - **Gate C (Deterministic Feature Extraction):** 6-feature physics contract + window SHA-256 hash.
  - **Gate D (Production ML Adapter):** 120-tree Gradient Boosting Classifier (Joblib & ONNX).
  - **Gate E (Cryptographic Provenance):** Device-local HMAC-SHA256 manifest signing.
  - **Gate F (Store-and-Forward Buffer):** Monotonic sequence FIFO queue for offline resilience.
  - **Gate G (Independent Cloud Verifier):** Out-of-band signature verification and replay guard.
  - **Gate H (Closed-Loop Repair & Passport):** Fresh re-test and append-only Digital Passport ledger.

---

## Slide 6: Novelty & Differentiators

### Title
**Beyond Conventional Health Monitoring: CyaplaneX Core Innovations**

### Key Content Points
| Feature Dimension | Traditional Predictive Maintenance | CyaplaneX Novel Approach |
| :--- | :--- | :--- |
| **Sensor Ingest** | Blind acceptance of raw analog/digital data | **Pre-Inference Sensor Trust Gate** (adjudicates range, stuck, drift, consensus) |
| **Model Traceability** | Black-box prediction without code linkage | **Artifact-Bound Manifest** (binds exact model ID, version, and SHA-256 hash) |
| **Security & Tamper** | Cleartext JSON or post-hoc cloud encryption | **Device-Local HMAC-SHA256 Signing** (100% rejection on payload modification) |
| **Network Resilience** | Fails or drops records when cloud drops | **Autonomous FIFO Buffering** with lossless monotonic sequence synchronization |
| **Repair Closure** | Clerical sign-off / technician stamp | **Empirical Fresh Re-Test** with quantitative repair effectiveness ($\ge 0.80$) |
| **Component History** | Siloed relational maintenance database | **Immutable Digital Passport** chaining cradle-to-grave component health events |

---

## Slide 7: Engineering Challenges & Mitigation

### Title
**Key Technical Hurdles Solved During Development**

### Key Content Points
1. **The Sensor Drift vs. Real Fault Dilemma:**
   - *Challenge:* Distinguishing true mechanical bearing spalls from sensor failure or loose wiring.
   - *Solution:* Multi-sensor cross-channel consensus and statistical feature coupling preventing premature sensor discarding.
2. **Edge Hardware Resource Constraints:**
   - *Challenge:* Complex deep learning ensembles exceed MCU memory and real-time execution bounds.
   - *Solution:* Compact 120-estimator Gradient Boosting model exported to ONNX Runtime ($28.3\ \mu\text{s}$ inference).
3. **Cryptographic Integrity Without Cloud Dependencies:**
   - *Challenge:* Standard PKI infrastructure requires constant online certificate revocation (CRL/OCSP).
   - *Solution:* Deterministic device-local HMAC-SHA256 manifests using canonical payload hashing and monotonic sequences.
4. **Verification Integrity:**
   - *Challenge:* Technicians prematurely closing work orders without confirming mechanical repair efficacy.
   - *Solution:* Mandatory fresh sensor window acquisition enforcing quantitative repair effectiveness $\ge 0.80$.

---

## Slide 8: Technical Implementation & ML Contracts

### Title
**Strict Contracts, Production Model & Optimization**

### Key Content Points
- **The Frozen 6-Feature Physics Contract:**
  1. `vib_rms` (float, acceleration RMS, $\text{g}$)
  2. `vib_p2p` (float, peak-to-peak shock, $\text{g}$)
  3. `temp_mean` (float, bearing housing mean temperature, $^\circ\text{C}$)
  4. `temp_max` (float, bearing housing peak temperature, $^\circ\text{C}$)
  5. `rpm_mean` (float, rotational speed mean, $\text{RPM}$)
  6. `rpm_std` (float, rotational speed stability std, $\text{RPM}$)
- **Production Artifact Integrity:**
  - **Joblib Model:** [`ml/models/production_model.joblib`](file:///d:/CyplaneX/ml/models/production_model.joblib) (`95ae7ef37e1fd3f3...`)
  - **ONNX Model:** [`ml/models/production_model.onnx`](file:///d:/CyplaneX/ml/models/production_model.onnx) (`74c7fd44d5f74cc4...`)
  - **Parity Verification:** 100% classification agreement between Joblib and ONNX on multi-condition test suite.
  - **12-Point Acceptance Gate:** All 12 automated checks pass (`scripts/verify_ml_artifact.py`).

---

## Slide 9: Results & Empirical Achievements

### Title
**Empirical Evidence Matrix & Measured Performance**

### Key Content Points
| Evaluation Metric | Measured Result | Population / Dataset | Evidence File | Environment | Boundary & Limitation |
| :--- | :---: | :--- | :--- | :--- | :--- |
| **Held-Out Test Accuracy** | **99.80%** | 1,000 held-out samples (200/class) | `ml/models/model_metadata.json` | CPython 3.14.5 | CWRU vibration benchmark with synthetic thermal/RPM |
| **Held-Out Weighted F1** | **0.9980** | 1,000 test samples across 5 classes | `ml/evaluate.py` | CPython 3.14.5 | Evaluated on benchmark split, not operational flight |
| **5-Fold CV Weighted F1** | **0.9997** | 5,000 balanced benchmark samples | `ml/models/model_metadata.json` | CPython 3.14.5 | 1,000 samples per class across 5 fault classes |
| **Full Benchmark Accuracy** | **99.96%** | Full 5,000 curated dataset records | `ml/evaluate.py` | CPython 3.14.5 | Curated benchmark dataset |
| **Full Benchmark Macro F1** | **0.9996** | 5 fault classes balanced | `ml/evaluate.py` | CPython 3.14.5 | Macro-averaged across all 5 conditions |
| **HEALTHY OvR FPR** | **0.025%** | $N = 4,000$ non-healthy samples ($\text{FP}=1$) | `ml/models/model_metadata.json` | CPython 3.14.5 | 1 false alarm out of 4,000 non-healthy samples |
| **Joblib Inference Latency** | **~1.05 ms** | 100 consecutive predictions | Benchmark script | Host x86_64 CPU | Host CPU measurement; not embedded MCU latency |
| **ONNX Inference Latency** | **~28.3 µs** | 100 consecutive predictions | Benchmark script | Host x86_64 CPU | Host CPU measurement; not embedded MCU latency |
| **Tamper Rejection Rate** | **100%** | Altered payload field suite | `scripts/tamper_test.py` | Local CPython | 100% rejection on modified health score / hashes |
| **Offline Event Loss** | **0.00%** | Network disconnect simulation | `scripts/e2e_demo.py` | Local CPython | In-memory FIFO queue (100-event capacity) |
| **Repair Effectiveness** | **0.92** | Pre: 7.7% $\rightarrow$ Post: 100.0% | `scripts/e2e_demo.py` | Local CPython | Evaluated on simulated bearing fault & re-test |

---

## Slide 10: Demonstration Flow

### Title
**Live 20-Step Closed-Loop Demonstration Architecture**

### Key Content Points
- **The Complete Demonstration Cycle:**
  1. **Healthy Baseline:** Health score 100.0%, Sensor trust `TRUSTED`.
  2. **Fault Injection:** Controlled dynamic vibration anomaly ($1.85\text{g}$) injected.
  3. **Production ML Diagnosis:** Model `cyaplanex-gb-aeromodel-v1` diagnoses `HIGH_VIBRATION`, Health: **7.7%**, Severity: `CRITICAL`.
  4. **Maintenance Reasoning:** Priority `P1` dispatched with mechanical inspection recommendations.
  5. **Cryptographic Manifest:** Raw window hash, manifest hash, and HMAC signature generated.
  6. **Tamper Test:** Maliciously modified health score ($7.7\% \rightarrow 99.0\%$) triggers `PROVENANCE_VIOLATION`.
  7. **Offline Buffering:** Network dropped; events safely buffered in FIFO queue; drained upon reconnect.
  8. **Fresh Re-Test:** Bearing replaced, post-repair health restored to **100.0%**, repair effectiveness **0.92**.
  9. **Digital Passport:** Signed `ClosureRecord` permanently recorded in the asset's service ledger.

---

## Slide 11: Future Enhancements & Scalability

### Title
**Path to Flight Qualification: DO-178C, Asymmetric HSM & Cloud Mesh**

### Key Content Points
1. **Physical HIL Benchtop Execution:** Complete wiring and sensor stream validation of the ESP32 + ADXL345 + MAX6675 testbed per [`docs/HIL_RUNBOOK.md`](file:///d:/CyplaneX/docs/HIL_RUNBOOK.md).
2. **Hardware Security Module (HSM) Integration:** Transition from device-local HMAC keys to asymmetric ECDSA (SECP256R1) signing via hardware secure elements (e.g., ATECC608A / TPM 2.0).
3. **Live AWS Production Deployment:** Execute Terraform provisioning in [`cloud/infrastructure/terraform/`](file:///d:/CyplaneX/cloud/infrastructure/terraform/) to activate AWS IoT Core, Greengrass v2, and Timestream analytics.
4. **Airworthiness Certification Roadmap:** Align edge software design with RTCA DO-178C (Software Considerations in Airborne Systems) and DO-254 (Complex Electronic Hardware).

---

## Slide 12: Project Plan & Competition Milestones

### Title
**Development Timeline, Verification Gates & Competition Milestones**

### Key Content Points
- **Phase 1 — Discovery & Architecture Freeze (Weeks 1–2):** Pipeline specifications, 6-feature contract definition, and JSON Schema authoring. *(COMPLETED)*
- **Phase 2 — Sensor Trust & Preprocessing (Weeks 3–4):** Gate B multi-sensor trust engine, FFT spectral extractor, and simulated/replay stream readers. *(COMPLETED)*
- **Phase 3 — Production ML Training & Optimization (Weeks 5–6):** CWRU benchmark model training, 120-tree gradient boosting tuning, ONNX quantization, and artifact export. *(COMPLETED)*
- **Phase 4 — Provenance, Security & Offline Queues (Weeks 7–8):** Device-local HMAC signing, tamper detection, replay protection, and store-and-forward sync coordinator. *(COMPLETED)*
- **Phase 5 — Full Software Freeze & Acceptance (Week 9):** 68/68 automated tests, 12/12 ML acceptance gate, and web dashboard validation. *(COMPLETED)*
- **Phase 6 — Physical HIL & Final Submission (Current):** Benchtop HIL readiness package prepared, final video shot list recorded, and jury presentation finalized. *(CURRENT)*

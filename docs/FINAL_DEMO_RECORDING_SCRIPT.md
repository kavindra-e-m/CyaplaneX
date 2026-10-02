# CyaplaneX — Final Competition Demo Recording & Video Script

**Project:** CyaplaneX (Tata Technologies InnoVent 2026)  
**Category:** Edge AI for Predictive Maintenance & Aircraft Health Monitoring  
**Target Video Duration:** 3 to 5 Minutes  
**Demonstration Mode:** Production ML Engine (`cyaplanex-gb-aeromodel-v1`) with Cryptographic Provenance  

---

## 1. Pre-Recording Setup & Launch Commands

### 1.1 Environment Verification
Open a split terminal or dual-window recording layout:
- **Left Window:** Interactive Web MRO Dashboard
- **Right Window:** Terminal running real-time CLI diagnostic execution

```bash
# Terminal 1: Navigate to repository root and verify Python environment
cd D:\CyplaneX
uv sync

# Terminal 2 (Optional local REST server):
uv run python -m cloud.api.app
```

### 1.2 Dashboard Launch Command
Open the web dashboard in Google Chrome or Microsoft Edge:
```bash
# On Windows:
start dashboard/web/public/index.html

# On Linux:
xdg-open dashboard/web/public/index.html
```

---

## 2. Step-by-Step Recording Sequence & Frame Capture Guide

The recording is structured into 7 core evidence milestones:

```
[Frame 1: Healthy Baseline & Gate B Trust]
       │
       ▼
[Frame 2: Controlled Vibration Fault & Dynamic Anomaly]
       │
       ▼
[Frame 3: Production ML Diagnosis (99.80% Acc Model, 7.7% Health)]
       │
       ▼
[Frame 4: Device-Local Cryptographic Provenance & Manifest]
       │
       ▼
[Frame 5: Tamper Attack Injection & Immediate Rejection]
       │
       ▼
[Frame 6: Transport Disconnect & Zero-Loss Offline Buffering]
       │
       ▼
[Frame 7: Fresh Post-Repair Re-Test & Digital Passport Closure (0.92 Eff)]
```

---

### Scene 1: Healthy Baseline & Sensor Trust Adjudication
- **Terminal Command:**
  ```bash
  uv run python scripts/e2e_demo.py
  ```
- **Operator Action:**
  - Let Step 1 and Step 2 print to the terminal.
  - On Web Dashboard: Click **"Open Asset"**.
- **Visual Result on Screen:**
  - Terminal: `Active AI Engine: PRODUCTION ML MODEL (Lead: Monhit Raju)`, `Model ID: cyaplanex-gb-aeromodel-v1 (v1.0.0)`, `Model Hash: 95ae7ef3...`.
  - Dashboard: System state pill shows `HEALTHY` (green). Sensor Trust Engine displays `TRUSTED` across range, freshness, stuck detection, and consensus score ($1.00$).
- **Screenshot / Video Frame to Capture:**
  - `frame_01_healthy_baseline.png`: Showing green trust status and model identity.
- **Evidence Proved:**
  - Gate B (Sensor Trust Engine) validates raw telemetry before feeding ML; active engine is confirmed as production ML model.

---

### Scene 2: Fault Injection & Production ML Diagnosis
- **Terminal Execution:**
  - Step 3 through Step 6 print to the terminal.
- **Operator Action:**
  - On Web Dashboard: Click **"View Diagnostic"**.
- **Visual Result on Screen:**
  - Terminal:
    ```text
    [Step 3] Controlled fault injected on bearing-thrust-01 (1.85g vibration).
    [Step 4] Sensor trust evaluated: DEGRADED (Range=OK, Fresh=OK, Not Stuck)
    [Step 5] Edge AI Diagnosis: Condition=HIGH_VIBRATION, Health Score=7.7%, Severity=CRITICAL
    [Step 6] Maintenance Reasoning: Priority=P1
             Reason: Elevated dynamic vibration detected on bearing-thrust-01...
             Action: Halt test-rig rotation; inspect bearing-thrust-01 mountings...
    ```
  - Dashboard: Health Score card drops to `7.7%` (red critical). Anomaly Score displays `0.94`. Maintenance Priority displays `PRIORITY: P1`.
- **Screenshot / Video Frame to Capture:**
  - `frame_02_production_ml_diagnosis.png`: Showing degraded health score (7.7%), critical severity, and P1 dispatch.
- **Evidence Proved:**
  - Production Gradient Boosting model accurately classifies bearing vibration anomalies under the strict 6-feature physics contract.

---

### Scene 3: Cryptographic Provenance Generation & Cloud Verification
- **Terminal Execution:**
  - Step 7 and Step 8 execute.
- **Operator Action:**
  - On Web Dashboard: Click **"Verify Provenance"**.
- **Visual Result on Screen:**
  - Terminal:
    ```text
    [Step 7] Cryptographic Provenance generated:
             Sensor Window Hash: 73d4f37a6d157fe05e9ba5642fcf5dca...
             Manifest Hash:      32e201316aaf821391f93ecd9b9452cb...
             Digital Signature:  hmac-sha256:65332fe2cbde4f69093d3092...
             Provenanced Model:  cyaplanex-gb-aeromodel-v1 (v1.0.0)
             Provenanced Hash:   95ae7ef37e1fd3f32de96f33f60c2971...
    [Step 8] Cloud verification: Status=PROVENANCE_VERIFIED (Verified=True)
    ```
  - Dashboard: Provenance pill reads `PROVENANCE VERIFIED` (green). Console prints: *"The available event evidence is consistent with the verification rules."*
- **Screenshot / Video Frame to Capture:**
  - `frame_03_provenance_verification.png`: Showing SHA-256 sensor window hash, manifest hash, and verified signature.
- **Evidence Proved:**
  - Diagnostic evidence is cryptographically bound to the raw sensor window, device key, and exact ML model artifact hash.

---

### Scene 4: Tamper Attack Injection & Immediate Rejection
- **Terminal Execution:**
  - Step 9 executes.
- **Operator Action:**
  - On Web Dashboard: Click **"Run Tamper Test"**.
- **Visual Result on Screen:**
  - Terminal:
    ```text
    [Step 9] Tamper Test: Modified health_score to 99.0 -> Status=PROVENANCE_VIOLATION (Tamper Detected!)
    ```
  - Dashboard: Provenance pill immediately flips to `PROVENANCE_VIOLATION` (flashing red). System State indicates violation. Console reads: *"Demo tamper test prepared... Expected Result: Modified evidence is rejected by server-side verification."*
- **Screenshot / Video Frame to Capture:**
  - `frame_04_tamper_rejection.png`: Showing server-side rejection of maliciously altered health score.
- **Evidence Proved:**
  - Any unauthorized post-inference alteration of telemetry or diagnostic metrics is detected and rejected with 100% certainty.

---

### Scene 5: Network Disconnect & Zero-Loss Offline Buffering
- **Terminal Execution:**
  - Steps 10 through 14 execute.
- **Operator Action:**
  - On Web Dashboard: Click **"Simulate Offline"** (observe buffering), then click **"Restore Connectivity"** (observe in-order drain).
- **Visual Result on Screen:**
  - Terminal:
    ```text
    [Step 10] Simulated cloud connectivity drop: Transport is_connected=False
    [Step 11] New event generated while offline (Report rep-demo-003).
    [Step 12] OFFLINE BUFFERING active: Queue depth=1 record buffered.
    [Step 13] Connectivity restored: Synchronizing buffered queue...
    [Step 14] Synchronized 1 event(s) in sequence. Remaining queue depth=0.
    ```
  - Dashboard: Connectivity pill toggles from `OFFLINE` (amber) with `QUEUE: 1 BUFFERED` to `ONLINE` with `QUEUE: 0 BUFFERED` upon synchronization.
- **Screenshot / Video Frame to Capture:**
  - `frame_05_offline_buffering_sync.png`: Showing local FIFO queue buffering during network drop and zero-loss sequence drain.
- **Evidence Proved:**
  - Autonomous edge operation survives loss of cloud uplink without data loss or sequence disruption.

---

### Scene 6: Maintenance Dispatch & Fresh Post-Repair Re-Test
- **Terminal Execution:**
  - Steps 15 through 19 execute.
- **Operator Action:**
  - On Web Dashboard: Click **"Mark Maintenance Started"**, then click **"Start Re-test"**.
- **Visual Result on Screen:**
  - Terminal:
    ```text
    [Step 15] MRO Maintenance Started: Report rep-demo-002 -> State=MAINTENANCE_IN_PROGRESS
    [Step 16] Prototype Maintenance performed: Thrust bearing replaced, shaft torqued to specification.
    [Step 17] Fresh Re-test executed against new sensor window.
    [Step 18] Post-maintenance Health Score: 100.0% (Pre-score: 7.7%) [PRODUCTION MODEL METRIC]
    [Step 19] Outcome: REPAIR_VERIFIED (Repair Effectiveness: 0.92) [PRODUCTION MODEL METRIC]
    ```
  - Dashboard: Health score restores to `100.0%` (green). Anomaly score resets to `0.00`. Vibration drops to `0.35 g`. System state transitions to `REPAIR_VERIFIED`.
- **Screenshot / Video Frame to Capture:**
  - `frame_06_repair_verified.png`: Showing post-repair health score restoration (100.0%) and measured repair effectiveness (0.92).
- **Evidence Proved:**
  - Closed-loop verification ensures maintenance cannot be marked complete without empirical re-testing against fresh sensor windows.

---

### Scene 7: Component Digital Passport & Lifecycle Audit Trail
- **Terminal Execution:**
  - Step 20 prints complete passport history.
- **Operator Action:**
  - On Web Dashboard: Scroll down to **"Component Digital Passport & Lifecycle Records"** table.
- **Visual Result on Screen:**
  - Terminal:
    ```text
    [Step 20] Component Digital Passport for bearing-thrust-01:
             Closure ID: clo-c690d3ff | Status: REPAIR_VERIFIED
             Total Historical Records: 2
             - [DIAGNOSTIC_EVENT] Timestamp=... | Detail=HIGH_VIBRATION
             - [MAINTENANCE_CLOSURE] Timestamp=... | Detail=Replaced thrust bearing assembly...
    ```
  - Dashboard: Passport table displays 3 permanent chronological records with cryptographic hashes, pre/post scores, and `REPAIR_VERIFIED` badges.
- **Screenshot / Video Frame to Capture:**
  - `frame_07_digital_passport_ledger.png`: Showing tamper-evident component service ledger.
- **Evidence Proved:**
  - Complete cradle-to-grave traceability linking predictive diagnoses, work orders, re-tests, and closure manifests into an immutable digital passport.

---

## 3. Audio Narration Script (Voiceover Guide)

- **[0:00 - 0:30] Introduction:**  
  *"Welcome to CyaplaneX, our engineering demonstrator for Tata Technologies InnoVent 2026. CyaplaneX solves the critical trust and traceability gap in aerospace predictive maintenance by combining physics-informed Edge AI with cryptographic provenance and closed-loop repair verification."*
- **[0:30 - 1:15] Sensor Trust & Edge AI:**  
  *"At Step 1, our edge orchestrator boots and binds our production Gradient Boosting ML model, identified by its independent SHA-256 hash. When we inject a dynamic bearing vibration fault, our Sensor Trust Engine validates the signal before our edge model evaluates a degraded health score of 7.7 percent and dispatches a Priority P1 maintenance recommendation."*
- **[1:15 - 2:00] Provenance & Tamper Rejection:**  
  *"Unlike black-box monitoring systems, CyaplaneX generates a cryptographic manifest containing raw sensor window hashes, model metadata, and a device-local HMAC signature. If an attacker attempts to modify the health score to falsely clear the aircraft, our independent verifier detects the tamper violation immediately and rejects the record."*
- **[2:00 - 2:45] Offline Store-and-Forward:**  
  *"In disconnected flight-line environments, CyaplaneX buffers diagnostic events in an autonomous FIFO queue with zero data loss. Once connectivity is restored, events synchronize in strict sequence order."*
- **[2:45 - 3:30] Closed-Loop Repair & Passport:**  
  *"Finally, CyaplaneX enforces closed-loop repair verification. Following physical component replacement, a fresh sensor window is acquired, restoring the health score to 100 percent with a measured repair effectiveness of 0.92. This creates an immutable closure record appended to the component's Digital Passport."*

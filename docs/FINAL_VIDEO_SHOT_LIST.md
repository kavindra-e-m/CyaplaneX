# CyaplaneX — Final Competition Video Shot List & Director's Guide

**Competition:** Tata Technologies InnoVent 2026  
**Category:** Edge AI for Predictive Maintenance & Aircraft Health Monitoring  
**Target Video Duration:** 3:30 to 4:30 minutes  
**Demonstration Mode:** Production ML Engine (`cyaplanex-gb-aeromodel-v1`) with Cryptographic Provenance  
**Target Resolution:** 1080p (1920x1080) @ 60 fps or 30 fps  
**Screen Layout:** Split Screen (50% Interactive MRO Dashboard / 50% Live Edge Terminal)  

---

## Technical Recording Setup

```text
+------------------------------------------+------------------------------------------+
|       WEB MRO DASHBOARD (Left Half)      |       LIVE EDGE RUNTIME (Right Half)     |
|   http://localhost:5000 / Chrome Window  |     PowerShell / Terminal Execution      |
|  - Real-time Health & Anomaly Gauges     |  - Raw Sensor Window Telemetry (g, C, RPM)|
|  - Sensor Trust Adjudication Flags       |  - Feature Extraction (6-Feature Tuple)   |
|  - Cryptographic Provenance Indicators   |  - Production ML Class & Hash Logging     |
|  - Button-Guided Workflow Triggers       |  - HMAC Signature Verification Output     |
|  - Digital Passport Ledger Table         |  - Offline Queue Draining Status          |
+------------------------------------------+------------------------------------------+
```

---

## Detailed Shot-by-Shot Director's Guide

### SHOT 1: System Boot, Baseline Health & Dashboard Overview (0:00 – 0:35)

- **Screen Setup:** Split view with clean dashboard and terminal ready.
- **Terminal Command:**
  ```bash
  uv run python scripts/e2e_demo.py
  ```
- **Operator Action:**
  - Execute command in terminal. Allow Steps 1 and 2 to execute.
  - On Web Dashboard: Click **"Open Asset"**.
- **Expected Visual Result:**
  - Terminal displays:
    ```text
    Active AI Engine: PRODUCTION ML MODEL (Lead: Monhit Raju)
    Model ID:         cyaplanex-gb-aeromodel-v1 (v1.0.0)
    Model Hash:       95ae7ef37e1fd3f32de96f33f60c2971...
    [Step 2] Healthy baseline: Condition=HEALTHY, Health Score=100.0%, Trust=TRUSTED
    ```
  - Dashboard: System state displays `HEALTHY` (green badge). Sensor Trust indicators show `PASSED` across Range, Freshness, Stuck Checks, and Consensus Score (`1.00`).
- **Narration (Voiceover):**
  *"Welcome to CyaplaneX, our trusted closed-loop Edge AI predictive maintenance demonstrator for Tata Technologies InnoVent 2026. On boot, our edge orchestrator verifies and binds our production Gradient Boosting ML model, authenticated by its independent SHA-256 artifact hash. Under nominal flight-line conditions, the Sensor Trust Engine validates multi-sensor streams, reporting a baseline health score of 100 percent."*
- **Evidence Demonstrated:**
  - Production model initialization, independent SHA-256 verification, and Gate B (Sensor Trust) baseline validation.

---

### SHOT 2: Controlled Fault Injection & Production ML Diagnosis (0:35 – 1:10)

- **Screen Setup:** Focus on metric gauges and terminal Step 3–5 output.
- **Terminal Command:** (Continuous execution from previous step).
- **Operator Action:**
  - Allow Steps 3, 4, and 5 to print.
  - On Web Dashboard: Click **"View Diagnostic"**.
- **Expected Visual Result:**
  - Terminal displays:
    ```text
    [Step 3] Controlled fault injected on bearing-thrust-01 (1.85g vibration).
    [Step 4] Sensor trust evaluated: DEGRADED (Range=OK, Fresh=OK, Not Stuck)
    [Step 5] Edge AI Diagnosis: Condition=HIGH_VIBRATION, Health Score=7.7%, Severity=CRITICAL
    ```
  - Dashboard: Health score drops sharply from `100.0%` to `7.7%` (red alert). Anomaly score rises to `0.94`. Vibration card displays `1.85 g`.
- **Narration (Voiceover):**
  *"When a dynamic mechanical fault occurs—simulated here by high-frequency vibration spikes on the thrust bearing—the Sensor Trust Engine evaluates the anomaly. Rather than failing the sensor, it confirms the reading is genuine but degraded. The production ML model ingests the frozen 6-feature physics vector, diagnosing a critical condition with a health score of just 7.7 percent."*
- **Evidence Demonstrated:**
  - Multi-sensor trust gating, strict 6-feature contract execution, and production ML anomaly classification under simulated mechanical degradation.

---

### SHOT 3: Maintenance Reasoning & Actionable Dispatch (1:10 – 1:40)

- **Screen Setup:** Zoom or highlight the Maintenance Reasoning panel on dashboard and terminal Step 6.
- **Terminal Command:** (Continuous execution).
- **Operator Action:**
  - Highlight the reason and recommended action fields.
- **Expected Visual Result:**
  - Terminal displays:
    ```text
    [Step 6] Maintenance Reasoning: Priority=P1
             Reason: Elevated dynamic vibration detected on bearing-thrust-01 with severity CRITICAL...
             Action: Halt test-rig rotation; inspect bearing-thrust-01 mountings...
    ```
  - Dashboard: Priority badge highlights `PRIORITY: P1`. Diagnostic reason and actionable mechanical repair instructions populate the operator console.
- **Narration (Voiceover):**
  *"Predictive AI is useless without actionable guidance. CyaplaneX's Maintenance Reasoning Engine immediately escalates the fault to Priority P1, generating mechanical dispatch instructions to halt rotation, inspect shaft alignment, and replace the spalled bearing assembly before catastrophic failure occurs."*
- **Evidence Demonstrated:**
  - Automated translation from ML classification to deterministic MRO maintenance priority and corrective action.

---

### SHOT 4: Cryptographic Provenance & Model Metadata Binding (1:40 – 2:15)

- **Screen Setup:** Focus on Provenance panel, SHA-256 hashes, and digital signature display.
- **Terminal Command:** (Continuous execution).
- **Operator Action:**
  - Allow Steps 7 and 8 to print.
  - On Web Dashboard: Click **"Verify Provenance"**.
- **Expected Visual Result:**
  - Terminal displays:
    ```text
    [Step 7] Cryptographic Provenance generated:
             Sensor Window Hash: e7455ae4e26015ff7ccf5db97402ebde...
             Manifest Hash:      3ad6c16a9fe59b5b51d37556e8e89162...
             Digital Signature:  hmac-sha256:23f125f4720cbdd2d7cd8e70...
             Provenanced Model:  cyaplanex-gb-aeromodel-v1 (v1.0.0)
             Provenanced Hash:   95ae7ef37e1fd3f32de96f33f60c2971...
    [Step 8] Cloud verification: Status=PROVENANCE_VERIFIED (Verified=True)
    ```
  - Dashboard: Provenance status pill glows `PROVENANCE VERIFIED` (green). Window hash, manifest hash, and HMAC signature are fully visible in the UI.
- **Narration (Voiceover):**
  *"In mission-critical aerospace maintenance, data integrity is paramount. CyaplaneX binds every diagnostic inference to an immutable evidence manifest containing the raw sensor window hash, monotonic sequence number, and the exact model artifact hash `95ae7ef3`. The device signs this payload locally using HMAC-SHA256, allowing independent verifiers to cryptographically authenticate the diagnosis without blind trust."*
- **Evidence Demonstrated:**
  - Device-local cryptographic signing, tamper-evident lineage, and independent model hash binding.

---

### SHOT 5: Tamper Attack Injection & Immediate Rejection (2:15 – 2:45)

- **Screen Setup:** High alert visual transition; split screen showing tamper injection.
- **Terminal Command:** (Continuous execution).
- **Operator Action:**
  - Allow Step 9 to print.
  - On Web Dashboard: Click **"Run Tamper Test"**.
- **Expected Visual Result:**
  - Terminal displays:
    ```text
    [Step 9] Tamper Test: Modified health_score to 99.0 -> Status=PROVENANCE_VIOLATION (Tamper Detected!)
    ```
  - Dashboard: Provenance indicator flashes red with `PROVENANCE_VIOLATION`. System state shifts to alert. Operator prompt reads: *"Expected Result: Modified evidence is rejected by server-side verification."*
- **Narration (Voiceover):**
  *"To prove tamper resilience, we simulate a malicious adversary modifying the health score in transit from 7.7 percent to 99 percent to falsely clear the aircraft. The independent cloud verifier recomputes the canonical manifest hash, detects the signature mismatch, and instantly flags a `PROVENANCE_VIOLATION`, rejecting the corrupted record with 100 percent certainty."*
- **Evidence Demonstrated:**
  - Cryptographic tamper detection; prevention of unauthorized record falsification.

---

### SHOT 6: Disconnected Flight-Line Operation & Offline Buffering (2:45 – 3:20)

- **Screen Setup:** Highlight network indicator, queue counter, and store-and-forward sync.
- **Terminal Command:** (Continuous execution).
- **Operator Action:**
  - Allow Steps 10 through 14 to print.
  - On Web Dashboard: Click **"Simulate Offline"** (observe buffering), then click **"Restore Connectivity"** (observe automatic draining).
- **Expected Visual Result:**
  - Terminal displays:
    ```text
    [Step 10] Simulated cloud connectivity drop: Transport is_connected=False
    [Step 11] New event generated while offline (Report rep-demo-003).
    [Step 12] OFFLINE BUFFERING active: Queue depth=1 record buffered.
    [Step 13] Connectivity restored: Synchronizing buffered queue...
    [Step 14] Synchronized 1 event(s) in sequence. Remaining queue depth=0.
    ```
  - Dashboard: Connectivity pill changes to `OFFLINE` (amber) with `QUEUE: 1 BUFFERED`. Upon restore, flips to `ONLINE` and `QUEUE: 0 BUFFERED`.
- **Narration (Voiceover):**
  *"Aircraft frequently operate in remote or contested hangars without cloud uplinks. When we simulate a total network loss, CyaplaneX continues autonomous operation, signing events locally and buffering them in a bounded FIFO queue. As soon as connectivity is restored, the Store-and-Forward coordinator synchronizes buffered records in strict sequence order with zero data loss."*
- **Evidence Demonstrated:**
  - Fault-tolerant edge autonomy, in-memory FIFO buffering, and lossless store-and-forward synchronization.

---

### SHOT 7: Fresh Post-Repair Re-Test, Verification & Digital Passport (3:20 – 4:00)

- **Screen Setup:** Highlight maintenance state, fresh re-test, repair effectiveness gauge, and the component passport table.
- **Terminal Command:** (Continuous execution).
- **Operator Action:**
  - Allow Steps 15 through 20 to finish.
  - On Web Dashboard: Click **"Mark Maintenance Started"**, then click **"Start Re-test"**, and scroll down to the **Digital Passport Table**.
- **Expected Visual Result:**
  - Terminal displays:
    ```text
    [Step 15] MRO Maintenance Started -> State=MAINTENANCE_IN_PROGRESS
    [Step 16] Prototype Maintenance performed: Thrust bearing replaced...
    [Step 17] Fresh Re-test executed against new sensor window.
    [Step 18] Post-maintenance Health Score: 100.0% (Pre-score: 7.7%) [PRODUCTION MODEL METRIC]
    [Step 19] Outcome: REPAIR_VERIFIED (Repair Effectiveness: 0.92) [PRODUCTION MODEL METRIC]
    [Step 20] Component Digital Passport for bearing-thrust-01:
             Closure ID: clo-1fc447c2 | Status: REPAIR_VERIFIED
    ```
  - Dashboard: Health score restores to `100.0%` (green). System state confirms `REPAIR_VERIFIED`. Digital Passport ledger permanently records the diagnostic event and closure record.
- **Narration (Voiceover):**
  *"Finally, CyaplaneX closes the loop. After technicians replace the bearing, the system enforces a mandatory re-test against fresh telemetry. The post-maintenance health score returns to 100 percent, yielding a measured repair effectiveness of 0.92. This automatically emits a signed Closure Record into the component's immutable Digital Passport—providing a lifelong, tamper-evident audit trail for civil aviation authorities."*
- **Evidence Demonstrated:**
  - Closed-loop maintenance verification, quantitative repair effectiveness calculation (0.92), and permanent Digital Passport ledger logging.

---

## 3. Post-Recording Quality Verification Checklist

- [ ] Audio levels clear and normalized (-12 dB to -6 dB).
- [ ] No dropped frames; terminal font is crisp and legible (Consolas / Menlo >= 14 pt).
- [ ] Model ID clearly visible: `cyaplanex-gb-aeromodel-v1`.
- [ ] Pre-health (7.7%) and post-health (100.0%) clearly legible.
- [ ] Repair effectiveness (0.92) clearly displayed.
- [ ] Video ends with standard Tata Technologies InnoVent 2026 title card.

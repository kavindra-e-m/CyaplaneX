// AeroTrust AI - MRO Dashboard Interactive Controller
(function() {
  "use strict";

  // System State Model
  const state = {
    assetId: "aircraft-wing-lh",
    componentId: "bearing-thrust-01",
    reportId: "rep-2026-001",
    healthScore: 6.2,
    anomalyScore: 0.94,
    confidence: 0.92,
    condition: "HIGH_VIBRATION",
    severity: "CRITICAL",
    priority: "P1",
    trustStatus: "TRUSTED",
    vibration: 1.85,
    temperature: 54.2,
    rpm: 3600,
    connectivity: "ONLINE",
    queueDepth: 0,
    provenanceStatus: "PROVENANCE_VERIFIED",
    windowHash: "9f83c60517b4a02aca02648667232e7568b5e618e6d5da50e02fb8f54279ac4f",
    manifestHash: "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
    signature: "hmac-sha256:d8a1c028be4910cf1c94d039f60ad0cfa82672bf6c6a85f2b2c9a9d701e4a11f",
    sequence: 1,
    nonce: "n-550e8400-e29b-41d4-a716-446655440000",
    maintenanceState: "MAINTENANCE_REQUIRED",
    reason: "Elevated dynamic vibration (RMS 1.85g) detected on bearing-thrust-01 with TRUSTED sensor evidence.",
    action: "Halt test-rig rotation; inspect bearing-thrust-01 mountings, shaft alignment, and bearing race for spalling."
  };

  // DOM Elements
  const el = {
    txtSystemState: document.getElementById("txt-system-state"),
    indSystemState: document.getElementById("ind-system-state"),
    txtConnectivity: document.getElementById("txt-connectivity"),
    indConnectivity: document.getElementById("ind-connectivity"),
    txtProvenance: document.getElementById("txt-provenance"),
    indProvenance: document.getElementById("ind-provenance"),
    consoleOutput: document.getElementById("console-output"),
    lblStepState: document.getElementById("lbl-step-state"),
    valHealthScore: document.getElementById("val-health-score"),
    valAnomalyScore: document.getElementById("val-anomaly-score"),
    valConfidence: document.getElementById("val-confidence"),
    valCondition: document.getElementById("val-condition"),
    valReportId: document.getElementById("val-report-id"),
    lblTrustStatus: document.getElementById("lbl-trust-status"),
    valVibration: document.getElementById("val-vibration"),
    valTemperature: document.getElementById("val-temperature"),
    valRpm: document.getElementById("val-rpm"),
    lblPriority: document.getElementById("lbl-priority"),
    txtReason: document.getElementById("txt-reason"),
    txtRecommendation: document.getElementById("txt-recommendation"),
    lblQueueDepth: document.getElementById("lbl-queue-depth"),
    txtWindowHash: document.getElementById("txt-window-hash"),
    txtManifestHash: document.getElementById("txt-manifest-hash"),
    txtSignature: document.getElementById("txt-signature"),
    txtSeqNonce: document.getElementById("txt-seq-nonce"),
    passportTbody: document.getElementById("passport-tbody"),
    lblPassportCount: document.getElementById("lbl-passport-count")
  };

  function updateView() {
    el.valHealthScore.textContent = `${state.healthScore.toFixed(1)}%`;
    if (state.healthScore >= 75) {
      el.valHealthScore.className = "metric-val text-healthy";
    } else if (state.healthScore >= 40) {
      el.valHealthScore.className = "metric-val text-warning";
    } else {
      el.valHealthScore.className = "metric-val text-critical";
    }

    el.valAnomalyScore.textContent = state.anomalyScore.toFixed(2);
    el.valConfidence.textContent = `${Math.round(state.confidence * 100)}%`;
    el.valCondition.textContent = state.condition;
    el.valReportId.textContent = state.reportId;

    el.lblTrustStatus.textContent = state.trustStatus;
    el.lblTrustStatus.className = `badge-tag ${state.trustStatus === "TRUSTED" ? "text-healthy" : "text-critical"}`;

    el.valVibration.textContent = `${state.vibration.toFixed(2)} g`;
    el.valTemperature.textContent = `${state.temperature.toFixed(1)} °C`;
    el.valRpm.textContent = `${Math.round(state.rpm)} rpm`;

    el.lblPriority.textContent = `PRIORITY: ${state.priority}`;
    el.txtReason.textContent = state.reason;
    el.txtRecommendation.textContent = state.action;

    el.txtWindowHash.textContent = state.windowHash;
    el.txtManifestHash.textContent = state.manifestHash;
    el.txtSignature.textContent = state.signature;
    el.txtSeqNonce.textContent = `Seq: ${state.sequence} | Nonce: ${state.nonce.slice(0, 10)}...`;

    el.lblQueueDepth.textContent = `QUEUE: ${state.queueDepth} BUFFERED`;

    // Connectivity Pill
    el.txtConnectivity.textContent = state.connectivity;
    if (state.connectivity === "ONLINE") {
      el.indConnectivity.className = "status-indicator status-online";
    } else {
      el.indConnectivity.className = "status-indicator status-offline";
    }

    // Provenance Pill
    el.txtProvenance.textContent = state.provenanceStatus;
    if (state.provenanceStatus === "PROVENANCE_VERIFIED") {
      el.indProvenance.className = "status-indicator status-online";
    } else {
      el.indProvenance.className = "status-indicator status-violation";
    }

    // System State Pill
    el.txtSystemState.textContent = state.maintenanceState;
    if (state.maintenanceState === "HEALTHY" || state.maintenanceState === "REPAIR_VERIFIED") {
      el.indSystemState.className = "status-indicator status-online";
    } else if (state.maintenanceState === "OFFLINE BUFFERING" || state.maintenanceState === "MAINTENANCE_IN_PROGRESS") {
      el.indSystemState.className = "status-indicator status-offline";
    } else {
      el.indSystemState.className = "status-indicator status-violation";
    }
  }

  function setPrompt(stepName, promptText) {
    el.lblStepState.textContent = stepName;
    el.consoleOutput.innerHTML = promptText;
  }

  // Button 1: Open Asset
  document.getElementById("btn-open-asset").addEventListener("click", function() {
    setPrompt(
      "ASSET LOADED",
      "Asset selected. Review the latest health result, sensor trust state, and provenance status before taking maintenance action."
    );
    updateView();
  });

  // Button 2: View Diagnostic
  document.getElementById("btn-view-diagnostic").addEventListener("click", function() {
    setPrompt(
      "DIAGNOSTIC REVIEW",
      "Diagnostic evidence loaded. Confirm that the sensor window, model metadata, and maintenance recommendation correspond to the same report."
    );
    updateView();
  });

  // Button 3: Verify Provenance
  document.getElementById("btn-verify-provenance").addEventListener("click", function() {
    if (state.provenanceStatus === "PROVENANCE_VERIFIED") {
      setPrompt(
        "PROVENANCE VERIFIED",
        "Provenance verified. The available event evidence is consistent with the verification rules."
      );
    } else {
      setPrompt(
        "PROVENANCE FAILED",
        "Provenance verification failed. Do not treat this record as verified evidence until the violation is investigated."
      );
    }
    updateView();
  });

  // Button 4: Run Tamper Test (Demo)
  document.getElementById("btn-tamper-test").addEventListener("click", function() {
    state.provenanceStatus = "PROVENANCE_VIOLATION";
    state.healthScore = 12.0; // modified field
    setPrompt(
      "TAMPER DETECTED",
      "Demo tamper test prepared. One protected event value was modified.<br><strong style='color: var(--accent-rose);'>Expected Result: Modified evidence is rejected by server-side verification.</strong>"
    );
    updateView();
  });

  // Button 5: Simulate Offline
  document.getElementById("btn-simulate-offline").addEventListener("click", function() {
    state.connectivity = "OFFLINE";
    state.maintenanceState = "OFFLINE BUFFERING";
    state.queueDepth += 1;
    setPrompt(
      "OFFLINE MODE",
      "Offline mode enabled. New signed events will remain locally buffered until connectivity is restored."
    );
    updateView();
  });

  // Button 6: Restore Connectivity
  document.getElementById("btn-restore-connectivity").addEventListener("click", function() {
    state.connectivity = "ONLINE";
    state.maintenanceState = "MAINTENANCE_REQUIRED";
    const drained = state.queueDepth;
    state.queueDepth = 0;
    state.provenanceStatus = "PROVENANCE_VERIFIED";
    setPrompt(
      "SYNC COMPLETE",
      `Connectivity restored. Synchronizing buffered evidence in sequence (${drained} events transferred).`
    );
    updateView();
  });

  // Button 7: Mark Maintenance Started
  document.getElementById("btn-mark-maintenance").addEventListener("click", function() {
    state.maintenanceState = "MAINTENANCE_IN_PROGRESS";
    setPrompt(
      "MAINTENANCE STARTED",
      "Maintenance started for this report. The original diagnostic evidence will remain unchanged."
    );
    updateView();
  });

  // Button 8: Start Re-test
  document.getElementById("btn-start-retest").addEventListener("click", function() {
    // Post-maintenance fresh sensor collection
    state.healthScore = 100.0;
    state.anomalyScore = 0.0;
    state.condition = "HEALTHY";
    state.severity = "HEALTHY";
    state.vibration = 0.35;
    state.temperature = 48.5;
    state.priority = "P3";
    state.maintenanceState = "REPAIR_VERIFIED";
    state.reason = "Component bearing-thrust-01 operates within healthy parameters following bearing assembly replacement.";
    state.action = "Scheduled monitoring resumed. Closure record created.";

    // Add entry to passport table
    const row = document.createElement("tr");
    row.innerHTML = `
      <td class="mono">2026-09-30 10:45:00</td>
      <td>MAINTENANCE_CLOSURE</td>
      <td class="mono">clo-2026-002</td>
      <td>Replaced thrust bearing and re-torqued</td>
      <td>Pre: 6.2% &rarr; Post: 100.0% (Eff: 0.94)</td>
      <td class="mono">8a1e2f...b3c9</td>
      <td><span class="badge-tag text-healthy">REPAIR_VERIFIED</span></td>
    `;
    el.passportTbody.appendChild(row);
    el.lblPassportCount.textContent = "3 Records Recorded";

    setPrompt(
      "REPAIR VERIFIED",
      "Re-test started. Collecting a fresh sensor window and running the post-maintenance verification path.<br><strong style='color: var(--accent-emerald);'>Post-maintenance evidence meets the configured repair-verification rule. Closure record can be created.</strong>"
    );
    updateView();
  });

  // Initial load
  updateView();
})();

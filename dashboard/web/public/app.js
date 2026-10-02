// CyaplaneX Enterprise Aerospace MRO Platform — Client Controller
// Reference-Driven Design System Implementation

(function() {
  "use strict";

  // =========================================================================
  // State Model
  // =========================================================================
  const state = {
    // Current Active Navigation View
    currentView: "view-overview",

    // Engine & Asset Identity
    assetId: "aircraft-wing-lh",
    componentId: "bearing-thrust-01",
    engineSerial: "AIRC-CF34-01",
    engineModel: "CF34-8E Turbofan",

    // Model Provenance Metadata
    modelId: "cyaplanex-gb-aeromodel-v1",
    modelVersion: "1.0.0",
    modelHash: "95ae7ef37e1fd3f32de96f33f60c2971514ca8ea21fc22a72d632f3166af643b",
    modelStatus: "OPTIMAL",

    // System Telemetry & Diagnostic Health
    systemStatus: "HEALTHY", // "HEALTHY" | "CRITICAL FAULT"
    healthScore: 100.0,
    failureRisk: 2.4,
    anomalyScore: 0.06,
    confidence: 0.94,
    condition: "HEALTHY",
    severity: "LOW", // "LOW" | "CRITICAL"
    priority: "P3 - NORMAL", // "P3 - NORMAL" | "P1 - CRITICAL"

    // Sensor Readings (6-Feature Tuple Contract)
    vibrationRms: 0.35,
    vibrationP2p: 0.82,
    temperatureMean: 48.5,
    temperatureMax: 51.0,
    rpmMean: 1750,
    rpmStd: 4.8,
    scavengePressure: 72.4,

    // Sensor Trust Gating (Gate B)
    trustStatus: "TRUSTED", // "TRUSTED" | "DEGRADED"

    // Connectivity & Store-and-Forward Sync
    connectivity: "ONLINE", // "ONLINE" | "OFFLINE"
    queueDepth: 0,

    // Cryptographic Provenance
    provenanceStatus: "PROVENANCE_VERIFIED", // "PROVENANCE_VERIFIED" | "PROVENANCE_VIOLATION"
    windowHash: "73d4f37a6d157fe05e9ba5642fcf5dca658920192e44810938bb0912fa8901b2",
    manifestHash: "32e201316aaf821391f93ecd9b9452cb90145892019485bb0941829384756281",
    signature: "hmac-sha256:65332fe2cbde4f69093d30928475930294857201948572019485720194857201",
    sequence: 1,
    nonce: "n-550e8400-e29b-41d4-a716-446655440000",

    // MRO Maintenance Lifecycle State
    maintenanceState: "NOMINAL", // "NOMINAL" | "MAINTENANCE_REQUIRED" | "MAINTENANCE_IN_PROGRESS" | "REPAIR_VERIFIED" | "CLOSED"
    repairEffectiveness: 0.92,
    currentReportId: "rep-demo-002",
    closureId: "clo-1fc447c2"
  };

  // =========================================================================
  // DOM Elements
  // =========================================================================
  const el = {
    // Header & Badges
    pageHeading: document.getElementById("page-heading"),
    badgeAiModel: document.getElementById("badge-ai-model"),
    txtAiModel: document.getElementById("txt-ai-model"),
    dotAiModel: document.getElementById("dot-ai-model"),
    badgeConnectivity: document.getElementById("badge-connectivity"),
    txtConnectivity: document.getElementById("txt-connectivity"),
    dotConnectivity: document.getElementById("dot-connectivity"),
    badgeProvenance: document.getElementById("badge-provenance"),
    txtProvenance: document.getElementById("txt-provenance"),
    dotProvenance: document.getElementById("dot-provenance"),
    lblDemoStatus: document.getElementById("lbl-demo-status"),

    // KPI Cards
    kpiSysStatus: document.getElementById("kpi-sys-status"),
    kpiSysSub: document.getElementById("kpi-sys-sub"),
    kpiHealthScore: document.getElementById("kpi-health-score"),
    kpiFailureRisk: document.getElementById("kpi-failure-risk"),
    kpiPriority: document.getElementById("kpi-priority"),
    kpiPrioritySub: document.getElementById("kpi-priority-sub"),
    kpiAlerts: document.getElementById("kpi-alerts"),
    kpiAlertsSub: document.getElementById("kpi-alerts-sub"),

    // Sensor Overview
    valVibration: document.getElementById("val-vibration"),
    valTemperature: document.getElementById("val-temperature"),
    valRpm: document.getElementById("val-rpm"),
    trustVibration: document.getElementById("trust-vibration"),
    trustTemperature: document.getElementById("trust-temperature"),
    trustRpm: document.getElementById("trust-rpm"),
    badgeAggregateTrust: document.getElementById("badge-aggregate-trust"),

    // Callout Overlays on Engine Visual
    coutVibration: document.getElementById("cout-vibration"),
    coutStatusVib: document.getElementById("cout-status-vib"),
    coutTemp: document.getElementById("cout-temp"),
    coutStatusTemp: document.getElementById("cout-status-temp"),
    coutRpm: document.getElementById("cout-rpm"),
    coutStatusRpm: document.getElementById("cout-status-rpm"),

    // Predictive Insights
    insConditionText: document.getElementById("ins-condition-text"),
    insModelHash: document.getElementById("ins-model-hash"),
    insConfidence: document.getElementById("ins-confidence"),
    insSeverity: document.getElementById("ins-severity"),
    insAction: document.getElementById("ins-action"),

    // Evidence Drawer
    drawer: document.getElementById("evidence-drawer"),
    drawerBackdrop: document.getElementById("drawer-backdrop"),
    drwBadgeProv: document.getElementById("drw-badge-prov"),
    drwEventId: document.getElementById("drw-event-id"),
    drwVibRms: document.getElementById("drw-vib-rms"),
    drwVibP2p: document.getElementById("drw-vib-p2p"),
    drwTempMean: document.getElementById("drw-temp-mean"),
    drwTempMax: document.getElementById("drw-temp-max"),
    drwRpmMean: document.getElementById("drw-rpm-mean"),
    drwRpmStd: document.getElementById("drw-rpm-std"),
    drwCond: document.getElementById("drw-cond"),
    drwHealth: document.getElementById("drw-health"),
    drwSev: document.getElementById("drw-sev"),
    drwAnomaly: document.getElementById("drw-anomaly"),
    drwModhash: document.getElementById("drw-modhash"),
    drwWinhash: document.getElementById("drw-winhash"),
    drwSig: document.getElementById("drw-sig"),

    // Provenance Tab Elements
    txtProvWinhash: document.getElementById("txt-prov-winhash"),
    txtProvManhash: document.getElementById("txt-prov-manhash"),
    txtProvModhash: document.getElementById("txt-prov-modhash"),
    txtProvSignature: document.getElementById("txt-prov-signature"),
    txtTamperResult: document.getElementById("txt-tamper-result"),
    provStatusTag: document.getElementById("prov-status-tag"),

    // Sensors Tab
    stVibVal: document.getElementById("st-vib-val"),
    stTempVal: document.getElementById("st-temp-val"),
    stRpmVal: document.getElementById("st-rpm-val"),
    stVibTrust: document.getElementById("st-vib-trust"),

    // Table elements
    tblAlertCond: document.getElementById("tbl-alert-cond"),
    tblAlertScore: document.getElementById("tbl-alert-score"),
    tblAlertProv: document.getElementById("tbl-alert-prov"),
    tblTaskPrio: document.getElementById("tbl-task-prio"),
    tblTaskStatus: document.getElementById("tbl-task-status"),

    // Toast Container
    toastContainer: document.getElementById("toast-container")
  };

  // =========================================================================
  // Toast Notification Generator
  // =========================================================================
  function showToast(message, isError) {
    if (!el.toastContainer) return;
    const toast = document.createElement("div");
    toast.className = "toast";
    if (isError) {
      toast.style.borderLeft = "4px solid var(--status-critical)";
    } else {
      toast.style.borderLeft = "4px solid var(--accent-orange)";
    }
    toast.innerHTML = `<span>${message}</span>`;
    el.toastContainer.appendChild(toast);

    // Animate in
    setTimeout(function() {
      toast.classList.add("show");
    }, 10);

    // Remove after 3s
    setTimeout(function() {
      toast.classList.remove("show");
      setTimeout(function() {
        if (toast.parentNode) toast.parentNode.removeChild(toast);
      }, 300);
    }, 3200);
  }

  // =========================================================================
  // UI Render & Synchronization
  // =========================================================================
  function render() {
    // 1. Top Badges
    if (el.txtAiModel) {
      el.txtAiModel.textContent = `AI MODEL: ${state.modelStatus} (v${state.modelVersion})`;
    }

    if (el.txtConnectivity && el.badgeConnectivity && el.dotConnectivity) {
      if (state.connectivity === "ONLINE") {
        el.txtConnectivity.textContent = "ONLINE";
        el.badgeConnectivity.className = "system-status-badge badge-optimal";
        el.dotConnectivity.className = "status-dot dot-green";
      } else {
        el.txtConnectivity.textContent = `OFFLINE (${state.queueDepth} BUFFERED)`;
        el.badgeConnectivity.className = "system-status-badge badge-offline";
        el.dotConnectivity.className = "status-dot dot-amber";
      }
    }

    if (el.txtProvenance && el.badgeProvenance && el.dotProvenance) {
      if (state.provenanceStatus === "PROVENANCE_VERIFIED") {
        el.txtProvenance.textContent = "PROVENANCE VERIFIED";
        el.badgeProvenance.className = "system-status-badge badge-optimal";
        el.dotProvenance.className = "status-dot dot-green";
      } else {
        el.txtProvenance.textContent = "PROVENANCE VIOLATION";
        el.badgeProvenance.className = "system-status-badge badge-degraded";
        el.dotProvenance.className = "status-dot dot-red";
      }
    }

    // 2. Top KPI Cards
    if (el.kpiSysStatus) {
      el.kpiSysStatus.textContent = state.systemStatus;
      if (state.systemStatus === "HEALTHY") {
        el.kpiSysStatus.style.color = "var(--status-success)";
        if (el.kpiSysSub) el.kpiSysSub.textContent = "Nominal Flight Operating Envelope";
      } else {
        el.kpiSysStatus.style.color = "var(--status-critical)";
        if (el.kpiSysSub) el.kpiSysSub.textContent = "Dynamic Bearing Anomaly Detected";
      }
    }

    if (el.kpiHealthScore) {
      el.kpiHealthScore.textContent = `${state.healthScore.toFixed(1)}%`;
      if (state.healthScore >= 75) {
        el.kpiHealthScore.style.color = "var(--accent-orange)";
      } else {
        el.kpiHealthScore.style.color = "var(--status-critical)";
      }
    }

    if (el.kpiFailureRisk) {
      el.kpiFailureRisk.textContent = `${state.failureRisk.toFixed(1)}%`;
      el.kpiFailureRisk.style.color = state.failureRisk > 50 ? "var(--status-critical)" : "var(--text-primary)";
    }

    if (el.kpiPriority) {
      el.kpiPriority.textContent = state.priority;
      el.kpiPriority.style.color = state.priority.indexOf("P1") !== -1 ? "var(--status-critical)" : "var(--text-primary)";
      if (el.kpiPrioritySub) {
        el.kpiPrioritySub.textContent = state.priority.indexOf("P1") !== -1 ? "1 Immediate Work Order Dispatched" : "0 Immediate Work Orders";
      }
    }

    if (el.kpiAlerts) {
      el.kpiAlerts.textContent = state.healthScore < 75 ? "1" : "0";
      if (el.kpiAlertsSub) {
        el.kpiAlertsSub.textContent = state.healthScore < 75 ? "Bearing Vibration Spike" : "All Transducers Nominal";
      }
    }

    // 3. Sensor Overview
    if (el.valVibration) el.valVibration.textContent = `${state.vibrationRms.toFixed(2)} g`;
    if (el.valTemperature) el.valTemperature.textContent = `${state.temperatureMean.toFixed(1)} °C`;
    if (el.valRpm) el.valRpm.textContent = `${Math.round(state.rpmMean).toLocaleString()} rpm`;

    if (el.trustVibration) {
      el.trustVibration.textContent = state.trustStatus === "TRUSTED" ? "● TRUSTED" : "● DEGRADED";
      el.trustVibration.className = `trust-badge-pill ${state.trustStatus === "TRUSTED" ? "trusted" : "degraded"}`;
    }

    if (el.badgeAggregateTrust) {
      el.badgeAggregateTrust.textContent = state.trustStatus === "TRUSTED" ? "● TRUSTED" : "● DEGRADED";
      el.badgeAggregateTrust.className = `trust-badge-pill ${state.trustStatus === "TRUSTED" ? "trusted" : "degraded"}`;
    }

    // 4. Central Callouts
    if (el.coutVibration) el.coutVibration.textContent = `${state.vibrationRms.toFixed(2)} g`;
    if (el.coutStatusVib) {
      el.coutStatusVib.textContent = state.vibrationRms > 0.8 ? "● ANOMALY" : "● NOMINAL";
      el.coutStatusVib.style.color = state.vibrationRms > 0.8 ? "var(--status-critical)" : "var(--status-success)";
    }
    if (el.coutTemp) el.coutTemp.textContent = `${state.temperatureMean.toFixed(1)} °C`;
    if (el.coutRpm) el.coutRpm.textContent = `${Math.round(state.rpmMean).toLocaleString()} RPM`;

    // 5. Predictive Insights
    if (el.insConditionText) {
      el.insConditionText.textContent = state.condition;
      el.insConditionText.style.color = state.condition === "HEALTHY" ? "var(--status-success)" : "var(--status-critical)";
    }
    if (el.insModelHash) {
      el.insModelHash.textContent = `${state.modelHash.slice(0, 16)}...`;
    }
    if (el.insSeverity) {
      el.insSeverity.textContent = state.severity;
      el.insSeverity.style.color = state.severity === "LOW" ? "var(--status-success)" : "var(--status-critical)";
    }
    if (el.insAction) {
      if (state.condition === "HEALTHY") {
        el.insAction.textContent = "Component bearing-thrust-01 operates within healthy operating envelope. Continue scheduled flight-line monitoring.";
      } else {
        el.insAction.textContent = "Halt test-rig rotation; inspect bearing-thrust-01 mountings, shaft alignment, and bearing race for spalling.";
      }
    }

    // 6. Evidence Drawer Fields
    if (el.drwCond) el.drwCond.textContent = state.condition;
    if (el.drwHealth) el.drwHealth.textContent = `${state.healthScore.toFixed(1)}%`;
    if (el.drwSev) el.drwSev.textContent = state.severity;
    if (el.drwAnomaly) el.drwAnomaly.textContent = state.anomalyScore.toFixed(2);
    if (el.drwVibRms) el.drwVibRms.textContent = `${state.vibrationRms.toFixed(2)} g`;
    if (el.drwVibP2p) el.drwVibP2p.textContent = `${state.vibrationP2p.toFixed(2)} g`;
    if (el.drwTempMean) el.drwTempMean.textContent = `${state.temperatureMean.toFixed(1)} °C`;
    if (el.drwTempMax) el.drwTempMax.textContent = `${state.temperatureMax.toFixed(1)} °C`;
    if (el.drwRpmMean) el.drwRpmMean.textContent = `${Math.round(state.rpmMean)} rpm`;
    if (el.drwRpmStd) el.drwRpmStd.textContent = `${state.rpmStd.toFixed(1)} rpm`;

    if (el.drwBadgeProv) {
      el.drwBadgeProv.textContent = state.provenanceStatus === "PROVENANCE_VERIFIED" ? "VERIFIED" : "VIOLATION";
      el.drwBadgeProv.className = `trust-badge-pill ${state.provenanceStatus === "PROVENANCE_VERIFIED" ? "trusted" : "degraded"}`;
    }

    // 7. Provenance Tab
    if (el.txtProvWinhash) el.txtProvWinhash.textContent = state.windowHash;
    if (el.txtProvManhash) el.txtProvManhash.textContent = state.manifestHash;
    if (el.txtProvModhash) el.txtProvModhash.textContent = state.modelHash;
    if (el.txtProvSignature) el.txtProvSignature.textContent = state.signature;
    if (el.provStatusTag) {
      el.provStatusTag.textContent = state.provenanceStatus;
      el.provStatusTag.className = `trust-badge-pill ${state.provenanceStatus === "PROVENANCE_VERIFIED" ? "trusted" : "degraded"}`;
    }

    // 8. Sensors Tab
    if (el.stVibVal) el.stVibVal.textContent = `${state.vibrationRms.toFixed(2)} g`;
    if (el.stTempVal) el.stTempVal.textContent = `${state.temperatureMean.toFixed(1)} °C`;
    if (el.stRpmVal) el.stRpmVal.textContent = `${Math.round(state.rpmMean)} rpm`;
    if (el.stVibTrust) {
      el.stVibTrust.textContent = state.trustStatus;
      el.stVibTrust.className = `trust-badge-pill ${state.trustStatus === "TRUSTED" ? "trusted" : "degraded"}`;
    }

    // 9. Tables
    if (el.tblAlertCond) el.tblAlertCond.textContent = state.condition;
    if (el.tblAlertScore) {
      el.tblAlertScore.textContent = `${state.healthScore.toFixed(1)}%`;
      el.tblAlertScore.style.color = state.healthScore < 75 ? "var(--status-critical)" : "var(--status-success)";
    }
    if (el.tblAlertProv) {
      el.tblAlertProv.textContent = state.provenanceStatus;
      el.tblAlertProv.className = `trust-badge-pill ${state.provenanceStatus === "PROVENANCE_VERIFIED" ? "trusted" : "degraded"}`;
    }
  }

  // =========================================================================
  // View Switcher (Tab Controller)
  // =========================================================================
  function switchView(targetViewId) {
    state.currentView = targetViewId;
    const views = document.querySelectorAll(".view-panel");
    views.forEach(function(v) {
      v.classList.remove("active");
    });

    const activeView = document.getElementById(targetViewId);
    if (activeView) activeView.classList.add("active");

    // Update Navigation Rail active highlight
    const navItems = document.querySelectorAll(".nav-item");
    navItems.forEach(function(item) {
      if (item.getAttribute("data-view") === targetViewId) {
        item.classList.add("active");
      } else {
        item.classList.remove("active");
      }
    });

    // Update Heading
    if (el.pageHeading) {
      if (targetViewId === "view-overview") {
        el.pageHeading.textContent = "CF34-8E Turbofan Diagnostic Overview";
      } else if (targetViewId === "view-sensors") {
        el.pageHeading.textContent = "Gate B: Sensor Trust Adjudication Panel";
      } else if (targetViewId === "view-maintenance") {
        el.pageHeading.textContent = "MRO Closed-Loop Maintenance Workbench";
      } else if (targetViewId === "view-provenance") {
        el.pageHeading.textContent = "Cryptographic Provenance & Tamper Defense";
      } else if (targetViewId === "view-passport") {
        el.pageHeading.textContent = "Component Digital Passport Ledger";
      }
    }
  }

  // =========================================================================
  // Demonstration Scenarios
  // =========================================================================
  function setScenarioHealthy() {
    state.systemStatus = "HEALTHY";
    state.healthScore = 100.0;
    state.failureRisk = 2.4;
    state.anomalyScore = 0.06;
    state.condition = "HEALTHY";
    state.severity = "LOW";
    state.priority = "P3 - NORMAL";
    state.vibrationRms = 0.35;
    state.vibrationP2p = 0.82;
    state.temperatureMean = 48.5;
    state.temperatureMax = 51.0;
    state.rpmMean = 1750;
    state.trustStatus = "TRUSTED";
    state.provenanceStatus = "PROVENANCE_VERIFIED";
    state.connectivity = "ONLINE";
    state.queueDepth = 0;
    state.maintenanceState = "NOMINAL";

    if (el.lblDemoStatus) el.lblDemoStatus.textContent = "Step 1: Nominal Flight-Ready Baseline Active (100% Health)";
    showToast("Reset to Nominal Baseline: Model cyaplanex-gb-aeromodel-v1 active.", false);
    render();
  }

  function setScenarioFault() {
    state.systemStatus = "CRITICAL FAULT";
    state.healthScore = 7.7; // Exact production model metric
    state.failureRisk = 94.2;
    state.anomalyScore = 0.94;
    state.condition = "HIGH_VIBRATION";
    state.severity = "CRITICAL";
    state.priority = "P1 - CRITICAL";
    state.vibrationRms = 1.85; // Injected fault
    state.vibrationP2p = 2.92;
    state.temperatureMean = 54.2;
    state.temperatureMax = 58.0;
    state.rpmMean = 3600;
    state.trustStatus = "DEGRADED";
    state.provenanceStatus = "PROVENANCE_VERIFIED";
    state.maintenanceState = "MAINTENANCE_REQUIRED";

    if (el.lblDemoStatus) el.lblDemoStatus.textContent = "Step 2: Dynamic Fault Injected (7.7% Health, Priority P1 Dispatched)";
    showToast("Fault Injected: Vibration 1.85g. Model diagnosed HIGH_VIBRATION (7.7% Health).", true);
    render();
  }

  function setScenarioTamper() {
    state.provenanceStatus = "PROVENANCE_VIOLATION";
    if (el.txtTamperResult) {
      el.txtTamperResult.innerHTML = "<span style='color: var(--status-critical);'>Tamper Detected! Payload altered from 7.7% to 99.0%. HMAC Signature Mismatch &rarr; PROVENANCE_VIOLATION (100% Rejection).</span>";
    }
    if (el.lblDemoStatus) el.lblDemoStatus.textContent = "Step 3: Tamper Attack Rejection (PROVENANCE_VIOLATION)";
    showToast("PROVENANCE_VIOLATION: Altered health score rejected by cryptographic verifier.", true);
    render();
  }

  function setScenarioOffline() {
    state.connectivity = "OFFLINE";
    state.queueDepth = 1;
    if (el.lblDemoStatus) el.lblDemoStatus.textContent = "Step 4: Network Disconnect (1 Event Buffered Locally)";
    showToast("Transport Disconnected: Diagnostic events stored in autonomous FIFO queue.", false);
    render();
  }

  function setScenarioReconnect() {
    state.connectivity = "ONLINE";
    const drained = state.queueDepth;
    state.queueDepth = 0;
    state.provenanceStatus = "PROVENANCE_VERIFIED";
    if (el.lblDemoStatus) el.lblDemoStatus.textContent = "Step 5: Connection Restored (Lossless Sequence Sync Complete)";
    showToast(`Reconnected: Synchronized ${drained} buffered event(s) in strict sequence.`, false);
    render();
  }

  function setScenarioMaintain() {
    state.maintenanceState = "MAINTENANCE_IN_PROGRESS";
    if (el.lblDemoStatus) el.lblDemoStatus.textContent = "Step 6: Maintenance Started (Thrust Bearing Replacement In Progress)";
    showToast("Maintenance Started: Component taken offline for certified repair.", false);
    render();
  }

  function setScenarioRetest() {
    state.systemStatus = "HEALTHY";
    state.healthScore = 100.0;
    state.failureRisk = 2.4;
    state.anomalyScore = 0.08;
    state.condition = "HEALTHY";
    state.severity = "LOW";
    state.priority = "P3 - NORMAL";
    state.vibrationRms = 0.35;
    state.vibrationP2p = 0.84;
    state.temperatureMean = 48.5;
    state.rpmMean = 1750;
    state.trustStatus = "TRUSTED";
    state.provenanceStatus = "PROVENANCE_VERIFIED";
    state.maintenanceState = "REPAIR_VERIFIED";

    if (el.lblDemoStatus) el.lblDemoStatus.textContent = "Step 7: Fresh Re-Test Verified (Effectiveness: 0.92, REPAIR_VERIFIED)";
    showToast("Fresh Re-test Passed: Repair Effectiveness = 0.92 [PRODUCTION MODEL]. Closure appended to Digital Passport.", false);
    render();
  }

  // =========================================================================
  // Evidence Drawer Controls
  // =========================================================================
  function openDrawer(eventId) {
    if (el.drwEventId && eventId) el.drwEventId.textContent = eventId;
    if (el.drawer && el.drawerBackdrop) {
      el.drawerBackdrop.classList.add("open");
      el.drawer.classList.add("open");
    }
  }

  function closeDrawer() {
    if (el.drawer && el.drawerBackdrop) {
      el.drawerBackdrop.classList.remove("open");
      el.drawer.classList.remove("open");
    }
  }

  // =========================================================================
  // Clipboard Copy Utility
  // =========================================================================
  function copyTextToClipboard(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function() {
        showToast("SHA-256 Hash copied to clipboard!", false);
      }).catch(function() {
        showToast("Copied to clipboard.", false);
      });
    } else {
      // Fallback
      const ta = document.createElement("textarea");
      ta.value = text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
      showToast("SHA-256 Hash copied to clipboard!", false);
    }
  }

  // =========================================================================
  // Event Listeners & Binding
  // =========================================================================
  function setupEventListeners() {
    // 1. Navigation Item Clicks
    const navItems = document.querySelectorAll(".nav-item");
    navItems.forEach(function(item) {
      item.addEventListener("click", function() {
        const viewId = item.getAttribute("data-view");
        if (viewId) switchView(viewId);
      });
    });

    const brandHome = document.getElementById("btn-brand-home");
    if (brandHome) {
      brandHome.addEventListener("click", function(e) {
        e.preventDefault();
        switchView("view-overview");
      });
    }

    // 2. Demo Bar Scene Triggers
    const btnHealthy = document.getElementById("btn-scene-healthy");
    if (btnHealthy) btnHealthy.addEventListener("click", setScenarioHealthy);

    const btnFault = document.getElementById("btn-scene-fault");
    if (btnFault) btnFault.addEventListener("click", setScenarioFault);

    const btnTamper = document.getElementById("btn-scene-tamper");
    if (btnTamper) btnTamper.addEventListener("click", setScenarioTamper);

    const btnOffline = document.getElementById("btn-scene-offline");
    if (btnOffline) btnOffline.addEventListener("click", setScenarioOffline);

    const btnReconnect = document.getElementById("btn-scene-reconnect");
    if (btnReconnect) btnReconnect.addEventListener("click", setScenarioReconnect);

    const btnMaintain = document.getElementById("btn-scene-maintain");
    if (btnMaintain) btnMaintain.addEventListener("click", setScenarioMaintain);

    const btnRetest = document.getElementById("btn-scene-retest");
    if (btnRetest) btnRetest.addEventListener("click", setScenarioRetest);

    const btnOpenDrawer = document.getElementById("btn-open-drawer");
    if (btnOpenDrawer) btnOpenDrawer.addEventListener("click", function() { openDrawer(state.currentReportId); });

    // 3. Drawer Controls
    const btnCloseDrawer = document.getElementById("btn-close-drawer");
    if (btnCloseDrawer) btnCloseDrawer.addEventListener("click", closeDrawer);

    if (el.drawerBackdrop) el.drawerBackdrop.addEventListener("click", closeDrawer);

    // 4. Central Engine Visual Sensor Points
    const ptVib = document.getElementById("pulse-pt-vib");
    const coutVib = document.getElementById("callout-vib");
    const srowVib = document.getElementById("srow-vibration");
    [ptVib, coutVib, srowVib].forEach(function(node) {
      if (node) {
        node.addEventListener("click", function() {
          openDrawer(state.currentReportId);
          showToast("Inspecting Bearing-Thrust-01 Vibration Telemetry.", false);
        });
      }
    });

    const ptTemp = document.getElementById("pulse-pt-temp");
    const coutTemp = document.getElementById("callout-temp");
    const srowTemp = document.getElementById("srow-temperature");
    [ptTemp, coutTemp, srowTemp].forEach(function(node) {
      if (node) {
        node.addEventListener("click", function() {
          openDrawer(state.currentReportId);
          showToast("Inspecting Bearing Housing Temperature Telemetry.", false);
        });
      }
    });

    const ptRpm = document.getElementById("pulse-pt-rpm");
    const coutRpm = document.getElementById("callout-rpm");
    const srowRpm = document.getElementById("srow-rpm");
    [ptRpm, coutRpm, srowRpm].forEach(function(node) {
      if (node) {
        node.addEventListener("click", function() {
          openDrawer(state.currentReportId);
          showToast("Inspecting Shaft RPM Telemetry.", false);
        });
      }
    });

    // 5. Workbench Buttons
    const btnViewWb = document.getElementById("btn-view-workbench");
    const btnGotoMro = document.getElementById("btn-goto-mro");
    [btnViewWb, btnGotoMro].forEach(function(b) {
      if (b) {
        b.addEventListener("click", function() {
          switchView("view-maintenance");
        });
      }
    });

    const wbBtnStart = document.getElementById("wb-btn-start");
    if (wbBtnStart) wbBtnStart.addEventListener("click", setScenarioMaintain);

    const wbBtnRetest = document.getElementById("wb-btn-retest");
    if (wbBtnRetest) wbBtnRetest.addEventListener("click", setScenarioRetest);

    const wbBtnEvidence = document.getElementById("wb-btn-evidence");
    if (wbBtnEvidence) wbBtnEvidence.addEventListener("click", function() { openDrawer(state.currentReportId); });

    // 6. Provenance Page Buttons
    const btnProvTamper = document.getElementById("btn-prov-tamper");
    if (btnProvTamper) btnProvTamper.addEventListener("click", setScenarioTamper);

    const btnProvRestore = document.getElementById("btn-prov-restore");
    if (btnProvRestore) {
      btnProvRestore.addEventListener("click", function() {
        state.provenanceStatus = "PROVENANCE_VERIFIED";
        if (el.txtTamperResult) {
          el.txtTamperResult.innerHTML = "Unmodified Baseline: Signature matches computed manifest hash.";
        }
        showToast("Restored to verified baseline payload.", false);
        render();
      });
    }

    // 7. Copy Buttons
    document.addEventListener("click", function(e) {
      if (e.target && e.target.classList.contains("btn-copy")) {
        const targetId = e.target.getAttribute("data-target");
        if (targetId) {
          const targetEl = document.getElementById(targetId);
          if (targetEl) {
            copyTextToClipboard(targetEl.textContent.trim());
          }
        }
      }

      // Drawer trigger buttons inside tables
      if (e.target && e.target.classList.contains("btn-drawer-event")) {
        const repId = e.target.getAttribute("data-rep") || state.currentReportId;
        openDrawer(repId);
      }
    });

    // Alert row click opens drawer
    const alertRows = document.querySelectorAll(".clickable-alert-row");
    alertRows.forEach(function(row) {
      row.addEventListener("click", function() {
        openDrawer(state.currentReportId);
      });
    });

    const btnOpenAlertsEvidence = document.getElementById("btn-open-alerts-evidence");
    if (btnOpenAlertsEvidence) {
      btnOpenAlertsEvidence.addEventListener("click", function() {
        switchView("view-provenance");
      });
    }
  }

  // =========================================================================
  // Initialization
  // =========================================================================
  setupEventListeners();
  render();

  // Try fetching live /health from local WSGI server if available
  if (typeof window !== "undefined" && window.fetch) {
    fetch("/health").then(function(res) {
      return res.json();
    }).then(function(data) {
      if (data && data.status) {
        state.systemStatus = data.status.toUpperCase();
        render();
      }
    }).catch(function() {
      // Running standalone offline via file:// protocol
    });
  }
})();

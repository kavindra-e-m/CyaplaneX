// CyaplaneX Enterprise Aerospace MRO Platform — Client Controller
// Complete Interactive Engine & Reference-Driven Design Implementation

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
    engineSerial: "AIRC-CF34-01 (Controlled Demo)",
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

    // Sensor Readings (Frozen 6-Feature Tuple Contract)
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
    connectivity: "ONLINE", // "ONLINE" | "SYNCING" | "OFFLINE"
    queueDepth: 0,

    // Cryptographic Provenance
    provenanceStatus: "PROVENANCE_VERIFIED", // "PROVENANCE_VERIFIED" | "PROVENANCE_VIOLATION"
    windowHash: "73d4f37a6d157fe05e9ba5642fcf5dca658920192e44810938bb0912fa8901b2",
    manifestHash: "32e201316aaf821391f93ecd9b9452cb90145892019485bb0941829384756281",
    signature: "hmac-sha256:65332fe2cbde4f69093d30928475930294857201948572019485720194857201",
    sequence: 1,
    nonce: "n-550e8400-e29b-41d4-a716-446655440000",

    // MRO Maintenance Lifecycle State
    // "NOMINAL" | "MAINTENANCE_REQUIRED" | "MAINTENANCE_IN_PROGRESS" | "REPAIR_VERIFIED" | "CLOSED"
    maintenanceState: "NOMINAL",
    repairEffectiveness: 0.92,
    currentReportId: "rep-demo-002",
    closureId: "clo-1fc447c2",

    // Active selected timeline stage
    selectedTimelineStage: 1,

    // Active Stream Mode
    streamMode: "Live Telemetry • Flight-Line Stream"
  };

  // =========================================================================
  // Canonical Event Database (For Specific Event Inspection)
  // =========================================================================
  const eventRecords = {
    "rep-demo-002": {
      id: "rep-demo-002",
      type: "DIAGNOSTIC_EVENT",
      subtitle: "Report: rep-demo-002 • Injected Vibration Fault Event",
      asset: "aircraft-wing-lh",
      component: "bearing-thrust-01",
      timestamp: "2026-10-02T09:14:03Z",
      seq: "Seq: 1 | n-550e84",
      condition: "HIGH_VIBRATION",
      health: 7.7,
      severity: "CRITICAL",
      anomaly: 0.94,
      vibrationRms: 1.85,
      vibrationP2p: 2.92,
      tempMean: 54.2,
      tempMax: 58.0,
      rpmMean: 3600,
      rpmStd: 14.2,
      modelId: "cyaplanex-gb-aeromodel-v1 (v1.0.0)",
      modelHash: "95ae7ef37e1fd3f32de96f33f60c2971514ca8ea21fc22a72d632f3166af643b",
      windowHash: "73d4f37a6d157fe05e9ba5642fcf5dca658920192e44810938bb0912fa8901b2",
      signature: "hmac-sha256:65332fe2cbde4f69093d30928475930294857201948572019485720194857201",
      provenanceStatus: "PROVENANCE_VERIFIED",
      repairAction: "Pending MRO action; work order WO-AERO-2026-002 dispatched.",
      postHealth: "Pending re-test",
      repairEffectiveness: "Pending inspection",
      closureId: "Pending repair completion"
    },
    "clo-1fc447c2": {
      id: "clo-1fc447c2",
      type: "MAINTENANCE_CLOSURE",
      subtitle: "Record: clo-1fc447c2 • Cryptographically Verified Maintenance Closure & Passport Entry",
      asset: "aircraft-wing-lh",
      component: "bearing-thrust-01",
      timestamp: "2026-10-02T10:45:00Z",
      seq: "Seq: 2 | n-771a92",
      condition: "HEALTHY",
      health: 100.0,
      severity: "LOW",
      anomaly: 0.08,
      vibrationRms: 0.35,
      vibrationP2p: 0.84,
      tempMean: 48.5,
      tempMax: 51.0,
      rpmMean: 1750,
      rpmStd: 4.8,
      modelId: "cyaplanex-gb-aeromodel-v1 (v1.0.0)",
      modelHash: "95ae7ef37e1fd3f32de96f33f60c2971514ca8ea21fc22a72d632f3166af643b",
      windowHash: "8a1e2f949281a0b3c9e472619028347102938475620194857201948572019485",
      signature: "hmac-sha256:71982ab91c8430e495a820491823901928374619283746192837461928374619",
      provenanceStatus: "PROVENANCE_VERIFIED",
      repairAction: "Replaced thrust bearing with calibrated SKF Explorer 6205 assembly; torqued mountings to 45 Nm per AMM Chapter 72-00-02.",
      postHealth: "100.0% (Pre-repair: 7.7%)",
      repairEffectiveness: "0.92 (Threshold: \u2265 0.80) \u2192 REPAIR_VERIFIED",
      closureId: "clo-1fc447c2 (Added to Component Passport)"
    }
  };

  // =========================================================================
  // DOM Elements Cache
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
    txtEngineSub: document.getElementById("txt-engine-sub"),
    filterPill: document.querySelector(".filter-pill"),

    // KPI Cards
    cardKpiStatus: document.getElementById("card-kpi-status"),
    cardKpiHealth: document.getElementById("card-kpi-health"),
    cardKpiRisk: document.getElementById("card-kpi-risk"),
    cardKpiPriority: document.getElementById("card-kpi-priority"),
    cardKpiAlerts: document.getElementById("card-kpi-alerts"),
    kpiSysStatus: document.getElementById("kpi-sys-status"),
    kpiSysSub: document.getElementById("kpi-sys-sub"),
    kpiHealthScore: document.getElementById("kpi-health-score"),
    kpiFailureRisk: document.getElementById("kpi-failure-risk"),
    kpiPriority: document.getElementById("kpi-priority"),
    kpiPrioritySub: document.getElementById("kpi-priority-sub"),
    kpiAlerts: document.getElementById("kpi-alerts"),
    kpiAlertsSub: document.getElementById("kpi-alerts-sub"),

    // Sensor Overview (Left Panel)
    valVibration: document.getElementById("val-vibration"),
    valTemperature: document.getElementById("val-temperature"),
    valRpm: document.getElementById("val-rpm"),
    trustVibration: document.getElementById("trust-vibration"),
    trustTemperature: document.getElementById("trust-temperature"),
    trustRpm: document.getElementById("trust-rpm"),
    badgeAggregateTrust: document.getElementById("badge-aggregate-trust"),
    srowVibration: document.getElementById("srow-vibration"),
    srowTemperature: document.getElementById("srow-temperature"),
    srowRpm: document.getElementById("srow-rpm"),

    // Callout Overlays on Central Engine Visual
    coutVibration: document.getElementById("cout-vibration"),
    coutStatusVib: document.getElementById("cout-status-vib"),
    coutTemp: document.getElementById("cout-temp"),
    coutStatusTemp: document.getElementById("cout-status-temp"),
    coutRpm: document.getElementById("cout-rpm"),
    coutStatusRpm: document.getElementById("cout-status-rpm"),

    // Predictive Insights (Right Panel)
    insConditionText: document.getElementById("ins-condition-text"),
    insModelHash: document.getElementById("ins-model-hash"),
    insConfidence: document.getElementById("ins-confidence"),
    insSeverity: document.getElementById("ins-severity"),
    insAction: document.getElementById("ins-action"),

    // Evidence Drawer
    drawer: document.getElementById("evidence-drawer"),
    drawerBackdrop: document.getElementById("drawer-backdrop"),
    drawerSubtitle: document.getElementById("drawer-subtitle"),
    drwBadgeProv: document.getElementById("drw-badge-prov"),
    drwEventId: document.getElementById("drw-event-id"),
    drwTime: document.getElementById("drw-time"),
    drwSeq: document.getElementById("drw-seq"),
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
    drwRepairAction: document.getElementById("drw-repair-action"),
    drwPostHealth: document.getElementById("drw-post-health"),
    drwEff: document.getElementById("drw-eff"),
    drwClosureId: document.getElementById("drw-closure-id"),

    // Provenance Tab Elements
    txtProvWinhash: document.getElementById("txt-prov-winhash"),
    txtProvManhash: document.getElementById("txt-prov-manhash"),
    txtProvModhash: document.getElementById("txt-prov-modhash"),
    txtProvSignature: document.getElementById("txt-prov-signature"),
    txtTamperResult: document.getElementById("txt-tamper-result"),
    provStatusTag: document.getElementById("prov-status-tag"),

    // Sensors Tab (Gate B)
    stVibVal: document.getElementById("st-vib-val"),
    stTempVal: document.getElementById("st-temp-val"),
    stRpmVal: document.getElementById("st-rpm-val"),
    stVibTrust: document.getElementById("st-vib-trust"),

    // Workbench Tab Elements
    wbStatusTag: document.getElementById("wb-status-tag"),
    wbBtnStart: document.getElementById("wb-btn-start"),
    wbBtnRetest: document.getElementById("wb-btn-retest"),
    wbBtnClose: document.getElementById("wb-btn-close"),
    wbBtnEvidence: document.getElementById("wb-btn-evidence"),
    stageInProg: document.getElementById("stage-in-prog"),
    stageRetest: document.getElementById("stage-retest"),
    stageVerified: document.getElementById("stage-verified"),
    stageClosed: document.getElementById("stage-closed"),

    // Tables
    tblAlertCond: document.getElementById("tbl-alert-cond"),
    tblAlertScore: document.getElementById("tbl-alert-score"),
    tblAlertProv: document.getElementById("tbl-alert-prov"),
    tblTaskPrio: document.getElementById("tbl-task-prio"),
    tblTaskStatus: document.getElementById("tbl-task-status"),

    // Chart Canvas & Tooltips
    svgChartVibration: document.getElementById("svg-chart-vibration"),
    tooltipVib: document.getElementById("tooltip-vib"),
    svgChartTemp: document.getElementById("svg-chart-temp"),
    tooltipTemp: document.getElementById("tooltip-temp"),

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

    setTimeout(function() {
      toast.classList.add("show");
    }, 10);

    setTimeout(function() {
      toast.classList.remove("show");
      setTimeout(function() {
        if (toast.parentNode) toast.parentNode.removeChild(toast);
      }, 300);
    }, 3200);
  }

  // =========================================================================
  // Clipboard Copy Utility with Visual Button State Transition
  // =========================================================================
  function copyTextToClipboard(text, btnElement) {
    if (btnElement) {
      const originalText = btnElement.textContent;
      btnElement.textContent = "COPIED";
      btnElement.classList.add("copied");
      setTimeout(function() {
        btnElement.textContent = originalText;
        btnElement.classList.remove("copied");
      }, 1500);
    }

    showToast("SHA-256 Hash copied to clipboard!", false);

    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).catch(function() {
        fallbackCopy(text);
      });
    } else {
      fallbackCopy(text);
    }
  }

  function fallbackCopy(text) {
    try {
      const ta = document.createElement("textarea");
      ta.value = text;
      ta.style.position = "fixed";
      ta.style.opacity = "0";
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
    } catch {
      // silent fallback
    }
  }

  // =========================================================================
  // UI Render & Complete Synchronization
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
      } else if (state.connectivity === "SYNCING") {
        el.txtConnectivity.textContent = "SYNCING (1 EVENT)...";
        el.badgeConnectivity.className = "system-status-badge badge-offline";
        el.dotConnectivity.className = "status-dot dot-amber";
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
        if (el.kpiSysSub) el.kpiSysSub.textContent = "Nominal Flight Envelope";
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
    if (el.insConfidence) {
      el.insConfidence.textContent = `${(state.confidence * 100).toFixed(0)}%`;
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

    // 6. Provenance Tab
    if (el.txtProvWinhash) el.txtProvWinhash.textContent = state.windowHash;
    if (el.txtProvManhash) el.txtProvManhash.textContent = state.manifestHash;
    if (el.txtProvModhash) el.txtProvModhash.textContent = state.modelHash;
    if (el.txtProvSignature) el.txtProvSignature.textContent = state.signature;
    if (el.provStatusTag) {
      el.provStatusTag.textContent = state.provenanceStatus === "PROVENANCE_VERIFIED" ? "PROVENANCE VERIFIED" : "PROVENANCE VIOLATION";
      el.provStatusTag.className = `trust-badge-pill ${state.provenanceStatus === "PROVENANCE_VERIFIED" ? "trusted" : "degraded"}`;
    }

    // 7. Sensors Tab
    if (el.stVibVal) el.stVibVal.textContent = `${state.vibrationRms.toFixed(2)} g`;
    if (el.stTempVal) el.stTempVal.textContent = `${state.temperatureMean.toFixed(1)} °C`;
    if (el.stRpmVal) el.stRpmVal.textContent = `${Math.round(state.rpmMean)} rpm`;
    if (el.stVibTrust) {
      el.stVibTrust.textContent = state.trustStatus;
      el.stVibTrust.className = `trust-badge-pill ${state.trustStatus === "TRUSTED" ? "trusted" : "degraded"}`;
    }

    // 8. Tables
    if (el.tblAlertCond) el.tblAlertCond.textContent = state.condition;
    if (el.tblAlertScore) {
      el.tblAlertScore.textContent = `${state.healthScore.toFixed(1)}%`;
      el.tblAlertScore.style.color = state.healthScore < 75 ? "var(--status-critical)" : "var(--status-success)";
    }
    if (el.tblAlertProv) {
      el.tblAlertProv.textContent = state.provenanceStatus;
      el.tblAlertProv.className = `trust-badge-pill ${state.provenanceStatus === "PROVENANCE_VERIFIED" ? "trusted" : "degraded"}`;
    }

    // 9. Workbench State Machine Synchronization
    renderWorkbenchState();

    // 10. Timeline Node Highlight Synchronization
    renderTimelineNodes();
  }

  // =========================================================================
  // Maintenance Workbench State Engine
  // =========================================================================
  function renderWorkbenchState() {
    if (!el.wbStatusTag) return;

    // Reset breadcrumb highlights
    const mutedColor = "var(--text-muted)";
    const orangeColor = "var(--accent-orange)";
    const greenColor = "var(--status-success)";

    if (el.stageInProg) el.stageInProg.style.color = mutedColor;
    if (el.stageRetest) el.stageRetest.style.color = mutedColor;
    if (el.stageVerified) el.stageVerified.style.color = mutedColor;
    if (el.stageClosed) el.stageClosed.style.color = mutedColor;

    if (state.maintenanceState === "NOMINAL") {
      el.wbStatusTag.textContent = "STAGE: NOMINAL / IDLE";
      if (el.wbBtnStart) el.wbBtnStart.disabled = false;
      if (el.wbBtnRetest) el.wbBtnRetest.disabled = true;
      if (el.wbBtnClose) el.wbBtnClose.disabled = true;
    } else if (state.maintenanceState === "MAINTENANCE_REQUIRED") {
      el.wbStatusTag.textContent = "STAGE: WORK ORDER DISPATCHED (P1)";
      if (el.wbBtnStart) el.wbBtnStart.disabled = false;
      if (el.wbBtnRetest) el.wbBtnRetest.disabled = true;
      if (el.wbBtnClose) el.wbBtnClose.disabled = true;
    } else if (state.maintenanceState === "MAINTENANCE_IN_PROGRESS") {
      el.wbStatusTag.textContent = "STAGE: MAINTENANCE IN PROGRESS";
      if (el.stageInProg) el.stageInProg.style.color = orangeColor;
      if (el.wbBtnStart) el.wbBtnStart.disabled = true;
      if (el.wbBtnRetest) el.wbBtnRetest.disabled = false;
      if (el.wbBtnClose) el.wbBtnClose.disabled = true;
    } else if (state.maintenanceState === "REPAIR_VERIFIED") {
      el.wbStatusTag.textContent = "STAGE: REPAIR VERIFIED (Eff: 0.92)";
      if (el.stageInProg) el.stageInProg.style.color = greenColor;
      if (el.stageRetest) el.stageRetest.style.color = greenColor;
      if (el.stageVerified) el.stageVerified.style.color = greenColor;
      if (el.wbBtnStart) el.wbBtnStart.disabled = true;
      if (el.wbBtnRetest) el.wbBtnRetest.disabled = true;
      if (el.wbBtnClose) el.wbBtnClose.disabled = false;
    } else if (state.maintenanceState === "CLOSED") {
      el.wbStatusTag.textContent = "STAGE: ORDER CLOSED (IN PASSPORT)";
      if (el.stageInProg) el.stageInProg.style.color = greenColor;
      if (el.stageRetest) el.stageRetest.style.color = greenColor;
      if (el.stageVerified) el.stageVerified.style.color = greenColor;
      if (el.stageClosed) el.stageClosed.style.color = greenColor;
      if (el.wbBtnStart) el.wbBtnStart.disabled = true;
      if (el.wbBtnRetest) el.wbBtnRetest.disabled = true;
      if (el.wbBtnClose) el.wbBtnClose.disabled = true;
    }
  }

  // =========================================================================
  // Timeline Highlight Synchronization
  // =========================================================================
  function renderTimelineNodes() {
    for (let i = 1; i <= 9; i++) {
      const node = document.getElementById(`tnode-${i}`);
      if (node) {
        if (i === state.selectedTimelineStage) {
          node.classList.add("active");
        } else {
          node.classList.remove("active");
        }
      }
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
  // Evidence Drawer Controls (Specific Event Context Injection)
  // =========================================================================
  function openDrawer(eventId) {
    const targetId = eventId || state.currentReportId;
    const record = eventRecords[targetId];

    if (record) {
      // Inject specific record context
      if (el.drwEventId) el.drwEventId.textContent = record.id;
      if (el.drawerSubtitle) el.drawerSubtitle.textContent = record.subtitle;
      if (el.drwTime) el.drwTime.textContent = record.timestamp;
      if (el.drwSeq) el.drwSeq.textContent = record.seq;
      if (el.drwCond) {
        el.drwCond.textContent = record.condition;
        el.drwCond.style.color = record.condition === "HEALTHY" ? "var(--status-success)" : "var(--status-critical)";
      }
      if (el.drwHealth) el.drwHealth.textContent = `${record.health.toFixed(1)}%`;
      if (el.drwSev) el.drwSev.textContent = record.severity;
      if (el.drwAnomaly) el.drwAnomaly.textContent = record.anomaly.toFixed(2);
      if (el.drwVibRms) el.drwVibRms.textContent = `${record.vibrationRms.toFixed(2)} g`;
      if (el.drwVibP2p) el.drwVibP2p.textContent = `${record.vibrationP2p.toFixed(2)} g`;
      if (el.drwTempMean) el.drwTempMean.textContent = `${record.tempMean.toFixed(1)} °C`;
      if (el.drwTempMax) el.drwTempMax.textContent = `${record.tempMax.toFixed(1)} °C`;
      if (el.drwRpmMean) el.drwRpmMean.textContent = `${Math.round(record.rpmMean).toLocaleString()} rpm`;
      if (el.drwRpmStd) el.drwRpmStd.textContent = `${record.rpmStd.toFixed(1)} rpm`;

      if (el.drwModhash) {
        el.drwModhash.textContent = record.modelHash;
        el.drwModhash.title = record.modelHash;
      }
      if (el.drwWinhash) {
        el.drwWinhash.textContent = record.windowHash;
        el.drwWinhash.title = record.windowHash;
      }
      if (el.drwSig) {
        el.drwSig.textContent = record.signature;
        el.drwSig.title = record.signature;
      }

      if (el.drwBadgeProv) {
        const isViolation = (targetId === "rep-demo-002" && state.provenanceStatus === "PROVENANCE_VIOLATION");
        el.drwBadgeProv.textContent = isViolation ? "PROVENANCE VIOLATION" : "VERIFIED";
        el.drwBadgeProv.className = `trust-badge-pill ${isViolation ? "degraded" : "trusted"}`;
      }

      if (el.drwRepairAction) el.drwRepairAction.textContent = record.repairAction;
      if (el.drwPostHealth) el.drwPostHealth.textContent = record.postHealth;
      if (el.drwEff) el.drwEff.textContent = record.repairEffectiveness;
      if (el.drwClosureId) el.drwClosureId.textContent = record.closureId;
    } else {
      // Dynamic live view based on current state
      if (el.drwEventId) el.drwEventId.textContent = state.currentReportId;
      if (el.drawerSubtitle) el.drawerSubtitle.textContent = `Report: ${state.currentReportId} • Live Engine Telemetry`;
      if (el.drwCond) el.drwCond.textContent = state.condition;
      if (el.drwHealth) el.drwHealth.textContent = `${state.healthScore.toFixed(1)}%`;
      if (el.drwSev) el.drwSev.textContent = state.severity;
      if (el.drwAnomaly) el.drwAnomaly.textContent = state.anomalyScore.toFixed(2);
      if (el.drwVibRms) el.drwVibRms.textContent = `${state.vibrationRms.toFixed(2)} g`;
      if (el.drwVibP2p) el.drwVibP2p.textContent = `${state.vibrationP2p.toFixed(2)} g`;
      if (el.drwTempMean) el.drwTempMean.textContent = `${state.temperatureMean.toFixed(1)} °C`;
      if (el.drwTempMax) el.drwTempMax.textContent = `${state.temperatureMax.toFixed(1)} °C`;
      if (el.drwRpmMean) el.drwRpmMean.textContent = `${Math.round(state.rpmMean).toLocaleString()} rpm`;
      if (el.drwRpmStd) el.drwRpmStd.textContent = `${state.rpmStd.toFixed(1)} rpm`;

      if (el.drwModhash) {
        el.drwModhash.textContent = state.modelHash;
        el.drwModhash.title = state.modelHash;
      }
      if (el.drwWinhash) {
        el.drwWinhash.textContent = state.windowHash;
        el.drwWinhash.title = state.windowHash;
      }
      if (el.drwSig) {
        el.drwSig.textContent = state.signature;
        el.drwSig.title = state.signature;
      }

      if (el.drwBadgeProv) {
        el.drwBadgeProv.textContent = state.provenanceStatus === "PROVENANCE_VERIFIED" ? "VERIFIED" : "PROVENANCE VIOLATION";
        el.drwBadgeProv.className = `trust-badge-pill ${state.provenanceStatus === "PROVENANCE_VERIFIED" ? "trusted" : "degraded"}`;
      }
    }

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
  // Demonstration Scenarios & State Machine Actions
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
    state.rpmStd = 4.8;
    state.trustStatus = "TRUSTED";
    state.provenanceStatus = "PROVENANCE_VERIFIED";
    state.connectivity = "ONLINE";
    state.queueDepth = 0;
    state.maintenanceState = "NOMINAL";
    state.selectedTimelineStage = 1;

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
    state.rpmStd = 14.2;
    state.trustStatus = "DEGRADED";
    state.provenanceStatus = "PROVENANCE_VERIFIED";
    state.maintenanceState = "MAINTENANCE_REQUIRED";
    state.selectedTimelineStage = 3;

    if (el.lblDemoStatus) el.lblDemoStatus.textContent = "Step 2: Dynamic Fault Injected (7.7% Health, Priority P1 Dispatched)";
    showToast("Fault Injected: Vibration 1.85g. Model diagnosed HIGH_VIBRATION (7.7% Health).", true);
    render();
  }

  function setScenarioTamper() {
    state.provenanceStatus = "PROVENANCE_VIOLATION";
    if (el.txtTamperResult) {
      el.txtTamperResult.innerHTML = "<span style='color: var(--status-critical); font-weight: 700;'>Tamper Detected! Payload altered from 7.7% to 99.0%. HMAC Signature Mismatch &rarr; PROVENANCE_VIOLATION (100% Rejection).</span>";
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
    if (state.connectivity === "ONLINE" && state.queueDepth === 0) {
      showToast("System already online. All events are in sync.", false);
      return;
    }

    state.connectivity = "SYNCING";
    render();

    setTimeout(function() {
      const drained = state.queueDepth || 1;
      state.connectivity = "ONLINE";
      state.queueDepth = 0;
      state.provenanceStatus = "PROVENANCE_VERIFIED";
      if (el.lblDemoStatus) el.lblDemoStatus.textContent = "Step 5: Connection Restored (Lossless Sequence Sync Complete)";
      showToast(`Reconnected: Synchronized ${drained} buffered event(s) in strict sequence.`, false);
      render();
    }, 600);
  }

  function setScenarioMaintain() {
    if (state.systemStatus === "HEALTHY" && state.maintenanceState === "NOMINAL") {
      showToast("Starting routine maintenance overhaul on bearing-thrust-01...", false);
    }
    state.maintenanceState = "MAINTENANCE_IN_PROGRESS";
    state.selectedTimelineStage = 6;
    if (el.lblDemoStatus) el.lblDemoStatus.textContent = "Step 6: Maintenance Started (Thrust Bearing Replacement In Progress)";
    showToast("Maintenance Started: Component taken offline for scheduled repair.", false);
    render();
  }

  function setScenarioRetest() {
    if (state.maintenanceState !== "MAINTENANCE_IN_PROGRESS" && state.maintenanceState !== "REPAIR_VERIFIED" && state.maintenanceState !== "CLOSED") {
      showToast("Repair must be initiated first. Starting repair now...", false);
      state.maintenanceState = "MAINTENANCE_IN_PROGRESS";
    }

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
    state.temperatureMax = 51.0;
    state.rpmMean = 1750;
    state.rpmStd = 4.8;
    state.trustStatus = "TRUSTED";
    state.provenanceStatus = "PROVENANCE_VERIFIED";
    state.maintenanceState = "REPAIR_VERIFIED";
    state.selectedTimelineStage = 8;

    if (el.lblDemoStatus) el.lblDemoStatus.textContent = "Step 7: Fresh Re-Test Verified (Effectiveness: 0.92, REPAIR_VERIFIED)";
    showToast("Fresh Re-test Passed: Repair Effectiveness = 0.92 [PRODUCTION MODEL]. Closure ready for Passport.", false);
    render();
  }

  function closeMaintenanceWorkOrder() {
    if (state.maintenanceState !== "REPAIR_VERIFIED") {
      showToast("A fresh re-test must verify the repair before closing the work order.", true);
      return;
    }

    state.maintenanceState = "CLOSED";
    state.selectedTimelineStage = 9;
    showToast("Work Order WO-AERO-2026-002 closed. Signed ClosureRecord clo-1fc447c2 appended to Digital Passport.", false);
    render();
    setTimeout(function() {
      switchView("view-passport");
    }, 400);
  }

  // =========================================================================
  // Chart Hover Tooltip Controller
  // =========================================================================
  function setupChartTooltips() {
    if (el.svgChartVibration && el.tooltipVib) {
      el.svgChartVibration.addEventListener("mousemove", function(e) {
        const rect = el.svgChartVibration.getBoundingClientRect();
        const mouseX = e.clientX - rect.left;
        const pct = Math.max(0, Math.min(1, mouseX / rect.width));
        const val = (pct > 0.65 && state.systemStatus !== "HEALTHY") ? 1.85 : (0.28 + pct * 0.12);
        const status = val > 0.8 ? "ANOMALY" : "TRUSTED";

        el.tooltipVib.innerHTML = `Vib RMS: <strong>${val.toFixed(2)}g</strong> • ${status}`;
        el.tooltipVib.style.left = `${mouseX}px`;
        el.tooltipVib.style.top = `${e.clientY - rect.top}px`;
        el.tooltipVib.classList.add("show");
      });

      el.svgChartVibration.addEventListener("mouseleave", function() {
        el.tooltipVib.classList.remove("show");
      });
    }

    if (el.svgChartTemp && el.tooltipTemp) {
      el.svgChartTemp.addEventListener("mousemove", function(e) {
        const rect = el.svgChartTemp.getBoundingClientRect();
        const mouseX = e.clientX - rect.left;
        const pct = Math.max(0, Math.min(1, mouseX / rect.width));
        const temp = 45.0 + pct * 6.5;

        el.tooltipTemp.innerHTML = `Temp: <strong>${temp.toFixed(1)}°C</strong> • NOMINAL`;
        el.tooltipTemp.style.left = `${mouseX}px`;
        el.tooltipTemp.style.top = `${e.clientY - rect.top}px`;
        el.tooltipTemp.classList.add("show");
      });

      el.svgChartTemp.addEventListener("mouseleave", function() {
        el.tooltipTemp.classList.remove("show");
      });
    }
  }

  // =========================================================================
  // Event Listeners & Complete Element Binding
  // =========================================================================
  function setupEventListeners() {
    // 1. Navigation Rail Item Clicks
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

    // 2. Demo Toolbar Scene Triggers
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

    // 3. Evidence Drawer Controls & Backdrop
    const btnCloseDrawer = document.getElementById("btn-close-drawer");
    if (btnCloseDrawer) btnCloseDrawer.addEventListener("click", closeDrawer);

    if (el.drawerBackdrop) el.drawerBackdrop.addEventListener("click", closeDrawer);

    // Global Accessibility & Keyboard listener
    document.addEventListener("keydown", function(e) {
      if (e.key === "Escape") {
        closeDrawer();
      }
      if ((e.key === "Enter" || e.key === " ") && e.target && e.target.getAttribute("role") === "button") {
        e.preventDefault();
        e.target.click();
      }
    });

    // 4. KPI Cards Interactive Clicks
    if (el.cardKpiStatus) {
      el.cardKpiStatus.addEventListener("click", function() {
        openDrawer(state.currentReportId);
        showToast("Inspecting System Status Diagnostic Evidence.", false);
      });
    }

    if (el.cardKpiHealth) {
      el.cardKpiHealth.addEventListener("click", function() {
        openDrawer(state.currentReportId);
        showToast("Inspecting Health Score Evidence & Feature Vector.", false);
      });
    }

    if (el.cardKpiRisk) {
      el.cardKpiRisk.addEventListener("click", function() {
        openDrawer(state.currentReportId);
        showToast("Inspecting Anomaly Probability & Diagnosis.", false);
      });
    }

    if (el.cardKpiPriority) {
      el.cardKpiPriority.addEventListener("click", function() {
        switchView("view-maintenance");
        showToast("Navigated to MRO Maintenance Workbench.", false);
      });
    }

    if (el.cardKpiAlerts) {
      el.cardKpiAlerts.addEventListener("click", function() {
        switchView("view-provenance");
        showToast("Navigated to Cryptographic Provenance Evidence.", false);
      });
    }

    // 5. Central Engine Visual Sensors & Callouts
    const ptVib = document.getElementById("pulse-pt-vib");
    const coutVib = document.getElementById("callout-vib");
    const srowVib = document.getElementById("srow-vibration");
    [ptVib, coutVib, srowVib].forEach(function(node) {
      if (node) {
        node.addEventListener("click", function() {
          openDrawer(state.currentReportId);
          showToast("Inspecting ADXL345 Thrust Bearing Vibration Telemetry.", false);
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
          showToast("Inspecting MAX6675 Bearing Cap Thermal Telemetry.", false);
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
          showToast("Inspecting A3144 Hall-Effect Shaft RPM Telemetry.", false);
        });
      }
    });

    // 6. Gate B Sensor Table Rows in #view-sensors
    const stRowVib = document.getElementById("st-row-vib");
    if (stRowVib) {
      stRowVib.addEventListener("click", function() {
        openDrawer(state.currentReportId);
        showToast("Inspecting Gate B ADXL345 Vibration Trust Metrics.", false);
      });
    }

    const stRowTemp = document.getElementById("st-row-temp");
    if (stRowTemp) {
      stRowTemp.addEventListener("click", function() {
        openDrawer(state.currentReportId);
        showToast("Inspecting Gate B MAX6675 Temperature Trust Metrics.", false);
      });
    }

    const stRowRpm = document.getElementById("st-row-rpm");
    if (stRowRpm) {
      stRowRpm.addEventListener("click", function() {
        openDrawer(state.currentReportId);
        showToast("Inspecting Gate B A3144 RPM Trust Metrics.", false);
      });
    }

    // 7. Timeline Nodes Interaction (#tnode-1 to #tnode-9)
    for (let i = 1; i <= 9; i++) {
      const tnode = document.getElementById(`tnode-${i}`);
      if (tnode) {
        tnode.addEventListener("click", function() {
          state.selectedTimelineStage = i;
          renderTimelineNodes();

          if (i === 1) {
            openDrawer(state.currentReportId);
            showToast("Timeline Stage 1: Telemetry Ingest snapshot opened in drawer.", false);
          } else if (i === 2) {
            switchView("view-sensors");
            showToast("Timeline Stage 2: Gate B Sensor Trust Adjudication Panel.", false);
          } else if (i === 3) {
            openDrawer(state.currentReportId);
            showToast("Timeline Stage 3: Machine Learning Diagnostic Classification.", false);
          } else if (i === 4) {
            switchView("view-provenance");
            showToast("Timeline Stage 4: Device-Local HMAC-SHA256 Manifest Signing.", false);
          } else if (i === 5) {
            switchView("view-maintenance");
            showToast("Timeline Stage 5: MRO Maintenance Priority Dispatched.", false);
          } else if (i === 6) {
            switchView("view-maintenance");
            showToast("Timeline Stage 6: Mechanical Assembly Replacement & Torque.", false);
          } else if (i === 7) {
            openDrawer(state.currentReportId);
            showToast("Timeline Stage 7: Fresh Post-Maintenance Sensor Window.", false);
          } else if (i === 8) {
            openDrawer("clo-1fc447c2");
            showToast("Timeline Stage 8: Quantitative Repair Verification (Eff: 0.92).", false);
          } else if (i === 9) {
            switchView("view-passport");
            showToast("Timeline Stage 9: Signed Closure Record Appended to Digital Passport.", false);
          }
        });
      }
    }

    // 8. Workbench Action Buttons
    if (el.wbBtnStart) el.wbBtnStart.addEventListener("click", setScenarioMaintain);
    if (el.wbBtnRetest) el.wbBtnRetest.addEventListener("click", setScenarioRetest);
    if (el.wbBtnClose) el.wbBtnClose.addEventListener("click", closeMaintenanceWorkOrder);
    if (el.wbBtnEvidence) el.wbBtnEvidence.addEventListener("click", function() { openDrawer(state.currentReportId); });

    // 9. View CTAs
    const btnViewWb = document.getElementById("btn-view-workbench");
    const btnGotoMro = document.getElementById("btn-goto-mro");
    [btnViewWb, btnGotoMro].forEach(function(b) {
      if (b) {
        b.addEventListener("click", function() {
          switchView("view-maintenance");
        });
      }
    });

    const btnOpenAlertsEvidence = document.getElementById("btn-open-alerts-evidence");
    if (btnOpenAlertsEvidence) {
      btnOpenAlertsEvidence.addEventListener("click", function() {
        switchView("view-provenance");
      });
    }

    // 10. Provenance Page Buttons
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

    // 11. Header Badges as Functional Navigators
    if (el.badgeAiModel) {
      el.badgeAiModel.style.cursor = "pointer";
      el.badgeAiModel.addEventListener("click", function() {
        openDrawer(state.currentReportId);
        showToast("Inspecting Active Model Artifact Identity & Hash.", false);
      });
    }

    if (el.badgeConnectivity) {
      el.badgeConnectivity.style.cursor = "pointer";
      el.badgeConnectivity.addEventListener("click", function() {
        if (state.connectivity === "ONLINE") {
          setScenarioOffline();
        } else {
          setScenarioReconnect();
        }
      });
    }

    if (el.badgeProvenance) {
      el.badgeProvenance.style.cursor = "pointer";
      el.badgeProvenance.addEventListener("click", function() {
        switchView("view-provenance");
      });
    }

    if (el.filterPill) {
      el.filterPill.style.cursor = "pointer";
      el.filterPill.addEventListener("click", function() {
        if (state.streamMode.indexOf("Live") !== -1) {
          state.streamMode = "Benchmark Replay • Physical CWRU Stream";
        } else {
          state.streamMode = "Live Telemetry • Flight-Line Stream";
        }
        const span = el.filterPill.querySelector("span");
        if (span) span.textContent = state.streamMode;
        showToast(`Stream switched to: ${state.streamMode}`, false);
      });
    }

    if (el.txtEngineSub) {
      el.txtEngineSub.style.cursor = "pointer";
      el.txtEngineSub.addEventListener("click", function() {
        switchView("view-passport");
      });
    }

    // 12. Copy Buttons (Delegation with Visual Feedback)
    document.addEventListener("click", function(e) {
      if (e.target && e.target.classList.contains("btn-copy")) {
        const targetId = e.target.getAttribute("data-target");
        if (targetId) {
          const targetEl = document.getElementById(targetId);
          if (targetEl) {
            copyTextToClipboard(targetEl.textContent.trim(), e.target);
          }
        }
      }

      // Drawer trigger buttons inside tables
      if (e.target && e.target.classList.contains("btn-drawer-event")) {
        const repId = e.target.getAttribute("data-rep") || state.currentReportId;
        openDrawer(repId);
      }
    });

    // Alert rows click
    const alertRows = document.querySelectorAll(".clickable-alert-row");
    alertRows.forEach(function(row) {
      row.addEventListener("click", function() {
        openDrawer("rep-demo-002");
      });
    });

    // Passport table rows click
    const passportRows = document.querySelectorAll("#tbl-passport-full tr");
    passportRows.forEach(function(row) {
      row.style.cursor = "pointer";
      row.addEventListener("click", function(e) {
        if (e.target.tagName !== "BUTTON") {
          const btn = row.querySelector(".btn-drawer-event");
          if (btn) {
            const repId = btn.getAttribute("data-rep");
            openDrawer(repId);
          }
        }
      });
    });

    // 13. Initialize Chart Tooltips
    setupChartTooltips();
  }

  // =========================================================================
  // Initialization
  // =========================================================================
  setupEventListeners();
  render();

  // Automatic live sync with local WSGI server when served over HTTP
  if (typeof window !== "undefined" && window.fetch) {
    fetch("/health").then(function(res) {
      return res.json();
    }).then(function(data) {
      if (data && data.status) {
        state.systemStatus = data.status.toUpperCase();
        render();
      }
    }).catch(function() {
      // Standalone mode via file:// protocol
    });
  }
})();

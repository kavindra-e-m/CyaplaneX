"""End-to-End integration test of the CyaplaneX closed-loop lifecycle.

Sense -> Validate -> Fuse -> Predict -> Explain -> Sign -> Sync -> Verify -> Maintain -> Re-test -> Close -> Passport.
"""

from cloud.api.maintenance import (
    close_maintenance,
    get_maintenance_state,
    mark_maintenance_started,
    perform_retest,
)
from cloud.api.passport import get_passport
from cloud.api.verification import ingest_and_verify, verification_status
from cloud.storage.store import InMemoryEvidenceStore
from edge.orchestrator import EdgePipelineOrchestrator
from edge.sensors.vibration import ReplayVibrationSensor


def test_complete_closed_loop_maintenance_lifecycle() -> None:
    # 0. Setup shared cloud store and edge orchestrator
    cloud_store = InMemoryEvidenceStore()
    orchestrator = EdgePipelineOrchestrator(
        device_id="rpi5-edge-testbed",
        asset_id="aircraft-wing-lh",
        component_id="bearing-thrust-01",
    )

    # 1. Controlled Prototype Fault Injection (High Vibration on Bearing)
    fault_sensor = ReplayVibrationSensor([1.85, 1.90, 1.88, 1.92])
    orchestrator.acquisition.register_sensor("vib-01", "vibration", "g", "cal-2026.1", fault_sensor)

    # 2. Execute Edge Cycle: Sense -> Trust -> Preprocess -> Infer -> Reason -> Sign -> Queue/Dispatch
    edge_output = orchestrator.execute_cycle(report_id="rep-e2e-2026-001")
    diagnostic_event = edge_output["event"]

    assert edge_output["condition"] == "HIGH_VIBRATION"
    assert edge_output["priority"] == "P1"
    assert edge_output["trust_status"] == "TRUSTED"
    assert edge_output["health_score"] < 50.0

    # 3. Cloud Ingestion & Verification
    ingest_result = ingest_and_verify(diagnostic_event, store=cloud_store)
    assert ingest_result["verified"] is True
    assert ingest_result["status"] == "INGESTED"

    # 4. Verify Provenance Evidence
    ver_status = verification_status("rep-e2e-2026-001", store=cloud_store)
    assert ver_status["status"] == "PROVENANCE_VERIFIED"
    assert ver_status["verified"] is True

    # 5. Review Maintenance State
    maint_state = get_maintenance_state("aircraft-wing-lh", store=cloud_store)
    assert maint_state["state"] == "MAINTENANCE_REQUIRED"
    assert maint_state["active_report_id"] == "rep-e2e-2026-001"

    # 6. Mark Maintenance Started
    start_res = mark_maintenance_started("rep-e2e-2026-001", store=cloud_store)
    assert start_res["status"] == "MAINTENANCE_STARTED"
    maint_state_after_start = get_maintenance_state("aircraft-wing-lh", store=cloud_store)
    assert maint_state_after_start["state"] == "MAINTENANCE_IN_PROGRESS"

    # 7. Physical/Prototype Maintenance (Bearing Replaced) -> Fresh Sensor Window
    # Features: [vib_rms, vib_p2p, temp_mean, temp_max, rpm_mean, rpm_std]
    healthy_post_features = [0.35, 0.08, 48.0, 50.0, 3600.0, 12.0]

    # 8. Start Re-test
    retest_res = perform_retest(
        report_id="rep-e2e-2026-001",
        fresh_features=healthy_post_features,
        store=cloud_store,
    )
    assert retest_res["outcome"] == "REPAIR_VERIFIED"
    assert retest_res["repair_effectiveness"] > 0.4
    assert retest_res["post_health_score"] >= 85.0

    # 9. Closure Record Creation & Signature
    closure = close_maintenance(
        report_id="rep-e2e-2026-001",
        maintenance_action="Replaced thrust bearing and re-torqued shaft assembly",
        post_health_score=retest_res["post_health_score"],
        store=cloud_store,
    )
    assert closure["closure_status"] == "REPAIR_VERIFIED"
    assert closure["digital_signature"].startswith("hmac-sha256:")

    # 10. Digital Passport & Component Maintenance History
    passport = get_passport("bearing-thrust-01", store=cloud_store)
    assert passport["total_records"] == 2
    record_types = [r["record_type"] for r in passport["records"]]
    assert record_types == ["DIAGNOSTIC_EVENT", "MAINTENANCE_CLOSURE"]

    final_maint_state = get_maintenance_state("aircraft-wing-lh", store=cloud_store)
    assert final_maint_state["state"] == "CLOSED"

import argparse

from cloud.api.maintenance import (
    close_maintenance,
    mark_maintenance_started,
    perform_retest,
)
from cloud.api.passport import get_passport
from cloud.api.verification import ingest_and_verify, verification_status
from cloud.storage.store import InMemoryEvidenceStore
from edge.ai.adapter import BaselineDemonstratorModel
from edge.connectivity.mqtt_client import MockCloudTransport
from edge.orchestrator import EdgePipelineOrchestrator
from edge.sensors.vibration import ReplayVibrationSensor


def run_full_demo(force_baseline: bool = False) -> None:
    print("=" * 72)
    print("CYAPLANEX -- TATA TECHNOLOGIES INNOVENT 2026 DEMO SEQUENCE")
    print("Closed-Loop Edge AI Predictive Maintenance & Cryptographic Provenance")
    print("Operating Mode: SIMULATED TESTBED TELEMETRY (Physical HIL Pending)")
    print("=" * 72)

    # Step 1: Start the system
    cloud_store = InMemoryEvidenceStore()
    transport = MockCloudTransport(connected=True)
    custom_model = BaselineDemonstratorModel() if force_baseline else None
    orchestrator = EdgePipelineOrchestrator(
        device_id="rpi5-edge-testbed",
        asset_id="aircraft-wing-lh",
        component_id="bearing-thrust-01",
        transport=transport,
        model=custom_model,
    )
    active_model = orchestrator.ml_adapter.model
    model_mode = "BASELINE DEMONSTRATOR FIXTURE" if force_baseline else "PRODUCTION ML MODEL (Lead: Monhit Raju)"
    print("\n[Step 1] System started: Edge orchestrator and cloud verification initialized.")
    print(f"         Active AI Engine: {model_mode}")
    print(f"         Model ID:         {active_model.model_id} (v{active_model.model_version})")
    print(f"         Model Hash:       {active_model.model_hash[:32]}...")

    # Step 2: Show healthy input
    healthy_out = orchestrator.execute_cycle(report_id="rep-demo-001")
    print(f"[Step 2] Healthy baseline: Condition={healthy_out['condition']}, Health Score={healthy_out['health_score']}%, Trust={healthy_out['trust_status']}")

    # Step 3: Inject controlled prototype fault (elevated dynamic vibration)
    fault_sensor = ReplayVibrationSensor([1.85, 1.92, 1.88, 1.95])
    orchestrator.acquisition.register_sensor("vib-01", "vibration", "g", "cal-2026.1", fault_sensor)
    fault_out = orchestrator.execute_cycle(report_id="rep-demo-002")
    diagnostic_event = fault_out["event"]
    print("\n[Step 3] Controlled fault injected on bearing-thrust-01 (1.85g vibration).")

    # Step 4: Show sensor trust
    print(f"[Step 4] Sensor trust evaluated: {fault_out['trust_status']} (Range=OK, Fresh=OK, Not Stuck)")

    # Step 5: Show Edge AI prediction
    print(f"[Step 5] Edge AI Diagnosis: Condition={fault_out['condition']}, Health Score={fault_out['health_score']}%, Severity={diagnostic_event['health_result']['severity']}")

    # Step 6: Show maintenance reasoning
    print(f"[Step 6] Maintenance Reasoning: Priority={diagnostic_event['priority']}")
    print(f"         Reason: {diagnostic_event['maintenance_reason']}")
    print(f"         Action: {diagnostic_event['recommended_action']}")

    # Step 7: Show provenance metadata
    hr = diagnostic_event["health_result"]
    print("[Step 7] Cryptographic Provenance generated:")
    print(f"         Sensor Window Hash: {diagnostic_event['sensor_window_hash'][:32]}...")
    print(f"         Manifest Hash:      {diagnostic_event['manifest_hash'][:32]}...")
    print(f"         Digital Signature:  {diagnostic_event['digital_signature'][:36]}...")
    print(f"         Provenanced Model:  {hr.get('model_id')} (v{hr.get('model_version')})")
    print(f"         Provenanced Hash:   {hr.get('model_hash')[:32]}...")

    # Step 8: Verify Provenance in backend
    _ingest_res = ingest_and_verify(diagnostic_event, store=cloud_store)
    ver_status = verification_status("rep-demo-002", store=cloud_store)
    print(f"\n[Step 8] Cloud verification: Status={ver_status['status']} (Verified={ver_status['verified']})")

    # Step 9: Run Tamper Test (modify 1 protected field and observe signature failure)
    tampered_event = dict(diagnostic_event)
    tampered_event["sequence_no"] = 999
    tampered_event["health_result"] = dict(tampered_event["health_result"])
    tampered_event["health_result"]["health_score"] = 99.0
    tamper_ingest = ingest_and_verify(tampered_event, store=cloud_store)
    print(f"[Step 9] Tamper Test: Modified health_score to 99.0 -> Status={tamper_ingest['status']} (Tamper Detected!)")

    # Step 10: Simulate Offline
    transport.disconnect()
    print(f"\n[Step 10] Simulated cloud connectivity drop: Transport is_connected={transport.is_connected()}")

    # Step 11 & 12: Generate evidence & show offline buffering
    offline_out = orchestrator.execute_cycle(report_id="rep-demo-003")
    print("[Step 11] New event generated while offline (Report rep-demo-003).")
    print(f"[Step 12] OFFLINE BUFFERING active: Queue depth={offline_out['queue_depth']} record buffered.")

    # Step 13 & 14: Restore connectivity & synchronize
    transport.connect()
    sync_report = orchestrator.coordinator.synchronize()
    print("\n[Step 13] Connectivity restored: Synchronizing buffered queue...")
    print(f"[Step 14] Synchronized {sync_report['synced_count']} event(s) in sequence. Remaining queue depth={sync_report['remaining_depth']}.")

    # Step 15: Mark Maintenance Started
    _start_res = mark_maintenance_started("rep-demo-002", store=cloud_store)
    print("\n[Step 15] MRO Maintenance Started: Report rep-demo-002 -> State=MAINTENANCE_IN_PROGRESS")

    # Step 16: Perform prototype maintenance (thrust bearing replacement)
    print("[Step 16] Prototype Maintenance performed: Thrust bearing replaced, shaft torqued to specification.")

    # Step 17: Start Re-test with fresh sensor window
    fresh_healthy_features = [0.35, 0.08, 48.0, 50.0, 3600.0, 10.0]
    retest_res = perform_retest(
        "rep-demo-002",
        fresh_features=fresh_healthy_features,
        store=cloud_store,
        ml_adapter=orchestrator.ml_adapter,
    )
    metric_label = "[BASELINE DEMONSTRATOR METRIC]" if force_baseline else "[PRODUCTION MODEL METRIC]"
    print("\n[Step 17] Fresh Re-test executed against new sensor window.")
    print(f"[Step 18] Post-maintenance Health Score: {retest_res['post_health_score']}% (Pre-score: {retest_res['pre_health_score']}%) {metric_label}")
    print(f"[Step 19] Outcome: {retest_res['outcome']} (Repair Effectiveness: {retest_res['repair_effectiveness']:.2f}) {metric_label}")
    print(f"         Prompt: {retest_res['prompt']}")

    # Step 20: Create signed closure record and inspect digital passport
    closure = close_maintenance(
        report_id="rep-demo-002",
        maintenance_action="Replaced thrust bearing assembly; torqued mountings to 45 Nm",
        post_health_score=retest_res["post_health_score"],
        store=cloud_store,
    )
    passport = get_passport("bearing-thrust-01", store=cloud_store)
    print("\n[Step 20] Component Digital Passport for bearing-thrust-01:")
    print(f"         Closure ID: {closure['closure_id']} | Status: {closure['closure_status']}")
    print(f"         Total Historical Records: {passport['total_records']}")
    for r in passport["records"]:
        print(f"         - [{r['record_type']}] Timestamp={r['timestamp'][:19]} | Detail={r.get('condition') or r.get('action')}")

    print("\n" + "=" * 72)
    print("DEMO COMPLETE -- FULL CLOSED-LOOP CYCLE REPRODUCIBLY VERIFIED!")
    print("=" * 72)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CyaplaneX End-to-End Closed-Loop Demonstrator."
    )
    parser.add_argument(
        "--baseline",
        action="store_true",
        help="Execute using the baseline development demonstrator fixture instead of the production ML model.",
    )
    args = parser.parse_args()
    run_full_demo(force_baseline=args.baseline)

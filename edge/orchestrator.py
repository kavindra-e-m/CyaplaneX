"""Edge runtime pipeline orchestrator.

Executes the closed-loop edge pipeline:
Sense -> Validate Trust -> Preprocess/Window -> Infer Health -> Reason Maintenance -> Build Manifest -> Sign -> Dispatch/Queue.
"""
from __future__ import annotations

from typing import Any

from edge.ai.adapter import EdgeMLAdapter
from edge.connectivity.mqtt_client import CloudTransport, MockCloudTransport
from edge.connectivity.queue import OfflineQueue
from edge.connectivity.sync import SyncCoordinator
from edge.maintenance.reasoning_engine import MaintenanceReasoningEngine
from edge.preprocessing.pipeline import FeaturePipeline
from edge.provenance.manifest import assemble_maintenance_event, build_manifest
from edge.provenance.signer import DeviceLocalSigner
from edge.sensor_trust.engine import SensorTrustEngine
from edge.sensors.acquisition import SensorAcquisitionService
from edge.sensors.rpm import SimulatedRpmSensor
from edge.sensors.temperature import SimulatedTemperatureSensor
from edge.sensors.vibration import SimulatedVibrationSensor


class EdgePipelineOrchestrator:
    """Coordinates edge subsystems through the closed-loop diagnostic cycle."""

    def __init__(
        self,
        device_id: str = "rpi5-edge-01",
        asset_id: str = "aircraft-wing-lh",
        component_id: str = "bearing-thrust-01",
        transport: CloudTransport | None = None,
        queue: OfflineQueue | None = None,
        model: Any | None = None,
    ) -> None:
        self.device_id = device_id
        self.asset_id = asset_id
        self.component_id = component_id

        # Edge services
        self.acquisition = SensorAcquisitionService(device_id=device_id)
        self.trust_engine = SensorTrustEngine()
        self.feature_pipeline = FeaturePipeline()
        if model is None:
            try:
                from ml.export.model import ProductionModel
                resolved_model = ProductionModel()
            except (ImportError, OSError, ValueError):
                resolved_model = None
        else:
            resolved_model = model

        self.ml_adapter = EdgeMLAdapter(model=resolved_model)
        self.reasoning_engine = MaintenanceReasoningEngine()
        self.signer = DeviceLocalSigner()

        # Connectivity & Queuing
        self.queue = queue or OfflineQueue()
        self.transport = transport or MockCloudTransport(connected=True)
        self.coordinator = SyncCoordinator(queue=self.queue, transport=self.transport)

        # Pipeline state tracking
        self.sequence_no: int = 0
        self.last_manifest_hash: str = "0" * 64

        # Register standard simulated sensors by default
        self._setup_default_sensors()

    def _setup_default_sensors(self) -> None:
        self.acquisition.register_sensor(
            "vib-01", "vibration", "g", "cal-2026.1", SimulatedVibrationSensor(baseline=0.35)
        )
        self.acquisition.register_sensor(
            "temp-01", "temperature", "degC", "cal-2026.1", SimulatedTemperatureSensor(baseline=52.0)
        )
        self.acquisition.register_sensor(
            "rpm-01", "rpm", "rpm", "cal-2026.1", SimulatedRpmSensor(target_rpm=3600.0)
        )

    def execute_cycle(
        self,
        report_id: str,
        custom_samples: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """Execute one complete edge cycle from sensor readings to signed event dispatch."""
        # 1. Sense (Acquisition)
        if custom_samples:
            samples = custom_samples
        else:
            # Collect multiple readings to form a window
            samples = []
            for _ in range(4):
                samples.extend(self.acquisition.acquire_all())

        # 2. Validate (Sensor Trust)
        trust_results = [self.trust_engine.evaluate_sample(s) for s in samples]
        composite_trust = self.trust_engine.aggregate_trust(trust_results)

        # 3. Fuse & Preprocess (Windowing & Feature Extraction)
        window = self.feature_pipeline.process_window(samples)

        # 4. Predict (ML Health Engine)
        health_result = self.ml_adapter.infer(window.features)

        # 5. Explain (Maintenance Reasoning)
        assessment = self.reasoning_engine.evaluate(
            health_result=health_result,
            sensor_trust=composite_trust,
            component_id=self.component_id,
            asset_id=self.asset_id,
        )

        # 6. Build Deterministic Manifest
        self.sequence_no += 1
        manifest = build_manifest(
            report_id=report_id,
            asset_id=self.asset_id,
            component_id=self.component_id,
            sensor_window_hash=window.sensor_window_hash,
            sensor_trust=composite_trust,
            health_result=health_result.to_dict(),
            maintenance_reason=assessment.maintenance_reason,
            recommended_action=assessment.recommended_action,
            priority=assessment.priority,
            device_id=self.device_id,
            sequence_no=self.sequence_no,
            previous_record_hash=self.last_manifest_hash,
        )

        # 7. Sign Locally
        signature = self.signer.sign_manifest(manifest)
        event = assemble_maintenance_event(manifest, signature)
        self.last_manifest_hash = str(manifest["manifest_hash"])

        # 8. Dispatch / Offline Queue
        dispatch_res = self.coordinator.handle_event(event)

        return {
            "event": event,
            "dispatch": dispatch_res,
            "health_score": health_result.health_score,
            "condition": health_result.condition,
            "priority": assessment.priority,
            "trust_status": composite_trust["trust_status"],
            "queue_depth": len(self.queue),
        }

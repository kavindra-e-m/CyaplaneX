# Data Contracts — CyaplaneX

Canonical JSON Schemas live in `shared/schemas/` for SensorSample, SensorTrustResult, HealthResult, MaintenanceEvent, and ClosureRecord. Contract changes require versioning, compatibility review, and updates to edge, cloud, dashboard, and tests.

The maintenance event includes sensor-window hash, model identity/version/hash, device and sequence metadata, nonce, timestamp, previous record hash, manifest hash, and digital signature for provenance.


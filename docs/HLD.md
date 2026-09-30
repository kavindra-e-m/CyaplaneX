# High-Level Design (HLD) — CyaplaneX

## Scope
CyaplaneX is a trusted closed-loop Edge AI predictive maintenance demonstrator for aerospace engineering. The architecture strictly separates sensor acquisition, sensor trust, edge intelligence, provenance, connectivity, local/cloud verification, and MRO workflow.

## Data Path
Sensors -> Sensor Trust -> Preprocessing/Fusion -> Model Adapters -> Maintenance Reasoning -> Local Provenance (HMAC-SHA256) -> Offline Queue -> Cloud Transport -> Verification API -> Evidence Store -> MRO Dashboard -> Repair Re-test -> Closure Record -> Digital Passport.

## Infrastructure Status
- **IMPLEMENTED LOCALLY:** In-memory evidence store, local WSGI REST API server, cryptographic verifier, and offline synchronization coordinator.
- **TARGET AWS ARCHITECTURE:** AWS IoT Greengrass v2 (edge runtime), AWS IoT Core (MQTT broker), Amazon S3 (evidence archive), Amazon Timestream (telemetry metrics), and AWS KMS (cloud key management).
- **LIVE AWS DEPLOYMENT:** PENDING / NOT DEPLOYED. Local demonstrator operates independently without requiring live AWS infrastructure.

## Security Posture
The edge signs evidence locally via device-local HMAC-SHA256 and remains functional without cloud connectivity. Cloud KMS is reserved for cloud-side key governance. Monotonic sequence, timestamp, nonce, sensor-window hash, model metadata, and previous-record hash guarantee cryptographically verifiable and tamper-evident lineage.


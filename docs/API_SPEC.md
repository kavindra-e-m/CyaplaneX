# API Specification — CyaplaneX Verification & Maintenance API

The CyaplaneX Cloud API is a framework-neutral WSGI application implemented in `cloud/api/app.py` running on port 8000.

## 1. System Health
- **Endpoint:** `GET /health`
- **Response:**
  ```json
  {
    "status": "ok",
    "service": "cyaplanex-verification-api"
  }
  ```

## 2. Cryptographic Provenance & Ingestion
- **Endpoint:** `POST /verification/events`
- **Request Body:** JSON `MaintenanceEvent` object conforming to `shared/schemas/maintenance_event.schema.json`.
- **Response (200 OK):**
  ```json
  {
    "verified": true,
    "report_id": "rep-demo-002",
    "status": "PROVENANCE_VERIFIED",
    "message": "Signature verified and replay sequence accepted."
  }
  ```
- **Error Responses:**
  - `400 Bad Request`: Payload tampering detected (`PROVENANCE_VIOLATION`) or schema validation failure.
  - `409 Conflict`: Non-monotonic sequence or duplicate sequence (`REPLAY_REJECTED`).

- **Endpoint:** `GET /verification/{report_id}`
- **Response (200 OK):** Detailed verification record including signature status, manifest hash, sequence, model hash, and verification timestamp.

## 3. Maintenance Closed Loop
- **Endpoint:** `GET /maintenance/{asset_id}`
- **Response (200 OK):** Current asset maintenance state (`HEALTHY`, `MAINTENANCE_REQUIRED`, `MAINTENANCE_IN_PROGRESS`, `REPAIR_VERIFIED`) and active report ID.

- **Endpoint:** `POST /maintenance/{report_id}/start`
- **Response (200 OK):** Transitions state to `MAINTENANCE_IN_PROGRESS`.

- **Endpoint:** `POST /maintenance/retest`
- **Request Body:**
  ```json
  {
    "report_id": "rep-demo-002",
    "fresh_features": [0.35, 0.08, 48.0, 50.0, 3600.0, 10.0]
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "report_id": "rep-demo-002",
    "pre_health_score": 6.2,
    "post_health_score": 100.0,
    "repair_effectiveness": 0.94,
    "outcome": "REPAIR_VERIFIED",
    "post_condition": "HEALTHY",
    "prompt": "Post-maintenance evidence meets the configured repair-verification rule. Closure record can be created."
  }
  ```

- **Endpoint:** `POST /maintenance/closure`
- **Request Body:**
  ```json
  {
    "report_id": "rep-demo-002",
    "maintenance_action": "Replaced thrust bearing and re-torqued shaft",
    "post_health_score": 100.0
  }
  ```
- **Response (200 OK):** Returns signed `ClosureRecord` with `closure_id`, `digital_signature`, and `repair_effectiveness: 0.94`.

## 4. Digital Passport
- **Endpoint:** `GET /passport/{component_id}`
- **Response (200 OK):** Chronological, append-only history of diagnostic events and signed closure records for the component.


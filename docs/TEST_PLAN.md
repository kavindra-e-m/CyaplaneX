# Test Plan & Verification Strategy — CyaplaneX

CyaplaneX maintains a 47-test automated suite executed via pytest (`uv run pytest -v`).

## Test Coverage Layers
1. **Contracts (`tests/unit/test_contracts.py`):** 14 tests validating all Draft 2020-12 JSON schemas (positive, missing field, out-of-range, additional properties).
2. **Sensor Acquisition (`tests/unit/test_sensor_acquisition.py`):** 6 tests validating simulated and replay generators and acquisition registry.
3. **Sensor Trust (`tests/unit/test_sensor_trust_engine.py`, `test_sensor_checks.py`):** 8 tests validating range boundaries, freshness degradation, stuck detection, consensus drift, and multi-sensor aggregation.
4. **Preprocessing & Model Boundary (`tests/unit/test_ml_and_preprocessing.py`, `test_health_result.py`):** 5 tests validating 6-feature statistical window extraction, deterministic window hashing, and `EdgeMLAdapter` health evaluation.
5. **Provenance & Connectivity (`tests/unit/test_provenance_and_connectivity.py`):** 4 tests validating canonical JSON manifests, HMAC signing/verification, FIFO queue capacity, and offline sync.
6. **Security & Tamper Abuse (`tests/security/`):** 4 tests validating key-order independence, 100% tamper detection (`PROVENANCE_VIOLATION`), and replay sequence rejection (`REPLAY_REJECTED`).
7. **Cloud Verification & Maintenance API (`tests/integration/`):** 5 tests asserting WSGI REST endpoints (`/health`, `/verification/events`, `/maintenance/*`, `/passport/*`).
8. **Closed-Loop Lifecycle (`tests/e2e/test_closed_loop_lifecycle.py`):** Complete E2E integration test verifying fault -> diagnosis -> maintenance -> fresh re-test -> repair effectiveness (0.94) -> signed closure.


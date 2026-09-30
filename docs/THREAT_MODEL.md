# Threat Model — CyaplaneX

## Assets
Sensor evidence, model metadata, maintenance decisions, signatures, keys, sequence state, cloud records, and component history.

## Threats
Sensor spoofing or failure, stale/replayed events, modified payloads, lost connectivity, credential leakage, model mismatch, unauthorized maintenance updates, and cloud-side tampering.

## Controls
- Multi-check sensor trust engine (range, freshness, stuck, drift, consensus).
- Device-local HMAC-SHA256 provenance signing for offline tamper-evidence demonstration.
- Zero credential leakage: no live AWS credentials or hardcoded private secrets in repository.
- Monotonic sequence tracking and replay rejection guard.
- Cryptographic sensor-window and model metadata hashes in canonical manifest.
- Tamper-evident append-only digital passport.

## Boundaries & Limitations
Current implementation uses device-local HMAC-SHA256. Production key custody, asymmetric signatures (e.g. ECDSA/Ed25519), and hardware HSM integration remain target architecture enhancements.


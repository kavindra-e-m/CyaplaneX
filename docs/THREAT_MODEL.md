# Threat Model

## Assets
Sensor evidence, model metadata, maintenance decisions, signatures, keys, sequence state, cloud records, and component history.

## Threats
Sensor spoofing or failure, stale/replayed events, modified payloads, lost connectivity, credential leakage, model mismatch, unauthorized maintenance updates, and cloud-side tampering.

## Controls
Range/freshness/stuck/drift/consensus checks; local signing; no hardcoded private keys or AWS credentials; nonce/timestamp/sequence replay fields; sensor-window and model hashes; chain verification; least-privilege deployment; protected branches and architecture review.

Production key custody, asymmetric signature implementation, device identity, rotation, and incident response are TODOs.

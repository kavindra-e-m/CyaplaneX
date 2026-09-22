# Demo Script

1. Run `python scripts/seed_mock_data.py` to show healthy, warning, and critical telemetry.
2. Run `python scripts/tamper_test.py` to show a valid event becoming invalid after one field changes.
3. Run `python scripts/replay_test.py` to show duplicate and old sequence rejection.
4. Explain offline buffering and local signing boundaries.
5. Walk through dashboard states: sensor failure, offline buffering, provenance verified/violation, maintenance required, repair verified, and re-inspection required.

The demo is a scaffold demonstration, not a production or aircraft-certification claim.

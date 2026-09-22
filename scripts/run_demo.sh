#!/usr/bin/env bash
set -euo pipefail
# TODO: Start local MQTT and any future mock storage services.
# Optional services: docker compose --profile demo up -d
python scripts/seed_mock_data.py
python scripts/tamper_test.py
python scripts/replay_test.py

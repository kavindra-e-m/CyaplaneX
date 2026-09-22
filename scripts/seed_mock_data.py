"""Generate simple mock telemetry states for local demonstrations."""
import json


def build_samples() -> list[dict[str, object]]:
    """Return representative healthy, warning, and critical records."""
    return [
        {"state": "HEALTHY", "health_score": 96, "sensor_trust": "TRUSTED"},
        {"state": "WARNING", "health_score": 68, "sensor_trust": "TRUSTED"},
        {"state": "CRITICAL", "health_score": 21, "sensor_trust": "DEGRADED"},
    ]


if __name__ == "__main__":
    print(json.dumps(build_samples(), indent=2))

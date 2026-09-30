"""Maintenance action recommendation module."""


def recommend_action(condition: str, severity: str, sensor_trust_status: str, component_id: str) -> str:
    """Return prototype engineering action recommendation."""
    if sensor_trust_status == "FAILED":
        return f"Inspect, calibrate, or replace physical telemetry probe for {component_id}."

    if condition == "HEALTHY":
        return f"Continue scheduled monitoring for {component_id}."
    if condition == "HIGH_VIBRATION":
        if severity == "CRITICAL":
            return f"Halt test-rig rotation; inspect {component_id} mountings, shaft alignment, and bearing race for spalling."
        return f"Schedule visual inspection of {component_id} and verify fastening torque."
    if condition == "OVERHEATING":
        return f"Inspect thermal dissipation, check lubrication level and coolant flow on {component_id}."
    if condition == "SPEED_INSTABILITY":
        return f"Check drive coupling and motor controller feedback loop for {component_id}."
    if condition == "MECHANICAL_WEAR":
        return f"Perform acoustic emission and vibration spectral analysis on {component_id}."

    return f"Perform engineering inspection on {component_id}."

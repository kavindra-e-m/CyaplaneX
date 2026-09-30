"""Explainable maintenance reasoning module."""


def explain_condition(condition: str, severity: str, sensor_trust_status: str, component_id: str) -> str:
    """Generate engineering explanation for observed component state and sensor trust context."""
    if sensor_trust_status == "FAILED":
        return f"Telemetry trust FAILED for {component_id}. Evidence is insufficient for predictive maintenance diagnosis."

    if condition == "HEALTHY":
        return f"Component {component_id} operates within expected parameters with {sensor_trust_status} sensor evidence."
    if condition == "HIGH_VIBRATION":
        return f"Elevated dynamic vibration detected on {component_id} with severity {severity}; harmonic excitation or bearing defect suspected."
    if condition == "OVERHEATING":
        return f"Thermal envelope exceeded on {component_id} with severity {severity}; lubrication breakdown or friction suspected."
    if condition == "SPEED_INSTABILITY":
        return f"Rotational speed instability observed on {component_id}; shaft coupling or drive governor variance suspected."
    if condition == "MECHANICAL_WEAR":
        return f"Composite mechanical wear signatures detected on {component_id} with severity {severity}."

    return f"Condition '{condition}' flagged on {component_id} with severity {severity}."

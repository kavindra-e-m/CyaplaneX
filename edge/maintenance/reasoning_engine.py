"""Comprehensive maintenance reasoning engine.

Fuses SensorTrustResult, HealthResult, and asset context into actionable, explainable
maintenance recommendations and priority assignments.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from edge.ai.health_engine import HealthResult
from edge.maintenance.priority import prioritize
from edge.maintenance.reasoner import explain_condition
from edge.maintenance.recommendation import recommend_action


@dataclass(frozen=True)
class MaintenanceAssessment:
    """Outcome of maintenance reasoning."""
    maintenance_reason: str
    recommended_action: str
    priority: str
    requires_action: bool
    evidence_context: dict[str, Any]


class MaintenanceReasoningEngine:
    """Engine translating diagnostic and sensor trust state into maintenance advice."""

    def evaluate(
        self,
        health_result: HealthResult | dict[str, Any],
        sensor_trust: dict[str, Any],
        component_id: str,
        asset_id: str,
    ) -> MaintenanceAssessment:
        """Evaluate inputs and generate a structured MaintenanceAssessment."""
        h_dict = health_result.to_dict() if isinstance(health_result, HealthResult) else health_result

        condition = str(h_dict.get("condition", "UNKNOWN"))
        severity = str(h_dict.get("severity", "HEALTHY"))
        trust_status = str(sensor_trust.get("trust_status", "TRUSTED"))

        # Base priority from health severity
        base_priority = prioritize(severity)
        if trust_status == "FAILED":
            # If sensor trust failed, raise probe check priority
            priority = "P2" if base_priority == "P3" else base_priority
            requires_action = True
        elif severity in ("CRITICAL", "WARNING") or condition != "HEALTHY":
            priority = base_priority
            requires_action = True
        else:
            priority = "P3"
            requires_action = False

        reason = explain_condition(
            condition=condition,
            severity=severity,
            sensor_trust_status=trust_status,
            component_id=component_id,
        )

        action = recommend_action(
            condition=condition,
            severity=severity,
            sensor_trust_status=trust_status,
            component_id=component_id,
        )

        evidence_context = {
            "asset_id": asset_id,
            "component_id": component_id,
            "condition": condition,
            "severity": severity,
            "health_score": h_dict.get("health_score"),
            "model_id": h_dict.get("model_id"),
            "model_hash": h_dict.get("model_hash"),
            "sensor_trust_status": trust_status,
        }

        return MaintenanceAssessment(
            maintenance_reason=reason,
            recommended_action=action,
            priority=priority,
            requires_action=requires_action,
            evidence_context=evidence_context,
        )

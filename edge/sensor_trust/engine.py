"""Sensor trust engine.

Evaluates sensor samples against range, freshness, stuck-value, drift, and consensus rules,
producing contract-compliant SensorTrustResult payloads.
"""
from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from edge.sensor_trust.consensus import consensus_score
from edge.sensor_trust.drift_check import drift_suspected
from edge.sensor_trust.freshness import is_fresh
from edge.sensor_trust.range_check import validate_range
from edge.sensor_trust.stuck_check import is_stuck
from shared.contracts import SchemaName, TrustStatus, ensure_valid


@dataclass(frozen=True)
class SensorTrustLimits:
    """Configurable boundaries for a sensor type."""
    min_value: float
    max_value: float
    max_age_seconds: float = 10.0
    stuck_threshold: int = 4
    drift_threshold: float = 0.5
    consensus_allowed_spread: float = 1.0


DEFAULT_LIMITS: dict[str, SensorTrustLimits] = {
    "vibration": SensorTrustLimits(min_value=-5.0, max_value=5.0, drift_threshold=0.8, consensus_allowed_spread=0.5),
    "temperature": SensorTrustLimits(min_value=-20.0, max_value=120.0, drift_threshold=5.0, consensus_allowed_spread=4.0),
    "rpm": SensorTrustLimits(min_value=0.0, max_value=10000.0, drift_threshold=200.0, consensus_allowed_spread=100.0),
}


class SensorTrustEngine:
    """Evaluates sensor readings and maintains trust state."""

    def __init__(self, limits: dict[str, SensorTrustLimits] | None = None) -> None:
        self.limits = limits or DEFAULT_LIMITS
        self._history: dict[str, list[float]] = defaultdict(list)
        self._max_history: int = 20

    def evaluate_sample(
        self,
        sample: dict[str, Any],
        redundant_values: Sequence[float] | None = None,
        now: datetime | None = None,
    ) -> dict[str, Any]:
        """Evaluate a SensorSample dictionary and return a validated SensorTrustResult."""
        sensor_id = str(sample["sensor_id"])
        sensor_type = str(sample.get("sensor_type", "vibration"))
        val = float(sample["value"])
        raw_ts = sample["timestamp"]

        # Parse timestamp
        if isinstance(raw_ts, str):
            ts = datetime.fromisoformat(raw_ts)
        else:
            ts = raw_ts

        # Append to rolling history
        hist = self._history[sensor_id]
        hist.append(val)
        if len(hist) > self._max_history:
            hist.pop(0)

        # Retrieve limits
        limits = self.limits.get(sensor_type, DEFAULT_LIMITS["vibration"])

        # 1. Range check
        range_valid = validate_range(val, (limits.min_value, limits.max_value))

        # 2. Freshness check
        fresh = is_fresh(ts, max_age_seconds=limits.max_age_seconds, now=now)

        # 3. Stuck check
        stuck = is_stuck(hist, minimum_repeated=limits.stuck_threshold) if len(hist) >= limits.stuck_threshold else False

        # 4. Drift check
        drift = drift_suspected(hist, threshold=limits.drift_threshold)

        # 5. Consensus check
        c_score = consensus_score(
            redundant_values or [val],
            max_allowed_spread=limits.consensus_allowed_spread,
        )

        # Determine overall trust status
        if not range_valid or not fresh:
            trust_status = TrustStatus.FAILED.value
        elif stuck or drift or c_score < 0.5:
            trust_status = TrustStatus.DEGRADED.value
        else:
            trust_status = TrustStatus.TRUSTED.value

        result: dict[str, Any] = {
            "sensor_id": sensor_id,
            "trust_status": trust_status,
            "range_valid": bool(range_valid),
            "fresh": bool(fresh),
            "stuck": bool(stuck),
            "drift_suspected": bool(drift),
            "consensus_score": float(c_score),
        }

        ensure_valid(result, SchemaName.SENSOR_TRUST)
        return result

    def aggregate_trust(self, results: Sequence[dict[str, Any]]) -> dict[str, Any]:
        """Aggregate multiple SensorTrustResults into a unified subsystem trust state."""
        if not results:
            return {
                "sensor_id": "composite",
                "trust_status": TrustStatus.FAILED.value,
                "range_valid": False,
                "fresh": False,
                "stuck": False,
                "drift_suspected": False,
                "consensus_score": 0.0,
            }

        statuses = [r["trust_status"] for r in results]
        if TrustStatus.FAILED.value in statuses:
            overall = TrustStatus.FAILED.value
        elif TrustStatus.DEGRADED.value in statuses:
            overall = TrustStatus.DEGRADED.value
        else:
            overall = TrustStatus.TRUSTED.value

        all_range_valid = all(r["range_valid"] for r in results)
        all_fresh = all(r["fresh"] for r in results)
        any_stuck = any(r["stuck"] for r in results)
        any_drift = any(r["drift_suspected"] for r in results)
        avg_consensus = sum(r["consensus_score"] for r in results) / len(results)

        composite: dict[str, Any] = {
            "sensor_id": "composite",
            "trust_status": overall,
            "range_valid": all_range_valid,
            "fresh": all_fresh,
            "stuck": any_stuck,
            "drift_suspected": any_drift,
            "consensus_score": round(avg_consensus, 4),
        }

        ensure_valid(composite, SchemaName.SENSOR_TRUST)
        return composite

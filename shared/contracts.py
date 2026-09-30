"""Shared contract validator and typed lifecycle constants.

Provides deterministic validation against shared JSON schemas in shared/schemas/.
"""
from __future__ import annotations

import json
from enum import Enum
from pathlib import Path
from typing import Any

import jsonschema

SCHEMAS_DIR = Path(__file__).resolve().parent / "schemas"


class SchemaName(str, Enum):
    SENSOR_SAMPLE = "sensor_sample.schema.json"
    SENSOR_TRUST = "sensor_trust.schema.json"
    HEALTH_RESULT = "health_result.schema.json"
    MAINTENANCE_EVENT = "maintenance_event.schema.json"
    CLOSURE_RECORD = "closure_record.schema.json"


class TrustStatus(str, Enum):
    TRUSTED = "TRUSTED"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"


class HealthSeverity(str, Enum):
    HEALTHY = "HEALTHY"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class ClosureStatus(str, Enum):
    VERIFIED = "REPAIR_VERIFIED"
    RE_INSPECTION_REQUIRED = "RE_INSPECTION_REQUIRED"


_SCHEMA_CACHE: dict[str, dict[str, Any]] = {}


def load_schema(schema_name: str | SchemaName) -> dict[str, Any]:
    """Load and cache a JSON schema from shared/schemas/."""
    key = schema_name.value if isinstance(schema_name, SchemaName) else schema_name
    if key not in _SCHEMA_CACHE:
        schema_path = SCHEMAS_DIR / key
        if not schema_path.is_file():
            raise FileNotFoundError(f"Schema not found: {schema_path}")
        with open(schema_path, "r", encoding="utf-8") as f:
            _SCHEMA_CACHE[key] = json.load(f)
    return _SCHEMA_CACHE[key]


def validate_contract(payload: dict[str, Any], schema_name: str | SchemaName) -> tuple[bool, str | None]:
    """Validate a payload against the specified schema.

    Returns:
        (True, None) if valid.
        (False, error_message) if invalid.
    """
    schema = load_schema(schema_name)
    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
    if errors:
        return False, errors[0].message
    return True, None


def ensure_valid(payload: dict[str, Any], schema_name: str | SchemaName) -> None:
    """Validate payload, raising jsonschema.ValidationError if invalid."""
    is_valid, error_msg = validate_contract(payload, schema_name)
    if not is_valid:
        raise jsonschema.ValidationError(error_msg or "Contract validation failed")

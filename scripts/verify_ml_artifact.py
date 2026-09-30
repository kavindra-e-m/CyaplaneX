"""CyaplaneX — ML Artifact Integration & Acceptance Verification Tool.

Used to validate a candidate ML model against the frozen 6-feature contract
and the 12-point acceptance gate before deployment into EdgeMLAdapter.

Usage:
    # Verify baseline demonstrator model:
    uv run python scripts/verify_ml_artifact.py

    # Verify custom candidate model from module:
    uv run python scripts/verify_ml_artifact.py --module path.to.model --class CustomModel
"""
from __future__ import annotations

import argparse
import importlib
import sys
from typing import Any

from edge.ai.adapter import BaselineDemonstratorModel, EdgeMLAdapter, validate_model_artifact


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify an ML model artifact against the CyaplaneX frozen contract."
    )
    parser.add_argument(
        "--module",
        type=str,
        default=None,
        help="Python module containing the candidate model class.",
    )
    parser.add_argument(
        "--class",
        dest="class_name",
        type=str,
        default=None,
        help="Class name of the candidate model inside --module.",
    )
    args = parser.parse_args()

    print("=" * 72)
    print("CYAPLANEX -- ML MODEL INTEGRATION ACCEPTANCE GATE")
    print("=" * 72)

    # 1. Resolve model instance
    is_baseline = False
    if args.module and args.class_name:
        print(f"Loading candidate model: {args.module}.{args.class_name}")
        try:
            mod = importlib.import_module(args.module)
            cls = getattr(mod, args.class_name)
            model_instance: Any = cls()
        except (ImportError, AttributeError, TypeError, ValueError, RuntimeError) as err:
            print(f"[REJECTED] Failed to load model artifact: {err}")
            return 1
    else:
        print("Evaluating: BaselineDemonstratorModel (Temporary Development Fixture)")
        model_instance = BaselineDemonstratorModel()
        is_baseline = True

    # 2. Run validation checks
    report = validate_model_artifact(model_instance)

    print("\n--- Acceptance Check Results ---")
    print(f"1. Callable predict() method:      {'PASSED' if report['has_predict_method'] else 'FAILED'}")
    print(f"2. 6-Feature Input Contract:       {'PASSED' if report['input_contract_verified'] else 'FAILED'}")
    print("   Order: [vib_rms, vib_p2p, temp_mean, temp_max, rpm_mean, rpm_std]")
    print(f"3. HealthResult Schema Contract:   {'PASSED' if report['output_schema_verified'] else 'FAILED'}")
    print(f"4. Model Identifier:               {report.get('model_id')}")
    print(f"5. Model Version:                  {report.get('model_version')}")
    print(f"6. Model SHA-256 Hash:             {report.get('model_hash')}")
    print(f"7. Sample Health Score:            {report.get('sample_health_score')}%")
    print(f"8. Sample Diagnosed Condition:     {report.get('sample_condition')}")

    if is_baseline:
        print("\n[NOTE] Model evaluated is the BASELINE DEMONSTRATOR.")
        print("       Monhit Raju's trained production model handoff remains PENDING.")

    if not report["compatible"]:
        print("\n[REJECTED] Model is NOT compatible with CyaplaneX EdgeMLAdapter:")
        for err in report["errors"]:
            print(f"  - {err}")
        return 1

    # 3. Test through EdgeMLAdapter
    adapter = EdgeMLAdapter(model=model_instance)
    res = adapter.infer([0.35, 0.1, 50.0, 52.0, 3000.0, 10.0])
    print(f"\n[PASSED] EdgeMLAdapter integration verified. Condition={res.condition}, Health={res.health_score}%")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())

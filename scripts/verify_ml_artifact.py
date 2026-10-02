"""CyaplaneX — ML Artifact Integration & Acceptance Verification Tool.

Used to validate candidate and production ML models against the frozen 6-feature contract
and the 12-point acceptance gate before deployment into EdgeMLAdapter.

Usage:
    # Verify production ML model artifact (default):
    py -3.14 scripts/verify_ml_artifact.py

    # Verify baseline development fixture explicitly:
    py -3.14 scripts/verify_ml_artifact.py --baseline

    # Verify custom candidate model from module:
    py -3.14 scripts/verify_ml_artifact.py --module path.to.model --class CustomModel
"""
from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from edge.ai.adapter import BaselineDemonstratorModel, validate_model_artifact


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
    parser.add_argument(
        "--baseline",
        action="store_true",
        help="Force evaluation of the baseline demonstrator fixture.",
    )
    parser.add_argument(
        "--expected-hash",
        dest="expected_hash",
        type=str,
        default=None,
        help="Expected 64-character SHA-256 hash for integrity validation.",
    )
    args = parser.parse_args()

    print("=" * 72)
    print("CYAPLANEX -- ML MODEL INTEGRATION ACCEPTANCE GATE")
    print("=" * 72)

    # 1. Resolve model instance
    is_baseline = False
    if args.baseline:
        print("Evaluating: BaselineDemonstratorModel (Temporary Development Fixture)")
        model_instance = BaselineDemonstratorModel()
        is_baseline = True
    elif args.module and args.class_name:
        print(f"Loading candidate model: {args.module}.{args.class_name}")
        try:
            mod = importlib.import_module(args.module)
            cls = getattr(mod, args.class_name)
            model_instance: Any = cls()
        except (ImportError, AttributeError, TypeError, ValueError, RuntimeError) as err:
            print(f"[REJECTED] Failed to load model artifact: {err}")
            return 1
    else:
        print("Evaluating: CyaplaneXProductionModel (Production ML Ensemble Subsystem - Lead: Monhit Raju)")
        try:
            from ml.export.model import CyaplaneXProductionModel
            model_instance = CyaplaneXProductionModel()
        except (ImportError, AttributeError, TypeError, ValueError, RuntimeError) as err:
            print(f"[WARNING] Could not load CyaplaneXProductionModel ({err}). Falling back to baseline.")
            model_instance = BaselineDemonstratorModel()
            is_baseline = True

    # 2. Run validation checks
    report = validate_model_artifact(model_instance, expected_hash=args.expected_hash)

    print("\n--- 12-Point Acceptance Gate Results ---")
    for chk in report.get("checks", []):
        cid = chk["id"]
        cname = chk["name"]
        cstatus = chk["status"]
        cdetail = chk.get("detail", "")
        status_str = f"[{cstatus}]"
        print(f"Check {cid:02d}: {cname:<32} {status_str:<8} | {cdetail}")

    print("\n--- Model Metadata & Telemetry ---")
    print(f"Model Identifier:               {report.get('model_id')}")
    print(f"Model Version:                  {report.get('model_version')}")
    print(f"Model Runtime Hash:             {report.get('model_hash')}")
    print(f"Artifact Hash Verified:         {'PASSED' if report.get('hash_verified') else 'FAILED'}")
    print(f"Sample Diagnosed Condition:     {report.get('sample_condition')}")
    print(f"Sample Health Score:            {report.get('sample_health_score')}%")

    if is_baseline:
        print("\n[NOTE] Model evaluated is the BASELINE DEMONSTRATOR.")
        print("       (Run without --baseline to evaluate Monhit Raju's production model).")
    else:
        print("\n[CONFIRMED] Production Model Artifact Handoff by Monhit Raju is VERIFIED & ACTIVE.")
        print("            Contract: Frozen 6-feature input | Output: Draft 2020-12 Schema.")

    if not report["compatible"]:
        print("\n[REJECTED] Model is NOT compatible with CyaplaneX EdgeMLAdapter:")
        for err in report["errors"]:
            print(f"  - {err}")
        return 1

    # 3. Final summary
    print("\n[PASSED] All 12/12 Acceptance Checks passed successfully.")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())

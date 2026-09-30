"""Edge application entry point executing the CyaplaneX diagnostic cycle."""
from __future__ import annotations

from edge.orchestrator import EdgePipelineOrchestrator


def main() -> None:
    """Run an edge diagnostic cycle using the configured orchestrator."""
    print("==================================================")
    print("CyaplaneX — Edge Runtime Pipeline")
    print("Sense -> Trust -> Preprocess -> Predict -> Sign -> Dispatch")
    print("==================================================")

    orchestrator = EdgePipelineOrchestrator()
    result = orchestrator.execute_cycle(report_id="rep-edge-live-001")

    print(f"Report ID:     {result['event']['report_id']}")
    print(f"Condition:     {result['condition']}")
    print(f"Health Score:  {result['health_score']}%")
    print(f"Sensor Trust:  {result['trust_status']}")
    print(f"Priority:      {result['priority']}")
    print(f"Dispatch:      {result['dispatch']['status']}")
    print(f"Manifest Hash: {result['event']['manifest_hash'][:24]}...")
    print(f"Signature:     {result['event']['digital_signature'][:28]}...")
    print("==================================================")


if __name__ == "__main__":
    main()

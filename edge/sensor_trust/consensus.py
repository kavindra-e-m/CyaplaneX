"""Cross-sensor consensus placeholder."""

def consensus_score(values: list[float]) -> float:
    """Return a neutral score when no fusion policy is configured."""
    # TODO: Implement domain-approved multi-sensor consensus.
    return 0.0 if not values else 1.0

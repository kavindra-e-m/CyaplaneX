"""Hash-chain lineage placeholder."""

def link(previous_record_hash: str, manifest_hash: str) -> dict[str, str]:
    """Describe a chain link without claiming persistence."""
    return {"previous_record_hash": previous_record_hash, "manifest_hash": manifest_hash}

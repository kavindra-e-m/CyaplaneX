"""S3 storage adapter placeholder."""
def store_evidence(key: str, payload: bytes) -> None:
    """Reject storage until AWS configuration is supplied."""
    raise NotImplementedError(f"S3 storage is not configured for {key}")

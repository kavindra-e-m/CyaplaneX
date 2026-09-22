"""Local signing boundary placeholder."""

def sign_locally(payload: bytes, private_key_reference: str) -> bytes:
    """Reject direct key material and defer secure implementation."""
    if not private_key_reference:
        raise ValueError("a local key reference is required")
    # TODO: Use an approved hardware-backed/local signing provider.
    raise NotImplementedError("production local signing is not implemented")

"""Feature Engineering and Contract Verification for CyaplaneX ML Pipeline.

Validates feature vectors against the frozen 6-feature contract:
[vib_rms, vib_p2p, temp_mean, temp_max, rpm_mean, rpm_std]
and provides standard scaling and feature transformations.
"""
from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import pandas as pd

FROZEN_FEATURE_NAMES: tuple[str, ...] = (
    "vib_rms",
    "vib_p2p",
    "temp_mean",
    "temp_max",
    "rpm_mean",
    "rpm_std",
)


class FeatureExtractor:
    """Validates and prepares feature vectors for ML model inference."""

    FEATURE_NAMES: tuple[str, ...] = FROZEN_FEATURE_NAMES

    @classmethod
    def validate_features(cls, features: Sequence[float]) -> np.ndarray:
        """Validate feature vector adheres to the frozen 6-feature contract."""
        if len(features) != len(cls.FEATURE_NAMES):
            raise ValueError(
                f"Frozen ML contract violation: expected exactly {len(cls.FEATURE_NAMES)} features "
                f"{list(cls.FEATURE_NAMES)}, received {len(features)}"
            )
        arr = np.array(features, dtype=np.float64)
        if np.isnan(arr).any() or np.isinf(arr).any():
            raise ValueError("Feature vector contains NaN or Inf values")
        return arr

    @classmethod
    def compute_correlations(cls, df: pd.DataFrame) -> pd.DataFrame:
        """Compute Pearson correlation matrix between the 6 physical features."""
        subset = df[list(cls.FEATURE_NAMES)]
        return subset.corr()

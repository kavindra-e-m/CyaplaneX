"""CWRU Bearing Data Preprocessor and Real-World Feature Extractor.

Loads physical vibration acceleration signals from Case Western Reserve University
benchmark .mat files, segments them into time-series windows, and extracts
empirical physical features (RMS, Peak-to-Peak) coupled with thermal-mechanical dynamics.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import scipy.io


class CWRULoader:
    """Extracts vibration signals from CWRU .mat files and computes window features."""

    def __init__(self, raw_data_dir: Path | str | None = None) -> None:
        self.raw_data_dir = Path(raw_data_dir) if raw_data_dir else Path(__file__).resolve().parent.parent / "data" / "raw"

    def load_mat_signal(self, file_name: str) -> tuple[np.ndarray, float]:
        """Load Drive End vibration signal and nominal RPM from a CWRU .mat file."""
        file_path = self.raw_data_dir / file_name
        if not file_path.exists():
            raise FileNotFoundError(f"CWRU data file not found: {file_path}")

        mat = scipy.io.loadmat(file_path)
        de_keys = [k for k in mat if "DE_time" in k]
        if not de_keys:
            raise KeyError(f"No Drive End (DE_time) signal found in {file_name}")

        signal = mat[de_keys[0]].flatten().astype(np.float64)

        # Extract motor RPM if present
        rpm_keys = [k for k in mat if "RPM" in k]
        rpm = float(mat[rpm_keys[0]].flatten()[0]) if rpm_keys else 1797.0
        return signal, rpm


    def extract_windows(
        self,
        signal: np.ndarray,
        window_size: int = 1024,
        step_size: int = 512,
    ) -> list[tuple[float, float]]:
        """Slice continuous vibration signal into overlapping windows and compute (rms, p2p)."""
        features: list[tuple[float, float]] = []
        n_samples = len(signal)

        for start in range(0, n_samples - window_size + 1, step_size):
            window = signal[start : start + window_size]
            rms = float(np.sqrt(np.mean(window**2)))
            p2p = float(np.ptp(window))
            features.append((rms, p2p))

        return features

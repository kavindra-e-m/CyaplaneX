"""Frequency-Domain Spectral Analysis & Bearing Fault Frequency Analyzer.

Calculates kinematic bearing defect frequencies and extracts spectral harmonics via FFT:
- BPFO: Ball Pass Frequency Outer Race
- BPFI: Ball Pass Frequency Inner Race
- BSF: Ball Spin Frequency
- FTF: Fundamental Train Frequency (Cage)
"""
from __future__ import annotations

from typing import Any

import numpy as np


class BearingKinematics:
    """Kinematic fault frequency equations for rolling element bearings."""

    # Default parameters for SKF 6205-2RS JEM deep groove ball bearing (CWRU testbed)
    DEFAULT_N_BALLS = 9
    DEFAULT_BALL_DIAM_MM = 7.94
    DEFAULT_PITCH_DIAM_MM = 39.04
    DEFAULT_CONTACT_ANGLE_DEG = 0.0

    @classmethod
    def calculate_defect_frequencies(
        cls,
        rpm: float,
        n_balls: int = DEFAULT_N_BALLS,
        ball_diam: float = DEFAULT_BALL_DIAM_MM,
        pitch_diam: float = DEFAULT_PITCH_DIAM_MM,
        contact_angle_deg: float = DEFAULT_CONTACT_ANGLE_DEG,
    ) -> dict[str, float]:
        """Compute theoretical characteristic defect frequencies in Hz."""
        fr = rpm / 60.0  # Shaft rotational frequency (Hz)
        theta = np.radians(contact_angle_deg)
        gamma = (ball_diam / pitch_diam) * np.cos(theta)

        bpfo = (n_balls / 2.0) * fr * (1.0 - gamma)
        bpfi = (n_balls / 2.0) * fr * (1.0 + gamma)
        bsf = (pitch_diam / (2.0 * ball_diam)) * fr * (1.0 - gamma**2)
        ftf = 0.5 * fr * (1.0 - gamma)

        return {
            "shaft_fr_hz": round(float(fr), 2),
            "bpfo_hz": round(float(bpfo), 2),
            "bpfi_hz": round(float(bpfi), 2),
            "bsf_hz": round(float(bsf), 2),
            "ftf_hz": round(float(ftf), 2),
        }


class SpectralFeatureExtractor:
    """Extracts frequency-domain features from raw vibration time series using FFT."""

    def __init__(self, sampling_rate_hz: float = 12000.0) -> None:
        self.fs = sampling_rate_hz

    def analyze_spectrum(
        self,
        signal: np.ndarray,
        rpm: float = 1797.0,
    ) -> dict[str, Any]:
        """Perform FFT and compute spectral power in bearing fault bands."""
        n = len(signal)
        if n < 128:
            raise ValueError(f"Signal length too short for FFT ({n} samples)")

        # Detrend and windowing (Hanning window to minimize spectral leakage)
        detrended = signal - np.mean(signal)
        window = np.hanning(n)
        windowed = detrended * window

        # Compute one-sided FFT
        fft_vals = np.fft.rfft(windowed)
        freqs = np.fft.rfftfreq(n, d=1.0 / self.fs)
        amplitudes = (2.0 / n) * np.abs(fft_vals)

        # Dominant spectral peaks
        peak_indices = np.argsort(amplitudes)[::-1][:5]
        dominant_peaks = [
            {"frequency_hz": round(float(freqs[idx]), 2), "amplitude_g": round(float(amplitudes[idx]), 4)}
            for idx in peak_indices
        ]

        # Theoretical bearing frequencies
        fault_freqs = BearingKinematics.calculate_defect_frequencies(rpm)

        # Spectral energy in outer/inner race defect bands (within +/- 5% tolerance)
        def band_energy(center_hz: float, tolerance: float = 0.05) -> float:
            low, high = center_hz * (1.0 - tolerance), center_hz * (1.0 + tolerance)
            mask = (freqs >= low) & (freqs <= high)
            return float(np.sum(amplitudes[mask] ** 2)) if np.any(mask) else 0.0

        bpfo_energy = band_energy(fault_freqs["bpfo_hz"])
        bpfi_energy = band_energy(fault_freqs["bpfi_hz"])
        total_energy = float(np.sum(amplitudes**2)) + 1e-12

        return {
            "sampling_rate_hz": self.fs,
            "signal_length": n,
            "dominant_peaks": dominant_peaks,
            "bearing_kinematic_frequencies": fault_freqs,
            "spectral_metrics": {
                "bpfo_band_energy": round(bpfo_energy, 6),
                "bpfi_band_energy": round(bpfi_energy, 6),
                "bpfo_energy_ratio": round(bpfo_energy / total_energy, 6),
                "bpfi_energy_ratio": round(bpfi_energy / total_energy, 6),
            },
        }

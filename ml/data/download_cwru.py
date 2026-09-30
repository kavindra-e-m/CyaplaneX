"""CWRU Bearing Data Center — Automated Benchmark Downloader.

Downloads real accelerometer vibration data from Case Western Reserve University:
- 97.mat: Normal baseline (1797 RPM, 0 HP)
- 98.mat: Normal baseline (1772 RPM, 1 HP)
- 105.mat: Inner race fault 7 mil (1797 RPM)
- 106.mat: Inner race fault 7 mil (1772 RPM)
- 118.mat: Ball fault 7 mil (1797 RPM)
- 119.mat: Ball fault 7 mil (1772 RPM)
- 130.mat: Outer race fault 7 mil (1797 RPM)
- 131.mat: Outer race fault 7 mil (1772 RPM)
"""
from __future__ import annotations

import urllib.request
from pathlib import Path

CWRU_URL_TEMPLATE = "https://engineering.case.edu/sites/default/files/{file_id}.mat"

DATASET_FILES: dict[int, str] = {
    97: "normal_0hp",
    98: "normal_1hp",
    105: "inner_race_fault_0hp",
    106: "inner_race_fault_1hp",
    118: "ball_fault_0hp",
    119: "ball_fault_1hp",
    130: "outer_race_fault_0hp",
    131: "outer_race_fault_1hp",
}


def download_cwru_benchmarks(raw_dir: Path | None = None) -> list[Path]:
    """Download CWRU benchmark .mat files into raw directory."""
    target_dir = raw_dir or Path(__file__).parent / "raw"
    target_dir.mkdir(parents=True, exist_ok=True)
    downloaded_paths: list[Path] = []

    print(f"Downloading CWRU Bearing Data Center benchmarks to {target_dir}...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    for file_id, label in DATASET_FILES.items():
        dest = target_dir / f"{file_id}.mat"
        if dest.exists() and dest.stat().st_size > 10000:
            print(f"  [EXISTS] {file_id}.mat ({label}) already present.")
            downloaded_paths.append(dest)
            continue

        url = CWRU_URL_TEMPLATE.format(file_id=file_id)
        print(f"  [FETCHING] {url} -> {dest.name} ({label})...")
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                content = resp.read()
            dest.write_bytes(content)
            print(f"  [SAVED] {dest.name} ({len(content):,} bytes)")
            downloaded_paths.append(dest)
        except (urllib.error.URLError, TimeoutError, OSError) as err:
            print(f"  [ERROR] Failed to fetch {url}: {err}")

    return downloaded_paths


if __name__ == "__main__":
    download_cwru_benchmarks()

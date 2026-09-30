"""Benchmark inference latency for the EdgeMLAdapter and BaselineDemonstratorModel.

Provides reproducible measurement evidence including min, mean, median, p95, p99, and max latency.
"""
from __future__ import annotations

import platform
import time

from edge.ai.adapter import EdgeMLAdapter


def run_benchmark(warmup_cycles: int = 100, measured_cycles: int = 10000) -> dict:
    adapter = EdgeMLAdapter()
    sample_features = [0.35, 0.1, 52.0, 54.0, 3600.0, 15.0]

    # Warm-up phase
    for _ in range(warmup_cycles):
        adapter.infer(sample_features)

    # Measured timing phase using perf_counter_ns
    timings_ns: list[int] = []
    for _ in range(measured_cycles):
        t0 = time.perf_counter_ns()
        adapter.infer(sample_features)
        t1 = time.perf_counter_ns()
        timings_ns.append(t1 - t0)

    timings_ns.sort()
    n = len(timings_ns)

    # Convert to microseconds (us) and milliseconds (ms)
    min_us = timings_ns[0] / 1000.0
    mean_us = (sum(timings_ns) / n) / 1000.0
    med_us = timings_ns[n // 2] / 1000.0
    p95_us = timings_ns[int(n * 0.95)] / 1000.0
    p99_us = timings_ns[int(n * 0.99)] / 1000.0
    max_us = timings_ns[-1] / 1000.0

    report = {
        "hardware": {
            "platform": platform.platform(),
            "processor": platform.processor(),
            "machine": platform.machine(),
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
        },
        "benchmark_config": {
            "model_tested": adapter.model.MODEL_ID,
            "model_version": adapter.model.MODEL_VERSION,
            "warmup_cycles": warmup_cycles,
            "measured_cycles": measured_cycles,
            "timing_clock": "time.perf_counter_ns",
        },
        "results_microseconds": {
            "min_us": round(min_us, 2),
            "mean_us": round(mean_us, 2),
            "median_us": round(med_us, 2),
            "p95_us": round(p95_us, 2),
            "p99_us": round(p99_us, 2),
            "max_us": round(max_us, 2),
        },
        "results_milliseconds": {
            "min_ms": round(min_us / 1000.0, 4),
            "mean_ms": round(mean_us / 1000.0, 4),
            "median_ms": round(med_us / 1000.0, 4),
            "p95_ms": round(p95_us / 1000.0, 4),
            "p99_ms": round(p99_us / 1000.0, 4),
            "max_ms": round(max_us / 1000.0, 4),
        },
    }
    return report


if __name__ == "__main__":
    import json
    data = run_benchmark()
    print(json.dumps(data, indent=2))

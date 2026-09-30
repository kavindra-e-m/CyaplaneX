"""ONNX Model Exporter for CyaplaneX Edge ML System.

Trains an edge-optimized neural network (AeroBearingNet) on the CWRU dataset
and exports it to standard ONNX format (ml/models/cyaplanex_model.onnx).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from torch import nn

from ml.feature_engineering.extractors import FROZEN_FEATURE_NAMES


class AeroBearingNet(nn.Module):
    """Compact edge neural network for rotating machinery fault classification."""

    def __init__(self, input_dim: int = 6, num_classes: int = 5) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.BatchNorm1d(16),
            nn.ReLU(),
            nn.Linear(16, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


def export_onnx_model(output_dir: Path | None = None) -> Path:
    """Train AeroBearingNet and export to cyaplanex_model.onnx."""
    base_dir = Path(__file__).resolve().parent.parent
    data_path = base_dir / "data" / "processed" / "cyaplanex_bearing_dataset.csv"
    models_dir = output_dir or base_dir / "models"
    models_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(data_path)
    feature_cols = list(FROZEN_FEATURE_NAMES)
    X_raw = df[feature_cols].values.astype(np.float32)

    # Standard feature normalization
    mean = X_raw.mean(axis=0)
    std = X_raw.std(axis=0) + 1e-6
    X = (X_raw - mean) / std

    classes = sorted(df["condition"].unique())
    class_to_idx = {c: i for i, c in enumerate(classes)}
    y = np.array([class_to_idx[c] for c in df["condition"]], dtype=np.int64)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    model = AeroBearingNet(input_dim=6, num_classes=len(classes))
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=1e-4)

    X_tr_tensor = torch.tensor(X_train, dtype=torch.float32)
    y_tr_tensor = torch.tensor(y_train, dtype=torch.long)

    # Quick 40-epoch training loop
    model.train()
    for _ in range(40):
        optimizer.zero_grad()
        logits = model(X_tr_tensor)
        loss = criterion(logits, y_tr_tensor)
        loss.backward()
        optimizer.step()

    model.eval()
    with torch.no_grad():
        test_logits = model(torch.tensor(X_test, dtype=torch.float32))
        test_preds = torch.argmax(test_logits, dim=1).numpy()
        acc = float(np.mean(test_preds == y_test))
        print(f"ONNX AeroBearingNet Test Accuracy: {acc * 100:.2f}%")

    # Export to ONNX
    onnx_path = models_dir / "cyaplanex_model.onnx"
    dummy_input = torch.randn(1, 6, dtype=torch.float32)

    # Wrap model with normalization baked in for single vector input
    class NormalizedInferenceNet(nn.Module):
        def __init__(self, core_net: nn.Module, mean_vec: np.ndarray, std_vec: np.ndarray) -> None:
            super().__init__()
            self.core = core_net
            self.register_buffer("mean", torch.tensor(mean_vec, dtype=torch.float32))
            self.register_buffer("std", torch.tensor(std_vec, dtype=torch.float32))

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            norm_x = (x - self.mean) / self.std
            return torch.softmax(self.core(norm_x), dim=-1)

    inference_net = NormalizedInferenceNet(model, mean, std)
    inference_net.eval()

    torch.onnx.export(
        inference_net,
        dummy_input,
        str(onnx_path),
        input_names=["features"],
        output_names=["probabilities"],
        dynamic_axes={"features": {0: "batch_size"}, "probabilities": {0: "batch_size"}},
        opset_version=17,
    )

    onnx_hash = hashlib.sha256(onnx_path.read_bytes()).hexdigest()
    print(f"ONNX Model saved: {onnx_path} ({onnx_path.stat().st_size:,} bytes)")
    print(f"ONNX SHA-256 Hash: {onnx_hash}")

    onnx_meta = {
        "model_id": "cyaplanex-onnx-aeromodel-v1",
        "model_version": "1.0.0",
        "model_hash": onnx_hash,
        "classes": classes,
        "input_features": feature_cols,
        "test_accuracy": round(acc, 4),
    }
    meta_path = models_dir / "onnx_metadata.json"
    meta_path.write_text(json.dumps(onnx_meta, indent=2))
    return onnx_path


if __name__ == "__main__":
    export_onnx_model()

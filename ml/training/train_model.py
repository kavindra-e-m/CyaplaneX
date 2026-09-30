"""Model Training Pipeline for CyaplaneX Edge ML System.

Trains an ensemble classifier (GradientBoostingClassifier / RandomForestClassifier)
on real CWRU-derived vibration & thermal features, evaluates cross-validation metrics,
calibrates anomaly/health scores, and exports trained artifacts.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import StratifiedKFold, train_test_split

from ml.feature_engineering.extractors import FROZEN_FEATURE_NAMES


def train_production_model(
    data_path: Path | str | None = None,
    output_dir: Path | str | None = None,
    random_state: int = 42,
) -> dict[str, Any]:
    """Train and evaluate the production model for CyaplaneX."""
    base_dir = Path(__file__).resolve().parent.parent
    csv_file = Path(data_path) if data_path else base_dir / "data" / "processed" / "cyaplanex_bearing_dataset.csv"
    out_dir = Path(output_dir) if output_dir else base_dir / "models"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading training dataset: {csv_file}...")
    df = pd.read_csv(csv_file)

    feature_cols = list(FROZEN_FEATURE_NAMES)
    X = df[feature_cols].values
    y = df["condition"].values

    # Stratified Train/Test Split (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=random_state, stratify=y
    )
    print(f"Dataset split: Train samples={len(X_train)}, Test samples={len(X_test)}")

    # 1. 5-Fold Stratified Cross-Validation
    print("Executing 5-Fold Stratified Cross-Validation...")
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)
    cv_scores: list[float] = []

    for fold, (train_idx, val_idx) in enumerate(skf.split(X_train, y_train), 1):
        fold_model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=4,
            random_state=random_state,
        )
        fold_model.fit(X_train[train_idx], y_train[train_idx])
        val_preds = fold_model.predict(X_train[val_idx])
        f1 = f1_score(y_train[val_idx], val_preds, average="weighted")
        cv_scores.append(f1)
        print(f"  Fold {fold} Weighted F1-Score: {f1:.4f}")

    mean_cv_f1 = float(np.mean(cv_scores))
    print(f"Mean Cross-Validation F1-Score: {mean_cv_f1:.4f}")

    # 2. Fit Full Production Model
    print("Fitting production GradientBoostingClassifier...")
    model = GradientBoostingClassifier(
        n_estimators=120,
        learning_rate=0.1,
        max_depth=4,
        random_state=random_state,
    )
    model.fit(X_train, y_train)

    # 3. Test Evaluation
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)
    test_acc = accuracy_score(y_test, y_pred)
    test_f1 = f1_score(y_test, y_pred, average="weighted")
    report = classification_report(y_test, y_pred, output_dict=True)

    print(f"Production Model Test Accuracy: {test_acc * 100:.2f}%")
    print(f"Production Model Test Weighted F1: {test_f1:.4f}")

    # 4. Save Model Artifact (.joblib)
    artifact_path = out_dir / "cyaplanex_production_model.joblib"
    joblib.dump(model, artifact_path, compress=3)
    print(f"Model artifact saved: {artifact_path}")

    # Calculate cryptographic SHA-256 hash of artifact
    artifact_bytes = artifact_path.read_bytes()
    import hashlib
    artifact_hash = hashlib.sha256(artifact_bytes).hexdigest()

    metadata = {
        "model_id": "cyaplanex-gb-aeromodel-v1",
        "model_version": "1.0.0",
        "model_hash": artifact_hash,
        "algorithm": "GradientBoostingClassifier",
        "n_estimators": 120,
        "max_depth": 4,
        "classes": list(model.classes_),
        "feature_order": feature_cols,
        "cv_mean_f1": round(mean_cv_f1, 4),
        "test_accuracy": round(float(test_acc), 4),
        "test_f1_weighted": round(float(test_f1), 4),
        "feature_importances": {
            feat: round(float(imp), 4)
            for feat, imp in zip(feature_cols, model.feature_importances_)
        },
    }

    metadata_path = out_dir / "model_metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2))
    print(f"Model metadata written: {metadata_path}")
    print(f"Model SHA-256 Hash: {artifact_hash}")

    return {
        "model": model,
        "metadata": metadata,
        "test_data": (X_test, y_test, y_pred, y_prob),
        "report": report,
    }


if __name__ == "__main__":
    train_production_model()

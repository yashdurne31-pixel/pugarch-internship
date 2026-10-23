"""
Model Training and Evaluation Pipeline for Smart Hygiene Risk Prediction System.
Trains multiple classification and regression algorithms, performs Stratified K-Fold CV,
evaluates comprehensive metrics (Accuracy, Precision, Recall, F1, ROC-AUC), and exports production artifacts.
"""

import os
import json
import time
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple
import joblib

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier, GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
    r2_score,
    mean_absolute_error,
    root_mean_squared_error,
)

from preprocessing import (
    HygieneDataPreprocessor,
    TARGET_COL_CLASS,
    TARGET_COL_REG,
    RISK_CLASS_MAPPING,
    INV_RISK_CLASS_MAPPING,
)


def train_and_evaluate_models(data_path: str, models_dir: str) -> Dict[str, Any]:
    print("=" * 70)
    print("HYGIENE RISK PREDICTION - MODEL TRAINING & BENCHMARKING PIPELINE")
    print("=" * 70)

    # 1. Load Data
    df = pd.read_csv(data_path)
    print(f"Loaded inspection records: {df.shape[0]} rows, {df.shape[1]} columns")

    # 2. Stratified Train / Test Split
    df_train, df_test = train_test_split(
        df, test_size=0.20, random_state=42, stratify=df[TARGET_COL_CLASS]
    )
    print(f"Dataset split: Train = {len(df_train)} (80%), Test = {len(df_test)} (20%)")

    # 3. Fit Preprocessor on Train set only (strict leakage prevention)
    preprocessor = HygieneDataPreprocessor()
    X_train = preprocessor.fit_transform(df_train)
    X_test = preprocessor.transform(df_test)

    # Classification targets
    y_train_cls = preprocessor.encode_labels(df_train[TARGET_COL_CLASS])
    y_test_cls = preprocessor.encode_labels(df_test[TARGET_COL_CLASS])

    # Continuous regression targets (Risk Score 0 - 100)
    y_train_reg = df_train[TARGET_COL_REG].values
    y_test_reg = df_test[TARGET_COL_REG].values

    # 4. Define Candidate Classification Models
    candidate_models = {
        "Random Forest": RandomForestClassifier(
            n_estimators=200,
            max_depth=12,
            min_samples_split=4,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1,
        ),
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=180,
            learning_rate=0.08,
            max_depth=5,
            subsample=0.85,
            random_state=42,
        ),
        "Extra Trees": ExtraTreesClassifier(
            n_estimators=180,
            max_depth=14,
            min_samples_split=4,
            random_state=42,
            n_jobs=-1,
        ),
        "Logistic Regression": LogisticRegression(
            C=1.2,
            max_iter=1500,
            solver="lbfgs",
            random_state=42,
        ),
    }

    results = {}
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    best_score = -1.0
    best_model_name = None
    best_classifier = None

    print("\n--- Model Benchmark & 5-Fold Stratified Cross-Validation ---")
    for name, model in candidate_models.items():
        t0 = time.time()
        # 5-fold cross validation on training data
        cv_scores = cross_val_score(model, X_train, y_train_cls, cv=cv, scoring="f1_weighted", n_jobs=-1)
        train_time = time.time() - t0

        # Fit model on entire train set
        model.fit(X_train, y_train_cls)

        # Test set predictions
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test) if hasattr(model, "predict_proba") else None

        # Metrics calculation
        acc = accuracy_score(y_test_cls, y_pred)
        f1_w = f1_score(y_test_cls, y_pred, average="weighted")
        f1_m = f1_score(y_test_cls, y_pred, average="macro")
        prec_w = precision_score(y_test_cls, y_pred, average="weighted", zero_division=0)
        rec_w = recall_score(y_test_cls, y_pred, average="weighted", zero_division=0)

        # ROC-AUC (One-vs-Rest)
        try:
            auc = roc_auc_score(y_test_cls, y_prob, multi_class="ovr", average="weighted")
        except Exception:
            auc = 0.0

        cm = confusion_matrix(y_test_cls, y_pred).tolist()
        report = classification_report(
            y_test_cls,
            y_pred,
            target_names=["Low Risk", "Medium Risk", "High Risk"],
            output_dict=True,
        )

        results[name] = {
            "cv_f1_mean": float(round(cv_scores.mean(), 4)),
            "cv_f1_std": float(round(cv_scores.std(), 4)),
            "accuracy": float(round(acc, 4)),
            "f1_weighted": float(round(f1_w, 4)),
            "f1_macro": float(round(f1_m, 4)),
            "precision_weighted": float(round(prec_w, 4)),
            "recall_weighted": float(round(rec_w, 4)),
            "roc_auc_weighted": float(round(auc, 4)),
            "training_time_sec": float(round(train_time, 2)),
            "confusion_matrix": cm,
            "classification_report": report,
        }

        print(
            f"{name:<22} | CV F1: {cv_scores.mean():.4f} ± {cv_scores.std():.4f} | "
            f"Test Acc: {acc*100:.2f}% | Test F1: {f1_w:.4f} | AUC: {auc:.4f}"
        )

        # We prioritize weighted F1 score for best model selection
        if f1_w > best_score:
            best_score = f1_w
            best_model_name = name
            best_classifier = model

    print(f"\n>> Selected Best Model: {best_model_name} (F1: {best_score:.4f})")

    # 5. Train Continuous Risk Score Regressor
    print("\n--- Training Continuous Risk Score Regressor (0-100) ---")
    regressor = GradientBoostingRegressor(
        n_estimators=150,
        learning_rate=0.08,
        max_depth=5,
        random_state=42,
    )
    regressor.fit(X_train, y_train_reg)
    y_reg_pred = regressor.predict(X_test)
    r2 = r2_score(y_test_reg, y_reg_pred)
    mae = mean_absolute_error(y_test_reg, y_reg_pred)
    rmse = root_mean_squared_error(y_test_reg, y_reg_pred)

    reg_metrics = {
        "r2_score": float(round(r2, 4)),
        "mae": float(round(mae, 2)),
        "rmse": float(round(rmse, 2)),
    }
    print(f"Regressor performance -> R2: {r2:.4f} | MAE: {mae:.2f} | RMSE: {rmse:.2f}")

    # 6. Save Model Artifacts
    os.makedirs(models_dir, exist_ok=True)
    best_model_path = os.path.join(models_dir, "best_classifier.joblib")
    regressor_path = os.path.join(models_dir, "best_regressor.joblib")
    preprocessor_path = os.path.join(models_dir, "preprocessor.joblib")
    metrics_path = os.path.join(models_dir, "model_metrics.json")
    metadata_path = os.path.join(models_dir, "metadata.json")

    joblib.dump(best_classifier, best_model_path)
    joblib.dump(regressor, regressor_path)
    preprocessor.save(preprocessor_path)

    summary_metrics = {
        "best_model_name": best_model_name,
        "models_benchmark": results,
        "regression_metrics": reg_metrics,
        "classes": ["Low Risk", "Medium Risk", "High Risk"],
        "class_mapping": RISK_CLASS_MAPPING,
        "training_samples": len(df_train),
        "test_samples": len(df_test),
        "trained_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(summary_metrics, f, indent=2)

    metadata = {
        "project": "Smart Hygiene Risk Prediction System",
        "version": "1.0.0",
        "features": {
            "numerical": preprocessor.numerical_features,
            "categorical": preprocessor.categorical_features,
            "all_encoded": preprocessor.feature_names_out,
        },
        "target_class": TARGET_COL_CLASS,
        "target_score": TARGET_COL_REG,
        "best_model": best_model_name,
        "test_accuracy": results[best_model_name]["accuracy"],
        "test_f1": results[best_model_name]["f1_weighted"],
        "test_auc": results[best_model_name]["roc_auc_weighted"],
    }
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"\nArtifacts successfully persisted to: {models_dir}")
    print(f"  - Classifier: {best_model_path}")
    print(f"  - Regressor:  {regressor_path}")
    print(f"  - Preprocessor: {preprocessor_path}")
    print(f"  - Metrics:    {metrics_path}")
    print(f"  - Metadata:   {metadata_path}")

    return summary_metrics


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(current_dir, "..", "data", "hygiene_inspections.csv")
    models_dir = os.path.join(current_dir, "..", "models")
    train_and_evaluate_models(data_file, models_dir)

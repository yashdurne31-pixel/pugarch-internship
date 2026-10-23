"""
train_model.py
==============
Model training and evaluation for the Smart Hygiene Risk Prediction System.

This script:
1. Loads and preprocesses the dataset.
2. Trains two classifiers:
   - Logistic Regression (with StandardScaler already in the preprocessor)
   - Random Forest Classifier
3. Evaluates both on the held-out test set.
4. Saves the confusion matrix for the better model to outputs/.
5. Saves the complete pipeline (preprocessor + best model) to models/.
6. Prints a concise training summary.

IMPORTANT EVALUATION DISCLAIMER
---------------------------------
- The dataset is synthetic and the target is rule-generated.
- High accuracy reflects how closely the model approximates the rule,
  NOT how well it predicts real-world hygiene outcomes.
- Evaluation on synthetic / rule-generated labels does NOT establish
  real-world predictive performance.

Usage
-----
    python src/train_model.py
"""

import os
import sys

# Ensure UTF-8 output on Windows (avoids cp1252 UnicodeEncodeError)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import warnings
import numpy as np
import pandas as pd
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, ConfusionMatrixDisplay,
)

warnings.filterwarnings("ignore")

# ── paths ────────────────────────────────────────────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, ".."))

from src.data_preprocessing import load_and_preprocess, build_preprocessor

OUTPUT_DIR = os.path.join(_HERE, "..", "outputs")
MODEL_DIR = os.path.join(_HERE, "..", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "hygiene_risk_model.joblib")

RANDOM_STATE = 42
CLASSES = ["Low", "Medium", "High"]


# ── helper ────────────────────────────────────────────────────────────────────

def evaluate_model(model, X_test, y_test, model_name: str) -> dict:
    """
    Evaluate a trained model and return a metrics dictionary.

    Parameters
    ----------
    model : fitted estimator
    X_test : np.ndarray
    y_test : pd.Series
    model_name : str

    Returns
    -------
    dict with accuracy, precision, recall, f1
    """
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average="macro", zero_division=0)
    rec = recall_score(y_test, y_pred, average="macro", zero_division=0)
    f1 = f1_score(y_test, y_pred, average="macro", zero_division=0)

    print(f"\n{'-'*50}")
    print(f"  {model_name}")
    print(f"{'-'*50}")
    print(f"  Accuracy  : {acc:.4f}")
    print(f"  Precision : {prec:.4f}  (macro-avg)")
    print(f"  Recall    : {rec:.4f}  (macro-avg)")
    print(f"  F1-Score  : {f1:.4f}  (macro-avg)")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=CLASSES, zero_division=0))

    return {"model": model_name, "accuracy": acc, "precision": prec,
            "recall": rec, "f1": f1, "y_pred": y_pred}


def save_confusion_matrix(y_test, y_pred, model_name: str):
    """Save the confusion matrix heatmap."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    cm = confusion_matrix(y_test, y_pred, labels=CLASSES)

    fig, ax = plt.subplots(figsize=(6, 5))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=CLASSES)
    disp.plot(ax=ax, cmap="Blues", colorbar=False)
    ax.set_title(f"Confusion Matrix — {model_name}\n(Synthetic Data / Rule-Generated Labels)", fontsize=11)
    path = os.path.join(OUTPUT_DIR, "confusion_matrix.png")
    fig.savefig(path, bbox_inches="tight", dpi=120)
    plt.close(fig)
    print(f"[OK] Saved: {path}")


def print_comparison_table(results: list):
    """Pretty-print a comparison table of model metrics."""
    df = pd.DataFrame(results)[["model", "accuracy", "precision", "recall", "f1"]]
    df = df.rename(columns={
        "model": "Model",
        "accuracy": "Accuracy",
        "precision": "Precision",
        "recall": "Recall",
        "f1": "F1 (macro)",
    })
    df = df.round(4)
    print("\n" + "=" * 60)
    print("  MODEL COMPARISON TABLE")
    print("=" * 60)
    print(df.to_string(index=False))


def main():
    print("=" * 60)
    print("  SMART HYGIENE RISK PREDICTION — MODEL TRAINING")
    print("=" * 60)

    # ── load data ─────────────────────────────────────────────────────────
    X_train, X_test, y_train, y_test, preprocessor, feature_names = load_and_preprocess()

    results = []

    # ─────────────────────────────────────────────────────────────────────
    # MODEL 1 : Logistic Regression
    # Note: preprocessor already applies StandardScaler to numeric features.
    # ─────────────────────────────────────────────────────────────────────
    print("\n[1/2] Training Logistic Regression …")
    lr_model = LogisticRegression(
        max_iter=1000,
        random_state=RANDOM_STATE,
        class_weight="balanced",
        solver="lbfgs",
    )
    lr_model.fit(X_train, y_train)
    lr_results = evaluate_model(lr_model, X_test, y_test, "Logistic Regression")
    results.append(lr_results)

    # ─────────────────────────────────────────────────────────────────────
    # MODEL 2 : Random Forest Classifier
    # ─────────────────────────────────────────────────────────────────────
    print("\n[2/2] Training Random Forest Classifier …")
    rf_model = RandomForestClassifier(
        n_estimators=200,
        max_depth=12,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )
    rf_model.fit(X_train, y_train)
    rf_results = evaluate_model(rf_model, X_test, y_test, "Random Forest")
    results.append(rf_results)

    # ── comparison ────────────────────────────────────────────────────────
    print_comparison_table(results)

    # ── select best model by macro F1 ────────────────────────────────────
    best = max(results, key=lambda r: r["f1"])
    best_model = lr_model if best["model"] == "Logistic Regression" else rf_model

    print(f"\n[SELECT] Best model: {best['model']}  (F1 macro = {best['f1']:.4f})")

    # ── save confusion matrix for best model ──────────────────────────────
    save_confusion_matrix(y_test, best["y_pred"], best["model"])

    # ── bundle preprocessor + best model and save ─────────────────────────
    os.makedirs(MODEL_DIR, exist_ok=True)
    bundle = {
        "preprocessor": preprocessor,
        "model": best_model,
        "model_name": best["model"],
        "feature_names": feature_names,
        "classes": list(best_model.classes_),
        "metadata": {
            "dataset": "synthetic — hygiene_inspections.csv",
            "target": "hygiene_risk (rule-generated)",
            "random_state": RANDOM_STATE,
            "test_f1_macro": round(best["f1"], 4),
        },
    }
    joblib.dump(bundle, MODEL_PATH)
    print(f"[OK] Model bundle saved: {MODEL_PATH}")

    # ── training summary ──────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  TRAINING SUMMARY")
    print("=" * 60)
    print(f"  Dataset          : synthetic (1 000 records)")
    print(f"  Training rows    : {len(y_train)}")
    print(f"  Test rows        : {len(y_test)}")
    print(f"  Features used    : {len(feature_names)}")
    print(f"  Selected model   : {best['model']}")
    print(f"  Test Accuracy    : {best['accuracy']:.4f}")
    print(f"  Test F1 (macro)  : {best['f1']:.4f}")
    print(f"  Model saved to   : {MODEL_PATH}")
    print("\n[DISCLAIMER] All metrics are computed on synthetic, rule-generated")
    print("             labels and do NOT reflect real-world performance.")

    # ── feature importance chart (RF only) ────────────────────────────────
    if isinstance(best_model, RandomForestClassifier):
        _save_feature_importance(best_model, feature_names)


def _save_feature_importance(rf_model, feature_names):
    """Save feature importance chart for Random Forest model."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    importances = rf_model.feature_importances_
    indices = np.argsort(importances)[::-1]
    top_n = min(12, len(feature_names))
    top_idx = indices[:top_n]

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = plt.cm.RdYlGn(np.linspace(0.2, 0.9, top_n))[::-1]
    ax.barh(
        [feature_names[i] for i in top_idx[::-1]],
        importances[top_idx[::-1]],
        color=colors,
        edgecolor="white",
    )
    ax.set_title(f"Feature Importance (Top {top_n}) — Random Forest", fontsize=12, pad=10)
    ax.set_xlabel("Mean Decrease in Impurity")
    sns.set_theme(style="whitegrid")
    sns.despine()
    path = os.path.join(OUTPUT_DIR, "feature_importance.png")
    fig.savefig(path, bbox_inches="tight", dpi=120)
    plt.close(fig)
    print(f"[OK] Saved: {path}")


if __name__ == "__main__":
    main()

"""
feature_selection.py
====================
Feature importance analysis for the Smart Hygiene Risk Prediction System.

This module trains a lightweight Random Forest classifier on the training set
and ranks features by their mean decrease in impurity (Gini importance).

IMPORTANT: Feature selection is performed using ONLY training data.
           Test data are never used to guide feature selection.

OUTPUT
------
- Prints a ranked feature importance table.
- Saves outputs/feature_importance.png (horizontal bar chart).
- Returns a list of selected feature names for use in train_model.py.

NOTE ON LEAKAGE
---------------
Because the target `hygiene_risk` in this dataset is generated from a linear
combination of the input features, feature importance scores will reflect the
coefficients of that rule rather than genuine predictive relationships.

Usage
-----
    python src/feature_selection.py
"""

import os
import sys

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier

warnings.filterwarnings("ignore")

# ── paths ────────────────────────────────────────────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, ".."))

from src.data_preprocessing import load_and_preprocess, NUMERIC_FEATURES, CATEGORICAL_FEATURES

OUTPUT_DIR = os.path.join(_HERE, "..", "outputs")

IMPORTANCE_THRESHOLD = 0.01   # keep features with importance ≥ 1 %


def get_feature_names_from_preprocessor(preprocessor) -> list:
    """
    Derive the output feature name list from a fitted ColumnTransformer.

    Parameters
    ----------
    preprocessor : fitted ColumnTransformer

    Returns
    -------
    list[str]
    """
    ohe = preprocessor.named_transformers_["cat"]["encoder"]
    cat_names = list(ohe.get_feature_names_out(CATEGORICAL_FEATURES))
    return NUMERIC_FEATURES + cat_names


def select_features(
    X_train: np.ndarray,
    y_train: pd.Series,
    feature_names: list,
    random_state: int = 42,
    threshold: float = IMPORTANCE_THRESHOLD,
) -> tuple:
    """
    Rank features by Random Forest Gini importance and return selected names.

    Parameters
    ----------
    X_train : np.ndarray
        Preprocessed training features.
    y_train : pd.Series
        Training labels.
    feature_names : list[str]
        Names corresponding to columns in X_train.
    random_state : int
        Seed for reproducibility.
    threshold : float
        Minimum importance score to retain a feature.

    Returns
    -------
    tuple
        (importance_df, selected_feature_names)
        - importance_df : pd.DataFrame with 'feature' and 'importance' columns
        - selected_feature_names : list[str] of features above threshold
    """
    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=random_state,
        n_jobs=-1,
    )
    rf.fit(X_train, y_train)

    importances = rf.feature_importances_
    importance_df = pd.DataFrame({
        "feature": feature_names,
        "importance": importances,
    }).sort_values("importance", ascending=False).reset_index(drop=True)

    selected = importance_df[importance_df["importance"] >= threshold]["feature"].tolist()

    return importance_df, selected


def plot_feature_importance(importance_df: pd.DataFrame, output_dir: str = OUTPUT_DIR):
    """
    Save a horizontal bar chart of feature importances.

    Parameters
    ----------
    importance_df : pd.DataFrame
        DataFrame with 'feature' and 'importance' columns, sorted descending.
    output_dir : str
        Directory where the PNG will be saved.
    """
    os.makedirs(output_dir, exist_ok=True)

    top_n = min(15, len(importance_df))
    plot_df = importance_df.head(top_n).sort_values("importance")

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = plt.cm.RdYlGn(np.linspace(0.2, 0.9, len(plot_df)))[::-1]
    bars = ax.barh(plot_df["feature"], plot_df["importance"], color=colors, edgecolor="white")

    for bar, val in zip(bars, plot_df["importance"]):
        ax.text(bar.get_width() + 0.002, bar.get_y() + bar.get_height() / 2,
                f"{val:.3f}", va="center", fontsize=9)

    ax.set_title(f"Feature Importance (Top {top_n})\nRandom Forest — Gini Impurity", fontsize=13, pad=12)
    ax.set_xlabel("Mean Decrease in Impurity")
    ax.set_ylabel("Feature")
    ax.set_xlim(0, plot_df["importance"].max() * 1.18)
    sns.set_theme(style="whitegrid")
    sns.despine()
    path = os.path.join(output_dir, "feature_importance.png")
    fig.savefig(path, bbox_inches="tight", dpi=120)
    plt.close(fig)
    print(f"[OK] Saved: {path}")


def main():
    print("=" * 60)
    print("  FEATURE SELECTION")
    print("=" * 60)

    X_train, X_test, y_train, y_test, preprocessor, feature_names = load_and_preprocess()

    print(f"\n[INFO] Running Random Forest feature importance on training set …")
    importance_df, selected = select_features(X_train, y_train, feature_names)

    print("\nRanked feature importances:")
    print(importance_df.to_string(index=False))

    print(f"\nSelected features (importance ≥ {IMPORTANCE_THRESHOLD}):")
    for f in selected:
        print(f"  - {f}")

    plot_feature_importance(importance_df)

    print("\n[NOTE] These importance scores reflect how well each feature")
    print("       predicts the rule-generated label, not real hygiene risk.")


if __name__ == "__main__":
    main()

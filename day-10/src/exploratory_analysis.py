"""
exploratory_analysis.py
=======================
Exploratory Data Analysis (EDA) for the Smart Hygiene Risk Prediction System.

This module generates structured visualizations and summary statistics for the
synthetic hygiene inspection dataset.

Outputs saved to outputs/
--------------------------
- risk_distribution.png       : Count of each hygiene risk category
- cleanliness_distribution.png: Histogram of cleanliness scores by risk class
- odor_score_distribution.png : Box plot of odor scores per risk class
- waste_level_chart.png       : Stacked bar — waste level vs. hygiene risk
- correlation_heatmap.png     : Pearson correlation matrix of numeric features

Usage
-----
    python src/exploratory_analysis.py
"""

import os
import sys

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import warnings
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")          # non-interactive backend (safe for scripts)
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore")

# ── paths ────────────────────────────────────────────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(_HERE, "..", "data", "hygiene_inspections.csv")
OUTPUT_DIR = os.path.join(_HERE, "..", "outputs")

# ── plotting style ───────────────────────────────────────────────────────────
PALETTE = {"Low": "#2ecc71", "Medium": "#f39c12", "High": "#e74c3c"}
sns.set_theme(style="whitegrid", font_scale=1.1)
plt.rcParams.update({
    "figure.dpi": 120,
    "savefig.bbox": "tight",
    "font.family": "DejaVu Sans",
})


def ensure_output_dir():
    """Create the outputs directory if it does not exist."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_data(path: str = DATA_PATH) -> pd.DataFrame:
    """Load and return the raw CSV dataset."""
    if not os.path.exists(path):
        print(f"[ERROR] Dataset not found: {path}")
        print("        Run  python data/generate_data.py  first.")
        sys.exit(1)
    return pd.read_csv(path)


# ── EDA functions ─────────────────────────────────────────────────────────────

def print_summary(df: pd.DataFrame):
    """Print dataset dimensions, dtypes, missing values, and duplicates."""
    print("\n" + "=" * 60)
    print("  EXPLORATORY DATA ANALYSIS — SUMMARY")
    print("=" * 60)
    print(f"\n  Rows      : {df.shape[0]}")
    print(f"  Columns   : {df.shape[1]}")

    print("\n--- Column dtypes ---")
    print(df.dtypes.to_string())

    print("\n--- Descriptive statistics (numeric) ---")
    print(df.describe(include=[np.number]).T.to_string())

    print("\n--- Missing values ---")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    miss_df = pd.DataFrame({"Missing": missing, "Pct %": missing_pct})
    miss_df = miss_df[miss_df["Missing"] > 0]
    print(miss_df.to_string() if not miss_df.empty else "  None detected")

    print(f"\n--- Duplicate rows ---")
    dupes = df.duplicated().sum()
    print(f"  {dupes} duplicate row(s) found")

    print("\n--- Target distribution (hygiene_risk) ---")
    vc = df["hygiene_risk"].value_counts()
    pct = (vc / len(df) * 100).round(1)
    for cat in ["Low", "Medium", "High"]:
        if cat in vc:
            print(f"  {cat:<8}: {vc[cat]:>5}  ({pct[cat]:.1f}%)")


def plot_risk_distribution(df: pd.DataFrame):
    """Bar chart of hygiene risk category counts."""
    fig, ax = plt.subplots(figsize=(7, 4))
    order = ["Low", "Medium", "High"]
    counts = df["hygiene_risk"].value_counts().reindex(order)
    bars = ax.bar(order, counts, color=[PALETTE[c] for c in order], width=0.5, edgecolor="white")

    for bar, val in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
                str(val), ha="center", va="bottom", fontweight="bold")

    ax.set_title("Hygiene Risk Category Distribution\n(Rule-Generated Labels)", fontsize=13, pad=12)
    ax.set_xlabel("Hygiene Risk Category")
    ax.set_ylabel("Number of Facilities")
    ax.set_ylim(0, counts.max() * 1.15)
    sns.despine()
    path = os.path.join(OUTPUT_DIR, "risk_distribution.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"[OK] Saved: {path}")


def plot_cleanliness_distribution(df: pd.DataFrame):
    """Overlapping histogram of cleanliness scores by risk category."""
    fig, ax = plt.subplots(figsize=(8, 4))
    for cat in ["Low", "Medium", "High"]:
        subset = df[df["hygiene_risk"] == cat]["cleanliness_score"].dropna()
        ax.hist(subset, bins=20, alpha=0.55, color=PALETTE[cat], label=cat, edgecolor="white")

    ax.set_title("Cleanliness Score Distribution by Hygiene Risk", fontsize=13, pad=12)
    ax.set_xlabel("Cleanliness Score (0 – 100)")
    ax.set_ylabel("Frequency")
    ax.legend(title="Hygiene Risk")
    sns.despine()
    path = os.path.join(OUTPUT_DIR, "cleanliness_distribution.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"[OK] Saved: {path}")


def plot_odor_score_distribution(df: pd.DataFrame):
    """Box plot of odor scores for each hygiene risk class."""
    fig, ax = plt.subplots(figsize=(7, 4))
    order = ["Low", "Medium", "High"]
    data = [df[df["hygiene_risk"] == c]["odor_score"].dropna() for c in order]
    bp = ax.boxplot(data, tick_labels=order, patch_artist=True, notch=False,
                    medianprops=dict(color="black", linewidth=2))
    for patch, cat in zip(bp["boxes"], order):
        patch.set_facecolor(PALETTE[cat])
        patch.set_alpha(0.75)

    ax.set_title("Odor Score Distribution by Hygiene Risk", fontsize=13, pad=12)
    ax.set_xlabel("Hygiene Risk Category")
    ax.set_ylabel("Odor Score (0 – 10)")
    sns.despine()
    path = os.path.join(OUTPUT_DIR, "odor_score_distribution.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"[OK] Saved: {path}")


def plot_waste_level_chart(df: pd.DataFrame):
    """Stacked/grouped bar chart: waste level vs. hygiene risk."""
    cross = pd.crosstab(df["waste_level"], df["hygiene_risk"])
    cross = cross.reindex(["Low", "Medium", "High"], axis=1)
    cross = cross.reindex(["Low", "Medium", "High"], axis=0)

    fig, ax = plt.subplots(figsize=(7, 4))
    cross.plot(kind="bar", ax=ax, color=[PALETTE[c] for c in cross.columns],
               edgecolor="white", width=0.6)
    ax.set_title("Waste Level vs. Hygiene Risk Category", fontsize=13, pad=12)
    ax.set_xlabel("Waste Level")
    ax.set_ylabel("Count")
    ax.legend(title="Hygiene Risk", bbox_to_anchor=(1.01, 1), loc="upper left")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    sns.despine()
    path = os.path.join(OUTPUT_DIR, "waste_level_chart.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"[OK] Saved: {path}")


def plot_correlation_heatmap(df: pd.DataFrame):
    """Pearson correlation heatmap for numeric features."""
    numeric_cols = [
        "cleanliness_score", "odor_score", "footfall", "complaints"
    ]
    corr = df[numeric_cols].corr()

    fig, ax = plt.subplots(figsize=(7, 5))
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    sns.heatmap(
        corr, ax=ax, annot=True, fmt=".2f",
        cmap="RdYlGn_r", center=0,
        linewidths=0.5, linecolor="white",
        cbar_kws={"shrink": 0.8},
    )
    ax.set_title("Correlation Heatmap — Numeric Features", fontsize=13, pad=12)
    path = os.path.join(OUTPUT_DIR, "correlation_heatmap.png")
    fig.savefig(path)
    plt.close(fig)
    print(f"[OK] Saved: {path}")


def main():
    ensure_output_dir()
    df = load_data()
    print_summary(df)

    print("\n--- Generating visualizations ---")
    plot_risk_distribution(df)
    plot_cleanliness_distribution(df)
    plot_odor_score_distribution(df)
    plot_waste_level_chart(df)
    plot_correlation_heatmap(df)

    print("\n[OK] EDA complete. All plots saved in outputs/")
    print("\nKey findings (note: correlations do not imply causation):")
    print("  • Higher odor scores and waste levels trend with higher risk classes.")
    print("  • Cleanliness scores show an inverse relationship with risk category.")
    print("  • Water availability 'No' is associated with elevated risk.")
    print("  • Complaint count correlates with risk class assignment.")
    print("  These patterns reflect the rule used to generate labels, not")
    print("  independently verified real-world inspection outcomes.")


if __name__ == "__main__":
    main()

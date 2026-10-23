"""
Feature Selection and Importance Analysis for Smart Hygiene Risk Prediction System.
Evaluates Random Forest Importance, Mutual Information, and ANOVA F-scores to rank top risk drivers.
"""

import os
import json
import numpy as np
import pandas as pd
from typing import Dict, Any, List
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import mutual_info_classif, f_classif
from preprocessing import HygieneDataPreprocessor, TARGET_COL_CLASS


def run_feature_selection(data_path: str, models_dir: str) -> Dict[str, Any]:
    """
    Perform multi-metric feature selection and ranking.
    """
    df = pd.read_csv(data_path)
    preprocessor = HygieneDataPreprocessor()
    X = preprocessor.fit_transform(df)
    y = preprocessor.encode_labels(df[TARGET_COL_CLASS])
    feature_names = preprocessor.feature_names_out

    print(f"Computing Random Forest Feature Importances across {len(feature_names)} features...")
    rf = RandomForestClassifier(n_estimators=150, max_depth=12, random_state=42, n_jobs=-1)
    rf.fit(X, y)
    rf_importances = rf.feature_importances_

    print("Computing Mutual Information Scores...")
    mi_scores = mutual_info_classif(X, y, random_state=42)

    print("Computing ANOVA F-Classif Statistics...")
    f_scores, p_values = f_classif(X, y)
    # Replace nan or inf in f_scores if any
    f_scores = np.nan_to_num(f_scores, nan=0.0, posinf=0.0)

    # Normalize metrics to 0-1 scale for balanced ranking
    def min_max(arr):
        denom = (arr.max() - arr.min())
        return (arr - arr.min()) / denom if denom > 0 else np.zeros_like(arr)

    norm_rf = min_max(rf_importances)
    norm_mi = min_max(mi_scores)
    norm_f = min_max(f_scores)

    composite_score = (0.45 * norm_rf + 0.35 * norm_mi + 0.20 * norm_f).round(4)

    feature_records = []
    for i, name in enumerate(feature_names):
        feature_records.append({
            "feature": name,
            "rf_importance": float(round(rf_importances[i], 4)),
            "mutual_info": float(round(mi_scores[i], 4)),
            "f_score": float(round(f_scores[i], 2)),
            "composite_score": float(composite_score[i]),
        })

    # Sort descending by composite score
    feature_records.sort(key=lambda x: x["composite_score"], reverse=True)

    # Add cumulative importance
    total_rf = sum(x["rf_importance"] for x in feature_records)
    cum_sum = 0.0
    for r in feature_records:
        cum_sum += r["rf_importance"]
        r["cumulative_rf_ratio"] = float(round(cum_sum / total_rf, 4))

    top_10 = [r["feature"] for r in feature_records[:10]]
    result = {
        "ranked_features": feature_records,
        "top_10_features": top_10,
        "n_features_total": len(feature_names),
    }

    os.makedirs(models_dir, exist_ok=True)
    out_file = os.path.join(models_dir, "feature_importance.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f"\nFeature Selection complete. Saved results to: {out_file}")
    print("\nTop 10 Hygiene Risk Drivers:")
    for rank, item in enumerate(feature_records[:10], 1):
        print(f"  {rank:2d}. {item['feature']:<35} | Composite: {item['composite_score']:.3f} | RF: {item['rf_importance']:.3f} | MI: {item['mutual_info']:.3f}")

    return result


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(current_dir, "..", "data", "hygiene_inspections.csv")
    models_path = os.path.join(current_dir, "..", "models")
    run_feature_selection(data_file, models_path)

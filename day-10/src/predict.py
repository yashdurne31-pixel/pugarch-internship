"""
predict.py
==========
Prediction module for the Smart Hygiene Risk Prediction System.

Loads the saved model pipeline and generates predictions for new facility
inspection records.

DISCLAIMER
----------
Predictions are produced by a model trained on synthetic, rule-generated
data. They must NOT be used as official hygiene certifications or as a
substitute for professional facility inspections.

Illustrative input example
--------------------------
{
    "cleanliness_score": 35,
    "odor_score": 8,
    "waste_level": "High",
    "water_availability": "No",
    "footfall": 250,
    "complaints": 12
}

Usage (standalone)
------------------
    python src/predict.py
"""

from __future__ import annotations

import os
import sys

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import warnings
import joblib
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# ── paths ────────────────────────────────────────────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(_HERE, "..", "models", "hygiene_risk_model.joblib")

# ── required input fields ────────────────────────────────────────────────────
REQUIRED_FIELDS = [
    "cleanliness_score",
    "odor_score",
    "waste_level",
    "water_availability",
    "footfall",
    "complaints",
]

VALID_WASTE_LEVELS = {"Low", "Medium", "High"}
VALID_WATER_OPTIONS = {"Yes", "No"}


# ── validation ────────────────────────────────────────────────────────────────

def validate_input(record: dict) -> tuple:
    """
    Validate a single inspection record dictionary.

    Parameters
    ----------
    record : dict
        Raw input fields.

    Returns
    -------
    tuple (is_valid: bool, errors: list[str])
    """
    errors = []

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in record:
            errors.append(f"Missing required field: '{field}'")

    if errors:
        return False, errors

    # Numeric range validation
    cs = record.get("cleanliness_score")
    if cs is not None and not (0 <= float(cs) <= 100):
        errors.append(f"'cleanliness_score' must be between 0 and 100. Got: {cs}")

    os_val = record.get("odor_score")
    if os_val is not None and not (0 <= float(os_val) <= 10):
        errors.append(f"'odor_score' must be between 0 and 10. Got: {os_val}")

    ft = record.get("footfall")
    if ft is not None and float(ft) < 0:
        errors.append(f"'footfall' must be non-negative. Got: {ft}")

    cp = record.get("complaints")
    if cp is not None and float(cp) < 0:
        errors.append(f"'complaints' must be non-negative. Got: {cp}")

    # Categorical validation
    wl = record.get("waste_level")
    if wl not in VALID_WASTE_LEVELS:
        errors.append(f"'waste_level' must be one of {VALID_WASTE_LEVELS}. Got: '{wl}'")

    wa = record.get("water_availability")
    if wa not in VALID_WATER_OPTIONS:
        errors.append(f"'water_availability' must be one of {VALID_WATER_OPTIONS}. Got: '{wa}'")

    return len(errors) == 0, errors


# ── model loading ─────────────────────────────────────────────────────────────

def load_model(path: str = MODEL_PATH) -> dict:
    """
    Load the saved model bundle from disk.

    Parameters
    ----------
    path : str
        Path to the .joblib file.

    Returns
    -------
    dict with keys: preprocessor, model, classes, feature_names, metadata
    """
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Model file not found: {path}\n"
            "Run  python src/train_model.py  first."
        )
    bundle = joblib.load(path)
    return bundle


# ── prediction ────────────────────────────────────────────────────────────────

def predict(record: dict, bundle=None) -> dict:
    """
    Predict the hygiene risk category for a single facility inspection record.

    Parameters
    ----------
    record : dict
        Input inspection fields. See REQUIRED_FIELDS for mandatory keys.
    bundle : dict or None
        Pre-loaded model bundle. If None, the bundle is loaded from MODEL_PATH.

    Returns
    -------
    dict with keys:
        - predicted_class : str  (Low / Medium / High)
        - probabilities   : dict {class_name: probability}
        - model_name      : str
        - disclaimer      : str
    """
    # Validate
    is_valid, errors = validate_input(record)
    if not is_valid:
        raise ValueError("Input validation failed:\n" + "\n".join(f"  - {e}" for e in errors))

    if bundle is None:
        bundle = load_model()

    preprocessor = bundle["preprocessor"]
    model = bundle["model"]
    classes = bundle["classes"]

    # Build a single-row DataFrame that matches the training schema.
    # Date features (inspection_month, inspection_dayofweek) are set to
    # median-like defaults when not supplied by the caller.
    row = {
        "cleanliness_score":   float(record["cleanliness_score"]),
        "odor_score":          float(record["odor_score"]),
        "waste_level":         record["waste_level"],
        "water_availability":  record["water_availability"],
        "footfall":            float(record["footfall"]),
        "complaints":          float(record["complaints"]),
        "inspection_month":    float(record.get("inspection_month", 6)),      # default: June
        "inspection_dayofweek": float(record.get("inspection_dayofweek", 2)),  # default: Wednesday
    }

    df_input = pd.DataFrame([row])
    X_proc = preprocessor.transform(df_input)

    predicted_class = model.predict(X_proc)[0]

    proba_dict = {}
    if hasattr(model, "predict_proba"):
        probas = model.predict_proba(X_proc)[0]
        proba_dict = {cls: round(float(p), 4) for cls, p in zip(classes, probas)}

    return {
        "predicted_class": predicted_class,
        "probabilities": proba_dict,
        "model_name": bundle.get("model_name", "Unknown"),
        "disclaimer": (
            "Prediction is based on a model trained on synthetic, rule-generated "
            "data. Do NOT use this as an official hygiene certification."
        ),
    }


# ── standalone demo ───────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  HYGIENE RISK PREDICTION — DEMO")
    print("=" * 60)

    # Illustrative test cases (not real facilities)
    test_cases = [
        {
            "name": "High-risk scenario",
            "record": {
                "cleanliness_score": 25,
                "odor_score": 9,
                "waste_level": "High",
                "water_availability": "No",
                "footfall": 400,
                "complaints": 18,
            },
        },
        {
            "name": "Low-risk scenario",
            "record": {
                "cleanliness_score": 90,
                "odor_score": 1,
                "waste_level": "Low",
                "water_availability": "Yes",
                "footfall": 80,
                "complaints": 0,
            },
        },
        {
            "name": "Medium-risk scenario",
            "record": {
                "cleanliness_score": 55,
                "odor_score": 5,
                "waste_level": "Medium",
                "water_availability": "Yes",
                "footfall": 200,
                "complaints": 5,
            },
        },
    ]

    bundle = load_model()
    print(f"[OK] Model loaded: {bundle.get('model_name')}")
    print(f"     Classes     : {bundle['classes']}")

    for case in test_cases:
        print(f"\n{'-'*50}")
        print(f"  Test: {case['name']}")
        print(f"  Input: {case['record']}")
        result = predict(case["record"], bundle)
        print(f"  -> Predicted Class : {result['predicted_class']}")
        if result["probabilities"]:
            proba_str = "  | ".join(f"{k}: {v:.2%}" for k, v in result["probabilities"].items())
            print(f"  -> Probabilities   : {proba_str}")
        print(f"  [!] {result['disclaimer']}")

    # Demo: invalid input handling
    print(f"\n{'-'*50}")
    print("  Test: Invalid input (missing field + out-of-range value)")
    bad_record = {"cleanliness_score": 150, "odor_score": -1}
    try:
        predict(bad_record, bundle)
    except ValueError as e:
        print(f"  → Validation Error caught correctly:\n{e}")

    print("\n[OK] Prediction demo complete.")


if __name__ == "__main__":
    main()

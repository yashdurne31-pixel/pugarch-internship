"""
data_preprocessing.py
=====================
Data loading and preprocessing pipeline for the Smart Hygiene Risk Prediction System.

Responsibilities
----------------
1. Load the CSV dataset and report basic shape/dtype information.
2. Display missing-value counts and duplicate record counts.
3. Drop the `facility_id` column (unique identifier — not a predictive feature).
4. Extract date features (inspection month, day-of-week) from `inspection_date`.
5. Separate features (X) from the target column (y = `hygiene_risk`).
6. Build a scikit-learn ColumnTransformer pipeline:
   - Numeric columns  → SimpleImputer(median) → StandardScaler
   - Categorical cols → SimpleImputer(most_frequent) → OneHotEncoder
7. Return a train/test split with stratification.
8. Fit the preprocessor ONLY on training data to prevent data leakage.

NOTE ON TARGET LEAKAGE
-----------------------
The target `hygiene_risk` in this dataset is rule-generated from the input
features. If we were to include the raw components of that rule as features,
the model would learn a near-perfect approximation. We exclude `facility_id`
and `location` from the model features but retain numeric inspection scores and
categorical inspection attributes. The evaluation metrics therefore reflect how
well the model approximates the labeling rule, NOT real-world hygiene outcomes.

Usage
-----
    from src.data_preprocessing import load_and_preprocess

    X_train, X_test, y_train, y_test, preprocessor, feature_names = load_and_preprocess()
"""

import os
import sys

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

# ── paths ────────────────────────────────────────────────────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(_HERE, "..", "data", "hygiene_inspections.csv")

# ── column definitions ───────────────────────────────────────────────────────
TARGET_COL = "hygiene_risk"
DROP_COLS = ["facility_id", "location"]      # identifiers, not predictive
DATE_COL = "inspection_date"

NUMERIC_FEATURES = [
    "cleanliness_score",
    "odor_score",
    "footfall",
    "complaints",
    "inspection_month",
    "inspection_dayofweek",
]

CATEGORICAL_FEATURES = [
    "waste_level",
    "water_availability",
]


# ── helpers ──────────────────────────────────────────────────────────────────

def load_raw(path: str = DATA_PATH) -> pd.DataFrame:
    """
    Load the raw CSV dataset and display basic information.

    Parameters
    ----------
    path : str
        Path to the hygiene_inspections.csv file.

    Returns
    -------
    pd.DataFrame
        Raw DataFrame.
    """
    if not os.path.exists(path):
        print(f"[ERROR] Dataset not found at: {path}")
        print("        Run  python data/generate_data.py  first.")
        sys.exit(1)

    df = pd.read_csv(path)

    print("\n" + "=" * 60)
    print("  DATA LOADING REPORT")
    print("=" * 60)
    print(f"  Rows    : {df.shape[0]}")
    print(f"  Columns : {df.shape[1]}")
    print("\nColumn names and data types:")
    print(df.dtypes.to_string())

    print("\nMissing values per column:")
    missing = df.isnull().sum()
    print(missing[missing > 0].to_string() if missing.any() else "  None detected")

    duplicates = df.duplicated().sum()
    print(f"\nDuplicate rows: {duplicates}")
    if duplicates > 0:
        df = df.drop_duplicates()
        print(f"  -> Dropped {duplicates} duplicate(s). Remaining rows: {len(df)}")

    return df


def extract_date_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parse `inspection_date` and create numeric month / day-of-week features.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing the `inspection_date` column.

    Returns
    -------
    pd.DataFrame
        DataFrame with new date-derived columns and original date column dropped.
    """
    df = df.copy()
    if DATE_COL in df.columns:
        dt = pd.to_datetime(df[DATE_COL], errors="coerce")
        df["inspection_month"] = dt.dt.month.astype(float)
        df["inspection_dayofweek"] = dt.dt.dayofweek.astype(float)
        df.drop(columns=[DATE_COL], inplace=True)
    return df


def build_preprocessor() -> ColumnTransformer:
    """
    Build a scikit-learn ColumnTransformer that handles numeric and
    categorical columns independently.

    The preprocessor is returned UNFITTED so it can be fitted exclusively
    on training data.

    Returns
    -------
    ColumnTransformer
        Unfitted preprocessing transformer.
    """
    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, NUMERIC_FEATURES),
            ("cat", categorical_pipeline, CATEGORICAL_FEATURES),
        ],
        remainder="drop",
    )
    return preprocessor


def load_and_preprocess(
    path: str = DATA_PATH,
    test_size: float = 0.20,
    random_state: int = 42,
):
    """
    Full preprocessing pipeline: load → clean → split → fit preprocessor.

    Parameters
    ----------
    path : str
        Path to the CSV dataset.
    test_size : float
        Fraction of data used for testing (default 0.20).
    random_state : int
        Random seed for reproducibility.

    Returns
    -------
    tuple
        (X_train_proc, X_test_proc, y_train, y_test, preprocessor, feature_names)
        - X_train_proc : np.ndarray — preprocessed training features
        - X_test_proc  : np.ndarray — preprocessed test features
        - y_train      : pd.Series  — training labels
        - y_test       : pd.Series  — test labels
        - preprocessor : fitted ColumnTransformer
        - feature_names: list[str]  — output feature names after encoding
    """
    df = load_raw(path)
    df = extract_date_features(df)

    # Drop identifier columns
    df.drop(columns=[c for c in DROP_COLS if c in df.columns], inplace=True)

    # Separate target
    if TARGET_COL not in df.columns:
        print(f"[ERROR] Target column '{TARGET_COL}' not found in dataset.")
        sys.exit(1)

    X = df.drop(columns=[TARGET_COL])
    y = df[TARGET_COL]

    print(f"\nFeature matrix shape : {X.shape}")
    print(f"Target series shape  : {y.shape}")
    print(f"\nClass distribution (before split):")
    print(y.value_counts().to_string())

    # Train / test split with stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

    # Fit preprocessor on TRAINING data only
    preprocessor = build_preprocessor()
    X_train_proc = preprocessor.fit_transform(X_train)
    X_test_proc = preprocessor.transform(X_test)

    # Derive output feature names
    ohe = preprocessor.named_transformers_["cat"]["encoder"]
    cat_feature_names = list(ohe.get_feature_names_out(CATEGORICAL_FEATURES))
    feature_names = NUMERIC_FEATURES + cat_feature_names

    print(f"\nPreprocessed training set shape : {X_train_proc.shape}")
    print(f"Preprocessed test set shape     : {X_test_proc.shape}")
    print(f"Total output features           : {len(feature_names)}")

    return X_train_proc, X_test_proc, y_train, y_test, preprocessor, feature_names


# ── standalone execution ─────────────────────────────────────────────────────
if __name__ == "__main__":
    load_and_preprocess()
    print("\n[OK] Preprocessing completed successfully.")

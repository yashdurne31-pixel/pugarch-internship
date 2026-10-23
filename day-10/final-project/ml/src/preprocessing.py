"""
Preprocessing Pipeline for Smart Hygiene Risk Prediction System.
Handles missing value imputation, outlier management, categorical encoding, and feature scaling.
"""

import os
import joblib
import numpy as np
import pandas as pd
from typing import Tuple, List, Optional, Dict, Any
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


NUMERICAL_FEATURES: List[str] = [
    "temperature_compliance_score",
    "sanitation_protocol_score",
    "water_potability_index",
    "ppe_handwashing_score",
    "pest_control_score",
    "food_handler_cert_ratio",
    "structural_maintenance_score",
    "waste_management_score",
    "cross_contamination_control",
    "historical_violation_count",
    "ambient_kitchen_temp",
    "relative_humidity",
]

CATEGORICAL_FEATURES: List[str] = [
    "facility_type",
    "inspection_type",
]

TARGET_COL_CLASS: str = "hygiene_risk_level"
TARGET_COL_REG: str = "hygiene_risk_score"

RISK_CLASS_MAPPING: Dict[str, int] = {
    "Low Risk": 0,
    "Medium Risk": 1,
    "High Risk": 2,
}

INV_RISK_CLASS_MAPPING: Dict[int, str] = {
    0: "Low Risk",
    1: "Medium Risk",
    2: "High Risk",
}


class OutlierCapper(BaseEstimator, TransformerMixin):
    """
    Caps numerical features within realistic domain bounds / IQR percentiles
    to prevent adverse skew in linear and distance-based estimators.
    """
    def __init__(self, factor: float = 1.5):
        self.factor = factor
        self.lower_bounds_: Dict[str, float] = {}
        self.upper_bounds_: Dict[str, float] = {}

    def fit(self, X, y=None):
        X_df = pd.DataFrame(X).copy()
        for col in X_df.columns:
            q25 = X_df[col].quantile(0.01)
            q75 = X_df[col].quantile(0.99)
            iqr = q75 - q25
            self.lower_bounds_[col] = q25 - self.factor * iqr
            self.upper_bounds_[col] = q75 + self.factor * iqr
        return self

    def transform(self, X):
        X_df = pd.DataFrame(X).copy()
        for col in X_df.columns:
            if col in self.lower_bounds_:
                X_df[col] = np.clip(X_df[col], self.lower_bounds_[col], self.upper_bounds_[col])
        return X_df.values


class HygieneDataPreprocessor:
    """
    Complete production preprocessor encapsulating imputation, encoding, and scaling.
    """
    def __init__(self):
        self.numerical_features = NUMERICAL_FEATURES
        self.categorical_features = CATEGORICAL_FEATURES
        self.column_transformer: Optional[ColumnTransformer] = None
        self.feature_names_out: List[str] = []
        self.is_fitted: bool = False

    def build_pipeline(self) -> ColumnTransformer:
        num_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("outlier_capper", OutlierCapper()),
            ("scaler", StandardScaler()),
        ])

        cat_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", num_pipeline, self.numerical_features),
                ("cat", cat_pipeline, self.categorical_features),
            ],
            remainder="drop",
        )
        return preprocessor

    def fit(self, df: pd.DataFrame) -> "HygieneDataPreprocessor":
        self.column_transformer = self.build_pipeline()
        self.column_transformer.fit(df)

        # Extract output feature names
        num_names = self.numerical_features
        cat_encoder = self.column_transformer.named_transformers_["cat"].named_steps["encoder"]
        cat_names = list(cat_encoder.get_feature_names_out(self.categorical_features))
        self.feature_names_out = num_names + cat_names
        self.is_fitted = True
        return self

    def transform(self, df: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted or self.column_transformer is None:
            raise ValueError("Preprocessor is not fitted yet. Call fit() first.")
        return self.column_transformer.transform(df)

    def fit_transform(self, df: pd.DataFrame) -> np.ndarray:
        return self.fit(df).transform(df)

    def encode_labels(self, labels: pd.Series) -> np.ndarray:
        """Map categorical risk levels to integers (0, 1, 2)"""
        return np.array([RISK_CLASS_MAPPING.get(lbl, 1) for lbl in labels])

    def decode_labels(self, label_ids: np.ndarray) -> List[str]:
        """Convert integer class predictions back to descriptive string levels"""
        return [INV_RISK_CLASS_MAPPING.get(int(idx), "Medium Risk") for idx in label_ids]

    def save(self, filepath: str) -> None:
        """Persist preprocessor to disk using joblib"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self, filepath)

    @classmethod
    def load(cls, filepath: str) -> "HygieneDataPreprocessor":
        """Load persisted preprocessor from disk"""
        return joblib.load(filepath)


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "..", "data", "hygiene_inspections.csv")
    
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        preprocessor = HygieneDataPreprocessor()
        X_trans = preprocessor.fit_transform(df)
        print("Preprocessor fit & transform successful!")
        print(f"Original shape: {df.shape}")
        print(f"Transformed feature matrix shape: {X_trans.shape}")
        print(f"Engineered features ({len(preprocessor.feature_names_out)}):")
        for i, fname in enumerate(preprocessor.feature_names_out):
            print(f"  [{i+1}] {fname}")
        
        save_path = os.path.join(current_dir, "..", "models", "preprocessor.joblib")
        preprocessor.save(save_path)
        print(f"Saved preprocessor to: {save_path}")
    else:
        print(f"Data file not found at {data_path}. Run dataset_generator.py first.")

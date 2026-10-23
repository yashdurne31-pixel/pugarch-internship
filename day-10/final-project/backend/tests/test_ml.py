"""
Unit and Integration Tests for Machine Learning Pipeline.
Smart Hygiene Risk Prediction System.
"""

import os
import sys
import pytest
import numpy as np
import pandas as pd

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(TEST_DIR, "..", ".."))
sys.path.append(os.path.join(PROJECT_ROOT, "ml", "src"))

from preprocessing import HygieneDataPreprocessor, NUMERICAL_FEATURES, CATEGORICAL_FEATURES
from predict import HygienePredictor


def test_preprocessor_fit_transform():
    sample_df = pd.DataFrame([{
        "facility_type": "Restaurant",
        "inspection_type": "Routine",
        "temperature_compliance_score": 90.0,
        "sanitation_protocol_score": 88.0,
        "water_potability_index": 92.0,
        "ppe_handwashing_score": 85.0,
        "pest_control_score": 89.0,
        "food_handler_cert_ratio": 95.0,
        "structural_maintenance_score": 80.0,
        "waste_management_score": 85.0,
        "cross_contamination_control": 90.0,
        "historical_violation_count": 0,
        "ambient_kitchen_temp": 24.0,
        "relative_humidity": 50.0,
        "hygiene_risk_level": "Low Risk",
        "hygiene_risk_score": 15.0,
    }])

    preprocessor = HygieneDataPreprocessor()
    X = preprocessor.fit_transform(sample_df)
    assert X is not None
    assert X.shape[0] == 1
    assert len(preprocessor.feature_names_out) > len(NUMERICAL_FEATURES)


def test_label_encoding():
    preprocessor = HygieneDataPreprocessor()
    labels = pd.Series(["Low Risk", "Medium Risk", "High Risk", "Unknown"])
    encoded = preprocessor.encode_labels(labels)
    assert list(encoded[:3]) == [0, 1, 2]

    decoded = preprocessor.decode_labels(np.array([0, 1, 2]))
    assert decoded == ["Low Risk", "Medium Risk", "High Risk"]


def test_predictor_inference():
    predictor = HygienePredictor()

    safe_sample = {
        "facility_type": "Restaurant",
        "inspection_type": "Routine",
        "temperature_compliance_score": 98.0,
        "sanitation_protocol_score": 96.0,
        "water_potability_index": 99.0,
        "ppe_handwashing_score": 95.0,
        "pest_control_score": 98.0,
        "food_handler_cert_ratio": 95.0,
        "structural_maintenance_score": 92.0,
        "waste_management_score": 94.0,
        "cross_contamination_control": 98.0,
        "historical_violation_count": 0,
        "ambient_kitchen_temp": 23.0,
        "relative_humidity": 48.0,
    }

    res = predictor.predict_single(safe_sample)
    assert res["status"] == "success"
    assert res["predicted_risk_level"] == "Low Risk"
    assert res["predicted_risk_score"] < 35.0
    assert "Grade A" in res["hygiene_grade"]
    assert res["confidence_percentage"] >= 50.0
    assert "Low Risk" in res["class_probabilities"]


def test_predictor_hazardous_facility():
    predictor = HygienePredictor()

    hazard_sample = {
        "facility_type": "Fast Food",
        "inspection_type": "Complaint-driven",
        "temperature_compliance_score": 25.0,
        "sanitation_protocol_score": 30.0,
        "water_potability_index": 45.0,
        "ppe_handwashing_score": 20.0,
        "pest_control_score": 15.0,
        "food_handler_cert_ratio": 20.0,
        "structural_maintenance_score": 35.0,
        "waste_management_score": 30.0,
        "cross_contamination_control": 20.0,
        "historical_violation_count": 9,
        "ambient_kitchen_temp": 39.0,
        "relative_humidity": 88.0,
    }

    res = predictor.predict_single(hazard_sample)
    assert res["predicted_risk_level"] == "High Risk"
    assert res["predicted_risk_score"] >= 62.0
    assert "Grade C" in res["hygiene_grade"]
    assert len(res["recommendations"]) > 0
    # Check that critical pest or temperature recommendations are triggered
    rec_texts = " ".join(res["recommendations"])
    assert "CRITICAL" in rec_texts

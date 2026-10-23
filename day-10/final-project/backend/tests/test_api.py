"""
Integration Tests for REST API Endpoints.
Smart Hygiene Risk Prediction System.
"""

import os
import sys
import pytest
from starlette.testclient import TestClient

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(TEST_DIR, "..", ".."))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "backend"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "database"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "ml", "src"))

from main import app

client = TestClient(app)


def test_health_check_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database_connected"] is True


def test_predict_endpoint_valid():
    payload = {
        "facility_type": "Restaurant",
        "inspection_type": "Routine",
        "temperature_compliance_score": 92.0,
        "sanitation_protocol_score": 90.0,
        "water_potability_index": 95.0,
        "ppe_handwashing_score": 88.0,
        "pest_control_score": 91.0,
        "food_handler_cert_ratio": 85.0,
        "structural_maintenance_score": 85.0,
        "waste_management_score": 88.0,
        "cross_contamination_control": 92.0,
        "historical_violation_count": 0,
        "ambient_kitchen_temp": 24.0,
        "relative_humidity": 50.0,
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["predicted_risk_level"] in ["Low Risk", "Medium Risk", "High Risk"]
    assert "hygiene_grade" in data
    assert "class_probabilities" in data
    assert isinstance(data["recommendations"], list)


def test_predict_endpoint_validation_error():
    # Negative score violates ge=0.0 schema constraint
    payload = {
        "facility_type": "Restaurant",
        "temperature_compliance_score": -15.0,
        "sanitation_protocol_score": 90.0,
        "water_potability_index": 95.0,
        "ppe_handwashing_score": 88.0,
        "pest_control_score": 91.0,
        "cross_contamination_control": 92.0,
    }
    response = client.post("/api/predict", json=payload)
    assert response.status_code == 422
    err_json = response.json()
    assert err_json["status"] == "error"
    assert err_json["error_type"] == "ValidationError"


def test_predict_csv_upload():
    csv_content = (
        "facility_type,temperature_compliance_score,sanitation_protocol_score,water_potability_index,pest_control_score,cross_contamination_control\n"
        "Restaurant,95.0,90.0,98.0,92.0,94.0\n"
        "Hospital,80.0,85.0,90.0,88.0,82.0\n"
    )
    files = {"file": ("test.csv", csv_content.encode("utf-8"), "text/csv")}
    response = client.post("/api/predict/upload-csv", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["total_rows_evaluated"] == 2
    assert len(data["results"]) == 2



def test_facilities_endpoint():
    response = client.get("/api/facilities")
    assert response.status_code == 200
    facilities = response.json()
    assert isinstance(facilities, list)
    assert len(facilities) > 0


def test_inspections_endpoint():
    response = client.get("/api/inspections?limit=10")
    assert response.status_code == 200
    inspections = response.json()
    assert isinstance(inspections, list)
    if inspections:
        assert "predicted_risk_level" in inspections[0]


def test_analytics_endpoints():
    # Stats
    res_stats = client.get("/api/analytics/stats")
    assert res_stats.status_code == 200
    stats = res_stats.json()
    assert "total_facilities" in stats
    assert "risk_distribution" in stats

    # Feature Importance
    res_fi = client.get("/api/analytics/feature-importance")
    assert res_fi.status_code == 200
    fi = res_fi.json()
    assert "ranked_features" in fi

    # Model Info
    res_model = client.get("/api/analytics/model-info")
    assert res_model.status_code == 200
    model_info = res_model.json()
    assert "metrics" in model_info
    assert "best_model_name" in model_info["metrics"]

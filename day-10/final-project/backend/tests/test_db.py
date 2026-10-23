"""
Unit and Integration Tests for Database and Repository.
Smart Hygiene Risk Prediction System.
"""

import os
import sys
import pytest

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(TEST_DIR, "..", ".."))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "database"))

from db import initialize_database
from repository import HygieneRepository


@pytest.fixture(scope="module")
def setup_db():
    initialize_database()
    return HygieneRepository()


def test_facility_creation_and_retrieval(setup_db):
    repo = setup_db
    import uuid
    lic = f"LIC-TEST-{uuid.uuid4().hex[:6]}"
    facility_data = {
        "name": "Test Gourmet Kitchen",
        "facility_type": "Restaurant",
        "license_number": lic,
        "address": "123 Test Street",
        "contact_email": "test@kitchen.com",
        "contact_phone": "+1 555-0199",
        "rating_grade": "Grade A",
    }
    f_id = repo.create_facility(facility_data)
    assert f_id > 0

    fetched = repo.get_facility_by_id(f_id)
    assert fetched is not None
    assert fetched["name"] == "Test Gourmet Kitchen"
    assert fetched["license_number"] == lic


def test_inspection_creation_and_stats(setup_db):
    repo = setup_db
    facilities = repo.get_all_facilities()
    assert len(facilities) > 0
    f_id = facilities[0]["id"]

    insp_data = {
        "facility_id": f_id,
        "inspector_name": "Unit Tester",
        "inspection_date": "2026-10-23",
        "inspection_type": "Routine",
        "temperature_compliance_score": 95.0,
        "sanitation_protocol_score": 92.0,
        "water_potability_index": 98.0,
        "ppe_handwashing_score": 90.0,
        "pest_control_score": 94.0,
        "food_handler_cert_ratio": 92.0,
        "structural_maintenance_score": 88.0,
        "waste_management_score": 90.0,
        "cross_contamination_control": 95.0,
        "historical_violation_count": 0,
        "ambient_kitchen_temp": 24.0,
        "relative_humidity": 50.0,
        "predicted_risk_level": "Low Risk",
        "predicted_risk_score": 12.5,
        "hygiene_grade": "Grade A (Pristine Compliance)",
        "confidence_percentage": 98.5,
        "recommendations": ["Routine monitoring approved."],
        "notes": "Automated unit test record",
    }

    insp_id = repo.create_inspection(insp_data)
    assert insp_id > 0

    fetched = repo.get_inspection_by_id(insp_id)
    assert fetched is not None
    assert fetched["inspector_name"] == "Unit Tester"
    assert fetched["predicted_risk_level"] == "Low Risk"

    # Verify system stats calculation
    stats = repo.get_system_stats()
    assert stats["total_facilities"] >= 1
    assert stats["total_inspections"] >= 1
    assert "Low Risk" in stats["risk_distribution"]

"""
FastAPI Routes for Inspection Logging, History, and CRUD.
Smart Hygiene Risk Prediction System.
"""

import os
import sys
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query

# Ensure local directories are in Python path for standalone & package executions
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))

for path in [BACKEND_DIR, PROJECT_ROOT, os.path.join(PROJECT_ROOT, "database"), os.path.join(PROJECT_ROOT, "ml", "src")]:
    if path not in sys.path:
        sys.path.insert(0, path)

try:
    from backend.schemas import InspectionCreateRecord, InspectionResponse
except ImportError:
    from schemas import InspectionCreateRecord, InspectionResponse

try:
    from database.repository import HygieneRepository
except (ImportError, ValueError):
    from repository import HygieneRepository

try:
    from ml.src.predict import HygienePredictor
except (ImportError, ValueError):
    from predict import HygienePredictor

router = APIRouter(prefix="/api/inspections", tags=["Inspections Management"])

repo = HygieneRepository()
predictor = None


def get_predictor() -> HygienePredictor:
    global predictor
    if predictor is None:
        predictor = HygienePredictor()
    return predictor


@router.get("", response_model=List[InspectionResponse])
def get_all_inspections(
    risk: Optional[str] = Query(None, description="Filter by risk level (Low Risk, Medium Risk, High Risk)"),
    search: Optional[str] = Query(None, description="Search by facility name, license, inspector"),
    limit: int = Query(100, ge=1, le=500),
):
    """
    Retrieve inspection logs with optional risk filtering and keyword search.
    """
    try:
        records = repo.get_all_inspections(limit=limit, risk_filter=risk, search=search)
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")


@router.post("", response_model=InspectionResponse)
def create_new_inspection(payload: InspectionCreateRecord):
    """
    Record an official inspection: automatically executes ML inference,
    computes risk score, generates corrective remediation alerts, and updates facility rating.
    """
    # 1. Verify facility exists
    facility = repo.get_facility_by_id(payload.facility_id)
    if not facility:
        raise HTTPException(status_code=404, detail=f"Facility ID {payload.facility_id} not found.")

    try:
        # 2. Run ML prediction on the inspection data
        input_dict = payload.model_dump()
        input_dict["facility_type"] = facility["facility_type"]

        pred_res = get_predictor().predict_single(input_dict)

        # 3. Save to database
        db_payload = {
            **input_dict,
            "predicted_risk_level": pred_res["predicted_risk_level"],
            "predicted_risk_score": pred_res["predicted_risk_score"],
            "hygiene_grade": pred_res["hygiene_grade"],
            "confidence_percentage": pred_res["confidence_percentage"],
            "recommendations": pred_res["recommendations"],
        }

        inspection_id = repo.create_inspection(db_payload)

        # 4. Return complete inspection record
        created = repo.get_inspection_by_id(inspection_id)
        return created
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to record inspection: {str(e)}")


@router.get("/{inspection_id}", response_model=InspectionResponse)
def get_inspection_details(inspection_id: int):
    """
    Retrieve comprehensive inspection report by ID.
    """
    record = repo.get_inspection_by_id(inspection_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Inspection ID {inspection_id} not found.")
    return record


@router.delete("/{inspection_id}")
def delete_inspection(inspection_id: int):
    """
    Delete an inspection record.
    """
    success = repo.delete_inspection(inspection_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Inspection ID {inspection_id} not found.")
    return {"status": "success", "message": f"Inspection #{inspection_id} deleted."}


if __name__ == "__main__":
    records = repo.get_all_inspections(limit=5)
    print(f"Inspections loaded: {len(records)}")

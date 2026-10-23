"""
FastAPI Routes for Facility Registry and Profiling.
Smart Hygiene Risk Prediction System.
"""

import os
import sys
from typing import List
from fastapi import APIRouter, HTTPException

# Ensure local directories are in Python path for standalone & package executions
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))

for path in [BACKEND_DIR, PROJECT_ROOT, os.path.join(PROJECT_ROOT, "database"), os.path.join(PROJECT_ROOT, "ml", "src")]:
    if path not in sys.path:
        sys.path.insert(0, path)

try:
    from backend.schemas import FacilityCreate, FacilityResponse
except ImportError:
    from schemas import FacilityCreate, FacilityResponse

try:
    from database.repository import HygieneRepository
except (ImportError, ValueError):
    # pyrefly: ignore[missing-import]
    from repository import HygieneRepository

router = APIRouter(prefix="/api/facilities", tags=["Facilities Registry"])
repo = HygieneRepository()


@router.get("", response_model=List[FacilityResponse])
def get_all_facilities():
    """
    Retrieve registered facilities.
    """
    try:
        return repo.get_all_facilities()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@router.post("", response_model=FacilityResponse)
def register_new_facility(payload: FacilityCreate):
    """
    Register a new food facility or commercial kitchen.
    """
    try:
        f_id = repo.create_facility(payload.model_dump())
        created = repo.get_facility_by_id(f_id)
        return created
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to register facility: {str(e)}")


@router.get("/{facility_id}", response_model=FacilityResponse)
def get_facility(facility_id: int):
    """
    Retrieve single facility profile by ID.
    """
    fac = repo.get_facility_by_id(facility_id)
    if not fac:
        raise HTTPException(status_code=404, detail=f"Facility ID {facility_id} not found.")
    return fac


if __name__ == "__main__":
    facilities = repo.get_all_facilities()
    print(f"Facilities loaded: {len(facilities)}")

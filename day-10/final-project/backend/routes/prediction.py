"""
FastAPI Routes for ML Prediction (Single, Batch, CSV Upload).
Smart Hygiene Risk Prediction System.
"""

import io
import csv
import os
import sys
from typing import List
import pandas as pd
from fastapi import APIRouter, HTTPException, UploadFile, File

# Ensure local directories are in Python path for standalone & package executions
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))

for path in [BACKEND_DIR, PROJECT_ROOT, os.path.join(PROJECT_ROOT, "database"), os.path.join(PROJECT_ROOT, "ml", "src")]:
    if path not in sys.path:
        sys.path.insert(0, path)

try:
    from backend.schemas import (
        PredictionRequest,
        PredictionResponse,
        BatchPredictionRequest,
        BatchPredictionResponse,
    )
except ImportError:
    from schemas import (
        PredictionRequest,
        PredictionResponse,
        BatchPredictionRequest,
        BatchPredictionResponse,
    )

try:
    from ml.src.predict import HygienePredictor
except (ImportError, ValueError):
    # pyrefly: ignore[missing-import]
    from predict import HygienePredictor

router = APIRouter(prefix="/api/predict", tags=["Prediction Engine"])

predictor = None

def get_predictor() -> HygienePredictor:
    global predictor
    if predictor is None:
        predictor = HygienePredictor()
    return predictor


@router.post("", response_model=PredictionResponse)
def predict_hygiene_risk(payload: PredictionRequest):
    """
    Evaluate single facility inspection metrics and return risk grade, probabilities, and recommendations.
    """
    pred_engine = get_predictor()
    try:
        data_dict = payload.model_dump()
        result = pred_engine.predict_single(data_dict)
        return result
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(err)}")


@router.post("/batch", response_model=BatchPredictionResponse)
def predict_batch_records(payload: BatchPredictionRequest):
    """
    Predict hygiene risk for a collection of facility inspection records in batch.
    """
    pred_engine = get_predictor()
    try:
        results = []
        for item in payload.inspections:
            res = pred_engine.predict_single(item.model_dump())
            results.append(res)

        return {
            "status": "success",
            "total_processed": len(results),
            "predictions": results,
        }
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Batch prediction error: {str(err)}")


@router.post("/upload-csv")
async def predict_from_csv(file: UploadFile = File(...)):
    """
    Upload a CSV containing facility inspection data, parse, score each row, and return predictions.
    """
    pred_engine = get_predictor()
    if not file.filename or not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a .csv format.")

    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

        # Check required columns
        required = [
            "temperature_compliance_score",
            "sanitation_protocol_score",
            "water_potability_index",
            "pest_control_score",
            "cross_contamination_control",
        ]
        missing = [col for col in required if col not in df.columns]
        if missing:
            raise HTTPException(
                status_code=422,
                detail=f"CSV missing mandatory inspection columns: {missing}",
            )

        # Set default values for optional missing columns
        defaults = {
            "facility_type": "Restaurant",
            "inspection_type": "Routine",
            "ppe_handwashing_score": 85.0,
            "food_handler_cert_ratio": 80.0,
            "structural_maintenance_score": 80.0,
            "waste_management_score": 80.0,
            "historical_violation_count": 0,
            "ambient_kitchen_temp": 24.5,
            "relative_humidity": 55.0,
        }
        for k, v in defaults.items():
            if k not in df.columns:
                df[k] = v

        records = df.to_dict(orient="records")
        annotated_results = []
        for idx, row in enumerate(records):
            prediction = pred_engine.predict_single(row)
            annotated_results.append({
                "row_index": idx + 1,
                "facility_type": row.get("facility_type", "Restaurant"),
                "predicted_risk_level": prediction["predicted_risk_level"],
                "predicted_risk_score": prediction["predicted_risk_score"],
                "hygiene_grade": prediction["hygiene_grade"],
                "confidence_percentage": prediction["confidence_percentage"],
                "recommendations": prediction["recommendations"][:2],  # top 2 for concise summary
            })

        return {
            "status": "success",
            "filename": file.filename,
            "total_rows_evaluated": len(annotated_results),
            "results": annotated_results,
        }
    except HTTPException:
        raise
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Error parsing and predicting CSV: {str(err)}")

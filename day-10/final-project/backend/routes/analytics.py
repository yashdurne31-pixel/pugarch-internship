"""
FastAPI Routes for Analytics, System KPIs, and Model Metadata.
Smart Hygiene Risk Prediction System.
"""

import os
import sys
import json
from fastapi import APIRouter, HTTPException

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
sys.path.append(os.path.join(PROJECT_ROOT, "database"))

# pyrefly: ignore[missing-import]
from repository import HygieneRepository

router = APIRouter(prefix="/api/analytics", tags=["Analytics & Model Intelligence"])
repo = HygieneRepository()


@router.get("/stats")
def get_system_kpis():
    """
    Retrieve live system dashboard KPIs: total facilities, total inspections,
    risk categorization distribution, critical hazard warnings, and average risk score.
    """
    try:
        return repo.get_system_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch system stats: {str(e)}")


@router.get("/feature-importance")
def get_feature_importances():
    """
    Retrieve ranked risk drivers and impact weights from the multi-metric feature selection analysis.
    """
    feat_path = os.path.join(PROJECT_ROOT, "ml", "models", "feature_importance.json")
    if not os.path.exists(feat_path):
        raise HTTPException(status_code=404, detail="Feature importance artifact not generated yet.")

    try:
        with open(feat_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read feature importance: {str(e)}")


@router.get("/model-info")
def get_model_information():
    """
    Retrieve ML benchmark results, cross-validation scores, accuracy, F1, and hyperparameter metadata.
    """
    metrics_path = os.path.join(PROJECT_ROOT, "ml", "models", "model_metrics.json")
    metadata_path = os.path.join(PROJECT_ROOT, "ml", "models", "metadata.json")

    if not os.path.exists(metrics_path):
        raise HTTPException(status_code=404, detail="Model metrics artifact not found.")

    try:
        with open(metrics_path, "r", encoding="utf-8") as f:
            metrics = json.load(f)

        metadata = {}
        if os.path.exists(metadata_path):
            with open(metadata_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)

        return {
            "metrics": metrics,
            "metadata": metadata,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load model info: {str(e)}")

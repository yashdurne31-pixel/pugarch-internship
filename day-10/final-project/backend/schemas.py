"""
Pydantic Schemas for Request Validation and Response Serialization.
Smart Hygiene Risk Prediction System.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class InspectionBase(BaseModel):
    facility_type: str = Field(default="Restaurant", description="Type of facility (Restaurant, Fast Food, Hospital Cafeteria, etc.)")
    inspection_type: str = Field(default="Routine", description="Routine, Follow-up, Complaint-driven, License Renewal")
    temperature_compliance_score: float = Field(..., ge=0.0, le=100.0, description="Compliance score (0-100)")
    sanitation_protocol_score: float = Field(..., ge=0.0, le=100.0, description="Cleanliness and sanitizer adherence (0-100)")
    water_potability_index: float = Field(..., ge=0.0, le=100.0, description="Water safety and purity index (0-100)")
    ppe_handwashing_score: float = Field(..., ge=0.0, le=100.0, description="Hand hygiene station adherence (0-100)")
    pest_control_score: float = Field(..., ge=0.0, le=100.0, description="Absence of infestation and pest barrier score (0-100)")
    food_handler_cert_ratio: float = Field(default=85.0, ge=0.0, le=100.0, description="Certified staff percentage (0-100)")
    structural_maintenance_score: float = Field(default=80.0, ge=0.0, le=100.0, description="Building & equipment integrity score (0-100)")
    waste_management_score: float = Field(default=80.0, ge=0.0, le=100.0, description="Waste segregation and containment score (0-100)")
    cross_contamination_control: float = Field(..., ge=0.0, le=100.0, description="Separation of raw and cooked zones (0-100)")
    historical_violation_count: int = Field(default=0, ge=0, le=30, description="Recorded past non-compliances")
    ambient_kitchen_temp: float = Field(default=24.0, ge=10.0, le=55.0, description="Ambient kitchen temperature in Celsius")
    relative_humidity: float = Field(default=55.0, ge=10.0, le=100.0, description="Relative humidity %")


class PredictionRequest(InspectionBase):
    pass


class KeyRiskDriver(BaseModel):
    feature: str
    value: float
    impact: str
    severity: str


class PredictionResponse(BaseModel):
    status: str
    predicted_risk_level: str
    predicted_risk_score: float
    hygiene_grade: str
    confidence_percentage: float
    class_probabilities: Dict[str, float]
    recommendations: List[str]
    key_risk_drivers: List[KeyRiskDriver]


class BatchPredictionRequest(BaseModel):
    inspections: List[InspectionBase]


class BatchPredictionResponse(BaseModel):
    status: str
    total_processed: int
    predictions: List[PredictionResponse]


class FacilityCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    facility_type: str = Field(...)
    license_number: str = Field(..., min_length=3, max_length=50)
    address: str = Field(..., min_length=5, max_length=250)
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None


class FacilityResponse(BaseModel):
    id: int
    name: str
    facility_type: str
    license_number: str
    address: str
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    rating_grade: Optional[str] = "Grade A"
    created_at: Optional[str] = None


class InspectionCreateRecord(InspectionBase):
    facility_id: int = Field(..., gt=0)
    inspector_name: str = Field(..., min_length=2, max_length=100)
    inspection_date: str = Field(..., description="YYYY-MM-DD")
    notes: Optional[str] = ""


class InspectionResponse(BaseModel):
    id: int
    facility_id: int
    facility_name: Optional[str] = None
    facility_type: Optional[str] = None
    license_number: Optional[str] = None
    inspector_name: str
    inspection_date: str
    inspection_type: str
    temperature_compliance_score: float
    sanitation_protocol_score: float
    water_potability_index: float
    ppe_handwashing_score: float
    pest_control_score: float
    food_handler_cert_ratio: float
    structural_maintenance_score: float
    waste_management_score: float
    cross_contamination_control: float
    historical_violation_count: int
    ambient_kitchen_temp: float
    relative_humidity: float
    predicted_risk_level: str
    predicted_risk_score: float
    hygiene_grade: str
    confidence_percentage: float
    recommendations: List[str] = []
    notes: Optional[str] = None
    created_at: Optional[str] = None

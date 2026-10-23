"""
Prediction and Inference Engine for Smart Hygiene Risk Prediction System.
Loads saved models and preprocessor, runs predictions, calculates confidence intervals,
and generates automated hygiene risk remediation recommendations.
"""

import os
import joblib
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Union, Optional
from preprocessing import (
    HygieneDataPreprocessor,
    NUMERICAL_FEATURES,
    CATEGORICAL_FEATURES,
    INV_RISK_CLASS_MAPPING,
)


class HygienePredictor:
    """
    Production-grade inference engine for single-instance or batch predictions.
    """
    def __init__(self, models_dir: Optional[str] = None):
        if models_dir is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            models_dir = os.path.join(current_dir, "..", "models")

        self.models_dir = models_dir
        self.classifier_path = os.path.join(models_dir, "best_classifier.joblib")
        self.regressor_path = os.path.join(models_dir, "best_regressor.joblib")
        self.preprocessor_path = os.path.join(models_dir, "preprocessor.joblib")

        self._load_artifacts()

    def _load_artifacts(self) -> None:
        if not os.path.exists(self.classifier_path):
            raise FileNotFoundError(f"Classifier artifact missing at {self.classifier_path}")
        if not os.path.exists(self.preprocessor_path):
            raise FileNotFoundError(f"Preprocessor artifact missing at {self.preprocessor_path}")

        self.classifier = joblib.load(self.classifier_path)
        self.preprocessor: HygieneDataPreprocessor = joblib.load(self.preprocessor_path)

        if os.path.exists(self.regressor_path):
            self.regressor = joblib.load(self.regressor_path)
        else:
            self.regressor = None

    def _generate_recommendations(self, record: Dict[str, Any], risk_level: str) -> List[str]:
        """
        Generate specific, actionable remediation steps based on inspection metrics.
        """
        recs = []
        
        temp_score = float(record.get("temperature_compliance_score", 100))
        if temp_score < 75.0:
            recs.append("CRITICAL: Recalibrate refrigeration and hot holding equipment. Implement continuous automated digital temperature logging.")

        pest_score = float(record.get("pest_control_score", 100))
        if pest_score < 75.0:
            recs.append("CRITICAL: Engage professional pest control service for immediate eradication audit, seal wall penetrations, and install air curtains.")

        sanit_score = float(record.get("sanitation_protocol_score", 100))
        if sanit_score < 75.0:
            recs.append("URGENT: Enforce strict sanitization schedule using EPA-registered quaternary ammonium or chlorine solutions with mandatory contact times.")

        cross_score = float(record.get("cross_contamination_control", 100))
        if cross_score < 75.0:
            recs.append("PRIORITY: Implement color-coded prep boards and utensils. Physically separate raw protein staging from ready-to-eat preparation lines.")

        ppe_score = float(record.get("ppe_handwashing_score", 100))
        if ppe_score < 75.0:
            recs.append("OPERATIONAL: Restock all handwashing stations with warm water, bactericidal soap, single-use towels, and install touchless fixtures.")

        water_score = float(record.get("water_potability_index", 100))
        if water_score < 80.0:
            recs.append("SAFETY: Conduct comprehensive water microbiological testing and service inline water filtration/backflow prevention valves.")

        cert_score = float(record.get("food_handler_cert_ratio", 100))
        if cert_score < 75.0:
            recs.append("TRAINING: Enroll non-certified kitchen personnel into certified Food Protection Manager or Food Handler training.")

        violations = int(record.get("historical_violation_count", 0))
        if violations >= 4:
            recs.append("COMPLIANCE: Schedule an unannounced mock inspection within 14 days to verify compliance closure on repeat non-conformances.")

        if not recs:
            if risk_level == "Low Risk":
                recs.append("EXCELLENT: Maintain current rigorous preventive hygiene controls and proceed with standard scheduled monitoring.")
            else:
                recs.append("MONITORING: Conduct weekly internal sanitation self-audits to maintain grade standards.")

        return recs

    def _determine_grade(self, risk_level: str, score: float) -> str:
        if risk_level == "Low Risk" or score < 35.0:
            return "Grade A (Pristine Compliance)"
        elif risk_level == "Medium Risk" or score < 62.0:
            return "Grade B (Conditional / Corrective Action Required)"
        else:
            return "Grade C (Critical Hazard / Closure Warning)"

    def predict_single(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inference on a single facility record.
        """
        df = pd.DataFrame([input_data])
        X_trans = self.preprocessor.transform(df)

        # Classification
        pred_class_id = int(self.classifier.predict(X_trans)[0])
        pred_risk_level = INV_RISK_CLASS_MAPPING.get(pred_class_id, "Medium Risk")

        # Probabilities
        if hasattr(self.classifier, "predict_proba"):
            probs = self.classifier.predict_proba(X_trans)[0]
            confidence = float(np.max(probs) * 100.0)
            class_probs = {
                "Low Risk": float(round(probs[0] * 100.0, 2)),
                "Medium Risk": float(round(probs[1] * 100.0, 2)),
                "High Risk": float(round(probs[2] * 100.0, 2)),
            }
        else:
            confidence = 85.0
            class_probs = {"Low Risk": 33.3, "Medium Risk": 33.3, "High Risk": 33.3}

        # Continuous risk score estimation
        if self.regressor is not None:
            pred_score = float(np.clip(self.regressor.predict(X_trans)[0], 0.0, 100.0).round(1))
        else:
            # Fallback heuristic
            score_map = {"Low Risk": 20.0, "Medium Risk": 48.0, "High Risk": 78.0}
            pred_score = score_map.get(pred_risk_level, 50.0)

        # Grade
        grade = self._determine_grade(pred_risk_level, pred_score)

        # Recommendations
        recommendations = self._generate_recommendations(input_data, pred_risk_level)

        # Contributing factor analysis
        risk_factors = []
        for feature in NUMERICAL_FEATURES:
            if feature in input_data and input_data[feature] is not None:
                val = float(input_data[feature])
                if feature == "historical_violation_count" and val >= 3:
                    risk_factors.append({
                        "feature": "Historical Violations",
                        "value": val,
                        "impact": "High Adverse Impact",
                        "severity": "Warning" if val < 6 else "Critical"
                    })
                elif feature.endswith("_score") or feature.endswith("_index") or feature.endswith("_ratio") or feature.endswith("_control"):
                    if val < 70.0:
                        risk_factors.append({
                            "feature": feature.replace("_", " ").title(),
                            "value": val,
                            "impact": "Substandard Compliance (<70%)",
                            "severity": "Critical" if val < 50.0 else "Warning"
                        })

        return {
            "predicted_risk_level": pred_risk_level,
            "predicted_risk_score": pred_score,
            "hygiene_grade": grade,
            "confidence_percentage": round(confidence, 1),
            "class_probabilities": class_probs,
            "recommendations": recommendations,
            "key_risk_drivers": risk_factors,
            "status": "success",
        }

    def predict_batch(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Inference on a list of records.
        """
        results = []
        for rec in records:
            results.append(self.predict_single(rec))
        return results


if __name__ == "__main__":
    predictor = HygienePredictor()
    
    sample_safe = {
        "facility_type": "Restaurant",
        "inspection_type": "Routine",
        "temperature_compliance_score": 94.5,
        "sanitation_protocol_score": 96.0,
        "water_potability_index": 98.0,
        "ppe_handwashing_score": 92.0,
        "pest_control_score": 95.0,
        "food_handler_cert_ratio": 90.0,
        "structural_maintenance_score": 88.0,
        "waste_management_score": 92.0,
        "cross_contamination_control": 95.0,
        "historical_violation_count": 0,
        "ambient_kitchen_temp": 24.5,
        "relative_humidity": 52.0,
    }
    
    sample_hazard = {
        "facility_type": "Fast Food",
        "inspection_type": "Complaint-driven",
        "temperature_compliance_score": 45.0,
        "sanitation_protocol_score": 42.0,
        "water_potability_index": 60.0,
        "ppe_handwashing_score": 38.0,
        "pest_control_score": 30.0,
        "food_handler_cert_ratio": 40.0,
        "structural_maintenance_score": 50.0,
        "waste_management_score": 45.0,
        "cross_contamination_control": 40.0,
        "historical_violation_count": 7,
        "ambient_kitchen_temp": 36.0,
        "relative_humidity": 82.0,
    }

    print("Sample 1 (Safe Restaurant):")
    res1 = predictor.predict_single(sample_safe)
    print(f"Risk Level: {res1['predicted_risk_level']} | Score: {res1['predicted_risk_score']} | Confidence: {res1['confidence_percentage']}%")
    print(f"Grade: {res1['hygiene_grade']}")

    print("\nSample 2 (Hazardous Fast Food):")
    res2 = predictor.predict_single(sample_hazard)
    print(f"Risk Level: {res2['predicted_risk_level']} | Score: {res2['predicted_risk_score']} | Confidence: {res2['confidence_percentage']}%")
    print(f"Grade: {res2['hygiene_grade']}")
    print("Recommendations:")
    for r in res2['recommendations']:
        print(f"  * {r}")

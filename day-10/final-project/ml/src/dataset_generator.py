"""
Dataset Generator for Smart Hygiene Risk Prediction System
Generates scientifically grounded synthetic food & facility hygiene inspection datasets
incorporating FDA/WHO food safety standards, non-linear risk interactions, and realistic correlations.
"""

import os
import numpy as np
import pandas as pd


def generate_hygiene_dataset(n_samples: int = 3500, random_seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic hygiene inspection records with realistic distributions
    and microbiological hazard interactions.
    """
    np.random.seed(random_seed)

    facility_types = [
        "Restaurant",
        "Fast Food",
        "Hospital Cafeteria",
        "Catering Service",
        "Supermarket Deli",
        "Bakery & Confectionery",
    ]
    facility_probs = [0.35, 0.22, 0.10, 0.13, 0.12, 0.08]

    inspection_types = ["Routine", "Follow-up", "Complaint-driven", "License Renewal"]
    inspection_probs = [0.60, 0.20, 0.12, 0.08]

    facilities = np.random.choice(facility_types, size=n_samples, p=facility_probs)
    inspections = np.random.choice(inspection_types, size=n_samples, p=inspection_probs)

    # Core operational compliance features (0 - 100 scale, higher is better)
    # Facility baseline quality factors
    facility_quality_baseline = {
        "Restaurant": 76.0,
        "Fast Food": 72.0,
        "Hospital Cafeteria": 88.0,
        "Catering Service": 74.0,
        "Supermarket Deli": 79.0,
        "Bakery & Confectionery": 81.0,
    }

    base_scores = np.array([facility_quality_baseline[f] for f in facilities])
    # Add random operational variation
    op_noise = np.random.normal(0, 12, size=n_samples)
    latent_quality = np.clip(base_scores + op_noise, 20.0, 99.0)

    # Generate correlated hygiene components
    temperature_compliance = np.clip(
        latent_quality * 0.95 + np.random.normal(0, 8, size=n_samples), 10.0, 100.0
    ).round(1)

    sanitation_protocol = np.clip(
        latent_quality * 0.98 + np.random.normal(0, 7, size=n_samples), 15.0, 100.0
    ).round(1)

    water_potability = np.clip(
        latent_quality * 0.85 + np.random.normal(10, 6, size=n_samples), 30.0, 100.0
    ).round(1)

    ppe_handwashing = np.clip(
        latent_quality * 0.92 + np.random.normal(0, 9, size=n_samples), 10.0, 100.0
    ).round(1)

    pest_control = np.clip(
        latent_quality * 0.90 + np.random.normal(5, 10, size=n_samples), 10.0, 100.0
    ).round(1)

    food_handler_cert = np.clip(
        latent_quality * 0.88 + np.random.normal(5, 11, size=n_samples), 15.0, 100.0
    ).round(1)

    structural_maintenance = np.clip(
        latent_quality * 0.91 + np.random.normal(2, 8, size=n_samples), 20.0, 100.0
    ).round(1)

    waste_management = np.clip(
        latent_quality * 0.94 + np.random.normal(0, 8, size=n_samples), 20.0, 100.0
    ).round(1)

    cross_contamination_control = np.clip(
        latent_quality * 0.93 + np.random.normal(0, 8, size=n_samples), 15.0, 100.0
    ).round(1)

    # Historical violations inversely correlated with latent quality
    historical_violations = np.clip(
        np.round((100.0 - latent_quality) / 10.0 + np.random.exponential(1.2, size=n_samples)),
        0,
        15,
    ).astype(int)

    # Environmental indicators
    ambient_kitchen_temp = np.clip(
        np.random.normal(27.5, 4.5, size=n_samples) + (100.0 - structural_maintenance) * 0.05,
        18.0,
        44.0,
    ).round(1)

    relative_humidity = np.clip(
        np.random.normal(58.0, 12.0, size=n_samples) + (100.0 - structural_maintenance) * 0.08,
        30.0,
        95.0,
    ).round(1)

    # Non-linear hazard synthesis:
    # Critical hazard multipliers:
    # severe failure in temperature or pest control multiplies danger significantly
    temp_deficit = np.maximum(0, 70.0 - temperature_compliance)
    pest_deficit = np.maximum(0, 65.0 - pest_control)
    sanitation_deficit = np.maximum(0, 70.0 - sanitation_protocol)
    cross_contam_deficit = np.maximum(0, 65.0 - cross_contamination_control)

    # Weighted hazard calculation
    base_hazard = (
        (100.0 - temperature_compliance) * 0.18
        + (100.0 - sanitation_protocol) * 0.18
        + (100.0 - pest_control) * 0.16
        + (100.0 - cross_contamination_control) * 0.14
        + (100.0 - ppe_handwashing) * 0.10
        + (100.0 - water_potability) * 0.08
        + (100.0 - waste_management) * 0.06
        + (100.0 - structural_maintenance) * 0.05
        + (100.0 - food_handler_cert) * 0.05
        + (historical_violations * 2.2)
        + np.maximum(0, ambient_kitchen_temp - 30.0) * 0.8
        + np.maximum(0, relative_humidity - 70.0) * 0.3
    )

    # Non-linear critical penalties for hazardous failures
    penalty = (temp_deficit ** 1.35) * 0.15 + (pest_deficit ** 1.35) * 0.18 + (sanitation_deficit ** 1.25) * 0.12

    computed_risk_score = np.clip(base_hazard + penalty + np.random.normal(0, 3.5, size=n_samples), 0.0, 100.0).round(1)

    # Multi-class target categorization
    # Low Risk: score < 35.0 (Pristine / Grade A)
    # Medium Risk: 35.0 <= score < 62.0 (Needs Correction / Grade B)
    # High Risk: score >= 62.0 (Critical Hazard / Grade C)
    risk_level = []
    for score in computed_risk_score:
        if score < 35.0:
            risk_level.append("Low Risk")
        elif score < 62.0:
            risk_level.append("Medium Risk")
        else:
            risk_level.append("High Risk")

    df = pd.DataFrame({
        "facility_type": facilities,
        "inspection_type": inspections,
        "temperature_compliance_score": temperature_compliance,
        "sanitation_protocol_score": sanitation_protocol,
        "water_potability_index": water_potability,
        "ppe_handwashing_score": ppe_handwashing,
        "pest_control_score": pest_control,
        "food_handler_cert_ratio": food_handler_cert,
        "structural_maintenance_score": structural_maintenance,
        "waste_management_score": waste_management,
        "cross_contamination_control": cross_contamination_control,
        "historical_violation_count": historical_violations,
        "ambient_kitchen_temp": ambient_kitchen_temp,
        "relative_humidity": relative_humidity,
        "hygiene_risk_score": computed_risk_score,
        "hygiene_risk_level": risk_level,
    })

    # Introduce realistic subtle missing values (approx 1.5% in optional fields) to test preprocessing
    mask_cert = np.random.rand(n_samples) < 0.02
    df.loc[mask_cert, "food_handler_cert_ratio"] = np.nan

    mask_temp = np.random.rand(n_samples) < 0.015
    df.loc[mask_temp, "ambient_kitchen_temp"] = np.nan

    mask_hum = np.random.rand(n_samples) < 0.015
    df.loc[mask_hum, "relative_humidity"] = np.nan

    return df


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(current_dir, "..", "data")
    os.makedirs(output_dir, exist_ok=True)

    csv_path = os.path.join(output_dir, "hygiene_inspections.csv")
    print(f"Generating realistic hygiene risk dataset...")
    data = generate_hygiene_dataset(n_samples=3500)
    data.to_csv(csv_path, index=False)
    print(f"Dataset successfully created: {csv_path}")
    print(f"Shape: {data.shape}")
    print(f"Target distribution:\n{data['hygiene_risk_level'].value_counts(normalize=True).round(3)}")

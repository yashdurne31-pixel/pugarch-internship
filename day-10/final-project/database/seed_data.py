"""
Seed script to populate initial facilities, inspection logs, and remediation items.
Leverages the trained ML predictor to ensure authentic predictions and recommendations.
"""

import os
import sys

# Ensure ml and database modules are resolvable
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, "..")
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, "ml", "src"))

from database.db import initialize_database
from database.repository import HygieneRepository
from predict import HygienePredictor


FACILITIES_SEED = [
    {
        "name": "The Grand Royal Bistro",
        "facility_type": "Restaurant",
        "license_number": "LIC-REST-2024-001",
        "address": "42 Heritage Avenue, Downtown Sector",
        "contact_email": "manager@grandroyalbistro.com",
        "contact_phone": "+1 (555) 234-5678",
    },
    {
        "name": "St. Jude Hospital Central Cafeteria",
        "facility_type": "Hospital Cafeteria",
        "license_number": "LIC-HOSP-2023-882",
        "address": "700 Medical Center Blvd, Wing B",
        "contact_email": "dietary@stjudehospital.org",
        "contact_phone": "+1 (555) 890-1234",
    },
    {
        "name": "Golden Crust Artisan Bakery",
        "facility_type": "Bakery & Confectionery",
        "license_number": "LIC-BAKE-2024-114",
        "address": "15 Baker Street, Old Quarter",
        "contact_email": "orders@goldencrust.io",
        "contact_phone": "+1 (555) 345-6789",
    },
    {
        "name": "Express Burger & Fries Co.",
        "facility_type": "Fast Food",
        "license_number": "LIC-FAST-2024-909",
        "address": "108 Highway Expressway Mall",
        "contact_email": "gm.highway@expressburger.com",
        "contact_phone": "+1 (555) 456-7890",
    },
    {
        "name": "Ocean Harvest Supermarket Deli",
        "facility_type": "Supermarket Deli",
        "license_number": "LIC-DELI-2023-455",
        "address": "890 Coastal Parkway Plaza",
        "contact_email": "deli.dept@oceanharvest.com",
        "contact_phone": "+1 (555) 567-8901",
    },
    {
        "name": "Metropolitan Premier Catering",
        "facility_type": "Catering Service",
        "license_number": "LIC-CATR-2024-320",
        "address": "55 Industrial Park Road, Unit 4",
        "contact_email": "kitchen@metrocatering.com",
        "contact_phone": "+1 (555) 678-9012",
    },
    {
        "name": "Szechuan Spice Pavilion",
        "facility_type": "Restaurant",
        "license_number": "LIC-REST-2023-551",
        "address": "22 Dragon Gate Plaza",
        "contact_email": "info@spicepavilion.com",
        "contact_phone": "+1 (555) 789-0123",
    },
    {
        "name": "City General Pediatric Nutrition Kitchen",
        "facility_type": "Hospital Cafeteria",
        "license_number": "LIC-HOSP-2024-019",
        "address": "330 Health Sciences Way",
        "contact_email": "clinicalnutrition@citygen.org",
        "contact_phone": "+1 (555) 901-2345",
    },
]

INSPECTION_SCENARIOS = [
    # Facility 1: Grand Royal (Excellent)
    {
        "facility_idx": 0,
        "inspector_name": "Inspector Sarah Jenkins (Lead)",
        "inspection_date": "2026-10-14",
        "inspection_type": "Routine",
        "temperature_compliance_score": 96.0,
        "sanitation_protocol_score": 94.5,
        "water_potability_index": 98.0,
        "ppe_handwashing_score": 93.0,
        "pest_control_score": 95.0,
        "food_handler_cert_ratio": 95.0,
        "structural_maintenance_score": 90.0,
        "waste_management_score": 92.0,
        "cross_contamination_control": 96.0,
        "historical_violation_count": 0,
        "ambient_kitchen_temp": 24.0,
        "relative_humidity": 50.0,
        "notes": "Impeccable cold chain tracking and pristine sanitation documentation.",
    },
    # Facility 2: St Jude Hospital (Exceptional)
    {
        "facility_idx": 1,
        "inspector_name": "Dr. Marcus Vance (Sanitary Officer)",
        "inspection_date": "2026-10-18",
        "inspection_type": "Routine",
        "temperature_compliance_score": 99.0,
        "sanitation_protocol_score": 98.0,
        "water_potability_index": 100.0,
        "ppe_handwashing_score": 99.0,
        "pest_control_score": 100.0,
        "food_handler_cert_ratio": 100.0,
        "structural_maintenance_score": 96.0,
        "waste_management_score": 98.0,
        "cross_contamination_control": 100.0,
        "historical_violation_count": 0,
        "ambient_kitchen_temp": 22.0,
        "relative_humidity": 45.0,
        "notes": "Exemplary healthcare facility hygiene conforming to ISO 22000 standards.",
    },
    # Facility 3: Golden Crust Bakery (Moderate Warning)
    {
        "facility_idx": 2,
        "inspector_name": "Inspector Robert Lee",
        "inspection_date": "2026-10-10",
        "inspection_type": "Routine",
        "temperature_compliance_score": 78.0,
        "sanitation_protocol_score": 72.0,
        "water_potability_index": 88.0,
        "ppe_handwashing_score": 70.0,
        "pest_control_score": 68.0,
        "food_handler_cert_ratio": 75.0,
        "structural_maintenance_score": 74.0,
        "waste_management_score": 78.0,
        "cross_contamination_control": 72.0,
        "historical_violation_count": 2,
        "ambient_kitchen_temp": 29.5,
        "relative_humidity": 68.0,
        "notes": "Flour dust accumulation near exhaust ducts; pest exclusion screen needs repair.",
    },
    # Facility 4: Express Burger (Critical Hazard)
    {
        "facility_idx": 3,
        "inspector_name": "Inspector Elena Rostova",
        "inspection_date": "2026-10-21",
        "inspection_type": "Complaint-driven",
        "temperature_compliance_score": 38.0,
        "sanitation_protocol_score": 35.0,
        "water_potability_index": 62.0,
        "ppe_handwashing_score": 32.0,
        "pest_control_score": 28.0,
        "food_handler_cert_ratio": 35.0,
        "structural_maintenance_score": 42.0,
        "waste_management_score": 36.0,
        "cross_contamination_control": 34.0,
        "historical_violation_count": 8,
        "ambient_kitchen_temp": 37.5,
        "relative_humidity": 85.0,
        "notes": "Critical cold-table breakdown (14°C raw beef patty staging), rodent droppings noted.",
    },
    # Facility 5: Ocean Harvest Supermarket Deli (Moderate)
    {
        "facility_idx": 4,
        "inspector_name": "Inspector Sarah Jenkins",
        "inspection_date": "2026-09-28",
        "inspection_type": "Follow-up",
        "temperature_compliance_score": 82.0,
        "sanitation_protocol_score": 80.0,
        "water_potability_index": 92.0,
        "ppe_handwashing_score": 84.0,
        "pest_control_score": 82.0,
        "food_handler_cert_ratio": 80.0,
        "structural_maintenance_score": 85.0,
        "waste_management_score": 86.0,
        "cross_contamination_control": 82.0,
        "historical_violation_count": 1,
        "ambient_kitchen_temp": 23.5,
        "relative_humidity": 55.0,
        "notes": "Follow-up inspection shows improvement from previous notice; deli slicer sanitized.",
    },
    # Facility 6: Metro Catering (Good)
    {
        "facility_idx": 5,
        "inspector_name": "Inspector Robert Lee",
        "inspection_date": "2026-10-05",
        "inspection_type": "Routine",
        "temperature_compliance_score": 89.0,
        "sanitation_protocol_score": 88.0,
        "water_potability_index": 94.0,
        "ppe_handwashing_score": 87.0,
        "pest_control_score": 90.0,
        "food_handler_cert_ratio": 88.0,
        "structural_maintenance_score": 86.0,
        "waste_management_score": 88.0,
        "cross_contamination_control": 89.0,
        "historical_violation_count": 0,
        "ambient_kitchen_temp": 25.0,
        "relative_humidity": 58.0,
        "notes": "Commercial transport hot-boxes and blast chillers verified in optimal order.",
    },
    # Facility 7: Szechuan Spice (Warning)
    {
        "facility_idx": 6,
        "inspector_name": "Inspector Elena Rostova",
        "inspection_date": "2026-10-15",
        "inspection_type": "Routine",
        "temperature_compliance_score": 68.0,
        "sanitation_protocol_score": 65.0,
        "water_potability_index": 82.0,
        "ppe_handwashing_score": 64.0,
        "pest_control_score": 62.0,
        "food_handler_cert_ratio": 60.0,
        "structural_maintenance_score": 66.0,
        "waste_management_score": 64.0,
        "cross_contamination_control": 62.0,
        "historical_violation_count": 4,
        "ambient_kitchen_temp": 32.5,
        "relative_humidity": 72.0,
        "notes": "Wok station grease accumulation on hoods; meat thawing at ambient room temperature.",
    },
]


def seed_all():
    print("Initializing Database...")
    initialize_database()

    repo = HygieneRepository()
    predictor = HygienePredictor()

    print("Seeding Facilities...")
    facility_ids = []
    for fac in FACILITIES_SEED:
        f_id = repo.create_facility(fac)
        facility_ids.append(f_id)
        print(f"  [+] Facility created: {fac['name']} (ID: {f_id})")

    print("\nRunning ML Predictions and Seeding Historical Inspections...")
    for scn in INSPECTION_SCENARIOS:
        f_idx = scn["facility_idx"]
        fac_id = facility_ids[f_idx]
        fac_obj = FACILITIES_SEED[f_idx]

        # Prepare payload for predictor
        ml_input = {
            "facility_type": fac_obj["facility_type"],
            "inspection_type": scn["inspection_type"],
            "temperature_compliance_score": scn["temperature_compliance_score"],
            "sanitation_protocol_score": scn["sanitation_protocol_score"],
            "water_potability_index": scn["water_potability_index"],
            "ppe_handwashing_score": scn["ppe_handwashing_score"],
            "pest_control_score": scn["pest_control_score"],
            "food_handler_cert_ratio": scn["food_handler_cert_ratio"],
            "structural_maintenance_score": scn["structural_maintenance_score"],
            "waste_management_score": scn["waste_management_score"],
            "cross_contamination_control": scn["cross_contamination_control"],
            "historical_violation_count": scn["historical_violation_count"],
            "ambient_kitchen_temp": scn["ambient_kitchen_temp"],
            "relative_humidity": scn["relative_humidity"],
        }

        # Run ML Inference
        pred_res = predictor.predict_single(ml_input)

        # Build DB Record
        db_record = {
            "facility_id": fac_id,
            "inspector_name": scn["inspector_name"],
            "inspection_date": scn["inspection_date"],
            "inspection_type": scn["inspection_type"],
            **ml_input,
            "predicted_risk_level": pred_res["predicted_risk_level"],
            "predicted_risk_score": pred_res["predicted_risk_score"],
            "hygiene_grade": pred_res["hygiene_grade"],
            "confidence_percentage": pred_res["confidence_percentage"],
            "recommendations": pred_res["recommendations"],
            "notes": scn["notes"],
        }

        insp_id = repo.create_inspection(db_record)
        print(
            f"  [+] Inspection #{insp_id} -> {fac_obj['name']} | "
            f"Risk: {pred_res['predicted_risk_level']} (Score: {pred_res['predicted_risk_score']}) | "
            f"Grade: {pred_res['hygiene_grade']}"
        )

    stats = repo.get_system_stats()
    print("\nDatabase Seeding Successfully Completed!")
    print(f"Stats: {stats}")


if __name__ == "__main__":
    seed_all()

"""
Data generation script for the Smart Hygiene Risk Prediction System.

This script generates a SYNTHETIC dataset that simulates facility hygiene
inspection records. The data are entirely fabricated for educational purposes.

IMPORTANT DISCLAIMER
--------------------
- The dataset is synthetic: no real facilities, locations, or inspections are
  represented.
- The target variable `hygiene_risk` is rule-generated, not independently
  verified by public-health authorities.
- A model trained on this dataset learns to approximate the labeling rule,
  NOT to predict real-world hygiene outcomes.
- Do NOT use predictions from this system as official safety certifications.

Labeling Rule (transparent, documented)
----------------------------------------
A composite risk score is computed from:
    risk_score = (100 - cleanliness_score) * 0.40
              + odor_score            * 1.50
              + waste_num             * 5.00   # 0=Low,1=Med,2=High
              + (1 - water_num) * 10.00        # 1=Yes,0=No
              + complaints         * 1.20
              + footfall           * 0.02

Thresholds (tuned so classes are roughly balanced):
    risk_score < 40  → Low
    40 ≤ risk_score < 70  → Medium
    risk_score ≥ 70  → High

Usage
-----
    python data/generate_data.py
"""

import os
import numpy as np
import pandas as pd

# ── reproducibility ──────────────────────────────────────────────────────────
RANDOM_SEED = 42
rng = np.random.default_rng(RANDOM_SEED)

# ── config ───────────────────────────────────────────────────────────────────
N_RECORDS = 1_000
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "hygiene_inspections.csv")

LOCATIONS = [
    "Zone A - North", "Zone B - South", "Zone C - East",
    "Zone D - West", "Zone E - Central",
]

WASTE_LEVELS = ["Low", "Medium", "High"]
WATER_OPTIONS = ["Yes", "No"]


def generate_dataset(n: int = N_RECORDS) -> pd.DataFrame:
    """
    Generate a synthetic hygiene inspection dataset.

    Parameters
    ----------
    n : int
        Number of records to generate.

    Returns
    -------
    pd.DataFrame
        Synthetic dataset with all required columns.
    """
    facility_ids = [f"FAC{str(i).zfill(4)}" for i in range(1, n + 1)]

    locations = rng.choice(LOCATIONS, size=n)
    cleanliness_score = rng.integers(5, 101, size=n).astype(float)  # 5–100
    odor_score = rng.integers(0, 11, size=n).astype(float)          # 0–10
    waste_level = rng.choice(WASTE_LEVELS, size=n, p=[0.40, 0.35, 0.25])
    water_availability = rng.choice(WATER_OPTIONS, size=n, p=[0.75, 0.25])
    footfall = rng.integers(50, 501, size=n).astype(float)          # 50–500
    complaints = rng.integers(0, 21, size=n).astype(float)           # 0–20

    # inspection_date: last 2 years
    start_date = np.datetime64("2023-01-01")
    days_offset = rng.integers(0, 730, size=n)
    inspection_dates = [
        str((start_date + np.timedelta64(int(d), "D")).astype("datetime64[D]"))
        for d in days_offset
    ]

    # Introduce ~3 % missing values in numeric cols (realistic noise)
    for arr in [cleanliness_score, odor_score, footfall, complaints]:
        miss_idx = rng.choice(n, size=int(n * 0.03), replace=False)
        arr[miss_idx] = np.nan

    # ── rule-generated target ─────────────────────────────────────────────
    waste_map = {"Low": 0, "Medium": 1, "High": 2}
    water_map = {"Yes": 1, "No": 0}

    waste_num = np.array([waste_map[w] for w in waste_level], dtype=float)
    water_num = np.array([water_map[w] for w in water_availability], dtype=float)

    # Use median-filled values for score (NaN-safe)
    cs_filled = np.where(np.isnan(cleanliness_score), np.nanmedian(cleanliness_score), cleanliness_score)
    os_filled = np.where(np.isnan(odor_score), np.nanmedian(odor_score), odor_score)
    ft_filled = np.where(np.isnan(footfall), np.nanmedian(footfall), footfall)
    cp_filled = np.where(np.isnan(complaints), np.nanmedian(complaints), complaints)

    risk_score = (
        (100 - cs_filled) * 0.40
        + os_filled         * 1.50
        + waste_num         * 5.00
        + (1 - water_num)   * 10.00
        + cp_filled         * 1.20
        + ft_filled         * 0.02
    )

    # Add small noise to avoid perfectly deterministic labels
    risk_score += rng.normal(0, 2.0, size=n)

    hygiene_risk = np.where(
        risk_score < 40, "Low",
        np.where(risk_score < 70, "Medium", "High")
    )

    df = pd.DataFrame({
        "facility_id":       facility_ids,
        "location":          locations,
        "cleanliness_score": cleanliness_score,
        "odor_score":        odor_score,
        "waste_level":       waste_level,
        "water_availability": water_availability,
        "footfall":          footfall,
        "complaints":        complaints,
        "inspection_date":   inspection_dates,
        "hygiene_risk":      hygiene_risk,
    })

    return df


def main():
    print("=" * 60)
    print("  Smart Hygiene Risk Prediction System")
    print("  Synthetic Dataset Generator")
    print("=" * 60)
    print(f"\n[INFO] Random seed : {RANDOM_SEED}")
    print(f"[INFO] Records     : {N_RECORDS}")
    print(f"[INFO] Output path : {OUTPUT_PATH}\n")

    df = generate_dataset(N_RECORDS)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"[OK] Dataset saved  : {OUTPUT_PATH}")
    print(f"     Shape          : {df.shape}")
    print(f"     Columns        : {list(df.columns)}")
    print("\nRisk distribution (rule-generated labels):")
    print(df["hygiene_risk"].value_counts().to_string())
    print("\n[DISCLAIMER] This dataset is entirely synthetic.")
    print("             Target labels are rule-generated, not verified.")


if __name__ == "__main__":
    main()

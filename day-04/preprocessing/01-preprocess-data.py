from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "dataset"

INPUT_FILE = DATASET_DIR / "facility_hygiene_risk.csv"
OUTPUT_FILE = DATASET_DIR / "preprocessed_facility_data.csv"


def preprocess_data():
    df = pd.read_csv(INPUT_FILE)

    print("Original dataset shape:", df.shape)

    df = df.drop_duplicates().copy()

    numeric_columns = [
        "cleanliness_score",
        "odor_score",
        "complaints",
        "footfall",
        "hours_since_cleaning",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")
        df[column] = df[column].fillna(df[column].median())

    df["waste_level"] = df["waste_level"].fillna(
        df["waste_level"].mode()[0]
    )

    df["hygiene_risk"] = df["hygiene_risk"].fillna(
        df["hygiene_risk"].mode()[0]
    )

    df["waste_level"] = df["waste_level"].map({
        "Low": 0,
        "Medium": 1,
        "High": 2,
    })

    df["hygiene_risk"] = df["hygiene_risk"].map({
        "Low": 0,
        "High": 1,
    })

    df = df.dropna()

    df.to_csv(OUTPUT_FILE, index=False)

    print("Preprocessing completed successfully.")
    print("Processed dataset shape:", df.shape)
    print("Saved file:", OUTPUT_FILE)


if __name__ == "__main__":
    preprocess_data()
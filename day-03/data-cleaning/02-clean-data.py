import pandas as pd


INPUT_FILE = "../dataset/facility_data.csv"
OUTPUT_FILE = "../dataset/cleaned_facility_data.csv"


df = pd.read_csv(INPUT_FILE)

df["inspection_date"] = pd.to_datetime(df["inspection_date"])

df = df.drop_duplicates()

numeric_columns = [
    "cleanliness_score",
    "odor_score",
    "footfall",
    "complaints"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

df["cleanliness_score"] = df["cleanliness_score"].fillna(
    df["cleanliness_score"].median()
)

df["odor_score"] = df["odor_score"].fillna(
    df["odor_score"].median()
)

df["footfall"] = df["footfall"].fillna(
    df["footfall"].median()
)

df["complaints"] = df["complaints"].fillna(
    df["complaints"].median()
)

df = df[
    (df["cleanliness_score"].between(0, 100)) &
    (df["odor_score"].between(1, 10)) &
    (df["footfall"] >= 0) &
    (df["complaints"] >= 0)
]

df.to_csv(OUTPUT_FILE, index=False)

print("Data cleaning completed.")
print(f"Records after cleaning: {len(df)}")
print(f"Missing values: {df.isnull().sum().sum()}")
print(f"Duplicate records: {df.duplicated().sum()}")
print(f"Saved to: {OUTPUT_FILE}")
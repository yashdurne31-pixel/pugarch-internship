import pandas as pd


FILE_NAME = "../dataset/cleaned_facility_data.csv"


df = pd.read_csv(FILE_NAME)

print("Overall Statistics")
print(f"Average Cleanliness Score: {df['cleanliness_score'].mean():.2f}")
print(f"Average Odor Score: {df['odor_score'].mean():.2f}")
print(f"Average Footfall: {df['footfall'].mean():.2f}")
print(f"Average Complaints: {df['complaints'].mean():.2f}")

print("\nLocation-wise Cleanliness")
print(
    df.groupby("location")["cleanliness_score"]
    .mean()
    .sort_values(ascending=False)
)

print("\nLocation-wise Complaints")
print(
    df.groupby("location")["complaints"]
    .sum()
    .sort_values(ascending=False)
)

print("\nWater Availability")
print(df["water_availability"].value_counts())

print("\nWaste Level")
print(df["waste_level"].value_counts())

print("\nHighest Cleanliness Facilities")
print(
    df.nlargest(5, "cleanliness_score")[
        ["facility_id", "location", "cleanliness_score"]
    ]
)

print("\nHighest Complaint Facilities")
print(
    df.nlargest(5, "complaints")[
        ["facility_id", "location", "complaints"]
    ]
)
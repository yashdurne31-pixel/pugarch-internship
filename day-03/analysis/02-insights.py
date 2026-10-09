import pandas as pd


FILE_NAME = "../dataset/cleaned_facility_data.csv"


df = pd.read_csv(FILE_NAME)

location_cleanliness = (
    df.groupby("location")["cleanliness_score"]
    .mean()
    .sort_values(ascending=False)
)

location_complaints = (
    df.groupby("location")["complaints"]
    .sum()
    .sort_values(ascending=False)
)

highest_cleanliness_location = location_cleanliness.index[0]
lowest_cleanliness_location = location_cleanliness.index[-1]
highest_complaint_location = location_complaints.index[0]
lowest_complaint_location = location_complaints.index[-1]

print("Key Insights")
print("=" * 40)

print(
    f"1. {highest_cleanliness_location} has the highest "
    f"average cleanliness score of "
    f"{location_cleanliness.iloc[0]:.2f}."
)

print(
    f"2. {lowest_cleanliness_location} has the lowest "
    f"average cleanliness score of "
    f"{location_cleanliness.iloc[-1]:.2f}."
)

print(
    f"3. {highest_complaint_location} has the highest "
    f"total number of complaints: "
    f"{location_complaints.iloc[0]}."
)

print(
    f"4. {lowest_complaint_location} has the lowest "
    f"total number of complaints: "
    f"{location_complaints.iloc[-1]}."
)

print(
    f"5. The overall average cleanliness score is "
    f"{df['cleanliness_score'].mean():.2f}."
)
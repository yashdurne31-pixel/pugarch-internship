import pandas as pd
import matplotlib.pyplot as plt


FILE_NAME = "../dataset/cleaned_facility_data.csv"


df = pd.read_csv(FILE_NAME)

location_complaints = (
    df.groupby("location")["complaints"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(8, 5))

location_complaints.plot(kind="bar")

plt.title("Total Complaints by Location")
plt.xlabel("Location")
plt.ylabel("Total Complaints")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("complaints-by-location.png")
plt.show()
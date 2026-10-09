import pandas as pd
import matplotlib.pyplot as plt


FILE_NAME = "../dataset/cleaned_facility_data.csv"


df = pd.read_csv(FILE_NAME)

location_cleanliness = (
    df.groupby("location")["cleanliness_score"]
    .mean()
    .sort_values(ascending=False)
)

plt.figure(figsize=(8, 5))

location_cleanliness.plot(kind="bar")

plt.title("Average Cleanliness Score by Location")
plt.xlabel("Location")
plt.ylabel("Average Cleanliness Score")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("cleanliness-by-location.png")
plt.show()
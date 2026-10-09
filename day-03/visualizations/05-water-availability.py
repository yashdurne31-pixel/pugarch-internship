import pandas as pd
import matplotlib.pyplot as plt


FILE_NAME = "../dataset/cleaned_facility_data.csv"


df = pd.read_csv(FILE_NAME)

water_data = df["water_availability"].value_counts()

plt.figure(figsize=(7, 7))

plt.pie(
    water_data.values,
    labels=water_data.index,
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Water Availability Across Facilities")
plt.tight_layout()

plt.savefig("water-availability.png")
plt.show()
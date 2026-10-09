import pandas as pd
import matplotlib.pyplot as plt


FILE_NAME = "../dataset/cleaned_facility_data.csv"


df = pd.read_csv(FILE_NAME)

plt.figure(figsize=(8, 5))

plt.hist(
    df["cleanliness_score"],
    bins=5,
    edgecolor="black"
)

plt.title("Distribution of Cleanliness Scores")
plt.xlabel("Cleanliness Score")
plt.ylabel("Number of Facilities")
plt.tight_layout()

plt.savefig("cleanliness-histogram.png")
plt.show()
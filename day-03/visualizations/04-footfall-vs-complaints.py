import pandas as pd
import matplotlib.pyplot as plt


FILE_NAME = "../dataset/cleaned_facility_data.csv"


df = pd.read_csv(FILE_NAME)

plt.figure(figsize=(8, 5))

plt.scatter(
    df["footfall"],
    df["complaints"]
)

plt.title("Footfall vs Complaints")
plt.xlabel("Footfall")
plt.ylabel("Complaints")
plt.tight_layout()

plt.savefig("footfall-vs-complaints.png")
plt.show()
import pandas as pd


data = {
    "facility": ["F001", "F002", "F003", "F004", "F005", "F006"],
    "location": ["Amravati", "Nagpur", "Nagpur", "Akola", "Amravati", "Wardha"],
    "cleanliness_score": [85, 72, 91, 64, 78, 88],
    "complaints": [4, 8, 2, 12, 6, 3]
}


df = pd.DataFrame(data)

print("Cleanliness Score Above 80:")
print(df[df["cleanliness_score"] > 80])

print("\nSorted by Cleanliness Score:")
print(df.sort_values("cleanliness_score", ascending=False))

print("\nAverage Cleanliness by Location:")
print(df.groupby("location")["cleanliness_score"].mean())

print("\nTotal Complaints by Location:")
print(df.groupby("location")["complaints"].sum())
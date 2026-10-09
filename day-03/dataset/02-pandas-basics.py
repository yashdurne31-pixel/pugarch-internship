import pandas as pd


data = {
    "facility": ["F001", "F002", "F003", "F004", "F005"],
    "location": ["Amravati", "Nagpur", "Wardha", "Akola", "Yavatmal"],
    "cleanliness_score": [85, 72, 91, 64, 78],
    "complaints": [4, 8, 2, 12, 6]
}


df = pd.DataFrame(data)

print("DataFrame:")
print(df)

print("\nShape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst Three Records:")
print(df.head(3))

print("\nCleanliness Average:", df["cleanliness_score"].mean())

print("\nHighest Cleanliness Score:")
print(df["cleanliness_score"].max())

print("\nLowest Cleanliness Score:")
print(df["cleanliness_score"].min())
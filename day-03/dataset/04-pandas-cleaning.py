import pandas as pd


data = {
    "facility": ["F001", "F002", "F003", "F004", "F005", "F005"],
    "location": ["Amravati", "Nagpur", "Nagpur", "Akola", "Wardha", "Wardha"],
    "cleanliness_score": [85, 72, None, 64, 78, 78],
    "complaints": [4, 8, 2, None, 6, 6]
}


df = pd.DataFrame(data)

print("Original Data:")
print(df)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records:")
print(df.duplicated().sum())

df["cleanliness_score"] = df["cleanliness_score"].fillna(
    df["cleanliness_score"].mean()
)

df["complaints"] = df["complaints"].fillna(
    df["complaints"].median()
)

df = df.drop_duplicates()

print("\nCleaned Data:")
print(df)

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

print("\nDuplicate Records After Cleaning:")
print(df.duplicated().sum())
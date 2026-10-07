import csv
from collections import Counter


FILE_NAME = "employees.csv"


def load_data():
    with open(FILE_NAME, "r", newline="") as file:
        return list(csv.DictReader(file))


def analyze_data(data):
    print(f"Record Count: {len(data)}")

    missing_values = {
        field: sum(not row[field].strip() for row in data)
        for field in data[0]
    }

    print("\nMissing Values:")
    for field, count in missing_values.items():
        print(f"{field}: {count}")

    records = [tuple(row.items()) for row in data]
    duplicate_count = len(records) - len(set(records))

    print(f"\nDuplicate Records: {duplicate_count}")

    salaries = [
        float(row["salary"])
        for row in data
        if row["salary"].strip()
    ]

    print(f"\nAverage Salary: {sum(salaries) / len(salaries):.2f}")
    print(f"Minimum Salary: {min(salaries):.2f}")
    print(f"Maximum Salary: {max(salaries):.2f}")

    departments = Counter(row["department"] for row in data)

    print("\nCategory-wise Statistics:")
    for department, count in departments.items():
        print(f"{department}: {count}")


def main():
    try:
        data = load_data()

        if not data:
            print("CSV file is empty.")
            return

        analyze_data(data)

    except FileNotFoundError:
        print("CSV file not found.")
    except (ValueError, KeyError) as error:
        print(f"Data error: {error}")


if __name__ == "__main__":
    main()
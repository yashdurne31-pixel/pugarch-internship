import json

FILE_NAME = "employees.json"


def load_employees():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Invalid data file.")
        return []


def save_employees(employees):
    with open(FILE_NAME, "w") as file:
        json.dump(employees, file, indent=4)


def get_next_id(employees):
    if not employees:
        return 1

    return max(employee["id"] for employee in employees) + 1


def add_employee(employees):
    try:
        name = input("Enter name: ").strip()
        salary = float(input("Enter salary: "))
        department = input("Enter department: ").strip()

        if not name or not department:
            raise ValueError("Name and department cannot be empty.")

        employee = {
            "id": get_next_id(employees),
            "name": name,
            "salary": salary,
            "department": department
        }

        employees.append(employee)
        save_employees(employees)

        print("Employee added successfully.")

    except ValueError as error:
        print(f"Error: {error}")


def update_employee(employees):
    try:
        employee_id = int(input("Enter employee ID: "))

        employee = next(
            (employee for employee in employees if employee["id"] == employee_id),
            None
        )

        if employee is None:
            print("Employee not found.")
            return

        name = input("Enter new name: ").strip()
        salary = float(input("Enter new salary: "))
        department = input("Enter new department: ").strip()

        if not name or not department:
            raise ValueError("Name and department cannot be empty.")

        employee["name"] = name
        employee["salary"] = salary
        employee["department"] = department

        save_employees(employees)

        print("Employee updated successfully.")

    except ValueError as error:
        print(f"Error: {error}")


def delete_employee(employees):
    try:
        employee_id = int(input("Enter employee ID: "))

        employee = next(
            (employee for employee in employees if employee["id"] == employee_id),
            None
        )

        if employee is None:
            print("Employee not found.")
            return

        employees.remove(employee)
        save_employees(employees)

        print("Employee deleted successfully.")

    except ValueError as error:
        print(f"Error: {error}")


def search_employee(employees):
    name = input("Enter employee name: ").strip().lower()

    results = [
        employee
        for employee in employees
        if name in employee["name"].lower()
    ]

    if results:
        for employee in results:
            print(employee)
    else:
        print("Employee not found.")


def filter_department(employees):
    department = input("Enter department: ").strip().lower()

    results = [
        employee
        for employee in employees
        if employee["department"].lower() == department
    ]

    if results:
        for employee in results:
            print(employee)
    else:
        print("No employees found.")


def sort_employees(employees):
    if not employees:
        print("No employees available.")
        return

    sorted_employees = sorted(
        employees,
        key=lambda employee: employee["salary"],
        reverse=True
    )

    for employee in sorted_employees:
        print(employee)


def statistics(employees):
    if not employees:
        print("No employees available.")
        return

    salaries = [employee["salary"] for employee in employees]

    total = sum(salaries)
    average = total / len(salaries)
    highest = max(salaries)
    lowest = min(salaries)

    print(f"Total Employees: {len(employees)}")
    print(f"Average Salary: {average:.2f}")
    print(f"Highest Salary: {highest:.2f}")
    print(f"Lowest Salary: {lowest:.2f}")


def list_employees(employees):
    if not employees:
        print("No employees available.")
        return

    for employee in employees:
        print(employee)


def show_menu():
    print("\nEmployee Management System")
    print("1. Add Employee")
    print("2. Update Employee")
    print("3. Delete Employee")
    print("4. Search Employee")
    print("5. List Employees")
    print("6. Filter by Department")
    print("7. Sort by Salary")
    print("8. Statistics")
    print("9. Exit")


def main():
    employees = load_employees()

    while True:
        show_menu()

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                add_employee(employees)
            elif choice == 2:
                update_employee(employees)
            elif choice == 3:
                delete_employee(employees)
            elif choice == 4:
                search_employee(employees)
            elif choice == 5:
                list_employees(employees)
            elif choice == 6:
                filter_department(employees)
            elif choice == 7:
                sort_employees(employees)
            elif choice == 8:
                statistics(employees)
            elif choice == 9:
                print("Thank you.")
                break
            else:
                print("Invalid choice.")

        except ValueError:
            print("Please enter a valid number.")


if __name__ == "__main__":
    main()
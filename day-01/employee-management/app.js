// ==========================================
// DAY 1 - EMPLOYEE MANAGEMENT CLI
// ==========================================

const readline = require("readline");

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Employee data
let employees = [
    {
        id: 1,
        name: "Rahul",
        salary: 35000,
        department: "IT"
    },
    {
        id: 2,
        name: "Amit",
        salary: 45000,
        department: "HR"
    },
    {
        id: 3,
        name: "Sneha",
        salary: 55000,
        department: "IT"
    }
];

// ==========================================
// SHOW MENU
// ==========================================

function showMenu() {

    console.log("\n================================");
    console.log("    EMPLOYEE MANAGEMENT SYSTEM");
    console.log("================================");

    console.log("1. Add Employee");
    console.log("2. Update Employee");
    console.log("3. Delete Employee");
    console.log("4. Search Employee");
    console.log("5. List Employees");
    console.log("6. Highest Salary");
    console.log("7. Average Salary");
    console.log("8. Department Filter");
    console.log("9. Exit");

    rl.question("\nEnter your choice: ", handleChoice);
}

// ==========================================
// 1. ADD EMPLOYEE
// ==========================================

function addEmployee() {

    rl.question("Enter employee name: ", name => {

        rl.question("Enter salary: ", salary => {

            rl.question("Enter department: ", department => {

                const employee = {
                    id: employees.length + 1,
                    name: name,
                    salary: Number(salary),
                    department: department
                };

                employees.push(employee);

                console.log("\nEmployee added successfully!");

                showMenu();
            });
        });
    });
}

// ==========================================
// 2. UPDATE EMPLOYEE
// ==========================================

function updateEmployee() {

    rl.question("Enter employee ID: ", id => {

        const employee = employees.find(
            emp => emp.id === Number(id)
        );

        if (!employee) {

            console.log("\nEmployee not found!");

            return showMenu();
        }

        rl.question("Enter new name: ", name => {

            rl.question("Enter new salary: ", salary => {

                rl.question("Enter new department: ", department => {

                    employee.name = name;
                    employee.salary = Number(salary);
                    employee.department = department;

                    console.log("\nEmployee updated successfully!");

                    showMenu();
                });
            });
        });
    });
}

// ==========================================
// 3. DELETE EMPLOYEE
// ==========================================

function deleteEmployee() {

    rl.question("Enter employee ID: ", id => {

        const index = employees.findIndex(
            emp => emp.id === Number(id)
        );

        if (index === -1) {

            console.log("\nEmployee not found!");

            return showMenu();
        }

        employees.splice(index, 1);

        console.log("\nEmployee deleted successfully!");

        showMenu();
    });
}

// ==========================================
// 4. SEARCH EMPLOYEE
// ==========================================

function searchEmployee() {

    rl.question("Enter employee name: ", name => {

        const result = employees.filter(
            emp =>
                emp.name
                    .toLowerCase()
                    .includes(name.toLowerCase())
        );

        if (result.length === 0) {

            console.log("\nEmployee not found!");

        } else {

            console.table(result);
        }

        showMenu();
    });
}

// ==========================================
// 5. LIST EMPLOYEES
// ==========================================

function listEmployees() {

    console.log("\nAll Employees:");

    console.table(employees);

    showMenu();
}

// ==========================================
// 6. HIGHEST SALARY
// ==========================================

function highestSalary() {

    if (employees.length === 0) {

        console.log("\nNo employees available.");

        return showMenu();
    }

    const highest = employees.reduce(
        (max, employee) =>
            employee.salary > max.salary
                ? employee
                : max
    );

    console.log("\nHighest Paid Employee:");

    console.table([highest]);

    showMenu();
}

// ==========================================
// 7. AVERAGE SALARY
// ==========================================

function averageSalary() {

    if (employees.length === 0) {

        console.log("\nNo employees available.");

        return showMenu();
    }

    const totalSalary = employees.reduce(
        (total, employee) =>
            total + employee.salary,
        0
    );

    const average = totalSalary / employees.length;

    console.log("\nAverage Salary:", average);

    showMenu();
}

// ==========================================
// 8. DEPARTMENT FILTER
// ==========================================

function departmentFilter() {

    rl.question("Enter department: ", department => {

        const result = employees.filter(
            emp =>
                emp.department.toLowerCase() ===
                department.toLowerCase()
        );

        if (result.length === 0) {

            console.log("\nNo employees found.");

        } else {

            console.table(result);
        }

        showMenu();
    });
}

// ==========================================
// HANDLE MENU
// ==========================================

function handleChoice(choice) {

    switch (choice) {

        case "1":
            addEmployee();
            break;

        case "2":
            updateEmployee();
            break;

        case "3":
            deleteEmployee();
            break;

        case "4":
            searchEmployee();
            break;

        case "5":
            listEmployees();
            break;

        case "6":
            highestSalary();
            break;

        case "7":
            averageSalary();
            break;

        case "8":
            departmentFilter();
            break;

        case "9":
            console.log("\nThank you for using Employee Management System!");
            rl.close();
            break;

        default:
            console.log("\nInvalid choice!");
            showMenu();
    }
}

// ==========================================
// START APPLICATION
// ==========================================

console.log("\nWelcome to Employee Management System!");

showMenu();
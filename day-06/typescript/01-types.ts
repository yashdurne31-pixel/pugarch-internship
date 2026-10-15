type EmployeeStatus = "active" | "inactive";

interface Employee {
  id: number;
  name: string;
  email: string;
  department: string;
  salary: number;
  status?: EmployeeStatus;
}

const employees: Employee[] = [
  { id: 1, name: "Aarav Sharma", email: "aarav@example.com", department: "Engineering", salary: 72000, status: "active" },
  { id: 2, name: "Meera Patel", email: "meera@example.com", department: "HR", salary: 54000, status: "active" }
];

function averageSalary(items: Employee[]): number {
  if (items.length === 0) return 0;
  return items.reduce((total, employee) => total + employee.salary, 0) / items.length;
}

function describeEmployee(employee: Employee): string {
  const status = employee.status ?? "active";
  return `${employee.name} works in ${employee.department} (${status}).`;
}

console.log(employees.map(describeEmployee));
console.log("Average salary:", averageSalary(employees));

export type Employee = { id: number; name: string; email: string; department: string; role: string; salary: number };
const employees: Employee[] = [
  { id: 1, name: "Aarav Sharma", email: "aarav@example.com", department: "Engineering", role: "Frontend Developer", salary: 72000 },
  { id: 2, name: "Meera Patel", email: "meera@example.com", department: "Human Resources", role: "HR Executive", salary: 54000 },
  { id: 3, name: "Rohan Deshmukh", email: "rohan@example.com", department: "Finance", role: "Accountant", salary: 61000 }
];
export function listEmployees() { return employees; }
export function getEmployee(id: number) { return employees.find(employee => employee.id === id); }

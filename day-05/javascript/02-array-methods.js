const employees = [
  { id: 1, name: "Aarav Sharma", department: "Engineering", salary: 65000 },
  { id: 2, name: "Priya Patel", department: "Design", salary: 58000 },
  { id: 3, name: "Rohan Verma", department: "Engineering", salary: 72000 },
  { id: 4, name: "Meera Joshi", department: "HR", salary: 52000 },
  { id: 5, name: "Kabir Khan", department: "Finance", salary: 61000 }
];

console.log("Find employee:", employees.find(employee => employee.id === 3));
console.log("Engineering:", employees.filter(employee => employee.department === "Engineering"));
console.log("Names:", employees.map(employee => employee.name));
console.log("Average salary:", employees.reduce((sum, employee) => sum + employee.salary, 0) / employees.length);
console.log("Sorted by salary:", [...employees].sort((a, b) => b.salary - a.salary));
console.log("Any salary above 70000:", employees.some(employee => employee.salary > 70000));
console.log("All salaries positive:", employees.every(employee => employee.salary > 0));

const employee = {
  id: 1,
  name: "Aarav Sharma",
  department: "Engineering",
  role: "Frontend Developer",
  salary: 65000,
  active: true
};

const formatCurrency = amount =>
  new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0
  }).format(amount);

const names = ["Aarav", "Priya", "Rohan", "Meera"];
const uppercaseNames = names.map(name => name.toUpperCase());
const longNames = names.filter(name => name.length > 4);
const totalSalary = [45000, 65000, 72000].reduce((total, salary) => total + salary, 0);

const { name, department, ...employeeDetails } = employee;
const updatedEmployee = { ...employee, department: "Product" };

console.log({ name, department, employeeDetails, updatedEmployee });
console.log("Uppercase names:", uppercaseNames);
console.log("Names longer than four characters:", longNames);
console.log("Total salary:", formatCurrency(totalSalary));
console.log("Any active employee:", [employee].some(item => item.active));
console.log("All employees have IDs:", [employee].every(item => Number.isInteger(item.id)));

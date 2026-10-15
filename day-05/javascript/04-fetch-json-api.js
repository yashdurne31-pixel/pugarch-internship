async function loadEmployees() {
  try {
    const response = await fetch("../employee-dashboard/data/employees.json");

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    const employees = await response.json();
    console.table(employees);
  } catch (error) {
    console.error("Could not load employee data:", error.message);
  }
}

loadEmployees();

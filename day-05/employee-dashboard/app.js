const DATA_URL = "./data/employees.json";
const STORAGE_KEY = "peopledesk-employees-v1";

const tableBody = document.querySelector("#employeeTable");
const searchInput = document.querySelector("#searchInput");
const departmentFilter = document.querySelector("#departmentFilter");
const sortSelect = document.querySelector("#sortSelect");
const employeeDialog = document.querySelector("#employeeDialog");
const employeeForm = document.querySelector("#employeeForm");
const detailsDialog = document.querySelector("#detailsDialog");
const toast = document.querySelector("#toast");

let employees = [];
let toastTimer;

const currency = amount => new Intl.NumberFormat("en-IN", {
  style: "currency",
  currency: "INR",
  maximumFractionDigits: 0
}).format(Number(amount) || 0);

const initials = name => name.split(/\s+/).slice(0, 2).map(part => part[0] || "").join("").toUpperCase();

function escapeHTML(value) {
  return String(value ?? "").replace(/[&<>"']/g, character => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;"
  })[character]);
}

function saveEmployees() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(employees));
}

function showToast(message) {
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("show"), 2600);
}

async function loadEmployees() {
  const saved = localStorage.getItem(STORAGE_KEY);
  if (saved) {
    try {
      employees = JSON.parse(saved);
      if (!Array.isArray(employees)) throw new Error("Saved data is not a list");
      return;
    } catch {
      localStorage.removeItem(STORAGE_KEY);
    }
  }

  try {
    const response = await fetch(DATA_URL);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    employees = await response.json();
  } catch (error) {
    console.error("Could not load JSON seed data:", error);
    employees = [
      { id: 1001, name: "Aarav Sharma", email: "aarav@example.com", department: "Engineering", role: "Frontend Developer", salary: 780000, status: "Active", location: "Pune" },
      { id: 1002, name: "Priya Patel", email: "priya@example.com", department: "Design", role: "Product Designer", salary: 720000, status: "Active", location: "Mumbai" },
      { id: 1003, name: "Rohan Verma", email: "rohan@example.com", department: "Engineering", role: "Backend Developer", salary: 900000, status: "Active", location: "Nagpur" },
      { id: 1004, name: "Meera Joshi", email: "meera@example.com", department: "Human Resources", role: "HR Specialist", salary: 610000, status: "Inactive", location: "Pune" },
      { id: 1005, name: "Kabir Khan", email: "kabir@example.com", department: "Finance", role: "Financial Analyst", salary: 680000, status: "Active", location: "Hyderabad" },
      { id: 1006, name: "Ananya Deshmukh", email: "ananya@example.com", department: "Marketing", role: "Marketing Executive", salary: 590000, status: "Active", location: "Amravati" },
      { id: 1007, name: "Ishaan Gupta", email: "ishaan@example.com", department: "Operations", role: "Operations Analyst", salary: 640000, status: "Active", location: "Pune" },
      { id: 1008, name: "Sara Thomas", email: "sara@example.com", department: "Sales", role: "Account Executive", salary: 700000, status: "Inactive", location: "Mumbai" }
    ];
  }
  saveEmployees();
}

function updateStats() {
  document.querySelector("#totalEmployees").textContent = employees.length;
  const average = employees.length
    ? employees.reduce((sum, employee) => sum + Number(employee.salary || 0), 0) / employees.length
    : 0;
  document.querySelector("#averageSalary").textContent = currency(average);
  document.querySelector("#totalDepartments").textContent = new Set(employees.map(employee => employee.department)).size;
  document.querySelector("#activeEmployees").textContent = employees.filter(employee => employee.status === "Active").length;
}

function updateDepartmentOptions() {
  const current = departmentFilter.value;
  const departments = [...new Set(employees.map(employee => employee.department))].sort((a, b) => a.localeCompare(b));
  departmentFilter.innerHTML = '<option value="">All departments</option>' +
    departments.map(department => `<option value="${escapeHTML(department)}">${escapeHTML(department)}</option>`).join("");
  if (departments.includes(current)) departmentFilter.value = current;
}

function getVisibleEmployees() {
  const query = searchInput.value.trim().toLowerCase();
  const department = departmentFilter.value;
  const visible = employees.filter(employee => {
    const searchable = [employee.name, employee.email, employee.role, employee.department, employee.location]
      .join(" ").toLowerCase();
    return searchable.includes(query) && (!department || employee.department === department);
  });

  const [field, direction] = sortSelect.value.split("-");
  visible.sort((a, b) => {
    let result;
    if (field === "salary") result = Number(a.salary) - Number(b.salary);
    else result = String(a[field] ?? "").localeCompare(String(b[field] ?? ""));
    return direction === "desc" ? -result : result;
  });
  return visible;
}

function renderEmployees() {
  updateStats();
  updateDepartmentOptions();
  const visible = getVisibleEmployees();
  document.querySelector("#resultCount").textContent = `${visible.length} employee${visible.length === 1 ? "" : "s"}`;
  document.querySelector("#emptyState").hidden = visible.length > 0;
  tableBody.innerHTML = visible.map(employee => `
    <tr>
      <td><div class="person"><span class="person-avatar">${escapeHTML(initials(employee.name))}</span><div><strong>${escapeHTML(employee.name)}</strong><small>${escapeHTML(employee.email)}</small></div></div></td>
      <td>${escapeHTML(employee.department)}</td>
      <td>${escapeHTML(employee.role)}</td>
      <td>${currency(employee.salary)}</td>
      <td><span class="status ${employee.status === "Active" ? "active" : "inactive"}">${escapeHTML(employee.status)}</span></td>
      <td><div class="actions">
        <button class="action-btn" data-action="details" data-id="${employee.id}">View</button>
        <button class="action-btn" data-action="edit" data-id="${employee.id}">Edit</button>
        <button class="action-btn delete" data-action="delete" data-id="${employee.id}">Delete</button>
      </div></td>
    </tr>`).join("");
}

function openAddDialog() {
  employeeForm.reset();
  document.querySelector("#employeeId").value = "";
  document.querySelector("#dialogTitle").textContent = "Add employee";
  employeeDialog.showModal();
}

function openEditDialog(employee) {
  employeeForm.reset();
  document.querySelector("#employeeId").value = employee.id;
  document.querySelector("#dialogTitle").textContent = "Edit employee";
  document.querySelector("#nameInput").value = employee.name;
  document.querySelector("#emailInput").value = employee.email;
  document.querySelector("#departmentInput").value = employee.department;
  if (![...document.querySelector("#departmentInput").options].some(option => option.value === employee.department)) {
    const option = new Option(employee.department, employee.department);
    document.querySelector("#departmentInput").add(option);
    document.querySelector("#departmentInput").value = employee.department;
  }
  document.querySelector("#roleInput").value = employee.role;
  document.querySelector("#salaryInput").value = employee.salary;
  document.querySelector("#statusInput").value = employee.status;
  document.querySelector("#locationInput").value = employee.location || "";
  employeeDialog.showModal();
}

function showDetails(employee) {
  const fields = [
    ["Name", employee.name], ["Email", employee.email],
    ["Department", employee.department], ["Job title", employee.role],
    ["Annual salary", currency(employee.salary)], ["Status", employee.status],
    ["Location", employee.location || "Not specified"], ["Employee ID", employee.id]
  ];
  document.querySelector("#detailsContent").innerHTML = fields.map(([label, value]) =>
    `<div class="detail-item"><span>${escapeHTML(label)}</span><strong>${escapeHTML(value)}</strong></div>`
  ).join("");
  detailsDialog.showModal();
}

employeeForm.addEventListener("submit", event => {
  event.preventDefault();
  if (!employeeForm.reportValidity()) return;

  const idValue = document.querySelector("#employeeId").value;
  const record = {
    id: idValue ? Number(idValue) : Math.max(1000, ...employees.map(employee => Number(employee.id) || 0)) + 1,
    name: document.querySelector("#nameInput").value.trim(),
    email: document.querySelector("#emailInput").value.trim(),
    department: document.querySelector("#departmentInput").value,
    role: document.querySelector("#roleInput").value.trim(),
    salary: Number(document.querySelector("#salaryInput").value),
    status: document.querySelector("#statusInput").value,
    location: document.querySelector("#locationInput").value.trim()
  };

  if (!record.name || !record.email || !record.role || !Number.isFinite(record.salary) || record.salary < 0) {
    showToast("Please check the employee details.");
    return;
  }

  const duplicateEmail = employees.some(employee =>
    employee.email.toLowerCase() === record.email.toLowerCase() && employee.id !== record.id
  );
  if (duplicateEmail) {
    showToast("An employee with this email already exists.");
    document.querySelector("#emailInput").focus();
    return;
  }

  if (idValue) {
    employees = employees.map(employee => employee.id === record.id ? record : employee);
    showToast("Employee updated successfully.");
  } else {
    employees.push(record);
    showToast("Employee added successfully.");
  }

  saveEmployees();
  renderEmployees();
  employeeDialog.close();
});

tableBody.addEventListener("click", event => {
  const button = event.target.closest("button[data-action]");
  if (!button) return;
  const employee = employees.find(item => item.id === Number(button.dataset.id));
  if (!employee) return;

  if (button.dataset.action === "details") showDetails(employee);
  if (button.dataset.action === "edit") openEditDialog(employee);
  if (button.dataset.action === "delete") {
    if (!confirm(`Delete ${employee.name} from the directory?`)) return;
    employees = employees.filter(item => item.id !== employee.id);
    saveEmployees();
    renderEmployees();
    showToast("Employee deleted.");
  }
});

searchInput.addEventListener("input", renderEmployees);
departmentFilter.addEventListener("change", renderEmployees);
sortSelect.addEventListener("change", renderEmployees);
document.querySelector("#addEmployeeBtn").addEventListener("click", openAddDialog);
document.querySelector("#closeDialogBtn").addEventListener("click", () => employeeDialog.close());
document.querySelector("#cancelBtn").addEventListener("click", () => employeeDialog.close());
document.querySelector("#closeDetailsBtn").addEventListener("click", () => detailsDialog.close());
document.querySelector("#detailsDoneBtn").addEventListener("click", () => detailsDialog.close());
document.querySelector("#clearFiltersBtn").addEventListener("click", () => {
  searchInput.value = "";
  departmentFilter.value = "";
  sortSelect.value = "name-asc";
  renderEmployees();
});

loadEmployees().then(renderEmployees);

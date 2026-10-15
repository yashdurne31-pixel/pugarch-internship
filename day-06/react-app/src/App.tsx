import { useEffect, useMemo, useState, type FormEvent } from "react";
import type { Employee } from "./types";

const seed: Employee[] = [
  { id: 1, name: "Aarav Sharma", email: "aarav@example.com", department: "Engineering", role: "Frontend Developer", salary: 72000 },
  { id: 2, name: "Meera Patel", email: "meera@example.com", department: "Human Resources", role: "HR Executive", salary: 54000 },
  { id: 3, name: "Rohan Deshmukh", email: "rohan@example.com", department: "Finance", role: "Accountant", salary: 61000 },
  { id: 4, name: "Ananya Joshi", email: "ananya@example.com", department: "Engineering", role: "QA Engineer", salary: 68000 },
  { id: 5, name: "Kabir Khan", email: "kabir@example.com", department: "Design", role: "UI Designer", salary: 59000 }
];

export default function App() {
  const [employees, setEmployees] = useState<Employee[]>(() => {
    try {
      const saved = localStorage.getItem("day06-employees");
      return saved ? JSON.parse(saved) as Employee[] : seed;
    } catch { return seed; }
  });
  const [query, setQuery] = useState("");
  const [department, setDepartment] = useState("All");
  const [sortBy, setSortBy] = useState("name");
  const [editing, setEditing] = useState<Employee | null>(null);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [dept, setDept] = useState("Engineering");
  const [role, setRole] = useState("");
  const [salary, setSalary] = useState("50000");
  const [message, setMessage] = useState("");

  useEffect(() => localStorage.setItem("day06-employees", JSON.stringify(employees)), [employees]);

  const departments = useMemo(() => ["All", ...Array.from(new Set(employees.map(e => e.department))).sort()], [employees]);
  const filtered = useMemo(() => employees
    .filter(e => [e.name, e.email, e.role, e.department].some(v => v.toLowerCase().includes(query.toLowerCase().trim())))
    .filter(e => department === "All" || e.department === department)
    .sort((a, b) => sortBy === "salary" ? b.salary - a.salary : a[sortBy as "name" | "department"].localeCompare(b[sortBy as "name" | "department"])),
  [employees, query, department, sortBy]);

  const average = employees.length ? Math.round(employees.reduce((s, e) => s + e.salary, 0) / employees.length) : 0;

  function resetForm() {
    setEditing(null); setName(""); setEmail(""); setDept("Engineering"); setRole(""); setSalary("50000");
  }

  function submit(event: FormEvent) {
    event.preventDefault();
    if (!name.trim() || !role.trim() || !email.includes("@") || Number(salary) <= 0) {
      setMessage("Enter a valid name, email, role and positive salary."); return;
    }
    const duplicate = employees.some(e => e.email.toLowerCase() === email.trim().toLowerCase() && e.id !== editing?.id);
    if (duplicate) { setMessage("That email is already in use."); return; }
    const record: Employee = { id: editing?.id ?? Date.now(), name: name.trim(), email: email.trim(), department: dept, role: role.trim(), salary: Number(salary) };
    setEmployees(old => editing ? old.map(e => e.id === editing.id ? record : e) : [record, ...old]);
    setMessage(editing ? "Employee updated." : "Employee added.");
    resetForm();
  }

  function editEmployee(employee: Employee) {
    setEditing(employee); setName(employee.name); setEmail(employee.email); setDept(employee.department); setRole(employee.role); setSalary(String(employee.salary));
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function deleteEmployee(employee: Employee) {
    if (window.confirm(`Delete ${employee.name}?`)) {
      setEmployees(old => old.filter(e => e.id !== employee.id));
      setMessage("Employee deleted.");
    }
  }

  return <main className="shell">
    <header className="hero"><div><p className="eyebrow">PEOPLE OPERATIONS</p><h1>Employee Dashboard</h1><p className="muted">Day 6 · React + TypeScript</p></div><span className="badge">LIVE DEMO</span></header>
    <section className="metrics">
      <article><span>Total employees</span><strong>{employees.length}</strong></article>
      <article><span>Departments</span><strong>{Math.max(0, departments.length - 1)}</strong></article>
      <article><span>Average salary</span><strong>₹{average.toLocaleString("en-IN")}</strong></article>
    </section>
    <section className="panel">
      <h2>{editing ? "Edit employee" : "Add employee"}</h2>
      <form className="form" onSubmit={submit}>
        <label>Full name<input value={name} onChange={e => setName(e.target.value)} placeholder="Employee name" required /></label>
        <label>Email<input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="name@example.com" required /></label>
        <label>Department<select value={dept} onChange={e => setDept(e.target.value)}>{["Engineering", "Human Resources", "Finance", "Design", "Operations"].map(d => <option key={d}>{d}</option>)}</select></label>
        <label>Role<input value={role} onChange={e => setRole(e.target.value)} placeholder="Job title" required /></label>
        <label>Salary (₹)<input type="number" min="1" value={salary} onChange={e => setSalary(e.target.value)} required /></label>
        <div className="actions"><button type="submit">{editing ? "Save changes" : "Add employee"}</button>{editing && <button type="button" className="secondary" onClick={resetForm}>Cancel</button>}</div>
      </form>
      {message && <p className="message" role="status">{message}</p>}
    </section>
    <section className="panel">
      <div className="list-head"><div><h2>Team directory</h2><p className="muted">{filtered.length} matching records</p></div><div className="filters">
        <input aria-label="Search employees" value={query} onChange={e => setQuery(e.target.value)} placeholder="Search team…" />
        <select aria-label="Filter department" value={department} onChange={e => setDepartment(e.target.value)}>{departments.map(d => <option key={d}>{d}</option>)}</select>
        <select aria-label="Sort employees" value={sortBy} onChange={e => setSortBy(e.target.value)}><option value="name">Sort: name</option><option value="department">Sort: department</option><option value="salary">Sort: salary</option></select>
      </div></div>
      <div className="table-wrap"><table><thead><tr><th>Employee</th><th>Department</th><th>Role</th><th>Salary</th><th>Actions</th></tr></thead>
        <tbody>{filtered.map(e => <tr key={e.id}><td><strong>{e.name}</strong><small>{e.email}</small></td><td>{e.department}</td><td>{e.role}</td><td>₹{e.salary.toLocaleString("en-IN")}</td><td><div className="row-actions"><button className="secondary" onClick={() => alert(`${e.name}\n${e.email}\n${e.department} · ${e.role}\nSalary: ₹${e.salary.toLocaleString("en-IN")}`)}>Details</button><button className="secondary" onClick={() => editEmployee(e)}>Edit</button><button className="danger" onClick={() => deleteEmployee(e)}>Delete</button></div></td></tr>)}
        {filtered.length === 0 && <tr><td colSpan={5} className="empty">No employees match your search.</td></tr>}</tbody>
      </table></div>
    </section>
    <footer>Built with React, TypeScript, Vite and browser localStorage.</footer>
  </main>;
}

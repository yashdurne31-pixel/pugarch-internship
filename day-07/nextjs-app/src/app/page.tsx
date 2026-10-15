import Link from "next/link";
import { listEmployees } from "@/lib/employees";
export default function HomePage() {
  const employees = listEmployees();
  const average = Math.round(employees.reduce((sum, e) => sum + e.salary, 0) / employees.length);
  const departments = new Set(employees.map(e => e.department)).size;
  return <main className="wrap">
    <p className="eyebrow">DAY 7 · NEXT.JS + NODE.JS</p><h1>Employee Portal</h1><p className="muted">A small App Router example with list, detail and create routes.</p>
    <section className="grid"><div className="metric">Employees<strong>{employees.length}</strong></div><div className="metric">Departments<strong>{departments}</strong></div><div className="metric">Average salary<strong>₹{average.toLocaleString("en-IN")}</strong></div></section>
    <section className="card"><h2>Employees</h2>{employees.map(e => <div className="row" key={e.id}><div><strong>{e.name}</strong><div className="muted">{e.role} · {e.department}</div></div><Link href={`/employees/${e.id}`}>View profile →</Link></div>)}<p><Link href="/employees">Browse all employees</Link></p><p><Link href="/employees/create">Create employee (demo form)</Link></p></section>
    <p className="muted">This starter uses in-memory sample data. The Express API in <code>../node-api</code> is a separate backend.</p>
  </main>;
}

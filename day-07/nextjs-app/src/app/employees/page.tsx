import Link from "next/link";
import { listEmployees } from "@/lib/employees";
export default function EmployeesPage() {
  return <main className="wrap"><p className="eyebrow">DIRECTORY</p><h1>Employees</h1><p><Link href="/">← Dashboard</Link></p><section className="card">{listEmployees().map(e => <div className="row" key={e.id}><div><strong>{e.name}</strong><div className="muted">{e.email}</div></div><Link href={`/employees/${e.id}`}>Details</Link></div>)}</section><Link href="/employees/create">Create employee →</Link></main>;
}

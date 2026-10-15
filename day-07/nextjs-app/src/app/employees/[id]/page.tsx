import Link from "next/link";
import { notFound } from "next/navigation";
import { getEmployee } from "@/lib/employees";
export default async function EmployeeDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const employee = getEmployee(Number(id));
  if (!employee) notFound();
  return <main className="wrap"><p className="eyebrow">EMPLOYEE PROFILE</p><h1>{employee.name}</h1><p><Link href="/employees">← Back to employees</Link></p><section className="card"><p><strong>Email:</strong> {employee.email}</p><p><strong>Department:</strong> {employee.department}</p><p><strong>Role:</strong> {employee.role}</p><p><strong>Salary:</strong> ₹{employee.salary.toLocaleString("en-IN")}</p></section></main>;
}

"use client";
import Link from "next/link";
import { useState, type FormEvent } from "react";
export default function CreateEmployeePage() {
  const [message, setMessage] = useState("");
  function submit(event: FormEvent<HTMLFormElement>) { event.preventDefault(); setMessage("Demo form validated. Connect this form to the Express API to persist a new employee."); }
  return <main className="wrap"><p className="eyebrow">NEW RECORD</p><h1>Create employee</h1><p><Link href="/employees">← Back to employees</Link></p><section className="card"><form onSubmit={submit} style={{display:"grid",gap:12,maxWidth:500}}><label>Name<input name="name" required style={{display:"block",width:"100%",padding:10,marginTop:5}} /></label><label>Email<input name="email" type="email" required style={{display:"block",width:"100%",padding:10,marginTop:5}} /></label><label>Department<input name="department" required style={{display:"block",width:"100%",padding:10,marginTop:5}} /></label><button style={{padding:12,background:"#1e3a8a",color:"white",border:0,borderRadius:8}}>Validate form</button></form>{message && <p role="status">{message}</p>}</section></main>;
}

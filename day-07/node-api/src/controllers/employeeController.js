import { employeeService } from "../services/employeeService.js";
const required = ["name", "email", "department", "role", "salary"];
function validate(body) {
  const missing = required.filter(key => body[key] === undefined || body[key] === "");
  if (missing.length) return `Missing fields: ${missing.join(", ")}`;
  if (!String(body.email).includes("@")) return "A valid email is required";
  if (!Number.isFinite(Number(body.salary)) || Number(body.salary) <= 0) return "Salary must be a positive number";
  return null;
}
export const employeeController = {
  list: (_req, res) => res.json({ data: employeeService.list() }),
  get: (req, res) => { const item = employeeService.get(req.params.id); return item ? res.json({ data: item }) : res.status(404).json({ error: "Employee not found" }); },
  create: (req, res) => { const error = validate(req.body); if (error) return res.status(400).json({ error }); const item = employeeService.create({ ...req.body, salary: Number(req.body.salary) }); return res.status(201).json({ data: item }); },
  update: (req, res) => { const error = validate(req.body); if (error) return res.status(400).json({ error }); const item = employeeService.update(req.params.id, { ...req.body, salary: Number(req.body.salary) }); return item ? res.json({ data: item }) : res.status(404).json({ error: "Employee not found" }); },
  remove: (req, res) => employeeService.remove(req.params.id) ? res.status(204).end() : res.status(404).json({ error: "Employee not found" })
};

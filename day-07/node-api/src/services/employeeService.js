import { employees } from "../data/employees.js";
let nextId = Math.max(...employees.map(e => e.id), 0) + 1;
export const employeeService = {
  list: () => employees,
  get: id => employees.find(e => e.id === Number(id)),
  create: data => { const item = { id: nextId++, ...data }; employees.push(item); return item; },
  update: (id, data) => { const index = employees.findIndex(e => e.id === Number(id)); if (index < 0) return null; employees[index] = { ...employees[index], ...data, id: Number(id) }; return employees[index]; },
  remove: id => { const index = employees.findIndex(e => e.id === Number(id)); if (index < 0) return false; employees.splice(index, 1); return true; }
};

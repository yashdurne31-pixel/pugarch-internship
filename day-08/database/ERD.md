# Database design

```text
departments 1 ─── * employees * ─── 0..1 users
facilities  1 ─── * inspections
facilities  1 ─── * complaints
users       1 ─── * inspections (optional inspector)
users       1 ─── * complaints  (optional reporter)
```

- `users.email` is unique.
- `employees.department_id` references departments.
- Inspection history is indexed by `(facility_id, inspection_date)`.
- Complaints have a status index to support open-complaint queries.
- Deleting a facility cascades to its inspections and complaints in this training schema.

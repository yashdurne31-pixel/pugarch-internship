# Day 09 — Angular Facility Inspection Dashboard

Angular 20 standalone app for the Day 08 Laravel facility API.

## Requirements
Node.js 20.19+ or 22.12+, npm, and the Laravel API running at `http://127.0.0.1:8000`.

## Run
Open PowerShell in `day-09/angular-app`:
```powershell
npm install
npm start
```
Open the localhost URL printed by Angular CLI (usually `http://localhost:4200`).

## Build
```powershell
npm run build
```

## Expected API routes
- `GET /api/facilities` returns Laravel pagination data.
- `GET /api/facilities/{id}` returns a facility.
- `GET /api/inspections` returns inspection list/pagination.
- `GET /api/inspections?facility_id={id}` optionally filters.
- `POST /api/inspections` creates an inspection.

Facilities API was verified in the prior setup. Inspection routes and the create payload depend on your Laravel implementation; adjust `src/app/core/services/api.service.ts` if your route names or fields differ.

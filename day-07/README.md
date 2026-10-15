# Day 7 — Next.js + Node.js

## Contents
- `nextjs-app/`: Next.js App Router pages for dashboard, employee list, dynamic employee details, create form, loading/error/not-found concepts.
- `node-api/`: Express REST API with routes, controllers, service, in-memory model data, validation and error middleware.

## Run Express API
Open a terminal:
```bash
cd day-07/node-api
npm install
npm run dev
```
API base: `http://localhost:4000/api/employees`
- `GET /api/employees`
- `GET /api/employees/:id`
- `POST /api/employees`
- `PUT /api/employees/:id`
- `DELETE /api/employees/:id`
- `GET /health`

Example JSON for POST/PUT:
```json
{"name":"Isha Kulkarni","email":"isha@example.com","department":"Engineering","role":"Developer","salary":65000}
```

## Run Next.js app
In a second terminal:
```bash
cd day-07/nextjs-app
npm install
npm run dev
```
Open `http://localhost:3000`.

## Important limitations
The Express API uses in-memory data, so records reset when the server restarts. The Next.js pages currently use local sample data; connecting the pages to the Express API is a follow-up integration task. No production authentication is implemented. Do not expose this demo API publicly.

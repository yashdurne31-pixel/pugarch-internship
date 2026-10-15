# Day 5 — JavaScript Employee Dashboard

## Project Overview
A vanilla JavaScript employee dashboard that demonstrates modern JavaScript, asynchronous JSON loading, reusable functions, filtering, sorting, and CRUD operations.

## Problem Statement
Create an employee dashboard that can list, search, filter, sort, view, add, edit, and delete employee records.

## Features
- Employee list loaded from a local JSON file using `fetch` and `async/await`
- Search by name, email, department, role, or location
- Filter by department
- Sort by name, department, or salary
- Employee detail view
- Add, edit, and delete employees
- Form validation and duplicate-email protection
- Dashboard statistics: employee count, average salary, departments, active employees
- Browser `localStorage` persistence
- Responsive layout for desktop and mobile
- Standalone JavaScript exercises covering fundamentals, array methods, closures, promises, and API/JSON handling

## Technology Stack
HTML5, CSS3, modern JavaScript (ES6+), JSON, Fetch API, browser localStorage.

## Architecture
- `javascript/`: short learning exercises
- `employee-dashboard/index.html`: page structure and dialogs
- `employee-dashboard/styles.css`: responsive dashboard styling
- `employee-dashboard/app.js`: data loading, rendering, search, filtering, sorting and CRUD logic
- `employee-dashboard/data/employees.json`: sample seed data

## API Documentation
The dashboard fetches the seed JSON from `./data/employees.json` using HTTP GET. Since this is a static demo, create/update/delete operations are stored in browser `localStorage`; no remote REST server is included.

## Installation
No npm packages or external libraries are required. Install the VS Code Live Server extension if you do not already have a local HTTP server.

## How to Run
1. Open the project folder in VS Code.
2. Right-click `employee-dashboard/index.html`.
3. Choose **Open with Live Server**.
4. Use Add employee, View, Edit, Delete, search, department filter and sort controls.
5. To run an exercise, open the terminal in the project root and run, for example: `node day-05/javascript/01-fundamentals.js`.

Do not open the dashboard by double-clicking `index.html` if you want to load the seed JSON with `fetch`; use Live Server or another local HTTP server.

## Environment Variables
None required.

## Database Design
No database is used. The demo stores browser-local records in the `peopledesk-employees-v1` localStorage key.

## Challenges Faced
- Browsers restrict some `fetch` requests when a page is opened directly from `file://`.
- A static frontend does not provide a shared server-side database.

## Solutions
- Run the page using VS Code Live Server or another local HTTP server.
- Use localStorage for a self-contained CRUD demonstration.

## Future Improvements
- Connect a REST API with persistent database storage.
- Add pagination, role-based access, and automated tests.
- Add server-side validation and authentication.

## Learning Checklist
- `let`, `const`, data types, functions, arrow functions, arrays and objects
- Destructuring, spread/rest, template literals
- `map`, `filter`, `reduce`, `find`, `some`, `every`, `sort`
- Scope, closures, promises, async/await, error handling
- HTTP, JSON, Fetch API, and REST method concepts (GET, POST, PUT, DELETE)

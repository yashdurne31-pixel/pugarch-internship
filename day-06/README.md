# Day 6 — TypeScript + React

## Objective
Convert the employee-management exercise into a typed, component-based React application.

## Contents
- `typescript/`: interfaces, optional properties, unions, generics, and type narrowing exercises.
- `react-app/`: responsive Employee Dashboard with search, department filtering, sorting, details, add/edit/delete, form validation, statistics, and localStorage persistence.

## Run the React app
Install Node.js LTS first. In a terminal:
```bash
cd day-06/react-app
npm install
npm run dev
```
Open the local URL printed by Vite.

## Run TypeScript exercises
```bash
cd day-06/typescript
npm init -y
npm install --save-dev typescript tsx
npx tsx 01-types.ts
npx tsx 02-generics-and-narrowing.ts
```

## Data note
This is a frontend learning project. It persists records in the browser's localStorage and does not use a production backend or authentication.

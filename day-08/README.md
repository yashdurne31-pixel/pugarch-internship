# Day 8 — SQL + Laravel API

## Contents
- `sql/schema.sql`: relational schema for users, departments, employees, facilities, inspections and complaints.
- `sql/seed.sql`: sample rows for local learning only.
- `sql/queries.sql`: joins, grouping, subqueries, filters, complaint counts and a transaction example.
- `database/ERD.md`: relationship summary.
- `laravel-api/`: Laravel API source scaffold with API resource routes, Eloquent models, migrations, and validated CRUD controllers for facilities, inspections and complaints.

## Run SQL
Use MySQL Workbench or a local MySQL server. Run `schema.sql`, then `seed.sql`, then `queries.sql` in order. Sample password hashes are placeholders and must never be used for authentication.

## Laravel scaffold setup
This folder contains selected Laravel project files, not the full Laravel framework runtime. Install PHP 8.2+, Composer and a supported Laravel environment. From the `day-08/laravel-api` folder, use Composer to install dependencies after creating/merging these files into a standard Laravel 12 project. Ensure the Laravel bootstrap enables API routes (Laravel 11/12: `php artisan install:api` on a fresh project if needed), configure `.env` for MySQL, then run:
```bash
php artisan migrate
php artisan serve
```
Test endpoints at `/api/facilities`, `/api/inspections`, and `/api/complaints`.

## Data and security notes
This is a training scaffold. User/inspector foreign-key columns are plain nullable IDs in these migrations; add actual user foreign keys when your Laravel project has the users table. Add authentication, authorization, rate limiting and tests before deployment.

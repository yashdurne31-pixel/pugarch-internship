USE facility_management;

INSERT INTO departments (name)
VALUES
    ('Engineering'),
    ('Operations'),
    ('Finance'),
    ('Human Resources')
ON DUPLICATE KEY UPDATE
    name = VALUES(name);

INSERT INTO users (name, email, password_hash)
VALUES
    ('Aarav Sharma', 'aarav@example.com', 'DEMO_HASH_NOT_FOR_AUTH'),
    ('Meera Patel', 'meera@example.com', 'DEMO_HASH_NOT_FOR_AUTH'),
    ('Rohan Deshmukh', 'rohan@example.com', 'DEMO_HASH_NOT_FOR_AUTH')
ON DUPLICATE KEY UPDATE
    name = VALUES(name);

INSERT INTO employees (user_id, department_id, job_title, salary, hired_on)
SELECT u.id, d.id, seed.job_title, seed.salary, seed.hired_on
FROM (
    SELECT 'aarav@example.com' AS email,
           'Engineering' AS department_name,
           'Frontend Developer' AS job_title,
           72000.00 AS salary,
           '2024-02-01' AS hired_on
    UNION ALL
    SELECT 'meera@example.com', 'Human Resources',
           'HR Executive', 54000.00, '2023-09-12'
    UNION ALL
    SELECT 'rohan@example.com', 'Finance',
           'Accountant', 61000.00, '2022-04-18'
) AS seed
JOIN users u ON u.email = seed.email
JOIN departments d ON d.name = seed.department_name
ON DUPLICATE KEY UPDATE
    department_id = VALUES(department_id),
    job_title = VALUES(job_title),
    salary = VALUES(salary),
    hired_on = VALUES(hired_on);

INSERT INTO facilities (name, location, cleanliness_score, status)
SELECT seed.name, seed.location, seed.cleanliness_score, seed.status
FROM (
    SELECT 'Central Office' AS name, 'Wardha' AS location,
           92 AS cleanliness_score, 'active' AS status
    UNION ALL
    SELECT 'Warehouse A', 'Amravati', 54, 'maintenance'
    UNION ALL
    SELECT 'Training Centre', 'Nagpur', 73, 'active'
) AS seed
WHERE NOT EXISTS (
    SELECT 1
    FROM facilities f
    WHERE f.name = seed.name
      AND f.location = seed.location
);

INSERT INTO inspections
    (facility_id, inspector_user_id, inspection_date, cleanliness_score, notes)
SELECT f.id, u.id, seed.inspection_date, seed.cleanliness_score, seed.notes
FROM (
    SELECT 'Central Office' AS facility_name,
           'Wardha' AS location,
           'aarav@example.com' AS inspector_email,
           '2026-10-01' AS inspection_date,
           92 AS cleanliness_score,
           'Good condition' AS notes
    UNION ALL
    SELECT 'Warehouse A', 'Amravati', 'meera@example.com',
           '2026-10-03', 54, 'Needs cleaning and repair'
    UNION ALL
    SELECT 'Training Centre', 'Nagpur', 'aarav@example.com',
           '2026-10-05', 73, 'Follow-up recommended'
) AS seed
JOIN facilities f
    ON f.name = seed.facility_name
   AND f.location = seed.location
JOIN users u ON u.email = seed.inspector_email
WHERE NOT EXISTS (
    SELECT 1
    FROM inspections i
    WHERE i.facility_id = f.id
      AND i.inspection_date = seed.inspection_date
      AND i.notes = seed.notes
);

INSERT INTO complaints
    (facility_id, reported_by_user_id, description, status)
SELECT f.id, u.id, seed.description, seed.status
FROM (
    SELECT 'Warehouse A' AS facility_name,
           'Amravati' AS location,
           'meera@example.com' AS reporter_email,
           'Washroom cleaning required' AS description,
           'open' AS status
    UNION ALL
    SELECT 'Warehouse A', 'Amravati', 'rohan@example.com',
           'Broken tap in washroom', 'in_progress'
    UNION ALL
    SELECT 'Training Centre', 'Nagpur', 'aarav@example.com',
           'Waste bin collection delayed', 'resolved'
) AS seed
JOIN facilities f
    ON f.name = seed.facility_name
   AND f.location = seed.location
JOIN users u ON u.email = seed.reporter_email
WHERE NOT EXISTS (
    SELECT 1
    FROM complaints c
    WHERE c.facility_id = f.id
      AND c.description = seed.description
);
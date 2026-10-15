USE facility_management;

-- 1. Employees and departments
SELECT u.name, u.email, d.name AS department, e.job_title, e.salary
FROM employees e JOIN users u ON u.id = e.user_id
JOIN departments d ON d.id = e.department_id
ORDER BY d.name, u.name;

-- 2. Average salary by department
SELECT d.name AS department, ROUND(AVG(e.salary), 2) AS average_salary
FROM departments d LEFT JOIN employees e ON e.department_id = d.id
GROUP BY d.id, d.name ORDER BY average_salary DESC;

-- 3. Highest-paid employee
SELECT u.name, e.job_title, e.salary
FROM employees e JOIN users u ON u.id = e.user_id
ORDER BY e.salary DESC LIMIT 1;

-- 4. Facilities with poor cleanliness score
SELECT name, location, cleanliness_score
FROM facilities WHERE cleanliness_score < 60
ORDER BY cleanliness_score ASC;

-- 5. Complaint counts by facility and status
SELECT f.name, c.status, COUNT(c.id) AS complaint_count
FROM facilities f LEFT JOIN complaints c ON c.facility_id = f.id
GROUP BY f.id, f.name, c.status ORDER BY f.name;

-- 6. Inspection history
SELECT f.name, i.inspection_date, i.cleanliness_score, i.notes
FROM inspections i JOIN facilities f ON f.id = i.facility_id
ORDER BY i.inspection_date DESC;

-- 7. Open complaints
SELECT c.id, f.name, c.description, c.created_at
FROM complaints c JOIN facilities f ON f.id = c.facility_id
WHERE c.status <> 'resolved' ORDER BY c.created_at DESC;

-- 8. Subquery: facilities below average cleanliness
SELECT name, cleanliness_score FROM facilities
WHERE cleanliness_score < (SELECT AVG(cleanliness_score) FROM facilities);

-- 9. Transaction example (run deliberately in a test database)
START TRANSACTION;
UPDATE complaints SET status = 'in_progress' WHERE id = 1;
COMMIT;

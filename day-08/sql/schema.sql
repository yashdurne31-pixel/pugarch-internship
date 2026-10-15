CREATE DATABASE IF NOT EXISTS facility_management;

USE facility_management;

CREATE TABLE IF NOT EXISTS departments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(180) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNIQUE,
    department_id INT NOT NULL,
    job_title VARCHAR(120) NOT NULL,
    salary DECIMAL(12,2) NOT NULL CHECK (salary > 0),
    hired_on DATE,
    FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE SET NULL,
    FOREIGN KEY (department_id)
        REFERENCES departments(id)
);

CREATE TABLE IF NOT EXISTS facilities (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(160) NOT NULL,
    location VARCHAR(180) NOT NULL,
    cleanliness_score TINYINT NOT NULL DEFAULT 0
        CHECK (cleanliness_score BETWEEN 0 AND 100),
    status ENUM('active', 'maintenance', 'closed')
        NOT NULL DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS inspections (
    id INT PRIMARY KEY AUTO_INCREMENT,
    facility_id INT NOT NULL,
    inspector_user_id INT,
    inspection_date DATE NOT NULL,
    cleanliness_score TINYINT NOT NULL
        CHECK (cleanliness_score BETWEEN 0 AND 100),
    notes TEXT,
    FOREIGN KEY (facility_id)
        REFERENCES facilities(id)
        ON DELETE CASCADE,
    FOREIGN KEY (inspector_user_id)
        REFERENCES users(id)
        ON DELETE SET NULL,
    INDEX idx_inspections_facility_date
        (facility_id, inspection_date)
);

CREATE TABLE IF NOT EXISTS complaints (
    id INT PRIMARY KEY AUTO_INCREMENT,
    facility_id INT NOT NULL,
    reported_by_user_id INT,
    description TEXT NOT NULL,
    status ENUM('open', 'in_progress', 'resolved')
        NOT NULL DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP NULL,
    FOREIGN KEY (facility_id)
        REFERENCES facilities(id)
        ON DELETE CASCADE,
    FOREIGN KEY (reported_by_user_id)
        REFERENCES users(id)
        ON DELETE SET NULL,
    INDEX idx_complaints_status (status)
);
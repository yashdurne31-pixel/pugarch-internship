"""
Database Connection and Schema Manager for Smart Hygiene Risk Prediction System.
Uses SQLite with foreign keys enforced and transactional context management.
"""

import os
import sqlite3
from typing import Generator
from contextlib import contextmanager

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(DB_DIR, "hygiene_system.db")


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


@contextmanager
def get_db_cursor() -> Generator[sqlite3.Cursor, None, None]:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def initialize_database() -> None:
    """
    Creates tables and indices if they do not exist.
    """
    schema_sql = """
    CREATE TABLE IF NOT EXISTS facilities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        facility_type TEXT NOT NULL,
        license_number TEXT UNIQUE NOT NULL,
        address TEXT NOT NULL,
        contact_email TEXT,
        contact_phone TEXT,
        rating_grade TEXT DEFAULT 'Grade A',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS inspections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        facility_id INTEGER NOT NULL,
        inspector_name TEXT NOT NULL,
        inspection_date TEXT NOT NULL,
        inspection_type TEXT NOT NULL,
        temperature_compliance_score REAL NOT NULL,
        sanitation_protocol_score REAL NOT NULL,
        water_potability_index REAL NOT NULL,
        ppe_handwashing_score REAL NOT NULL,
        pest_control_score REAL NOT NULL,
        food_handler_cert_ratio REAL NOT NULL,
        structural_maintenance_score REAL NOT NULL,
        waste_management_score REAL NOT NULL,
        cross_contamination_control REAL NOT NULL,
        historical_violation_count INTEGER NOT NULL,
        ambient_kitchen_temp REAL NOT NULL,
        relative_humidity REAL NOT NULL,
        predicted_risk_level TEXT NOT NULL,
        predicted_risk_score REAL NOT NULL,
        hygiene_grade TEXT NOT NULL,
        confidence_percentage REAL NOT NULL,
        recommendations_json TEXT NOT NULL,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (facility_id) REFERENCES facilities (id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS remediation_actions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        inspection_id INTEGER NOT NULL,
        action_text TEXT NOT NULL,
        priority TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'PENDING',
        resolved_at TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (inspection_id) REFERENCES inspections (id) ON DELETE CASCADE
    );

    CREATE INDEX IF NOT EXISTS idx_inspections_facility_id ON inspections(facility_id);
    CREATE INDEX IF NOT EXISTS idx_inspections_risk_level ON inspections(predicted_risk_level);
    CREATE INDEX IF NOT EXISTS idx_facilities_type ON facilities(facility_type);
    CREATE INDEX IF NOT EXISTS idx_remediation_status ON remediation_actions(status);
    """

    with get_db_cursor() as cursor:
        cursor.executescript(schema_sql)
    print(f"Database schema initialized at: {DB_FILE}")


if __name__ == "__main__":
    initialize_database()

"""
Repository layer providing clean CRUD operations and aggregation queries for SQLite.
"""

import json
from typing import Dict, Any, List, Optional
try:
    from .db import get_db_cursor, get_db_connection
except (ImportError, ValueError):
    from db import get_db_cursor, get_db_connection


class HygieneRepository:
    """
    Data Access Object encapsulating database queries.
    """

    # --- Facilities ---
    @staticmethod
    def create_facility(data: Dict[str, Any]) -> int:
        query = """
        INSERT INTO facilities (name, facility_type, license_number, address, contact_email, contact_phone, rating_grade)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            data["name"],
            data["facility_type"],
            data["license_number"],
            data["address"],
            data.get("contact_email"),
            data.get("contact_phone"),
            data.get("rating_grade", "Grade A"),
        )
        with get_db_cursor() as cursor:
            cursor.execute(query, params)
            return cursor.lastrowid

    @staticmethod
    def get_facility_by_id(facility_id: int) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        row = conn.execute("SELECT * FROM facilities WHERE id = ?", (facility_id,)).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def get_all_facilities() -> List[Dict[str, Any]]:
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM facilities ORDER BY name ASC").fetchall()
        conn.close()
        return [dict(r) for r in rows]

    # --- Inspections ---
    @staticmethod
    def create_inspection(data: Dict[str, Any]) -> int:
        query = """
        INSERT INTO inspections (
            facility_id, inspector_name, inspection_date, inspection_type,
            temperature_compliance_score, sanitation_protocol_score, water_potability_index,
            ppe_handwashing_score, pest_control_score, food_handler_cert_ratio,
            structural_maintenance_score, waste_management_score, cross_contamination_control,
            historical_violation_count, ambient_kitchen_temp, relative_humidity,
            predicted_risk_level, predicted_risk_score, hygiene_grade, confidence_percentage,
            recommendations_json, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        recs = data.get("recommendations", [])
        recs_json = json.dumps(recs) if isinstance(recs, list) else str(recs)

        params = (
            data["facility_id"],
            data["inspector_name"],
            data["inspection_date"],
            data["inspection_type"],
            data["temperature_compliance_score"],
            data["sanitation_protocol_score"],
            data["water_potability_index"],
            data["ppe_handwashing_score"],
            data["pest_control_score"],
            data["food_handler_cert_ratio"],
            data["structural_maintenance_score"],
            data["waste_management_score"],
            data["cross_contamination_control"],
            data["historical_violation_count"],
            data["ambient_kitchen_temp"],
            data["relative_humidity"],
            data["predicted_risk_level"],
            data["predicted_risk_score"],
            data["hygiene_grade"],
            data["confidence_percentage"],
            recs_json,
            data.get("notes", ""),
        )

        with get_db_cursor() as cursor:
            cursor.execute(query, params)
            inspection_id = cursor.lastrowid

            # Update parent facility rating grade to match the latest inspection
            cursor.execute(
                "UPDATE facilities SET rating_grade = ? WHERE id = ?",
                (data["hygiene_grade"], data["facility_id"]),
            )

            # Insert remediation items if high/medium risk
            if isinstance(recs, list):
                for rec_text in recs:
                    priority = "ROUTINE"
                    if "CRITICAL" in rec_text.upper():
                        priority = "CRITICAL"
                    elif "URGENT" in rec_text.upper():
                        priority = "URGENT"
                    elif "PRIORITY" in rec_text.upper():
                        priority = "PRIORITY"
                    elif "SAFETY" in rec_text.upper():
                        priority = "SAFETY"

                    cursor.execute(
                        """
                        INSERT INTO remediation_actions (inspection_id, action_text, priority, status)
                        VALUES (?, ?, ?, 'PENDING')
                        """,
                        (inspection_id, rec_text, priority),
                    )

            return inspection_id

    @staticmethod
    def get_inspection_by_id(inspection_id: int) -> Optional[Dict[str, Any]]:
        conn = get_db_connection()
        query = """
        SELECT i.*, f.name AS facility_name, f.facility_type, f.license_number, f.address
        FROM inspections i
        JOIN facilities f ON i.facility_id = f.id
        WHERE i.id = ?
        """
        row = conn.execute(query, (inspection_id,)).fetchone()
        conn.close()
        if not row:
            return None
        item = dict(row)
        try:
            item["recommendations"] = json.loads(item["recommendations_json"])
        except Exception:
            item["recommendations"] = []
        return item

    @staticmethod
    def get_all_inspections(
        limit: int = 100,
        risk_filter: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        query = """
        SELECT i.*, f.name AS facility_name, f.facility_type, f.license_number
        FROM inspections i
        JOIN facilities f ON i.facility_id = f.id
        WHERE 1=1
        """
        params = []
        if risk_filter and risk_filter.lower() != "all":
            query += " AND i.predicted_risk_level = ?"
            params.append(risk_filter)

        if search:
            query += " AND (f.name LIKE ? OR f.license_number LIKE ? OR i.inspector_name LIKE ?)"
            term = f"%{search}%"
            params.extend([term, term, term])

        query += " ORDER BY i.id DESC LIMIT ?"
        params.append(limit)

        rows = conn.execute(query, tuple(params)).fetchall()
        conn.close()

        results = []
        for r in rows:
            d = dict(r)
            try:
                d["recommendations"] = json.loads(d["recommendations_json"])
            except Exception:
                d["recommendations"] = []
            results.append(d)
        return results

    @staticmethod
    def delete_inspection(inspection_id: int) -> bool:
        with get_db_cursor() as cursor:
            cursor.execute("DELETE FROM inspections WHERE id = ?", (inspection_id,))
            return cursor.rowcount > 0

    @staticmethod
    def get_system_stats() -> Dict[str, Any]:
        """
        Aggregates dashboard KPI metrics.
        """
        conn = get_db_connection()
        total_facilities = conn.execute("SELECT COUNT(*) FROM facilities").fetchone()[0]
        total_inspections = conn.execute("SELECT COUNT(*) FROM inspections").fetchone()[0]
        
        risk_counts = conn.execute("""
            SELECT predicted_risk_level, COUNT(*) 
            FROM inspections 
            GROUP BY predicted_risk_level
        """).fetchall()
        
        avg_score = conn.execute("SELECT AVG(predicted_risk_score) FROM inspections").fetchone()[0]
        
        pending_actions = conn.execute(
            "SELECT COUNT(*) FROM remediation_actions WHERE status = 'PENDING'"
        ).fetchone()[0]
        
        critical_alerts = conn.execute(
            "SELECT COUNT(*) FROM inspections WHERE predicted_risk_level = 'High Risk'"
        ).fetchone()[0]

        conn.close()

        risk_dist = {"Low Risk": 0, "Medium Risk": 0, "High Risk": 0}
        for level, count in risk_counts:
            if level in risk_dist:
                risk_dist[level] = count

        return {
            "total_facilities": total_facilities,
            "total_inspections": total_inspections,
            "risk_distribution": risk_dist,
            "average_risk_score": round(avg_score or 0.0, 1),
            "pending_remediation_actions": pending_actions,
            "critical_hazard_count": critical_alerts,
        }

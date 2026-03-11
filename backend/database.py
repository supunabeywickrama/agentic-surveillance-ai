import sqlite3
from typing import Dict, Any

class IncidentDatabase:
    def __init__(self, db_path="incidents.db"):
        self.db_path = db_path
        self._init_db()
        
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            event_type TEXT,
            location TEXT,
            risk_level TEXT,
            description TEXT
        )
        ''')
        conn.commit()
        conn.close()
        
    def insert_incident(self, incident: Dict[str, Any]):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO incidents (timestamp, event_type, location, risk_level, description)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            incident.get("timestamp"),
            incident.get("event_type"),
            incident.get("location", "Camera 1"),
            incident.get("risk_level"),
            incident.get("description")
        ))
        conn.commit()
        incident_id = cursor.lastrowid
        conn.close()
        return incident_id
        
    def get_all_incidents(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM incidents ORDER BY timestamp DESC')
        rows = cursor.fetchall()
        
        incidents = []
        for row in rows:
            incidents.append(dict(row))
            
        conn.close()
        return incidents

from datetime import datetime
from .database import get_db_connection

def mark_attendance(name: str):
    """Record attendance for a person"""
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO attendance (name, time) VALUES (?, ?)",
                    (name, datetime.now()))
        conn.commit()
    finally:
        conn.close()

def get_attendance_records(search_term: str = None):
    """Retrieve attendance records, optionally filtered by search term"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        if search_term:
            cursor.execute("SELECT * FROM attendance WHERE name LIKE ? ORDER BY time DESC",
                         (f"%{search_term}%",))
        else:
            cursor.execute("SELECT * FROM attendance ORDER BY time DESC")
        return cursor.fetchall()
    finally:
        conn.close()
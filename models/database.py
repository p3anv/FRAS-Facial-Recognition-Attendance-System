# attendance_system/models/database.py
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "attendance.db"

def init_db():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if table exists first
    cursor.execute("""SELECT name FROM sqlite_master 
                   WHERE type='table' AND name='attendance'""")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        cursor.execute('''CREATE TABLE attendance
                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        time TIMESTAMP)''')
        conn.commit()
        print("Database table created successfully")
    else:
        print("Database table already exists")
    
    conn.close()

def get_db_connection():
    """Return a new database connection"""
    return sqlite3.connect(DB_PATH)
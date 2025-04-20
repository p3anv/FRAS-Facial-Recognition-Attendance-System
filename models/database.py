import sqlite3
from pathlib import Path
from typing import Optional, List, Tuple

DB_PATH = Path(__file__).parent / "attendance.db"

def get_db_connection():
    """Return a new database connection"""
    return sqlite3.connect(DB_PATH)

def init_db():
    """
    Initialize the database with proper schema.
    Handles both new installations and upgrades.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON")
    
    # Create students table
    cursor.execute('''CREATE TABLE IF NOT EXISTS students
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    roll_number TEXT UNIQUE NOT NULL,
                    department TEXT NOT NULL)''')
    
    # Check if old attendance table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='attendance'")
    old_table_exists = cursor.fetchone()
    
    if old_table_exists:
        # Check if old table has roll_number column
        cursor.execute("PRAGMA table_info(attendance)")
        columns = [col[1] for col in cursor.fetchall()]
        has_roll_number = 'roll_number' in columns
        
        if not has_roll_number:
            # Migrate from old schema to new schema
            cursor.execute('''CREATE TABLE new_attendance
                           (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            roll_number TEXT,
                            name TEXT,
                            time TIMESTAMP,
                            FOREIGN KEY(roll_number) REFERENCES students(roll_number))''')
            
            # Try to match existing records with students
            cursor.execute('''INSERT INTO new_attendance (id, name, time)
                           SELECT a.id, a.name, a.time 
                           FROM attendance a''')
            
            cursor.execute("DROP TABLE attendance")
            cursor.execute("ALTER TABLE new_attendance RENAME TO attendance")
    else:
        # Create fresh attendance table with proper schema
        cursor.execute('''CREATE TABLE attendance
                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        roll_number TEXT,
                        name TEXT,
                        time TIMESTAMP,
                        FOREIGN KEY(roll_number) REFERENCES students(roll_number))''')
    
    conn.commit()
    conn.close()

def mark_attendance(roll_number: str, name: str) -> bool:
    """
    Record attendance for a student
    Returns True if successful, False otherwise
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        
        # Verify student exists
        cursor.execute("SELECT 1 FROM students WHERE roll_number = ?", (roll_number,))
        if not cursor.fetchone():
            raise ValueError(f"Student with roll number {roll_number} not found")
        
        # Record attendance
        cursor.execute('''INSERT INTO attendance (roll_number, name, time)
                       VALUES (?, ?, datetime('now'))''',
                       (roll_number, name))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        conn.close()

def get_student(roll_number: str) -> Optional[Tuple]:
    """Get student by roll number"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE roll_number = ?", (roll_number,))
        return cursor.fetchone()
    finally:
        conn.close()

def get_all_students() -> List[Tuple]:
    """Get all registered students"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students ORDER BY roll_number")
        return cursor.fetchall()
    finally:
        conn.close()

def get_attendance_records(search_term: str = None, limit: int = None) -> List[Tuple]:
    """
    Get attendance records with all required fields
    Args:
        search_term: Optional filter term
        limit: Maximum number of records to return
    Returns:
        List of tuples with (roll_no, first_name, last_name, department, timestamp)
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        query = '''SELECT 
                   s.roll_number, 
                   s.first_name, 
                   s.last_name, 
                   s.department, 
                   a.time 
                   FROM attendance a
                   JOIN students s ON a.roll_number = s.roll_number'''
        
        params = []
        if search_term:
            query += ''' WHERE s.roll_number LIKE ? 
                      OR s.first_name LIKE ? 
                      OR s.last_name LIKE ?
                      OR s.department LIKE ?'''
            params = [f"%{search_term}%"] * 4
        
        query += " ORDER BY a.time DESC"
        
        if limit:
            query += " LIMIT ?"
            params.append(limit)
        
        cursor.execute(query, params)
        return cursor.fetchall()
    finally:
        conn.close()

def add_student(first_name: str, last_name: str, roll_number: str, department: str) -> bool:
    """Add a new student to the database"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO students 
                       (first_name, last_name, roll_number, department)
                       VALUES (?, ?, ?, ?)''',
                       (first_name, last_name, roll_number, department))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print(f"Student with roll number {roll_number} already exists")
        return False
    finally:
        conn.close()

# Initialize database when module is imported
init_db()
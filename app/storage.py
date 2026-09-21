import sqlite3
from pathlib import Path

DB_PATH = Path("data/database.db")

def get_connection(db_path=None):
    target = db_path or DB_PATH
    return sqlite3.connect(target)

def init_db(db_path=None):

    conn = get_connection(db_path)

    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS projects(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS memories(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        entry_type TEXT,
        content TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS snapshots(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        memory_count INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

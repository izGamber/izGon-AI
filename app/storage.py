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
        importance INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS snapshots(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        memory_count INTEGER,
        snapshot_data TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Add snapshot_data column if it doesn't exist (migration)
    cur.execute("PRAGMA table_info(snapshots)")
    columns = [col[1] for col in cur.fetchall()]
    if 'snapshot_data' not in columns:
        try:
            cur.execute("ALTER TABLE snapshots ADD COLUMN snapshot_data TEXT")
        except:
            pass

    # Add importance column if it doesn't exist (migration for existing DBs)
    cur.execute("PRAGMA table_info(memories)")
    columns = [col[1] for col in cur.fetchall()]
    if 'importance' not in columns:
        try:
            cur.execute("ALTER TABLE memories ADD COLUMN importance INTEGER DEFAULT 1")
        except:
            pass

    conn.commit()
    conn.close()

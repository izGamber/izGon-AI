"""
Brain Engine - AI Memory System
Memorijsko-orijentisani AI sistem za čuvanje i recall-ovanje memorija
"""
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from app.storage import get_connection, DB_PATH


class BrainEngine:
    """Kompletna AI memorijska baza"""
    
    def __init__(self, db_path: str = str(DB_PATH)):
        self.db_path = db_path
        self._ensure_tables()
    
    def _ensure_tables(self):
        """Osiguraj da sve tabele postoje"""
        conn = get_connection(self.db_path)
        cur = conn.cursor()
        
        # Memorije tabela
        cur.execute("""
        CREATE TABLE IF NOT EXISTS memories(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            entry_type TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            importance INTEGER DEFAULT 1
        )
        """)
        
        # Snapshots tabela
        cur.execute("""
        CREATE TABLE IF NOT EXISTS snapshots(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            memory_count INTEGER,
            snapshot_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        conn.commit()
        conn.close()
    
    def remember(self, project_id: int, memory_type: str, content: str, importance: int = 1) -> Dict:
        """
        Čuva novu memoriju u bazu
        
        memory_type: 'note', 'learning', 'insight', 'error', 'solution'
        importance: 1-5 (1=low, 5=critical)
        """
        conn = get_connection(self.db_path)
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO memories (project_id, entry_type, content, importance)
            VALUES (?, ?, ?, ?)
        """, (project_id, memory_type, content, importance))
        
        conn.commit()
        memory_id = cur.lastrowid
        conn.close()
        
        return {
            "status": "remembered",
            "memory_id": memory_id,
            "timestamp": datetime.now().isoformat()
        }
    
    def recall(self, project_id: int, limit: int = 20, memory_type: Optional[str] = None) -> List[Dict]:
        """
        Vraćaj relevantne memorije
        Sortira po važnosti i vremenu
        """
        conn = get_connection(self.db_path)
        cur = conn.cursor()
        
        if memory_type:
            cur.execute("""
                SELECT id, project_id, entry_type, content, created_at, importance
                FROM memories 
                WHERE project_id = ? AND entry_type = ?
                ORDER BY importance DESC, created_at DESC
                LIMIT ?
            """, (project_id, memory_type, limit))
        else:
            cur.execute("""
                SELECT id, project_id, entry_type, content, created_at, importance
                FROM memories 
                WHERE project_id = ?
                ORDER BY importance DESC, created_at DESC
                LIMIT ?
            """, (project_id, limit))
        
        memories = cur.fetchall()
        conn.close()
        
        return [
            {
                "id": m[0],
                "project_id": m[1],
                "type": m[2],
                "content": m[3],
                "timestamp": m[4],
                "importance": m[5]
            }
            for m in memories
        ]
    
    def take_snapshot(self, project_id: int) -> Dict:
        """
        Pravi snimak svih memorija projekta
        Za vraćanje stanja kasnije
        """
        memories = self.recall(project_id, limit=1000)
        memory_count = len(memories)
        
        conn = get_connection(self.db_path)
        cur = conn.cursor()
        
        import json
        snapshot_data = json.dumps(memories)
        
        cur.execute("""
            INSERT INTO snapshots (project_id, memory_count, snapshot_data)
            VALUES (?, ?, ?)
        """, (project_id, memory_count, snapshot_data))
        
        conn.commit()
        snapshot_id = cur.lastrowid
        conn.close()
        
        return {
            "status": "snapshot_created",
            "snapshot_id": snapshot_id,
            "memory_count": memory_count,
            "timestamp": datetime.now().isoformat()
        }
    
    def restore_snapshot(self, snapshot_id: int) -> Dict:
        """Vrati memorije iz prethodnog snapshota"""
        conn = get_connection(self.db_path)
        cur = conn.cursor()
        
        cur.execute("""
            SELECT snapshot_data FROM snapshots WHERE id = ?
        """, (snapshot_id,))
        
        result = cur.fetchone()
        conn.close()
        
        if not result:
            return {"error": "Snapshot not found"}
        
        import json
        memories = json.loads(result[0])
        
        return {
            "status": "snapshot_restored",
            "snapshot_id": snapshot_id,
            "memories_count": len(memories),
            "memories": memories
        }
    
    def get_brain_stats(self, project_id: int) -> Dict:
        """Vrati statistiku mozga"""
        conn = get_connection(self.db_path)
        cur = conn.cursor()
        
        # Ukupne memorije
        cur.execute("SELECT COUNT(*) FROM memories WHERE project_id = ?", (project_id,))
        total_memories = cur.fetchone()[0]
        
        # Po tipovima
        cur.execute("""
            SELECT entry_type, COUNT(*) 
            FROM memories 
            WHERE project_id = ?
            GROUP BY entry_type
        """, (project_id,))
        memory_types = dict(cur.fetchall())
        
        # Snapshots
        cur.execute("SELECT COUNT(*) FROM snapshots WHERE project_id = ?", (project_id,))
        snapshot_count = cur.fetchone()[0]
        
        # Važne memorije
        cur.execute("""
            SELECT COUNT(*) FROM memories 
            WHERE project_id = ? AND importance >= 4
        """, (project_id,))
        critical_memories = cur.fetchone()[0]
        
        conn.close()
        
        return {
            "total_memories": total_memories,
            "memory_types": memory_types,
            "snapshot_count": snapshot_count,
            "critical_memories": critical_memories,
            "brain_health": "optimal" if total_memories > 0 else "needs_learning"
        }
    
    def search_memories(self, project_id: int, keyword: str) -> List[Dict]:
        """Pretraži memorije po ključnoj reči"""
        conn = get_connection(self.db_path)
        cur = conn.cursor()
        
        cur.execute("""
            SELECT id, project_id, entry_type, content, created_at, importance
            FROM memories 
            WHERE project_id = ? AND content LIKE ?
            ORDER BY importance DESC, created_at DESC
        """, (project_id, f"%{keyword}%"))
        
        memories = cur.fetchall()
        conn.close()
        
        return [
            {
                "id": m[0],
                "project_id": m[1],
                "type": m[2],
                "content": m[3],
                "timestamp": m[4],
                "importance": m[5]
            }
            for m in memories
        ]
    
    def forget(self, memory_id: int) -> Dict:
        """Ukloni memoriju"""
        conn = get_connection(self.db_path)
        cur = conn.cursor()
        
        cur.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
        conn.commit()
        conn.close()
        
        return {
            "status": "memory_deleted",
            "memory_id": memory_id
        }
    
    def update_memory_importance(self, memory_id: int, importance: int) -> Dict:
        """Ažuriraj važnost memorije"""
        if not 1 <= importance <= 5:
            return {"error": "Importance must be between 1 and 5"}
        
        conn = get_connection(self.db_path)
        cur = conn.cursor()
        
        cur.execute("""
            UPDATE memories 
            SET importance = ?
            WHERE id = ?
        """, (importance, memory_id))
        
        conn.commit()
        conn.close()
        
        return {
            "status": "importance_updated",
            "memory_id": memory_id,
            "importance": importance
        }

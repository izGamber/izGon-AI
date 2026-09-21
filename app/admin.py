"""
Admin funkcionalnosti - čišćenje, export, backup
"""
import json
import sqlite3
from datetime import datetime
from pathlib import Path
from app.storage import get_connection, DB_PATH

class AdminManager:
    """Admin operacije"""
    
    def __init__(self):
        self.db_path = DB_PATH
        self.backups_dir = Path("data/backups")
        self.backups_dir.mkdir(exist_ok=True)
    
    def delete_all_memories(self, project_id: int) -> dict:
        """Obriši sve memorije za projekat"""
        conn = get_connection(str(self.db_path))
        cur = conn.cursor()
        
        cur.execute("DELETE FROM memories WHERE project_id = ?", (project_id,))
        deleted = cur.rowcount
        
        conn.commit()
        conn.close()
        
        return {
            "status": "deleted",
            "count": deleted,
            "message": f"Obrisano {deleted} memorija"
        }
    
    def export_all_data(self, project_id: int) -> dict:
        """Eksportuj sve podatke projekta"""
        conn = get_connection(str(self.db_path))
        cur = conn.cursor()
        
        # Vrati projekat
        cur.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        project = cur.fetchone()
        
        # Vrati memorije
        cur.execute("SELECT * FROM memories WHERE project_id = ?", (project_id,))
        memories = cur.fetchall()
        
        # Vrati snapshots
        cur.execute("SELECT * FROM snapshots WHERE project_id = ?", (project_id,))
        snapshots = cur.fetchall()
        
        conn.close()
        
        return {
            "project": {
                "id": project[0],
                "name": project[1],
                "description": project[2]
            } if project else None,
            "memories": [
                {
                    "id": m[0],
                    "type": m[2],
                    "content": m[3],
                    "created_at": m[4],
                    "importance": m[5]
                }
                for m in memories
            ],
            "snapshots": len(snapshots),
            "export_date": datetime.now().isoformat()
        }
    
    def import_data(self, data: dict, project_id: int) -> dict:
        """Importuj podatke"""
        conn = get_connection(str(self.db_path))
        cur = conn.cursor()
        
        imported = 0
        
        # Importuj memorije
        for memory in data.get("memories", []):
            cur.execute("""
                INSERT INTO memories (project_id, entry_type, content, importance)
                VALUES (?, ?, ?, ?)
            """, (
                project_id,
                memory["type"],
                memory["content"],
                memory.get("importance", 1)
            ))
            imported += 1
        
        conn.commit()
        conn.close()
        
        return {
            "status": "imported",
            "count": imported,
            "message": f"Importovano {imported} memorija"
        }
    
    def create_backup(self, project_id: int) -> dict:
        """Kreiraj backup"""
        data = self.export_all_data(project_id)
        
        backup_name = f"backup-{project_id}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
        backup_path = self.backups_dir / backup_name
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return {
            "status": "created",
            "backup_id": backup_name,
            "size": backup_path.stat().st_size,
            "timestamp": datetime.now().isoformat()
        }
    
    def list_backups(self, project_id: int) -> list:
        """Vrati sve backupe"""
        backups = []
        
        for backup_file in self.backups_dir.glob(f"backup-{project_id}-*.json"):
            stat = backup_file.stat()
            backups.append({
                "id": backup_file.name,
                "date": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "size": stat.st_size
            })
        
        return sorted(backups, key=lambda x: x["date"], reverse=True)
    
    def restore_backup(self, backup_id: str, project_id: int) -> dict:
        """Vrati backup"""
        backup_path = self.backups_dir / backup_id
        
        if not backup_path.exists():
            return {"error": "Backup not found"}
        
        with open(backup_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Obriši stare memorije
        self.delete_all_memories(project_id)
        
        # Importuj iz backupa
        result = self.import_data(data, project_id)
        
        return {
            "status": "restored",
            "backup_id": backup_id,
            "memories_restored": result["count"]
        }
    
    def get_stats(self) -> dict:
        """Vrati admin statistiku"""
        conn = get_connection(str(self.db_path))
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*) FROM projects")
        projects = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM memories")
        memories = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM snapshots")
        snapshots = cur.fetchone()[0]
        
        cur.execute("SELECT SUM(memory_count) FROM snapshots")
        total_backed_up = cur.fetchone()[0] or 0
        
        conn.close()
        
        return {
            "projects": projects,
            "memories": memories,
            "snapshots": snapshots,
            "total_backed_up": total_backed_up,
            "db_path": str(self.db_path),
            "db_size": self.db_path.stat().st_size if self.db_path.exists() else 0
        }

# Globalna instanca
admin_manager = AdminManager()

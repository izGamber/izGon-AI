"""
izGon AI - FastAPI Backend
Brain Engine sa WebSocket real-time komunikacijom
"""

from fastapi import FastAPI, WebSocket, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from starlette.websockets import WebSocketDisconnect
import socketio
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict

from app.brain import BrainEngine
from app.storage import init_db, get_connection

# ===== SETUP =====
app = FastAPI(
    title="IZgoN AI",
    description="Advanced AI Brain System sa Memory Management",
    version="1.0.0"
)

# Socket.IO setup za real-time komunikaciju
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',
    ping_timeout=60,
    ping_interval=25
)

# Asgi app sa Socket.IO
asgi_app = socketio.ASGIApp(sio, app)

# Templates i static fajlovi
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Inicijalizuj bazu PRVO
init_db()

# Brain Engine
brain = BrainEngine()

# ===== WEBSOCKET EVENTS =====
@sio.event
async def connect(sid, environ):
    print(f"✅ Klijent konektovan: {sid}")

@sio.event
async def disconnect(sid):
    print(f"❌ Klijent diskonektovan: {sid}")

@sio.event
async def memory_added(sid, data):
    """Emituj svim klijentima da je memorija dodana"""
    await sio.emit('memory_added', data, to=None)

@sio.event
async def snapshot_created(sid, data):
    """Emituj svim klijentima da je snapshot kreiran"""
    await sio.emit('snapshot_created', data, to=None)

# ===== HTML ROUTES =====
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page sa dashboard-om"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# ===== BRAIN API ENDPOINTS =====
@app.get("/api/brain/stats")
async def get_brain_stats():
    """Vrati statistiku mozga"""
    # Koristi project_id=1 kao default
    stats = brain.get_brain_stats(project_id=1)
    return stats

@app.post("/api/brain/remember")
async def remember(
    content: str = Query(...),
    memory_type: str = Query("note"),
    importance: int = Query(3),
    project_id: int = Query(1)
):
    """
    Dodaj novu memoriju
    
    memory_type opcije: 'note', 'learning', 'insight', 'error', 'solution'
    importance: 1-5
    """
    result = brain.remember(
        project_id=project_id,
        memory_type=memory_type,
        content=content,
        importance=min(5, max(1, importance))
    )
    
    # Emit kroz Socket.IO svim klijentima
    await sio.emit('memory_added', result, to=None)
    
    return result

@app.get("/api/brain/memories")
async def get_memories(
    limit: int = Query(20),
    memory_type: str = Query(None),
    project_id: int = Query(1)
):
    """Vrati sve memorije sa opcionalnim filterima"""
    memories = brain.recall(
        project_id=project_id,
        limit=limit,
        memory_type=memory_type
    )
    return {
        "memories": memories,
        "count": len(memories),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/brain/search")
async def search_memories(
    keyword: str = Query(...),
    project_id: int = Query(1)
):
    """Pretraži memorije po ključnoj reči"""
    results = brain.search_memories(
        project_id=project_id,
        keyword=keyword
    )
    return {
        "keyword": keyword,
        "results": results,
        "count": len(results)
    }

@app.post("/api/brain/snapshot")
async def create_snapshot(project_id: int = Query(1)):
    """Kreiraj snapshot trenutnog stanja memorija"""
    result = brain.take_snapshot(project_id=project_id)
    
    # Emit event
    await sio.emit('snapshot_created', result, to=None)
    
    return result

@app.post("/api/brain/snapshot/{snapshot_id}")
async def restore_snapshot(snapshot_id: int):
    """Vrati stanje iz snapshota"""
    result = brain.restore_snapshot(snapshot_id)
    
    # Emit event
    await sio.emit('snapshot_restored', {"snapshot_id": snapshot_id}, to=None)
    
    return result

@app.delete("/api/brain/forget/{memory_id}")
async def delete_memory(memory_id: int):
    """Obriši memoriju"""
    result = brain.forget(memory_id)
    
    # Emit event
    await sio.emit('memory_deleted', {"memory_id": memory_id}, to=None)
    
    return result

@app.patch("/api/brain/importance/{memory_id}")
async def update_importance(
    memory_id: int,
    importance: int = Query(3)
):
    """Ažuriraj važnost memorije"""
    result = brain.update_memory_importance(memory_id, importance)
    
    # Emit event
    await sio.emit('importance_updated', result, to=None)
    
    return result

# ===== ACTIVITY API =====
@app.get("/api/activities")
async def get_activities(project_id: int = Query(1), limit: int = Query(10)):
    """Vrati nedavnu aktivnost"""
    memories = brain.recall(project_id=project_id, limit=limit)
    
    activities = [
        {
            "id": m["id"],
            "type": m["type"],
            "title": f"Nova {m['type']}: {m['content'][:50]}...",
            "content": m["content"],
            "timestamp": m["timestamp"],
            "importance": m["importance"]
        }
        for m in memories
    ]
    
    return activities

# ===== PROJECTS API =====
@app.get("/api/projects")
async def get_projects():
    """Vrati sve projekte"""
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT id, name, description FROM projects
    """)
    
    projects = []
    for row in cur.fetchall():
        project_id = row[0]
        stats = brain.get_brain_stats(project_id)
        projects.append({
            "id": project_id,
            "name": row[1],
            "description": row[2],
            "memories": stats["total_memories"],
            "snapshots": stats["snapshot_count"]
        })
    
    conn.close()
    
    return {
        "projects": projects,
        "count": len(projects)
    }

@app.post("/api/projects")
async def create_project(name: str = Query(...), description: str = Query("")):
    """Kreiraj novi projekat"""
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO projects (name, description)
        VALUES (?, ?)
    """, (name, description))
    
    conn.commit()
    project_id = cur.lastrowid
    conn.close()
    
    # Emit event
    await sio.emit('project_created', {
        "id": project_id,
        "name": name
    }, to=None)
    
    return {
        "status": "project_created",
        "project_id": project_id,
        "name": name
    }

# ===== ADMIN ENDPOINTS =====
@app.post("/api/admin/reset-brain")
async def reset_brain(project_id: int = Query(1)):
    """Resetuj brain za projekat (OPASNO!)"""
    conn = get_connection()
    cur = conn.cursor()
    
    # Obriši sve memorije i snapshote
    cur.execute("DELETE FROM memories WHERE project_id = ?", (project_id,))
    cur.execute("DELETE FROM snapshots WHERE project_id = ?", (project_id,))
    
    conn.commit()
    conn.close()
    
    # Emit event
    await sio.emit('brain_reset', {"project_id": project_id}, to=None)
    
    return {
        "status": "brain_reset",
        "project_id": project_id
    }

@app.get("/api/admin/db-info")
async def get_db_info():
    """Vrati informacije o bazi"""
    conn = get_connection()
    cur = conn.cursor()
    
    # Statistika po tabelama
    cur.execute("SELECT COUNT(*) FROM projects")
    projects_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM memories")
    memories_count = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM snapshots")
    snapshots_count = cur.fetchone()[0]
    
    conn.close()
    
    return {
        "database": "SQLite",
        "tables": {
            "projects": projects_count,
            "memories": memories_count,
            "snapshots": snapshots_count
        },
        "total_records": projects_count + memories_count + snapshots_count
    }

# ===== ERROR HANDLERS =====
@app.exception_handler(Exception)
async def universal_exception_handler(request: Request, exc: Exception):
    return {
        "error": str(exc),
        "timestamp": datetime.now().isoformat()
    }

# ===== SERVER INFO =====
@app.get("/api/info")
async def get_info():
    """Vrati info o serveru"""
    return {
        "name": "IZgoN AI",
        "version": "1.0.0",
        "description": "Advanced AI Brain System",
        "features": [
            "Memory Management",
            "Brain Engine",
            "Real-time WebSockets",
            "Project Management",
            "Snapshot System"
        ],
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }

# ===== STARTUP EVENT =====
@app.on_event("startup")
async def startup():
    """Inicijalizuj pri startu"""
    print("✅ izGon AI pokrenut!")
    print("📊 Dashboard: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(asgi_app, host="0.0.0.0", port=8000)

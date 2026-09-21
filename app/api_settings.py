"""
Settings API endpoints za izGon-AI
"""

from fastapi import APIRouter, Query
from app.settings import settings_manager
import json
from pathlib import Path

router = APIRouter(prefix="/api/settings", tags=["settings"])

@router.get("/")
async def get_all_settings():
    """Vrati sve postavke"""
    return settings_manager.get_all()

@router.get("/{key}")
async def get_setting(key: str):
    """Vrati specifičnu postavku"""
    value = settings_manager.get(key)
    if value is None:
        return {"error": f"Setting '{key}' not found"}
    return {key: value}

@router.post("/update")
async def update_setting(key: str = Query(...), value: str = Query(...)):
    """Ažuriraj postavku"""
    try:
        # Konvertuj vrednost u odgovarajući tip
        if value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False
        elif value.isdigit():
            value = int(value)
        
        settings_manager.set(key, value)
        return {"status": "updated", "key": key, "value": value}
    except Exception as e:
        return {"error": str(e)}

@router.post("/model")
async def toggle_ai_model(model: str = Query(...), enabled: bool = Query(...)):
    """Aktiviraj/deaktiviraj AI model"""
    settings_manager.update_ai_model(model, enabled)
    return {
        "status": "updated",
        "model": model,
        "enabled": enabled
    }

@router.get("/models/active")
async def get_active_models():
    """Vrati samo aktivne AI modele"""
    return {
        "active_models": settings_manager.get_active_models()
    }

@router.post("/reset")
async def reset_to_default():
    """Resetuj sve postavke na default"""
    settings_manager.reset_to_default()
    return {"status": "reset", "message": "Sve postavke resetovane na default"}

@router.post("/export")
async def export_settings():
    """Eksportuj sve postavke"""
    return settings_manager.get_all()

@router.post("/import")
async def import_settings(data: dict):
    """Importuj postavke"""
    try:
        for key, value in data.items():
            settings_manager.set(key, value)
        return {"status": "imported"}
    except Exception as e:
        return {"error": str(e)}

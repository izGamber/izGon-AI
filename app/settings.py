"""
Settings - Konfiguracija izGon-AI
"""
from pathlib import Path
import json
from typing import Dict, Any

SETTINGS_FILE = Path("data/settings.json")

DEFAULT_SETTINGS = {
    "app_name": "izGon AI",
    "version": "1.0.0",
    "theme": "light",
    "auto_backup": True,
    "backup_interval": 60,  # minuta
    "max_memories": 10000,
    "enable_notifications": True,
    "enable_analytics": False,
    "language": "sr",
    "ai_models": [
        {"name": "GPT-4", "enabled": True},
        {"name": "Claude", "enabled": True},
        {"name": "Gemini", "enabled": True},
        {"name": "Custom API", "enabled": False}
    ],
    "memory_retention_days": 365,
    "export_format": "json",
    "api_key": None,
    "pricing_tier": "free",
}

class SettingsManager:
    """Upravljanje podešavanjima"""
    
    def __init__(self):
        self.settings = self._load_settings()
    
    def _load_settings(self) -> Dict[str, Any]:
        """Učitaj settings ili kreiraj default"""
        if SETTINGS_FILE.exists():
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return DEFAULT_SETTINGS.copy()
    
    def save(self):
        """Sačuvaj settings"""
        SETTINGS_FILE.parent.mkdir(exist_ok=True)
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.settings, f, indent=2, ensure_ascii=False)
    
    def get(self, key: str, default=None):
        """Vrati setting"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """Postavi setting"""
        self.settings[key] = value
        self.save()
    
    def get_all(self) -> Dict[str, Any]:
        """Vrati sve settings"""
        return self.settings.copy()
    
    def reset_to_default(self):
        """Resetuj na default"""
        self.settings = DEFAULT_SETTINGS.copy()
        self.save()
    
    def update_ai_model(self, model_name: str, enabled: bool):
        """Ažuriraj AI model status"""
        for model in self.settings["ai_models"]:
            if model["name"] == model_name:
                model["enabled"] = enabled
                break
        self.save()
    
    def get_active_models(self):
        """Vrati samo aktivne modele"""
        return [m for m in self.settings["ai_models"] if m["enabled"]]

# Globalna instanca
settings_manager = SettingsManager()

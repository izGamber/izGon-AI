"""
Kompletan test set za izGon AI aplikaciju
Testira sve glavne funkcionalnosti
"""
import pytest
from app.brain import BrainEngine
from app.settings import SettingsManager
from app.admin import AdminManager
from app.storage import init_db, get_connection
import tempfile
import os
import json


class TestBrainEngine:
    """Testovi za Brain Engine - AI Memory System"""
    
    @pytest.fixture
    def temp_db(self):
        fd, path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        yield path
        os.unlink(path)
    
    @pytest.fixture
    def brain(self, temp_db):
        init_db(temp_db)
        return BrainEngine(temp_db)
    
    def test_remember_memory(self, brain):
        """Test: Dodavanje memorije"""
        result = brain.remember(1, "note", "Test memorija", 3)
        assert result["status"] == "remembered"
        assert result["memory_id"] is not None
        print("✓ Memorija dodana")
    
    def test_recall_memories(self, brain):
        """Test: Vraćanje memorija"""
        brain.remember(1, "note", "Test 1", 3)
        brain.remember(1, "learning", "Test 2", 4)
        brain.remember(1, "insight", "Test 3", 5)
        
        memories = brain.recall(1)
        assert len(memories) == 3
        assert memories[0]["importance"] == 5  # Sortiran po važnosti
        print("✓ Memorije vraćene sa sortiranjem")
    
    def test_search_memories(self, brain):
        """Test: Pretraga memorija"""
        brain.remember(1, "note", "Python je lep jezik", 3)
        brain.remember(1, "note", "Docker je odličan", 3)
        brain.remember(1, "note", "Python + Docker", 5)
        
        results = brain.search_memories(1, "Python")
        assert len(results) == 2
        print("✓ Pretraga memorija radi")
    
    def test_snapshot_creation(self, brain):
        """Test: Pravljenje snapshota"""
        brain.remember(1, "note", "Test 1", 3)
        brain.remember(1, "learning", "Test 2", 4)
        
        snapshot = brain.take_snapshot(1)
        assert snapshot["status"] == "snapshot_created"
        assert snapshot["memory_count"] == 2
        print("✓ Snapshot kreiran")
    
    def test_snapshot_restore(self, brain):
        """Test: Vraćanje snapshota"""
        brain.remember(1, "note", "Test", 3)
        snapshot = brain.take_snapshot(1)
        
        restored = brain.restore_snapshot(snapshot["snapshot_id"])
        assert restored["status"] == "snapshot_restored"
        assert restored["memories_count"] == 1
        print("✓ Snapshot vraćen")
    
    def test_memory_importance_update(self, brain):
        """Test: Ažuriranje važnosti memorije"""
        result = brain.remember(1, "note", "Test", 1)
        memory_id = result["memory_id"]
        
        brain.update_memory_importance(memory_id, 5)
        memories = brain.recall(1)
        assert memories[0]["importance"] == 5
        print("✓ Važnost memorije ažurirana")
    
    def test_delete_memory(self, brain):
        """Test: Brisanje memorije"""
        result = brain.remember(1, "note", "Test", 3)
        memory_id = result["memory_id"]
        
        brain.forget(memory_id)
        memories = brain.recall(1)
        assert len(memories) == 0
        print("✓ Memorija obrisana")
    
    def test_memory_types(self, brain):
        """Test: Različiti tipovi memorija"""
        types = ["note", "learning", "insight", "error", "solution"]
        
        for mtype in types:
            brain.remember(1, mtype, f"Test {mtype}", 3)
        
        memories = brain.recall(1, limit=100)
        assert len(memories) == 5
        print("✓ Svi tipovi memorija rade")
    
    def test_brain_stats(self, brain):
        """Test: Brain statistika"""
        brain.remember(1, "note", "Test 1", 3)
        brain.remember(1, "learning", "Test 2", 4)
        brain.remember(1, "error", "Test 3", 5)
        
        stats = brain.get_brain_stats(1)
        assert stats["total_memories"] == 3
        assert "note" in stats["memory_types"]
        assert stats["brain_health"] == "optimal"
        print("✓ Brain statistika radi")


class TestSettings:
    """Testovi za Settings sistem"""
    
    def test_get_all_settings(self):
        """Test: Čitanje svih postavki"""
        settings = SettingsManager()
        all_settings = settings.get_all()
        
        assert "app_name" in all_settings
        assert all_settings["app_name"] == "izGon AI"
        print("✓ Sve postavke učitane")
    
    def test_set_setting(self):
        """Test: Postavljanje vrednosti"""
        settings = SettingsManager()
        settings.set("theme", "dark")
        
        value = settings.get("theme")
        assert value == "dark"
        print("✓ Postavka sačuvana")
    
    def test_ai_model_toggle(self):
        """Test: Aktivacija/deaktivacija AI modela"""
        settings = SettingsManager()
        
        settings.update_ai_model("GPT-4", True)
        active = settings.get_active_models()
        
        assert len(active) > 0
        print("✓ AI model toggle radi")
    
    def test_reset_to_default(self):
        """Test: Resetovanje na default"""
        settings = SettingsManager()
        settings.set("theme", "dark")
        settings.reset_to_default()
        
        value = settings.get("theme")
        assert value == "light"
        print("✓ Reset na default radi")


class TestAdmin:
    """Testovi za Admin funkcionalnosti"""
    
    @pytest.fixture
    def temp_db(self):
        fd, path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        yield path
        os.unlink(path)
    
    @pytest.fixture
    def admin(self, temp_db):
        init_db(temp_db)
        brain = BrainEngine(temp_db)
        brain.remember(1, "note", "Test 1", 3)
        brain.remember(1, "learning", "Test 2", 4)
        
        admin = AdminManager()
        admin.db_path = temp_db
        return admin, brain
    
    def test_export_all_data(self, admin):
        """Test: Export svih podataka"""
        admin_mgr, brain = admin
        
        data = admin_mgr.export_all_data(1)
        assert "memories" in data
        assert len(data["memories"]) == 2
        print("✓ Export podataka radi")
    
    def test_create_backup(self, admin):
        """Test: Pravljenje backupa"""
        admin_mgr, brain = admin
        
        backup = admin_mgr.create_backup(1)
        assert backup["status"] == "created"
        assert backup["backup_id"] is not None
        print("✓ Backup kreiran")
    
    def test_list_backups(self, admin):
        """Test: Listanje backupa"""
        admin_mgr, brain = admin
        
        admin_mgr.create_backup(1)
        backups = admin_mgr.list_backups(1)
        
        assert len(backups) > 0
        print("✓ Backup lista radi")


class TestIntegration:
    """Integracijski testovi - kompletan workflow"""
    
    @pytest.fixture
    def temp_db(self):
        fd, path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        yield path
        os.unlink(path)
    
    def test_complete_workflow(self, temp_db):
        """Test: Kompletan workflow od start do kraja"""
        init_db(temp_db)
        brain = BrainEngine(temp_db)
        admin = AdminManager()
        admin.db_path = temp_db
        
        # Dodaj memorije
        brain.remember(1, "note", "Rad na AI projektu", 5)
        brain.remember(1, "learning", "Naučio o memoriji", 4)
        brain.remember(1, "insight", "AI radi bolje sa kontekstom", 5)
        
        # Vrati memorije
        memories = brain.recall(1)
        assert len(memories) == 3
        
        # Kreiraj snapshot
        snapshot = brain.take_snapshot(1)
        assert snapshot["memory_count"] == 3
        
        # Pretraži
        results = brain.search_memories(1, "AI")
        assert len(results) > 0
        
        # Export
        data = admin.export_all_data(1)
        assert len(data["memories"]) == 3
        
        print("✓ Kompletan workflow prošao sve testove")
    
    def test_performance(self, temp_db):
        """Test: Performanse sa puno memorija"""
        init_db(temp_db)
        brain = BrainEngine(temp_db)
        
        # Dodaj 1000 memorija
        for i in range(1000):
            brain.remember(1, "note", f"Memorija {i}", (i % 5) + 1)
        
        # Vrati sve
        memories = brain.recall(1, limit=1000)
        assert len(memories) == 1000
        
        # Pretraži
        results = brain.search_memories(1, "Memorija")
        assert len(results) > 0
        
        print("✓ Performanse su dobre sa 1000 memorija")


# Test Runner
if __name__ == "__main__":
    import sys
    
    print("\n" + "="*60)
    print("🧠 izGon AI - KOMPLETAN TEST SET")
    print("="*60 + "\n")
    
    # Pokreni sve testove
    pytest.main([__file__, "-v", "--tb=short"])
    
    print("\n" + "="*60)
    print("✅ TESTIRANJE ZAVRŠENO")
    print("="*60 + "\n")

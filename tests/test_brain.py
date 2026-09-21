"""
Test fajl za izGon AI
"""
import pytest
from app.brain import BrainEngine
from app.storage import init_db, get_connection
import tempfile
import os


@pytest.fixture
def temp_db():
    """Kreiraj privremenu bazu za testove"""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    yield path
    os.unlink(path)


@pytest.fixture
def brain(temp_db):
    """Kreiraj Brain Engine instancu"""
    init_db(temp_db)
    return BrainEngine(temp_db)


class TestBrainEngine:
    """Testovi za Brain Engine"""
    
    def test_remember(self, brain):
        """Test dodavanja memorije"""
        result = brain.remember(
            project_id=1,
            memory_type="note",
            content="Test memorija",
            importance=3
        )
        
        assert result["status"] == "remembered"
        assert result["memory_id"] is not None
    
    def test_recall(self, brain):
        """Test vraćanja memorija"""
        # Dodaj memorije
        brain.remember(1, "note", "Test 1", 3)
        brain.remember(1, "note", "Test 2", 4)
        
        # Vrati memorije
        memories = brain.recall(1)
        
        assert len(memories) == 2
        assert memories[0]["importance"] == 4  # Viša važnost prvo
    
    def test_search(self, brain):
        """Test pretrage memorija"""
        brain.remember(1, "note", "Python je lep", 3)
        brain.remember(1, "note", "Docker je cool", 3)
        brain.remember(1, "note", "Python + Docker", 3)
        
        results = brain.search_memories(1, "Python")
        
        assert len(results) == 2
    
    def test_snapshot(self, brain):
        """Test snapshot sistema"""
        # Dodaj memorije
        brain.remember(1, "note", "Test 1", 3)
        brain.remember(1, "note", "Test 2", 4)
        
        # Kreiraj snapshot
        snapshot = brain.take_snapshot(1)
        
        assert snapshot["status"] == "snapshot_created"
        assert snapshot["memory_count"] == 2
    
    def test_brain_stats(self, brain):
        """Test brain statistike"""
        # Dodaj različite memorije
        brain.remember(1, "note", "Test 1", 3)
        brain.remember(1, "learning", "Test 2", 4)
        brain.remember(1, "insight", "Test 3", 5)
        
        stats = brain.get_brain_stats(1)
        
        assert stats["total_memories"] == 3
        assert "note" in stats["memory_types"]
        assert "learning" in stats["memory_types"]
    
    def test_delete_memory(self, brain):
        """Test brisanja memorije"""
        result = brain.remember(1, "note", "Test", 3)
        memory_id = result["memory_id"]
        
        # Obriši
        brain.forget(memory_id)
        
        # Proveri da je obrisana
        memories = brain.recall(1)
        assert len(memories) == 0
    
    def test_importance_update(self, brain):
        """Test ažuriranja važnosti"""
        result = brain.remember(1, "note", "Test", 1)
        memory_id = result["memory_id"]
        
        # Ažuriraj
        brain.update_memory_importance(memory_id, 5)
        
        # Proveri
        memories = brain.recall(1)
        assert memories[0]["importance"] == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

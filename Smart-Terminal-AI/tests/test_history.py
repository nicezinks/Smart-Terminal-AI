"""
Testes para o sistema de histórico.
"""

import tempfile

import pytest

from core.history import History

class TestHistory:
   

    def test_history_add(self):
        """Deve adicionar entrada ao histórico."""
        with tempfile.TemporaryDirectory() as tmpdir:
            hist = History(history_path=f"{tmpdir}/history.json")
            hist.add("pergunta", "resposta", [], 1.5, 3)
            assert len(hist.get_all()) == 1

    def test_history_recent(self):
       
        with tempfile.TemporaryDirectory() as tmpdir:
            hist = History(history_path=f"{tmpdir}/history.json")
            for i in range(5):
                hist.add(f"q{i}", f"r{i}", [], 1.0, 1)
            recent = hist.get_recent(limit=3)
            assert len(recent) == 3

    def test_history_search(self):
    
        with tempfile.TemporaryDirectory() as tmpdir:
            hist = History(history_path=f"{tmpdir}/history.json")
            hist.add("python programming", "resposta", [], 1.0, 1)
            hist.add("java programming", "outra", [], 1.0, 1)
            results = hist.search("python")
            assert len(results) == 1
            assert results[0]["query"] == "python programming"

    def test_history_stats(self):
      
        with tempfile.TemporaryDirectory() as tmpdir:
            hist = History(history_path=f"{tmpdir}/history.json")
            hist.add("q1", "r1", [], 2.0, 1)
            hist.add("q2", "r2", [], 4.0, 2)
            stats = hist.stats()
            assert stats["total"] == 2
            assert stats["avg_duration"] == 3.0

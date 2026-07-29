"""
Testes para o sistema de cache.
"""

import json
import tempfile
from pathlib import Path

import pytest

from core.cache import Cache

class TestCache:
    """Testes do sistema de cache."""

    def test_cache_set_and_get(self):
        """Deve armazenar e recuperar dados do cache."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = Cache(cache_path=f"{tmpdir}/cache.json")
            cache.set("pergunta teste", {"response": "resposta teste"})
            result = cache.get("pergunta teste")
            assert result is not None
            assert result["response"] == "resposta teste"

    def test_cache_miss(self):
        """Query não cacheada deve retornar None."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = Cache(cache_path=f"{tmpdir}/cache.json")
            result = cache.get("query inexistente")
            assert result is None

    def test_cache_clear(self):
        """Limpar cache deve remover todas as entradas."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = Cache(cache_path=f"{tmpdir}/cache.json")
            cache.set("q1", {"r": "a"})
            cache.clear()
            assert cache.get("q1") is None
            assert cache.stats()["total_entries"] == 0

    def test_cache_case_insensitive(self):
        """Cache deve ser case-insensitive."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = Cache(cache_path=f"{tmpdir}/cache.json")
            cache.set("Python", {"r": "a"})
            assert cache.get("python") is not None
            assert cache.get("PYTHON") is not None

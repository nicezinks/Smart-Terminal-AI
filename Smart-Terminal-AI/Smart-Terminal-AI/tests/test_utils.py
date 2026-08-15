
import pytest
from core.utils import (
    generate_id, clean_text, truncate_text, format_duration,
    current_timestamp, sanitize_filename, is_valid_url, merge_dicts
)

class TestUtils:


    def test_generate_id_consistency(self):
     
        id1 = generate_id("teste")
        id2 = generate_id("teste")
        assert id1 == id2
        assert len(id1) == 16

    def test_generate_id_uniqueness(self):
       
        id1 = generate_id("teste1")
        id2 = generate_id("teste2")
        assert id1 != id2

    def test_clean_text(self):
        dirty = "  texto com espaços  


  excessivos  "
        clean = clean_text(dirty)
        assert "  " not in clean
        assert clean.startswith("texto")

    def test_truncate_text(self):
       
        long_text = "a" * 1000
        truncated = truncate_text(long_text, 100)
        assert len(truncated) <= 103
        assert truncated.endswith("...")

    def test_truncate_text_short(self):
    
        short = "texto curto"
        assert truncate_text(short, 100) == short

    def test_format_duration_seconds(self):
     
        assert format_duration(45.5) == "45.5s"

    def test_format_duration_minutes(self):
        assert format_duration(125) == "2m 5s"

    def test_sanitize_filename(self):
       
        dirty = 'arquivo<>\:"/\\|?*teste.txt'
        clean = sanitize_filename(dirty)
        assert "<" not in clean
        assert ">" not in clean
        assert ":" not in clean

    def test_is_valid_url(self):
        assert is_valid_url("https://www.google.com") is True
        assert is_valid_url("http://localhost:8080") is True
        assert is_valid_url("não é uma url") is False

    def test_merge_dicts(self):
        
        base = {"a": 1, "b": {"c": 2}}
        override = {"b": {"d": 3}, "e": 4}
        result = merge_dicts(base, override)
        assert result["a"] == 1
        assert result["b"]["c"] == 2
        assert result["b"]["d"] == 3
        assert result["e"] == 4

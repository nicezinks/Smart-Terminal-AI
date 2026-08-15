
import hashlib
import re
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

def generate_id(text: str) -> str:

    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]

def clean_text(text: str) -> str:
    text = re.sub(r'[\s]+', ' ', text)
    text = re.sub(r'[\n\r\t]+', '\n', text)
    return text.strip()

def truncate_text(text: str, max_length: int = 500) -> str:
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(' ', 1)[0] + "..."

def format_duration(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}m {secs}s"

def current_timestamp() -> str:
    return datetime.now().isoformat()

def current_date() -> str:
    return datetime.now().strftime("%Y-%m-%d")

def current_time() -> str:
    return datetime.now().strftime("%H:%M:%S")

def sanitize_filename(filename: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def merge_dicts(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result

def chunk_list(items: List[Any], chunk_size: int) -> List[List[Any]]:
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]

def is_valid_url(url: str) -> bool:
    pattern = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(pattern.match(url))

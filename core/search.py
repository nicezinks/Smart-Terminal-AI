"""Busca web via DuckDuckGo + filtro de links ativos."""
import json
from pathlib import Path
from typing import List, Dict
from urllib.parse import urlparse

import requests
from ddgs import DDGS

class SearchResult:
    def __init__(self, title: str, url: str, snippet: str = ""):
        self.title = title; self.url = url; self.snippet = snippet
    def to_dict(self): return {"title": self.title, "url": self.url, "snippet": self.snippet}


def _load_trusted_domains() -> set:
    """Carrega domínios confiáveis."""
    base = Path(__file__).resolve().parent.parent
    fpath = base / "trusted_sources.json"
    domains = set()
    if fpath.exists():
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            for cat, sites in data.items():
                for site in sites:
                    url = site.get("url", "")
                    if url:
                        dom = urlparse(url).netloc.replace("www.", "")
                        if dom:
                            domains.add(dom)
                            domains.add("www." + dom)
        except Exception:
            pass
    return domains


def _url_alive(url: str) -> bool:
    """Verifica se URL responde (timeout curto para não travar)."""
    try:
        r = requests.head(url, timeout=4, allow_redirects=True, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })
        return r.status_code == 200
    except Exception:
        return False


def search_duckduckgo(query: str, max_results: int = 10) -> List[SearchResult]:
    """Busca no DDGS, filtra links mortos, prioriza fontes confiáveis."""
    trusted = _load_trusted_domains()
    raw_results: List[SearchResult] = []

    # Busca normal
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=20):
                raw_results.append(SearchResult(
                    title=r.get("title", "Sem titulo"),
                    url=r.get("href", ""),
                    snippet=r.get("body", "")
                ))
    except Exception:
        return []

    # Separa: confiáveis primeiro, depois outros
    trusted_results = []
    other_results = []
    for r in raw_results:
        dom = urlparse(r.url).netloc.replace("www.", "")
        if dom in trusted:
            trusted_results.append(r)
        else:
            other_results.append(r)

    ordered = trusted_results + other_results

    # Filtra links mortos (verifica até max_results * 2 para ter margem)
    alive = []
    for r in ordered:
        if len(alive) >= max_results:
            break
        if _url_alive(r.url):
            alive.append(r)

    return alive

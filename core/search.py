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
    """
    Verifica se URL está no ar e respondendo corretamente.

    Tenta primeiro com HEAD (mais rápido), se falhar tenta GET.
    Aceita status 200-399 (inclui redirecionamentos válidos).
    Timeout curto para não travar a busca.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
    }

    # Tenta HEAD primeiro (mais leve)
    try:
        r = requests.head(url, timeout=5, allow_redirects=True, headers=headers)
        if 200 <= r.status_code < 400:
            return True
    except Exception:
        pass

    # Se HEAD falhar, tenta GET (alguns servidores bloqueiam HEAD)
    try:
        r = requests.get(url, timeout=8, allow_redirects=True, headers=headers, stream=True)
        # Lê só os primeiros bytes pra confirmar que não é página de erro
        _ = r.raw.read(1024)
        r.close()
        if 200 <= r.status_code < 400:
            return True
    except Exception:
        pass

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

    # Filtra links mortos — verifica até max_results * 3 pra ter margem
    alive = []
    checked = 0
    max_checks = max_results * 3

    for r in ordered:
        if len(alive) >= max_results:
            break
        if checked >= max_checks:
            break
        checked += 1

        if _url_alive(r.url):
            alive.append(r)

    return alive

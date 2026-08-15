
import asyncio
import re
from typing import List, Dict, Any

from bs4 import BeautifulSoup, Comment

from core.browser import BrowserManager
from core.config import Config
from core.logger import Logger
from core.utils import clean_text

class ScrapedContent:
    def __init__(self, url: str, title: str, text: str, word_count: int, success: bool = True):
        self.url = url
        self.title = title
        self.text = text
        self.word_count = word_count
        self.success = success

    def to_dict(self) -> Dict[str, Any]:
        return {"url": self.url, "title": self.title, "text": self.text,
                "word_count": self.word_count, "success": self.success}

class WebScraper:
    JUNK_TAGS = ["script", "style", "nav", "footer", "header", "aside",
                 "advertisement", "ad", "iframe", "noscript", "form",
                 "button", "input", "select", "textarea", "svg", "canvas",
                 "video", "audio", "source", "track", "embed", "object",
                 "template", "portal", "noscript"]

    JUNK_PATTERNS = re.compile(
        r'(ads?|advertisement|banner|popup|modal|sidebar|menu|nav|footer|header|'
        r'cookie|consent|newsletter|subscribe|social|share|comment|related|'
        r'recommend|promo|sponsored|breadcrumb|pagination|toolbar|widget|overlay)',
        re.IGNORECASE
    )

    def __init__(self):
        self.config = Config()
        self.logger = Logger()
        self.max_pages = self.config.get("search.max_pages_to_visit", 10)
        self.delay = self.config.get("search.delay_between_requests", 0.5)

    def _clean_html(self, html: str) -> str:
        soup = BeautifulSoup(html, "lxml")
        for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
            comment.extract()
        for tag in self.JUNK_TAGS:
            for t in soup.find_all(tag):
                t.decompose()
        for elem in soup.find_all(True):
            cls = " ".join(elem.get("class", []) or [])
            eid = elem.get("id", "") or ""
            if self.JUNK_PATTERNS.search(cls) or self.JUNK_PATTERNS.search(eid):
                elem.decompose()
        return str(soup)

    def _extract_text(self, html: str) -> str:
        soup = BeautifulSoup(html, "lxml")
        main = None
        for sel in ["main", "article", "[role='main']", ".content", "#content",
                    ".post", ".entry", ".article-body", "#article-body",
                    ".post-content", ".entry-content", "#main-content"]:
            main = soup.select_one(sel)
            if main:
                break
        if main:
            text = main.get_text(separator="\n", strip=True)
        else:
            body = soup.find("body")
            text = body.get_text(separator="\n", strip=True) if body else ""
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        return "\n".join(lines[:1000])

    async def scrape_url(self, url: str) -> ScrapedContent:
        browser = BrowserManager()
        try:
            await asyncio.wait_for(browser.start(), timeout=10.0)
            if not await asyncio.wait_for(browser.navigate(url), timeout=15.0):
                return ScrapedContent(url, "", "", 0, False)

            await asyncio.sleep(1.0)
            html = await browser.get_content()

            raw_title = await browser.evaluate("document.title")
            title = raw_title if raw_title else "Sem título"

            if not html or len(html) < 500:
                return ScrapedContent(url, title, "", 0, False)

            text = clean_text(self._extract_text(self._clean_html(html)))
            wc = len(text.split())
            return ScrapedContent(url, title, text, wc)
        except asyncio.TimeoutError:
            return ScrapedContent(url, "", "", 0, False)
        except Exception:
            return ScrapedContent(url, "", "", 0, False)
        finally:
            try:
                await asyncio.wait_for(browser.close(), timeout=5.0)
            except Exception:
                pass

    async def scrape_multiple(self, urls: List[str]) -> List[ScrapedContent]:
        results = []
        for i, url in enumerate(urls[:self.max_pages]):
            if i > 0:
                await asyncio.sleep(self.delay)
            r = await self.scrape_url(url)
            if r.success and r.word_count > 30:
                results.append(r)
        return results

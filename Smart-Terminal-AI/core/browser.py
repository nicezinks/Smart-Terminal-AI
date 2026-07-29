"""
Gerenciador de navegador headless com stealth anti-detecção.
"""

import asyncio
from typing import Optional, Any, Dict

from playwright.async_api import async_playwright, Browser, BrowserContext, Page

from core.config import Config
from core.logger import Logger

class BrowserManager:
    """Navegador headless com stealth anti-bot."""

    def __init__(self) -> None:
        self.config = Config()
        self.logger = Logger()
        self._playwright: Optional[Any] = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None

    async def start(self) -> None:
        try:
            self._playwright = await async_playwright().start()

            self._browser = await self._playwright.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--disable-blink-features=AutomationControlled",
                    "--disable-web-security",
                    "--disable-features=IsolateOrigins,site-per-process",
                    "--disable-site-isolation-trials",
                    "--disable-setuid-sandbox",
                    "--no-first-run",
                    "--no-default-browser-check",
                    "--disable-default-apps",
                    "--disable-extensions",
                    "--disable-component-extensions-with-background-pages",
                    "--hide-scrollbars",
                    "--mute-audio",
                    "--window-size=1920,1080",
                    "--start-maximized",
                    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
                ]
            )

            self._context = await self._browser.new_context(
                viewport={"width": 1920, "height": 1080},
                locale="pt-BR",
                timezone_id="America/Sao_Paulo",
                java_script_enabled=True,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
                extra_http_headers={
                    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Encoding": "gzip, deflate, br",
                    "DNT": "1",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "none",
                    "Sec-Fetch-User": "?1",
                    "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                }
            )

            # Stealth script completo
            await self._context.add_init_script("""
                // Esconde webdriver
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});

                // Plugins falsos
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [
                        {name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer'},
                        {name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai'},
                        {name: 'Native Client', filename: 'internal-nacl-plugin'}
                    ]
                });

                // Languages
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['pt-BR', 'pt', 'en-US', 'en']
                });

                // Chrome runtime
                window.chrome = { runtime: {} };

                // Permissions
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
                );

                // Notification permission
                Object.defineProperty(Notification, 'permission', {
                    get: () => 'default'
                });

                // Canvas fingerprint randomization prevention
                const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
                HTMLCanvasElement.prototype.toDataURL = function(type) {
                    if (this.width > 16 && this.height > 16) {
                        const ctx = this.getContext('2d');
                        if (ctx) {
                            ctx.fillStyle = '#f0f0f0';
                            ctx.fillRect(0, 0, 1, 1);
                        }
                    }
                    return originalToDataURL.apply(this, arguments);
                };

                // WebGL
                const getParameter = WebGLRenderingContext.prototype.getParameter;
                WebGLRenderingContext.prototype.getParameter = function(parameter) {
                    if (parameter === 37445) return 'Intel Inc.';
                    if (parameter === 37446) return 'Intel Iris Xe Graphics';
                    return getParameter(parameter);
                };

                // iFrame
                window.alert = () => {};
                window.confirm = () => true;
                window.prompt = () => null;
            """)

            self._page = await self._context.new_page()
            self._page.set_default_timeout(15000)

        except Exception as e:
            if self.logger:
                self.logger.error(f"Falha ao iniciar navegador: {e}")
            raise

    async def navigate(self, url: str) -> bool:
        if not self._page:
            return False
        try:
            response = await self._page.goto(
                url,
                wait_until="networkidle",
                timeout=20000
            )
            return response is not None
        except Exception:
            return False

    async def get_content(self) -> str:
        if not self._page:
            return ""
        try:
            return await self._page.content()
        except Exception:
            return ""

    async def get_text(self) -> str:
        if not self._page:
            return ""
        try:
            return await self._page.inner_text("body")
        except Exception:
            return ""

    async def evaluate(self, script: str) -> Any:
        if not self._page:
            return None
        try:
            return await self._page.evaluate(script)
        except Exception:
            return None

    async def close(self) -> None:
        try:
            if self._context:
                await self._context.close()
            if self._browser:
                await self._browser.close()
            if self._playwright:
                await self._playwright.stop()
        except Exception:
            pass

    async def __aenter__(self) -> "BrowserManager":
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

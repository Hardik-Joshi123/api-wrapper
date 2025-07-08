import requests
from playwright.sync_api import sync_playwright
from utils.logger import log
from config.settings import settings
from utils.error_handler import ErrorHandler

class CaptchaSolver:
    def __init__(self):
        self.error_handler = ErrorHandler(max_retries=2)
    
    def solve_with_flaresolverr(self, url):
        log.info(f"Solving CAPTCHA via FlareSolverr: {url}")
        payload = {
            "cmd": "request.get",
            "url": url,
            "maxTimeout": 60000,
            "session": "global_session"
        }
        try:
            response = requests.post(
                settings.FLARESOLVERR_URL, 
                json=payload,
                timeout=120
            )
            result = response.json()
            if result.get("status") == "ok":
                return result["solution"]["response"]
            log.error(f"FlareSolverr failed: {result.get('message')}")
        except Exception as e:
            log.error(f"FlareSolverr error: {e}")
        return None

    def solve_with_playwright(self, url):
        log.warning(f"Falling back to Playwright for: {url}")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # Visible for manual solving
            context = browser.new_context()
            page = context.new_page()
            
            page.goto(url)
            log.info("Please solve CAPTCHA manually in browser window...")
            
            # Wait for navigation or element indicating success
            page.wait_for_selector("body", state="attached", timeout=300000)  # 5 min timeout
            
            content = page.content()
            browser.close()
            return content

    def solve(self, url):
        # First try FlareSolverr
        content = self.error_handler.handle(self.solve_with_flaresolverr, url)
        if content:
            return content
            
        # Fallback to Playwright
        return self.error_handler.handle(self.solve_with_playwright, url)
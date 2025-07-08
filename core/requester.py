import requests
import time
import random
from utils.logger import log
from utils.error_handler import ErrorHandler
from utils.proxy_rotator import ProxyRotator
from utils.user_agents import get_random_agent
from config.settings import settings
from core.cache import configure_cache

class SmartRequester:
    def __init__(self):
        self.session = configure_cache()
        self.proxy_rotator = ProxyRotator()
        self.error_handler = ErrorHandler(max_retries=settings.MAX_RETRIES)
        self.last_request = 0

    def _get_headers(self):
        return {
            "User-Agent": get_random_agent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "DNT": "1"
        }

    def _respect_rate_limit(self):
        elapsed = time.time() - self.last_request
        if elapsed < settings.RATE_LIMIT_DELAY:
            sleep_time = settings.RATE_LIMIT_DELAY - elapsed + random.uniform(0, 1.5)
            log.debug(f"Rate limiting: Sleeping {sleep_time:.2f}s")
            time.sleep(sleep_time)
        self.last_request = time.time()

    def request(self, method, url, **kwargs):
        self._respect_rate_limit()
        
        headers = self._get_headers()
        proxy = self.proxy_rotator.get_proxy()
        
        log.info(f"Requesting {url} with {proxy or 'no proxy'}")
        
        try:
            response = self.error_handler.handle(
                self.session.request,
                method,
                url,
                headers=headers,
                proxies=proxy,
                timeout=settings.REQUEST_TIMEOUT,
                **kwargs
            )
            log.debug(f"Response: {response.status_code} for {url}")
            return response
        except requests.exceptions.RequestException as e:
            log.error(f"Request failed: {e}")
            raise

    def get(self, url, **kwargs):
        return self.request("GET", url, **kwargs)
    
    def post(self, url, **kwargs):
        return self.request("POST", url, **kwargs)
import requests
from core.cache import cache
from utils.logger import log
from config.settings import settings

class ProxyRotator:
    @cache(expire=3600)  # Cache proxy list for 1 hour
    def _fetch_proxies(self):
        try:
            response = requests.get(
                "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http",
                timeout=10
            )
            return [p.strip() for p in response.text.split('\n') if p.strip()]
        except Exception as e:
            log.warning(f"Proxy fetch failed: {e}")
            return []

    def get_proxy(self):
        proxies = self._fetch_proxies()
        if proxies:
            return {"http": f"http://{proxies[0]}", "https": f"http://{proxies[0]}"}
        return None
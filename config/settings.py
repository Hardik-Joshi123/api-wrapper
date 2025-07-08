import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Request settings
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 30))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))
    RATE_LIMIT_DELAY = float(os.getenv("RATE_LIMIT_DELAY", 2.5))
    
    # CAPTCHA settings
    FLARESOLVERR_URL = os.getenv("FLARESOLVERR_URL", "http://localhost:8191/v1")
    
    # Caching
    CACHE_EXPIRATION = int(os.getenv("CACHE_EXPIRATION", 3600))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

settings = Settings()
import requests_cache
from config.settings import settings

def configure_cache():
    return requests_cache.CachedSession(
        'api_cache',
        backend='sqlite',
        expire_after=settings.CACHE_EXPIRATION,
        allowable_methods=('GET', 'POST'),
        stale_if_error=True
    )

def cache(expire=300):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # aching implementation
            key = f"{func.__name__}-{str(args)}-{str(kwargs)}"
            if not hasattr(func, '_cache'):
                func._cache = {}
                
            if key in func._cache:
                return func._cache[key]
                
            result = func(*args, **kwargs)
            func._cache[key] = result
            return result
        return wrapper
    return decorator
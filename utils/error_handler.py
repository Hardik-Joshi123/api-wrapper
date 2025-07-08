import time
from utils.logger import log

class ErrorHandler:
    def __init__(self, max_retries=3, backoff_factor=1):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def handle(self, func, *args, **kwargs):
        for attempt in range(self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == self.max_retries:
                    log.error(f"Final attempt failed: {e}")
                    raise
                
                wait_time = self.backoff_factor * (2 ** attempt)
                log.warning(f"Attempt {attempt+1} failed. Retrying in {wait_time}s: {e}")
                time.sleep(wait_time)
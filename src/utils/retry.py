# src/utils/retry.py
import time
import functools
from config import settings

def retry(max_attempts=None, backoff=None):
    """
    A decorator to retry a function on exception.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            ma = max_attempts or settings.retry.max_retries
            bf = backoff or settings.retry.backoff_factor
            delay = 0.5
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception:
                    attempts += 1
                    if attempts >= ma:
                        raise
                    time.sleep(delay)
                    delay *= bf
        return wrapper
    return decorator

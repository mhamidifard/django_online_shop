import random
from django.core.cache import cache

def set_cache_with_jitter(key, value, timeout, jitter_percent=0.2):
    """
    Sets cache with jitter to prevent cache stampede.
    If timeout is 3600 and jitter_percent is 0.2 (20%), 
    the actual timeout will be randomized between 2880 and 4320 seconds.
    """
    if timeout is not None:
        jitter_variance = timeout * jitter_percent
        jitter = random.uniform(-jitter_variance, jitter_variance)
        actual_timeout = int(timeout + jitter)
    else:
        actual_timeout = None
        
    cache.set(key, value, timeout=actual_timeout)

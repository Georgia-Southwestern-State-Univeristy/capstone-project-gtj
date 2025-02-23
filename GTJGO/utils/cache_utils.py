from django.core.cache import cache
from django.conf import settings
from functools import wraps
import hashlib
import json
import logging
import time

logger = logging.getLogger(__name__)

class APICache:
    def __init__(self, timeout=3600):
        self.timeout = timeout
        self.prefix = getattr(settings, 'CACHE_KEY_PREFIX', 'gtjgo')

    def _make_key(self, prefix, *args, **kwargs):
        """Generate a unique cache key"""
        # Convert args and kwargs to a string
        args_str = json.dumps(args, sort_keys=True)
        kwargs_str = json.dumps(kwargs, sort_keys=True)
        
        # Create a unique string
        key_input = f"{prefix}:{args_str}:{kwargs_str}"
        
        # Create an MD5 hash
        key_hash = hashlib.md5(key_input.encode()).hexdigest()
        
        return f"{self.prefix}:{prefix}:{key_hash}"

    def cached_api_call(self, prefix, timeout=None):
        """Decorator for caching API calls with retry mechanism"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                cache_key = self._make_key(prefix, *args, **kwargs)
                cache_timeout = timeout or self.timeout

                try:
                    # Try to get from cache
                    cached_data = cache.get(cache_key)
                    if cached_data is not None:
                        logger.debug(f"Cache hit for {cache_key}")
                        return cached_data

                    # If not in cache, call the function
                    data = func(*args, **kwargs)
                    
                    # Store in cache
                    cache.set(cache_key, data, cache_timeout)
                    logger.debug(f"Stored in cache: {cache_key}")
                    
                    return data

                except Exception as e:
                    logger.error(f"Cache error for {cache_key}: {str(e)}")
                    # If cache fails, just execute the function
                    return func(*args, **kwargs)
                
            return wrapper
        return decorator

    def invalidate_keys(self, *prefixes):
        """Invalidate cache for given prefixes"""
        try:
            for prefix in prefixes:
                pattern = f"{self.prefix}:{prefix}:*"
                keys = cache.keys(pattern)
                if keys:
                    cache.delete_many(keys)
                    logger.info(f"Invalidated {len(keys)} keys for prefix {prefix}")
        except Exception as e:
            logger.error(f"Cache invalidation error: {str(e)}")

    def clear_all(self):
        """Clear all cache entries with this prefix"""
        try:
            pattern = f"{self.prefix}:*"
            keys = cache.keys(pattern)
            if keys:
                cache.delete_many(keys)
                logger.info(f"Cleared {len(keys)} cache entries")
        except Exception as e:
            logger.error(f"Cache clear error: {str(e)}")

# Initialize global cache instance
api_cache = APICache()
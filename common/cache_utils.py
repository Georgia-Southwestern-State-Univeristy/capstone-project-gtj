# common/cache_utils.py

from django.core.cache import cache
from django.conf import settings
from functools import wraps
import hashlib
import json
import logging

logger = logging.getLogger(__name__)

class CommonAPICache:
    def __init__(self, timeout=3600):
        self.timeout = timeout
        self.prefix = getattr(settings, 'CACHE_KEY_PREFIX', 'gtjgo')

    def _make_key(self, prefix, request_data):
        """Generate a unique cache key from request data"""
        if isinstance(request_data, dict):
            key_data = json.dumps(request_data, sort_keys=True)
        else:
            key_data = str(request_data)
        
        key_input = f"{prefix}:{key_data}"
        key_hash = hashlib.md5(key_input.encode()).hexdigest()
        
        return f"{self.prefix}:{prefix}:{key_hash}"

    def cached_api_call(self, prefix, timeout=None):
        """Decorator for caching API calls"""
        def decorator(func):
            @wraps(func)
            def wrapper(request, *args, **kwargs):
                # Extract relevant data from request
                request_data = {
                    'method': request.method,
                    'path': request.path,
                    'GET': dict(request.GET.items()),
                }
                
                cache_key = self._make_key(prefix, request_data)
                cache_timeout = timeout or self.timeout

                try:
                    cached_data = cache.get(cache_key)
                    if cached_data is not None:
                        logger.debug(f"Cache hit for {cache_key}")
                        return cached_data

                    response = func(request, *args, **kwargs)
                    
                    if hasattr(response, 'status_code') and response.status_code == 200:
                        cache.set(cache_key, response, cache_timeout)
                        logger.debug(f"Stored in cache: {cache_key}")
                    
                    return response

                except Exception as e:
                    logger.error(f"Cache error for {cache_key}: {str(e)}")
                    return func(request, *args, **kwargs)
                
            return wrapper
        return decorator

    def invalidate_cache(self, prefix):
        """Invalidate cache for a specific prefix"""
        try:
            pattern = f"{self.prefix}:{prefix}:*"
            cache.delete_pattern(pattern)
            logger.info(f"Invalidated cache for prefix {prefix}")
        except Exception as e:
            logger.error(f"Cache invalidation error: {str(e)}")

# Create a global instance
api_cache = CommonAPICache()
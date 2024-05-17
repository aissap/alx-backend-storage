#!/usr/bin/env python3
import redis
import requests
from typing import Callable
from functools import wraps
"""
Implementing an expiring web cache and tracker.
"""

redis_client = redis.Redis()


def track_and_cache(func: Callable) -> Callable:
    """
    Track URL access counts and cache the result with an expiry time.
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        count_key = f"count:{url}"
        redis_client.incr(count_key)

        cache_key = f"cache:{url}"
        cached_result = redis_client.get(cache_key)
        if cached_result:
            return cached_result.decode('utf-8')

        result = func(url)
        redis_client.setex(cache_key, 10, result)
        return result
    return wrapper


@track_and_cache
def get_page(url: str) -> str:
    """
    Fetches content of a URL, caches it for 10 sec, tracks the access counts.
    """
    response = requests.get(url)
    return response.text

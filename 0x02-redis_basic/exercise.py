#!/usr/bin/env python3
import redis
import uuid
from typing import Union
''' Writing strings to Redis. '''


class Cache:
    """
    A class to represent a caching system using Redis.

    Attributes:
        _redis: An instance of the Redis client.
    """
    def __init__(self):
        """
        Initializes the Cache object with a Redis client instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the provided data in Redis with a randomly generated key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

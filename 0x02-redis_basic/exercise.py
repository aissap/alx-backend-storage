#!/usr/bin/env python3
import redis
import uuid
from typing import Union, Callable, Optional
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

    def get(
            self,
            key: str,
            fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float, None]:
        """
        Retrieves data from Redis using the given key.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Retrieves a string value from Redis using the given key.
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Retrieves an integer value from Redis using the given key.
        """
        return self.get(key, int)

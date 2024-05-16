#!/usr/bin/env python3
import redis
import uuid
from typing import Union, Callable, Optional, Any
import functools

def count_calls(method: Callable) -> Callable:
    """
    function to count the number of times a method is called.
    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        function that increments the call count in Redis and calls the original method.
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    store the history of inputs and outputs for a function in Redis.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """
        function to execute the method and store its inputs and outputs in Redis.
        """
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(inputs_key, str(args))

        result = method(self, *args, **kwargs)

        self._redis.rpush(outputs_key, result)

        return result

    return wrapper


def replay(method: Callable, cache: Cache) -> None:
    """
    Function to display the history of calls of a particular function.
    """
    inputs_key = f"{method.__qualname__}:inputs"
    outputs_key = f"{method.__qualname__}:outputs"

    inputs = cache._redis.lrange(inputs_key, 0, -1)
    outputs = cache._redis.lrange(outputs_key, 0, -1)

    num_calls = min(len(inputs), len(outputs))

    print(f"{method.__qualname__} was called {num_calls} times:")

    for inp, outp in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{inp.decode('utf-8')}) -> {outp.decode('utf-8')}")


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

    @call_history
    @count_calls
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
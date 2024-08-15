#!/usr/bin/env python3
"""
Cache module for storing data in Redis, counting method calls, tracking call hi
story, and replaying function calls.
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of calls to a method."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs for a method."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))

        return output
    return wrapper


def replay(method: Callable):
    """
    Display the history of calls of a particular function.

    Args:
        method (Callable): The method to replay the history for.
    """
    redis_client = method.__self__._redis
    qualname = method.__qualname__
    inputs = redis_client.lrange(f"{qualname}:inputs", 0, -1)
    outputs = redis_client.lrange(f"{qualname}:outputs", 0, -1)

    print(f"{qualname} was called {len(inputs)} times:")
    for input_args, output in zip(inputs, outputs):
        print(f"{qualname}(*{input_args.decode('utf-8')}) -> {output.decode('utf-8')}")


class Cache:
    """Cache class for interacting with Redis."""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Optional[Union[str, bytes, int, float]]:
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        return self.get(key, fn=int)

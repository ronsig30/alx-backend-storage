#!/usr/bin/env python3
"""
Cache module for storing data in Redis, counting method calls, and tracking cal
l history.
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of calls to a method.

    Args:
        method (Callable): The method to wrap.

    Returns:
        Callable: The wrapped method that increments the call count.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments the count for the method and calls the
        original method.

        Args:
            *args: Positional arguments for the original method.
            **kwargs: Keyword arguments for the original method.

        Returns:
            Any: The return value of the original method.
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a method.

    Args:
        method (Callable): The method to wrap.

    Returns:
        Callable: The wrapped method that stores input/output history.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that stores input and output history in Redis.

        Args:
            *args: Positional arguments for the original method.
            **kwargs: Keyword arguments for the original method.

        Returns:
            Any: The return value of the original method.
        """
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Store the input arguments in the inputs list
        self._redis.rpush(input_key, str(args))

        # Execute the original method and store the output in the outputs list
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))

        return output

    return wrapper


class Cache:
    """Cache class for interacting with Redis."""

    def __init__(self):
        """Initialize the Cache class and flush the Redis database."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store data in Redis with a random key and return the key.

        Args:
            data (Union[str, bytes, int, float]): Data to be stored in Redis.

        Returns:
            str: The randomly generated key associated with the stored data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Optional[Union[str, bytes, int, float]]:
        """
        Retrieve data from Redis and optionally apply a conversion function.

        Args:
            key (str): The key to retrieve data from Redis.
            fn (Optional[Callable]): Optional function to apply to the retrieve
            d data.

        Returns:
            Optional[Union[str, bytes, int, float]]: The retrieved data, possib
            ly converted.
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve a string from Redis.

        Args:
            key (str): The key to retrieve data from Redis.

        Returns:
            Optional[str]: The retrieved data as a string.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve an integer from Redis.

        Args:
            key (str): The key to retrieve data from Redis.

        Returns:
            Optional[int]: The retrieved data as an integer.
        """
        return self.get(key, fn=int)

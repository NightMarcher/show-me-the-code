import pickle
import time
from typing import Any, Callable, Tuple

import redis


def get_cached_data_safe(
    conn: redis.Redis,
    func: Callable,
    cache_key: str,
    cache_timeout: int = 300,
    lock_key: str = None,
    lock_timeout: int = 2,
    retry_times: int = 4,
    retry_interval: float = 0.125,
    encoder: Callable = pickle.dumps,
    decoder: Callable = pickle.loads,
    *args,
    **kwargs
) -> Tuple[Any, bool, int]:
    """
    Get data through Redis cache, using distributed lock to ensure only one thread fetches data

    Args:
        conn: Redis client instance
        func: Function to get data
        cache_key: Cache key
        cache_timeout: Cache expiration time in seconds
        lock_key: Distributed lock key, defaults to cache_key + ":lock"
        lock_timeout: Lock timeout in seconds
        retry_times: Number of retries
        retry_interval: Retry interval in seconds
        encoder: Data encoding function
        decoder: Data decoding function
        *args: Positional arguments passed to func
        **kwargs: Keyword arguments passed to func

    Returns:
        Tuple[Any, bool, int]: (data, from_cache, retries)
    """
    # 1. Try to get data from cache
    cache = conn.get(cache_key)
    if cache is not None:
        return decoder(cache), True, 0

    # 2. Try to acquire lock
    if not lock_key:
        lock_key = f"{cache_key}:lock"
    acquired = conn.set(lock_key, "lock", ex=lock_timeout, nx=True)

    if acquired:
        try:
            # Got lock, execute data fetching logic
            data = func(*args, **kwargs)
            # Store data in cache
            conn.set(cache_key, encoder(data), ex=cache_timeout)
            return data, False, 0
        finally:
            # Release lock
            conn.delete(lock_key)
    else:
        # 3. Failed to acquire lock, retry getting from cache
        retries = 0
        for _ in range(retry_times):
            time.sleep(retry_interval)
            retries += 1
            cache = conn.get(cache_key)
            if cache is not None:
                return decoder(cache), True, retries

        # If still no data after retries, raise exception
        raise TimeoutError(f"Failed to get data after {retry_times} retries")


# Usage example
if __name__ == "__main__":
    # Create Redis client
    conn = redis.Redis(host="localhost", port=6379, db=0)

    # Example data fetching function
    def get_data(param1: str, param2: int = 0):
        print(f"Fetching data from source with params: {param1}, {param2}...")
        return {"message": f"Hello, {param1}!", "value": param2}

    # Get data using the function
    try:
        data, from_cache, retries = get_cached_data_safe(
            conn=conn,
            func=get_data,
            cache_key="test:data",
            param1="World",
            param2=42,
        )
        print(f"Result: {data}")
        print(f"From cache: {from_cache}")
        print(f"Retries: {retries}")
    except TimeoutError as e:
        print(f"Error: {e}") 

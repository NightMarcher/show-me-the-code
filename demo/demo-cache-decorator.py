import functools
import hashlib
import logging
import pickle

import redis


def cache(timeout_sec=60, encoder=pickle.dumps, decoder=pickle.loads):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            params = "{}|{}".format(
                ",".join(str(item) for item in args if isinstance(item, (str, bool, int, float, dict, list, tuple))),
                "&".join(sorted(f"{k}={v}" for k, v in kwargs.items())),
            )
            key = "{}:{}".format(
                func.__qualname__,
                hashlib.md5(params.encode()).hexdigest(),
            )
            try:
                rcli = redis.Redis()
                result = rcli.get(key)
                print(f"{func.__qualname__} => params:{params}, result:{result}")
                if result is not None:
                    result = decoder(result)
                else:
                    result = func(*args, **kwargs)
                    rcli.set(key, encoder(result), ex=timeout_sec)
            except Exception as e:
                logging.exception(e)
            else:
                return result
        return inner
    return wrapper


@cache(timeout_sec=5)
def demo_func(p, *args, r=2, **kwargs):
    """docstring of demo_func"""
    import random
    return random.randrange(0, 100)


if __name__ == "__main__":
    print(demo_func.__qualname__, demo_func.__doc__, demo_func.__annotations__, "\n", sep="\n")
    demo_func(0, 1, k=3)
    demo_func(0, 1, k=3)
    demo_func(0, r=1, k=3)
    demo_func(0, r=1, k=3)

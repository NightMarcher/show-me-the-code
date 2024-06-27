import functools
import hashlib
import json
import logging
import redis


def cache(timeout_sec=60):
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
                rcli = redis.Redis(decode_responses=True)
                result = rcli.get(key)
                print(f"{func.__qualname__} => params:{params}, result:{result}")
                if result is not None:
                    result = json.loads(result)
                else:
                    result = func(*args, **kwargs)
                    rcli.set(key, json.dumps(result), ex=timeout_sec)
            except Exception as e:
                logging.exception(e)
            else:
                return result
        return inner
    return wrapper


@cache()
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

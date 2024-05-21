import functools
import hashlib
import json
import logging
import redis


def cache(timeout_sec=60):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            params_str = "{}|{}".format(
                ",".join(str(item) for item in args),
                "&".join(sorted(f"{k}={v}" for k, v in kwargs.items())),
            )
            key = "{}:{}".format(
                func.__qualname__,
                hashlib.md5(params_str.encode()).hexdigest(),
            )
            rds = redis.Redis(decode_responses=True)
            result = rds.get(key)
            print(params_str, key, result, sep="\n")
            try:
                if result is not None:
                    result = json.loads(result)
                else:
                    result = func(*args, **kwargs)
                    rds.set(key, json.dumps(result), ex=timeout_sec)
            except Exception as e:
                logging.exception(e)
            else:
                print(result, "\n")
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

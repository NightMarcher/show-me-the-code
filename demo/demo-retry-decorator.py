import functools
import logging
import time

import requests


def retry(reties=2, sleep_sec=0.125, retry_on=Exception):
    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            tries = reties + 1
            for idx in range(tries):
                try:
                    return func(*args, **kwargs)
                except retry_on as e:
                    logging.warning(f"No.{idx + 1} attempt of `{func.__qualname__}` failed => {e}")
                    time.sleep(sleep_sec)
            logging.exception(f"{func.__qualname__} tried {tries} times but all failed!")
        return inner
    return wrapper


if __name__ == "__main__":
    retry_get = retry(retry_on=(
            # requests.exceptions.ConnectionError,
            ValueError,
        )
    )(requests.get)

    try:
        resp = retry_get(
            # "http://localhost"
            "http://baidu.com"
        )
    except Exception as e:
        print(f"e => {e}")
    else:
        print(f"resp => {resp}")
        if resp:
            print(resp.status_code, resp.reason, resp.text)

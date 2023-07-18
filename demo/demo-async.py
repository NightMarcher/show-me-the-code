import asyncio
from os import urandom
from random import uniform
from time import perf_counter


# @asyncio.coroutine
# def sleep(cid=None):
async def sleep(cid=None):
    if cid is None:
        cid = urandom(5).hex()
    sec = uniform(0, 2)
    # yield from asyncio.sleep(sec)
    print(f"Coroutine({cid}) will sleep {sec:.2f} seconds")
    await asyncio.sleep(sec)
    print(f"Coroutine({cid}) has slept")
    return sec


async def main():
    # 1. coroutine object sleep
    # future = sleep()

    # 2. pending Task
    future = asyncio.create_task(sleep())
    # future = asyncio.ensure_future(sleep())

    # 3. pending _GatheringFuture
    # future = asyncio.gather(sleep(), sleep(), sleep())

    # 4. coroutine object wait, deprecated since Python 3.8
    # future = asyncio.wait([sleep(), sleep(), sleep()])

    print(future)
    return await future


if __name__ == "__main__":
    st = perf_counter()
    result = asyncio.run(main())
    # loop = asyncio.get_event_loop()
    # result = loop.run_until_complete(main())
    et = perf_counter()
    print(f"total duration: {et - st:.3f}, result: {result}")

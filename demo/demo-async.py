import asyncio
from os import urandom
from random import uniform
from time import perf_counter


# @asyncio.coroutine
# def sleep(cid):
async def sleep(cid=None):
    if not cid:
        cid = urandom(5).hex()
    sec = uniform(0, 2)
    # yield from asyncio.sleep(sec)
    await asyncio.sleep(sec)
    print(f"Coroutine({cid}) has slept {sec:.2f} seconds")
    return sec

# 1. coroutine object
# future = sleep()

# 2. pending Task
# future = asyncio.ensure_future(sleep())

# 3. coroutine object wait
future = asyncio.wait([sleep(), sleep(), sleep()])

# 4. pending _GatheringFuture
# future = asyncio.gather(sleep(), sleep(), sleep())

print(future)

st = perf_counter()
result = asyncio.run(future)
# loop = asyncio.get_event_loop()
# result = loop.run_until_complete(future)
et = perf_counter()

print(f"total duration: {et - st:.3f}, result: {result}")

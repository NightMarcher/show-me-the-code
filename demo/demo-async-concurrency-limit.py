import asyncio
from os import urandom
from random import uniform
from time import perf_counter, time


async def handle_sleep(sem):
    async with sem:
        res = await sleep()

    print("sleeping")
    await asyncio.sleep(1)
    return res


async def sleep(cid=None):
    if cid is None:
        cid = urandom(5).hex()
    sec = uniform(0, 2)
    print(f"Coroutine({cid}) will sleep {sec:.3f} seconds, started at {time():.3f}")
    await asyncio.sleep(sec)
    print(f"Coroutine({cid}) has slept")
    return sec


async def using_gather():
    coros = init_coroutines()
    return await asyncio.gather(*coros)


async def using_for_loop():
    coros = init_coroutines()
    # return [await fut for fut in coros]  # coros will run one by one
    return [await fut for fut in asyncio.as_completed(coros)]


def init_coroutines():
    sem = asyncio.Semaphore(2)
    return [handle_sleep(sem) for _ in range(4)]


if __name__ == "__main__":
    st = perf_counter()
    # result = asyncio.run(using_gather())
    result = asyncio.run(using_for_loop())
    et = perf_counter()
    print(f"total duration: {et - st:.3f}, result: {result}")

#!/usr/bin/python
# -*- coding: utf-8 -*-
import asyncio
from random import uniform

# @asyncio.coroutine
# def sleep(id_='Null'):
async def sleep(id_='Null'):
    while True:
        time = uniform(0, 2)
        # yield from asyncio.sleep(time)
        await asyncio.sleep(time)
        print(f'Coroutine #{id_} slept {time:.2f} seconds')
        return time

# coroutine
# future = sleep()

# generator
# future = asyncio.wait([sleep('a'), sleep('b'), sleep('c')])

# _GatheringFuture
future = asyncio.gather(sleep('a'), sleep('b'), sleep('c'))

loop = asyncio.get_event_loop()
result = loop.run_until_complete(future)
print(f'result: {result}')
loop.close()

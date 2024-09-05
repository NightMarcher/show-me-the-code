#!/usr/bin/env python

import asyncio
from websockets.asyncio.server import serve

async def echo(websocket):
    print(websocket.id, websocket.state)
    async for message in websocket:
        print(f"Echo: {message}")
        await websocket.send(message)

async def main():
    async with serve(echo, "localhost", 8765):
        print("start serving")
        await asyncio.get_running_loop().create_future()  # run forever

asyncio.run(main())

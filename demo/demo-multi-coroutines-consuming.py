import asyncio
from random import randrange
import signal
from time import perf_counter, time


def graceful_exit(signum, frame):
    global running
    running = False


async def get_task():
    return {
        "ts": time(),
        "id": randrange(0, 1_000_000),
    }


async def handle_task(task):
    ...


async def work(queue, handler):
    while running or not queue.empty():
        task = await queue.get()
        print(f"handled {task}")
        await handler(task)
        global handled_tasks
        handled_tasks += 1
        await asyncio.sleep(sleep_sec)


async def main(queue_size, worker_num, handle_task):
    queue = asyncio.Queue(queue_size)
    workers = [asyncio.create_task(work(queue, handle_task)) for _ in range(worker_num)]

    while running:
        task = await get_task()
        print(f"got {task}")
        await queue.put(task)
        global got_tasks
        got_tasks += 1

    await asyncio.gather(*workers, return_exceptions=True)


if __name__ == "__main__":
    running = True
    signal.signal(signal.SIGINT, graceful_exit)  # Ctrl+C
    signal.signal(signal.SIGTERM, graceful_exit)  # sent by `kill` command

    # About concurrency
    worker_num = 8
    queue_size = 8  # max size of queue in memory

    # For statistics
    got_tasks = 0
    handled_tasks = 0
    sleep_sec = 1 / 8
    st = perf_counter()
    asyncio.run(main(queue_size, worker_num, handle_task))
    duration = perf_counter() - st
    print(f"got_tasks: {got_tasks}, handled_tasks: {handled_tasks}")
    print(
        f"Maximum calls of `handle_task` per second on paper: {1 / sleep_sec * worker_num}\n"
        f"Actual rate: {handled_tasks / duration}"
    )

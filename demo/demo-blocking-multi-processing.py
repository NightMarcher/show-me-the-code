from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Queue
from random import uniform
from time import perf_counter, sleep, time

pool = ProcessPoolExecutor(4)
queue = Queue()
num = 8


def async_run(target, *args, **kwargs):
    fut = pool.submit(target, *args, **kwargs)
    # fut.result()

def fake_target(uid):
    st = time()
    sec = uniform(0, 2)
    sleep(sec)
    print(f"{uid} started at {st:.3f}, lasts for {sec:.3f} sec")
    queue.put(sec)

def main():
    st = perf_counter()
    for idx in range(num):
        async_run(fake_target, uid=idx)

    # pool.shutdown()
    sec_list = []
    for _ in range(num):
        sec_list.append(queue.get())
    et = perf_counter()
    print(f"sec_list: {sec_list}")
    print(f"total duration: {et - st:.3f}, raw sec: {sum(sec_list):.3f}")

if __name__ == "__main__":
    main()

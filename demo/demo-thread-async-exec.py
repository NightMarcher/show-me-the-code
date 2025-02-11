from functools import partial
from threading import Thread


class ThreadTimeout(Exception):
    pass


class ResponseDict(dict):
    def __missing__(self, key):
        raise ThreadTimeout("Missing key: %s" % key)


class ThreadManager:
    def __init__(self):
        self.thread_list = []
        self.async_res = ResponseDict()

    def activate_thread(self, key, func, *args):
        partial_func = partial(func, *args)
        t = RequestThread(key, self.async_res, partial_func)
        t.start()
        self.thread_list.append(t)

    def wait_res(self, timeout=5):
        for t in self.thread_list:
            t.join(timeout)
        return self.async_res


class RequestThread(Thread):
    def __init__(self, key, res_dict, func):
        super(RequestThread, self).__init__()
        self.key = key
        self.res_dict = res_dict
        self.func = func

    def run(self):
        res = self.func()
        self.res_dict[self.key] = res


if __name__=="__main__":
    from time import sleep
    def func(sec):
        sleep(sec)
        print("func done")

    tm = ThreadManager()
    tm.activate_thread("test_func1", func, 2)
    tm.activate_thread("test_func2", func, 3)
    print("Activated")
    print(tm.wait_res())
    print("Waited")

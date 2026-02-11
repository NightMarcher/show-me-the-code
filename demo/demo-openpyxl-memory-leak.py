import gc
import os
import sys
import time
import weakref


class Cell:
    def __init__(self, worksheet, row=None, column=None, value=None):
        self.parent = worksheet  # strong reference to worksheet, will cause memory leak, only `worksheet._cells.clear()` can release it
        # self.parent = weakref.proxy(worksheet)
        self.row = row
        self.column = column
        self.value = value


class Worksheet:
    def __init__(self):
        self._cells = {}

    def add_empty_cell(self, row, column):
        self._cells[(row, column)] = Cell(self, row=row, column=column)


def demo():
    worksheet = Worksheet()
    rows = 3000
    columns = 3000
    for i in range(1, rows + 1):
        for j in range(1, columns + 1):
            worksheet.add_empty_cell(i, j)
    print(
        f"worksheet._cells => len:{len(worksheet._cells)}, size:{sys.getsizeof(worksheet._cells) / 1024 / 1024:.2f}MB, "
        f"key&value: {sum(sys.getsizeof(k) + sys.getsizeof(v) for k, v in worksheet._cells.items()) / 1024 / 1024:.2f}MB"
    )

    first_cell = worksheet._cells[(1, 1)]
    print(sys.getrefcount(worksheet) - 1)
    print(sys.getrefcount(first_cell.parent) - 1, sys.getrefcount(first_cell) - 1)
    worksheet._cells.clear()
    # del worksheet
    # gc.collect()
    print(sys.getrefcount(first_cell.parent) - 1, sys.getrefcount(first_cell) - 1)


if __name__ == "__main__":
    print("PID:", os.getpid())
    demo()
    time.sleep(60)

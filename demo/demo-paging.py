from typing import List


def paging(dicts: List[dict], total: int, limit: int = 10, offset: int = 0):
    return {
        "more": total > offset + limit,
        "total": total,
        "count": len(dicts),
        "dicts": dicts,
    }


if __name__ == "__main__":
    print(paging(range(9), 9))
    print(paging(range(10), 10))
    print(paging(range(10), 11))

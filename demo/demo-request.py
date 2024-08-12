#!/usr/bin/python3
from json import dumps
from os import path
from sys import argv

from requests import get
from tqdm import tqdm

def main(url, fn, chunk_size=1024 * 1024):
    print(fn, url)
    req_headers = {
        "Content-Type": "video/mp4",
        "Accept-Ranges": "bytes",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    }
    pre_resp = get(url, stream=True, headers=req_headers)
    rsp_headers = pre_resp.headers
    print(dumps(dict(rsp_headers), indent=2))
    if not pre_resp.ok:
        return print(pre_resp.status_code, pre_resp.reason, pre_resp.text)

    total_size = int(rsp_headers.get("content-length", 0))
    start_size = path.getsize(fn) if path.exists(fn) else 0
    if start_size >= total_size:
        return print(f"{fn} Existed!")

    resp = get(
        url, stream=True, headers={"Range": f"bytes={start_size}-{total_size}", **req_headers},
    )
    pbar = tqdm(
        total=total_size, initial=start_size, unit="B", unit_scale=True, desc=fn,
    )
    with open(fn, "ab+") as fs:
        for chunk in resp.iter_content(chunk_size=chunk_size):
            fs.write(chunk)
            pbar.update(len(chunk))
        pbar.close()

if __name__ == "__main__":
    url, fn = argv[1], argv[2]
    main(url, (fn or "tmp") + ".mp4")


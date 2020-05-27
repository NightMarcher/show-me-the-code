import socket
from datetime import datetime


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('114.114.114.114', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def get_now_str():
    return datetime.now().strftime('%x %X')


print(f'{__name__}: get_host_ip: {id(get_host_ip)}')

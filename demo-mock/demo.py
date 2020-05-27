from defines import get_host_ip, get_now_str

print(f'{__name__}: get_host_ip: {id(get_host_ip)}')


def func(your_name):
    if not your_name:
        return False, 'please check your input params'

    try:
        your_ip = get_host_ip()
        print(f'got ip: {your_ip}')
    except Exception as e:
        print(e)
        return False, str(e)

    return True, {'name': your_name, 'ip': your_ip, 'now': get_now_str()}

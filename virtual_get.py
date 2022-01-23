import time


def get_data(ip: str):
    time.sleep(int(ip) // 100)
    return int(ip) % 100

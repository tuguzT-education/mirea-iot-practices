import random
import time


def emulator():
    while True:
        print(random.randint(10, 1000))
        time.sleep(random.randint(1, 3))


if __name__ == '__main__':
    emulator()

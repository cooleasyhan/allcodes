import time
from threading import Thread


def countdown(n):
    while n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(1)


t = Thread(target=countdown, args=(10,), daemon=True)
t.start()

if t.is_alive():
    print('still running')
else:
    print ('stoped')

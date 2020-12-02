from threading import Thread
from time import sleep

from bluepy import btle

from common import SFM2S, SFM2_SFQT_ID, Counter


class MyDelegate(btle.DefaultDelegate):
    def __init__(self, counter):
        btle.DefaultDelegate.__init__(self)
        self._counter = counter

    def handleNotification(self, cHandle, data):
        if len(data) > 20:
            print("more")
        self._counter.increment()


p = None
try:
    p = btle.Peripheral(SFM2S[-1], btle.ADDR_TYPE_RANDOM)
    ch = p.getCharacteristics(uuid=SFM2_SFQT_ID)[0]
    counter = Counter()
    delegate = MyDelegate(counter)
    p.setDelegate(delegate)
    p.writeCharacteristic(ch.valHandle + 1, b"\x01\x00")

    print('Connected')

    def loop():
        while True:
            p.waitForNotifications(1)

    t = Thread(target=loop)
    t.daemon = True
    t.start()

    while True:
        print(f"{counter.get_inc_since_last()} Hz")
        sleep(1)


finally:
    p.disconnect()
from time import sleep, time

import pygatt

from common import SFM2_SFQT_ID, Counter, SFM2S

ADDRESS_TYPE = pygatt.BLEAddressType.random

# configure_adapter('hci0', 24, 24)
# configure_adapter('hci1', 30, 30)

# adapters = [pygatt.GATTToolBackend(hci_device='hci0') for _ in SFM2S[:3]] + [pygatt.GATTToolBackend(hci_device='hci1') for _ in SFM2S[3:]]
adapters = [pygatt.GATTToolBackend(hci_device='hci0') for _ in SFM2S]


def handle_data(counter: Counter, value):
    if len(value) > 20:
        print(f"Multi: x{len(value) // 20} ({len(value)}B)")
    counter.increment()
    # print("Received data: %s" % binascii.hexlify(value))


def setup(adapter, addr: str):
    device = adapter.connect(addr, address_type=ADDRESS_TYPE, timeout=1000, auto_reconnect=True)
    print(f"Connected to {addr}")
    counter = Counter()

    def sub():
        device.subscribe(SFM2_SFQT_ID,
                         callback=lambda _, v: handle_data(counter, v))
        return counter

    return sub


try:
    for a in adapters:
        a.start()

    devs = []
    for i in range(len(adapters)):
        c = setup(adapters[i], SFM2S[i])
        devs.append(c)

    cnts = [d() for d in devs]

    last_t = time() - 1
    while True:
        t = time()
        diff = t - last_t
        last_t = t

        print("  ".join((f"{c.get_inc_since_last() / diff}" for c in cnts)))
        sleep(1)
except Exception as e:
    print(e)
finally:
    for a in adapters:
        a.stop()

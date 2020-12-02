SFM2S = [
    "CA:97:13:6A:75:58",
    "ED:CA:1C:38:44:8C",
    "C6:04:7F:D4:EB:DF",
    "C6:56:4A:A4:C7:26",
    "C5:CF:C3:A4:D9:03",
    "D8:07:CF:41:77:74"
]

SFM2_SFQT_ID = "71D3" + "0102" + "-E8E7-4F91-AA3C-4A68051247BC"


class Counter:
    def __init__(self):
        self._value = 0
        self._last_value_read = 0

    def increment(self):
        self._value += 1

    def get_inc_since_last(self):
        value = self._value
        diff = value - self._last_value_read
        self._last_value_read = value
        return diff


def configure_adapter(hci: str, min_conn_interval: int, max_conn_interval: int):
    dir = f'/sys/kernel/debug/bluetooth/{hci}'
    min_filepath = f'{dir}/conn_min_interval'
    max_filepath = f'{dir}/conn_max_interval'
    _try_writing_setting(min_filepath, min_conn_interval)
    _try_writing_setting(max_filepath, max_conn_interval)
    _write_setting(min_filepath, min_conn_interval)
    _write_setting(max_filepath, max_conn_interval)


def _try_writing_setting(filepath: str, setting):
    try:
        _write_setting(filepath, setting)
    except:
        pass


def _write_setting(filepath: str, setting):
    with open(filepath, 'w') as f:
        f.write(f"{setting}\n")

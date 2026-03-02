import psutil

from exs_shell.interfaces.types import SystemSizeUnit


SIZE_MULTIPLIERS = {
    "B": 1,
    "KB": 1024,
    "MB": 1024**2,
    "GB": 1024**3,
    "TB": 1024**4,
    "PB": 1024**5,
    "EB": 1024**6,
    "ZB": 1024**7,
    "YB": 1024**8,
}


class CPUMonitor:
    def __init__(self):
        self._cpu = psutil.cpu_percent()

    @property
    def percent(self) -> float:
        return self._cpu


class NetMonitor:
    def __init__(self, size_unit: SystemSizeUnit):
        self._net = psutil.net_io_counters()
        self._size_unit = size_unit

    @property
    def rx(self) -> float:
        return self._net.bytes_recv / SIZE_MULTIPLIERS[self._size_unit]

    @property
    def tx(self) -> float:
        return self._net.bytes_sent / SIZE_MULTIPLIERS[self._size_unit]


class DiskMonitor:
    def __init__(self, size_unit: SystemSizeUnit):
        self._partitions = psutil.disk_partitions(all=False)
        self._size_unit = size_unit

    @property
    def total(self) -> float:
        total = 0
        for part in self._partitions:
            try:
                total += psutil.disk_usage(part.mountpoint).total
            except PermissionError:
                continue
        return total / SIZE_MULTIPLIERS[self._size_unit]

    @property
    def used(self) -> float:
        used = 0
        for part in self._partitions:
            try:
                used += psutil.disk_usage(part.mountpoint).used
            except PermissionError:
                continue
        return used / SIZE_MULTIPLIERS[self._size_unit]

    @property
    def free(self) -> float:
        free = 0
        for part in self._partitions:
            try:
                free += psutil.disk_usage(part.mountpoint).free
            except PermissionError:
                continue
        return free / SIZE_MULTIPLIERS[self._size_unit]

    @property
    def percent(self) -> float:
        t = self.total
        if t == 0:
            return 0.0
        return (self.used / t) * 100


class MemoryMonitor:
    def __init__(self, size_unit: SystemSizeUnit):
        self._mem = psutil.virtual_memory()
        self._size_unit = size_unit

    @property
    def total(self) -> float:
        return self._mem.total / SIZE_MULTIPLIERS[self._size_unit]

    @property
    def used(self) -> float:
        return self._mem.used / SIZE_MULTIPLIERS[self._size_unit]

    @property
    def free(self) -> float:
        return self._mem.free / SIZE_MULTIPLIERS[self._size_unit]

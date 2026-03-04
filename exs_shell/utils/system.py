from __future__ import annotations

import psutil

from dataclasses import dataclass
from typing import Any, Callable, List, Literal, Optional

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


@dataclass
class Process:
    pid: int
    name: str
    username: str
    cpu_percent: float
    memory: float
    status: str  # running, sleeping, zombie, etc.

    @property
    def is_active(self) -> bool:
        return self.status.lower() not in ("zombie", "stopped", "dead")


class ProcessMonitor:
    def __init__(self, size_unit: SystemSizeUnit = "MB"):
        self._size_unit = size_unit

    def list(
        self,
        sort_by: Literal["cpu", "memory", "pid", "name"] = "cpu",
        reverse: bool = True,
        filter_name: Optional[str] = None,
        filter_user: Optional[str] = None,
    ) -> List[Process]:
        processes: List[Process] = []

        for proc in psutil.process_iter(
            ["pid", "name", "username", "cpu_percent", "memory_info", "status"]
        ):
            try:
                info = proc.info

                if (
                    filter_name
                    and filter_name.lower() not in (info["name"] or "").lower()
                ):
                    continue
                if (
                    filter_user
                    and filter_user.lower() not in (info["username"] or "").lower()
                ):
                    continue

                memory = (
                    info["memory_info"].rss / SIZE_MULTIPLIERS[self._size_unit]
                    if info["memory_info"]
                    else 0.0
                )

                processes.append(
                    Process(
                        pid=info["pid"],
                        name=info["name"] or "",
                        username=info["username"] or "",
                        cpu_percent=info["cpu_percent"] or 0.0,
                        memory=memory,
                        status=info["status"] or "",
                    )
                )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        key_map: dict[str, Callable[[Process], Any]] = {
            "cpu": lambda p: p.cpu_percent,
            "memory": lambda p: p.memory,
            "pid": lambda p: p.pid,
            "name": lambda p: p.name.lower(),
        }

        return sorted(processes, key=key_map[sort_by], reverse=reverse)

    def kill(self, pid: int) -> bool:
        """send SIGKILL to process"""
        try:
            proc = psutil.Process(pid)
            proc.kill()
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False

    def terminate(self, pid: int) -> bool:
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False

    def suspend(self, pid: int) -> bool:
        try:
            proc = psutil.Process(pid)
            proc.suspend()
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False

    def resume(self, pid: int) -> bool:
        try:
            proc = psutil.Process(pid)
            proc.resume()
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False


class CPUMonitor:
    @property
    def percent(self) -> float:
        self._cpu = psutil.cpu_percent()
        return self._cpu


class NetMonitor:
    def __init__(self, size_unit: SystemSizeUnit):
        self._size_unit = size_unit

    @property
    def rx(self) -> float:
        self._net = psutil.net_io_counters()
        return self._net.bytes_recv / SIZE_MULTIPLIERS[self._size_unit]

    @property
    def tx(self) -> float:
        return self._net.bytes_sent / SIZE_MULTIPLIERS[self._size_unit]


class DiskMonitor:
    def __init__(self, size_unit: SystemSizeUnit):
        self._size_unit = size_unit

    @property
    def total(self) -> float:
        self._partitions = psutil.disk_partitions(all=False)
        total = 0
        for part in self._partitions:
            try:
                total += psutil.disk_usage(part.mountpoint).total
            except PermissionError:
                continue
        return total / SIZE_MULTIPLIERS[self._size_unit]

    @property
    def used(self) -> float:
        self._partitions = psutil.disk_partitions(all=False)
        used = 0
        for part in self._partitions:
            try:
                used += psutil.disk_usage(part.mountpoint).used
            except PermissionError:
                continue
        return used / SIZE_MULTIPLIERS[self._size_unit]

    @property
    def free(self) -> float:
        self._partitions = psutil.disk_partitions(all=False)
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
        self._size_unit = size_unit

    @property
    def total(self) -> float:
        self._mem = psutil.virtual_memory()
        return self._mem.total / SIZE_MULTIPLIERS[self._size_unit]

    @property
    def used(self) -> float:
        self._mem = psutil.virtual_memory()
        return self._mem.used / SIZE_MULTIPLIERS[self._size_unit]

    @property
    def free(self) -> float:
        self._mem = psutil.virtual_memory()
        return self._mem.free / SIZE_MULTIPLIERS[self._size_unit]

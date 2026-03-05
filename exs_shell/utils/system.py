from __future__ import annotations
import re
import subprocess

import psutil

from dataclasses import dataclass

from typing import Any, Callable, Optional

from exs_shell.interfaces.types import SystemSizeUnit, ProcessSortBy


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

    def lst(
        self,
        sort_by: ProcessSortBy = "cpu",
        reverse: bool = True,
        filter_name: Optional[str] = None,
        filter_user: Optional[str] = None,
    ) -> list[Process]:
        processes: list[Process] = []

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
        return psutil.cpu_percent()

    @property
    def all(self) -> list[float]:
        """
        :return: list of cpu usage per core
        """
        return psutil.cpu_percent(percpu=True)

    @property
    def cpu(self) -> tuple[float, float | str]:
        return self.percent, self.temperature or "N/A"

    @property
    def cores(self) -> list[tuple[str, float, float | str]]:
        temps = self.temperatures_per_core or []
        loads = self.all

        return [
            (f"C{i}", load, temps[i] if i < len(temps) else ";")
            for i, load in enumerate(loads)
        ]

    @property
    def name(self) -> str:
        try:
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if "model name" in line:
                        return line.split(":")[1].strip()
        finally:
            return "Unknown CPU"

    @property
    def temperature(self) -> float | None:
        cores = self.temperatures_per_core
        if cores:
            return sum(cores) / len(cores)
        return None

    @property
    def temperatures_per_core(self) -> list[float] | None:
        result = self._temps_from_psutil()
        if result:
            return result

        result = self._temps_from_sensors()
        if result:
            return result

        result = self._temps_from_thermal()
        if result:
            return result

        return None

    def _temps_from_psutil(self) -> list[float] | None:
        try:
            temps = psutil.sensors_temperatures()  # type: ignore
        except AttributeError:
            return None
        if not temps:
            return None

        for key in ("coretemp", "k10temp", "zenpower", "cpu_thermal", "acpitz"):
            if key not in temps:
                continue
            entries = temps[key]

            core_entries = sorted(
                [e for e in entries if re.match(r"Core\s*\d+", e.label)],
                key=lambda e: int(re.search(r"\d+", e.label).group()),  # type: ignore
            )
            if core_entries:
                return [e.current for e in core_entries]

            tccd = sorted(
                [e for e in entries if re.match(r"Tccd\d+", e.label)],
                key=lambda e: e.label,
            )
            if tccd:
                return [e.current for e in tccd]

            tctl = next((e for e in entries if e.label in ("Tctl", "Tdie", "")), None)
            if tctl:
                count = psutil.cpu_count(logical=False) or 1
                return [tctl.current] * count

        return None

    def _temps_from_sensors(self) -> list[float] | None:
        try:
            out = subprocess.check_output(
                ["sensors", "-u"],
                stderr=subprocess.DEVNULL,
                timeout=2,
            ).decode()
        except (
            FileNotFoundError,
            subprocess.TimeoutExpired,
            subprocess.CalledProcessError,
        ):
            return None

        temps = []
        current_section = ""

        for line in out.splitlines():
            line = line.strip()

            if not line.startswith(" ") and line.endswith(":"):
                current_section = line.lower()

            if not any(
                k in current_section for k in ("coretemp", "k10temp", "zenpower", "cpu")
            ):
                continue

            match = re.match(r"temp\d+_input:\s*([\d.]+)", line)
            if match:
                temps.append(float(match.group(1)))

        return temps if temps else None

    def _temps_from_thermal(self) -> list[float] | None:
        """Чтение /sys/class/thermal/* — для ARM и embedded"""
        import glob

        temps = []

        for zone in sorted(glob.glob("/sys/class/thermal/thermal_zone*")):
            try:
                with open(f"{zone}/type") as f:
                    zone_type = f.read().strip().lower()
                if not any(k in zone_type for k in ("cpu", "x86", "soc")):
                    continue
                with open(f"{zone}/temp") as f:
                    temps.append(int(f.read().strip()) / 1000.0)
            except Exception:
                continue

        return temps if temps else None


class NetMonitor:
    def __init__(self, size_unit: SystemSizeUnit):
        self._size_unit = size_unit

    @property
    def all(self) -> tuple[float, float]:
        """
        :return: received, sent
        """
        _net = psutil.net_io_counters()
        return (
            _net.bytes_recv / SIZE_MULTIPLIERS[self._size_unit],
            _net.bytes_sent / SIZE_MULTIPLIERS[self._size_unit],
        )

    @property
    def rx(self) -> float:
        return self.all[0]

    @property
    def tx(self) -> float:
        return self.all[1]


class DiskMonitor:
    def __init__(self, size_unit: SystemSizeUnit):
        self._size_unit = size_unit

    @property
    def all(self) -> tuple[float, float, float]:
        """
        :return: total, used, free
        """
        _partitions = psutil.disk_partitions(all=False)
        total = 0
        used = 0
        free = 0
        for part in _partitions:
            try:
                usage = psutil.disk_usage(part.mountpoint)
                total += usage.total
                used += usage.used
                free += usage.free
            except PermissionError:
                continue
        return (
            total / SIZE_MULTIPLIERS[self._size_unit],
            used / SIZE_MULTIPLIERS[self._size_unit],
            free / SIZE_MULTIPLIERS[self._size_unit],
        )

    @property
    def total(self) -> float:
        return self.all[0]

    @property
    def used(self) -> float:
        return self.all[1]

    @property
    def free(self) -> float:
        return self.all[2]

    @property
    def percent(self) -> float:
        data = self.all
        t = data[0]
        u = data[1]
        return (u / t) * 100


class MemoryMonitor:
    def __init__(self, size_unit: SystemSizeUnit):
        self._size_unit = size_unit

    @property
    def all(self) -> tuple[float, float, float, float, float]:
        """
        :return: total, used, free, cached, available
        """
        _mem = psutil.virtual_memory()
        return (
            _mem.total / SIZE_MULTIPLIERS[self._size_unit],
            _mem.used / SIZE_MULTIPLIERS[self._size_unit],
            _mem.free / SIZE_MULTIPLIERS[self._size_unit],
            _mem.cached / SIZE_MULTIPLIERS[self._size_unit],
            _mem.available / SIZE_MULTIPLIERS[self._size_unit],
        )

    @property
    def total(self) -> float:
        return self.all[0]

    @property
    def used(self) -> float:
        return self.all[1]

    @property
    def free(self) -> float:
        return self.all[2]

    @property
    def cached(self) -> float:
        return self.all[3]

    @property
    def available(self) -> float:
        return self.all[4]

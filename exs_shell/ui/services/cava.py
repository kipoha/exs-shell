import os
import struct
import subprocess

from typing import Callable

from exs_shell import register
from exs_shell.utils import Dirs, Paths
from exs_shell.utils.proc import set_death_signal
from exs_shell.utils.loop import run_in_thread

from gi.repository import GLib  # type: ignore


@register.service
class Cava:
    def __init__(self, fifo_path=f"{Dirs.TEMP_DIR}/cava.fifo", bars=20):
        self.fifo_path = fifo_path
        self.bars = bars
        self.byte_size = 2
        self.byte_norm = 65535
        self.proc: subprocess.Popen | None = None
        self._subscribers_text: list[Callable] = []
        self._subscribers_values: list[Callable] = []

        if not os.path.exists(self.fifo_path):
            os.mkfifo(self.fifo_path)

        self._running = True

        self._start_cava()
        self._start_reader()

    def subscribe_text(self, callback: Callable):
        if callback not in self._subscribers_text:
            self._subscribers_text.append(callback)

    def subscribe_values(self, callback: Callable):
        if callback not in self._subscribers_values:
            self._subscribers_values.append(callback)

    def unsubscribe_text(self, callback: Callable):
        if callback in self._subscribers_text:
            self._subscribers_text.remove(callback)

    def unsubscribe_values(self, callback: Callable):
        if callback in self._subscribers_values:
            self._subscribers_values.remove(callback)

    @run_in_thread
    def _start_cava(self):
        config = Paths.generate_path("configs/other/cava/cava.ini")
        try:
            self.proc = subprocess.Popen(
                ["cava", "-p", config],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=set_death_signal,
            )
            self.proc.wait()

        except Exception:
            pass

    def __del__(self):
        self._running = False
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()

    @run_in_thread
    def _start_reader(self):
        while not os.path.exists(self.fifo_path) and self._running:
            GLib.usleep(100_000)

        try:
            self.fd = os.open(self.fifo_path, os.O_RDONLY | os.O_NONBLOCK)
            GLib.io_add_watch(self.fd, GLib.IO_IN, self._read_data)
        except Exception:
            self.fd = None

    def _read_data(self, source: int, condition: int):
        chunk = self.bars * self.byte_size
        try:
            data = os.read(self.fd, chunk)  # type: ignore
            if len(data) < chunk:
                return True
        except BlockingIOError:
            return True
        except OSError:
            return False

        values = struct.unpack(f"{self.bars}H", data)
        values = [v / self.byte_norm for v in values]
        visual_text = self._make_visual(values)

        GLib.idle_add(self._notify_subscribers_values, values)
        GLib.idle_add(self._notify_subscribers_text, visual_text)
        return True

    def _make_visual(self, values: list[float]) -> str:
        # blocks = "⣀⣄⣤⣦⣶⣷⣿"

        blocks = "▁▂▃▄▅▆▇█"
        result = []
        for v in values:
            idx = min(int(v * (len(blocks) - 1)), len(blocks) - 1)
            result.append(blocks[idx])
        return "".join(result)

    def _notify_subscribers_text(self, visual: str):
        for callback in self._subscribers_text:
            callback(visual)

    def _notify_subscribers_values(self, values: list[float]):
        for callback in self._subscribers_values:
            callback(values)

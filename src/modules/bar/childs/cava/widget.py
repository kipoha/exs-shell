import os
import struct
import subprocess
import threading
from typing import Callable

from ignis import widgets

from utils import Dirs, PathUtils

from base.singleton import SingletonClass

from gi.repository import GLib  # type: ignore

# blocks = "⠁⠂⠄⡀⣀⣠⣤⣦⣶⣷⣿"
# blocks = " ▁▂▃▄▅▆▇█"
# blocks = "🔈🔉🔊"
# blocks = "░▒▓█"
# blocks = "▏▎▍▌▋▊▉█"
# blocks = "·•●"
# blocks = "─═█"
# blocks = "﹅﹆﹇﹈﹉﹊﹋﹌"
# blocks = "ᚋᚏᚐᚑᚔᚖᚘᚙ"
# blocks = ".:*oO8@"
# blocks = "⣀⣄⣤⣦⣶⣷⣿"


class CavaManager(SingletonClass):
    def __init__(self, fifo_path=f"{Dirs.TEMP_DIR}/cava.fifo", bars=20):
        self.fifo_path = fifo_path
        self.bars = bars
        self.byte_size = 2
        self.byte_norm = 65535
        self.proc: subprocess.Popen | None = None
        self._subscribers: list[Callable] = []

        if not os.path.exists(self.fifo_path):
            os.mkfifo(self.fifo_path)

        self._running = True

        self._cava_thread = threading.Thread(target=self._start_cava, daemon=True)
        self._cava_thread.start()

        self._reader_thread = threading.Thread(target=self._start_reader, daemon=True)
        self._reader_thread.start()

    def subscribe(self, callback: Callable):
        """Подписка виджета на обновления визуала"""
        if callback not in self._subscribers:
            self._subscribers.append(callback)

    def unsubscribe(self, callback: Callable):
        if callback in self._subscribers:
            self._subscribers.remove(callback)

    def _start_cava(self):
        config = PathUtils.generate_path("config/other/cava/cava.ini")
        try:
            self.proc = subprocess.Popen(
                ["cava", "-p", config],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            self.proc.wait()
        except Exception:
            pass

    def __del__(self):
        self._running = False
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()

    def _start_reader(self):
        while not os.path.exists(self.fifo_path) and self._running:
            GLib.usleep(100_000)

        try:
            self.fd = os.open(self.fifo_path, os.O_RDONLY | os.O_NONBLOCK)
            GLib.io_add_watch(self.fd, GLib.IO_IN, self._read_data)
        except Exception:
            self.fd = None

    def _read_data(self, source, condition):
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
        visual = self._make_visual(values)
        GLib.idle_add(self._notify_subscribers, visual)
        return True

    def _make_visual(self, values):
        # blocks = "⣀⣄⣤⣦⣶⣷⣿"

        blocks = "▁▂▃▄▅▆▇█"
        result = []
        for v in values:
            idx = min(int(v * (len(blocks) - 1)), len(blocks) - 1)
            result.append(blocks[idx])
        return "".join(result)

    def _notify_subscribers(self, visual):
        for callback in self._subscribers:
            callback(visual)


class Cava(widgets.Label):
    def __init__(self, **kwargs):
        super().__init__(label="", css_classes=["cava"], **kwargs)
        manager = CavaManager.get_default()
        manager.subscribe(self._update_label)

    def _update_label(self, visual):
        self.label = visual

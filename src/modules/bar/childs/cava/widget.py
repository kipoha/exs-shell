import os
import struct
import subprocess
import threading

from ignis import widgets

from utils import Dirs, PathUtils

from gi.repository import GLib  # type: ignore


class Cava(widgets.Label):
    def __init__(self, fifo_path=f"{Dirs.TEMP_DIR}/cava.fifo", bars=20, **kwargs):
        super().__init__(label="", css_classes=["cava"], **kwargs)

        self.fifo_path = fifo_path
        self.bars = bars
        self.byte_size = 2
        self.byte_norm = 65535
        self.proc: subprocess.Popen | None = None

        if not os.path.exists(self.fifo_path):
            os.mkfifo(self.fifo_path)

        self._cava_thread = threading.Thread(target=self._start_cava, daemon=True)
        self._cava_thread.start()

        self._reader_thread = threading.Thread(target=self._start_reader, daemon=True)
        self._reader_thread.start()

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
        if self.proc and self._check_proc():
            self.proc.terminate()

    def _check_proc(self):
        if self.proc and self.proc.poll() is not None:
            self.proc = None
            return False
        return True

    def _start_reader(self):
        while not os.path.exists(self.fifo_path) and self._running:
            GLib.usleep(100_000)

        try:
            self.fd = os.open(self.fifo_path, os.O_RDONLY | os.O_NONBLOCK)
            self._watch_id = GLib.io_add_watch(self.fd, GLib.IO_IN, self._read_data)
        except Exception:
            self.fd = None

    def _read_data(self, source, condition):
        chunk = self.bars * self.byte_size
        try:
            data = os.read(self.fd, chunk)
            if len(data) < chunk:
                return True
        except BlockingIOError:
            return True
        except OSError:
            return False

        values = struct.unpack(f"{self.bars}H", data)
        values = [v / self.byte_norm for v in values]
        visual = self._make_visual(values)
        GLib.idle_add(self._update_label, visual)
        return True

    def _make_visual(self, values):
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
        blocks = "⣀⣄⣤⣦⣶⣷⣿"
        result = []
        for v in values:
            # idx = min(int(v * (len(blocks) - 1) * 3), len(blocks) - 1)
            idx = min(int(v * (len(blocks) - 1)), len(blocks) - 1)
            result.append(blocks[idx])
        return "".join(result)

    def _update_label(self, visual):
        self.label = visual

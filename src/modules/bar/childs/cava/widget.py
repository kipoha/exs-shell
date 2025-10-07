import os
import struct
import subprocess

from ignis import utils, widgets

from gi.repository import GLib  # type: ignore


class Cava(widgets.Label):
    def __init__(self, fifo_path="/tmp/cava.fifo", bars=20, **kwargs):
        super().__init__(label="", css_classes=["cava"], **kwargs)
        self.fifo_path = fifo_path
        self.bars = bars
        self.byte_size = 2
        self.byte_norm = 65535
        self.proc = None

        if not os.path.exists(self.fifo_path):
            os.mkfifo(self.fifo_path)

        self._start_cava()
        self._start_reader()

    def _start_cava(self):
        config = os.path.expanduser("~/.config/exs-shell/src/config/other/cava/cava.ini")
        self.proc = subprocess.Popen(
            ["cava", "-p", config],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def _start_reader(self):
        self.fd = os.open(self.fifo_path, os.O_RDONLY | os.O_NONBLOCK)
        GLib.io_add_watch(self.fd, GLib.IO_IN, self._read_data)

    def _read_data(self, source, condition):
        chunk = self.bars * self.byte_size
        try:
            data = os.read(self.fd, chunk)
        except BlockingIOError:
            return True

        if len(data) < chunk:
            return True

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
            idx = min(int(v * (len(blocks) - 1) * 3), len(blocks) - 1)
            result.append(blocks[idx])
        return "".join(result)

    def _update_label(self, visual):
        self.label = visual

    def destroy(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
        if hasattr(self, "fd"):
            os.close(self.fd)
        super().destroy()

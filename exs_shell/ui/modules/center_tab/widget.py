import psutil
from gi.repository import Gtk, GLib  # type: ignore
import collections
from ignis.widgets import RegularWindow


# mem = psutil.virtual_memory().percent
# cpu = psutil.cpu_percent()
# disk = psutil.disk_usage('/').percent
# net = psutil.net_io_counters().bytes_recv
# proc = len(psutil.pids())

class Graph(Gtk.DrawingArea):
    def __init__(self):
        super().__init__()
        self.history = collections.deque(maxlen=100)
        self.set_draw_func(self.on_draw)

        GLib.timeout_add(1000, self.update)

    def update(self):
        value = psutil.cpu_percent()
        self.history.append(value)
        self.queue_draw()
        return True

    def on_draw(self, area, cr, width, height):
        cr.set_line_width(2)

        if not self.history:
            return

        step = width / len(self.history)

        for i, value in enumerate(self.history):
            x = i * step
            y = height - (value / 100) * height

            if i == 0:
                cr.move_to(x, y)
            else:
                cr.line_to(x, y)

        cr.stroke()


class CenterTab(RegularWindow):
    def __init__(self):
        super().__init__("Center Tab")
        self.set_child(CpuGraph())

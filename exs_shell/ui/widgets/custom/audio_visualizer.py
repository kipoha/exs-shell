from math import pi

from gi.repository import Gtk, GLib  # type: ignore

from ignis import widgets

from exs_shell import register
from exs_shell.state import State
from exs_shell.utils.colors import get_hex_color, hex_to_rgb
from exs_shell.ui.services.cava import Cava


@register.event
class AudioVisualizer(widgets.Box):
    def __init__(self, width: int = 220, height: int = 30, mirror: bool = False, **kwargs):
        super().__init__(vertical=False, spacing=2, **kwargs)
        self.width = width
        self.height = height
        self.mirror = mirror
        self.cava: Cava = State.services.cava
        self.bars = self.cava.bars

        self.audio_sample = [0] * self.bars

        self.area = Gtk.DrawingArea()
        self.area.set_size_request(self.width, self.height)
        self.area.set_draw_func(self.redraw)
        self.area.add_css_class("dashboard-widget-audio-visualizer")
        self.append(self.area)

        self.cava.subscribe_values(self.update_bars)

    @register.events.cava("values")
    def update_bars(self, values):
        self.audio_sample = values
        GLib.idle_add(self.area.queue_draw)

    def build(self, area, cr, width, height):
        hex_color = get_hex_color()
        accent_r, accent_g, accent_b = hex_to_rgb(hex_color)
        cr.set_source_rgb(accent_r, accent_g, accent_b)
        bar_width = width / self.bars
        padding = 2
        radius = 3

        for i, val in enumerate(self.audio_sample):
            h = max(2, int(val * height))
            idx = self.bars - 1 - i if self.mirror else i
            x = idx * bar_width
            y = height - h

            cr.move_to(x + padding / 2 + radius, y)
            cr.line_to(x + bar_width - padding - radius, y)
            cr.arc(x + bar_width - padding - radius, y + radius, radius, -pi / 2, 0)
            cr.line_to(x + bar_width - padding, y + h - radius)
            cr.arc(x + bar_width - padding - radius, y + h - radius, radius, 0, pi / 2)
            cr.line_to(x + padding / 2 + radius, y + h)
            cr.arc(x + padding / 2 + radius, y + h - radius, radius, pi / 2, pi)
            cr.line_to(x + padding / 2, y + radius)
            cr.arc(x + padding / 2 + radius, y + radius, radius, pi, 3 * pi / 2)
            cr.close_path()

        cr.fill()

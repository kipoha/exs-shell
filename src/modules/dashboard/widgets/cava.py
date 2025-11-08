import re

from math import pi

from gi.repository import Gtk, GLib  # type: ignore

from ignis import widgets

from modules.bar.childs.cava.widget import CavaManager

from utils.path import PathUtils


scss_file = PathUtils.generate_path("colors.scss")


class AudioVisualizer(widgets.Box):
    def __init__(self, width: int = 220, height: int = 30, mirror: bool = False):
        super().__init__(vertical=False, spacing=2)
        self.width = width
        self.height = height
        self.mirror = mirror
        self.cava = CavaManager.get_default()
        self.bars = self.cava.bars

        self.audio_sample = [0] * self.bars

        self.area = Gtk.DrawingArea()
        self.area.set_size_request(self.width, self.height)
        self.area.set_draw_func(self.redraw)
        self.area.add_css_class("dashboard-widget-audio-visualizer")
        self.append(self.area)

        self.cava.subscribe_values(self.update_bars)

    def update_bars(self, values):
        self.audio_sample = values
        GLib.idle_add(self.area.queue_draw)

    def get_hex_color(self) -> str:
        variables = {}
        with open(scss_file, "r") as f:
            for line in f:
                m = re.match(r"\s*\$(\w+):\s*(.+?);", line)
                if m:
                    var_name, value = m.groups()
                    variables[var_name] = value
        return variables["accent"]

    def hex_to_rgb1(self, hex_color: str):
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16) / 255
        g = int(hex_color[2:4], 16) / 255
        b = int(hex_color[4:6], 16) / 255
        return r, g, b

    def redraw(self, area, cr, width, height):
        hex_color = self.get_hex_color()
        accent_r, accent_g, accent_b = self.hex_to_rgb1(hex_color)
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

import cairo
import psutil
from ignis import widgets
from gi.repository import Gtk, GLib  # type: ignore
from math import pi

from exs_shell_deprecated.utils.colors import get_hex_color, hex_to_rgb


class CircularMeter(Gtk.DrawingArea):
    def __init__(
        self,
        radius: int = 80,
        thickness: int = 20,
        speed: float = 0.5,
        label: str = "",
    ):
        super().__init__()
        self.radius = radius
        self.thickness = thickness
        self.value = 0.0
        self.target_value = 0.0
        self.speed = speed
        self.label = label
        self.percentage = 0

        self.set_size_request(radius * 2 + thickness * 2, radius * 2 + thickness * 2)
        self.set_draw_func(self.redraw)

        GLib.timeout_add(30, self.animate)

    def set_value(self, value: float):
        self.target_value = max(0, min(1, value))
        self.percentage = int(self.target_value * 100)

    def animate(self):
        if abs(self.value - self.target_value) < 0.001:
            self.value = self.target_value
        else:
            self.value += (self.target_value - self.value) * self.speed
            self.queue_draw()
        return True

    def redraw(self, area, cr, width, height):
        hex_color = get_hex_color()
        accent_r, accent_g, accent_b = hex_to_rgb(hex_color)
        cx, cy = width / 2, height / 2
        cr.set_line_width(self.thickness)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)

        cr.set_source_rgba(0.2, 0.2, 0.2, 0.5)
        cr.arc(cx, cy, self.radius, 0, 2 * pi)
        cr.stroke()

        cr.set_source_rgb(accent_r, accent_g, accent_b)
        cr.arc(cx, cy, self.radius, -pi / 2, -pi / 2 + 2 * pi * self.value)
        cr.stroke()

        text = f"{self.label} {self.percentage}%"
        cr.set_source_rgb(accent_r, accent_g, accent_b)
        font_size = self.radius / 2.5
        cr.select_font_face(
            "JetBrainsMono Nerd Font", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD
        )
        cr.set_font_size(font_size)

        xbearing, ybearing, text_width, text_height, xadvance, yadvance = (
            cr.text_extents(text)
        )
        cr.move_to(cx - text_width / 2 - xbearing, cy - text_height / 2 - ybearing)
        cr.show_text(text)


class SystemMonitor(widgets.Box):
    def __init__(self):
        super().__init__(
            spacing=10,
            css_classes=["dashboard-widget-system-monitor"],
            valign="center",
            halign="center",
            vexpand=True,
            hexpand=True,
        )

        self.ram_meter = CircularMeter(label="", radius=90, thickness=22)
        self.cpu_meter = CircularMeter(label="", radius=110, thickness=25)
        self.disk_meter = CircularMeter(label="")

        self.append(self.ram_meter)
        self.append(self.cpu_meter)
        self.append(self.disk_meter)

        GLib.timeout_add(1000, self.update_metrics)

    def update_metrics(self):
        self.cpu_meter.set_value(psutil.cpu_percent() / 100)
        self.ram_meter.set_value(psutil.virtual_memory().percent / 100)
        self.disk_meter.set_value(psutil.disk_usage("/").percent / 100)
        return True

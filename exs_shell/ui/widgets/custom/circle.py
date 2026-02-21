import cairo

from math import pi

from gi.repository import Gtk, GLib, Pango, PangoCairo  # type: ignore

from exs_shell.utils.colors import get_hex_color, hex_to_rgb


class ArcMeter(Gtk.DrawingArea):
    def __init__(
        self,
        size: int = 200,
        thickness: int = 20,
        arc_ratio: float = 0.75,
        speed: float = 0.15,
        label: str = "",
        show_percentage: bool = False,
        font_size: float | None = None,
        css_classes: list[str] | None = None,
    ):
        Gtk.DrawingArea.__init__(self)

        self.size = size
        self.radius = size / 2
        self.thickness = thickness
        self.arc_ratio = arc_ratio
        self.speed = speed
        self.label = label

        self.value = 0.0
        self.target_value = 0.0
        self.percentage = 0
        self.show_percentage = show_percentage
        self.font_size = font_size

        self.set_size_request(size, size)
        self.set_draw_func(self.redraw)

        if css_classes:
            for css_class in css_classes:
                self.add_css_class(css_class)

        GLib.timeout_add(30, self.animate)

    def set_value(self, value: float):
        self.target_value = max(0.0, min(1.0, value))
        self.percentage = int(self.target_value * 100)
        self.queue_draw()

    def get_value(self):
        return self.value

    def animate(self):
        if abs(self.value - self.target_value) < 0.001:
            self.value = self.target_value
        else:
            self.value += (self.target_value - self.value) * self.speed
            self.queue_draw()
        return True

    def redraw(self, area, cr: cairo.Context, width: int, height: int):
        _colors = get_hex_color()
        hex_color = _colors["primary"]
        void_color = _colors["surface_container_highest"]

        cx, cy = width / 2, height / 2

        cr.set_line_width(self.thickness)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)

        total_arc = 2 * pi * self.arc_ratio
        start_angle = -pi / 2 - total_arc / 2
        end_angle = start_angle + total_arc

        r_void, g_void, b_void = hex_to_rgb(void_color)
        cr.set_source_rgb(r_void, g_void, b_void)
        cr.arc(cx, cy, self.radius - self.thickness, start_angle, end_angle)
        cr.stroke()

        r, g, b = hex_to_rgb(hex_color)
        cr.set_source_rgb(r, g, b)

        progress_end = start_angle + total_arc * self.value
        cr.arc(cx, cy, self.radius - self.thickness, start_angle, progress_end)
        cr.stroke()

        text = f"{self.label}"
        if self.show_percentage:
            text += f" {self.percentage}%"

        layout = PangoCairo.create_layout(cr)
        layout.set_text(text, -1)

        font_desc = Pango.FontDescription()

        font_desc.set_family(
            "Material Symbols Rounded, Material Icons Rounded, JetBrainsMono"
        )

        font_desc.set_weight(Pango.Weight.BOLD)

        font_size = self.font_size or self.radius / 3
        font_desc.set_absolute_size(font_size * Pango.SCALE)

        layout.set_font_description(font_desc)

        # Центрирование
        tw, th = layout.get_pixel_size()

        cr.set_source_rgb(r, g, b)
        cr.move_to(cx - tw / 2, cy - th / 2)
        PangoCairo.show_layout(cr, layout)

import collections
import cairo

from gi.repository import Gtk, Pango, PangoCairo

from exs_shell.interfaces.types import RGB, RGBA


class MultiGraph(Gtk.DrawingArea):
    def __init__(
        self,
        max_points: int = 100,
        min_value: float = 0,
        max_value: float = 100,
        unit: str = "",
        autoscale: bool = False,
        line_colors: list[RGB] | None = None,
        grid_color: RGBA = (0.5, 0.5, 0.5, 0.2),
        text_color: RGB = (1, 1, 1),
        font_size: int = 10,
        padding: int = 16,
    ):
        super().__init__()
        self.max_points = max_points
        self.min_value = min_value
        self.max_value = max_value
        self.autoscale = autoscale
        self.unit = unit
        self.grid_color = grid_color
        self.text_color = text_color
        self.font_size = font_size
        self.padding = padding

        if line_colors is None:
            line_colors = [(0.2, 0.8, 1.0)]
        self.line_colors = line_colors

        self.histories = [
            collections.deque([min_value] * max_points, maxlen=max_points)
            for _ in self.line_colors
        ]

        self.set_draw_func(self.on_draw)

    def push(self, values: list[float]):
        for hist, val in zip(self.histories, values):
            hist.append(val)
        self.queue_draw()

    def on_draw(self, _, cr: cairo.Context, width: int, height: int):
        pad = self.padding
        usable_height = height - pad * 2

        all_values = [v for hist in self.histories for v in hist]
        if self.autoscale:
            min_v = min(all_values)
            max_v = max(all_values)
            if min_v == max_v:
                max_v += 1
        else:
            min_v = self.min_value
            max_v = self.max_value
        value_range = max_v - min_v
        if value_range == 0:
            value_range = 1

        step_x = width / (self.max_points - 1)

        cr.set_line_width(1)
        cr.set_source_rgba(*self.grid_color)
        grid_lines = 4
        for i in range(grid_lines + 1):
            y = pad + i * usable_height / grid_lines
            cr.move_to(4, height - y)
            cr.line_to(width, height - y)
            cr.stroke()

            val = min_v + (value_range * i / grid_lines)
            val_text = f"{val:.1f}" + (f" {self.unit}" if self.unit else "")
            self._draw_text(cr, val_text, 4, height - y - self.font_size - 4)

        for idx, hist in enumerate(self.histories):
            cr.set_line_width(2)
            cr.set_source_rgb(*self.line_colors[idx])
            values = list(hist)
            for i, value in enumerate(values):
                x = i * step_x
                y = pad + ((value - min_v) / value_range) * usable_height
                y = height - y
                if i == 0:
                    cr.move_to(x, y)
                else:
                    cr.line_to(x, y)
            cr.stroke()

    def _draw_text(self, cr: cairo.Context, text: str, x: float, y: float):
        layout = PangoCairo.create_layout(cr)
        layout.set_text(text, -1)
        font_desc = Pango.FontDescription()
        font_desc.set_family("JetBrainsMono")
        font_desc.set_absolute_size(self.font_size * Pango.SCALE)
        layout.set_font_description(font_desc)
        cr.set_source_rgb(*self.text_color)
        cr.move_to(x, y)
        PangoCairo.show_layout(cr, layout)


class Graph(Gtk.DrawingArea):
    def __init__(
        self,
        max_points: int = 100,
        min_value: float = 0,
        max_value: float = 100,
        unit: str = "",
        autoscale: bool = False,
        line_color: RGB = (0.2, 0.8, 1.0),
        grid_color: RGBA = (0.5, 0.5, 0.5, 0.2),
        text_color: RGB = (1, 1, 1),
        font_size: int = 10,
        padding: int = 16,
    ):
        super().__init__()

        self.max_points = max_points
        self.min_value = min_value
        self.max_value = max_value
        self.autoscale = autoscale

        self.line_color = line_color
        self.grid_color = grid_color
        self.text_color = text_color
        self.font_size = font_size
        self.padding = padding
        self.unit = unit

        self.history = collections.deque([min_value] * max_points, maxlen=max_points)

        self.set_draw_func(self.on_draw)

    def push(self, value: float):
        self.history.append(value)
        self.queue_draw()

    def on_draw(self, _, cr: cairo.Context, width: int, height: int):
        if not self.history:
            return

        pad = self.padding

        usable_height = height - pad * 2

        values = list(self.history)

        if self.autoscale:
            min_v = min(values)
            max_v = max(values)
            if min_v == max_v:
                max_v += 1
        else:
            min_v = self.min_value
            max_v = self.max_value

        value_range = max_v - min_v
        if value_range == 0:
            value_range = 1

        step_x = width / (len(values) - 1)

        cr.set_line_width(1)
        cr.set_source_rgba(*self.grid_color)

        grid_lines = 4
        for i in range(grid_lines + 1):
            y = height - pad - (i / grid_lines) * usable_height

            cr.move_to(4, y)
            cr.line_to(width, y)
            cr.stroke()

            val = min_v + (value_range * i / grid_lines)
            val_text = f"{val:.1f}"
            if self.unit:
                val_text += f" {self.unit}"
            self._draw_text(cr, val_text, 4, y - self.font_size - 4)

        cr.set_line_width(2)
        cr.set_source_rgb(*self.line_color)

        for i, value in enumerate(values):
            x = i * step_x
            y = height - pad - ((value - min_v) / value_range) * usable_height

            if i == 0:
                cr.move_to(x, y)
            else:
                cr.line_to(x, y)

        cr.stroke()

    def _draw_text(self, cr: cairo.Context, text: str, x: float, y: float):
        layout = PangoCairo.create_layout(cr)
        layout.set_text(text, -1)

        font_desc = Pango.FontDescription()
        font_desc.set_family("JetBrainsMono")
        font_desc.set_absolute_size(self.font_size * Pango.SCALE)
        layout.set_font_description(font_desc)

        cr.set_source_rgb(*self.text_color)
        cr.move_to(x, y)
        PangoCairo.show_layout(cr, layout)

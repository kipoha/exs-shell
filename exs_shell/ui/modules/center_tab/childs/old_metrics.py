import math
from typing import Any
from gi.repository import GLib  # type: ignore

from ignis.widgets import Box, Button, Separator, Label

from exs_shell import register
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.ui.widgets.custom.graph import Graph, MultiGraph
from exs_shell.ui.widgets.custom.icon import Icon
from exs_shell.utils.colors import hex_to_rgb, get_hex_color
from exs_shell.utils.system import DiskMonitor, CPUMonitor, MemoryMonitor, NetMonitor, ProcessMonitor


h = 300
w = 700

MAIN_GRAPH_H = 100
PADDING = 6
LABEL_W = 40
TEMP_W = 50


@register.event
class CPU(Box):
    def __init__(self, **kwargs: Any):
        self.cpu = CPUMonitor()

        colors = get_hex_color()
        self.primary = hex_to_rgb(colors["primary"])
        self.primary_hex = colors["primary"]

        self.core_graphs: list[Graph] = []
        self.core_temp_labels: list[Label] = []

        super().__init__(
            vertical=True,
            spacing=PADDING,
            child=[
                self._build_header(),
                self._build_main(),
                self._build_cores(),
            ],
            **kwargs,
        )

    def _build_header(self) -> Label:
        self.name_label = Label(
            label=self.cpu.name,
            halign="start",
        )
        return self.name_label

    def _build_main(self) -> Box:
        self.main_graph = Graph(
            line_color=self.primary,
            text_color=self.primary,
            unit="%",
        )
        self.main_graph.set_size_request(w - TEMP_W - PADDING, MAIN_GRAPH_H)

        percent, temp = self.cpu.cpu
        self.main_graph.push(percent)

        self.main_temp_label = Label(
            label=self._fmt_temp(temp),
            valign="center",
        )
        self.main_temp_label.set_size_request(TEMP_W, -1)

        return Box(
            spacing=PADDING,
            child=[self.main_graph, self.main_temp_label],
        )

    def _build_cores(self) -> Box:
        cores = self.cpu.cores
        n = len(cores)
        cols = self._calc_cols(n)

        available_h = h - MAIN_GRAPH_H - PADDING * 4 - 24
        core_w = w // cols - PADDING
        core_h = available_h // math.ceil(n / cols) - PADDING

        rows_widgets: list[Box] = []
        row_children: list[Box] = []

        for i, (label, load, temp) in enumerate(cores):
            cell = self._make_core_cell(label, load, temp, core_w, core_h)
            row_children.append(cell)

            if len(row_children) == cols or i == n - 1:
                rows_widgets.append(Box(spacing=PADDING, child=list(row_children)))
                row_children.clear()

        return Box(vertical=True, spacing=PADDING, child=rows_widgets)

    def _make_core_cell(
        self, label: str, load: float, temp: float | str, w: int, h: int
    ) -> Box:
        lbl = Label(label=label, valign="center")
        lbl.set_size_request(LABEL_W, -1)

        graph = Graph(
            line_color=self.primary,
            text_color=self.primary,
            unit="%",
            font_size=8,
            padding=8,
        )
        graph.set_size_request(w - LABEL_W - TEMP_W - PADDING * 2, h)
        graph.push(load)
        self.core_graphs.append(graph)

        temp_lbl = Label(label=self._fmt_temp(temp), valign="center")
        temp_lbl.set_size_request(TEMP_W, -1)
        self.core_temp_labels.append(temp_lbl)

        return Box(spacing=2, child=[lbl, graph, temp_lbl])

    def _calc_cols(self, n: int) -> int:
        available_h = h - MAIN_GRAPH_H - PADDING * 4 - 24
        best = 1
        for cols in range(1, n + 1):
            rows = math.ceil(n / cols)
            if w // cols - PADDING >= 120 and available_h // rows - PADDING >= 40:
                best = cols
        return best

    def _fmt_temp(self, temp: float | str) -> str:
        return f"{temp:.0f}°" if isinstance(temp, float) else str(temp)

    @register.events.poll(1000)
    def _update(self) -> None:
        percent, temp = self.cpu.cpu
        self.main_graph.push(percent)
        self.main_temp_label.set_label(self._fmt_temp(temp))

        for i, (_, load, temp) in enumerate(self.cpu.cores):
            self.core_graphs[i].push(load)
            self.core_temp_labels[i].set_label(self._fmt_temp(temp))


class Memory(Box):
    def __init__(self, **kwargs: Any):
        self.mem = MemoryMonitor("GB")
        colors = get_hex_color()
        primary_hex = colors["primary"]
        on_tertiary_container_hex = colors["on_tertiary_container"]
        surface_variant_hex = colors["surface_variant"]
        primary = hex_to_rgb(primary_hex)
        on_tertiary_container = hex_to_rgb(on_tertiary_container_hex)
        self.graph = Graph(
            max_value=self.mem.total,
            line_color=primary,
            text_color=primary,
            unit="GB",
        )
        self.graph.set_size_request(w, h)
        super().__init__(**kwargs)


class Disk(Box):
    def __init__(self, **kwargs: Any):
        self.disk = DiskMonitor("GB")
        colors = get_hex_color()
        primary_hex = colors["primary"]
        on_tertiary_container_hex = colors["on_tertiary_container"]
        surface_variant_hex = colors["surface_variant"]
        primary = hex_to_rgb(primary_hex)
        on_tertiary_container = hex_to_rgb(on_tertiary_container_hex)
        self.graph = Graph(
            max_value=self.disk.total,
            line_color=primary,
            text_color=primary,
            unit="GB",
        )
        self.graph.set_size_request(w, h)
        super().__init__(**kwargs)


class Network(Box):
    def __init__(self, **kwargs: Any):
        self.net = NetMonitor("MB")
        colors = get_hex_color()
        primary_hex = colors["primary"]
        on_tertiary_container_hex = colors["on_tertiary_container"]
        surface_variant_hex = colors["surface_variant"]
        primary = hex_to_rgb(primary_hex)
        on_tertiary_container = hex_to_rgb(on_tertiary_container_hex)
        self.graph = MultiGraph(
            line_colors=[primary, on_tertiary_container],
            text_color=primary,
            autoscale=True,
            unit="MB",
        )
        self.graph.set_size_request(w, h - 18)
        super().__init__(**kwargs)


class Processers(Box): ...


class MonitorTab(Box):
    def __init__(self):
        self.mem = MemoryMonitor("GB")
        self.disk = DiskMonitor("GB")
        self.net = NetMonitor("MB")
        self.cpu = CPUMonitor()
        colors = get_hex_color()
        primary_hex = colors["primary"]
        on_tertiary_container_hex = colors["on_tertiary_container"]
        surface_variant_hex = colors["surface_variant"]
        primary = hex_to_rgb(primary_hex)
        on_tertiary_container = hex_to_rgb(on_tertiary_container_hex)
        self.active = Icons.ui.CPU
        self.mem_graph = Graph(
            max_value=self.mem.total,
            line_color=primary,
            text_color=primary,
            unit="GB",
        )
        self.cpu_graph = Graph(
            line_color=primary,
            text_color=primary,
            unit="%",
        )
        self.disk_graph = Graph(
            line_color=primary,
            text_color=primary,
            max_value=self.disk.total,
            unit="GB",
        )
        self.net_graph = MultiGraph(
            line_colors=[primary, on_tertiary_container],
            text_color=primary,
            autoscale=True,
            unit="MB",
        )
        self.mem_graph.set_size_request(w, h)
        self.cpu_graph.set_size_request(w, h)
        self.disk_graph.set_size_request(w, h)
        self.net_graph.set_size_request(w, h - 18)
        self.metrics: dict[str, Box] = {
            # Icons.ui.CPU: Box(child=[self.cpu_graph]),
            Icons.ui.CPU: CPU(),
            Icons.ui.MEMORY: Box(child=[self.mem_graph]),
            Icons.ui.STORAGE: Box(child=[self.disk_graph]),
            Icons.ui.NETWORK: Box(
                vertical=True,
                child=[
                    self.net_graph,
                    Box(
                        spacing=5,
                        child=[
                            Box(
                                spacing=8,
                                child=[
                                    Separator(
                                        css_classes=["exs-center-tab-metrics-line"],
                                        style=f"background-color: {primary_hex}; min-width: 2.5rem; min-height: .1rem; border-radius: 1rem; margin: 0.5rem 0.01rem;",
                                    ),
                                    Label(
                                        label="- Received",
                                        css_classes=["exs-center-tab-metrics-label"],
                                    ),
                                ],
                            ),
                            Separator(
                                vertical=True,
                                style=f"background-color: {surface_variant_hex}; min-width: .1rem; min-height: 1rem; border-radius: 1rem; margin: 0.01rem 0.5rem;",
                            ),
                            Box(
                                spacing=8,
                                child=[
                                    Separator(
                                        css_classes=["exs-center-tab-metrics-line"],
                                        style=f"background-color: {on_tertiary_container_hex}; min-width: 2.5rem; min-height: .1rem; border-radius: 1rem; margin: 0.5rem 0.01rem;",
                                    ),
                                    Label(
                                        label="- Transmitted",
                                        css_classes=["exs-center-tab-metrics-label"],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        }
        self.buttons = Box(
            vertical=True,
            spacing=10,
            valign="fill",
            vexpand=True,
            child=[
                Button(
                    child=Icon(m, "l"),
                    on_click=lambda btn, m=m: self.switch(btn, m),
                    css_classes=[
                        "exs-center-tab-menu-button",
                        "exs-center-tab-metrics-button",
                        "active" if self.active == m else "",
                    ],
                    can_focus=False,
                )
                for m in self.metrics.keys()
            ],
        )
        self.active_widget = Box(child=[self.metrics[self.active]])
        super().__init__(
            spacing=10,
            child=[
                self.buttons,
                self.active_widget,
            ],
            css_classes=["exs-center-tab-metrics"],
        )
        GLib.timeout_add_seconds(1, self.update)

    def update(self):
        self.mem_graph.push(self.mem.used)
        # self.cpu_graph.push(self.cpu.percent)
        self.disk_graph.push(self.disk.used)
        self.net_graph.push([self.net.rx, self.net.tx])
        return True

    def switch(self, btn: Button, m: str):
        if self.active == m:
            return
        self.active = m
        self.active_widget.set_child([self.metrics[m]])
        for b in self.buttons.get_child():
            b.remove_css_class("active")
        btn.add_css_class("active")

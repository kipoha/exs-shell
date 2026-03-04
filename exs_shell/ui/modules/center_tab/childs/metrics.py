from gi.repository import GLib  # type: ignore

from ignis.widgets import Box, Button, Separator, Label

from exs_shell.interfaces.enums.icons import Icons
from exs_shell.ui.widgets.custom.graph import Graph, MultiGraph
from exs_shell.ui.widgets.custom.icon import Icon
from exs_shell.utils.colors import hex_to_rgb, get_hex_color
from exs_shell.utils.system import DiskMonitor, CPUMonitor, MemoryMonitor, NetMonitor


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
        h = 300
        w = 700
        self.mem_graph.set_size_request(w, h)
        self.cpu_graph.set_size_request(w, h)
        self.disk_graph.set_size_request(w, h)
        self.net_graph.set_size_request(w, h - 18)
        self.metrics: dict[str, Box] = {
            Icons.ui.CPU: Box(child=[self.cpu_graph]),
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
        self.cpu_graph.push(self.cpu.percent)
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

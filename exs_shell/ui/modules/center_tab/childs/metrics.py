from gi.repository import GLib  # type: ignore

from ignis.widgets import Box

from exs_shell.ui.widgets.custom.graph import Graph, MultiGraph
from exs_shell.utils.colors import hex_to_rgb, get_hex_color
from exs_shell.utils.system import DiskMonitor, CPUMonitor, MemoryMonitor, NetMonitor


class MonitorTab(Box):
    def __init__(self):
        self.mem = MemoryMonitor("GB")
        self.disk = DiskMonitor("GB")
        self.net = NetMonitor("MB")
        self.cpu = CPUMonitor()
        colors = get_hex_color()
        primary = hex_to_rgb(colors["primary"])
        on_primary = hex_to_rgb(colors["on_primary"])
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
            line_colors=[primary, on_primary],
            text_color=primary,
            autoscale=True,
            unit="MB",
        )
        h = 100
        w = 300
        self.mem_graph.set_size_request(w, h)
        self.cpu_graph.set_size_request(w, h)
        self.disk_graph.set_size_request(w, h)
        self.net_graph.set_size_request(w, h)
        super().__init__(
            spacing=50,
            vertical=True,
            child=[
                Box(
                    child=[
                        self.mem_graph,
                        self.cpu_graph,
                    ]
                ),
                Box(
                    child=[
                        self.disk_graph,
                        self.net_graph,
                    ]
                ),
            ],
            style=f"background-color: {get_hex_color()['background']};",
        )
        GLib.timeout_add_seconds(1, self.update)

    def update(self):
        self.mem_graph.push(self.mem.used)
        self.cpu_graph.push(self.cpu.percent)
        self.disk_graph.push(self.disk.used)
        self.net_graph.push([self.net.rx, self.net.tx])
        return True

from gi.repository import GLib  # type: ignore
from ignis.widgets import RegularWindow, Box

from exs_shell.ui.widgets.custom.graph import Graph, MultiGraph
from exs_shell.ui.widgets.custom.mouse_trigger import MouseTrigger
from exs_shell.utils import monitor
from exs_shell.utils.colors import hex_to_rgb, get_hex_color
from exs_shell.utils.system import DiskMonitor, CPUMonitor, MemoryMonitor, NetMonitor


class MonitorTab(RegularWindow):
    def __init__(self):
        super().__init__("Center Tab")
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
        self._box = Box(
            spacing=50,
            vertical=True,
            child=[
                self.mem_graph,
                self.cpu_graph,
                self.disk_graph,
                self.net_graph,
            ],
            style=f"background-color: {get_hex_color()['background']};",
        )
        h = 200
        w = 100
        self.mem_graph.set_size_request(w, h)
        self.cpu_graph.set_size_request(w, h)
        self.disk_graph.set_size_request(w, h)
        self.net_graph.set_size_request(w, h)
        self.set_child(self._box)
        GLib.timeout_add_seconds(1, self.update)

    def update(self):
        self.mem_graph.push(self.mem.used)
        self.cpu_graph.push(self.cpu.percent)
        self.disk_graph.push(self.disk.used)
        self.net_graph.push([self.net.rx, self.net.tx])
        return True


def init() -> None:
    monitor.init_windows(
        MouseTrigger,
        namespace="center_tab_trigger",
        size=(400, 1),
        on_hover=lambda: print("hovered"),
        on_hover_lost=lambda: print("hover lost"),
        anchor=["bottom"],
    )

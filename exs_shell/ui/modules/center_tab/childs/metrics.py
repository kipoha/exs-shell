import math
from typing import Any
from gi.repository import GLib, Gtk  # type: ignore

from ignis.widgets import Box, Button, Separator, Label, Entry, Scroll

from exs_shell import register
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.interfaces.types import ProcessSortBy, SystemSizeUnit
from exs_shell.ui.widgets.custom.graph import Graph, MultiGraph
from exs_shell.ui.widgets.custom.icon import Icon
from exs_shell.utils.colors import hex_to_rgb, get_hex_color
from exs_shell.utils.system import (
    DiskMonitor,
    CPUMonitor,
    MemoryMonitor,
    NetMonitor,
    ProcessMonitor,
)


H = 300
W = 700
PADDING = 6
TEMP_W = 50
MAIN_GRAPH_H = 90
STAT_H = 24


def _label(text: str, **kwargs) -> Label:
    return Label(label=str(text), **kwargs)


def _stat_row(name: str, value: str, primary_hex: str) -> Box:
    return Box(
        spacing=8,
        child=[
            _label(name, halign="start", css_classes=["exs-stat-name"]),
            Separator(
                style=f"background-color: {primary_hex}; min-height: .1rem; min-width: 1rem; margin: 0;",
            ),
            _label(value, halign="end", css_classes=["exs-stat-value"]),
        ],
    )


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

    def _build_header(self) -> Box:
        percent, temp = self.cpu.cpu
        self.total_label = _label(
            f"{percent:.0f}%  {self._fmt_temp(temp)}",
            halign="end",
            css_classes=["exs-stat-value"],
        )
        return Box(
            child=[
                _label(self.cpu.name, halign="start", css_classes=["exs-stat-name"]),
                self.total_label,
            ],
        )

    def _build_main(self) -> Box:
        self.main_graph = Graph(
            line_color=self.primary,
            text_color=self.primary,
            unit="%",
        )
        self.main_graph.set_size_request(W, MAIN_GRAPH_H)
        percent, temp = self.cpu.cpu
        self.main_graph.push(percent)
        return Box(child=[self.main_graph])

    def _build_cores(self) -> Box:
        cores = self.cpu.cores
        n = len(cores)
        cols = self._calc_cols(n)
        available_h = H - MAIN_GRAPH_H - STAT_H - PADDING * 4
        core_h = available_h // math.ceil(n / cols) - PADDING
        core_w = W // cols - PADDING

        rows: list[Box] = []
        row: list[Gtk.Widget] = []

        for i, (lbl, load, temp) in enumerate(cores):
            row.append(self._make_core_cell(lbl, load, temp, core_w, core_h))
            if len(row) == cols or i == n - 1:
                rows.append(Box(spacing=PADDING, child=list(row)))
                row.clear()

        return Box(vertical=True, spacing=PADDING, child=rows)

    def _make_core_cell(
        self, label: str, load: float, temp: float | str, cw: int, ch: int
    ) -> Box:
        graph = Graph(
            line_color=self.primary,
            text_color=self.primary,
            unit="%",
            font_size=8,
            padding=6,
        )
        graph.set_size_request(cw, ch)
        graph.push(load)
        self.core_graphs.append(graph)

        temp_lbl = _label(self._fmt_temp(temp), css_classes=["exs-core-temp"])
        self.core_temp_labels.append(temp_lbl)

        overlay = Gtk.Overlay()
        overlay.set_child(graph)
        corner = Box(
            spacing=4,
            halign="end",
            valign="start",
            css_classes=["exs-core-overlay"],
            child=[
                _label(label, css_classes=["exs-core-label"]),
                temp_lbl,
            ],
        )
        overlay.add_overlay(corner)
        return Box(child=[overlay])

    def _calc_cols(self, n: int) -> int:
        available_h = H - MAIN_GRAPH_H - STAT_H - PADDING * 4
        best = 1
        for cols in range(1, n + 1):
            rows = math.ceil(n / cols)
            if W // cols - PADDING >= 60 and available_h // rows - PADDING >= 30:
                best = cols
        return best

    def _fmt_temp(self, temp: float | str) -> str:
        return f"{temp:.0f}°" if isinstance(temp, float) else str(temp)

    def update(self) -> None:
        percent, temp = self.cpu.cpu
        self.main_graph.push(percent)
        self.total_label.set_label(f"{percent:.0f}%  {self._fmt_temp(temp)}")
        for i, (_, load, temp) in enumerate(self.cpu.cores):
            self.core_graphs[i].push(load)
            self.core_temp_labels[i].set_label(self._fmt_temp(temp))


class Memory(Box):
    def __init__(self, **kwargs: Any):
        self.mem = MemoryMonitor("GB")
        colors = get_hex_color()
        self.primary = hex_to_rgb(colors["primary"])
        self.primary_hex = colors["primary"]
        self.on_tertiary = hex_to_rgb(colors["on_tertiary_container"])
        self.on_tertiary_hex = colors["on_tertiary_container"]

        self.graph = MultiGraph(
            line_colors=[self.primary, self.on_tertiary],
            text_color=self.primary,
            unit="GB",
            max_value=self.mem.total,
        )
        self.graph.set_size_request(W, H - STAT_H * 3 - PADDING * 4)

        self._lbl_used = _label("", css_classes=["exs-stat-value"])
        self._lbl_free = _label("", css_classes=["exs-stat-value"])
        self._lbl_cached = _label("", css_classes=["exs-stat-value"])
        self._lbl_available = _label("", css_classes=["exs-stat-value"])

        self._update_stat_labels()

        super().__init__(
            vertical=True,
            spacing=PADDING,
            child=[
                self._build_legend(),
                self.graph,
                self._build_stats(),
            ],
            **kwargs,
        )

    def _build_stats(self) -> Box:
        def row(name: str, lbl: Label) -> Box:
            return Box(
                spacing=8,
                child=[
                    _label(name, css_classes=["exs-stat-name"]),
                    lbl,
                ],
            )

        return Box(
            spacing=16,
            child=[
                Box(
                    vertical=True,
                    spacing=2,
                    child=[
                        row("Used", self._lbl_used),
                        row("Free", self._lbl_free),
                    ],
                ),
                Box(
                    vertical=True,
                    spacing=2,
                    child=[
                        row("Cached", self._lbl_cached),
                        row("Available", self._lbl_available),
                    ],
                ),
            ],
        )

    def _update_stat_labels(self) -> None:
        total, used, free, cached, available = self.mem.all
        self._lbl_used.set_label(f"{used:.2f} GB")
        self._lbl_free.set_label(f"{free:.2f} GB")
        self._lbl_cached.set_label(f"{cached:.2f} GB")
        self._lbl_available.set_label(f"{available:.2f} GB")

    @register.events.poll(1000)
    def update(self) -> None:
        total, used, free, cached, available = self.mem.all
        self.graph.push([used, cached])
        self._update_stat_labels()

    def _build_legend(self) -> Box:
        def line(color: str, text: str) -> Box:
            return Box(
                spacing=6,
                child=[
                    Separator(
                        style=f"background-color: {color}; min-width: 2rem; min-height: .15rem; border-radius: 1rem; margin: 0;",
                    ),
                    _label(text, css_classes=["exs-stat-name"]),
                ],
            )

        total = self.mem.total
        return Box(
            spacing=12,
            child=[
                _label(
                    f"RAM  total: {total:.1f} GB",
                    halign="start",
                    css_classes=["exs-stat-name"],
                ),
                line(self.primary_hex, "Used"),
                line(self.on_tertiary_hex, "Cached"),
            ],
        )
    #
    # def _build_stats(self) -> Box:
    #     return Box(
    #         spacing=16,
    #         child=[
    #             Box(
    #                 vertical=True,
    #                 spacing=2,
    #                 child=[
    #                     _stat_row("Used", "", self.primary_hex),
    #                     _stat_row("Free", "", self.primary_hex),
    #                 ],
    #             ),
    #             Separator(
    #                 vertical=True,
    #                 style=f"background-color: {self.primary_hex}; min-width: .1rem; min-height: 1rem; border-radius: 1rem; margin: 0.5rem;",
    #             ),
    #             Box(
    #                 vertical=True,
    #                 spacing=2,
    #                 child=[
    #                     _stat_row("Cached", "", self.primary_hex),
    #                     _stat_row("Available", "", self.primary_hex),
    #                 ],
    #             ),
    #         ],
    #     )
    #
    # def _push_stats(self) -> None:
    #     total, used, free, cached, available = self.mem.all
    #     self.graph.push([used, cached])
    #     self._used = used
    #     self._free = free
    #     self._cached = cached
    #     self._available = available
    #
    # def update(self) -> None:
    #     _, used, free, cached, available = self.mem.all
    #     self.graph.push([used, cached])
    #     stats = self.get_last_child()
    #     if stats:
    #         rows = stats.get_first_child()
    #     self._rebuild_stats(used, free, cached, available)
    #
    # def _rebuild_stats(
    #     self, used: float, free: float, cached: float, available: float
    # ) -> None:
    #     child = self.get_first_child()
    #     last = None
    #     while child:
    #         last = child
    #         child = child.get_next_sibling()
    #     if last:
    #         self.remove(last)
    #
    #     self.append(
    #         Box(
    #             spacing=16,
    #             child=[
    #                 Box(
    #                     vertical=True,
    #                     spacing=2,
    #                     child=[
    #                         _stat_row("Used", f"{used:.2f} GB", self.primary_hex),
    #                         _stat_row("Free", f"{free:.2f} GB", self.primary_hex),
    #                     ],
    #                 ),
    #                 Separator(
    #                     vertical=True,
    #                     style=f"background-color: {self.primary_hex}; min-width: .1rem; min-height: 1rem; border-radius: 1rem; margin: 0.5rem;",
    #                 ),
    #                 Box(
    #                     vertical=True,
    #                     spacing=2,
    #                     child=[
    #                         _stat_row("Cached", f"{cached:.2f} GB", self.primary_hex),
    #                         _stat_row(
    #                             "Available", f"{available:.2f} GB", self.primary_hex
    #                         ),
    #                     ],
    #                 ),
    #             ],
    #         )
    #     )


class Disk(Box):
    def __init__(self, **kwargs: Any):
        self.disk = DiskMonitor("GB")
        colors = get_hex_color()
        self.primary = hex_to_rgb(colors["primary"])
        self.primary_hex = colors["primary"]

        self.graph = Graph(
            max_value=self.disk.total,
            line_color=self.primary,
            text_color=self.primary,
            unit="GB",
        )
        self.graph.set_size_request(W, H - STAT_H * 2 - PADDING * 4)

        super().__init__(
            vertical=True,
            spacing=PADDING,
            child=[
                self._build_header(),
                self.graph,
                self._build_stats(),
            ],
            **kwargs,
        )

    def _build_header(self) -> Box:
        total = self.disk.total
        self.header_lbl = _label(
            f"Disk  total: {total:.1f} GB",
            halign="start",
            css_classes=["exs-stat-name"],
        )
        self.percent_lbl = _label(
            f"{self.disk.percent:.1f}%",
            halign="end",
            css_classes=["exs-stat-value"],
        )
        return Box(child=[self.header_lbl, self.percent_lbl])

    def _build_stats(self) -> Box:
        used, free = self.disk.used, self.disk.free
        self._stats_box = Box(
            spacing=16,
            child=[
                _stat_row("Used", f"{used:.2f} GB", self.primary_hex),
                Separator(
                    vertical=True,
                    style=f"background-color: {self.primary_hex}; min-width: .1rem; min-height: 1rem; border-radius: 1rem; margin: 0.5rem;",
                ),
                _stat_row("Free", f"{free:.2f} GB", self.primary_hex),
            ],
        )
        return self._stats_box

    def update(self) -> None:
        self.graph.push(self.disk.used)
        self.percent_lbl.set_label(f"{self.disk.percent:.1f}%")
        # Пересобираем stats
        self.remove(self._stats_box)
        self._stats_box = Box(
            spacing=16,
            child=[
                _stat_row("Used", f"{self.disk.used:.2f} GB", self.primary_hex),
                Separator(
                    vertical=True,
                    style=f"background-color: {self.primary_hex}; min-width: .1rem; min-height: 1rem; border-radius: 1rem; margin: 0.5rem;",
                ),
                _stat_row("Free", f"{self.disk.free:.2f} GB", self.primary_hex),
            ],
        )
        self.append(self._stats_box)


class Network(Box):
    def __init__(self, **kwargs: Any):
        self.unit: SystemSizeUnit = "KB"
        self.net = NetMonitor(self.unit)
        colors = get_hex_color()
        self.primary = hex_to_rgb(colors["primary"])
        self.primary_hex = colors["primary"]
        self.on_tertiary = hex_to_rgb(colors["on_tertiary_container"])
        self.on_tertiary_hex = colors["on_tertiary_container"]

        self.graph = MultiGraph(
            line_colors=[self.primary, self.on_tertiary],
            text_color=self.primary,
            autoscale=True,
            unit=self.unit,
        )
        self.graph.set_size_request(W, H - STAT_H * 2 - PADDING * 4)

        self.rx_lbl = _label(f"↓ 0.00 {self.unit}", css_classes=["exs-stat-value"])
        self.tx_lbl = _label(f"↑ 0.00 {self.unit}", css_classes=["exs-stat-value"])
        self._prev_rx = self.net.rx
        self._prev_tx = self.net.tx

        super().__init__(
            vertical=True,
            spacing=PADDING,
            child=[
                self._build_legend(),
                self.graph,
                self._build_stats(),
            ],
            **kwargs,
        )

    def _build_legend(self) -> Box:
        def line(color: str, text: str) -> Box:
            return Box(
                spacing=6,
                child=[
                    Separator(
                        style=f"background-color: {color}; min-width: 2rem; min-height: .15rem; border-radius: 1rem; margin: 0;",
                    ),
                    _label(text, css_classes=["exs-stat-name"]),
                ],
            )

        return Box(
            spacing=12,
            child=[
                _label("Network", halign="start", css_classes=["exs-stat-name"]),
                line(self.primary_hex, "↓ Received"),
                line(self.on_tertiary_hex, "↑ Transmitted"),
            ],
        )

    def _build_stats(self) -> Box:
        return Box(
            spacing=16,
            child=[
                Box(
                    spacing=6,
                    child=[
                        Separator(
                            style=f"background-color: {self.primary_hex}; min-width: 2rem; min-height: .15rem; border-radius: 1rem; margin: 0;",
                        ),
                        self.rx_lbl,
                    ],
                ),
                Separator(
                    vertical=True,
                    style=f"background-color: {self.primary_hex}; min-width: .1rem; min-height: 1rem; border-radius: 1rem; margin: 0.5rem;",
                ),
                Box(
                    spacing=6,
                    child=[
                        Separator(
                            style=f"background-color: {self.on_tertiary_hex}; min-width: 2rem; min-height: .15rem; border-radius: 1rem; margin: 0;",
                        ),
                        self.tx_lbl,
                    ],
                ),
            ],
        )

    def update(self) -> None:
        rx, tx = self.net.rx, self.net.tx
        d_rx = max(0.0, rx - self._prev_rx)
        d_tx = max(0.0, tx - self._prev_tx)
        self._prev_rx = rx
        self._prev_tx = tx
        self.graph.push([d_rx, d_tx])
        self.rx_lbl.set_label(f"↓ {d_rx:.2f} {self.unit}/s")
        self.tx_lbl.set_label(f"↑ {d_tx:.2f} {self.unit}/s")


class Processes(Box):
    def __init__(self, **kwargs: Any):
        self.procs = ProcessMonitor("MB")
        colors = get_hex_color()
        self.primary_hex = colors["primary"]
        self.primary = hex_to_rgb(self.primary_hex)
        self._sort_by: ProcessSortBy = "cpu"
        self._filter: str = ""
        self._row_cache: list[Box] = []

        self._search = Entry(
            placeholder_text="Search...",
            css_classes=["exs-proc-search"],
            on_change=self._on_search,
        )

        self._list_box = Box(vertical=True, spacing=1, css_classes=["exs-proc-list"])

        scroll = Scroll(child=self._list_box, vexpand=True)
        scroll.set_size_request(W, H - 52)

        super().__init__(
            vertical=True,
            spacing=PADDING,
            child=[
                self._build_toolbar(),
                scroll,
            ],
            **kwargs,
        )

        self._refresh()

    def _build_toolbar(self) -> Box:
        self._sort_btns: dict[str, Button] = {}
        sort_box = Box(spacing=4)
        for lbl, key in [
            ("CPU%", "cpu"),
            ("RAM", "memory"),
            ("PID", "pid"),
            ("Name", "name"),
        ]:
            btn = Button(
                child=_label(lbl),
                css_classes=["exs-proc-sort", "active" if key == self._sort_by else ""],
                on_click=lambda _, k=key: self._set_sort(k),  # type: ignore
                can_focus=False,
            )
            self._sort_btns[key] = btn
            sort_box.append(btn)

        return Box(spacing=8, child=[self._search, sort_box])

    def _build_header(self) -> Box:
        cols = [
            ("PID", 55),
            ("Name", 200),
            ("User", 95),
            ("CPU%", 60),
            ("RAM MB", 75),
            ("Status", 75),
        ]
        return Box(
            spacing=4,
            css_classes=["exs-proc-header-row"],
            child=[
                _label(
                    t, css_classes=["exs-proc-header"], halign="start", width_request=w
                )
                for t, w in cols
            ],
        )

    def _build_row(self, proc) -> Box:
        def c(text: str, w_: int) -> Label:
            lbl = _label(str(text)[:24], halign="start", css_classes=["exs-proc-cell"])
            lbl.set_size_request(w_, -1)
            return lbl

        is_suspended = proc.status == "stopped"

        kill_btn = Button(
            child=_label("Kill"),
            css_classes=["exs-proc-action", "exs-proc-kill"],
            on_click=lambda _, p=proc.pid: self._do(self.procs.kill, p),
            can_focus=False,
            tooltip_text="SIGKILL",
        )
        term_btn = Button(
            child=_label("Term"),
            css_classes=["exs-proc-action", "exs-proc-term"],
            on_click=lambda _, p=proc.pid: self._do(self.procs.terminate, p),
            can_focus=False,
            tooltip_text="SIGTERM",
        )
        susp_btn = Button(
            child=_label("Res" if is_suspended else "Susp"),
            css_classes=["exs-proc-action"],
            on_click=lambda _, p=proc.pid, s=is_suspended: self._do(
                self.procs.resume if s else self.procs.suspend, p
            ),
            can_focus=False,
            tooltip_text="SIGCONT / SIGSTOP",
        )

        return Box(
            spacing=4,
            css_classes=["exs-proc-row"],
            child=[
                c(proc.pid, 55),
                c(proc.name, 200),
                c(proc.username or "", 95),
                c(f"{proc.cpu_percent:.1f}", 60),
                c(f"{proc.memory:.1f}", 75),
                c(proc.status, 75),
                Box(spacing=3, child=[kill_btn, term_btn, susp_btn]),
            ],
        )

    # def _refresh(self) -> None:
    #     procs = self.procs.lst(sort_by=self._sort_by, filter_name=self._filter or None)
    #     for c in list(self._list_box.get_child()):
    #         self._list_box.remove(c)
    #     self._list_box.append(self._build_header())
    #     for p in procs[:80]:
    #         self._list_box.append(self._build_row(p))
    def _refresh(self) -> None:
        procs = self.procs.lst(
            sort_by=self._sort_by,
            filter_name=self._filter or None,
        )[:80]

        for i, proc in enumerate(procs):
            if i < len(self._row_cache):
                self._update_row(self._row_cache[i], proc)
            else:
                row = self._build_row(proc)
                self._row_cache.append(row)
                self._list_box.append(row)

        for i in range(len(procs), len(self._row_cache)):
            self._row_cache[i].set_visible(False)

    def _update_row(self, row: Box, proc) -> None:
        row.set_visible(True)
        cells = list(row.get_child())
        is_suspended = proc.status == "stopped"

        values = [
            str(proc.pid),
            proc.name[:24],
            (proc.username or "")[:24],
            f"{proc.cpu_percent:.1f}",
            f"{proc.memory:.1f}",
            proc.status,
        ]
        for i, val in enumerate(values):
            cells[i].set_label(val)

        action_box = cells[6]
        btns = list(action_box.get_child())
        if len(btns) >= 3:
            btns[2].get_child().set_label("Res" if is_suspended else "Susp")

        row._proc_pid = proc.pid
        row._proc_suspended = is_suspended

    def update(self) -> None:
        self._refresh()

    def _do(self, fn, pid: int) -> None:
        fn(pid)
        self._refresh()

    def _on_search(self, _: Entry, text: str) -> None:
        self._filter = text
        self._refresh()

    def _set_sort(self, key: ProcessSortBy) -> None:
        for k, btn in self._sort_btns.items():
            if k == key:
                btn.add_css_class("active")
            else:
                btn.remove_css_class("active")
        self._sort_by = key
        self._refresh()


@register.event
class MonitorTab(Box):
    def __init__(self):
        colors = get_hex_color()
        self.primary_hex = colors["primary"]
        self.surface_variant_hex = colors["surface_variant"]

        self.metrics: dict[str, Box] = {
            Icons.ui.CPU: CPU(),
            Icons.ui.MEMORY: Memory(),
            Icons.ui.STORAGE: Disk(),
            Icons.ui.NETWORK: Network(),
            Icons.ui.PROCESSES: Processes(),
        }

        self.active = Icons.ui.CPU

        self.buttons = Box(
            vertical=True,
            spacing=8,
            valign="fill",
            vexpand=True,
            child=[
                Button(
                    child=Icon(m, "l"),
                    on_click=lambda _, m=m: self._switch(m),
                    css_classes=[
                        "exs-center-tab-menu-button",
                        "exs-center-tab-metrics-button",
                        "active" if m == self.active else "",
                    ],
                    can_focus=False,
                )
                for m in self.metrics
            ],
        )

        self.content = Box(
            child=[self.metrics[self.active]],
            css_classes=["exs-center-tab-metrics-content"],
        )

        super().__init__(
            spacing=10,
            css_classes=["exs-center-tab-metrics"],
            child=[self.buttons, self.content],
        )

    def _switch(self, m: str) -> None:
        if self.active == m:
            return
        self.active = m

        for c in list(self.content.get_child()):
            self.content.remove(c)
        self.content.append(self.metrics[m])

        for btn in self.buttons.get_child():
            btn.remove_css_class("active")
        btns = list(self.buttons.get_child())
        keys = list(self.metrics.keys())
        idx = keys.index(m)
        if 0 <= idx < len(btns):
            btns[idx].add_css_class("active")

    @register.events.poll(1500)
    def _update(self) -> None:
        for m in self.metrics.values():
            if hasattr(m, "update"):
                m.update()

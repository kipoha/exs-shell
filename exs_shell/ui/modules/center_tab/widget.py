from typing import Any

from gi.repository import GLib  # type: ignore

from ignis.services.niri import NiriService
from ignis.widgets import Button, Corner, EventBox, Box, Separator

from exs_shell import register
from exs_shell.interfaces.enums.gtk.transitions import RevealerTransition
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.state import State
from exs_shell.ui.modules.center_tab.childs.metrics import MonitorTab
from exs_shell.ui.modules.center_tab.childs.workspaces import Workspaces
from exs_shell.ui.factory import window as win_factory
from exs_shell.ui.widgets.base import MonitorRevealerBaseWidget
from exs_shell.ui.widgets.custom.icon import Icon
from exs_shell.ui.widgets.windows import Revealer


@register.event
class CenterTab(MonitorRevealerBaseWidget):
    def __init__(
        self,
        monitor_id: int,
    ) -> None:
        self.niri: NiriService = State.services.niri
        self.animating: bool = False
        win = win_factory.create(
            f"centertab{monitor_id}",
            monitor_id,
            ["top"],
            visible=False,
        )
        self.monitor = monitor_id
        self.widget_build()
        self.widget_build_metrics()
        super().__init__(
            self._box,
            win,
            [
                self._rev_inner,
                self._rev_left,
                self._rev_right,
            ],
        )
        self._main.connect("notify::visible", self.on_open_close)

    def on_open_close(self, *_: Any):
        def do():
            if self.visible:
                if self._rev_metrics.get_reveal_child():
                    self.close_metrics(100)
                else:
                    self._set_content(self.main_content(), 100)
            else:
                self.animating = False
                self._rev_metrics.set_reveal_child(False)
                self._rev_container.set_reveal_child(False)

        GLib.timeout_add(300, do)

    def widget_build(self) -> None:
        self._container = self.main_content()
        self._rev_container = Revealer(
            self._container, RevealerTransition.SLIDE_LEFT, 300
        )
        self._inner = Box(
            css_classes=["exs-center-tab-inner"],
            spacing=10,
            hexpand=True,
            valign="start",
            child=[
                self._rev_container,
            ],
        )
        self.left_corner = Corner(
            css_classes=["exs-center-tab-left-corner"],
            orientation="top-right",
            width_request=30,
            height_request=30,
            halign="end",
            valign="start",
        )
        self.right_corner = Corner(
            css_classes=["exs-center-tab-right-corner"],
            orientation="top-left",
            width_request=30,
            height_request=30,
            halign="end",
            valign="start",
        )

        self._rev_left = Revealer(self.left_corner, RevealerTransition.SLIDE_LEFT, 300)
        self._rev_right = Revealer(
            self.right_corner, RevealerTransition.SLIDE_RIGHT, 300
        )
        self._rev_inner = Revealer(self._inner, RevealerTransition.SLIDE_DOWN, 400)
        self._box = EventBox(
            child=[
                self._rev_left,
                self._rev_inner,
                self._rev_right,
                self._rev_container,
            ],
            on_hover_lost=self.on_hover_lost,
        )

    @register.events.niri("notify::overview-opened")
    def overview(self, niri: NiriService, *_):
        self.set_visible(niri.overview_opened)

    def on_hover_lost(self, *_: Any):
        if self.animating:
            return
        if not self.niri.overview_opened:
            GLib.idle_add(lambda: self.set_visible(False))

    def open_menu(self):
        self._set_content(self.menu(), 400)

    def close_menu(self):
        self._set_content(self.main_content(), 400)

    def _set_content(self, box: Box, delay_ms: int = 0):
        self.animating = True
        self._rev_container.set_reveal_child(False)

        def do():
            self._rev_container.set_child(box)
            self._rev_container.set_reveal_child(True)
            self.animating = False
            return False

        GLib.timeout_add(delay_ms, do)

    def open_metrics(self):
        self._set_content(self._rev_metrics, 400)

        def do():
            self._rev_metrics.set_reveal_child(True)
            return False

        GLib.timeout_add(400, do)

    def menu(self) -> Box:
        return Box(
            css_classes=["exs-center-tab-inner-container"],
            spacing=10,
            hexpand=True,
            child=[
                Button(
                    child=Icon(Icons.ui.MONITOR_HEART, "m"),
                    on_click=lambda _: self.open_metrics(),
                    css_classes=["exs-center-tab-menu-button"],
                    can_focus=False,
                ),
                Button(
                    child=Icon(Icons.ui.WEATHER, "m"),
                    on_click=lambda _: print("weather"),
                    css_classes=["exs-center-tab-menu-button"],
                    can_focus=False,
                ),
                Button(
                    child=Icon(Icons.ui.WORKSPACE, "m"),
                    on_click=lambda _: print("workspace"),
                    css_classes=["exs-center-tab-menu-button"],
                    can_focus=False,
                ),
                Button(
                    child=Icon(Icons.ui.TOOL, "m"),
                    on_click=lambda _: print("tool"),
                    css_classes=["exs-center-tab-menu-button"],
                    can_focus=False,
                ),
                Button(
                    child=Icon(Icons.ui.POWER, "m"),
                    on_click=lambda _: print("power"),
                    css_classes=["exs-center-tab-menu-button"],
                    can_focus=False,
                ),
                Button(
                    child=Icon(Icons.ui.WINDOW_CLOSE, "m"),
                    on_click=lambda _: self.close_menu(),
                    css_classes=["exs-center-tab-menu-button"],
                    can_focus=False,
                ),
            ],
        )

    def main_content(self) -> Box:
        return Box(
            css_classes=["exs-center-tab-inner-container"],
            spacing=10,
            hexpand=True,
            child=[
                Workspaces(self.monitor),
                Separator(vertical=True),
                Button(
                    child=Icon(Icons.ui.MENU, "m"),
                    on_click=lambda _: self.open_menu(),
                    css_classes=["exs-center-tab-menu-button"],
                    can_focus=False,
                ),
            ],
        )

    def widget_build_metrics(self):
        monitor_tab = MonitorTab()

        close_btn = Button(
            child=Icon(Icons.ui.WINDOW_CLOSE, "m"),
            on_click=lambda _: self.close_metrics(200),
            css_classes=["exs-center-tab-menu-button"],
            can_focus=False,
        )
        box = Box(
            vertical=True,
            spacing=5,
            hexpand=True,
            valign="start",
            halign="start",
            child=[close_btn, monitor_tab],
        )
        self._rev_metrics = Revealer(box, RevealerTransition.SLIDE_DOWN, 400)

    def close_metrics(self, delay_ms: int = 0):
        if not self.visible:
            self._rev_metrics.set_reveal_child(False)
            return
        self._rev_metrics.set_reveal_child(False)
        self._set_content(self.main_content(), delay_ms)

from typing import Any
from gi.repository import GLib  # type: ignore

from ignis.services.niri import NiriService
from ignis.widgets import Button, Corner, EventBox, Box, Separator

from exs_shell import register
from exs_shell.interfaces.enums.gtk.transitions import RevealerTransition
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.state import State
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
        win = win_factory.create(
            f"centertab{monitor_id}",
            monitor_id,
            ["top"],
            visible=False,
        )
        self.monitor = monitor_id
        self.widget_build()
        super().__init__(
            self._box,
            win,
            [self._rev_inner, self._rev_left, self._rev_right],
        )

    def widget_build(self) -> None:
        self._inner = Box(
            css_classes=["exs-center-tab-inner"],
            spacing=10,
            hexpand=True,
            valign="start",
            child=[
                Workspaces(self.monitor),
                Separator(vertical=True),
                Button(
                    child=Icon(Icons.ui.MENU, "m"),
                    on_click=lambda _: print("menu"),
                    css_classes=["exs-center-tab-menu-button"],
                    can_focus=False,
                ),
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
            child=[self._rev_left, self._rev_inner, self._rev_right],
            on_hover_lost=self.on_hover_lost,
        )

    @register.events.niri("notify::overview-opened")
    def overview(self, niri: NiriService, *_):
        self.set_visible(niri.overview_opened)

    def on_hover_lost(self, *_: Any):
        if not self.niri.overview_opened:
            GLib.idle_add(lambda: self.set_visible(False))

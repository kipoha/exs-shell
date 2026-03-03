from typing import Any

from ignis.services.niri import NiriService, NiriWorkspace
from ignis.widgets import Box, Button

from exs_shell import register
from exs_shell.state import State
from exs_shell.ui.widgets.custom.icon import Icon
from exs_shell.utils import monitor
from exs_shell.interfaces.enums.icons import Icons


@register.event
class Workspaces(Box):
    def __init__(self, monitor_id: int) -> None:
        self.niri: NiriService = State.services.niri
        super().__init__(child=[], spacing=3)
        workspaces: list[NiriWorkspace] = self.niri.workspaces
        self.output: str = monitor.get_monitor(monitor_id).get_connector()  # type: ignore
        self.buttons = []
        for w in workspaces:
            if w.output == self.output:
                self.buttons.append(
                    self.create_btn(w)
                )
        self.set_child(self.buttons)

    @register.events.niri("notify::workspaces")
    def on_workspaces(self, service: NiriService, *_: Any):
        self.buttons.clear()
        for c in self.get_child():
            c.unparent()
        workspaces: list[NiriWorkspace] = service.workspaces
        for w in workspaces:
            if w.output == self.output:
                self.buttons.append(
                    self.create_btn(w)
                )
        self.set_child(self.buttons)

    def create_btn(self, w: NiriWorkspace) -> Button:
        return Button(
            child=Icon(Icons.ui.DOT, "s"),
            on_click=lambda _, w_idx=w.idx: self.on_change(_, w_idx),
            css_classes=["exs-center-tab-workspace-button", "active" if w.is_focused else ""],
            can_focus=False
        )
    
    def on_change(self, _: Button, w_idx: int) -> None:
        for btn in self.buttons:
            btn.remove_css_class("active")
        self.niri.switch_to_workspace(w_idx)
        _.add_css_class("active")

from gi.repository import GLib  # type: ignore
from typing import Any
from ignis import utils, widgets
from ignis.services.niri import NiriService
from ignis.window_manager import WindowManager

from modules.bar import center, left, right

from config import config

window_manager = WindowManager.get_default()


class Bar(widgets.Window):
    def __init__(
        self,
        monitor_id: int = 0,
        **extra: Any
    ):

        self.niri = NiriService.get_default()
        self.niri.connect("notify::overview-opened", self.on_overview_changed)
        GLib.idle_add(lambda: self.set_visible(True) if self.niri.get_property("overview-opened") else self.set_visible(False))

        # monitor_name = utils.get_monitor(monitor_id).get_connector()  # type: ignore
        super().__init__(
            namespace=f"{config.NAMESPACE}_bar_{monitor_id}",
            monitor=monitor_id,
            anchor=["left", "top", "right"],
            child=widgets.CenterBox(
                css_classes=["bar"],
                start_widget=left,
                center_widget=center,
                end_widget=right,
            ),
            **extra
        )
    def on_overview_changed(self, niri: NiriService, param):
        active = niri.overview_opened
        lockscreen = window_manager.get_window(f"{config.NAMESPACE}_lockscreen")
        launcher = window_manager.get_window(f"{config.NAMESPACE}_launcher")
        if active and not lockscreen.visible and not launcher.visible and (left.child and center.child and right.child):
            GLib.idle_add(self._show_bar)
        else:
            GLib.idle_add(self._hide_bar)

    def _show_bar(self):
        self.set_visible(True)
        GLib.timeout_add(150, lambda: self.get_child().add_css_class("visible") or False)
        self.get_child().remove_css_class("hidden")
        return False

    def _hide_bar(self):
        self.get_child().remove_css_class("visible")
        self.get_child().add_css_class("hidden")
        GLib.timeout_add(300, lambda: self.set_visible(False) or False)
        return False

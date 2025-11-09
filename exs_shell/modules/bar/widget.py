from gi.repository import GLib  # type: ignore
from typing import Any
from ignis import widgets
from ignis.services.niri import NiriService
from ignis.window_manager import WindowManager

from exs_shell.modules.bar import center, left, right

from exs_shell.config import config
from exs_shell.config.user import options

window_manager = WindowManager.get_default()


class Bar(widgets.Window):
    def __init__(self, monitor_id: int = 0, **extra: Any):
        self.niri = NiriService.get_default()
        self.niri.connect("notify::overview-opened", self.on_overview_changed)
        GLib.idle_add(
            lambda: self.set_visible(True)
            if self.niri.get_property("overview-opened")
            else self.set_visible(False)
        )

        # monitor_name = utils.get_monitor(monitor_id).get_connector()  # type: ignore
        super().__init__(
            namespace=f"{config.NAMESPACE}_bar_{monitor_id}",
            monitor=monitor_id,
            anchor=["left", options.bar.position, "right"],
            child=widgets.CenterBox(
                css_classes=["bar", options.bar.position],
                start_widget=left,
                center_widget=center,
                end_widget=right,
            ),
            **extra,
        )

        self.__update_bar()
        options.bar.connect_option("position", self.__update_bar)

    def __update_bar(self, *_):
        self.child.remove_css_class("top")
        self.child.remove_css_class("bottom")
        self.child.add_css_class(options.bar.position)

        self.anchor = None  # type: ignore
        self.anchor = ["left", options.bar.position, "right"]  # type: ignore

    def on_overview_changed(self, niri: NiriService, param):
        active = niri.overview_opened
        launcher = window_manager.get_window(f"{config.NAMESPACE}_launcher")
        if (
            active
            and not launcher.visible
            and (left.child or center.child or right.child)
        ):
            GLib.idle_add(self._show_bar)
        else:
            GLib.idle_add(self._hide_bar)

    def _show_bar(self):
        self.set_visible(True)
        GLib.timeout_add(
            150, lambda: self.get_child().add_css_class("visible") or False
        )
        self.get_child().remove_css_class("hidden")
        return False

    def _hide_bar(self):
        self.get_child().remove_css_class("visible")
        self.get_child().add_css_class("hidden")
        GLib.timeout_add(300, lambda: self.set_visible(False) or False)
        return False

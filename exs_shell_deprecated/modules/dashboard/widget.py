from ignis import widgets

from exs_shell_deprecated.base.window.animated import PartiallyAnimatedWindow, AnimatedWindowPopup
from exs_shell_deprecated.base.singleton import SingletonClass

from exs_shell_deprecated.config import config
from exs_shell_deprecated.modules.dashboard.pages.pages import DashboardPages


class Dashboard(PartiallyAnimatedWindow, AnimatedWindowPopup, SingletonClass):
    DASHBOARD_HEIGHT = 350

    def __init__(self):
        self.left_corner = widgets.Corner(
            css_classes=["dashboard-left-corner"],
            orientation="top-right",
            width_request=50,
            height_request=50,
            halign="center",
            valign="start",
        )
        self.right_corner = widgets.Corner(
            css_classes=["dashboard-right-corner"],
            orientation="top-left",
            width_request=50,
            height_request=50,
            halign="center",
            valign="start",
        )

        self.pages = DashboardPages(
            halign="center",
        )

        self._box = widgets.EventBox(
            vertical=True,
            css_classes=["dashboard-window", "hidden"],
            height_request=self.DASHBOARD_HEIGHT,
            spacing=10,
            child=[self.pages],
            on_hover_lost=self._on_mouse_leave,
        )

        self._animated_parts = [self.left_corner, self.right_corner, self._box]

        super().__init__(
            namespace=f"{config.NAMESPACE}_dashboard",
            anchor=["top"],
            visible=False,
            child=widgets.Box(
                css_classes=["dashboard-main"],
                child=[self.left_corner, self._box, self.right_corner],
            ),
        )

    def _on_mouse_leave(self, *_):
        self.close()


class DashboardTrigger(PartiallyAnimatedWindow, SingletonClass):
    SENSOR_HEIGHT = 4
    SENSOR_WIDTH = 600

    def __init__(self):
        self.dashboard = Dashboard.get_default()

        trigger_box = widgets.EventBox(
            vexpand=False,
            hexpand=True,
            height_request=self.SENSOR_HEIGHT,
            width_request=self.SENSOR_WIDTH,
            on_hover=self._on_hover,
            css_classes=["dashboard-trigger"],
        )

        super().__init__(
            namespace=f"{config.NAMESPACE}_dashboard_trigger",
            anchor=["top"],
            visible=True,
            child=trigger_box,
        )

    def _on_hover(self, *_):
        self.dashboard.open()

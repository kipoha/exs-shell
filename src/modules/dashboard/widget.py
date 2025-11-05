from ignis import widgets

from base.window.animated import PartiallyAnimatedWindow, AnimatedWindowPopup
from base.singleton import SingletonClass

from config import config


class Dashboard(PartiallyAnimatedWindow, AnimatedWindowPopup, SingletonClass):
    DASHBOARD_WIDTH = 700
    DASHBOARD_HEIGHT = 300

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

        self._box = widgets.EventBox(
            vertical=False,
            halign="center",
            css_classes=["dashboard-window", "hidden"],
            width_request=self.DASHBOARD_WIDTH,
            height_request=self.DASHBOARD_HEIGHT,
            spacing=10,
            child=[widgets.Label(label="Dashboard content here")],
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

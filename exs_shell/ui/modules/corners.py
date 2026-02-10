from ignis.widgets import Box, CenterBox, Corner

from exs_shell.interfaces.enums.gtk.transitions import RevealerTransition
from exs_shell.interfaces.enums.gtk.windows import Exclusivity, Layer
from exs_shell.ui.widgets.base import MonitorRevealerBaseWidget
from exs_shell.ui.factory import window


class TopCorners(MonitorRevealerBaseWidget):
    def __init__(self, monitor_id: int) -> None:
        self.monitor = monitor_id
        win = window.create(
            f"top_corners{monitor_id}",
            anchor=["left", "top", "right"],
            dynamic_input_region=True,
            monitor=monitor_id,
        )
        self.widget_build()
        super().__init__(self._box, win, RevealerTransition.CROSSFADE, 400, False)
        self._revealer_box.set_hexpand(True)

    def widget_build(self) -> None:
        self.top_left = Corner(
            css_classes=["exs-corners"],
            orientation="top-left",
            width_request=30,
            height_request=30,
            halign="start",
            valign="start",
        )
        self.top_right = Corner(
            css_classes=["exs-corners"],
            orientation="top-right",
            width_request=30,
            height_request=30,
            halign="end",
            valign="start",
        )
        self._box = CenterBox(
            vertical=False,
            start_widget=self.top_left,
            end_widget=self.top_right,
            hexpand=True,
        )


class BottomCorners(MonitorRevealerBaseWidget):
    def __init__(self, monitor_id: int) -> None:
        self.monitor = monitor_id
        win = window.create(
            f"bottom_corners{monitor_id}",
            anchor=["left", "bottom", "right"],
            dynamic_input_region=True,
            monitor=monitor_id,
        )
        self.widget_build()
        super().__init__(self._box, win, RevealerTransition.CROSSFADE, 400, False)

    def widget_build(self) -> None:
        self.bottom_left = Corner(
            css_classes=["exs-corners"],
            orientation="bottom-left",
            width_request=30,
            height_request=30,
            halign="start",
            valign="end",
        )
        self.bottom_right = Corner(
            css_classes=["exs-corners"],
            orientation="bottom-right",
            width_request=30,
            height_request=30,
            halign="end",
            valign="end",
        )
        self._box = CenterBox(
            start_widget=self.bottom_left,
            end_widget=self.bottom_right,
        )


class Corners:
    def __init__(self, monitor_id: int) -> None:
        TopCorners(monitor_id)
        BottomCorners(monitor_id)

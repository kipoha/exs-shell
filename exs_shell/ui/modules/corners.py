from ignis.widgets import Box, CenterBox, Corner

from exs_shell.interfaces.enums.gtk.transitions import RevealerTransition
from exs_shell.ui.widgets.base import MonitorRevealerBaseWidget
from exs_shell.ui.factory import window
from exs_shell.ui.widgets.windows import Revealer


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
        super().__init__(self._box, win, [self._rev_inner])

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
        self._inner = CenterBox(
            vertical=False,
            start_widget=self.top_left,
            end_widget=self.top_right,
            hexpand=True,
        )
        self._rev_inner = Revealer(
            child=self._inner,
            transition_type=RevealerTransition.CROSSFADE,
            transition_duration=200,
            hexpand=True
        )
        self._box = Box(
            child=[self._rev_inner],
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
        super().__init__(self._box, win, [self._rev_inner])

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
        self._inner = CenterBox(
            vertical=False,
            start_widget=self.bottom_left,
            end_widget=self.bottom_right,
            hexpand=True,
        )
        self._rev_inner = Revealer(
            child=self._inner,
            transition_type=RevealerTransition.CROSSFADE,
            transition_duration=200,
            hexpand=True
        )
        self._box = Box(
            child=[self._rev_inner],
            hexpand=True,
        )


class Corners:
    def __init__(self, monitor_id: int) -> None:
        TopCorners(monitor_id)
        BottomCorners(monitor_id)

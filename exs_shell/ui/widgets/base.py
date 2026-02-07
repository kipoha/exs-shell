from ignis.widgets import CenterBox, Box

from exs_shell.interfaces.enums.gtk.transitions import RevealerTransition
from exs_shell.interfaces.schemas.widget.base import WindowEntity
from exs_shell.ui.widgets.windows import RevealerWindow, Revealer, Window
from exs_shell.utils.monitor import get_active_monitor, get_monitor_scale


class BaseWidget:
    def __init__(
        self,
        child: Box | CenterBox,
        window_param: WindowEntity,
    ) -> None:
        self._box = child
        win_dict = window_param.asdict()
        if "child" not in win_dict:
            win_dict["child"] = self._box
        self._main = Window(**win_dict)

    def set_visible(self, value: bool):
        self._main.set_visible(value)

    def set_child(self, value: Box | CenterBox) -> None:
        self._box = value
        self._main.set_child(value)

    @property
    def window(self) -> Window:
        return self._main

    @property
    def visible(self) -> bool:
        return self._main.visible

    @visible.setter
    def visible(self, value: bool) -> None:
        self._main.set_visible(value)


class RevealerBaseWidget(BaseWidget):
    def __init__(
        self,
        child: Box | CenterBox,
        window_param: WindowEntity,
        transition_type: RevealerTransition = RevealerTransition.SLIDE_DOWN,
        transition_duration: int = 500,
        reveal_child: bool = False,
    ) -> None:
        self._box = child
        self._revealer = Revealer(
            child=child,
            transition_type=transition_type,
            transition_duration=transition_duration,
            reveal_child=reveal_child,
        )
        self._revealer_box = Box(child=[self._revealer])
        self._main = RevealerWindow(
            revealer=self._revealer, child=self._revealer_box, **window_param.asdict()
        )

    def set_child(self, value: Box | CenterBox) -> None:
        self._box = value
        return self._revealer_box.set_child(value)

    @property
    def window(self) -> RevealerWindow:
        return self._main

    @property
    def revealer(self) -> Revealer:
        return self._revealer

    @revealer.setter
    def revealer(self, value: Revealer) -> None:
        self._revealer = value


class MonitorWidget:
    def __init__(self) -> None:
        self.monitor: int = get_active_monitor()
        self.scale: float = get_monitor_scale(self.monitor)

    def rebuild(self) -> None:
        self.monitor = get_active_monitor()
        self.scale = get_monitor_scale(self.monitor)
        self._main.monitor = self.monitor  # type: ignore

    def widget_build(self) -> None:
        pass

    def set_visible(self, value: bool):
        self.rebuild()
        super().set_visible(value)  # type: ignore


class MonitorBaseWidget(MonitorWidget, BaseWidget):
    def __init__(self, child: Box | CenterBox, window_param: WindowEntity) -> None:
        MonitorWidget.__init__(self)
        BaseWidget.__init__(self, child=child, window_param=window_param)


class MonitorRevealerBaseWidget(MonitorWidget, RevealerBaseWidget):
    def __init__(
        self,
        child: Box | CenterBox,
        window_param: WindowEntity,
        transition_type: RevealerTransition = RevealerTransition.SLIDE_DOWN,
        transition_duration: int = 500,
        reveal_child: bool = False,
    ) -> None:
        MonitorWidget.__init__(self)
        RevealerBaseWidget.__init__(
            self,
            child=child,
            window_param=window_param,
            transition_type=transition_type,
            transition_duration=transition_duration,
            reveal_child=reveal_child,
        )

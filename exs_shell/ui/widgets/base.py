from ignis.widgets import CenterBox, Box

from exs_shell import register
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
        self._main.visible = value

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

    @property
    def width(self) -> int:
        return self._main.width


@register.event
class RevealerBaseWidget(BaseWidget):
    def __init__(
        self,
        child: Box | CenterBox,
        window_param: WindowEntity,
        revealers: list[Revealer] = [],
    ) -> None:
        self._box = child
        self._main = RevealerWindow(
            child=self._box, revealers=revealers, **window_param.asdict()
        )

    @property
    def window(self) -> RevealerWindow:
        return self._main

    @register.events.window("notify::visible")
    def _on_revealer(self, *_):
        for revealer in self._main.revealers:
            revealer.set_reveal_child(self.visible)


class MonitorWidget(BaseWidget):
    def __init__(self) -> None:
        self.monitor: int = get_active_monitor()
        self.scale: float = get_monitor_scale(self.monitor)

    def rebuild(self) -> None:
        self.monitor = get_active_monitor()
        self.scale = get_monitor_scale(self.monitor)
        self._main.set_monitor(self.monitor)

    def widget_build(self) -> None:
        pass

    def set_visible(self, value: bool):
        self.rebuild()
        super().set_visible(value)


class MonitorBaseWidget(MonitorWidget, BaseWidget):
    def __init__(self, child: Box | CenterBox, window_param: WindowEntity) -> None:
        MonitorWidget.__init__(self)
        BaseWidget.__init__(self, child=child, window_param=window_param)


class MonitorRevealerBaseWidget(MonitorWidget, RevealerBaseWidget):
    def __init__(
        self,
        child: Box | CenterBox,
        window_param: WindowEntity,
        revealers: list[Revealer] = [],
    ) -> None:
        MonitorWidget.__init__(self)
        RevealerBaseWidget.__init__(  # type: ignore
            self,
            child=child,
            window_param=window_param,
            revealers=revealers,
        )

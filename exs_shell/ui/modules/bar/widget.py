from ignis.widgets import CenterBox, Label

from ignis.utils import get_n_monitors

from loguru import logger

from exs_shell.app.register import register
from exs_shell.interfaces.enums.gtk.transitions import RevealerTransition
from exs_shell.controllers import events
from exs_shell.ui.factory import window
from exs_shell.ui.widgets.base import RevealerBaseWidget


@events.register
class BarBase(RevealerBaseWidget):
    def __init__(self, monitor_num: int):
        self.monitor_num = monitor_num
        self._box = CenterBox(
            vertical=False,
            start_widget=Label(label="start"),
            center_widget=Label(label="center"),
            end_widget=Label(label="end"),
        )
        win_param = window.create(
            namespace=f"bar{monitor_num}",
            monitor=monitor_num,
            visible=False
        )

        super().__init__(
            self._box,
            win_param,
            RevealerTransition.SWING_UP,
            transition_duration=200,
            reveal_child=False,
        )

    @events.niri("notify::overview-opened")
    def overview(self, niri, param):
        logger.info(f"changed Niri overview {niri.overview_opened=}")


def init_bars():
    for i in range(get_n_monitors()):
        class_name = f"Bar{i}"
        BarClass = type(class_name, (BarBase,), {})
        register(BarClass)
        BarClass(i)

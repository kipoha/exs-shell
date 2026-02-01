from ignis.widgets import CenterBox, Label
from ignis.utils import get_n_monitors

from exs_shell import register
from exs_shell.interfaces.enums.gtk.transitions import RevealerTransition
from exs_shell.ui.factory import window
from exs_shell.ui.widgets.base import RevealerBaseWidget
# from exs_shell.ui.widgets.custom.cava_tui import CavaLabel
# from exs_shell.ui.widgets.custom.audio_visualizer import AudioVisualizer


@register.event
class BarBase(RevealerBaseWidget):
    def __init__(self, monitor_num: int):
        self.monitor_num = monitor_num
        self._box = CenterBox(
            vertical=False,
            # start_widget=AudioVisualizer(),
            # center_widget=CavaLabel(),
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

    @register.events.niri("notify::overview-opened")
    def overview(self, niri, *_):
        pass


def init_bars():
    for i in range(get_n_monitors()):
        class_name = f"Bar{i}"
        BarClass = type(class_name, (BarBase,), {})
        register.widget(BarClass)
        BarClass(i)

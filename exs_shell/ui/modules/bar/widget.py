from ignis.widgets import CenterBox, Label
from ignis.utils import get_n_monitors

from exs_shell import register
from exs_shell.interfaces.enums.gtk.transitions import RevealerTransition
from exs_shell.ui.factory import window
from exs_shell.ui.widgets.base import RevealerBaseWidget
from exs_shell.ui.widgets.custom.audio_visualizer import AudioVisualizer, CircularAudioVisualizer
from exs_shell.ui.widgets.custom.circle import ArcMeter
from exs_shell.utils.monitor import get_monitor_size


@register.event
class BarBase(RevealerBaseWidget):
    def __init__(self, monitor_num: int):
        self.monitor_num = monitor_num
        width, height = get_monitor_size(monitor_num)
        self.arc_meter = ArcMeter(arc_ratio=0.65)
        self._box = CenterBox(
            vertical=False,
            start_widget=AudioVisualizer(),
            center_widget=CircularAudioVisualizer(),
            end_widget=self.arc_meter,
            # start_widget=Label(label=f"Monitor {monitor_num}"),
            # center_widget=Label(label="|"),
            # end_widget=Label(label="|"),
        )
        self.arc_meter.set_value(0.7)
        win_param = window.create(
            namespace=f"bar{monitor_num}",
            monitor=monitor_num,
            anchor=["top"],
            css_classes=["bar"],
            visible=False
        )

        super().__init__(
            self._box,
            win_param,
            RevealerTransition.CROSSFADE,
            transition_duration=200,
            reveal_child=True,
        )

    @register.events.niri("notify::overview-opened")
    def overview(self, niri, *_):
        self.set_visible(niri.overview_opened)


def init_bars():
    for i in range(get_n_monitors()):
        class_name = f"Bar{i}"
        BarClass = type(class_name, (BarBase,), {})
        register.widget(BarClass)
        BarClass(i)

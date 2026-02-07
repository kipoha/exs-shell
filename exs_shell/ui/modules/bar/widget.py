from ignis.widgets import Box, CenterBox
from ignis.utils import get_n_monitors

from exs_shell import register
from exs_shell.configs.user import bar
from exs_shell.interfaces.enums.gtk.transitions import RevealerTransition
from exs_shell.interfaces.types import AnyDict
from exs_shell.ui.factory import window
from exs_shell.ui.factory.bar_widgets import create_bar_widgets
from exs_shell.ui.widgets.base import RevealerBaseWidget
from exs_shell.utils.monitor import get_monitor_scale


@register.event
class Bar(RevealerBaseWidget):
    def __init__(self, monitor_num: int):
        self.monitor_num = monitor_num
        self.scale = get_monitor_scale(monitor_num)
        self._box = self._widget_factory()

        self._box.set_size_request(int(950 * self.scale), int(30 * self.scale))
        win_param = window.create(
            namespace=f"bar{monitor_num}",
            monitor=monitor_num,
            anchor=[bar.position],  # type: ignore
            visible=False,
            **self.get_option_margin(),
        )

        super().__init__(
            self._box,
            win_param,
            RevealerTransition.CROSSFADE,
            transition_duration=200,
            reveal_child=True,
        )

    def _widget_factory(self) -> CenterBox:
        return CenterBox(
            vertical=False,
            start_widget=Box(
                child=create_bar_widgets(bar.left, self.scale),
                spacing=bar.left_spacing,
                css_classes=["exs-bar-left"],
            ),
            center_widget=Box(
                child=create_bar_widgets(bar.center, self.scale),
                spacing=bar.center_spacing,
                css_classes=["exs-bar-center"],
            ),
            end_widget=Box(
                child=create_bar_widgets(bar.right, self.scale),
                spacing=bar.right_spacing,
                css_classes=["exs-bar-right"],
            ),
            css_classes=["exs-bar"],
        )

    def get_option_margin(self) -> AnyDict:
        if bar.position == "top":
            return {"margin_top": int(227 * self.scale), "margin_bottom": 0}
        else:
            return {"margin_bottom": int(227 * self.scale), "margin_top": 0}

    @register.events.niri("notify::overview-opened")
    def overview(self, niri, *_):
        self.set_visible(niri.overview_opened)

    @register.events.option(bar, "left")
    @register.events.option(bar, "left_spacing")
    @register.events.option(bar, "center")
    @register.events.option(bar, "center_spacing")
    @register.events.option(bar, "right")
    @register.events.option(bar, "right_spacing")
    def _update(self, *_):
        self._box = self._widget_factory()
        self._main.set_child(self._box)

    @register.events.option(bar, "position")
    def _update_margin(self, *_):
        margins = self.get_option_margin()
        self._main.set_margin_top(margins["margin_top"])
        self._main.set_margin_bottom(margins["margin_bottom"])
        self._main.set_anchor([bar.position])

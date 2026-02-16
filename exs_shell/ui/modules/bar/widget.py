from ignis.widgets import Box, CenterBox

from exs_shell import register
from exs_shell.configs.user import bar
from exs_shell.interfaces.enums.gtk.transitions import RevealerTransition
from exs_shell.interfaces.enums.gtk.windows import Layer
from exs_shell.interfaces.types import AnyDict
from exs_shell.ui.factory import window
from exs_shell.ui.factory.bar_widgets import create_bar_widgets
from exs_shell.ui.widgets.base import RevealerBaseWidget
from exs_shell.ui.widgets.windows import Revealer
from exs_shell.utils.monitor import get_monitor_scale


@register.event
class Bar(RevealerBaseWidget):
    def __init__(self, monitor_num: int):
        self.monitor_num = monitor_num
        self.scale = get_monitor_scale(monitor_num)
        self.widger_build()

        win_param = window.create(
            namespace=f"bar{monitor_num}",
            monitor=monitor_num,
            anchor=["left", bar.position, "right"],  # type: ignore
            visible=False,
            layer=Layer.OVERLAY,
            **self.get_option_margin(),
        )

        super().__init__(
            self._box,
            win_param,
            [self._rev_inner],
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
            hexpand=True,
        )

    def widger_build(self):
        self._inner = self._widget_factory()
        self._rev_inner = Revealer(
            self._inner,
            transition_type=RevealerTransition.SLIDE_DOWN,
            transition_duration=200,
            hexpand=True,
        )
        self._box = Box(child=[self._rev_inner], hexpand=True)

    def get_option_margin(self) -> AnyDict:
        m = 490 * self.scale
        if bar.position == "top":
            return {
                "margin_top": int(227 * self.scale),
                "margin_bottom": 0,
                "margin_left": m,
                "margin_right": m,
            }
        else:
            return {
                "margin_bottom": int(227 * self.scale),
                "margin_top": 0,
                "margin_left": m,
                "margin_right": m,
            }

    @register.events.niri("notify::overview-opened")
    def overview(self, niri, *_):
        if bar.show:
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
        # self._main.set_anchor("left", [bar.position], "right")
        self.win_dict["anchor"] = ["left", bar.position, "right"]
        self.widger_build()
        self.set_revealers([self._rev_inner])
        self.recreate_window()
        self._main.set_margin_top(margins["margin_top"])
        self._main.set_margin_bottom(margins["margin_bottom"])
        print(self._inner.start_widget.child)
        print(self._inner.center_widget.child)
        print(self._inner.end_widget.child)

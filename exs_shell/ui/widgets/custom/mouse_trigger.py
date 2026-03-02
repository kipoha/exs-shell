from typing import Any, Callable

from ignis.widgets import EventBox

from exs_shell.interfaces.enums.gtk.windows import Layer
from exs_shell.interfaces.types import Anchor
from exs_shell.ui.widgets.base import Window


class MouseTrigger(Window):
    def __init__(
        self,
        monitor: int,
        namespace: str,
        size: tuple[int, int],  #  width, height
        on_hover: Callable[[], None] = lambda: None,
        on_hover_lost: Callable[[], None] = lambda: None,
        anchor: list[Anchor] | None = None,
        layer: Layer = Layer.BOTTOM,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        **kwargs: Any,
    ):
        super().__init__(
            namespace=f"{namespace}{monitor}",
            monitor=monitor,
            anchor=anchor,
            layer=layer,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            **kwargs,
        )
        self.set_size_request(*size)
        event_box = EventBox(
            halign="fill",
            valign="fill",
            on_hover=lambda _: on_hover(),
            on_hover_lost=lambda _: on_hover_lost(),
            style="background: rgba(0,0,0,0.01);",
        )

        self.set_can_focus(False)
        self.set_dynamic_input_region(True)
        self.set_child(event_box)

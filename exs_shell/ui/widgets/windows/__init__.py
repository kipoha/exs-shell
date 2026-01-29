from typing import Any

from ignis.base_widget import BaseWidget
from ignis.widgets import (
    Window as IgnisWindow,
    Revealer as IgnisRevealer,
    RevealerWindow as IgnisRevealerWindow,
)

from exs_shell.app.vars import NAMESPACE
from exs_shell.interfaces.types import Anchor
from exs_shell.interfaces.enums.gtk.transitions import RevealerTransition
from exs_shell.interfaces.enums.gtk.windows import Layer, KeyboardMode, Exclusivity


class Window(IgnisWindow):
    def __init__(
        self,
        namespace: str,
        monitor: int | None = None,
        anchor: list[Anchor] | None = None,
        exclusivity: Exclusivity = Exclusivity.NORMAL,
        layer: Layer = Layer.TOP,
        kb_mode: KeyboardMode = KeyboardMode.NONE,
        popup: bool = False,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        dynamic_input_region: bool = False,
        **kwargs: Any,
    ):
        super().__init__(
            f"{NAMESPACE}_{namespace}",
            monitor,
            anchor,  # type: ignore
            exclusivity,
            layer,
            kb_mode,
            popup,
            margin_bottom,
            margin_left,
            margin_right,
            margin_top,
            dynamic_input_region,
            **kwargs,
        )


class Revealer(IgnisRevealer):
    def __init__(
        self,
        child: BaseWidget | None = None,
        transition_type: RevealerTransition = RevealerTransition.SLIDE_DOWN,
        transition_duration: int = 500,
        reveal_child: bool = False,
        **kwargs: Any,
    ):
        super().__init__(
            child=child,
            transition_type=transition_type,
            transition_duration=transition_duration,
            reveal_child=reveal_child,
            **kwargs,
        )


class RevealerWindow(IgnisRevealerWindow):
    def __init__(
        self,
        namespace: str,
        revealer: Revealer,
        monitor: int | None = None,
        anchor: list[Anchor] | None = None,
        exclusivity: Exclusivity = Exclusivity.NORMAL,
        layer: Layer = Layer.TOP,
        kb_mode: KeyboardMode = KeyboardMode.NONE,
        popup: bool = False,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        dynamic_input_region: bool = False,
        **kwargs: Any,
    ):
        super().__init__(
            revealer,
            namespace=f"{NAMESPACE}_{namespace}",
            monitor=monitor,
            anchor=anchor,
            exclusivity=exclusivity,
            layer=layer,
            kb_mode=kb_mode,
            popup=popup,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            margin_right=margin_right,
            margin_top=margin_top,
            dynamic_input_region=dynamic_input_region,
            **kwargs,
        )

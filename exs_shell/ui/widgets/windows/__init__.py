from typing import Any

from ignis.base_widget import BaseWidget
from ignis.gobject import IgnisProperty
from ignis.utils import Timeout
from ignis.widgets import (
    Window as IgnisWindow,
    Revealer as IgnisRevealer,
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


class BaseRevealerWindow(Window):
    transition_duration: int = 0
    _revealers: list[Revealer] = []

    def __init__(self, revealers: list[Revealer], **kwargs: Any) -> None:
        self._revealers = revealers
        self.transition_duration = max(
            (r.transition_duration for r in revealers), default=0
        )
        super().__init__(**kwargs)

    def set_property(self, prop_name: str, value: Any) -> None:
        if prop_name == "visible":
            if value:
                super().set_property(prop_name, value)
            else:
                Timeout(
                    ms=self.transition_duration,
                    target=lambda x=super(): x.set_property(prop_name, value),
                )
            for revealer in self._revealers:
                revealer.reveal_child = value
            self.notify("visible")
        else:
            super().set_property(prop_name, value)

    @IgnisProperty
    def visible(self) -> bool:
        return any(r.reveal_child for r in self._revealers)

    @visible.setter
    def visible(self, value: bool) -> None:
        super().set_visible(value)

    @IgnisProperty
    def revealers(self) -> list[Revealer]:
        """
        An instance of :class:`~ignis.widgets.Revealer`.
        """
        return self._revealers

    @revealers.setter
    def revealer(self, value: Revealer) -> None:
        self._revealer = value


class RevealerWindow(BaseRevealerWindow):
    def __init__(
        self,
        namespace: str,
        revealers: list[Revealer] = [],
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
            revealers,
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

from typing import Protocol, runtime_checkable

from exs_shell.ui.widgets.windows import Revealer, RevealerWindow, Window


@runtime_checkable
class SupportsVisibility(Protocol):
    @property
    def visible(self) -> bool: ...

    @visible.setter
    def visible(self, value: bool) -> None: ...

    def set_visible(self, value: bool) -> None: ...


class HasRevealer(Protocol):
    @property
    def revealer(self): ...
    @revealer.setter
    def revealer(self, value: Revealer): ...


class HasWindow(Protocol):
    @property
    def window(self) -> Window | RevealerWindow: ...


class IWindow(HasWindow, SupportsVisibility, Protocol): ...


class IRevealerWindow(
    SupportsVisibility,
    HasRevealer,
    HasWindow,
    Protocol,
): ...

from typing import Any

from exs_shell.state import State
from exs_shell.interfaces.types import AnyDict
from exs_shell.register.events import event
from exs_shell.register import events


def _register(cls: type, registry: AnyDict) -> type:
    original_init = cls.__init__

    def new_init(self, *args: Any, **kwargs: Any):
        key = cls.__name__.lower()
        if key in registry:
            raise ValueError(f"{key} already registered")
        original_init(self, *args, **kwargs)
        registry[key] = self

    cls.__init__ = new_init
    return cls


def widget(cls: type) -> type:
    return _register(cls, State.widgets)


def window(cls: type) -> type:
    return _register(cls, State.windows)


def service(cls: type) -> type:
    return _register(cls, State.services)


__all__ = [
    "widget",
    "service",
    "window",
    "event",
    "events",
]

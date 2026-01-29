from typing import Any

from exs_shell.state import State


def register(cls: type) -> type:
    """
    Register a class as a widget
    """
    original_init = cls.__init__

    def new_init(self, *args: Any, **kwargs: Any):
        key = cls.__name__.lower()
        if key in State.widgets:
            return
        original_init(self, *args, **kwargs)
        State.widgets[key] = self

    cls.__init__ = new_init
    return cls

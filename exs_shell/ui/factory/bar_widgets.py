from typing import Sequence

from ignis.base_widget import BaseWidget

from exs_shell.interfaces.types import AnyDict
from exs_shell.app.vars import BAR_WIDGETS
from exs_shell.state import State


def get_or_create_widget(name: str, **kwargs):
    if name in State.widgets:
        widget = State.widgets[name]

        parent = widget.get_parent()
        if parent is not None:
            parent.remove(widget)

        return widget

    cls = BAR_WIDGETS[name]
    instance = cls(**kwargs)
    State.widgets[name] = instance
    return instance


def create_bar_widgets(widgets: list[str], scale: float) -> Sequence[BaseWidget]:
    bar_widgets_args: dict[str, AnyDict] = {
        "battery": {
            "size": int(30 * scale),
            "thickness": int(4 * scale),
            "font_size": 12 * scale,
        },
        "tray": {
            "scale": scale,
        },
        "clock": {
            "css_classes": ["exs-clock"],
        },
        "kb_layout": {
            "css_classes": ["exs-kb-layout"],
        },
        "cava_tui": {
            "css_classes": ["exs-cava-tui"],
        },
    }
    return [
        get_or_create_widget(
            widget,
            **bar_widgets_args.get(widget, {})
        )
        for widget in widgets
    ]

from typing import Sequence

from ignis.base_widget import BaseWidget

from exs_shell.interfaces.types import AnyDict
from exs_shell.app.vars import BAR_WIDGETS


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
        BAR_WIDGETS[widget](**bar_widgets_args.get(widget, {})) for widget in widgets
    ]

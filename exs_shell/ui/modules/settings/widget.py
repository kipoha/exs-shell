from ignis.widgets import Label, Button, Box

from exs_shell.app.register import register
from exs_shell.interfaces.enums.gtk.transitions import RevealerTransition
from exs_shell.interfaces.schemas.widget.base import WindowParam
from exs_shell.ui.widgets.base import RevealerBase


@register
class Settings(RevealerBase):
    def __init__(self) -> None:
        self._box = Box(
            child=[
                Label(label="Settings"),
                Button(
                    child=Label(label="Close"), on_click=lambda _self: print("close")
                ),
            ],
            vertical=False,
            homogeneous=True,
            spacing=10,
        )
        win_param = WindowParam(
            visible=False,
            namespace="settings",
            default_width=800,
            default_height=800,
        )
        super().__init__(
            child=self._box,
            window_param=win_param,
            transition_type=RevealerTransition.SWING_UP,
            transition_duration=300,
            reveal_child=True,
        )

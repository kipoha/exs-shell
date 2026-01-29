from ignis.widgets import Label, Button, Box

from exs_shell.app.register import register
from exs_shell.interfaces.enums.gtk.transitions import RevealerTransition
from exs_shell.ui.widgets.windows import RevealerWindow, Revealer


@register
class Settings:
    def __init__(self):
        self.inner_box = Box(
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
        self.revealer = Revealer(
            self.inner_box,
            transition_type=RevealerTransition.SWING_UP,
            transition_duration=300,
            reveal_child=True,
        )

        self.box = Box(child=[self.revealer])

        self._main = RevealerWindow(
            visible=False,
            revealer=self.revealer,
            namespace="settings",
            default_width=800,
            default_height=800,
            child=self.box,
        )

    def set_visible(self, value: bool):
        self._main.set_visible(value)

    @property
    def visible(self):
        return self._main.visible

from ignis import widgets
from ignis.services.niri import NiriService

from exs_shell import register
from exs_shell.state import State


@register.widget
class KeyboardLayout(widgets.EventBox):
    def __init__(self, **kwargs):
        niri: NiriService = State.services.niri
        super().__init__(
            on_click=lambda _: niri.switch_kb_layout(),
            child=[widgets.Label(label=niri.keyboard_layouts.bind("current_name"))],
            **kwargs,
        )

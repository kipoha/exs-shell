from exs_shell import register
from exs_shell.ui.factory import window
from exs_shell.ui.widgets.base import MonitorRevealerBaseWidget


@register.event
class Workspaces(MonitorRevealerBaseWidget):
    def __init__(self) -> None:
        win = window.create(
            "workspaces"
        )
        super().__init__(self._box, win, [])

    def widget_build(self) -> None: ...

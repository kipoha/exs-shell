from ignis import widgets
from exs_shell_deprecated.window.settings.elements.row import SettingsRow
from typing import Callable
from ignis.gobject import Binding


class EntryRow(SettingsRow):
    def __init__(
        self,
        text: str | Binding | None = None,
        on_change: Callable | None = None,
        width: int | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._entry = widgets.Entry(
            on_accept=on_change,
            # on_change=on_change,
            text=text,
            halign="end",
            valign="center",
            width_request=width or -1,
            hexpand=True,
            css_classes=["settings-row-entry"],
        )
        self.child.append(self._entry)

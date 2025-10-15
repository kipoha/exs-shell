from ignis import widgets
from window.settings.elements.row import SettingsRow
from typing import Callable, Iterable
from ignis.gobject import Binding

class SelectRow(SettingsRow):
    def __init__(
        self,
        options: Iterable[str],
        active: str | Binding | None = None,
        on_selected: Callable[[str], None] | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self._select = widgets.DropDown(
            items=list(options),
            hexpand=True,
            halign="end",
        )

        if isinstance(active, Binding):
            active.bind("selected")
        elif active in options:  # type: ignore
            self._select.set_selected(options.index(active))  # type: ignore
        else:
            self._select.set_selected(0)

        if on_selected:
            self._select.connect("notify::selected-item", self._make_handler(on_selected))

        self.child.append(self._select)

    def _make_handler(self, callback: Callable[[str], None]):
        def handler(widget, _param):
            selected = widget.get_selected()
            if selected is not None:
                callback(str(selected))
        return handler

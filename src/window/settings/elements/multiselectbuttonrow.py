from ignis import widgets
from window.settings.elements.row import SettingsRow
from typing import Callable, Iterable


class MultiSelectButtonRow(SettingsRow):
    def __init__(
        self,
        options: Iterable[str],
        selected_items: list[str] | None = None,
        on_change: Callable[[list[str]], None] | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self._grid = widgets.Grid(
            hexpand=True,
            halign="end",
            css_classes=["settings-row-multi-select-button"],
            row_spacing=4,
            column_spacing=4,
        )
        self.child.append(self._grid)

        self._checkboxes = []
        selected_items = selected_items or []

        max_per_row = 4
        col = 0
        row = 0

        for opt in options:
            cb = widgets.CheckButton(label=opt)
            cb.set_active(opt in selected_items)
            cb.css_classes = ["settings-row-multi-select-button-checkbox"]
            if on_change:
                cb.connect("toggled", self._make_handler(on_change))

            self._checkboxes.append(cb)
            self._grid.attach(cb, col, row, 1, 1)

            col += 1
            if col >= max_per_row:
                col = 0
                row += 1

    def _make_handler(self, callback):
        def handler(_widget):
            checked = [cb.get_label() for cb in self._checkboxes if cb.get_active()]
            callback(checked)

        return handler

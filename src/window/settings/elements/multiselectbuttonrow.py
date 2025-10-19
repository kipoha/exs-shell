from ignis import widgets
from window.settings.elements.row import SettingsRow
from typing import Callable, Iterable


class MultiSelectButtonRow(SettingsRow):
    def __init__(
        self,
        options: Iterable[str],
        selected_items: list[str] | None = None,
        on_change: Callable[[list[str]], None] | None = None,
        max_per_row: int = 4,
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

        self._buttons = []
        selected_items = selected_items or []

        col = 0
        row = 0

        for opt in options:
            btn = widgets.Button(label=opt)
            btn.css_classes = ["settings-row-multi-select-button-btn"]
            if opt in selected_items:
                btn.get_style_context().add_class("active")

            if on_change:
                btn.connect("clicked", self._make_handler(on_change, btn))

            self._buttons.append(btn)
            self._grid.attach(btn, col, row, 1, 1)

            col += 1
            if col >= max_per_row:
                col = 0
                row += 1

    def _make_handler(self, callback: Callable[[list[str]], None], btn):
        def handler(_widget):
            sc = btn.get_style_context()
            if sc.has_class("active"):
                sc.remove_class("active")
            else:
                sc.add_class("active")

            checked = [b.get_label() for b in self._buttons if b.get_style_context().has_class("active")]
            callback(checked)

        return handler

from ignis import widgets
from exs_shell.window.settings.elements.row import SettingsRow
from typing import Callable, Iterable


class SelectButtonRow(SettingsRow):
    def __init__(
        self,
        options: Iterable[str],
        selected_item: str | None = None,
        on_change: Callable[[str | None], None] | None = None,
        max_per_row: int = 4,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self._grid = widgets.Grid(
            hexpand=True,
            halign="end",
            css_classes=["settings-row-select-button"],
            row_spacing=4,
            column_spacing=4,
        )
        self.child.append(self._grid)

        self._buttons = []
        self._selected_button = None
        col = 0
        row = 0

        for opt in options:
            btn = widgets.Button(label=opt)
            btn.css_classes = ["settings-row-select-button-btn"]

            if opt == selected_item:
                btn.css_classes += ["active"]
                self._selected_button = btn

            if on_change:
                btn.connect("clicked", self._make_handler(on_change, btn))

            self._buttons.append(btn)
            self._grid.attach(btn, col, row, 1, 1)

            col += 1
            if col >= max_per_row:
                col = 0
                row += 1

    def _make_handler(self, callback: Callable[[str | None], None], btn):
        def handler(_widget):
            for b in self._buttons:
                sc = b.get_style_context()
                if sc.has_class("active"):
                    sc.remove_class("active")

            btn.get_style_context().add_class("active")
            self._selected_button = btn

            callback(btn.get_label())

        return handler

    @property
    def selected(self) -> str | None:
        return self._selected_button.get_label() if self._selected_button else None

    def reset_selection(self):
        if self._selected_button:
            sc = self._selected_button.get_style_context()
            if sc.has_class("active"):
                sc.remove_class("active")
        self._selected_button = None

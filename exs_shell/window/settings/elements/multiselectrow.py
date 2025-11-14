from ignis import widgets

from typing import Callable, Iterable

from exs_shell.window.settings.elements.row import SettingsRow


class MultiSelectRow(SettingsRow):
    def __init__(
        self,
        options: Iterable[str],
        selected_items: list[str] | None = None,
        on_change: Callable[[list[str]], None] | None = None,
        max_per_row: int = 4,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.options = list(options)
        self.selected_items = selected_items or []
        self.on_change = on_change
        self.max_per_row = max_per_row

        self._added_items: list[widgets.Box] = []

        self._select = widgets.DropDown(
            items=self.options,
            hexpand=True,
            halign="end",
            css_classes=["settings-row-select"]
        )

        self._select_button_clear = widgets.Button(
            label="",
            css_classes=["settings-row-one-select-button-clear"],
            on_click=self._clear_selected,
        )

        self._select_button_add = widgets.Button(
            label="",
            css_classes=["settings-row-one-select-button-add"],
            on_click=self._make_handler,
        )

        self._grid = widgets.Grid(
            hexpand=True,
            halign="end",
            css_classes=["settings-row-multi-select"],
            row_spacing=10,
            column_spacing=10,
            visible=True if self.selected_items else False
        )

        self._select_box = widgets.Box(
            hexpand=True,
            halign="end",
            spacing=5,
            child=[self._select, self._select_button_clear, self._select_button_add],
        )

        self._box = widgets.Box(
            vertical=True,
            hexpand=True,
            halign="end",
            spacing=10,
            child=[self._select_box, self._grid],
        )
        self.child.append(self._box)

        for item in self.selected_items:
            self._add_item_to_grid(item)

    def _make_handler(self, *_):
        selected = self._select.get_selected()
        if selected is not None:
            self._on_select(selected)

    def _clear_selected(self, *_):
        for c in list(self._added_items):
            if c.get_parent() is self._grid:
                c.unparent()
        self._added_items.clear()
        self.selected_items.clear()
        self._grid.set_visible(False)
        if self.on_change:
            self.on_change(self.selected_items)

    def _on_select(self, value):
        if not value:
            return
        value = str(value)
        if value not in self.options:
            return
        self.selected_items.append(value)
        self._add_item_to_grid(value)
        self._grid.set_visible(True if self.selected_items else False)
        if self.on_change:
            self.on_change(self.selected_items)

    def _add_item_to_grid(self, value: str):
        index = len(self._added_items)
        row = index // self.max_per_row
        col = index % self.max_per_row

        label = widgets.Label(label=value)
        btn_delete = widgets.Button(
            css_classes=["settings-row-multi-select-item-del"],
            label="",
            on_click=lambda b, val=value: self._remove_item(val)
        )

        container = widgets.Box(spacing=8, css_classes=["settings-row-multi-select-item"])
        container.append(label)
        container.append(btn_delete)

        self._grid.attach(container, col, row, 1, 1)
        self._added_items.append(container)


    def _remove_item(self, value: str):
        container = next((c for c in self._added_items if c.child[0].get_label() == value), None)  # type: ignore
        if not container:
            return

        if container.get_parent() is self._grid:
            container.unparent()
        self._added_items.remove(container)
        self.selected_items.remove(value)

        for c in list(self._added_items):
            if c.get_parent() is self._grid:
                c.unparent()
        self._added_items.clear()

        for item in self.selected_items.copy():
            self._add_item_to_grid(item)

        if self.on_change:
            self.on_change(self.selected_items)

        self._grid.set_visible(True if self.selected_items else False)

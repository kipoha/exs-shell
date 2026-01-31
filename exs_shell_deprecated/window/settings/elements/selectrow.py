from ignis import widgets
from ignis.gobject import Binding

from typing import Callable, Iterable

from exs_shell_deprecated.window.settings.elements.row import SettingsRow


class SelectRow(SettingsRow):
    def __init__(
        self,
        options: Iterable[str],
        selected_item: str | Binding | None = None,
        on_selected: Callable[[str | None], None] | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self._select = widgets.DropDown(
            css_classes=["settings-row-select"],
            items=list(options),
            hexpand=True,
            halign="end",
        )
        self.method = on_selected

        self._selected_item = widgets.Label(
            label=selected_item, css_classes=["settings-row-selected-item"]
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

        self._select_box = widgets.Box(
            spacing=5,
            child=[self._select, self._select_button_clear, self._select_button_add],
        )

        self._selected_item_box = widgets.Box(
            spacing=10,
            css_classes=["settings-row-selected-item-box"],
            child=[self._selected_item],
            visible=bool(selected_item),
            hexpand=True,
            halign="end",
        )
        self._box = widgets.Box(
            vertical=True,
            hexpand=True,
            halign="end",
            spacing=10,
            child=[self._select_box, self._selected_item_box],
        )

        self.child.append(self._box)

    def _make_handler(self, *_):
        selected = self._select.get_selected()
        if selected is not None and self.method:
            self._selected_item.set_label(str(selected))
            self._selected_item_box.set_visible(True)
            self.method(selected)

    def _clear_selected(self, *_):
        self._selected_item.set_label("")
        if self.method:
            self._selected_item_box.set_visible(False)
            self.method(None)

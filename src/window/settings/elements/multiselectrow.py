from ignis import widgets
from window.settings.elements.row import SettingsRow
from typing import Callable, Iterable

class MultiSelectRow(SettingsRow):
    def __init__(
        self,
        options: Iterable[str],
        selected_items: list[str] | None = None,
        on_change: Callable[[list[str]], None] | None = None,
        max_row_width: int = 300,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._main_box = widgets.Box(orientation="vertical", spacing=6, hexpand=True)
        self._main_box.css_classes = ["multi-select-row"]

        self._checkboxes = []
        selected_items = selected_items or []

        current_row = widgets.Box(orientation="horizontal", spacing=6)
        current_width = 0

        for opt in options:
            cb = widgets.CheckButton(label=opt)
            cb.set_active(opt in selected_items)
            cb.css_classes = ["multi-checkbox"]
            if on_change:
                cb.connect("toggled", self._make_handler(on_change))

            # грубое измерение ширины кнопки
            cb_width = 8 + len(opt) * 7  # padding + примерная ширина текста
            if current_width + cb_width > max_row_width:
                self._main_box.append(current_row)
                current_row = widgets.Box(orientation="horizontal", spacing=6)
                current_width = 0

            current_row.append(cb)
            current_width += cb_width + 6  # +spacing
            self._checkboxes.append(cb)

        if len(current_row.child) > 0:
            self._main_box.append(current_row)

        self.child.append(self._main_box)

    def _make_handler(self, callback):
        def handler(_widget):
            checked = [cb.get_label() for cb in self._checkboxes if cb.get_active()]
            callback(checked)
        return handler

# from ignis import widgets
# from window.settings.elements.row import SettingsRow
# from typing import Callable, Iterable
#
#
# class MultiSelectRow(SettingsRow):
#     def __init__(
#         self,
#         options: Iterable[str],
#         selected_items: list[str] | None = None,
#         on_change: Callable[[list[str]], None] | None = None,
#         **kwargs,
#     ):
#         super().__init__(**kwargs)
#
#         self._flow_box = widgets.Box(
#             css_classes=["multi-select-row"],
#             spacing=6,
#             hexpand=False,
#             halign="end",
#             width_request=300,
#         )
#
#         self._checkboxes = []
#         selected_items = selected_items or []
#
#         for opt in options:
#             cb = widgets.CheckButton(label=opt)
#             cb.set_active(opt in selected_items)
#             cb.css_classes = ["multi-checkbox"]
#             if on_change:
#                 cb.connect("toggled", self._make_handler(on_change))
#             self._checkboxes.append(cb)
#             self._flow_box.append(cb)
#
#         self.child.append(self._flow_box)
#
#     def _make_handler(self, callback):
#         def handler(_widget):
#             checked = [cb.get_label() for cb in self._checkboxes if cb.get_active()]
#             callback(checked)
#
#         return handler

from uuid import uuid4

from typing import Any, Callable, Protocol, Sequence

from gi.repository import Gtk, Gdk  # type: ignore

from ignis.base_widget import BaseWidget
from ignis.gobject import Binding
from ignis.widgets import (
    Box,
    FileChooserButton,
    FileDialog,
    FileFilter,
    Grid,
    Label,
    Button,
    Switch,
    Entry,
    RegularWindow,
    SpinButton,
)

from exs_shell.app.vars import NAMESPACE
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.ui.widgets.custom.icon import Icon


class CategoryLabel(Box):
    def __init__(self, title: str, icon: str | None = None):
        child = []
        if icon:
            child.append(
                Icon(
                    label=icon,
                    size="m",
                    halign="start",
                    justify="left",
                ),
            )
        child.append(
            Label(
                label=title,
                css_classes=["settings-category-title"],
                halign="start",
                justify="left",
            )
        )
        super().__init__(
            css_classes=["settings-category-label"],
            spacing=10,
            child=child,
        )


class SettingsRow(Box):
    def __init__(
        self,
        icon: str | None = None,
        title: str | None = None,
        description: str | None = None,
        child: list[BaseWidget] | None = None,
        vertical: bool = False,
        css_classes: list = [],
        **kwargs,
    ):
        header = []
        title_header = []
        if icon:
            title_header.append(Icon(label=icon, size="s", halign="start"))
        if title:
            title_header.append(
                Label(label=title, css_classes=["settings-row-title"], halign="start")
            )

        if title_header:
            header.append(
                Box(
                    css_classes=["settings-row-title-header"],
                    halign="start",
                    hexpand=True,
                    child=title_header,
                    spacing=10,
                )
            )
        if description:
            header.append(
                Label(
                    label=description,
                    css_classes=["settings-row-description"],
                    halign="start",
                )
            )

        children = child or []

        classes = ["settings-row"]
        classes.extend(css_classes)

        super().__init__(
            css_classes=classes,
            vertical=vertical,
            hexpand=True,
            halign="fill",
            spacing=5,
            child=[
                Box(
                    vertical=True,
                    css_classes=["settings-row-header"],
                    valign="center",
                    halign="fill",
                    hexpand=True,
                    child=header,
                ),
                *children,
            ],
            **kwargs,
        )


def SelectRow(
    selects: Sequence[
        #     icon value
        tuple[str, str]
    ],
    on_change: Callable[[str], None],
    on_validate: Callable[[Button, str], bool] | None = None,
    active: str | None = None,
    vertical: bool = False,
    **kwargs: Any,
) -> Box:
    kwargs["css_classes"] = ["settings-row-select-choice"] + (
        kwargs.get("css_classes") or []
    )
    buttons: list[Button] = []

    def on_click(_, value: str) -> None:
        on_change(value)
        for button in buttons:
            button.remove_css_class("active")
        _.add_css_class("active")

    for icon, value in selects:
        button = Button(
            child=Icon(label=icon, size="s", halign="center"),
            on_click=lambda _, v=value: on_click(_, v),
            **kwargs,
        )
        if on_validate and not on_validate(button, value):
            continue
        if value == active:
            button.add_css_class("active")
        buttons.append(button)

    return Box(
        vertical=vertical,
        hexpand=True,
        halign="end",
        spacing=3,
        child=buttons,
        css_classes=["settings-row-select"],
    )


def DialogRow[_T](
    button_name: str = "Change",
    title: str | None = None,
    description: str | None = None,
    child: list[BaseWidget] | None = None,
    value_getter: Callable[[], _T] = lambda: None,
    on_change: Callable[[_T], None] = lambda _: None,
    clear_on_cancel: Callable[[], None] = lambda: None,
    **kwargs: Any,
) -> Button:
    kwargs["css_classes"] = ["settings-row-dialog-button"] + (
        kwargs.get("css_classes") or []
    )
    child = child or []

    for c in child:
        if isinstance(c, Entry):
            c.set_on_accept(lambda _: on_accept_in())

    dialog_window = RegularWindow(
        f"{NAMESPACE}_dialog_window_{uuid4()}",
        css_classes=["settings-dialog-window"],
        visible=False,
        default_height=200,
        default_width=300,
        hide_on_close=True,
    )

    content = Box(
        vertical=True,
        hexpand=True,
        halign="fill",
        css_classes=["settings-row-dialog-content"],
        child=[
            Label(
                label=title,
                css_classes=["settings-row-dialog-title"],
                halign="start",
            ),
            Label(
                label=description,
                css_classes=["settings-row-dialog-description"],
                halign="start",
            ),
            *child,
        ],
    )

    def on_accept_in() -> None:
        on_change(value_getter())
        dialog_window.set_visible(False)

    def on_cancel_in() -> None:
        dialog_window.set_visible(False)

    apply = Button(
        label="Apply",
        on_click=lambda _: on_accept_in(),
        css_classes=["settings-row-dialog-button-enter"],
    )
    cancel = Button(
        label="Cancel",
        on_click=lambda _: on_cancel_in(),
        css_classes=["settings-row-dialog-button-cancel"],
    )

    actions = Box(
        hexpand=True,
        halign="end",
        valign="end",
        spacing=5,
        child=[cancel, apply],
        css_classes=["settings-row-dialog-actions"],
    )

    def destroy(*_: Any):
        if not dialog_window.visible:
            dialog_window.destroy()
        clear_on_cancel()

    dialog_window.connect("notify::visible", destroy)

    dialog_window.child = Box(
        vertical=True,
        hexpand=True,
        halign="fill",
        valign="fill",
        child=[content, Box(vexpand=True, hexpand=True), actions],
        css_classes=["settings-row-dialog"],
    )

    def on_click(_):
        root = _.get_root()
        if root:
            dialog_window.set_modal(True)
            dialog_window.set_transient_for(root)
        dialog_window.set_visible(True)

    return Button(
        child=Label(label=button_name),
        on_click=on_click,
        **kwargs,
    )


class FileGTKObjProtocol(Protocol):
    def get_path(self) -> str: ...


def FileDialogRow(
    on_change: Callable[[FileDialog, FileGTKObjProtocol], None],
    button_name: str = "Change",
    initial_path: str | None | Binding = None,
    filters: Sequence[FileFilter] | None = None,
    select_folder: bool = False,
    **kwargs: Any,
) -> FileChooserButton:
    filters = filters or []
    file_dialog = FileDialog(
        select_folder=select_folder,
        filters=filters,
        initial_path=initial_path,
        on_file_set=on_change,
    )

    kwargs["css_classes"] = ["settings-row-dialog-button"] + (
        kwargs.get("css_classes") or []
    )

    return FileChooserButton(
        dialog=file_dialog,
        label=Label(label=button_name),
        **kwargs,
    )


def SwitchRow(
    active: bool | Binding = False,
    on_change: Callable[[bool], None] = lambda _: None,
    **kwargs: Any,
) -> Switch:
    kwargs["css_classes"] = ["settings-row-switch"] + (kwargs.get("css_classes") or [])
    return Switch(
        active=active, on_change=lambda _, active: on_change(active), **kwargs
    )


def SpinRow(
    on_change: Callable[[int], None] = lambda _: None,
    min: int = 1,
    max: int = 100,
    step: int = 1,
    value: int | Binding = 0,
    **kwargs: Any,
) -> SpinButton:
    kwargs["css_classes"] = ["settings-row-spin"] + (kwargs.get("css_classes") or [])
    return SpinButton(
        min=min,
        max=max,
        step=step,
        value=value,
        on_change=lambda _, value: on_change(value),
        **kwargs,
    )


class DnDBox(Box):
    def __init__(
        self,
        title: str,
        items: list[str],
        max_columns: int = 4,
        **kwargs: Any,
    ):
        self.max_columns = max_columns
        self.items_widgets: list[Label] = []

        self.title = Label(
            label=title, css_classes=["settings-row-drag-title"], halign="start"
        )

        self.items_grid = Grid(
            hexpand=True,
            halign="fill",
            row_spacing=5,
            column_spacing=10,
            css_classes=["settings-row-drag-grid"],
        )

        for item in items:
            self._add_item(item)

        super().__init__(vertical=True, child=[self.title, self.items_grid], **kwargs)

        drop_target = Gtk.DropTarget.new(Label, Gdk.DragAction.MOVE)
        drop_target.connect("drop", self._on_drop)
        self.items_grid.add_controller(drop_target)

    def _add_item(self, item_str: str):
        label = Label(label=item_str, css_classes=["settings-row-drag-item"])
        make_draggable(label)
        self.items_widgets.append(label)
        self._add_label_to_grid(label)

    def _add_label_to_grid(self, label: Label):
        index = len(self.items_widgets) - 1
        row = index // self.max_columns
        column = index % self.max_columns
        self.items_grid.attach(label, column, row, 1, 1)

    def _reorder_grid(self):
        child = self.items_grid.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.items_grid.remove(child)
            child = next_child

        for i, label in enumerate(self.items_widgets):
            row = i // self.max_columns
            column = i % self.max_columns
            self.items_grid.attach(label, column, row, 1, 1)

        self.items_grid.queue_allocate()
        self.items_grid.queue_draw()

    def _on_drop(self, _, widget: Label, x: int, y: int):
        old_parent = widget.get_parent()

        if old_parent is self.items_grid:
            self._reorder_inside(widget, x, y)
            return True

        if old_parent:
            old_box = old_parent.get_parent()
            if isinstance(old_box, DnDBox):
                if widget in old_box.items_widgets:
                    old_box.items_widgets.remove(widget)
                    old_box._reorder_grid()

            widget.unparent()

        self.items_widgets.append(widget)
        self._reorder_grid()

        return True

    def get_items(self) -> list[str]:
        return [w.get_text() for w in self.items_widgets]

    def clear_items(self, items: list[str] | None = None):
        if items is None:
            for w in self.items_widgets:
                w.unparent()
            self.items_widgets.clear()
            return

        for w in self.items_widgets:
            w.unparent()
        self.items_widgets.clear()

        for item in items:
            label = Label(label=item, css_classes=["settings-row-drag-item"])
            make_draggable(label)
            self.items_widgets.append(label)

        self._reorder_grid()

    def _reorder_inside(self, widget: Label, x: int, y: int):
        width = self.items_grid.get_allocated_width()
        column_width = width / self.max_columns

        target_column = int(x // column_width)
        target_row = int(y // 30)

        new_index = target_row * self.max_columns + target_column
        new_index = max(0, min(new_index, len(self.items_widgets) - 1))

        old_index = self.items_widgets.index(widget)

        if old_index == new_index:
            return

        self.items_widgets.pop(old_index)
        self.items_widgets.insert(new_index, widget)

        self._reorder_grid()


def make_draggable(widget: Label):
    drag_source = Gtk.DragSource()
    drag_source.set_actions(Gdk.DragAction.MOVE)

    def on_prepare(source, x, y):
        return Gdk.ContentProvider.new_for_value(widget)

    def on_drag_begin(source, drag):
        widget.set_opacity(0.3)

    def on_drag_end(source, drag, delete_data):
        widget.set_opacity(1.0)

    drag_source.connect("prepare", on_prepare)
    drag_source.connect("drag-begin", on_drag_begin)
    drag_source.connect("drag-end", on_drag_end)

    widget.add_controller(drag_source)


class DynamicTable[_T](Box):
    def __init__(
        self,
        column_names: list[str],
        column_types: list[type[BaseWidget]],
        row_datas: list[list[Any]] | None = None,
        data_builder: Callable[[list[list[Any]]], list[_T]] | None = None,
        entry_width: int = 250,
    ):
        super().__init__(vertical=True)
        self.column_names = column_names
        self.column_types = column_types
        self.rows: list[tuple[list[BaseWidget], Button]] = []
        self.data_builder = data_builder
        self.entry_width = entry_width
        self.row_datas = row_datas or []

        self.grid = Grid(
            column_spacing=10,
            row_spacing=5,
            hexpand=True,
            halign="fill",
            css_classes=["settings-row-list-edit"],
        )
        self.append(self.grid)

        for col, name in enumerate(self.column_names):
            lbl = Label(label=name, css_classes=["settings-row-list-header-label"])
            lbl.set_hexpand(True)
            lbl.set_halign("fill")
            self.grid.attach(lbl, col, 0, 1, 1)

        empty = Label(label="")
        self.grid.attach(empty, len(self.column_names), 0, 1, 1)

        self.btn_add = Button(
            child=Icon(label=Icons.ui.ADD, size="m"),
            on_click=lambda _: self.add_row(),
            css_classes=["settings-row-dialog-button-enter"],
        )
        self.append(self.btn_add)

        for data in self.row_datas:
            self.add_row(data)

    def add_row(self, data: list[Any] | None = None):
        data = (data or []) + [None] * len(self.column_types)
        data = data[:len(self.column_types)]

        widgets: list[BaseWidget] = []
        row_index = len(self.rows) + 1

        for col, value in enumerate(data):
            col_type = self.column_types[col]

            if col_type is Entry:
                w = Entry(
                    text=str(value) if value is not None else "",
                    css_classes=["settings-row-dialog-entry"],
                )
                w.set_hexpand(True)
                w.set_halign("fill")
                w.set_width_request(self.entry_width)
            elif col_type is SpinButton:
                w = SpinRow(max=10_000)
                if value is not None:
                    w.set_value(value)
            elif col_type is Switch:
                w = SwitchRow()
                if value is not None:
                    w.set_active(bool(value))
            else:
                raise TypeError(f"Unsupported column type: {col_type}")

            self.grid.attach(w, col, row_index, 1, 1)
            widgets.append(w)

        remove_btn = Button(
            child=Icon(label=Icons.ui.WINDOW_CLOSE, size="m"),
            on_click=lambda _, ws=widgets: self.remove_row(ws),
            css_classes=["settings-row-dialog-button"],
        )
        self.grid.attach(remove_btn, len(self.column_names), row_index, 1, 1)

        self.rows.append((widgets, remove_btn))

    def remove_row(self, widgets: list[BaseWidget]):
        for i, (ws, btn) in enumerate(self.rows):
            if ws == widgets:
                break
        else:
            return

        ws, btn = self.rows.pop(i)
        for w in ws:
            parent = w.get_parent()
            if parent:
                parent.remove(w)
        parent = btn.get_parent()
        if parent:
            parent.remove(btn)

        self._rebuild_rows()

    def _rebuild_rows(self):
        for child in list(self.grid.get_child()):
            _, y, _, _ = self.grid.query_child(child)
            if y > 0:
                self.grid.remove(child)

        for row_i, (widgets, remove_btn) in enumerate(self.rows, start=1):
            for col, w in enumerate(widgets):
                parent = w.get_parent()
                if parent:
                    parent.remove(w)
                self.grid.attach(w, col, row_i, 1, 1)

            parent = remove_btn.get_parent()
            if parent:
                parent.remove(remove_btn)
            self.grid.attach(remove_btn, len(self.column_names), row_i, 1, 1)

    def raw_data(self) -> list[list[Any]]:
        result: list[list[Any]] = []
        for widgets, _ in self.rows:
            row_data: list[Any] = []
            for w in widgets:
                if isinstance(w, Entry):
                    row_data.append(w.get_text())
                elif isinstance(w, SpinButton):
                    row_data.append(w.get_value())
                elif isinstance(w, Switch):
                    row_data.append(w.get_active())
            result.append(row_data)
        self.row_datas = result
        return result

    def get_data(self) -> list[Any]:
        result = self.raw_data()
        if self.data_builder:
            result = self.data_builder(result)
        return result

    def clear(self):
        for widgets, btn in self.rows:
            for w in widgets:
                parent = w.get_parent()
                if parent:
                    parent.remove(w)
            parent = btn.get_parent()
            if parent:
                parent.remove(btn)

        self.rows.clear()

        for data in self.row_datas:
            self.add_row(data)

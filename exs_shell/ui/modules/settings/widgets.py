from uuid import uuid4

from typing import Any, Callable, Protocol, Sequence

from ignis.base_widget import BaseWidget
from ignis.gobject import Binding
from ignis.widgets import (
    Box,
    FileChooserButton,
    FileDialog,
    FileFilter,
    Label,
    Button,
    Switch,
    Entry,
    RegularWindow,
    SpinButton,
)

from exs_shell.app.vars import NAMESPACE


class CategoryLabel(Box):
    def __init__(self, title: str, icon: str | None = None):
        child = []
        if icon:
            child.append(
                Label(
                    label=icon,
                    css_classes=["settings-category-icon"],
                    halign="start",
                    justify="left",
                )
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
            title_header.append(
                Label(label=icon, css_classes=["settings-row-icon"], halign="start")
            )
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
            child=Label(
                label=icon, halign="center", css_classes=["settings-row-select-icon"]
            ),
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


def DialogRow(
    on_change: Callable[[str], None],
    title: str,
    description: str,
    button_name: str = "Change",
    placeholder: str | None = None,
    value: str | Binding| None = None,
    **kwargs: Any,
) -> Button:
    kwargs["css_classes"] = ["settings-row-dialog-button"] + (
        kwargs.get("css_classes") or []
    )

    dialog_window = RegularWindow(
        f"{NAMESPACE}_dialog_window_{uuid4()}",
        css_classes=["settings-dialog-window"],
        visible=False,
        default_height=200,
        default_width=300,
        resizable=False,
        hide_on_close=True,
    )

    def on_accept(text: str) -> None:
        dialog_window.set_visible(False)
        on_change(text)

    entry = Entry(
        hexpand=True,
        halign="fill",
        placeholder_text=placeholder,
        text=value,
        on_accept=lambda _: on_accept(_.text),
        css_classes=["settings-row-dialog-entry"],
    )

    def on_cancel() -> None:
        dialog_window.set_visible(False)
        entry.text = value
        # dialog_window.destroy()

    content = Box(
        vertical=True,
        hexpand=True,
        halign="fill",
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
            entry,
        ],
    )

    apply = Button(
        label="Apply",
        on_click=lambda _: on_accept(entry.text),
        css_classes=["settings-row-dialog-button-enter"],
    )
    cancel = Button(
        label="Cancel",
        on_click=lambda _: on_cancel(),
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
        if dialog_window.visible:
            dialog_window.destroy()

    dialog_window.connect("notify::visible", destroy)

    dialog_window.child = Box(
        vertical=True,
        hexpand=True,
        halign="fill",
        valign="fill",
        child=[content, Box(vexpand=True, hexpand=True), actions],
        css_classes=["settings-row-dialog"],
    )

    return Button(
        child=Label(label=button_name),
        on_click=lambda _: dialog_window.set_visible(True),
        **kwargs,
    )


class FileGTKObjProtocol(Protocol):
    def get_path(self) -> str: ...


def FileDialogRow(
    on_change: Callable[[FileDialog, FileGTKObjProtocol], None],
    button_name: str = "Change",
    initial_path: str | None = None,
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
    active: bool | Binding,
    on_change: Callable[[bool], None],
    **kwargs: Any,
) -> Switch:
    kwargs["css_classes"] = ["settings-row-switch"] + (kwargs.get("css_classes") or [])
    return Switch(
        active=active, on_change=lambda _, active: on_change(active), **kwargs
    )


def SpinRow(
    on_change: Callable[[int], None],
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

from uuid import uuid4

from typing import Any, Callable, Sequence

# from gi.repository import Gtk  # type: ignore

from ignis.base_widget import BaseWidget
from ignis.widgets import Box, Label, Button, Switch, Entry, RegularWindow

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
    kwargs["css_classes"] = ["settings-row-select-choice"] + (kwargs.get("css_classes") or [])
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
    value: str | None = None,
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

    # def on_key_pressed(__, keyval, *_):
    #     match keyval:
    #         case 65307:  # 65307 = ESC
    #             dialog_window.set_visible(False)
    #     return True

    dialog_window.child = Box(
        vertical=True,
        hexpand=True,
        halign="fill",
        valign="fill",
        child=[content, Box(vexpand=True, hexpand=True), actions],
        css_classes=["settings-row-dialog"],
    )
    # key_controller = Gtk.EventControllerKey()
    # dialog_window.add_controller(key_controller)
    # dialog_window.connect("key-pressed", on_key_pressed)

    return Button(
        child=Label(label=button_name),
        on_click=lambda _: dialog_window.set_visible(True),
        **kwargs,
    )


def SwitchRow(
    active: bool,
    on_change: Callable[[bool], None],
    **kwargs: Any,
) -> Switch:
    kwargs["css_classes"] = ["settings-row-switch"] + (kwargs.get("css_classes") or [])
    return Switch(
        active=active, on_change=lambda _, active: on_change(active), **kwargs
    )

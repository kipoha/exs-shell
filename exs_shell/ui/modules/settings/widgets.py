from typing import Any
from ignis.base_widget import BaseWidget
from ignis.widgets import Box, Label, Button, Switch


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
            spacing=5,
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
        if icon:
            header.append(
                Label(
                    label=icon, css_classes=["settings-row-icon"], halign="start"
                )
            )
        if title:
            header.append(
                Label(
                    label=title, css_classes=["settings-row-title"], halign="start"
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


def SelectRow(**kwargs: Any): ...

def DialogRow(**kwargs: Any): ...

def MultiSelectRow(**kwargs: Any): ...

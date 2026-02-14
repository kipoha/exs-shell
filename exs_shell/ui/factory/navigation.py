from typing import Callable

from ignis.widgets import Box, Button, Label


class Navigation(Box):
    def __init__(
        self,
        tabs: dict[str, tuple[str, str]],
        on_select: Callable[[str], None],
        default: str | None = None,
        vertical: bool = True,
    ):
        super().__init__(
            css_classes=["settings-navigation"],
            vertical=vertical,
            spacing=5,
        )
        self.on_select = on_select
        self.buttons: dict[str, Button] = {}

        for key, (icon, label) in tabs.items():
            btn = Button(
                child=Box(
                    child=[
                        Label(label=icon, css_classes=["settings-navigation-button-icon"]),
                        Label(label=label, css_classes=["settings-navigation-button-label"]),
                    ],
                    vertical=vertical,
                    halign="center",
                    valign="center",
                    spacing=5,
                ),
                css_classes=["settings-navigation-button"],
                on_click=lambda *_, key=key: self.select(key),
            )
            self.buttons[key] = btn
            self.append(btn)

        if default:
            self.select(default)

    def select(self, key: str):
        for name, btn in self.buttons.items():
            if name == key:
                btn.add_css_class("active")
            else:
                btn.remove_css_class("active")
        self.on_select(key)

from typing import Any

from ignis.widgets import Box, Button, Label

from libexs import register
from libexs.enums.icons import Icons
from libexs.widgets.icon import Icon
from exs_shell.configs.user import appearance


@register.event
class DarkTheme(Box):
    def __init__(self, scale: float = 1.0, **kwargs: Any):
        self.scale = scale
        self.button = Button(
            child=Box(child=[Icon(label=Icons.ui.DARK, size="m"), Label(label="Dark Theme")], spacing=5 * self.scale, hexpand=True),
            on_click=lambda _: appearance.set_dark(not appearance.dark),
            css_classes=["control-center-quick-panel-dark-button", "active" if appearance.dark else ""],
            halign="fill",
        )
        self._box = Box(
            css_classes=["control-center-quick-panel-dark"],
            child=[self.button],
            hexpand=True,
        )
        super().__init__(child=[self._box], hexpand=True, **kwargs)

    @register.events.option(appearance, "dark")
    def __on_dark(self, *_: Any):
        if appearance.dark:
            self.button.add_css_class("active")
        else:
            self.button.remove_css_class("active")

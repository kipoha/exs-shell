from ignis.widgets import Box, Label, Picture

import exs_shell
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.ui.modules.settings.tabs.base import BaseTab, BaseCategory
from exs_shell.ui.modules.settings.widgets import (
    CategoryLabel,
)
from exs_shell.utils.path import Paths


description = f"""
Just Shell For Niri Wayland Compositor

Toolkit: GTK3 / GTK4
Framework: Ignis
Author: Kipoha
License: GNU GENERAL PUBLIC LICENSE
GitHub: https://github.com/kipoha/exs-shell
Discord: https://discord.com/invite/FbdqgpnY9P
Version: v{exs_shell.__version__}
"""


class AboutCategory(BaseCategory):
    def __init__(self):
        self.logo = Picture(
            image=str(Paths.assets / "default" / "logo.png"),
            width=100,
            height=100,
            css_classes=["settings-about-logo"],
        )
        self.title = Label(
            label="Exs Shell",
            css_classes=["settings-about-title"],
            halign="center",
        )
        self.description = Label(
            label=description,
            css_classes=["settings-about-description"],
            halign="center",
        )
        super().__init__(
            child=[
                CategoryLabel(title="About", icon=Icons.ui.INFO),
                Box(child=[self.logo], halign="center", valign="center"),
                Box(
                    child=[self.title], halign="center", valign="center", margin_top=20
                ),
                Box(child=[self.description], halign="center", valign="center"),
            ]
        )


class AboutTab(BaseTab):
    def __init__(self):
        super().__init__(
            child=[
                AboutCategory(),
            ]
        )

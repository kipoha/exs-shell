from ignis.widgets import Box, Label, Picture

import exs_shell
from exs_shell import __author__, __version__
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.ui.modules.settings.tabs.base import BaseTab, BaseCategory
from exs_shell.ui.modules.settings.widgets import (
    CategoryLabel,
)
from exs_shell.utils.path import Paths

authors = __author__.split(",")
author_text = ", ".join([f'<a href="https://github.com/{author}">{author}</a>' for author in authors])

description = f"""
Just Shell For Niri Wayland Compositor

Toolkit: <a href="https://www.gtk.org/">GTK3 / GTK4</a>
Framework: <a href="https://ignis-sh.github.io/ignis/stable/index.html">Ignis</a>
Author: {author_text}
License: GNU GENERAL PUBLIC LICENSE
GitHub: <a href="https://github.com/kipoha/exs-shell">GitHub Repository</a>
Discord: <a href="https://discord.com/invite/FbdqgpnY9P">Join Discord</a>
Version: v{__version__}
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
            use_markup=True,
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

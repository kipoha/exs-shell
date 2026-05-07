from collections.abc import Sequence
from pathlib import Path
from typing import Any
from ignis.widgets import Box, Button, Label, Separator
from libexs import State, register
from libexs.enums.icons import Icons
from libexs.settings.base import BaseCategory, BaseTab
from libexs.settings.widgets import CategoryLabel, SettingsRow, SwitchRow, DialogRow

from exs_shell.app.path import Dirs
from exs_shell.configs.user import user


class PluginManagerCategory(BaseCategory):
    def __init__(self):
        super().__init__(
            child=[
                CategoryLabel(title="Manage", icon=Icons.ui.SYSTEM),
                SettingsRow(
                    title="Plugins Toggle",
                    child=[self.create_dialog()],
                ),
            ]
        )

    def create_dialog(self) -> Button:
        plugins: Sequence[Path] = [
            plugin
            for plugin in (Dirs.PLUGINS_DIR).iterdir()
            if plugin.is_dir()
            and not plugin.name.startswith(".")
            and not plugin.name.startswith("_")
            and (plugin / "setup.py").exists()
        ]
        dialog_box = Box(
            spacing=10,
            vertical=True,
            halign="fill",
            hexpand=True,
            child=[
                Box(
                    hexpand=True,
                    child=[
                        # Label(label=plugin.name, halign="start"),
                        Box(
                            hexpand=True,
                            child=[Label(label=" " + plugin.name.capitalize(), halign="start")],
                        ),
                        SwitchRow(
                            plugin in user.plugins,
                            lambda switched, plugin=plugin: self.add_remove(
                                plugin, switched
                            ),
                            halign="end",
                        ),
                    ],
                    spacing=3,
                )
                for plugin in plugins
            ],
        )
        dialog = DialogRow(
            "Toggle Plugins",
            "Manage Plugins",
            "When enabling/disabling plugins, the shell will be restarted.",
            [dialog_box],
        )
        return dialog

    def add_remove(self, plugin: Path, switched: bool) -> None:
        if plugin in user.plugins and not switched:
            user.plugins.remove(str(plugin))
        else:
            user.plugins.append(str(plugin))


class PluginManagerTab(BaseTab):
    def __init__(self):
        plugins_category: Sequence[BaseCategory] = State.plugin_settings
        super().__init__(
            child=[
                PluginManagerCategory(),
                *plugins_category,
            ],
        )

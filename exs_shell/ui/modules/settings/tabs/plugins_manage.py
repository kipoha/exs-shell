from pathlib import Path
from typing import Any
from ignis.widgets import Separator
from libexs import register
from libexs.enums.icons import Icons
from libexs.settings.base import BaseCategory, BaseTab
from libexs.settings.widgets import CategoryLabel, SettingsRow, SwitchRow, FileDialogRow

from exs_shell.configs.user import user


class PluginManagerCategory(BaseCategory):
    def __init__(self):
        super().__init__(
            child=[
                CategoryLabel(title="Manage", icon=Icons.ui.SYSTEM),
                SettingsRow(
                    title="Plugins Directory",
                    child=[
                        FileDialogRow(
                            lambda _, path: user.set_plugins_dir(path.get_path()),
                            initial_path=user.bind("plugins_dir"),
                            select_folder=True,
                        )
                    ],
                ),
            ]
        )


@register.event
class PluginToggleCategory(BaseCategory):
    def __init__(self):
        self.plugins = [
            plugin for plugin in Path(user.plugins_dir).iterdir() if plugin.is_dir()
        ]

        self.plugin_switch_rows = [
            SettingsRow(
                title=plugin.name.capitalize(),
                child=[
                    SwitchRow(
                        plugin in user.plugins,
                        lambda x, pl=plugin: self.add_remove(x, pl.name),
                    )
                ],
            )
            for plugin in self.plugins
        ]
        super().__init__(
            child=[
                CategoryLabel(title="Plugins", icon=Icons.ui.EXTENSION),
                *self.plugin_switch_rows,
            ]
        )

    def add_remove(self, _, plugin: str) -> None:
        if plugin in user.plugins:
            user.plugins.remove(plugin)
        else:
            user.plugins.append(plugin)

    @register.events.option(user, "plugins_dir")
    def __on_plugins_dir_changed(self, *_: Any) -> None:
        user.plugins.clear()
        self.plugins = [
            plugin for plugin in Path(user.plugins_dir).iterdir() if plugin.is_dir()
        ]
        self.plugin_switch_rows = [
            SettingsRow(
                title=plugin.name.capitalize(),
                child=[
                    SwitchRow(
                        plugin in user.plugins,
                        lambda x, pl=plugin: self.add_remove(x, pl.name),
                    )
                ],
            )
            for plugin in self.plugins
        ]
        self.set_child(
            [
                CategoryLabel(title="Plugins", icon=Icons.ui.EXTENSION),
                *self.plugin_switch_rows,
            ]
        )


class PluginManagerTab(BaseTab):
    def __init__(self):
        super().__init__(
            child=[
                PluginManagerCategory(),
                PluginToggleCategory(),
            ],
        )

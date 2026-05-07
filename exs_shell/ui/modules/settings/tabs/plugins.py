from collections.abc import Sequence
from pathlib import Path
from ignis.widgets import Box, Button, Label
from libexs import State
from libexs.enums.icons import Icons
from libexs.settings.base import BaseCategory, BaseTab
from libexs.settings.widgets import CategoryLabel, SettingsRow, SwitchRow, DialogRow
from libexs.utils import plugin
from libexs.widgets.icon import Icon

from exs_shell.app.path import Dirs
from exs_shell.configs.user import user
from exs_shell.interfaces.schemas.plugin import Plugin


class PluginManagerCategory(BaseCategory):
    def __init__(self):
        super().__init__()
        self.update()

    def update(self) -> None:
        child = [
            CategoryLabel(title="Manage", icon=Icons.ui.SYSTEM),
            SettingsRow(
                title="Plugins Toggle",
                child=[
                    self.create_dialog(),
                    Button(
                        child=Icon(Icons.ui.REFRESH, "m"),
                        on_click=lambda _: self.update(),
                        css_classes=["settings-row-button"],
                    ),
                ],
            ),
        ]
        self.set_child(child)

    def create_dialog(self) -> Button:
        plugins: Sequence[Plugin] = [
            Plugin(name=p_data[1] or p_data[0].name, path=p_data[0])
            for p in Dirs.PLUGINS_DIR.iterdir()
            if (p_data := plugin.check(p))
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
                            child=[
                                Label(
                                    label=" " + plugin.name.capitalize(), halign="start"
                                )
                            ],
                        ),
                        SwitchRow(
                            plugin in user.plugins,
                            lambda switched, plugin=plugin: self.add_remove(
                                plugin.path, switched
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
        if not plugins:
            dialog.set_sensitive(False)
            dialog.set_label("No plugins found")
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

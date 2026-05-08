from collections.abc import Sequence
from pathlib import Path

from gi.repository import GLib
from ignis.app import IgnisApp
from ignis.widgets import Box, Button, Label
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
        self.plugins: Sequence[Plugin] = [
            Plugin(name=p_data[1] or p_data[0].name, path=p_data[0])
            for p in Dirs.PLUGINS_DIR.iterdir()
            if (p_data := plugin.check(p))
        ]
        self.plugins_state = self.plugin_state()
        super().__init__()
        self.update()

    def plugin_state(self) -> dict[str, tuple[Path, bool]]:
        return {
            plugin.name: (plugin.path, str(plugin.path) in user.plugins)
            for plugin in self.plugins
        }

    def update_pl(self, plugin_name: str, path: Path, switched: bool) -> None:
        self.plugins_state[plugin_name] = path, switched

    def clear_pl(self) -> None:
        self.plugins_state = self.plugin_state()

    def save_pl(self) -> None:
        plugins = [
            str(path)
            for _, (path, enabled) in self.plugins_state.items()
            if enabled
        ]
        user.plugins.clear()
        user.plugins.extend(plugins)
        GLib.timeout_add(100, lambda: IgnisApp.get_initialized().reload() or False)

    def update(self) -> None:
        child = [
            CategoryLabel(title="Manage", icon=Icons.ui.SYSTEM),
            SettingsRow(
                title="Plugins Toggle",
                description="Enable/Disable Plugins",
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
        dialog_box = Box(
            spacing=10,
            vertical=True,
            halign="fill",
            hexpand=True,
            child=[
                Box(
                    hexpand=True,
                    child=[
                        Box(
                            hexpand=True,
                            child=[
                                Label(
                                    label=" " + plugin_name.capitalize(), halign="start"
                                )
                            ],
                        ),
                        SwitchRow(
                            enabled,
                            lambda switched, name=plugin_name, path=path: (
                                self.update_pl(name, path, switched)
                            ),
                            halign="end",
                        ),
                    ],
                    spacing=3,
                )
                for plugin_name, (path, enabled) in self.plugins_state.items()
            ],
        )
        dialog = DialogRow(
            "Toggle Plugins",
            "Manage Plugins",
            "When enabling/disabling plugins, the shell will be restarted.",
            [dialog_box],
            lambda: self.plugins_state,
            lambda _: self.save_pl(),
            lambda: self.clear_pl(),
        )
        if not self.plugins:
            dialog.set_sensitive(False)
            dialog.set_label("No plugins found")
        return dialog


class PluginManagerTab(BaseTab):
    def __init__(self):
        super().__init__(
            child=[
                PluginManagerCategory(),
            ],
        )

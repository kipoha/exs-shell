from ignis.widgets import Separator
from libexs.enums.icons import Icons
from libexs.settings.base import BaseCategory, BaseTab
from libexs.settings.widgets import CategoryLabel, SettingsRow, SwitchRow, FileDialogRow

from exs_shell.configs.user import user


class PluginCategory(BaseCategory):
    def __init__(self):
        super().__init__(
            child=[
                CategoryLabel(title="Manage", icon=Icons.ui.LOCK),
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


class PluginTab(BaseTab):
    def __init__(self):
        super().__init__(child=[PluginCategory()])

from ignis.widgets import Entry, Label, Separator

from exs_shell.configs.user import user
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.ui.modules.settings.tabs.base import BaseTab, BaseCategory
from exs_shell.ui.modules.settings.widgets import (
    CategoryLabel,
    SettingsRow,
    DialogRow,
)


class LauncherCategory(BaseCategory):
    def __init__(self):
        self.entry_actions_prefix = Entry(
            hexpand=True,
            halign="fill",
            placeholder_text="Enter your actions prefix",
            text=user.bind("command_prefix"),
            css_classes=["settings-row-dialog-entry"],
        )
        super().__init__(
            child=[
                CategoryLabel(title="Launcher", icon=Icons.ui.LAUNCHER),
                SettingsRow(
                    title="Actions Command Prefix",
                    description="Set actions command prefix",
                    child=[
                        DialogRow(
                            button_name=user.bind("command_prefix"),
                            title="Actions Prefix",
                            description="Actions prefix",
                            child=[self.entry_actions_prefix],
                            value_getter=lambda: self.entry_actions_prefix.get_text(),
                            on_change=lambda x: user.set_command_prefix(x),
                            clear_on_cancel=lambda: self.entry_actions_prefix.set_text(
                                user.command_prefix
                            ),
                        ),
                    ],
                ),
            ]
        )


class LauncherTab(BaseTab):
    def __init__(self):
        super().__init__(child=[
            LauncherCategory(),
        ])

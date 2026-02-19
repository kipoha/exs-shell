from ignis.widgets import Entry, Separator

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
        self.entry_terminal_format = Entry(
            hexpand=True,
            halign="fill",
            placeholder_text="Enter your terminal format",
            text=user.bind("terminal_format"),
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
                Separator(),
                SettingsRow(
                    title="Terminal Format",
                    description="Set terminal format",
                    child=[
                        DialogRow(
                            title="Terminal Format",
                            description="Terminal format for launch commands and tui applications",
                            child=[self.entry_terminal_format],
                            value_getter=lambda: self.entry_terminal_format.get_text(),
                            on_change=lambda x: user.set_terminal_format(x),
                            clear_on_cancel=lambda: self.entry_terminal_format.set_text(
                                user.terminal_format
                            ),
                        ),
                    ],
                ),
                Separator(),
                SettingsRow(
                    title="Actions",
                    description="Set actions",
                    child=[
                        DialogRow(
                            title="Actions",
                            description="Actions commands",
                            child=[],
                            value_getter=lambda: user.actions,
                            # on_change=lambda x: user.set_command_suffix(x),
                            # clear_on_cancel=lambda: self.entry_actions_prefix.set_text(
                            #     user.command_suffix
                            # ),
                        ),
                    ],
                ),
            ]
        )


class LauncherTab(BaseTab):
    def __init__(self):
        super().__init__(
            child=[
                LauncherCategory(),
            ]
        )

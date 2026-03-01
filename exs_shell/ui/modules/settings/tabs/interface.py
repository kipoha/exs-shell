from typing import Any
from ignis.widgets import Box, Button, Entry, Separator

from exs_shell.app.vars import BAR_WIDGETS
from exs_shell.configs.user import bar, user
from exs_shell.interfaces.enums.configs.position import TopBottom
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.interfaces.types import AnyDict
from exs_shell.ui.modules.settings.tabs.base import BaseTab, BaseCategory
from exs_shell.ui.modules.settings.widgets import (
    CategoryLabel,
    DnDBox,
    DynamicTable,
    SettingsRow,
    DialogRow,
    SelectRow,
    SwitchRow,
    SpinRow,
)
from exs_shell.ui.widgets.custom.icon import Icon


class BarCategory(BaseCategory):
    def __init__(self):
        self.entry_clock_format = Entry(
            hexpand=True,
            halign="fill",
            placeholder_text="Enter your clock format",
            text=user.bind("clock_format"),
            css_classes=["settings-row-dialog-entry"],
        )

        items = []
        for i in BAR_WIDGETS.keys():
            if i not in bar.center + bar.left + bar.right:
                items.append(i)
        self.available_widgets = DnDBox("Available Widgets", items)
        self.left_widgets = DnDBox("Left Panel", bar.left)
        self.center_widgets = DnDBox("Center Panel", bar.center)
        self.right_widgets = DnDBox("Right Panel", bar.right)
        super().__init__(
            child=[
                CategoryLabel(title="Bar", icon=Icons.ui.INTERFACE),
                SettingsRow(
                    Icons.ui.SHOW,
                    title="Show",
                    description="Show bar",
                    child=[
                        SwitchRow(
                            active=bar.bind("show"),
                            on_change=lambda active: bar.set_show(active),
                        )
                    ],
                ),
                Separator(),
                SettingsRow(
                    Icons.align.TOP,
                    title="Position",
                    description="Bar position",
                    child=[
                        SelectRow(
                            TopBottom.aligns,
                            lambda x: bar.set_position(x),
                            active=bar.position,
                        )
                    ],
                ),
                Separator(),
                SettingsRow(
                    Icons.ui.WIDGET,
                    title="Widgets",
                    description="Replace widgets on bar",
                    child=[
                        DialogRow(
                            title="Bar widgets",
                            description="Widgets on bar",
                            child=[
                                self.available_widgets,
                                self.left_widgets,
                                self.center_widgets,
                                self.right_widgets,
                            ],
                            value_getter=self.get_widgets,
                            on_change=self.update_widgets,
                            clear_on_cancel=self.clear_widgets,
                        ),
                    ],
                ),
                Separator(),
                SettingsRow(
                    Icons.ui.CLOCK_ALARM,
                    title="Clock",
                    description="CLock format",
                    child=[
                        DialogRow(
                            title="Clock Format",
                            description="Clock format on bar",
                            child=[self.entry_clock_format],
                            value_getter=lambda: self.entry_clock_format.get_text(),
                            on_change=lambda x: user.set_clock_format(x),
                            clear_on_cancel=lambda: self.entry_clock_format.set_text(
                                user.clock_format
                            ),
                        ),
                    ],
                ),
            ]
        )

    def get_widgets(self) -> tuple[list[str], list[str], list[str]]:
        return (
            self.left_widgets.get_items(),
            self.center_widgets.get_items(),
            self.right_widgets.get_items(),
        )

    def update_widgets(self, widgets: tuple[list[str], list[str], list[str]]):
        left, center, right = widgets
        bar.set_center(center)
        bar.set_left(left)
        bar.set_right(right)

    def clear_widgets(self):
        items = []
        for i in BAR_WIDGETS.keys():
            if i not in bar.center + bar.left + bar.right:
                items.append(i)
        self.available_widgets.clear_items(items)
        self.left_widgets.clear_items(bar.left)
        self.center_widgets.clear_items(bar.center)
        self.right_widgets.clear_items(bar.right)


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
        row_datas = [[a.name, a.command, a.icon] for a in user.get_actions_objs()]

        def build(datas: list[list[Any]]) -> list[dict]:
            return [
                {
                    "name": data[0],
                    "command": data[1],
                    "icon": data[2],
                }
                for data in datas
            ]

        self.actions_table = DynamicTable(
            ["Name", "Command", "Icon"],
            [Entry, Entry, Entry],
            row_datas,
            build,
        )
        super().__init__(
            child=[
                CategoryLabel(title="Launcher", icon=Icons.ui.LAUNCHER),
                SettingsRow(
                    icon=Icons.ui.COMMAND,
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
                    icon=Icons.ui.TERM,
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
                    icon=Icons.ui.LAUNCHER,
                    title="Actions",
                    description="Set actions",
                    child=[
                        DialogRow(
                            title="Actions",
                            description="Actions commands\n\nCommand Names: Clipboard, Power Menu",
                            child=[self.actions_table],
                            value_getter=self.actions_table.get_data,
                            on_change=lambda x: user.set_actions(x),
                            clear_on_cancel=self.actions_table.clear,
                        ),
                    ],
                ),
            ]
        )


class PowerMenuCategory(BaseCategory):
    def __init__(self):
        # action_children = []
        # for i in user.get_powermenu_actions_objs():
        #     action_children.append(
        #         Box(
        #             child=[
        #                 Entry(
        #                     text=i.name,
        #                     css_classes=["settings-row-dialog-entry"],
        #                     width_request=150,
        #                 ),
        #                 Entry(
        #                     text=i.command,
        #                     placeholder_text="Example: {terminal_format} tmux",
        #                     css_classes=["settings-row-dialog-entry"],
        #                     width_request=250,
        #                 ),
        #                 Entry(
        #                     text=i.icon,
        #                     css_classes=["settings-row-dialog-entry"],
        #                     width_request=250,
        #                 ),
        #                 Button(
        #                     child=Icon(label=Icons.ui.WINDOW_CLOSE, size="m"),
        #                     on_click=lambda _: _.parent.unparent(),
        #                     css_classes=["settings-row-dialog-button"],
        #                 ),
        #             ],
        #             spacing=10,
        #             css_classes=["settings-row-list-obj"],
        #         )
        #     )
        # self.action_list = Box(
        #     vertical=True,
        #     css_classes=["settings-row-list-objs"],
        #     child=action_children,
        #     halign="fill",
        #     hexpand=True,
        # )
        # self.action_button_add = Button(
        #     child=Icon(label=Icons.ui.ADD, size="m"),
        #     halign="fill",
        #     css_classes=["settings-row-dialog-button-enter"],
        #     on_click=lambda _: self.action_list.append(
        #         Box(
        #             child=[
        #                 Entry(
        #                     text="",
        #                     css_classes=["settings-row-dialog-entry"],
        #                     width_request=150,
        #                 ),
        #                 Entry(
        #                     text="",
        #                     css_classes=["settings-row-dialog-entry"],
        #                     width_request=250,
        #                 ),
        #                 Entry(
        #                     text="",
        #                     css_classes=["settings-row-dialog-entry"],
        #                     width_request=250,
        #                 ),
        #                 Button(
        #                     child=Icon(label=Icons.ui.WINDOW_CLOSE, size="m"),
        #                     on_click=lambda _: _.parent.unparent(),
        #                     css_classes=["settings-row-dialog-button"],
        #                 ),
        #             ],
        #             spacing=10,
        #             css_classes=["settings-row-list-obj"],
        #         )
        #     ),
        # )
        # self.actions_box = Box(
        #     vertical=True,
        #     css_classes=["settings-row-list-edit"],
        #     child=[
        #         self.action_list,
        #         self.action_button_add,
        #     ],
        # )

        row_datas = [
            [a.name, a.command, a.icon] for a in user.get_powermenu_actions_objs()
        ]

        def build(datas: list[list[Any]]) -> list[dict]:
            return [
                {
                    "name": data[0],
                    "command": data[1],
                    "icon": data[2],
                }
                for data in datas
            ]

        self.actions_table = DynamicTable(
            ["Name", "Command", "Icon"],
            [Entry, Entry, Entry],
            row_datas,
            build,
        )

        super().__init__(
            child=[
                CategoryLabel(title="Power Menu", icon=Icons.ui.POWER),
                SettingsRow(
                    icon=Icons.ui.POWER,
                    title="Actions",
                    description="Set actions",
                    child=[
                        DialogRow(
                            title="Actions",
                            description="Actions power menu",
                            child=[self.actions_table],
                            value_getter=self.actions_table.get_data,
                            on_change=lambda x: user.set_powermenu_actions(x),
                            clear_on_cancel=self.actions_table.clear,
                        ),
                    ],
                ),
            ]
        )


class InterfaceTab(BaseTab):
    def __init__(self):
        super().__init__(
            child=[
                BarCategory(),
                LauncherCategory(),
                PowerMenuCategory(),
            ]
        )

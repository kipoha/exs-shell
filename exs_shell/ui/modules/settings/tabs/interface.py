from ignis.widgets import Box, Button, Entry, Label, Separator

from exs_shell.app.vars import BAR_WIDGETS
from exs_shell.configs.user import bar, user
from exs_shell.interfaces.enums.configs.position import TopBottom
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.interfaces.types import AnyDict
from exs_shell.ui.modules.settings.tabs.base import BaseTab, BaseCategory
from exs_shell.ui.modules.settings.widgets import (
    CategoryLabel,
    DnDBox,
    SettingsRow,
    DialogRow,
    SelectRow,
    SwitchRow,
    SpinRow,
)


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
                    description="Widgets2",
                    child=[
                        DialogRow(
                            title="Widgets3",
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
                Separator(),
                SettingsRow(
                    Icons.battery.CRITICAL,
                    title="Battery Critical Percentage",
                    description="Battery critical percentage",
                    child=[
                        SpinRow(
                            min=0,
                            max=100,
                            step=1,
                            value=user.bind("critical_percentage"),
                            on_change=lambda x: user.set_critical_percentage(x),
                        )
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
        print(widgets)
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
        action_children = []

        for i in user.get_actions_objs():
            action_children.append(
                Box(
                    child=[
                        Entry(
                            text=i.name,
                            css_classes=["settings-row-dialog-entry"],
                            width_request=150,
                        ),
                        Entry(
                            text=i.command,
                            placeholder_text="Example: {terminal_format} tmux",
                            css_classes=["settings-row-dialog-entry"],
                            width_request=250,
                        ),
                        Entry(
                            text=i.icon,
                            css_classes=["settings-row-dialog-entry"],
                            width_request=250,
                        ),
                        Button(
                            label=Icons.ui.WINDOW_CLOSE,
                            on_click=lambda _: _.parent.unparent(),
                            css_classes=["settings-row-dialog-button"],
                        ),
                    ],
                    spacing=10,
                    css_classes=["settings-row-list-obj"],
                )
            )
        self.action_list = Box(
            vertical=True,
            css_classes=["settings-row-list-objs"],
            child=action_children,
            halign="fill",
            hexpand=True,
        )
        self.action_button_add = Button(
            label=Icons.ui.ADD,
            halign="fill",
            css_classes=["settings-row-dialog-button-enter"],
            on_click=lambda _: self.action_list.append(
                Box(
                    child=[
                        Entry(
                            text="",
                            css_classes=["settings-row-dialog-entry"],
                            width_request=150,
                        ),
                        Entry(
                            text="",
                            css_classes=["settings-row-dialog-entry"],
                            width_request=250,
                        ),
                        Entry(
                            text="",
                            css_classes=["settings-row-dialog-entry"],
                            width_request=250,
                        ),
                        Button(
                            label=Icons.ui.WINDOW_CLOSE,
                            on_click=lambda _: _.parent.unparent(),
                            css_classes=["settings-row-dialog-button"],
                        ),
                    ],
                    spacing=10,
                    css_classes=["settings-row-list-obj"],
                )
            ),
        )
        self.actions_box = Box(
            vertical=True,
            css_classes=["settings-row-list-edit"],
            child=[
                self.action_list,
                self.action_button_add,
            ],
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
                            child=[self.actions_box],
                            value_getter=self.get_actions,
                            on_change=lambda x: user.set_actions(x),
                            clear_on_cancel=self.clear_on_cancel_actions,
                        ),
                    ],
                ),
            ]
        )

    def get_actions(self) -> list[AnyDict]:
        child = self.action_list.get_child()
        actions = []
        for c in child:
            sub_child = c.get_child()
            name, command, icon = (
                sub_child[0].get_text(),
                sub_child[1].get_text(),
                sub_child[2].get_text(),
            )
            actions.append({"name": name, "command": command, "icon": icon})
        return actions

    def on_change_actions(self, actions: list[AnyDict]):
        user.actions.clear()
        user.actions.extend(actions)

    def clear_on_cancel_actions(self):
        self.action_list.set_child([])
        for a in user.get_actions_objs():
            self.action_list.append(
                Box(
                    child=[
                        Entry(
                            text=a.name,
                            css_classes=["settings-row-dialog-entry"],
                            width_request=150,
                        ),
                        Entry(
                            text=a.command,
                            css_classes=["settings-row-dialog-entry"],
                            width_request=250,
                        ),
                        Entry(
                            text=a.icon,
                            css_classes=["settings-row-dialog-entry"],
                            width_request=250,
                        ),
                        Button(
                            label=Icons.ui.WINDOW_CLOSE,
                            on_click=lambda _: _.parent.unparent(),
                            css_classes=["settings-row-dialog-button"],
                        ),
                    ],
                    spacing=10,
                    css_classes=["settings-row-list-obj"],
                )
            )


class InterfaceTab(BaseTab):
    def __init__(self):
        super().__init__(
            child=[
                BarCategory(),
                LauncherCategory(),
            ]
        )

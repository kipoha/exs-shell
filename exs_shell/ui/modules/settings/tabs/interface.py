from ignis.widgets import Entry, Separator

from exs_shell.configs.user import bar, user
from exs_shell.interfaces.enums.configs.position import TopBottom
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.ui.modules.settings.tabs.base import BaseTab, BaseCategory
from exs_shell.ui.modules.settings.widgets import (
    CategoryLabel,
    DialogRow,
    SettingsRow,
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


class InterfaceTab(BaseTab):
    def __init__(self):
        super().__init__(
            child=[
                BarCategory(),
            ]
        )

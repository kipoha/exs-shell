from ignis.widgets import Separator

from exs_shell.configs.user import bar
from exs_shell.interfaces.enums.configs.position import TopBottom
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.ui.modules.settings.tabs.base import BaseTab, BaseCategory
from exs_shell.ui.modules.settings.widgets import (
    CategoryLabel,
    SettingsRow,
    SelectRow,
    SwitchRow,
)


class BarCategory(BaseCategory):
    def __init__(self):
        super().__init__(
            child=[
                CategoryLabel(title="Bar", icon=Icons.ui.INTERFACE),
                SettingsRow(
                    title="Show",
                    description="Show bar",
                    child=[
                        SwitchRow(
                            active=bar.bind("show"),  # type: ignore
                            on_change=lambda active: bar.set_show(active),
                        )
                    ],
                ),
                Separator(),
                SettingsRow(
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
            ]
        )


class InterfaceTab(BaseTab):
    def __init__(self):
        super().__init__(child=[
            BarCategory(),
        ])

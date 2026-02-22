from ignis.widgets import Label, Separator

from exs_shell.configs.user import weather
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.ui.modules.settings.tabs.base import BaseTab, BaseCategory
from exs_shell.ui.modules.settings.widgets import (
    CategoryLabel,
    SettingsRow,
    DialogRow,
    SwitchRow,
)


class NetworkTab(BaseTab):
    def __init__(self):
        super().__init__(child=[Label(label="Soon...")])

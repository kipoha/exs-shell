from ignis.widgets import Separator

from exs_shell.configs.user import weather
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.ui.modules.settings.tabs.base import BaseTab, BaseCategory
from exs_shell.ui.modules.settings.widgets import (
    CategoryLabel,
    SettingsRow,
    DialogRow,
    SwitchRow,
)


class LockTab(BaseTab):
    def __init__(self):
        super().__init__(child=[])

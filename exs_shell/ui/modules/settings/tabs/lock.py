from ignis.widgets import Separator
from libexs.enums.icons import Icons
from libexs.settings.base import BaseCategory, BaseTab
from libexs.settings.widgets import CategoryLabel, SelectRow, SettingsRow, SpinRow, SwitchRow

from exs_shell.configs.user import lock
from exs_shell.interfaces.enums.configs.position import LockEntryPosition


class LockCategory(BaseCategory):
    def __init__(self):
        super().__init__(
            child=[
                CategoryLabel(title="Lock", icon=Icons.ui.LOCK),
                SettingsRow(
                    title="Entry Visibility",
                    description="Lock entry visibility password",
                    child=[
                        SwitchRow(
                            lock.bind("entry_visibility"),
                            lambda x: lock.set_entry_visibility(x),
                        )
                    ],
                ),
                Separator(),
                SettingsRow(
                    title="Entry Position",
                    child=[
                        SelectRow(
                            LockEntryPosition.aligns,
                            lambda x: lock.set_entry_position(x),
                            active=lock.entry_position,
                        )
                    ],
                ),
                Separator(),
                SettingsRow(
                    title="Blur Radius",
                    child=[
                        SpinRow(
                            lambda x: lock.set_blur_radius(x),
                            0,
                            100,
                            1,
                            lock.bind("blur_radius"),
                        )
                    ],
                ),
            ]
        )


class LockTab(BaseTab):
    def __init__(self):
        super().__init__(child=[LockCategory()])

from typing import Any
from ignis.services.bluetooth import BluetoothService
from ignis.widgets import Label, Separator

from exs_shell import register
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.state import State
from exs_shell.ui.modules.settings.tabs.base import BaseTab, BaseCategory
from exs_shell.ui.modules.settings.widgets import (
    CategoryLabel,
    SettingsRow,
    SwitchRow,
)


@register.event
class BluetoothCategory(BaseCategory):
    def __init__(self):
        self.bluetooth: BluetoothService = State.services.bluetooth
        self.switcher = SwitchRow(
            self.bluetooth.powered,  # type: ignore
            lambda _: setattr(self.bluetooth, "powered", _),
        )
        super().__init__(
            child=[
                CategoryLabel(
                    title="Bluetooth",
                    icon=Icons.ui.BLUETOOTH,
                ),
                SettingsRow(
                    title="Bluetooth",
                    description="Enable Bluetooth",
                    child=[self.switcher],
                ),
            ]
        )

    @register.events.bluetooth("notify::powered")
    def __powered(self, bluetooth: BluetoothService, *_: Any):
        self.switcher.set_active(bluetooth.powered)


class BluetoothTab(BaseTab):
    def __init__(self):
        super().__init__(child=[BluetoothCategory()])

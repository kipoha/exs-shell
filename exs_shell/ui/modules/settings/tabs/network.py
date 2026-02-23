from typing import Any
from ignis.widgets import Label, Separator
from ignis.services.network import NetworkService, Wifi
# from ignis.services.network import (
#     NetworkService,
#     Wifi,
#     WifiDevice,
#     WifiAccessPoint,
#     WifiConnectDialog,
#     Ethernet,
#     EthernetDevice,
#     ActiveAccessPoint,
#     STATE,
# )

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
class NetworkCategory(BaseCategory):
    def __init__(self):
        self.network: NetworkService = State.services.network
        self.switcher = SwitchRow(
            self.network.wifi.enabled,  # type: ignore
            lambda _: setattr(self.network.wifi, "enabled", _),
        )
        super().__init__(
            child=[
                CategoryLabel(
                    title="Wi-Fi and Ethernet",
                    icon=Icons.wifi.CONNECTED,
                ),
                SettingsRow(
                    title="Wi-Fi",
                    description="Enable Wi-Fi",
                    child=[self.switcher],
                ),
            ]
        )

    @register.events.network("notify::enabled", "wifi")
    def __enabled(self, wifi: Wifi, *_: Any):
        self.switcher.set_active(wifi.enabled)


class NetworkTab(BaseTab):
    def __init__(self):
        super().__init__(child=[NetworkCategory()])

from typing import Any

from ignis.widgets import Box, Button, Label
from ignis.services.network import (
    NetworkService,
    Wifi,
    Ethernet,
)

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
from exs_shell.ui.widgets.custom.icon import Icon
from exs_shell.utils.commands import run_command


@register.event
class WifiWidget(Box):
    def __init__(self, scale: float = 1.0, **kwargs: Any):
        self.network: NetworkService = State.services.network
        self.scale = scale
        self.icon = Icon(
            label=Icons.wifi.DISABLED
            if not self.network.wifi.enabled
            else Icons.wifi.CONNECTED,
            size="m",
        )
        self.label = Label(
            label="Wifi", css_classes=["control-center-quick-panel-wifi-label"]
        )
        self.button_enable = Button(
            child=Box(
                child=[self.icon, self.label], spacing=5 * self.scale, hexpand=True
            ),
            on_click=lambda _: self.network.wifi.set_enabled(
                not self.network.wifi.enabled
            ),
            css_classes=[
                "control-center-quick-panel-wifi-button-enable",
                "active" if self.network.wifi.enabled else "",
            ],
            halign="fill",
        )
        self.button_open = Button(
            child=Icon(label=Icons.ui.OPEN_IN_WINDOW, size="m"),
            on_click=lambda _: run_command("settings", "wifi"),
            css_classes=["control-center-quick-panel-wifi-button-open"],
            halign="end",
        )
        self._box = Box(
            css_classes=["control-center-quick-panel-wifi"],
            child=[self.button_enable, self.button_open],
            hexpand=True,
        )
        super().__init__(child=[self._box], hexpand=True, **kwargs)

    @register.events.network("notify::enabled", "wifi")
    def __enabled(self, wifi: Wifi, *_: Any):
        if wifi.enabled:
            self.icon.set_label(Icons.wifi.CONNECTED)
            self.button_enable.add_css_class("active")
        else:
            self.icon.set_label(Icons.wifi.DISABLED)
            self.button_enable.remove_css_class("active")

    @register.events.network("notify::is-connected", "ethernet")
    def __connected(self, ethernet: Ethernet, *_: Any):
        if ethernet.is_connected:
            self.icon.set_label(Icons.wifi.CONNECTED)
        else:
            self.icon.set_label(Icons.wifi.DISCONNECTED)

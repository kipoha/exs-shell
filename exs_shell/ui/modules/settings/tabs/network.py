from typing import Any

from loguru import logger

from gi.repository import Gtk, GLib, Gdk  # type: ignore

from ignis.widgets import Box, Entry, Label, Separator, Button
from ignis.services.network import (
    NetworkService,
    Wifi,
    WifiDevice,
    WifiAccessPoint,
)

from exs_shell import register
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.state import State
from exs_shell.ui.modules.settings.tabs.base import BaseTab, BaseCategory
from exs_shell.ui.modules.settings.widgets import (
    CategoryLabel,
    SettingsRow,
    SwitchRow,
)
from exs_shell.ui.widgets.custom.icon import Icon
from exs_shell.utils.loop import run_async_task


@register.event
class NetworkCategory(BaseCategory):
    def __init__(self):
        self._updating = False
        self.network: NetworkService = State.services.network
        self.switcher = SwitchRow(
            self.network.wifi.enabled,  # type: ignore
            lambda _: setattr(self.network.wifi, "enabled", _),
        )
        self.wifi_list_box = Box(
            vertical=True, spacing=2, css_classes=["settings-network-list-container"]
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
                Separator(),
                SettingsRow(
                    title="Refresh",
                    description="Refresh Wifi List",
                    child=[
                        Button(
                            child=Box(
                                child=[
                                    Icon(label=Icons.ui.REFRESH, size="m"),
                                    Label(label="Refresh", halign="start", justify="left", valign="center"),
                                ],
                                spacing=5,
                            ),
                            on_click=self.on_update,
                            css_classes=["settings-row-button"],
                        )
                    ],
                ),
                # Separator(),
                SettingsRow(
                    vertical=True,
                    child=[self.wifi_list_box],
                ),
            ]
        )

    @register.events.network("notify::enabled", "wifi")
    @register.events.network("notify::is-connected", "wifi")
    def on_update(self, *_: Any):
        if getattr(self, "_updating", False):
            return
        run_async_task(self.update())

    async def update(self):
        if getattr(self, "_updating", False):
            return
        self._updating = True
        wifi: Wifi = self.network.wifi
        if self.switcher.active != self.network.wifi.enabled:
            self.switcher.set_active(self.network.wifi.enabled)

        try:
            for child in list(self.wifi_list_box.get_child()):
                child.unparent()

            if wifi.enabled:
                aps: list[WifiAccessPoint] = []
                devices: list[WifiDevice] = wifi.devices
                for device in devices:
                    await device.scan()
                    aps.extend(device.access_points)

                if not aps:
                    self.wifi_list_box.append(
                        Label(
                            label="No networks found.",
                            halign="center",
                            vexpand=True,
                            css_classes=["settings-no-networks-label"],
                        )
                    )
                else:
                    for ap in aps:
                        if row := self.create_access_point_row(ap):
                            self.wifi_list_box.append(row)
            else:
                self.wifi_list_box.append(
                    Label(label="Wi-Fi is disabled.", halign="center", vexpand=True)
                )
        finally:
            self._updating = False

    def create_access_point_row(self, ap: WifiAccessPoint):
        if not ap.ssid:
            return None
        row_content = Box(spacing=10, halign="fill", hexpand=True)

        icon_name = Icons.wifi.get_icon_ap(ap)

        icon = Icon(
            label=icon_name,
            size="m",
            halign="start",
            justify="left",
        )
        ssid_label = Label(label=ap.ssid, hexpand=True, halign="start")
        row_content.append(icon)
        row_content.append(ssid_label)

        if ap.is_connected:
            row_content.append(
                Label(
                    label="Connected",
                    css_classes=["settings-network-connected-status-label"],
                )
            )
            row_button = Button(
                on_click=lambda *_: run_async_task(
                    self._disconnect_wifi_and_refresh(ap)
                ),
                child=row_content,
                css_classes=["settings-network-row"],
            )
        elif ap.psk:
            row_button = Button(
                on_click=lambda *_: run_async_task(
                    self._connect_wifi_and_refresh(ap, ap.psk)  # type: ignore
                ),
                child=row_content,
                css_classes=["settings-network-row"],
            )
        else:

            def connect():
                controller = Gtk.EventControllerFocus()
                entry = Entry(
                    placeholder_text="Password",
                    css_classes=["settings-network-entry"],
                    width_request=100,
                    visibility=False,
                    on_accept=lambda e: run_async_task(
                        self._connect_wifi_and_refresh(ap, e.text, row_content, entry)
                    ),
                )

                def on_leave(controller):
                    def remove():
                        if entry.get_parent() is row_content:
                            entry.unparent()
                        return False

                    GLib.idle_add(remove)

                controller.connect("leave", on_leave)
                entry.add_controller(controller)
                key_controller = Gtk.EventControllerKey()

                def on_key_pressed(controller, keyval, keycode, state):
                    if keyval == Gdk.KEY_Escape:
                        if entry.get_parent() is row_content:
                            entry.unparent()
                        return True
                    return False

                key_controller.connect("key-pressed", on_key_pressed)
                entry.add_controller(key_controller)

                row_content.append(entry)
                entry.grab_focus()

            row_button = Button(
                on_click=lambda *_: connect(),
                child=row_content,
                css_classes=["settings-network-row"],
            )

        return row_button

    async def _connect_wifi_and_refresh(
        self,
        ap: WifiAccessPoint,
        password: str,
        row_content: Box | None = None,
        entry: Entry | None = None,
    ):
        async def reject():
            if row_content and entry:
                if entry not in row_content.get_child():
                    row_content.append(entry)

                entry.set_text("")
                entry.set_placeholder_text("Rejected")
                entry.grab_focus()

        try:
            if not password or len(password) < 8:
                await reject()
                self.on_update()
            await ap.connect_to(password)
        except Exception as e:
            logger.error(e)
            await reject()

    async def _disconnect_wifi_and_refresh(self, ap: WifiAccessPoint):
        await ap.disconnect_from()
        self.on_update()


class NetworkTab(BaseTab):
    def __init__(self):
        super().__init__(child=[NetworkCategory()])

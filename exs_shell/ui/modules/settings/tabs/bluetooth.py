from asyncio import sleep
from typing import Any
from ignis.services.bluetooth import BluetoothService, BluetoothDevice
from ignis.widgets import Box, Button, Label, Separator

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
class BluetoothCategory(BaseCategory):
    def __init__(self):
        self.bluetooth: BluetoothService = State.services.bluetooth
        self.switcher = SwitchRow(
            self.bluetooth.powered,  # type: ignore
            lambda _: setattr(self.bluetooth, "powered", _),
        )
        self.device_list_box = Box(
            vertical=True,
            spacing=2,
            css_classes=["settings-bluetooth-device-list-container"],
        )
        self.button_icon = Icon(label=Icons.ui.BLUETOOTH_SEARCHING, size="m")
        self.button_label = Label(
            label="Scan for Devices", halign="start", justify="left", valign="center"
        )
        self.button = Button(
            child=Box(
                child=[
                    self.button_icon,
                    self.button_label,
                ],
                spacing=5,
            ),
            on_click=lambda _: run_async_task(self.start_scan()),
            css_classes=["settings-row-button"],
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
                Separator(),
                SettingsRow(
                    title="Scan for Devices",
                    description="Scan for Bluetooth devices",
                    child=[self.button],
                ),
                SettingsRow(
                    vertical=True,
                    child=[self.device_list_box],
                )
            ]
        )

    @register.events.bluetooth("notify::powered")
    @register.events.bluetooth("device-added")
    def on_update(self, bluetooth: BluetoothService, *_: Any):
        run_async_task(self.update())

    async def start_scan(self):
        self.button.set_sensitive(False)
        self.button_label.label = "Scanning..."
        self.button_icon.label = Icons.ui.BLUETOOTH_SEARCHING

        for child in list(self.device_list_box.get_child()):
            self.device_list_box.remove(child)
        self.device_list_box.append(
            Label(label="Scanning...", halign="center", vexpand=True)
        )

        self.bluetooth.set_setup_mode(True)
        await sleep(15)

        self.bluetooth.set_setup_mode(False)

        self.button.set_sensitive(True)
        self.button_label.label = "Scan for Devices"
        self.button_icon.label = Icons.ui.BLUETOOTH_SEARCHING
        await self.update()

    async def update(self):
        if self.switcher.active != self.bluetooth.powered:
            self.switcher.set_active(self.bluetooth.powered)

        for child in list(self.device_list_box.get_child()):
            self.device_list_box.remove(child)

        if self.bluetooth.powered:
            found_devices = self.bluetooth.devices
            if not found_devices:
                self.device_list_box.append(
                    Label(
                        label="No devices found.",
                        halign="center",
                        vexpand=True,
                        css_classes=["settings-bluetooth-no-devices-label"],
                    )
                )
            else:
                for device in found_devices:
                    device_row = self.create_device_row(device)
                    self.device_list_box.append(device_row)
                    device.connect("removed", lambda *_: run_async_task(self.update()))
        else:
            self.device_list_box.append(
                Label(label="Bluetooth is off.", halign="center", vexpand=True)
            )

    def create_device_row(self, device: BluetoothDevice) -> Button:
        icon_map = {
            "Headset": Icons.ui.HEADSET,
            "Audio device": Icons.ui.AUDIO_DEVICE,
            "Keyboard": Icons.ui.KEYBOARD,
            "Mouse": Icons.ui.MOUSE,
            "Phone": Icons.ui.PHONE,
            "Camera": Icons.ui.CAMERA,
            "Computer": Icons.ui.COMPUTER,
            "Unknown": Icons.ui.BLUETOOTH_CONNECTED,
        }

        icon_name = device.icon_name

        mapped_icon = icon_map.get(device.device_type)
        if mapped_icon:
            icon_name = mapped_icon

        row_content = Box(spacing=10, halign="fill", hexpand=True)

        icon = Icon(
            label=icon_name,
            size="m",
        )
        alias_label = Label(label=device.alias, hexpand=True, halign="start")

        row_content.append(icon)
        row_content.append(alias_label)

        if device.connected:
            row_content.append(
                Label(label="Connected", css_classes=["settings-bluetooth-connected-status-label"])
            )
            button_handler = lambda *_: run_async_task(device.disconnect_from())
        else:
            row_content.append(
                Label(label="Not Connected", css_classes=["settings-bluetooth-not-connected-status-label"])
            )
            button_handler = lambda *_: run_async_task(device.connect_to())

        row_button = Button(
            on_click=button_handler,
            child=row_content,
            css_classes=["settings-bluetooth-row"],
        )
        return row_button


class BluetoothTab(BaseTab):
    def __init__(self):
        super().__init__(child=[BluetoothCategory()])

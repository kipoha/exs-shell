from typing import Any

from ignis.widgets import Box, Button, Label
from ignis.services.bluetooth import BluetoothService

from exs_shell import register
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.state import State
from exs_shell.utils.commands import run_command


@register.event
class BluetoothWidget(Box):
    def __init__(self, scale: float = 1.0, **kwargs: Any):
        self.bluetooth: BluetoothService = State.services.bluetooth
        self.scale = scale
        self.icon = Label(
            label=Icons.ui.BLUETOOTH,
            css_classes=["control-center-quick-panel-bluetooth-icon"],
        )
        self.label = Label(
            label="Bluetooth",
            css_classes=["control-center-quick-panel-bluetooth-label"],
        )
        self.button_enable = Button(
            child=Box(
                child=[self.icon, self.label], spacing=5 * self.scale, hexpand=True
            ),
            on_click=lambda _: self.bluetooth.set_powered(not self.bluetooth.powered),
            css_classes=[
                "control-center-quick-panel-bluetooth-button-enable",
                "active" if self.bluetooth.powered else "",
            ],
        )
        self.button_open = Button(
            child=Label(label=Icons.ui.OPEN_IN_WINDOW),
            on_click=lambda _: run_command("settings", "bluetooth"),
            css_classes=["control-center-quick-panel-bluetooth-button-open"],
        )
        self._box = Box(
            css_classes=["control-center-quick-panel-bluetooth"],
            child=[
                self.button_enable,
                self.button_open,
            ],
            hexpand=True,
        )
        super().__init__(child=[self._box], hexpand=True, **kwargs)

    @register.events.bluetooth("notify::powered")
    def __powered(self, bluetooth: BluetoothService, *_: Any):
        if bluetooth.powered:
            self.button_enable.add_css_class("active")
        else:
            self.button_enable.remove_css_class("active")

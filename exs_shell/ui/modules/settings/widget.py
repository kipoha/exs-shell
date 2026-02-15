from ignis.app import IgnisApp
from ignis.widgets import Label, Button, Box, RegularWindow, Scroll

from exs_shell import register
from exs_shell.app.vars import NAMESPACE
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.ui.factory.navigation import Navigation
from exs_shell.ui.modules.settings.tabs.main import MainTab
from exs_shell.ui.modules.settings.tabs.appearance import AppearanceTab
from exs_shell.ui.modules.settings.tabs.interface import InterfaceTab
from exs_shell.ui.modules.settings.tabs.lock import LockTab
from exs_shell.ui.modules.settings.tabs.services import ServicesTab
from exs_shell.ui.modules.settings.tabs.devices import DevicesTab
from exs_shell.ui.modules.settings.tabs.network import NetworkTab
from exs_shell.ui.modules.settings.tabs.bluetooth import BluetoothTab
from exs_shell.ui.modules.settings.tabs.system import SystemTab
from exs_shell.ui.modules.settings.tabs.about import AboutTab


@register.window
@register.commands
class Settings(RegularWindow):
    def __init__(self) -> None:
        main_box = Box(vertical=True, vexpand=True, valign="fill", css_classes=["settings"])
        self.reload_button = Button(
            child=Label(label=Icons.ui.REFRESH),
            on_click=lambda _: IgnisApp.get_initialized().reload(),
            css_classes=["settings-reload-button"],
        )

        self._test = Box(
            vertical=True,
            vexpand=True,
            hexpand=True,
        )
        for _ in range(100):
            self._test.append(Label(label="AAA"))

        self.content = Scroll(hexpand=True, halign="fill", child=self._test, hscrollbar_policy="never")
        self.tabs = {
            "main": (Icons.ui.MAIN, "Main"),
            "appearance": (Icons.ui.PALLETTE, "Appearance"),
            "interface": (Icons.ui.INTERFACE, "Interface"),
            "lock": (Icons.ui.LOCK, "Lock"),
            "services": (Icons.ui.SERVICES, "Services"),
            "devices": (Icons.ui.DEVICES, "Devices"),
            "network": (Icons.wifi.CONNECTED, "Network"),
            "bluetooth": (Icons.ui.BLUETOOTH, "Bluetooth"),
            "system": (Icons.ui.SYSTEM, "System"),
            "about": (Icons.ui.INFO, "About"),
        }

        self.active_tab_label = Label(
            label="", css_classes=["settings-active-tab-label"]
        )
        self.active_tab_label_icon = Label(label=Icons.ui.MAIN, css_classes=["settings-header-title-icon"])
        self.nav = Navigation(self.tabs, on_select=self.on_select, default="main")
        self.nav.vexpand = True
        self.nav.append(Box(vexpand=True))
        self.nav.append(self.reload_button)

        header = Box(css_classes=["settings-header-bar"], spacing=10)
        header.append(self.active_tab_label_icon)
        header.append(Label(label="Exs Settings", css_classes=["settings-header-title"]))
        header.append(Label(label=Icons.ui.RIGHT, css_classes=["settings-breadcrumb-separator"]))
        header.append(self.active_tab_label)

        content_box = Box(vexpand=True)
        content_box.append(self.nav)
        content_box.append(self.content)

        main_box.append(header)
        main_box.append(content_box)

        super().__init__(
            f"{NAMESPACE}_settings",
            title="Exs Settings",
            visible=False,
            default_width=1200,
            default_height=900,
            hide_on_close=True,
            css_classes=["settings-window"],
            child=main_box,
        )

    def on_select(self, key: str) -> None:
        self.active_tab_label_icon.label = self.tabs[key][0]
        self.active_tab_label.label = self.tabs[key][1]
        tab = None
        match key:
            case "main":
                tab = MainTab()
            case "appearance":
                tab = AppearanceTab()
            case "interface":
                tab = InterfaceTab()
            case "lock":
                tab = LockTab()
            case "services":
                tab = ServicesTab()
            case "devices":
                tab = DevicesTab()
            case "network":
                tab = NetworkTab()
            case "bluetooth":
                tab = BluetoothTab()
            case "system":
                tab = SystemTab()
            case "about":
                tab = AboutTab()
        if tab:
            self.content.set_child(tab)

    @register.command(group="settings", description="Toggle settings")
    def toggle(self):
        self.set_visible(not self.visible)

    @register.command(group="settings", description="Open Wifi")
    def wifi(self):
        self.nav.select("network")
        self.set_visible(True)

    @register.command(group="settings", description="Open Bluetooth")
    def bluetooth(self):
        self.nav.select("bluetooth")
        self.set_visible(True)

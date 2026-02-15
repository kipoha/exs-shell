from ignis.app import IgnisApp
from ignis.widgets import Label, Button, Box, RegularWindow, Scroll

from exs_shell import register
from exs_shell.app.vars import NAMESPACE
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.ui.factory.navigation import Navigation


@register.window
@register.commands
class Settings(RegularWindow):
    def __init__(self) -> None:
        main_box = Box(vertical=True, vexpand=True, valign="fill", css_classes=["settings"])
        # self.reload_button = Button(
        #     child=Label(label=Icons.ui.REFRESH),
        #     on_click=lambda _: IgnisApp.get_initialized().reload(),
        #     css_classes=["settings-reload-button"],
        # )

        self._test = Box(
            vertical=True,
            vexpand=True,
            hexpand=True,
        )
        for _ in range(100):
            self._test.append(Label(label="AAA"))

        self.content = Scroll(hexpand=True, halign="fill", child=self._test)
        self.tabs = {
            "main": (Icons.ui.MAIN, "Main"),
            "appearance": (Icons.ui.PALLETTE, "Appearance"),
            "interface": (Icons.ui.INTERFACE, "Interface"),
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
        nav = Navigation(self.tabs, on_select=self.on_select, default="main")
        nav.vexpand = True
        nav.append(Box(vexpand=True))
        # nav.append(self.reload_button)

        header = Box(css_classes=["settings-header-bar"], spacing=10)
        header.append(Label(label=Icons.ui.SYSTEM, css_classes=["settings-header-title-icon"]))
        header.append(Label(label="Exs Settings", css_classes=["settings-header-title"]))
        header.append(Label(label=Icons.ui.RIGHT, css_classes=["settings-breadcrumb-separator"]))
        header.append(self.active_tab_label)

        content_box = Box(vexpand=True)
        content_box.append(nav)
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
        self.active_tab_label.label = self.tabs[key][1]
        tab = None
        match key:
            case "main":
                tab = self._test
        if tab:
            self.content.set_child(tab)

    @register.command(group="settings", description="Toggle settings")
    def toggle(self):
        self.set_visible(not self.visible)

    @register.command(group="settings", description="Test")
    def test(self):
        from gi.repository import Pango

        def get_icon_width(label: Label):
            layout = label.get_layout()
            logical_extents, _ = layout.get_pixel_extents()
            return logical_extents.width

        icons = ["", "", "", Icons.wifi.CONNECTED]
        labels = [Label(label=ic) for ic in icons]
        max_width = max(get_icon_width(lbl) for lbl in labels)

# оборачиваем каждую иконку в Box с шириной max_width
        icon_boxes = [Box(width=max_width, child=lbl) for lbl in labels]
        print(icon_boxes)

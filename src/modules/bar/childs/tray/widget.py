from gi.repository import GLib, Gdk  # type: ignore
from ignis import widgets
from ignis.services.system_tray import SystemTrayService, SystemTrayItem


class SystemTrayItemButton(widgets.Button):
    def __init__(self, item: SystemTrayItem):
        self.item = item
        self.menu = item.menu.copy() if item.menu else None
        box = widgets.EventBox(
            child=[widgets.Icon(image=item.bind("icon"), pixel_size=24)],
            on_hover=lambda btn: GLib.timeout_add(150, lambda: self.popup() or False),
        )
        self._close_timeout = None

        super().__init__(
            child=widgets.Box(child=[box, self.menu]),
            setup=lambda btn: item.connect("removed", lambda x: btn.unparent()),
            tooltip_text=item.bind("tooltip"),
            on_click=lambda btn: self.popup(),
            on_right_click=lambda btn: self.popup(),
            css_classes=["tray-item"],
        )

    def popup(self):
        if self.menu:
            self.menu.popup()


class SystemTray(widgets.Box):
    def __init__(self):
        self.tray = SystemTrayService.get_default()
        super().__init__(
            setup=lambda self_: self.tray.connect("added", self.on_item_added),
            spacing=10,
        )

    def on_item_added(self, tray, item: SystemTrayItem):
        self.append(SystemTrayItemButton(item))

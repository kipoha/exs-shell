from typing import Any

from ignis.dbus_menu import DBusMenu
from ignis.services.system_tray import SystemTrayService, SystemTrayItem
from ignis.widgets import Box, EventBox, Icon

from exs_shell import register


@register.event
class SystemTrayItemButton(EventBox):
    def __init__(self, item: SystemTrayItem, scale: float):
        self.scale = scale
        self.item = item
        self.menu: DBusMenu | None = item.menu.copy() if item.menu else None
        box = Icon(image=item.bind("icon"), pixel_size=int(18 * scale))

        super().__init__(
            child=[box, self.menu],
            on_click=self.popup,
            on_right_click=self.popup,
            on_hover=self.popup,
            css_classes=["tray-item"],
        )

    @register.events.tray("removed", item=True)
    def on_item_removed(self, item: SystemTrayItem):
        self.unparent()

    def popup(self, _):
        if self.menu:
            self.menu.popup()


@register.event
@register.widget
class SystemTray(Box):
    def __init__(self, scale: float, **kwargs: Any):
        self.scale = scale
        super().__init__(spacing=10 * scale, **kwargs)

    @register.events.tray("added")
    def on_item_added(self, tray: SystemTrayService, item: SystemTrayItem):
        self.append(SystemTrayItemButton(item, self.scale))

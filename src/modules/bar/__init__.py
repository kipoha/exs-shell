from modules.bar.widgets import center, left, right
from modules.bar.childs.battery.widget import Battery
from modules.bar.childs.clock.widget import Clock
from modules.bar.childs.tray.widget import SystemTray


modules: dict[str, type] = {
    "clock": Clock,
    "battery": Battery,
    "tray": SystemTray,
}

__all__ = [
    "center",
    "left",
    "right",
    "modules",
]

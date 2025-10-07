from modules.bar.widgets import center, left, right
from modules.bar.childs.battery.widget import Battery
from modules.bar.childs.clock.widget import Clock
from modules.bar.childs.tray.widget import SystemTray
from modules.bar.childs.cava.widget import Cava


modules: dict[str, type] = {
    "clock": Clock,
    "battery": Battery,
    "tray": SystemTray,
    "cava": Cava
}

__all__ = [
    "center",
    "left",
    "right",
    "modules",
]

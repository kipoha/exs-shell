from modules.bar.childs.battery.widget import Battery
from modules.bar.childs.clock.widget import Clock
from modules.bar.childs.tray.widget import SystemTray
from modules.bar.childs.cava.widget import Cava
from modules.bar.childs.layout.widget import KeyboardLayout


modules: dict[str, type] = {
    "clock": Clock,
    "battery": Battery,
    "tray": SystemTray,
    "cava": Cava,
    "layout": KeyboardLayout
}

__all__ = [
    "modules",
]

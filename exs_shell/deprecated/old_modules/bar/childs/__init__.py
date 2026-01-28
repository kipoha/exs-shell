from exs_shell.modules.bar.childs.battery.widget import Battery
from exs_shell.modules.bar.childs.clock.widget import Clock
from exs_shell.modules.bar.childs.tray.widget import SystemTray
from exs_shell.modules.bar.childs.cava.widget import Cava
from exs_shell.modules.bar.childs.layout.widget import KeyboardLayout


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

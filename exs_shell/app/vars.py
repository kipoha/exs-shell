from exs_shell.ui.widgets.custom.battery import Battery
from exs_shell.ui.widgets.custom.cava_tui import CavaLabel
from exs_shell.ui.widgets.custom.clock import Clock
from exs_shell.ui.widgets.custom.kb_layout import KeyboardLayout
from exs_shell.ui.widgets.custom.tray import SystemTray


APP_NAME = "Exs Shell"
NAMESPACE = "EXS_SHELL"
NAME = "exs-shell"


BAR_WIDGETS: dict[str, type] = {
    "battery": Battery,
    "clock": Clock,
    "kb_layout": KeyboardLayout,
    "tray": SystemTray,
    "cava_tui": CavaLabel,
}

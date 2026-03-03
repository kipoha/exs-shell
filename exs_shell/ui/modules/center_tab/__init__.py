from exs_shell.ui.modules.center_tab.widget import CenterTab
from exs_shell.ui.widgets.custom.mouse_trigger import MouseTrigger
from exs_shell.utils import monitor, window


def on_hover(monitor_id: int) -> None:
    window.get(f"centertab{monitor_id}").set_visible(True)


def init() -> None:
    monitor.init_windows(CenterTab)
    monitor.init_windows(
        MouseTrigger,
        namespace="center_tab_trigger",
        size=(100, 1),
        on_hover=on_hover,
        anchor=["top"],
    )

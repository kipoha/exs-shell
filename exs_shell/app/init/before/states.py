from ignis.window_manager import WindowManager
from libexs import State


def init() -> None:
    State.widgets
    State.services
    State.windows
    State.commands
    State["plugin_settings"] = []
    State.window_manager = WindowManager()

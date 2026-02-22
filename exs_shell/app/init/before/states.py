from ignis.window_manager import WindowManager

from exs_shell.state import State


def init() -> None:
    State.widgets
    State.services
    State.windows
    State.commands
    State.window_manager = WindowManager()

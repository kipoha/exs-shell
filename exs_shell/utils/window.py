from exs_shell.state import State
from exs_shell.interfaces.protocols.window import IWindow


def get(name: str) -> IWindow:
    return State.windows[name]

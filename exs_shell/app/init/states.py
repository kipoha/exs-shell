from ignis.services.niri import NiriService
from ignis.services.system_tray import SystemTrayService

from exs_shell.state import State
from exs_shell.ui.services.cava import Cava


def init() -> None:
    State.widgets
    State.services
    Cava()
    State.services.niri = NiriService.get_default()
    State.services.tray = SystemTrayService.get_default()

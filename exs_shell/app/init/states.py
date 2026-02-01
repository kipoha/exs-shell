from ignis.services.niri import NiriService
from ignis.services.system_tray import SystemTrayService

from exs_shell.state import State


def init() -> None:
    State.widgets = {}
    State.niri = NiriService.get_default()
    State.tray = SystemTrayService.get_default()

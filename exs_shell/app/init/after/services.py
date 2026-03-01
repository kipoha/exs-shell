from ignis.services.mpris import MprisService

from exs_shell.state import State
from exs_shell.ui.services.battery_tracker import BatteryTrackerService
from exs_shell.ui.services.idle import IdleService

services = {
    "mpris": MprisService,
    "idle": IdleService,
    "battery_tracker": BatteryTrackerService
}


def init_services() -> None:
    for name, service in services.items():
        State.services[name] = service.get_default()


def init() -> None:
    init_services()

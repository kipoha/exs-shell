from ignis.services.niri import NiriService
from ignis.services.system_tray import SystemTrayService
from ignis.services.audio import AudioService
from ignis.services.backlight import BacklightService
from ignis.services.bluetooth import BluetoothService
from ignis.services.network import NetworkService
from ignis.services.notifications import NotificationService
from ignis.services.mpris import MprisService
from ignis.services.upower import UPowerService
from ignis.services.systemd import SystemdService

from exs_shell.state import State
from exs_shell.ui.services.cava import Cava

services = {
    "niri": NiriService,
    "tray": SystemTrayService,
    "audio": AudioService,
    "backlight": BacklightService,
    "bluetooth": BluetoothService,
    "network": NetworkService,
    "notifications": NotificationService,
    "mpris": MprisService,
    "upower": UPowerService,
    "systemd": SystemdService,
}


def init_services() -> None:
    for name, service in services.items():
        State.services[name] = service.get_default()


def init() -> None:
    Cava()
    init_services()
    from pprint import pprint
    pprint(State)

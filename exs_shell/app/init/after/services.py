from ignis.services.mpris import MprisService

from exs_shell.state import State

services = {"mpris": MprisService}


def init_services() -> None:
    for name, service in services.items():
        State.services[name] = service.get_default()


def init() -> None:
    init_services()

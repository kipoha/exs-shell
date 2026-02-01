from ignis.options_manager import OptionsGroup, OptionsManager

from exs_shell.register.events.base import _base_connector, EventDeco
from exs_shell.interfaces.types import CavaOutput
from exs_shell.state import State


def option(options_group: OptionsManager | OptionsGroup, option: str) -> EventDeco:
    return _base_connector(
        lambda _: options_group,
        "connect_option",
        option,
    )


def niri(event_name: str) -> EventDeco:
    return _base_connector(
        lambda _: State.services.niri,
        "connect",
        event_name,
    )


def tray(event_name: str) -> EventDeco:
    return _base_connector(
        lambda _: State.services.tray,
        "connect",
        event_name,
    )


def cava(output_type: CavaOutput) -> EventDeco:
    return _base_connector(
        lambda _: State.services.cava,
        f"subscribe_{output_type}",
    )

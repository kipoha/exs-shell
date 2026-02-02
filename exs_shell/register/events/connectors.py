from ignis.utils import Poll
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


def niri(signal: str) -> EventDeco:
    return _base_connector(
        lambda _: State.services.niri,
        "connect",
        signal,
    )


def tray(signal: str) -> EventDeco:
    return _base_connector(
        lambda _: State.services.tray,
        "connect",
        signal,
    )


def cava(output_type: CavaOutput) -> EventDeco:
    return _base_connector(
        lambda _: State.services.cava,
        f"subscribe_{output_type}",
    )


def notification(signal: str) -> EventDeco:
    return _base_connector(
        lambda _: State.services.notification,
        "connect",
        signal,
    )


def systemd_session(unit: str, signal: str) -> EventDeco:
    return _base_connector(
        lambda _: State.services.systemd_session.get_unit(unit),
        "connect",
        signal,
    )


def systemd_system(unit: str, signal: str) -> EventDeco:
    return _base_connector(
        lambda _: State.services.systemd_system.get_unit(unit),
        "connect",
        signal,
    )


def power_profiles(signal: str) -> EventDeco:
    return _base_connector(
        lambda _: State.services.power_profiles,
        "connect",
        signal,
    )


def audio(signal: str) -> EventDeco:
    return _base_connector(
        lambda _: State.services.audio,
        "connect",
        signal,
    )


def bluetooth(signal: str) -> EventDeco:
    return _base_connector(
        lambda _: State.services.bluetooth,
        "connect",
        signal,
    )


def network(signal: str) -> EventDeco:
    return _base_connector(
        lambda _: State.services.network,
        "connect",
        signal,
    )


def backlight(signal: str) -> EventDeco:
    return _base_connector(
        lambda _: State.services.backlight,
        "connect",
        signal,
    )


def upower(signal: str) -> EventDeco:
    return _base_connector(
        lambda _: State.services.upower,
        "connect",
        signal,
    )


if hasattr(State.services.upower, "batteries"):

    def battery(signal: str) -> EventDeco:
        return _base_connector(
            lambda _: State.services.upower.batteries[0],
            "connect",
            signal,
        )
else:

    def battery(signal: str) -> EventDeco:
        def _event_call(instance):
            pass

        def dummy(func):
            return func

        if not hasattr(dummy, "_event_calls"):
            setattr(dummy, "_event_calls", [])
        getattr(dummy, "_event_calls").append(_event_call)
        return dummy


def poll(interval_ms: int, *, bind: str | None = None) -> EventDeco:
    def decorator(func):
        def _event_call(instance):
            bound = func.__get__(instance, type(instance))
            p = Poll(interval_ms, lambda _: bound())

            if bind is not None:
                p.bind(bind)
            else:
                if not hasattr(instance, "_polls"):
                    instance._polls = []
                instance._polls.append(p)

        if not hasattr(func, "_event_calls"):
            setattr(func, "_event_calls", [])
        getattr(func, "_event_calls").append((None, None, (), {"_poll": _event_call}))
        return func

    return decorator

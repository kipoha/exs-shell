from typing import Any, Callable, TypeVar, TypeAlias

from ignis.options_manager import OptionsManager, OptionsGroup

from exs_shell.state import State

F = TypeVar("F", bound=Callable[..., Any])
EventDeco: TypeAlias = Callable[[F], F]


def register(cls: type):
    original_init = cls.__init__

    def new_init(self, *args: Any, **kwargs: Any):
        original_init(self, *args, **kwargs)
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if callable(attr) and hasattr(attr, "_event_call"):
                attr._event_call(self)  # type: ignore

    cls.__init__ = new_init
    return cls


def make_event_connector(
    target_getter: Callable[[Any], Any],
    connect_method: str,
    *connect_args: Any,
    **connect_kwargs: Any,
) -> EventDeco:
    def decorator(func: F) -> F:
        def _event_call(instance: Any) -> None:
            target = target_getter(instance)
            bound = func.__get__(instance, instance.__class__)
            getattr(target, connect_method)(*connect_args, bound, **connect_kwargs)

        func._event_call = _event_call  # type: ignore
        return func

    return decorator


def option(options_group: OptionsManager | OptionsGroup, option: str) -> EventDeco:
    return make_event_connector(
        lambda _: options_group,
        "connect_option",
        option,
    )


def niri(event_name: str) -> EventDeco:
    return make_event_connector(
        lambda _: State.niri,
        "connect",
        event_name,
    )


def tray(event_name: str) -> EventDeco:
    return make_event_connector(
        lambda _: State.tray,
        "connect",
        event_name,
    )

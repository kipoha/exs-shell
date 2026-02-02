from typing import Any, Callable, TypeVar, TypeAlias
from gi.repository import GLib  # type: ignore

F = TypeVar("F", bound=Callable[..., Any])
EventDeco: TypeAlias = Callable[[F], F]


def _base_connector(
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

        setattr(func, "_event_call", _event_call)
        return func

    return decorator


def event(cls: type):
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)

        def setup_events():
            for base in type(self).mro():
                for attr in base.__dict__.values():
                    if callable(attr) and hasattr(attr, "_event_call"):
                        method = attr.__get__(self, type(self))
                        method._event_call(self)

        GLib.idle_add(setup_events)

    cls.__init__ = new_init
    return cls

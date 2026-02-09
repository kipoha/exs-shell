from typing import Any, Callable, TypeVar, TypeAlias
from gi.repository import GLib  # type: ignore
from exs_shell.register.deco import add_post_init, run_method_handler

F = TypeVar("F", bound=Callable[..., Any])
EventDeco: TypeAlias = Callable[[F], F]


def _base_connector(
    target_getter: Callable[[Any], Any],
    connect_method: str,
    *connect_args: Any,
    **connect_kwargs: Any,
) -> EventDeco:
    def decorator(func: F) -> F:
        if not hasattr(func, "_event_calls"):
            setattr(func, "_event_calls", [])
        getattr(func, "_event_calls").append(
            (target_getter, connect_method, connect_args, connect_kwargs)
        )
        return func

    return decorator


def event_predicate(func):
    return hasattr(func, "_event_calls")


def event_handler(obj, bound):
    for target_getter, connect_method, args, kw in bound._event_calls:
        if target_getter is None and "_poll" in kw:
            kw["_poll"](obj)
        else:
            target = target_getter(obj)
            getattr(target, connect_method)(*args, bound, **kw)


def event(cls: type) -> type:
    def setup(self):
        GLib.idle_add(lambda: run_method_handler(self, event_predicate, event_handler))

    add_post_init(cls, setup)
    return cls

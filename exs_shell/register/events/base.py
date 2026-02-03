from typing import Any, Callable, TypeVar, TypeAlias
from gi.repository import GLib  # type: ignore
from exs_shell.register.deco import add_post_init

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


# def event(cls: type):
#     original_init = cls.__init__
#
#     def new_init(self: type, *args, **kwargs):
#         original_init(self, *args, **kwargs)
#
#         def setup_events():
#             for base in type(self).mro():  # type: ignore
#                 for attr in base.__dict__.values():
#                     if callable(attr) and hasattr(attr, "_event_calls"):
#                         bound = attr.__get__(self, type(self))
#                         for target_getter, connect_method, args, kw in getattr(
#                             attr, "_event_calls"
#                         ):
#                             if target_getter is None and "_poll" in kw:
#                                 kw["_poll"](self)
#                             else:
#                                 target = target_getter(self)
#                                 getattr(target, connect_method)(*args, bound, **kw)
#
#         GLib.idle_add(setup_events)
#
#     setattr(cls, "__init__", new_init)
#     return cls
def event(cls: type):
    def setup(self):
        def setup_events():
            for base in type(self).mro():
                for attr in base.__dict__.values():
                    if callable(attr) and hasattr(attr, "_event_calls"):
                        bound = attr.__get__(self, type(self))
                        for target_getter, connect_method, args, kw in getattr(
                            attr, "_event_calls"
                        ):
                            if target_getter is None and "_poll" in kw:
                                kw["_poll"](self)
                            else:
                                target = target_getter(self)
                                getattr(target, connect_method)(*args, bound, **kw)

        GLib.idle_add(setup_events)

    add_post_init(cls, setup)
    return cls

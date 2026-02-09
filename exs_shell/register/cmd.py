from functools import partial

from typing import Callable

from gi.repository import GLib  # type: ignore

from exs_shell.interfaces.types import AnyDict, AnyList
from exs_shell.register.deco import add_post_init, run_method_handler
from exs_shell.register.events.base import F
from exs_shell.interfaces.schemas.ipc.commands import Command
from exs_shell.state import State


def commands_predicate(func):
    return hasattr(func, "ipc_command")


def commands_handler(obj, bound):
    cmd_dict: dict[str, Command] = bound.ipc_command
    for name, cmd in cmd_dict.items():
        cmd.call = partial(cmd.call, obj)

        if cmd.group not in State.commands:
            State.commands[cmd.group] = {}

        State.commands[cmd.group][name] = cmd


def commands(cls: type) -> type:
    def register(self):
        GLib.idle_add(
            lambda: run_method_handler(self, commands_predicate, commands_handler)
        )

    add_post_init(cls, register)
    return cls


def command(
    group: str,
    args: AnyList = [],
    kwargs: AnyDict = {},
    name: str | None = None,
    description: str = "No description",
) -> Callable[[F], F]:
    def wrapper(func: F) -> F:
        cmd = Command(
            call=func,
            args=args,
            kwargs=kwargs,
            description=description,
            group=group,
        )
        setattr(func, "ipc_command", {name or func.__name__: cmd})
        return func

    return wrapper

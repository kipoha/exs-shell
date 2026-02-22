from typing import Any

from exs_shell.interfaces.types import Commands
from exs_shell.state import State

all_commands: Commands = State.commands


def run_command(group: str, name: str, *args: Any, **kwargs: Any) -> None:
    """
    Run a command from registered commands(in State)
    """
    cmd = all_commands[group][name]
    cmd.call(*args, **kwargs)

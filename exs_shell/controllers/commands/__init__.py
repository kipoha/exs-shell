from exs_shell.interfaces.types import Commands

from exs_shell.controllers.commands import settings


def include(*args: Commands) -> Commands:
    """include commands from another list of commands"""
    result: Commands = {}
    for cmds in args:
        result.update(cmds)
    return result


def include_commands() -> Commands:
    return include(
        settings.include(),
    )

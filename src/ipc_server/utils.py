from typing import Any

from ipc_server.commands.launcher import launcher_commands
from ipc_server.commands.notification import notification_commands
from ipc_server.commands.osd import osd_commands


def include(
    *args: dict[str, tuple[object, str, dict[str, Any], str]],
) -> dict[str, tuple[object, str, dict[str, Any], str]]:
    """include commands from another list of commands"""
    result: dict[str, tuple[object, str, dict[str, Any], str]] = {}
    for cmds in args:
        result.update(cmds)
    return result


commands = include(
    osd_commands(),
    launcher_commands(),
    notification_commands()
)

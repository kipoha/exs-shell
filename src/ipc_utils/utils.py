from typing import Any


def include(
    *args: dict[str, tuple[object, str, dict[str, Any], str]],
) -> dict[str, tuple[object, str, dict[str, Any], str]]:
    """include commands from another list of commands"""
    result: dict[str, tuple[object, str, dict[str, Any], str]] = {}
    for cmds in args:
        result.update(cmds)
    return result


def include_commands() -> dict[str, tuple[object, str, dict[str, Any], str]]:
    from ipc_utils.commands.launcher import launcher_commands
    from ipc_utils.commands.notification import notification_commands
    from ipc_utils.commands.powermenu import powermenu_commands
    from ipc_utils.commands.osd import osd_commands

    return include(
        osd_commands(),
        launcher_commands(),
        notification_commands(),
        powermenu_commands(),
    )


commands = include_commands()

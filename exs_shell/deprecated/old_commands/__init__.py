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
    from exs_shell.controllers.commands.launcher import launcher_commands
    from exs_shell.controllers.commands.notification import notification_commands
    from exs_shell.controllers.commands.powermenu import powermenu_commands
    from exs_shell.controllers.commands.osd import osd_commands
    from exs_shell.controllers.commands.settings import settings_commands
    from exs_shell.controllers.commands.clipboard import clipboard_commands
    from exs_shell.controllers.commands.actions import action_commands
    from exs_shell.controllers.commands.dashboard import dashboard_commands
    from exs_shell.controllers.commands.lockscreen import lockscreen_commands

    return include(
        osd_commands(),
        launcher_commands(),
        notification_commands(),
        powermenu_commands(),
        settings_commands(),
        clipboard_commands(),
        action_commands(),
        dashboard_commands(),
        lockscreen_commands(),
    )


commands = include_commands()

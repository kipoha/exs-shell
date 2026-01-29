from typing import Any


def launcher_commands() -> dict[str, tuple[object, str, dict[str, Any], str]]:
    from exs_shell.modules.launcher import Launcher

    launcher = Launcher.get_default()
    cmds: dict[str, tuple[object, str, dict[str, Any], str]] = {
        "toggle-launcher": (launcher, "toggle", {}, "Toggle Launcher"),
    }

    return cmds

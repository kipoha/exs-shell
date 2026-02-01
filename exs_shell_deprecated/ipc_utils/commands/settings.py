from typing import Any

from ignis.window_manager import WindowManager

from exs_shell_deprecated.config import config


def settings_commands() -> dict[str, tuple[object, str, dict[str, Any], str]]:

    window_manager = WindowManager.get_default()
    cmds: dict[str, tuple[object, str, dict[str, Any], str]] = {
        "toggle-settings": (window_manager, "toggle_window", {"window_name": f"{config.NAMESPACE}_settings"}, "Toggle Settings"),
    }

    return cmds

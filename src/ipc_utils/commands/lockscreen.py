from typing import Any
from ignis.window_manager import WindowManager
from config import config


def lockscreen_commands() -> dict[str, tuple[object, str, dict[str, Any], str]]:

    window_manager = WindowManager.get_default()
    cmds: dict[str, tuple[object, str, dict[str, Any], str]] = {
        "open-lockscreen": (window_manager, "open_window", {"window_name": f"{config.NAMESPACE}_lockscreen"}, "Open Lockscreen"),
    }

    return cmds

from typing import Any


def powermenu_commands() -> dict[str, tuple[object, str, dict[str, Any], str]]:
    from modules.powermenu import PowenMenu

    powermenu = PowenMenu.get_default()
    cmds: dict[str, tuple[object, str, dict[str, Any], str]] = {
        "toggle-powermenu": (powermenu, "toggle", {}, "Toggle Powermenu"),
    }

    return cmds

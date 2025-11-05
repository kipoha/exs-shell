from typing import Any


def dashboard_commands() -> dict[str, tuple[object, str, dict[str, Any], str]]:
    from modules.dashboard import Dashboard

    dashboard = Dashboard.get_default()
    cmds: dict[str, tuple[object, str, dict[str, Any], str]] = {
        "toggle-dashboard": (dashboard, "toggle", {}, "Toggle Dashboard"),
    }

    return cmds

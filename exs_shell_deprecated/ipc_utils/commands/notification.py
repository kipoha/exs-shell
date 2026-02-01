from typing import Any


def notification_commands() -> dict[str, tuple[object, str, dict[str, Any], str]]:
    from exs_shell_deprecated.modules.notification import NotificationCenter

    notification = NotificationCenter.get_default()
    cmds: dict[str, tuple[object, str, dict[str, Any], str]] = {
        "toggle-notification-center": (notification, "toggle", {}, "Toggle Notification Center"),
    }

    return cmds

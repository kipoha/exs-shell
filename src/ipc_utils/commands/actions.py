import subprocess

from typing import Any

from modules.notification.center import NotificationCenter
from utils.notify_system import send_notification


class Actions:
    @classmethod
    def colorpicker(cls):
        proc = subprocess.run(["hyprpicker"], capture_output=True, text=True)
        color_hex = proc.stdout.strip()

        if color_hex:
            subprocess.run(["wl-copy"], input=color_hex, text=True)
            send_notification("Color Copied", color_icon=color_hex)
        else:
            send_notification("No color selected")

    @classmethod
    def clear_notifications(cls):
        center = NotificationCenter.get_default()
        center.clear_all()


def action_commands() -> dict[str, tuple[object, str, dict[str, Any], str]]:
    cmds: dict[str, tuple[object, str, dict[str, Any], str]] = {
        "action-color-picker": (Actions, "colorpicker", {}, "Color Picker"),
        "action-clear-notifications": (
            Actions,
            "clear_notifications",
            {},
            "Clear Notifications",
        ),
    }

    return cmds

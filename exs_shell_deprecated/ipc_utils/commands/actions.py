import subprocess

from typing import Any

from exs_shell_deprecated.modules.dashboard.widget import Dashboard
from exs_shell_deprecated.modules.notification.center import NotificationCenter
from exs_shell_deprecated.utils.notify_system import send_notification


class Actions:
    _dashboard = Dashboard.get_default()
    _dashboard_pages = _dashboard.pages.pages
    _notification_center = NotificationCenter.get_default()

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
        cls._notification_center.clear_all()

    @classmethod
    def _toggle_dashboard(cls, key: str):
        target_page = cls._dashboard_pages[key].child
        visible_page = cls._dashboard.pages.stack.get_visible_child()

        if not cls._dashboard.visible or visible_page != target_page:
            cls._dashboard.open()
            cls._dashboard.pages.stack.set_visible_child(target_page)
        else:
            cls._dashboard.close()

    @classmethod
    def dashboard_main_open(cls):
        cls._toggle_dashboard("dashboard")

    @classmethod
    def dashboard_player_open(cls):
        cls._toggle_dashboard("player")

    @classmethod
    def dashboard_metrics_open(cls):
        cls._toggle_dashboard("metrics")


def action_commands() -> dict[str, tuple[object, str, dict[str, Any], str]]:
    cmds: dict[str, tuple[object, str, dict[str, Any], str]] = {
        "action-color-picker": (Actions, "colorpicker", {}, "Color Picker"),
        "action-clear-notifications": (
            Actions,
            "clear_notifications",
            {},
            "Clear Notifications",
        ),
        "action-dashboard-main-open": (
            Actions,
            "dashboard_main_open",
            {},
            "Open Dashboard Main",
        ),
        "action-dashboard-player-open": (
            Actions,
            "dashboard_player_open",
            {},
            "Open Dashboard Player",
        ),
        "action-dashboard-metrics-open": (
            Actions,
            "dashboard_metrics_open",
            {},
            "Open Dashboard Metrics",
        ),
    }

    return cmds

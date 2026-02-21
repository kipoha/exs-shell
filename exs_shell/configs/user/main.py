from ignis.options_manager import OptionsGroup, TrackedList

from exs_shell.interfaces.schemas.widget.launcher import Action, PowerMenuAction
from exs_shell.utils.path import Paths


class UserConfig(OptionsGroup):
    avatar: str = ""
    command_prefix: str = ">"
    clock_format: str = "󰥔 %H:%M:%S"
    critical_percentage: int = 15
    terminal_format: str = "kitty %command%"

    actions: TrackedList[dict] = TrackedList()
    for i in [
        {
            "name": "Clipboard",
            "command": "",
            "icon": "clipboard-symbolic",
        },
        {
            "name": "Color Picker",
            "command": "hyprpicker -a | wl-copy",
            "icon": "palette-symbolic",
        },
        {
            "name": "Power Menu",
            "command": "",
            "icon": "system-shutdown-symbolic",
        }
    ]:
        actions.append(i)

    def get_actions_objs(self) -> list[Action]:
        return [Action(**i) for i in self.actions]

    powermenu_actions: TrackedList[dict] = TrackedList()
    for i in [
        {"name": "Lock", "command": "sleep 0.5 && hyprlock", "icon": "lock-symbolic"},
        {"name": "Exit", "command": "niri msg action quit --skip-confirmation", "icon": "exit-symbolic"},
        {"name": "Suspend", "command": "systemctl suspend", "icon": "system-suspend-symbolic"},
        {"name": "Reboot", "command": "systemctl reboot", "icon": "system-reboot-symbolic"},
        {"name": "Shutdown", "command": "systemctl poweroff", "icon": "system-shutdown-symbolic"},
    ]:
        powermenu_actions.append(i)

    def get_powermenu_actions_objs(self) -> list[PowerMenuAction]:
        return [PowerMenuAction(**i) for i in self.powermenu_actions]

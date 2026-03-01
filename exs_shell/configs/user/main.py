from ignis.options_manager import OptionsGroup, TrackedList

from exs_shell.interfaces.enums.icons import Icons
from exs_shell.interfaces.schemas import IdleAction
from exs_shell.interfaces.schemas.widget.launcher import Action, PowerMenuAction


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
            "icon": Icons.ui.CLIPBOARD,
        },
        {
            "name": "Color Picker",
            "command": "hyprpicker -a | wl-copy",
            "icon": Icons.ui.COLOR_PICKER,
        },
        {
            "name": "Power Menu",
            "command": "",
            "icon": Icons.ui.SYSTEM_POWER,
        },
    ]:
        actions.append(i)

    def get_actions_objs(self) -> list[Action]:
        return [Action(**i) for i in self.actions]

    powermenu_actions: TrackedList[dict] = TrackedList()
    for i in [
        {
            "name": "Lock",
            "command": "sleep 0.5 && hyprlock",
            "icon": Icons.ui.LOCK,
        },
        {
            "name": "Exit",
            "command": "niri msg action quit --skip-confirmation",
            "icon": Icons.ui.EXIT,
        },
        {
            "name": "Suspend",
            "command": "systemctl suspend",
            "icon": Icons.ui.SUSPEND,
        },
        {
            "name": "Reboot",
            "command": "systemctl reboot",
            "icon": Icons.ui.REBOOT,
        },
        {
            "name": "Shutdown",
            "command": "systemctl poweroff",
            "icon": Icons.ui.POWER,
        },
    ]:
        powermenu_actions.append(i)

    def get_powermenu_actions_objs(self) -> list[PowerMenuAction]:
        return [PowerMenuAction(**i) for i in self.powermenu_actions]

    idle_enable: bool = True
    idle_actions: TrackedList[dict] = TrackedList()
    for i in [
        {
            "timeout_seconds": 600,
            "on_timeout": "hyprlock",
            "on_resume": "notify-send -t 10000 'Niri' 'You have been woken up'",
        },
    ]:
        idle_actions.append(i)

    def get_idle_actions_objs(self) -> list[IdleAction]:
        return [IdleAction(**i) for i in self.idle_actions]

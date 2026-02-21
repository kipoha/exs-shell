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
            "name": "Lock",
            "command": "exs-ipc open-lockscreen",
            "icon": Paths.generate_path("icons/action/lock_screen.png", Paths.assets),
        },
        {
            "name": "Clipboard",
            "command": "exs-ipc toggle-clipboard",
            "icon": Paths.generate_path("icons/action/clipboard.png", Paths.assets),
        },
        {
            "name": "Color Picker",
            "command": "exs-ipc action-color-picker",
            "icon": Paths.generate_path("icons/action/color_picker.png", Paths.assets),
        },
    ]:
        actions.append(i)

    def get_actions_objs(self) -> list[Action]:
        return [Action(**i) for i in self.actions]

    powermenu_actions: TrackedList[dict] = TrackedList()
    for i in [
        {"name": "Lock", "command": "exs-ipc open-lockscreen", "icon": ""},
        {"name": "Exit", "command": "niri msg action quit --skip-confirmation", "icon": "󰈆"},
        {"name": "Suspend", "command": "systemctl suspend", "icon": "󰤄"},
        {"name": "Reboot", "command": "systemctl reboot", "icon": ""},
        {"name": "Shutdown", "command": "systemctl poweroff", "icon": "⏻"},
    ]:
        powermenu_actions.append(i)

    def get_powermenu_actions(self) -> list[PowerMenuAction]:
        return [PowerMenuAction(**i) for i in self.powermenu_actions]

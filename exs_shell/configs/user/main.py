from ignis.options_manager import OptionsGroup, TrackedList

from exs_shell.utils.path import Paths


class UserConfig(OptionsGroup):
    avatar: str = ""
    command_prefix: str = ">"
    clock_format: str = "󰥔 %H:%M:%S"

    actions: TrackedList[dict] = TrackedList()
    for i in [
        {
            "name": "Lock",
            "command": "exs-ipc open-lockscreen",
            "icon": Paths.generate_path(
                "icons/action/lock_screen.png", Paths.assets
            ),
        },
        {
            "name": "Clipboard",
            "command": "exs-ipc toggle-clipboard",
            "icon": Paths.generate_path("icons/action/clipboard.png", Paths.assets),
        },
        {
            "name": "Color Picker",
            "command": "exs-ipc action-color-picker",
            "icon": Paths.generate_path(
                "icons/action/color_picker.png", Paths.assets
            ),
        },
    ]:
        actions.append(i)

    powermenu_actions: TrackedList[dict] = TrackedList()
    for i in [
        {"command": "exs-ipc open-lockscreen", "icon": "", "in_lock": False},
        {
            "command": "niri msg action quit --skip-confirmation",
            "icon": "󰈆",
            "in_lock": False,
        },
        {"command": "systemctl suspend", "icon": "󰤄", "in_lock": True},
        {"command": "systemctl reboot", "icon": "", "in_lock": True},
        {"command": "systemctl poweroff", "icon": "⏻", "in_lock": True},
    ]:
        powermenu_actions.append(i)

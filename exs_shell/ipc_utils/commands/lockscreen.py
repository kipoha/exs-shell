from typing import Any, Generator

from ignis import utils
from ignis.window_manager import WindowManager

from exs_shell.config import config
from exs_shell.modules.lockscreen import LockScreen


class LockscreenCommands:
    @staticmethod
    def open_lockscreen():
        window_manager = WindowManager.get_default()
        lockscreens: Generator[LockScreen] = (
            window_manager.get_window(f"{config.NAMESPACE}_lockscreen_{i}")
            for i in range(utils.get_n_monitors())
        )
        for lockscreen in lockscreens:
            lockscreen.open()


def lockscreen_commands() -> dict[str, tuple[object, str, dict[str, Any], str]]:
    cmds: dict[str, tuple[object, str, dict[str, Any], str]] = {
        "open-lockscreen": (
            LockscreenCommands,
            "open_lockscreen",
            {},
            "Open Lockscreen",
        ),
    }

    return cmds

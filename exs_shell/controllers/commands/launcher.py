from exs_shell.utils import window
from exs_shell.interfaces.schemas.ipc.commands import Command


def include():
    launcher = window.get("launcher")
    commands = {
        "toggle-launcher": Command(
            call=launcher.set_visible,
            kwargs={"value": not launcher.visible},
            description="Toggle settings window",
        ),
    }
    return commands

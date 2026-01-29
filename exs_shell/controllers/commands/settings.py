from exs_shell.utils import window
from exs_shell.interfaces.schemes.ipc.commands import Command


def include():
    settings = window.get("settings")
    commands = {
        "toggle-settings": Command(
            call=settings.set_visible,
            kwargs={"value": not settings.visible},
            description="Toggle settings window",
        ),
    }
    return commands

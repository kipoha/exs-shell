from typing import Any


def clipboard_commands() -> dict[str, tuple[object, str, dict[str, Any], str]]:
    from exs_shell_deprecated.modules.clipboard import ClipboardManager

    clipboard = ClipboardManager.get_default()
    cmds: dict[str, tuple[object, str, dict[str, Any], str]] = {
        "toggle-clipboard": (clipboard, "toggle", {}, "Toggle Clipboard"),
    }

    return cmds

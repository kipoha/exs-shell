import subprocess

from exs_shell.interfaces.schemes.utils.clipboard import ClipboardItem


def get_clipboard_history(limit: int = 50) -> list[ClipboardItem]:
    result = subprocess.run(["cliphist", "list"], capture_output=True, text=True)
    if result.returncode != 0:
        return []

    lines = result.stdout.strip().split("\n")
    history = []
    for line in lines[:limit]:
        idx, raw = line.split("\t", 1)
        history.append(
            ClipboardItem(id=idx, raw=raw, is_binary="[[ binary data" in raw)
        )
    return history

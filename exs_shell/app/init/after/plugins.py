from pathlib import Path
from libexs.utils import plugin, send_notification

from exs_shell.configs.user import user


def init() -> None:
    for pl in user.plugins:
        try:
            plugin.load(Path(pl))
        except ValueError as e:
            send_notification("Error loading plugin", str(e))

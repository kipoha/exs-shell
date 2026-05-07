from libexs.utils import plugin, send_notification

from exs_shell.app.path import Dirs


def init() -> None:
    for pl in Dirs.PLUGINS_DIR.iterdir():
        try:
            plugin.load(pl)
        except ValueError as e:
            send_notification("Error loading plugin", str(e))

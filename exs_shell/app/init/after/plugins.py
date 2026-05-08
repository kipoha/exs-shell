from pathlib import Path
from libexs import State
from libexs.settings.base import BaseTab
from libexs.utils import plugin, send_notification

from exs_shell.configs.user import user


def init() -> None:
    for pl in user.plugins:
        try:
            plugin.load(Path(pl))
        except ValueError as e:
            send_notification("Error loading plugin", str(e))

    tab: BaseTab = State.plugin_tab
    for s in State.plugin_settings:
        tab.append(s)

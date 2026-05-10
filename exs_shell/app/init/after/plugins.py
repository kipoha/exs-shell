from pathlib import Path
from libexs import State
from libexs.exceptions.plugin import PluginLoadError
from libexs.settings.base import BaseTab
from libexs.utils import plugin, send_notification
from loguru import logger

from exs_shell.configs.user import user


def init() -> None:
    for pl in user.plugins:
        try:
            plugin.load(Path(pl))
        except PluginLoadError as e:
            send_notification("Error loading plugin", str(e))
        except Exception as e:
            logger.exception(e)

    tab: BaseTab = State.plugin_tab
    for s in State.plugin_settings:
        tab.append(s)

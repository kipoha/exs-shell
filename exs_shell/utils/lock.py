from ignis import utils
from ignis.window_manager import WindowManager

from exs_shell.config import config


def locked() -> bool:
    window_manager = WindowManager.get_default()
    lockscreens = (
        window_manager.get_window(f"{config.NAMESPACE}_lockscreen_{i}")
        for i in range(utils.get_n_monitors())
    )
    return any(w.visible for w in lockscreens)

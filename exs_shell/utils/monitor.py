import json
from gi.repository import Gdk  # type: ignore

from ignis.services.niri import NiriService
from ignis.utils import exec_sh, get_monitor, get_n_monitors, get_monitors

from exs_shell import register
from exs_shell.state import State

BASE_WIDTH = 1920
BASE_HEIGHT = 1080


def get_monitor_size(monitor_num: int) -> tuple[float, float]:
    monitor = get_monitor(monitor_num)
    geometry = monitor.get_geometry()  # type: ignore
    width, height = geometry.width, geometry.height
    return width, height


def get_monitor_scale(monitor_id: int) -> float:
    w, h = get_monitor_size(monitor_id)

    return min(w / BASE_WIDTH, h / BASE_HEIGHT)


def get_active_monitor() -> int:
    monitors = get_monitors()
    data = json.loads(exec_sh("niri msg --json focused-output").stdout)
    model = data["model"]
    monitor_id = 0
    for i, monitor in enumerate(monitors):
        if str(monitor.get_model()) == str(model):
            monitor_id = i
            break
    return monitor_id


def init_windows(cls: type) -> None:
    for i in range(get_n_monitors()):
        class_name = f"{cls.__name__}{i}"
        _c = type(class_name, (cls,), {})
        register.window(_c)
        _c(i)

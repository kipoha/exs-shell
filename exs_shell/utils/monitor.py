from ignis.utils import get_monitor

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

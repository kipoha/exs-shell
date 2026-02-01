from ignis.utils import get_monitor

def get_monitor_size(monitor_num: int) -> tuple[float, float]:
    monitor = get_monitor(monitor_num)
    geometry = monitor.get_geometry()  # type: ignore
    width, height = geometry.width, geometry.height
    return width, height

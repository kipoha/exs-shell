from ignis.options_manager import OptionsGroup, TrackedList


class Bar(OptionsGroup):
    position: str = "top"
    left: TrackedList[str] = TrackedList()
    left.extend(["tray"])
    left_spacing: int = 10
    center: TrackedList[str] = TrackedList()
    center.extend(["cava_tui"])
    center_spacing: int = 20
    right: TrackedList[str] = TrackedList()
    right.extend(["kb_layout", "battery", "clock"])
    right_spacing: int = 10

from ignis.options_manager import OptionsGroup, TrackedList


class Bar(OptionsGroup):
    position: str = "top"
    right: TrackedList[str] = TrackedList()
    right_spacing: int = 10
    center: TrackedList[str] = TrackedList()
    center_spacing: int = 20
    left: TrackedList[str] = TrackedList()
    left_spacing: int = 10

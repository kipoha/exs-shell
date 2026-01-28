from ignis.options_manager import OptionsGroup


class Notifications(OptionsGroup):
    dnd: bool = False
    popup_timeout: int = 5000
    max_popups_count: int = 3
    popup_position: str = "top"

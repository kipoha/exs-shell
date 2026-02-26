from ignis.options_manager import OptionsGroup

from exs_shell.interfaces.types import EntryPosition


class LockGroup(OptionsGroup):
    entry_visibility: bool = False
    entry_position: EntryPosition = "bottom"
    blur_radius: int = 10

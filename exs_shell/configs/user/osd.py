from ignis.options_manager import OptionsGroup

from exs_shell.interfaces.types import Arrow, OSD


class OSDGroup(OptionsGroup):
    position: Arrow = "bottom"
    osd: OSD = "arc"

from ignis.options_manager import OptionsGroup

from exs_shell.interfaces.enums.colorschemes import ColorSchemes
from exs_shell.utils.path import Paths


class Appearance(OptionsGroup):
    wallpaper_path: str = str(Paths.root / "default" / "default.png")
    wallpaper_dir: str | None = None
    scheme: str = ColorSchemes.TONAL_SPOT
    dark: bool = True
    contrast: int = 0

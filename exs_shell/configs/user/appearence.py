from ignis.options_manager import OptionsGroup

from exs_shell.interfaces.enums.colorschemes import ColorSchemes


class Appearance(OptionsGroup):
    wallpaper_path: str = ""
    wallpaper_dir: str | None = None
    scheme: str = ColorSchemes.TONAL_SPOT
    dark: bool = True
    contrast: int = 0

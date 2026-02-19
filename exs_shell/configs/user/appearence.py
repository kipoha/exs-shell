from materialyoucolor.scheme.variant import Variant

from ignis.options_manager import OptionsGroup

# from exs_shell.interfaces.enums.colorschemes import ColorSchemes2 as ColorSchemes


class Appearance(OptionsGroup):
    wallpaper_path: str = ""
    wallpaper_dir: str | None = None
    scheme_variant: str | Variant = Variant.CONTENT
    # scheme: str = ColorSchemes.TONAL_SPOT
    dark: bool = True
    contrast: float = 0

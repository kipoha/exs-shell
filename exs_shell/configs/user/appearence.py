from materialyoucolor.scheme.variant import Variant

from ignis.options_manager import OptionsGroup


class Appearance(OptionsGroup):
    wallpaper_path: str = ""
    wallpaper_dir: str | None = None
    scheme_variant: str | Variant = Variant.CONTENT
    dark: bool = True
    contrast: float = 0

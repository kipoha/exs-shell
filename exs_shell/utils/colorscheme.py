import json

from dataclasses import asdict

from PIL import Image

from materialyoucolor.hct import Hct
from materialyoucolor.utils.color_utils import argb_from_rgb

from exs_shell.utils.path import Paths
from exs_shell.configs.user import appearance
from exs_shell.interfaces.enums.colorschemes import ColorSchemeClasses, ColorSchemes
from exs_shell.interfaces.schemas.utils.colors import (
    GeneratedPreviewColors,
    GeneratedTheme,
    MaterialColors,
    ColorSchemeList,
)


def to_scss_color(val: int) -> str:
    a = (val >> 24) & 0xFF
    r = (val >> 16) & 0xFF
    g = (val >> 8) & 0xFF
    b = val & 0xFF

    if a == 255:
        return f"#{r:02X}{g:02X}{b:02X}"
    return f"rgba({r},{g},{b},{a / 255:.2f})"


def theme_to_scss(theme: MaterialColors) -> str:
    return "\n".join(f"${key}: {value};" for key, value in asdict(theme).items())


def preview_to_scss(scheme_list: dict[str, dict[str, str]]) -> str:
    return "\n".join(
        f"$palette_{scheme_name}_{k}: {v};"
        for scheme_name, colors in scheme_list.items()
        for k, v in colors.items()
    )


def generate(
    wallpaper_path: str | None = appearance.wallpaper_path,
    scheme: ColorSchemes = ColorSchemes(appearance.scheme_variant),
    dark: bool = True,
    contrast: float = 0.0,
) -> GeneratedTheme:
    if not wallpaper_path:
        default = json.loads((Paths.path / "colors.json").read_text())
        theme = MaterialColors(**default)
        return GeneratedTheme(
            colors=theme,
            scss=theme_to_scss(theme),
            scheme=scheme,
            seed_rgb=(0, 0, 0),
        )

    img = Image.open(wallpaper_path).convert("RGB")
    pixels = list(img.getdata())  # type: ignore

    r = sum(p[0] for p in pixels) // len(pixels)
    g = sum(p[1] for p in pixels) // len(pixels)
    b = sum(p[2] for p in pixels) // len(pixels)

    argb = argb_from_rgb(r, g, b)
    seed = Hct.from_int(argb)

    scheme_cls = ColorSchemeClasses.get(scheme)
    dyn_scheme = scheme_cls(seed, dark, contrast)  # type: ignore
    theme = MaterialColors.create(dyn_scheme, to_scss_color)

    return GeneratedTheme(
        colors=theme,
        scss=theme_to_scss(theme),
        scheme=scheme,
        seed_rgb=(r, g, b),
    )


def generate_color_preview(
    wallpaper_path: str = appearance.wallpaper_path,
    dark: bool = appearance.dark,
    contrast: float = appearance.contrast,
) -> str:
    img = Image.open(wallpaper_path).convert("RGB")
    pixels = list(img.getdata())  # type: ignore

    r = sum(p[0] for p in pixels) // len(pixels)
    g = sum(p[1] for p in pixels) // len(pixels)
    b = sum(p[2] for p in pixels) // len(pixels)

    argb = argb_from_rgb(r, g, b)
    colors = {}
    for scheme in ColorSchemeClasses:
        scheme_cls = ColorSchemeClasses.get(scheme.name.upper())
        dyn_scheme = scheme_cls(Hct.from_int(argb), dark, contrast)  # type: ignore
        theme = GeneratedPreviewColors.create(dyn_scheme, to_scss_color)
        colors[scheme.name.lower()] = theme

    scheme_list = ColorSchemeList(**colors)
    return preview_to_scss(scheme_list.asdict())

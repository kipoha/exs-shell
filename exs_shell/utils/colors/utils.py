# from PIL import Image
#
# from materialyoucolor.utils.color_utils import argb_from_rgb
# from materialyoucolor.hct.hct import Hct
# from materialyoucolor.scheme.variant import Variant
# from materialyoucolor.scheme.scheme_monochrome import SchemeMonochrome
# from materialyoucolor.scheme.scheme_tonal_spot import SchemeTonalSpot
# from materialyoucolor.scheme.scheme_vibrant import SchemeVibrant
# from materialyoucolor.scheme.scheme_expressive import SchemeExpressive
# from materialyoucolor.scheme.scheme_fidelity import SchemeFidelity
# from materialyoucolor.scheme.scheme_content import SchemeContent
# from materialyoucolor.scheme.scheme_rainbow import SchemeRainbow
# from materialyoucolor.scheme.scheme_fruit_salad import SchemeFruitSalad
#
# from exs_shell.config.user import options
#
#
# SCHEME_MAP = {
#     Variant.MONOCHROME: SchemeMonochrome,
#     Variant.TONAL_SPOT: SchemeTonalSpot,
#     Variant.VIBRANT: SchemeVibrant,
#     Variant.EXPRESSIVE: SchemeExpressive,
#     Variant.FIDELITY: SchemeFidelity,
#     Variant.CONTENT: SchemeContent,
#     Variant.RAINBOW: SchemeRainbow,
#     Variant.FRUIT_SALAD: SchemeFruitSalad,
# }
#
#
# def get_average_rgb(image_path: str):
#     img = Image.open(image_path).convert("RGB")
#     pixels = list(img.getdata())
#     r = sum(p[0] for p in pixels) // len(pixels)
#     g = sum(p[1] for p in pixels) // len(pixels)
#     b = sum(p[2] for p in pixels) // len(pixels)
#     return [r, g, b, 255]
#
#
# def to_scss_color(val) -> str:
#     if isinstance(val, int):
#         a = (val >> 24) & 0xFF
#         r = (val >> 16) & 0xFF
#         g = (val >> 8) & 0xFF
#         b = val & 0xFF
#         if a == 255:
#             return f"#{r:02X}{g:02X}{b:02X}"
#         else:
#             return f"rgba({r},{g},{b},{a / 255:.2f})"
#     if isinstance(val, (list, tuple)) and len(val) in (3, 4):
#         r, g, b = val[:3]
#         a = val[3] if len(val) == 4 else 255
#         if a == 255:
#             return f"#{r:02X}{g:02X}{b:02X}"
#         else:
#             return f"rgba({r},{g},{b},{a / 255:.2f})"
#     if isinstance(val, str):
#         return val
#     raise ValueError(f"Cannot convert {val} to SCSS color")
#
#
# def generate_theme(
#     *,
#     variant: str = Variant.CONTENT,
#     wallpaper_path: str | None = options.wallpaper.wallpaper_path,
#     is_dark: bool = True,
# ) -> tuple[dict | None, str | None]:
#     scss_text = None
#     theme_json = None
#     if wallpaper_path:
#         img = Image.open(wallpaper_path).convert("RGB")
#         pixels = list(img.getdata())
#
#         r = sum(p[0] for p in pixels) // len(pixels)
#         g = sum(p[1] for p in pixels) // len(pixels)
#         b = sum(p[2] for p in pixels) // len(pixels)
#         argb = argb_from_rgb(r, g, b)
#         seed_hct = Hct.from_int(argb)
#
#         scheme_cls = SCHEME_MAP[variant]
#         scheme = scheme_cls(
#             source_color_hct=seed_hct, is_dark=is_dark, contrast_level=0
#         )
#
#         theme_json = {
#             "bg": to_scss_color(scheme.neutral_palette.tone(20)),
#             "bg-light": to_scss_color(scheme.neutral_variant_palette.tone(30)),
#             "fg": to_scss_color(scheme.neutral_palette.tone(90)),
#             "active": to_scss_color(scheme.primary_palette.tone(50)),
#             "unactive": to_scss_color(scheme.secondary_palette.tone(50)),
#             "bg-dark": to_scss_color(scheme.neutral_palette.tone(10)),
#             "bg-darker": to_scss_color(scheme.neutral_palette.tone(5)),
#             "bg-lighter": to_scss_color(scheme.neutral_variant_palette.tone(95)),
#             "surface": to_scss_color(scheme.neutral_palette.tone(90)),
#             "surface-light": to_scss_color(scheme.neutral_variant_palette.tone(95)),
#             "fg-strong": "#ffffff",
#             "fg-muted": to_scss_color(scheme.neutral_variant_palette.tone(70)),
#             "fg-disabled": to_scss_color(scheme.neutral_variant_palette.tone(50)),
#             "accent": to_scss_color(scheme.primary_palette.tone(60)),
#             "accent-light": to_scss_color(scheme.primary_palette.tone(80)),
#             "accent-dark": to_scss_color(scheme.primary_palette.tone(40)),
#             "accent-muted": to_scss_color(scheme.secondary_palette.tone(50)),
#             "border": to_scss_color(scheme.neutral_variant_palette.tone(50)),
#             "border-light": to_scss_color(scheme.neutral_variant_palette.tone(70)),
#             "shadow": "rgba(0, 0, 0, 0.4)",
#             "success": "#6FCF97",
#             "warning": "#F2C94C",
#             "error": "#EB5757",
#             "info": "#2F80ED",
#         }
#
#         # theme_json = {
#         #     "bg": to_scss_color(scheme.neutral_palette.tone(10)),
#         #     "bg-light": to_scss_color(scheme.neutral_variant_palette.tone(20)),
#         #     "fg": to_scss_color(scheme.neutral_palette.tone(90)),
#         #     "active": to_scss_color(scheme.primary_palette.tone(40)),
#         #     "unactive": to_scss_color(scheme.secondary_palette.tone(40)),
#         #     "bg-dark": to_scss_color(scheme.neutral_palette.tone(5)),
#         #     "bg-darker": to_scss_color(scheme.neutral_palette.tone(0)),
#         #     "bg-lighter": to_scss_color(scheme.neutral_variant_palette.tone(95)),
#         #     "surface": to_scss_color(scheme.neutral_palette.tone(95)),
#         #     "surface-light": to_scss_color(scheme.neutral_variant_palette.tone(90)),
#         #     "fg-strong": "#ffffff",
#         #     "fg-muted": to_scss_color(scheme.neutral_variant_palette.tone(60)),
#         #     "fg-disabled": to_scss_color(scheme.neutral_variant_palette.tone(50)),
#         #     "accent": to_scss_color(scheme.primary_palette.tone(40)),
#         #     "accent-light": to_scss_color(scheme.primary_palette.tone(80)),
#         #     "accent-dark": to_scss_color(scheme.primary_palette.tone(20)),
#         #     "accent-muted": to_scss_color(scheme.secondary_palette.tone(40)),
#         #     "border": to_scss_color(scheme.neutral_variant_palette.tone(30)),
#         #     "border-light": to_scss_color(scheme.neutral_variant_palette.tone(50)),
#         #     "shadow": "rgba(0, 0, 0, 0.4)",
#         #     "success": "#a3f7b5",
#         #     "warning": "#f7e3a3",
#         #     "error": "#f28b82",
#         #     "info": "#a3d9f7",
#         # }
#
#         scss_text = "\n".join(
#             [f"${k}: {to_scss_color(v)};" for k, v in theme_json.items()]
#         )
#
#     return theme_json, scss_text


import json
from dataclasses import asdict
from PIL import Image
from typing import Any

from materialyoucolor.scheme import Scheme
from materialyoucolor.scheme.variant import Variant
from materialyoucolor.scheme.dynamic_scheme import DynamicScheme, DynamicSchemeOptions
from materialyoucolor.scheme.scheme_android import SchemeAndroid
from materialyoucolor.scheme.scheme_content import SchemeContent
from materialyoucolor.scheme.scheme_expressive import SchemeExpressive
from materialyoucolor.scheme.scheme_fidelity import SchemeFidelity
from materialyoucolor.scheme.scheme_fruit_salad import SchemeFruitSalad
from materialyoucolor.scheme.scheme_monochrome import SchemeMonochrome
from materialyoucolor.scheme.scheme_neutral import SchemeNeutral
from materialyoucolor.scheme.scheme_rainbow import SchemeRainbow
from materialyoucolor.scheme.scheme_tonal_spot import SchemeTonalSpot
from materialyoucolor.scheme.scheme_vibrant import SchemeVibrant

# from materialyoucolor.utils.color_utils import argb_from_rgba
# from materialyoucolor.palettes.core_palette import CorePalette

from exs_shell.configs.user import options
from exs_shell.interfaces.schemes.utils.colors import ThemeColors
from exs_shell.utils.path import Paths


def generate_theme(
    wallpaper_path: str | None = options.wallpaper.wallpaper_path,
) -> tuple[ThemeColors, str]:
    def generate_scss_text(scheme: dict[str, Any]) -> str:
        return "\n".join(f"${k}: {v};" for k, v in scheme.items())

    if wallpaper_path:
        img = Image.open(wallpaper_path).convert("RGB")
        pixels = list(img.getdata())  # type: ignore

        r = sum(p[0] for p in pixels) // len(pixels)
        g = sum(p[1] for p in pixels) // len(pixels)
        b = sum(p[2] for p in pixels) // len(pixels)
        seed_rgb = [r, g, b, 255]

        scheme: Any = Scheme.dark_from_rgb(seed_rgb)

        def to_scss_color(val) -> str:
            if isinstance(val, int):
                a = (val >> 24) & 0xFF
                r = (val >> 16) & 0xFF
                g = (val >> 8) & 0xFF
                b = val & 0xFF
                if a == 255:
                    return f"#{r:02X}{g:02X}{b:02X}"
                else:
                    return f"rgba({r},{g},{b},{a / 255:.2f})"

            if isinstance(val, (list, tuple)) and len(val) in (3, 4):
                r, g, b = val[:3]
                a = val[3] if len(val) == 4 else 255
                if a == 255:
                    return f"#{r:02X}{g:02X}{b:02X}"
                else:
                    return f"rgba({r},{g},{b},{a / 255:.2f})"

            if isinstance(val, str):
                return val

            raise ValueError(f"Cannot convert {val} to SCSS color")

        theme = ThemeColors(
            bg=to_scss_color(scheme.background),
            bg_light=to_scss_color(scheme.surfaceVariant),
            fg=to_scss_color(scheme.onSurface),
            active=to_scss_color(scheme.primary),
            unactive=to_scss_color(scheme.secondary),
            bg_dark=to_scss_color(scheme.surface),
            bg_darker=to_scss_color(scheme.background),
            bg_lighter=to_scss_color(scheme.surfaceVariant),
            surface=to_scss_color(scheme.surface),
            surface_light=to_scss_color(scheme.surfaceVariant),
            fg_strong="#ffffff",
            fg_muted=to_scss_color(scheme.onSurfaceVariant),
            fg_disabled=to_scss_color(scheme.onSurfaceVariant),
            accent=to_scss_color(scheme.primary),
            accent_light=to_scss_color(scheme.primaryContainer),
            accent_dark=to_scss_color(scheme.primary),
            accent_muted=to_scss_color(scheme.secondary),
            border=to_scss_color(scheme.outline),
            border_light=to_scss_color(scheme.outlineVariant),
            shadow="rgba(0, 0, 0, 0.4)",
        )
    else:
        default_colors_file = Paths.path / "colors.json"
        default_colors_dict = json.loads(default_colors_file.read_text())
        theme = ThemeColors(**default_colors_dict)

    theme_dict = asdict(theme)
    scss_text = generate_scss_text(theme_dict)

    return theme, scss_text
